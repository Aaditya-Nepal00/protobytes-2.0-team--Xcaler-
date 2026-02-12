from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app import db
from app.models.forum import DiscussionThread, ThreadComment, ThreadVote
from app.models.user import User
import uuid
import random

forum_bp = Blueprint('forum', __name__)


# ==================== THREADS ====================

@forum_bp.route('/threads', methods=['GET'])
def get_threads():
    """Get all threads with sorting and filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    sort = request.args.get('sort', 'hot')  # hot, new, top, controversial
    category = request.args.get('category', None)

    query = DiscussionThread.query.filter_by(is_deleted=False)

    if category:
        query = query.filter_by(category=category)

    if sort == 'new':
        query = query.order_by(DiscussionThread.created_at.desc())
    elif sort == 'top':
        query = query.order_by(
            (DiscussionThread.upvotes - DiscussionThread.downvotes).desc()
        )
    elif sort == 'controversial':
        query = query.order_by(DiscussionThread.downvotes.desc())
    else:  # hot (default) - combination of votes and recency
        query = query.order_by(
            DiscussionThread.is_pinned.desc(),
            (DiscussionThread.upvotes - DiscussionThread.downvotes + DiscussionThread.comment_count).desc(),
            DiscussionThread.created_at.desc()
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Check if user is logged in and get their votes
    user_votes = {}
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            votes = ThreadVote.query.filter(
                ThreadVote.user_id == user_id,
                ThreadVote.thread_id.isnot(None)
            ).all()
            user_votes = {v.thread_id: v.vote_type for v in votes}
    except Exception:
        pass

    threads = []
    for thread in pagination.items:
        t = thread.to_dict(include_content=False)
        t['user_vote'] = user_votes.get(thread.id, None)
        threads.append(t)

    return jsonify({
        'threads': threads,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
    }), 200


@forum_bp.route('/threads/<thread_id>', methods=['GET'])
def get_thread(thread_id):
    """Get a single thread with comments"""
    thread = DiscussionThread.query.get(thread_id)

    if not thread or thread.is_deleted:
        return jsonify({'error': 'Thread not found'}), 404

    # Increment view count
    thread.view_count += 1
    db.session.commit()

    data = thread.to_dict()

    # Get top-level comments
    comments = ThreadComment.query.filter_by(
        thread_id=thread_id, parent_id=None, is_deleted=False
    ).order_by(
        (ThreadComment.upvotes - ThreadComment.downvotes).desc(),
        ThreadComment.created_at.asc()
    ).all()

    data['comments'] = [c.to_dict() for c in comments]

    # Check user's vote
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            vote = ThreadVote.query.filter_by(
                user_id=user_id, thread_id=thread_id
            ).first()
            data['user_vote'] = vote.vote_type if vote else None

            # Also get user's votes on comments
            comment_votes = ThreadVote.query.filter(
                ThreadVote.user_id == user_id,
                ThreadVote.comment_id.isnot(None)
            ).all()
            data['user_comment_votes'] = {v.comment_id: v.vote_type for v in comment_votes}
        else:
            data['user_vote'] = None
            data['user_comment_votes'] = {}
    except Exception:
        data['user_vote'] = None
        data['user_comment_votes'] = {}

    return jsonify(data), 200


@forum_bp.route('/threads', methods=['POST'])
@jwt_required()
def create_thread():
    """Create a new discussion thread"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    is_anonymous = data.get('is_anonymous', False)
    anonymous_name = None
    if is_anonymous:
        anonymous_name = f"Anonymous Citizen #{random.randint(1000, 9999)}"

    thread = DiscussionThread(
        id=str(uuid.uuid4()),
        title=title,
        content=content,
        author_id=user_id,
        is_anonymous=is_anonymous,
        anonymous_name=anonymous_name,
        category=data.get('category', 'general'),
        tags=','.join(data.get('tags', [])) if data.get('tags') else None,
    )

    db.session.add(thread)
    db.session.commit()

    return jsonify({
        'message': 'Thread created successfully',
        'thread': thread.to_dict()
    }), 201


@forum_bp.route('/threads/<thread_id>', methods=['PUT'])
@jwt_required()
def update_thread(thread_id):
    """Update a thread (author only)"""
    user_id = get_jwt_identity()
    thread = DiscussionThread.query.get(thread_id)

    if not thread or thread.is_deleted:
        return jsonify({'error': 'Thread not found'}), 404

    if thread.author_id != user_id:
        return jsonify({'error': 'You can only edit your own threads'}), 403

    data = request.json
    if data.get('title'):
        thread.title = data['title'].strip()
    if data.get('content'):
        thread.content = data['content'].strip()
    if data.get('category'):
        thread.category = data['category']

    db.session.commit()

    return jsonify({
        'message': 'Thread updated',
        'thread': thread.to_dict()
    }), 200


