import os
import sys

# Standardize path
sys.path.append(os.getcwd())

from app import create_app, db
from app.models import Project, User, Law, Tender

def verify():
    app = create_app('development')
    with app.app_context():
        print("--- DATABASE VERIFICATION ---")
        print(f"Users: {User.query.count()}")
        print(f"Projects: {Project.query.count()}")
        print(f"Laws: {Law.query.count()}")
        print(f"Tenders: {Tender.query.count()}")
        
        if Project.query.count() > 0:
            first = Project.query.first()
            print(f"Sample Project: {first.title} ({first.status})")
        else:
            print("ALERT: NO PROJECTS FOUND!")
        print("----------------------------")

if __name__ == "__main__":
    verify()
