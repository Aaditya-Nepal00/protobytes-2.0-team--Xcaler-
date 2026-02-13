import sys
import os
import uuid
import random
from datetime import datetime, timedelta
import bcrypt

# Add the parent directory to sys.path to import the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import (User, Project, Tender, Budget, CorruptionReport, Law, 
                        DiscussionThread, ThreadComment, ThreadVote)

def seed_data():
    app = create_app('development')
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        print("🌱 Seeding a MASSIVE amount of RICH localized data...")

        # 1. Create Users
        password_hash = bcrypt.hashpw("Password123!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        users = []
        demo_user = User(id=str(uuid.uuid4()), email="demo@sachet.np", password=password_hash, name="Aaditya Nepal", role="citizen", karma=500)
        db.session.add(demo_user)
        users.append(demo_user)

        first_names = ["Ram", "Sita", "Hari", "Gita", "Bijay", "Anjali", "Suresh", "Maya", "Kiran", "Samir", "Deepa", "Arjun", "Pooja", "Bikesh", "Sunita"]
        last_names = ["Sharma", "Thapa", "Adhikari", "Gurung", "Rai", "Shrestha", "Maharjan", "Lama", "Poudel", "Sherpa"]

        for i in range(20):
            u = User(id=str(uuid.uuid4()), email=f"citizen{i}@sachet.np", password=password_hash, 
                     name=f"{random.choice(first_names)} {random.choice(last_names)}", role="citizen", karma=random.randint(50, 800))
            users.append(u)
            db.session.add(u)

        # 2. RICH Project Data
        project_data = [
            {
                "title": "Kathmandu-Terai Fast Track (Expressway)",
                "status": "ongoing", "budget": 175e9, "lat": 27.6, "lng": 85.3, "cat": "Infrastructure", "dept": "Nepal Army / MoPIT",
                "contractor": "Poly Changda Engineering Co. Ltd",
                "desc": "A 72.5 km expressway connecting Kathmandu and Nijgadh. This project will reduce travel time to under an hour. It includes 87 bridges and 3 tunnels. Currently, sub-grade works are 70% complete in multiple segments. Challenges include complex geological terrain in Makwanpur district."
            },
            {
                "title": "Melamchi Water Supply Project - Phase 2",
                "status": "ongoing", "budget": 35e9, "lat": 27.8, "lng": 85.5, "cat": "Water", "dept": "Melamchi Water Supply Dev Board",
                "contractor": "Sino Hydro Corporation",
                "desc": "Expansion project to bring additional 340 million liters of water daily from Yangri and Larke rivers. Phase 1 tunnels are completed but Headworks rectification is ongoing due to 2021 flood damage. Focus is now on building permanent disaster-resilient headworks structure."
            },
            {
                "title": "Upper Tamakoshi Hydropower (456MW)",
                "status": "completed", "budget": 85e9, "lat": 27.9, "lng": 86.2, "cat": "Energy", "dept": "Nepal Electricity Authority",
                "contractor": "Sinohydro / Andritz Hydro",
                "desc": "Nepal's largest national pride hydropower project. It has significantly eliminated load-shedding and turned Nepal into an energy exporter. Located in Dolakha, it features 6 vertical pelton turbines and a 19km headrace tunnel."
            },
            {
                "title": "Nagdhunga-Naubise Tunnel Project",
                "status": "ongoing", "budget": 22e9, "lat": 27.7, "lng": 85.2, "cat": "Infrastructure", "dept": "Department of Roads",
                "contractor": "Hazama Ando Corporation (Japan)",
                "desc": "Nepal's first modern traffic tunnel. Total length is 2.68 km. It aims to eliminate the congestion at Nagdhunga pass. Tunnel breakthrough has been achieved, and interior works like lighting, ventilation, and road paving are nearing completion."
            },
            {
                "title": "Pokhara International Airport",
                "status": "completed", "budget": 22e9, "lat": 28.2, "lng": 83.9, "cat": "Aviation", "dept": "Civil Aviation Authority (CAAN)",
                "contractor": "CAMC Engineering",
                "desc": "The second international airport in Nepal. Features a 2500m runway capable of handling Boeing 737 and Airbus A320 aircraft. It aims to boost tourism in the Pokhara valley and Western Nepal."
            }
        ]

        for p in project_data:
            proj = Project(
                id=str(uuid.uuid4()), title=p['title'], status=p['status'], budget=p['budget'],
                latitude=p['lat'], longitude=p['lng'], category=p['cat'], department=p['dept'],
                description=p['desc'], contractor=p['contractor'], 
                spent=p['budget'] * random.uniform(0.3, 0.9),
                completion_percentage=random.randint(40, 95) if p['status'] == 'ongoing' else 100,
                start_date=datetime.now() - timedelta(days=random.randint(365, 1000)),
                expected_end_date=datetime.now() + timedelta(days=random.randint(100, 500)) if p['status'] == 'ongoing' else None
            )
            db.session.add(proj)

        # 3. RICH Tender Data
        tender_data = [
            {
                "title": "Construction of 4-Lane Bridge over Bagmati River",
                "org": "Department of Roads (DOR)", "budget": 150e6, "status": "active",
                "desc": "Bids are invited for the construction of a 120m pre-stressed box girder bridge. Technical requirements include previous experience in bridge construction over 100m. Design-build model preferred.",
                "cat": "Infrastructure", "loc": "Kathmandu/Lalitpur Border"
            },
            {
                "title": "Supply and Delivery of 50 Electric Public Buses",
                "org": "Sajha Yatayat", "budget": 450e6, "status": "awarded",
                "desc": "Awarded for the procurement of 50 eco-friendly electric buses to improve public transport in Kathmandu valley. Contract includes 5 years of maintenance and setting up 5 charging stations.",
                "awarded_to": "BYD Auto Industry Co.", "awarded_amount": 420e6
            },
            {
                "title": "Digitization of Land Ownership Records (Saptari)",
                "org": "Department of Land Reform", "budget": 25e6, "status": "active",
                "desc": "Scanning, indexing, and data entry of historical land records into the central LMBIS system. Bidder must have ISO 27001 certification for data security.",
                "cat": "IT/Services", "loc": "Saptari District"
            },
            {
                "title": "National Hydrology Information System Upgrade",
                "org": "DHM", "budget": 80e6, "status": "open",
                "desc": "Installation of 100 automatic weather stations with real-time satellite transmission capability. Project funded by World Bank under 'Building Resilience to Climate Related Hazards'.",
                "cat": "Environment", "loc": "Multiple Districts"
            }
        ]

        for t in tender_data:
            tend = Tender(
                id=str(uuid.uuid4()), title=t['title'], organization=t['org'], 
                budget=t.get('budget', 0), status=t['status'],
                description=t['desc'], category=t.get('cat', 'General'),
                location=t.get('loc', 'Nepal'),
                awarded_to=t.get('awarded_to'), awarded_amount=t.get('awarded_amount'),
                deadline=datetime.now() + timedelta(days=random.randint(10, 60)),
                published_date=datetime.now() - timedelta(days=random.randint(1, 10))
            )
            db.session.add(tend)

        # 4. Budget Data
        sectors = ["Education", "Health", "Energy", "Infrastructure", "Tourism"]
        for s in sectors:
            amt = random.randint(10, 50) * 1e9
            db.session.add(Budget(id=str(uuid.uuid4()), fiscal_year="2080/81", ministry=f"Ministry of {s}", sector=s.lower(), allocated=amt, released=amt*0.8, spent=amt*0.6))

        # 5. Law Data
        law_data = [
            ("Muluki Aparadh Sanhita, 2074", "Criminal Code", "Simplified punishments for crimes like theft, fraud, and assault. Theft can lead to 3 years in prison."),
            ("Right to Information (RTI) Act, 2064", "Civil Rights", "Empowers citizens to request information from public bodies. They must respond within 15 days."),
            ("Anti-Corruption Act, 2059", "Governance", "Strict laws against bribery and embezzlement. Covers both public officials and private sector bribes."),
            ("Electronic Transactions Act, 2063", "Cyber Law", "Covers cybercrimes like hacking, online fraud, and social media harassment.")
        ]
        for title, cat, simplified in law_data:
            db.session.add(Law(id=str(uuid.uuid4()), title=title, category=cat, simplified=simplified, content=f"Full legal text for {title}..."))

        # 6. Forum Data (THREADS & COMMENTS with VOTES)
        forum_topics = [
            ("Bribe requested at Ward 4, Lalitpur", "corruption", "I went for land registration and the assistant clerk hinted at a 'speed fee' of Rs 5000."),
            ("Why is the Fast Track taking decades?", "development", "It's a national pride project, yet progress seems stalled in Makwanpur."),
            ("Report: Substandard material in Koteshwor Road", "corruption", "The blacktopping done just last week is already peeling off."),
            ("Nepalese legal system is too complex for laymen", "general", "We need more simplified guides on our basic rights."),
            ("How to request budget breakdown for local ward?", "budget", "I want to see how much was spent on our local community hall.")
        ]

        for title, cat, content in forum_topics:
            author = random.choice(users)
            uv = random.randint(10, 300)
            dv = random.randint(0, 50)
            thread = DiscussionThread(
                id=str(uuid.uuid4()), title=title, category=cat, content=content,
                author_id=author.id, upvotes=uv, downvotes=dv,
                comment_count=0,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 4))
            )
            db.session.add(thread)
            
            # Add some comments
            for j in range(random.randint(2, 6)):
                c_author = random.choice(users)
                c_uv = random.randint(5, 50)
                c_dv = random.randint(0, 10)
                comment = ThreadComment(
                    id=str(uuid.uuid4()), thread_id=thread.id, content=f"This is an insightful point about {cat}. We need more transparency here.",
                    author_id=c_author.id, upvotes=c_uv, downvotes=c_dv,
                    created_at=thread.created_at + timedelta(hours=random.randint(1, 24))
                )
                db.session.add(comment)
                thread.comment_count += 1
                
                # Add a reply
                if random.random() > 0.5:
                    r_author = random.choice(users)
                    reply = ThreadComment(
                        id=str(uuid.uuid4()), thread_id=thread.id, parent_id=comment.id,
                        content=f"Totally agree with u/{c_author.name}. I've seen this too.",
                        author_id=r_author.id, upvotes=random.randint(2, 20),
                        created_at=comment.created_at + timedelta(hours=random.randint(1, 5))
                    )
                    db.session.add(reply)
                    thread.comment_count += 1

        db.session.commit()
        print("✅ Database RICHLY Seeded with Forum, Laws, & Votes!")

if __name__ == "__main__":
    seed_data()
