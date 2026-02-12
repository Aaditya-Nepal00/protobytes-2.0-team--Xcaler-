import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.tender import Tender, TenderBid
from app.models.budget import Budget
from app.models.corruption_report import CorruptionReport
from app.models.law import Law
from app.models.forum import DiscussionThread, ThreadComment, ThreadVote
from app.models.news import NewsArticle
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import uuid
import random

app = create_app('development')


def seed_users():
    """Create demo users"""
    users = [
        {'name': 'Admin User', 'email': 'admin@sachet.np', 'role': 'admin', 'karma': 500},
        {'name': 'Ram Shrestha', 'email': 'ram@example.com', 'role': 'user', 'karma': 120},
        {'name': 'Sita Gurung', 'email': 'sita@example.com', 'role': 'user', 'karma': 85},
        {'name': 'Hari Thapa', 'email': 'hari@example.com', 'role': 'user', 'karma': 200},
        {'name': 'Gita Maharjan', 'email': 'gita@example.com', 'role': 'user', 'karma': 45},
        {'name': 'Krishna Lama', 'email': 'krishna@example.com', 'role': 'user', 'karma': 310},
        {'name': 'Sarita Tamang', 'email': 'sarita@example.com', 'role': 'moderator', 'karma': 150},
        {'name': 'Binod KC', 'email': 'binod@example.com', 'role': 'user', 'karma': 60},
        {'name': 'Anita Poudel', 'email': 'anita@example.com', 'role': 'user', 'karma': 95},
        {'name': 'Demo User', 'email': 'demo@sachet.np', 'role': 'user', 'karma': 10},
    ]

    created = []
    for u in users:
        user = User(
            id=str(uuid.uuid4()),
            name=u['name'],
            email=u['email'],
            password=generate_password_hash('Xcaler009'),
            role=u['role'],
            karma=u['karma'],
        )
        db.session.add(user)
        created.append(user)

    db.session.commit()
    print(f"  ✓ Created {len(created)} users")
    return created