@forum_bp.route('/threads/<thread_id>', methods=['DELETE'])
@jwt_required()
def delete_thread(thread_id):
    """Soft delete a thread (author or admin)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    thread = DiscussionThread.query.get(thread_id)

    if not thread:
        return jsonify({'error': 'Thread not found'}), 404

    if thread.author_id != user_id and user.role != 'admin':
        return jsonify({'error': 'Not authorized'}), 403

    thread.is_deleted = True
    db.session.commit()

    return jsonify({'message': 'Thread deleted'}), 200


# ==================== COMMENTS ====================

@forum_bp.route('/threads/<thread_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(thread_id):
    """Add a comment to a thread"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    thread = DiscussionThread.query.get(thread_id)

    if not thread or thread.is_deleted:
        return jsonify({'error': 'Thread not found'}), 404

    if thread.is_locked:
        return jsonify({'error': 'This thread is locked'}), 403

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    content = data.get('content', '').strip()
    if not content:
        return jsonify({'error': 'Comment content is required'}), 400

    is_anonymous = data.get('is_anonymous', False)
    anonymous_name = None
    if is_anonymous:
        anonymous_name = f"Anonymous Citizen #{random.randint(1000, 9999)}"

    comment = ThreadComment(
        id=str(uuid.uuid4()),
        thread_id=thread_id,
        parent_id=data.get('parent_id', None),
        content=content,
        author_id=user_id,
        is_anonymous=is_anonymous,
        anonymous_name=anonymous_name,
    )

    # Update thread comment count
    thread.comment_count += 1

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        'message': 'Comment added',
        'comment': comment.to_dict()
    }), 201


