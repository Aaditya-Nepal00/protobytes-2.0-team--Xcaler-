def format_date(date_obj):
    """Format date object"""
    return date_obj.strftime('%Y-%m-%d') if date_obj else None

def paginate(query, page=1, per_page=20):
    """Paginate query results"""
    return query.paginate(page=page, per_page=per_page)

def success_response(data, message='Success', status_code=200):
    """Return success response"""
    return {'success': True, 'data': data, 'message': message}, status_code

def error_response(message='Error', status_code=400):
    """Return error response"""
    return {'success': False, 'message': message}, status_code