def seed_projects():
    """Create mock government projects"""
    projects_data = [
        {'title': 'Kathmandu-Terai Fast Track Road', 'description': 'A 76km expressway connecting Kathmandu with Nijgadh in the Terai plains, reducing travel time from 6 hours to 1 hour.', 'status': 'ongoing', 'budget': 1500000000, 'spent': 680000000, 'completion_percentage': 42, 'location': 'Kathmandu-Makwanpur', 'district': 'Makwanpur', 'province': 'Bagmati', 'department': 'Department of Roads', 'contractor': 'China Railway 15th Bureau Group', 'category': 'infrastructure', 'latitude': 27.6, 'longitude': 85.2},
        {'title': 'Melamchi Water Supply Project', 'description': 'Bringing water from Melamchi River to Kathmandu Valley to solve chronic water shortage.', 'status': 'completed', 'budget': 3500000000, 'spent': 3200000000, 'completion_percentage': 100, 'location': 'Sindhupalchok-Kathmandu', 'district': 'Sindhupalchok', 'province': 'Bagmati', 'department': 'Melamchi Water Supply Board', 'contractor': 'CMC di Ravenna', 'category': 'water', 'latitude': 27.85, 'longitude': 85.55},
        {'title': 'Pokhara International Airport', 'description': 'New international airport in Pokhara to boost tourism and regional connectivity.', 'status': 'completed', 'budget': 2200000000, 'spent': 2200000000, 'completion_percentage': 100, 'location': 'Pokhara', 'district': 'Kaski', 'province': 'Gandaki', 'department': 'Civil Aviation Authority', 'contractor': 'China CAMC Engineering Co.', 'category': 'infrastructure', 'latitude': 28.2, 'longitude': 83.98},
        {'title': 'Upper Tamakoshi Hydropower Project', 'description': '456 MW hydropower project, largest domestic hydropower plant in Nepal.', 'status': 'completed', 'budget': 4500000000, 'spent': 4100000000, 'completion_percentage': 100, 'location': 'Dolakha', 'district': 'Dolakha', 'province': 'Bagmati', 'department': 'Upper Tamakoshi Hydropower Ltd.', 'contractor': 'Sino Hydro Corporation', 'category': 'energy', 'latitude': 27.85, 'longitude': 86.15},
        {'title': 'Gautam Buddha International Airport', 'description': 'International airport in Bhairahawa to serve Buddhist pilgrimage tourism.', 'status': 'delayed', 'budget': 1800000000, 'spent': 1400000000, 'completion_percentage': 78, 'location': 'Bhairahawa', 'district': 'Rupandehi', 'province': 'Lumbini', 'department': 'Civil Aviation Authority', 'contractor': 'Northwest Civil Aviation Construction', 'category': 'infrastructure', 'latitude': 27.5, 'longitude': 83.42},
        {'title': 'Nagdhunga Tunnel Project', 'description': '2.68 km road tunnel to ease traffic congestion on Prithvi Highway near Kathmandu.', 'status': 'ongoing', 'budget': 1600000000, 'spent': 720000000, 'completion_percentage': 55, 'location': 'Kathmandu-Dhading', 'district': 'Kathmandu', 'province': 'Bagmati', 'department': 'Department of Roads', 'contractor': 'Hazama Ando Corporation', 'category': 'infrastructure', 'latitude': 27.72, 'longitude': 85.2},
        {'title': 'Pushpalal (Mid-Hill) Highway', 'description': 'East-west highway through the mid-hills of Nepal, connecting Chiyo Bhanjyang to Jhulaghat.', 'status': 'ongoing', 'budget': 5000000000, 'spent': 1250000000, 'completion_percentage': 28, 'location': 'Mid-Hills (East-West)', 'district': 'Multiple', 'province': 'Multiple', 'department': 'Department of Roads', 'contractor': 'Various Contractors', 'category': 'infrastructure', 'latitude': 28.0, 'longitude': 84.0},
        {'title': 'Motipur Community Health Center', 'description': 'Construction of a 30-bed community health center serving rural Dhanusha district.', 'status': 'ongoing', 'budget': 180000000, 'spent': 95000000, 'completion_percentage': 60, 'location': 'Motipur', 'district': 'Dhanusha', 'province': 'Madhesh', 'department': 'Ministry of Health', 'contractor': 'Nepal Construction Pvt. Ltd.', 'category': 'health', 'latitude': 26.85, 'longitude': 85.9},
        {'title': 'Surkhet-Jumla Road Upgrade', 'description': 'Upgrading road from Surkhet to Jumla to all-weather blacktopped road.', 'status': 'delayed', 'budget': 800000000, 'spent': 280000000, 'completion_percentage': 30, 'location': 'Surkhet-Jumla', 'district': 'Jumla', 'province': 'Karnali', 'department': 'Department of Roads', 'contractor': 'Kalika Construction', 'category': 'infrastructure', 'latitude': 29.27, 'longitude': 82.18},
        {'title': 'Dharan Sub-Metropolitan Digital City', 'description': 'Smart city initiative implementing digital infrastructure, free wifi, and e-governance.', 'status': 'ongoing', 'budget': 250000000, 'spent': 45000000, 'completion_percentage': 15, 'location': 'Dharan', 'district': 'Sunsari', 'province': 'Koshi', 'department': 'Ministry of Communications', 'contractor': 'Subisu Cablenet', 'category': 'technology', 'latitude': 26.81, 'longitude': 87.28},
        {'title': 'Postal Highway (Hulaki Rajmarg)', 'description': 'East-west highway through the southern Terai plains of Nepal.', 'status': 'ongoing', 'budget': 3200000000, 'spent': 1800000000, 'completion_percentage': 65, 'location': 'Terai (East-West)', 'district': 'Multiple', 'province': 'Multiple', 'department': 'Department of Roads', 'contractor': 'Various', 'category': 'infrastructure', 'latitude': 26.8, 'longitude': 85.5},
        {'title': 'Budhigandaki Hydropower Project', 'description': '1200 MW storage-type hydropower project on Budhi Gandaki River.', 'status': 'delayed', 'budget': 25000000000, 'spent': 2500000000, 'completion_percentage': 8, 'location': 'Gorkha-Dhading', 'district': 'Gorkha', 'province': 'Gandaki', 'department': 'Budhigandaki Hydropower Project', 'contractor': 'China Gezhouba Group', 'category': 'energy', 'latitude': 28.1, 'longitude': 84.7},
        {'title': 'Bhaktapur Hospital Expansion', 'description': 'Expansion of Bhaktapur Hospital from 100 to 300 beds with modern equipment.', 'status': 'ongoing', 'budget': 450000000, 'spent': 180000000, 'completion_percentage': 40, 'location': 'Bhaktapur', 'district': 'Bhaktapur', 'province': 'Bagmati', 'department': 'Ministry of Health', 'contractor': 'Sharma Construction', 'category': 'health', 'latitude': 27.67, 'longitude': 85.43},
        {'title': 'Janakpur Smart City Project', 'description': 'Developing Janakpur as a smart heritage city with improved infrastructure and tourism facilities.', 'status': 'ongoing', 'budget': 550000000, 'spent': 120000000, 'completion_percentage': 20, 'location': 'Janakpur', 'district': 'Dhanusha', 'province': 'Madhesh', 'department': 'Ministry of Urban Development', 'contractor': 'Multiple', 'category': 'development', 'latitude': 26.73, 'longitude': 85.92},
        {'title': 'Bardibas-Sindhuli Road Improvement', 'description': 'Widening and blacktopping of the Bardibas-Sindhuli road section.', 'status': 'completed', 'budget': 320000000, 'spent': 310000000, 'completion_percentage': 100, 'location': 'Bardibas-Sindhuli', 'district': 'Sindhuli', 'province': 'Bagmati', 'department': 'Department of Roads', 'contractor': 'Lumbini Construction', 'category': 'infrastructure', 'latitude': 27.1, 'longitude': 85.9},
        {'title': 'Karnali Province University', 'description': 'Establishment of a new provincial university in Karnali Province.', 'status': 'ongoing', 'budget': 600000000, 'spent': 85000000, 'completion_percentage': 12, 'location': 'Birendranagar', 'district': 'Surkhet', 'province': 'Karnali', 'department': 'Ministry of Education', 'contractor': 'Nepal Engineering Consultancy', 'category': 'education', 'latitude': 28.6, 'longitude': 81.63},
        {'title': 'Integrated Check Post - Birgunj', 'description': 'Modernized cross-border check post at Birgunj-Raxaul border point.', 'status': 'completed', 'budget': 260000000, 'spent': 255000000, 'completion_percentage': 100, 'location': 'Birgunj', 'district': 'Parsa', 'province': 'Madhesh', 'department': 'Ministry of Commerce', 'contractor': 'IRCON International', 'category': 'infrastructure', 'latitude': 27.01, 'longitude': 84.88},
        {'title': 'Irrigation Canal Renovation - Sarlahi', 'description': 'Renovation of 45km irrigation canal network serving 5000 hectares of farmland.', 'status': 'delayed', 'budget': 150000000, 'spent': 42000000, 'completion_percentage': 25, 'location': 'Sarlahi', 'district': 'Sarlahi', 'province': 'Madhesh', 'department': 'Department of Irrigation', 'contractor': 'Terai Construction', 'category': 'agriculture', 'latitude': 26.95, 'longitude': 85.6},
        {'title': 'Solar Power Plant - Dang', 'description': '25MW solar power plant in Dang valley to promote renewable energy.', 'status': 'inactive', 'budget': 380000000, 'spent': 0, 'completion_percentage': 0, 'location': 'Dang', 'district': 'Dang', 'province': 'Lumbini', 'department': 'Nepal Electricity Authority', 'contractor': 'TBD', 'category': 'energy', 'latitude': 28.08, 'longitude': 82.3},
        {'title': 'Chitwan National Park Visitor Center', 'description': 'Modern eco-visitor center with digital exhibits about biodiversity conservation.', 'status': 'completed', 'budget': 85000000, 'spent': 82000000, 'completion_percentage': 100, 'location': 'Chitwan', 'district': 'Chitwan', 'province': 'Bagmati', 'department': 'Department of National Parks', 'contractor': 'Green Build Nepal', 'category': 'tourism', 'latitude': 27.5, 'longitude': 84.35},
    ]

    for i, p in enumerate(projects_data):
        days_ago = random.randint(30, 900)
        project = Project(
            id=str(uuid.uuid4()),
            title=p['title'],
            description=p['description'],
            status=p['status'],
            budget=p['budget'],
            spent=p['spent'],
            completion_percentage=p['completion_percentage'],
            location=p['location'],
            district=p['district'],
            province=p['province'],
            department=p['department'],
            contractor=p['contractor'],
            category=p['category'],
            latitude=p['latitude'],
            longitude=p['longitude'],
            start_date=datetime.utcnow() - timedelta(days=days_ago),
            expected_end_date=datetime.utcnow() + timedelta(days=random.randint(30, 730)),
        )
        if p['status'] == 'completed':
            project.end_date = datetime.utcnow() - timedelta(days=random.randint(1, 60))
        db.session.add(project)

    db.session.commit()
    print(f"  ✓ Created {len(projects_data)} projects")