@forum_bp.route('/comments/<comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    """Update a comment (author only)"""
    user_id = get_jwt_identity()
    comment = ThreadComment.query.get(comment_id)

    if not comment or comment.is_deleted:
        return jsonify({'error': 'Comment not found'}), 404

    if comment.author_id != user_id:
        return jsonify({'error': 'You can only edit your own comments'}), 403

    data = request.json
    if data.get('content'):
        comment.content = data['content'].strip()

    db.session.commit()

    return jsonify({
        'message': 'Comment updated',
        'comment': comment.to_dict()
    }), 200


@forum_bp.route('/comments/<comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """Soft delete a comment"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    comment = ThreadComment.query.get(comment_id)

    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    if comment.author_id != user_id and user.role != 'admin':
        return jsonify({'error': 'Not authorized'}), 403

    comment.is_deleted = True

    # Update thread comment count
    thread = DiscussionThread.query.get(comment.thread_id)
    if thread:
        thread.comment_count = max(0, thread.comment_count - 1)

    db.session.commit()

    return jsonify({'message': 'Comment deleted'}), 200


# ==================== VOTING ====================

@forum_bp.route('/threads/<thread_id>/vote', methods=['POST'])
@jwt_required()
def vote_thread(thread_id):
    """Upvote or downvote a thread"""
    user_id = get_jwt_identity()
    thread = DiscussionThread.query.get(thread_id)

    if not thread or thread.is_deleted:
        return jsonify({'error': 'Thread not found'}), 404

    data = request.json
    vote_type = data.get('vote_type')  # 'upvote' or 'downvote'

    if vote_type not in ('upvote', 'downvote'):
        return jsonify({'error': 'Invalid vote type. Use upvote or downvote'}), 400

    existing_vote = ThreadVote.query.filter_by(
        user_id=user_id, thread_id=thread_id
    ).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote (toggle off)
            if vote_type == 'upvote':
                thread.upvotes = max(0, thread.upvotes - 1)
            else:
                thread.downvotes = max(0, thread.downvotes - 1)

            # Update author karma
            if thread.author_id:
                author = User.query.get(thread.author_id)
                if author:
                    if vote_type == 'upvote':
                        author.karma = max(0, author.karma - 1)
                    else:
                        author.karma += 1

            db.session.delete(existing_vote)
            db.session.commit()

            return jsonify({
                'message': 'Vote removed',
                'upvotes': thread.upvotes,
                'downvotes': thread.downvotes,
                'score': thread.score,
                'user_vote': None
            }), 200
        else:
            # Change vote
            if existing_vote.vote_type == 'upvote':
                thread.upvotes = max(0, thread.upvotes - 1)
                thread.downvotes += 1
            else:
                thread.downvotes = max(0, thread.downvotes - 1)
                thread.upvotes += 1

            # Update karma
            if thread.author_id:
                author = User.query.get(thread.author_id)
                if author:
                    if vote_type == 'upvote':
                        author.karma += 2  # reverse downvote + add upvote
                    else:
                        author.karma = max(0, author.karma - 2)

            existing_vote.vote_type = vote_type
            db.session.commit()

            return jsonify({
                'message': 'Vote changed',
                'upvotes': thread.upvotes,
                'downvotes': thread.downvotes,
                'score': thread.score,
                'user_vote': vote_type
            }), 200
    else:
        # New vote
        vote = ThreadVote(
            id=str(uuid.uuid4()),
            user_id=user_id,
            thread_id=thread_id,
            vote_type=vote_type,
        )

        if vote_type == 'upvote':
            thread.upvotes += 1
        else:
            thread.downvotes += 1

        # Update author karma
        if thread.author_id:
            author = User.query.get(thread.author_id)
            if author:
                if vote_type == 'upvote':
                    author.karma += 1
                else:
                    author.karma = max(0, author.karma - 1)

        db.session.add(vote)
        db.session.commit()

        return jsonify({
            'message': 'Vote recorded',
            'upvotes': thread.upvotes,
            'downvotes': thread.downvotes,
            'score': thread.score,
            'user_vote': vote_type
        }), 200


@forum_bp.route('/comments/<comment_id>/vote', methods=['POST'])
@jwt_required()
def vote_comment(comment_id):
    """Upvote or downvote a comment"""
    user_id = get_jwt_identity()
    comment = ThreadComment.query.get(comment_id)

    if not comment or comment.is_deleted:
        return jsonify({'error': 'Comment not found'}), 404

    data = request.json
    vote_type = data.get('vote_type')

    if vote_type not in ('upvote', 'downvote'):
        return jsonify({'error': 'Invalid vote type'}), 400

    existing_vote = ThreadVote.query.filter_by(
        user_id=user_id, comment_id=comment_id
    ).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Toggle off
            if vote_type == 'upvote':
                comment.upvotes = max(0, comment.upvotes - 1)
            else:
                comment.downvotes = max(0, comment.downvotes - 1)
            db.session.delete(existing_vote)
            db.session.commit()
            return jsonify({
                'message': 'Vote removed',
                'upvotes': comment.upvotes,
                'downvotes': comment.downvotes,
                'score': comment.score,
                'user_vote': None
            }), 200
        else:
            # Change vote
            if existing_vote.vote_type == 'upvote':
                comment.upvotes = max(0, comment.upvotes - 1)
                comment.downvotes += 1
            else:
                comment.downvotes = max(0, comment.downvotes - 1)
                comment.upvotes += 1
            existing_vote.vote_type = vote_type
            db.session.commit()
            return jsonify({
                'message': 'Vote changed',
                'upvotes': comment.upvotes,
                'downvotes': comment.downvotes,
                'score': comment.score,
                'user_vote': vote_type
            }), 200
    else:
        vote = ThreadVote(
            id=str(uuid.uuid4()),
            user_id=user_id,
            comment_id=comment_id,
            vote_type=vote_type,
        )
        if vote_type == 'upvote':
            comment.upvotes += 1
        else:
            comment.downvotes += 1

        db.session.add(vote)
        db.session.commit()
        return jsonify({
            'message': 'Vote recorded',
            'upvotes': comment.upvotes,
            'downvotes': comment.downvotes,
            'score': comment.score,
            'user_vote': vote_type
        }), 200


# ==================== CATEGORIES ====================

@forum_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get available forum categories"""
    categories = [
        {'id': 'governance', 'name': 'Governance', 'icon': '🏛️', 'description': 'General governance discussions'},
        {'id': 'corruption', 'name': 'Corruption', 'icon': '🔍', 'description': 'Discuss corruption issues'},
        {'id': 'budget', 'name': 'Budget', 'icon': '💰', 'description': 'Budget and spending transparency'},
        {'id': 'law', 'name': 'Law & Policy', 'icon': '⚖️', 'description': 'Legal discussions'},
        {'id': 'development', 'name': 'Development', 'icon': '🏗️', 'description': 'Infrastructure and development projects'},
        {'id': 'education', 'name': 'Education', 'icon': '📚', 'description': 'Education policy and issues'},
        {'id': 'health', 'name': 'Health', 'icon': '🏥', 'description': 'Healthcare discussions'},
        {'id': 'general', 'name': 'General', 'icon': '💬', 'description': 'General community discussions'},
    ]
    return jsonify(categories), 200