def seed_tenders():
    """Create mock tenders with bids"""
    tenders_data = [
        {'title': 'Construction of Bridge over Bagmati River at Thapathali', 'org': 'Department of Roads', 'budget': 450000000, 'status': 'awarded', 'category': 'infrastructure', 'location': 'Kathmandu', 'district': 'Kathmandu'},
        {'title': 'Supply of Medical Equipment for Bir Hospital', 'org': 'Ministry of Health', 'budget': 120000000, 'status': 'open', 'category': 'health', 'location': 'Kathmandu', 'district': 'Kathmandu'},
        {'title': 'Road Blacktopping - Pokhara Ring Road Phase 2', 'org': 'Pokhara Metropolitan', 'budget': 280000000, 'status': 'closed', 'category': 'infrastructure', 'location': 'Pokhara', 'district': 'Kaski'},
        {'title': 'School Building Construction - Dolpa', 'org': 'Ministry of Education', 'budget': 35000000, 'status': 'open', 'category': 'education', 'location': 'Dolpa', 'district': 'Dolpa'},
        {'title': 'IT Infrastructure for e-Governance System', 'org': 'Ministry of Communications', 'budget': 85000000, 'status': 'awarded', 'category': 'technology', 'location': 'Kathmandu', 'district': 'Kathmandu'},
        {'title': 'Waste Management System - Biratnagar', 'org': 'Biratnagar Metropolitan', 'budget': 65000000, 'status': 'open', 'category': 'environment', 'location': 'Biratnagar', 'district': 'Morang'},
        {'title': 'Drinking Water Pipeline - Dhangadhi', 'org': 'Water Supply Board', 'budget': 180000000, 'status': 'closed', 'category': 'water', 'location': 'Dhangadhi', 'district': 'Kailali'},
        {'title': 'Street Light Installation - Lalitpur', 'org': 'Lalitpur Metropolitan', 'budget': 25000000, 'status': 'awarded', 'category': 'infrastructure', 'location': 'Lalitpur', 'district': 'Lalitpur'},
        {'title': 'Agricultural Research Lab Construction', 'org': 'Nepal Agricultural Research Council', 'budget': 95000000, 'status': 'open', 'category': 'agriculture', 'location': 'Chitwan', 'district': 'Chitwan'},
        {'title': 'Emergency Vehicle Procurement - Nepal Police', 'org': 'Nepal Police HQ', 'budget': 200000000, 'status': 'closed', 'category': 'security', 'location': 'Kathmandu', 'district': 'Kathmandu'},
    ]

    bidder_names = [
        'Himalayan Construction Pvt. Ltd.', 'Nepal Infrastructure Corp.',
        'Sagarmatha Builders', 'Everest Engineering Co.', 'Lumbini Contractors',
        'Kantipur Construction', 'Terai Developers Pvt. Ltd.',
        'Mountain Tech Solutions', 'Gorkha Construction Co.', 'Valley Infrastructure'
    ]

    for t in tenders_data:
        days_ago = random.randint(5, 120)
        tender = Tender(
            id=str(uuid.uuid4()),
            title=t['title'],
            description=f"Procurement notice for {t['title']}. Published by {t['org']}.",
            organization=t['org'],
            budget=t['budget'],
            status=t['status'],
            category=t['category'],
            location=t['location'],
            district=t['district'],
            published_date=datetime.utcnow() - timedelta(days=days_ago),
            deadline=datetime.utcnow() + timedelta(days=random.randint(10, 60)) if t['status'] == 'open' else datetime.utcnow() - timedelta(days=random.randint(1, 30)),
        )
        if t['status'] == 'awarded':
            tender.awarded_to = random.choice(bidder_names)
            tender.awarded_amount = t['budget'] * random.uniform(0.85, 1.05)
        db.session.add(tender)
        db.session.flush()

        # Add bids
        num_bids = random.randint(2, 5)
        for _ in range(num_bids):
            bid = TenderBid(
                id=str(uuid.uuid4()),
                tender_id=tender.id,
                bidder_name=random.choice(bidder_names),
                bid_amount=t['budget'] * random.uniform(0.85, 1.15),
                technical_score=random.uniform(60, 95),
                financial_score=random.uniform(65, 98),
                status='awarded' if tender.awarded_to and _ == 0 else random.choice(['submitted', 'evaluated', 'rejected']),
            )
            db.session.add(bid)

    db.session.commit()
    print(f"  ✓ Created {len(tenders_data)} tenders with bids")


def seed_budgets():
    """Create mock budget data"""
    sectors_data = {
        'Education': {'ministry': 'Ministry of Education, Science & Technology', 'allocated': 195000000000},
        'Health': {'ministry': 'Ministry of Health and Population', 'allocated': 115000000000},
        'Infrastructure': {'ministry': 'Ministry of Physical Infrastructure', 'allocated': 175000000000},
        'Agriculture': {'ministry': 'Ministry of Agriculture & Livestock', 'allocated': 45000000000},
        'Defense': {'ministry': 'Ministry of Defence', 'allocated': 55000000000},
        'Energy': {'ministry': 'Ministry of Energy, Water Resources', 'allocated': 68000000000},
        'Tourism': {'ministry': 'Ministry of Culture, Tourism & Civil Aviation', 'allocated': 12000000000},
        'Technology': {'ministry': 'Ministry of Communications & IT', 'allocated': 8500000000},
        'Environment': {'ministry': 'Ministry of Forests and Environment', 'allocated': 15000000000},
        'Social Welfare': {'ministry': 'Ministry of Women, Children & Social Welfare', 'allocated': 32000000000},
    }

    fiscal_years = ['2079/80', '2080/81', '2081/82']

    for fy in fiscal_years:
        for sector, data in sectors_data.items():
            multiplier = 1.0 if fy == '2080/81' else (0.88 if fy == '2079/80' else 1.12)
            allocated = data['allocated'] * multiplier
            spent_ratio = random.uniform(0.45, 0.92) if fy != '2081/82' else random.uniform(0.15, 0.45)
            budget = Budget(
                id=str(uuid.uuid4()),
                fiscal_year=fy,
                ministry=data['ministry'],
                sector=sector,
                allocated=allocated,
                released=allocated * random.uniform(0.7, 0.95),
                spent=allocated * spent_ratio,
                level='federal',
                province=None,
            )
            db.session.add(budget)

    db.session.commit()
    print(f"  ✓ Created {len(sectors_data) * len(fiscal_years)} budget entries")


def seed_corruption_reports():
    """Create mock corruption reports"""
    reports_data = [
        {'title': 'Overpriced road construction materials in Kavre', 'description': 'The contractor is using substandard materials while billing for premium quality. The road surface started cracking within 2 months of construction. Cost inflation estimated at 40%.', 'department': 'Department of Roads', 'district': 'Kavrepalanchok', 'province': 'Bagmati', 'category': 'fraud', 'severity': 'high', 'status': 'investigating', 'amount': 25000000},
        {'title': 'Ghost teachers drawing salary in Bajura', 'description': 'Multiple teachers registered in government schools in Bajura district who never show up to teach. Local community confirms the positions exist only on paper.', 'department': 'Ministry of Education', 'district': 'Bajura', 'province': 'Sudurpashchim', 'category': 'embezzlement', 'severity': 'high', 'status': 'under_review', 'amount': 8400000},
        {'title': 'Bribery in land registration office Chitwan', 'description': 'Officials requiring unofficial payments of NPR 5000-20000 for processing land registration documents. Delays of 2-3 months if bribes not paid.', 'department': 'Department of Land Management', 'district': 'Chitwan', 'province': 'Bagmati', 'category': 'bribery', 'severity': 'medium', 'status': 'submitted'},
        {'title': 'Tender bid manipulation in Butwal municipality', 'description': 'Tender for waste management awarded to company owned by a council member relative. Other qualified bidders mysteriously disqualified on technicalities.', 'department': 'Butwal Sub-Metropolitan', 'district': 'Rupandehi', 'province': 'Lumbini', 'category': 'nepotism', 'severity': 'high', 'status': 'investigating', 'amount': 45000000},
        {'title': 'Medical supply overcharging at Dharan Hospital', 'description': 'Hospital procurement office purchasing medical supplies at 3x market rate. Suspected kickback scheme between procurement officer and supplier.', 'department': 'Ministry of Health', 'district': 'Sunsari', 'province': 'Koshi', 'category': 'fraud', 'severity': 'critical', 'status': 'under_review', 'amount': 12000000},
        {'title': 'Misuse of earthquake reconstruction funds in Gorkha', 'description': 'Reconstruction funds allocated for 200 homes diverted. Only 80 homes actually reconstructed while money for 120 homes unaccounted for.', 'department': 'National Reconstruction Authority', 'district': 'Gorkha', 'province': 'Gandaki', 'category': 'embezzlement', 'severity': 'critical', 'status': 'resolved', 'amount': 60000000},
        {'title': 'Fake beneficiaries in social security allowance', 'description': 'Dead and migrated residents still receiving elderly allowance in Dhanusha. Estimated 300+ fake beneficiaries.', 'department': 'Ministry of Home Affairs', 'district': 'Dhanusha', 'province': 'Madhesh', 'category': 'fraud', 'severity': 'medium', 'status': 'investigating', 'amount': 3600000},
        {'title': 'Irregularities in school bus procurement Lalitpur', 'description': 'School buses procured at costs significantly above market price. Vehicles appear to be refurbished sold as new.', 'department': 'Ministry of Education', 'district': 'Lalitpur', 'province': 'Bagmati', 'category': 'fraud', 'severity': 'medium', 'status': 'submitted', 'amount': 15000000},
        {'title': 'Revenue leakage at customs - Tatopani', 'description': 'Under-invoicing of imported goods going unchecked. Customs officials suspected of accepting payments to lower declared values.', 'department': 'Department of Customs', 'district': 'Sindhupalchok', 'province': 'Bagmati', 'category': 'bribery', 'severity': 'high', 'status': 'under_review', 'amount': 80000000},
        {'title': 'Water supply project fund mismanagement in Jumla', 'description': 'A completed water supply project on paper but non-functional pipes installed. Local residents still without clean water despite project marked as completed.', 'department': 'Water Supply Board', 'district': 'Jumla', 'province': 'Karnali', 'category': 'embezzlement', 'severity': 'high', 'status': 'submitted', 'amount': 18000000},
    ]

    for r in reports_data:
        report = CorruptionReport(
            id=str(uuid.uuid4()),
            tracking_id=CorruptionReport.generate_tracking_id(),
            title=r['title'],
            description=r['description'],
            department=r['department'],
            district=r['district'],
            province=r['province'],
            category=r['category'],
            severity=r['severity'],
            status=r['status'],
            anonymous=True,
            amount_involved=r.get('amount'),
            date_of_incident=datetime.utcnow() - timedelta(days=random.randint(10, 180)),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 90)),
        )
        db.session.add(report)

    db.session.commit()
    print(f"  ✓ Created {len(reports_data)} corruption reports")


def seed_laws():
    """Create mock Nepali law entries"""
    laws_data = [
        {'title': 'Constitution of Nepal, 2072', 'title_np': 'नेपालको संविधान, २०७२', 'category': 'constitutional', 'year': 2015, 'simplified': 'The supreme law of Nepal establishing it as a federal democratic republic. It guarantees fundamental rights including right to equality, freedom, property, religion, and social justice. It divides Nepal into 7 provinces and establishes three tiers of government: federal, provincial, and local.', 'tags': 'constitution,fundamental rights,federal,republic'},
        {'title': 'Right to Information Act, 2064', 'title_np': 'सूचनाको हक सम्बन्धी ऐन, २०६४', 'category': 'civil', 'year': 2007, 'simplified': 'Every citizen has the right to ask for and receive information from government bodies. Government offices must proactively publish their activities, budgets, and decisions. If information is denied, citizens can appeal to the National Information Commission.', 'tags': 'information,transparency,government,RTI'},
        {'title': 'Anti-Corruption Act, 2059', 'title_np': 'भ्रष्टाचार निवारण ऐन, २०५९', 'category': 'criminal', 'year': 2002, 'simplified': 'Makes corruption by public officials a punishable offense. Covers bribery, embezzlement, abuse of authority, and amassing disproportionate property. The CIAA (Commission for Investigation of Abuse of Authority) is the main body investigating corruption cases.', 'tags': 'corruption,bribery,CIAA,punishment'},
        {'title': 'Public Procurement Act, 2063', 'title_np': 'सार्वजनिक खरिद ऐन, २०६३', 'category': 'administrative', 'year': 2007, 'simplified': 'Governs how the government buys goods, constructs projects, and hires services. All procurement above a threshold must go through competitive bidding. The law aims to ensure transparency, fairness, and value for money in government spending.', 'tags': 'procurement,tender,bidding,government spending'},
        {'title': 'Local Government Operation Act, 2074', 'title_np': 'स्थानीय सरकार सञ्चालन ऐन, २०७४', 'category': 'administrative', 'year': 2017, 'simplified': 'Defines how local governments (municipalities and rural municipalities) function. Local governments can make their own laws, collect taxes, manage local infrastructure, education, and health services. They must publish their budget and activities publicly.', 'tags': 'local government,municipality,decentralization'},
        {'title': 'Cyber Crime and Computer Related Act, 2075', 'title_np': 'साइबर अपराध र कम्प्युटर सम्बन्धी ऐन, २०७५', 'category': 'criminal', 'year': 2018, 'simplified': 'Addresses crimes committed using computers and the internet. Covers hacking, data theft, cyber fraud, identity theft, and online harassment. Penalties range from fines to imprisonment depending on the severity of the offense.', 'tags': 'cybercrime,internet,hacking,digital,privacy'},
        {'title': 'Labor Act, 2074', 'title_np': 'श्रम ऐन, २०७४', 'category': 'civil', 'year': 2017, 'simplified': 'Protects workers rights in Nepal. Employers must provide fair wages, safe working conditions, and social security benefits. Workers can form unions. Limits working hours to 8 per day and 48 per week. Provides for overtime pay and annual leave.', 'tags': 'labor,employment,workers rights,wages'},
        {'title': 'Consumer Protection Act, 2075', 'title_np': 'उपभोक्ता संरक्षण ऐन, २०७५', 'category': 'civil', 'year': 2018, 'simplified': 'Protects consumers from unfair trade practices, false advertising, and unsafe products. Consumers can file complaints against businesses for defective products or poor services. Establishes consumer courts for dispute resolution.', 'tags': 'consumer,protection,trade,complaint'},
        {'title': 'Environment Protection Act, 2076', 'title_np': 'वातावरण संरक्षण ऐन, २०७६', 'category': 'environmental', 'year': 2019, 'simplified': 'Mandates environmental impact assessments for development projects. Polluters must pay for environmental damage. Prohibits activities harming national parks and protected areas. Promotes clean energy and sustainable development practices.', 'tags': 'environment,pollution,conservation,EIA'},
        {'title': 'Good Governance Act, 2064', 'title_np': 'सुशासन ऐन, २०६४', 'category': 'administrative', 'year': 2008, 'simplified': 'Government officials must be transparent, accountable, and responsive. Public services must be delivered within specified timeframes. Citizens can file complaints against officials who delay or deny services without valid reason.', 'tags': 'governance,accountability,transparency,public service'},
    ]

    for l in laws_data:
        law = Law(
            id=str(uuid.uuid4()),
            title=l['title'],
            title_nepali=l['title_np'],
            simplified=l['simplified'],
            category=l['category'],
            year_enacted=l['year'],
            tags=l['tags'],
            content=l['simplified'],
            source='Nepal Law Commission',
        )
        db.session.add(law)

    db.session.commit()
    print(f"  ✓ Created {len(laws_data)} laws")


def seed_forum(users):
    """Create mock forum threads and comments"""
    threads_data = [
        {'title': 'Why are most road projects always delayed?', 'content': 'I have been observing that almost every road construction project in Nepal faces significant delays. The Kathmandu-Terai Fast Track was supposed to be completed years ago. What are the systemic issues causing this? Is it corruption, poor planning, or lack of skilled contractors?', 'category': 'development', 'upvotes': 45, 'downvotes': 3, 'views': 320},
        {'title': 'Melamchi Water Supply - Finally working?', 'content': 'After decades of delays and billions spent, Melamchi water is finally reaching Kathmandu taps. But the quality seems inconsistent across different areas. Anyone else noticing this? Also, the per-unit cost for consumers seems high considering the massive investment.', 'category': 'governance', 'upvotes': 38, 'downvotes': 5, 'views': 250},
        {'title': 'Digital Nepal Framework - Progress or just talk?', 'content': 'The government announced the Digital Nepal Framework in 2019. Its been years - what progress has actually been made? E-governance services are still slow and unreliable. Most government offices still require physical documents and in-person visits.', 'category': 'governance', 'upvotes': 52, 'downvotes': 8, 'views': 410},
        {'title': 'Budget allocation for education is not reaching schools', 'content': 'Despite government data showing increased education budget, many public schools in rural areas still lack basic facilities. Books arrive 3 months into the school year, teacher positions remain vacant for years. Where is the money actually going?', 'category': 'budget', 'upvotes': 61, 'downvotes': 2, 'views': 580},
        {'title': 'How to effectively report corruption without fear?', 'content': 'I want to report a case of bribery at my local land revenue office, but I am afraid of consequences. What protections exist for whistleblowers in Nepal? Has anyone successfully reported corruption through official channels?', 'category': 'corruption', 'upvotes': 89, 'downvotes': 4, 'views': 890},
        {'title': 'New Anti-Money Laundering Act - What does it mean for citizens?', 'content': 'The recent amendments to anti-money laundering laws have changed reporting thresholds. Can someone explain in simple terms what this means for regular citizens and small businesses? The legal text is very confusing.', 'category': 'law', 'upvotes': 34, 'downvotes': 1, 'views': 195},
        {'title': 'Provincial government spending transparency - any improvements?', 'content': 'Since the federalization, provincial governments received significant budgets but transparency has been questionable. Has anyone tried to access provincial budget data? I find it nearly impossible to get detailed spending information from Bagmati Province offices.', 'category': 'budget', 'upvotes': 42, 'downvotes': 6, 'views': 320},
        {'title': 'Health infrastructure in Karnali - still neglected?', 'content': 'Living in Humla, the nearest hospital with proper facilities is days away. Despite government promises of improved health infrastructure in Karnali Province, we still have to travel to Nepalgunj or Kathmandu for serious medical issues. When will this change?', 'category': 'development', 'upvotes': 73, 'downvotes': 1, 'views': 520},
        {'title': 'Tender process needs major reform', 'content': 'The current tender process is rigged in favor of large contractors with political connections. Small local companies cant compete even when they offer better value. The evaluation criteria often seem designed to exclude newcomers. We need transparency in how bids are evaluated.', 'category': 'corruption', 'upvotes': 56, 'downvotes': 12, 'views': 400},
        {'title': 'Success story: Our ward got a new school building!', 'content': 'Wanted to share a positive story! After years of advocacy, our ward in Sindhupalchok finally got a new earthquake-resistant school building. The construction was completed on time and within budget. It IS possible when local leaders are committed and citizens stay vigilant!', 'category': 'development', 'upvotes': 125, 'downvotes': 2, 'views': 780},
        {'title': 'Understanding the new tax reform bill', 'content': 'The government recently introduced changes to the income tax slabs. Can someone break down what this means for salaried employees vs business owners? The finance minister\'s explanation was full of jargon.', 'category': 'law', 'upvotes': 28, 'downvotes': 3, 'views': 165},
        {'title': 'Pollution in Bagmati River - Who is accountable?', 'content': 'Despite the Bagmati cleanup campaign, factories along the river continue to dump waste. The monitoring seems non-existent. Who is responsible for enforcement and why are violators not being prosecuted?', 'category': 'governance', 'upvotes': 67, 'downvotes': 5, 'views': 450},
    ]

    comments_pool = [
        "This is a really important issue. I've seen the same problems in my district too.",
        "The government needs to be held accountable. We deserve better.",
        "I think the root cause is lack of proper monitoring. Contracts are awarded and then nobody checks progress.",
        "As someone who works in government, I can say the bureaucracy is a major bottleneck. Too many approvals needed.",
        "Has anyone tried filing an RTI request? I got some interesting data when I did.",
        "This is exactly why platforms like Sachet are needed. Transparency is the first step.",
        "I disagree somewhat - progress is being made, just slowly. Rome wasn't built in a day.",
        "The political interference in technical decisions is the biggest problem in my opinion.",
        "Can we organize a community meeting to discuss this further?",
        "Great post! Sharing this with my network.",
        "Same situation in Province 2. The hospitals are understaffed and under-resourced.",
        "I reported a similar issue to CIAA last year. Still waiting for any response...",
        "The new digital payment systems at least are working well in Kathmandu. Hope it expands soon.",
        "We should demand quarterly progress reports from all government projects above 10 crore.",
        "My village still doesn't have reliable internet. How can we participate in digital governance?",
        "Local government elections made a difference in our area. Active ward chairperson matters a lot.",
        "Thank you for raising this. Most people don't realize how much public money is wasted.",
        "I'm a journalist working on a story about this. Would appreciate if anyone can provide more details.",
    ]

    created_threads = []
    for t in threads_data:
        is_anon = random.random() < 0.3
        author = random.choice(users)
        thread = DiscussionThread(
            id=str(uuid.uuid4()),
            title=t['title'],
            content=t['content'],
            author_id=author.id,
            is_anonymous=is_anon,
            anonymous_name=f"Anonymous Citizen #{random.randint(1000, 9999)}" if is_anon else None,
            category=t['category'],
            upvotes=t['upvotes'],
            downvotes=t['downvotes'],
            view_count=t['views'],
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 60), hours=random.randint(0, 23)),
        )

        # Add comments
        num_comments = random.randint(3, 8)
        thread.comment_count = num_comments
        db.session.add(thread)
        db.session.flush()

        for j in range(num_comments):
            is_comment_anon = random.random() < 0.25
            comment_author = random.choice(users)
            comment = ThreadComment(
                id=str(uuid.uuid4()),
                thread_id=thread.id,
                content=random.choice(comments_pool),
                author_id=comment_author.id,
                is_anonymous=is_comment_anon,
                anonymous_name=f"Anonymous Citizen #{random.randint(1000, 9999)}" if is_comment_anon else None,
                upvotes=random.randint(0, 25),
                downvotes=random.randint(0, 5),
                created_at=thread.created_at + timedelta(hours=random.randint(1, 72)),
            )
            db.session.add(comment)

        created_threads.append(thread)

    db.session.commit()
    print(f"  ✓ Created {len(threads_data)} forum threads with comments")
    return created_threads


def seed_news():
    """Create mock news articles"""
    news_data = [
        {'title': 'Government Approves NPR 1.86 Trillion Budget for FY 2081/82', 'summary': 'The government has approved a budget of NPR 1.86 trillion for fiscal year 2081/82, with major allocations to infrastructure, education, and health sectors.', 'category': 'budget', 'source': 'Kathmandu Post'},
        {'title': 'Anti-Corruption Commission Files Cases Against 12 Officials', 'summary': 'CIAA has filed corruption cases against 12 government officials accused of embezzlement and bribery across 5 districts.', 'category': 'corruption', 'source': 'Republica'},
        {'title': 'Fast Track Road Project Reaches 42% Completion', 'summary': 'The Kathmandu-Terai Fast Track road project has reached 42% completion with Chinese contractor accelerating work.', 'category': 'development', 'source': 'The Himalayan Times'},
        {'title': 'Digital Payment Transactions Increase by 300% in Nepal', 'summary': 'Nepal sees massive growth in digital payments as more citizens adopt mobile banking and QR payments for daily transactions.', 'category': 'governance', 'source': 'Naya Patrika'},
        {'title': 'Supreme Court Orders Government to Protect River Systems', 'summary': 'The Supreme Court has issued a landmark order requiring the government to prevent industrial pollution in all major rivers.', 'category': 'governance', 'source': 'Kantipur'},
        {'title': 'Province Governments Struggle with Budget Utilization', 'summary': 'Provincial governments spent only 47% of allocated budget in FY 2080/81, raising concerns about capacity and planning.', 'category': 'budget', 'source': 'Online Khabar'},
    ]

    for n in news_data:
        article = NewsArticle(
            id=str(uuid.uuid4()),
            title=n['title'],
            content=n['summary'],
            summary=n['summary'],
            source=n['source'],
            category=n['category'],
            published_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            is_featured=random.random() < 0.3,
        )
        db.session.add(article)

    db.session.commit()
    print(f"  ✓ Created {len(news_data)} news articles")


def run_seed():
    """Run all seeders"""
    with app.app_context():
        print("\n🌱 Seeding Sachet Database...\n")

        # Drop and recreate all tables
        print("  Dropping existing tables...")
        db.drop_all()
        print("  Creating fresh tables...")
        db.create_all()

        # Seed data
        users = seed_users()
        seed_projects()
        seed_tenders()
        seed_budgets()
        seed_corruption_reports()
        seed_laws()
        seed_forum(users)
        seed_news()

        print(f"\n✅ Database seeded successfully!")
        print(f"\n📋 Demo Credentials:")
        print(f"   Admin: admin@sachet.np / Xcaler009")
        print(f"   User:  demo@sachet.np / Xcaler009")
        print()


if __name__ == '__main__':
    run_seed()
