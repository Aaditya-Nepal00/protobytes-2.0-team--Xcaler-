# Sachet - unified transparency platform 🇳🇵

Sachet is a unified transparency platform providing real-time project tracking, anonymous corruption reporting, simplified laws, budget visualization, and community discussions - all accessible to every Nepali citizen.

## Team Information
- **Team Name**: Xcaler
- **Team Members**:
  - [Aaditya Nepal](https://github.com/Aaditya-Nepal00) - [aadityanepal1200@gmail.com]
  - [Sarjak Khanal](https://github.com/devWisz) - [sarjak.khanal@gmail.com]
  - [Stuti Khatiwada](https://github.com/sturdyiestuti) - [stutikhatiwada.19@gmail.com]

## Project Details
- **Project Title**: Sachet
- **Category**: Open Innovation
- **Problem Statement**: Nepal faces critical governance transparency challenges: 85% of development projects face delays, limited budget visibility, complex legal documents, and fear of reporting corruption prevents accountability.
- **Solution Overview**: Sachet addresses these gaps by providing:
  - **Real-time Project Tracking**: Track national pride and local projects with visual indicators.
  - **Anonymous Corruption Reporting**: Secure, encrypted portal for citizens to report malpractice.
  - **Simplified Laws**: A "translated" legal library that makes complex acts understandable for laymen.
  - **Budget Visualization**: Interactive charts showing where national and local funds are allocated.
  - **Community Forum**: A Reddit-style discussion hub for civic engagement and voting.

## Technical Stack

### Backend Stack
- **Framework**: Flask 3.0 (Python 3.11+) - Lightweight, flexible, fast development.
- **Database**: SQLite + SQLAlchemy ORM - Relational data management with powerful querying.

### Frontend Stack
- **Framework**: React 18 + TypeScript - Type safety, component reusability, large ecosystem.
- **Build Tool**: Vite - Lightning-fast builds, hot module replacement.
- **UI Library**: shadcn/ui - Accessible components with Radix UI primitives.
- **Additional Libraries**:
  - **Chart.js**: Statistical charts for budget visibility.
  - **Leaflet.js**: Interactive maps for project tracking.
  - **Zustand**: Clean and efficient state management.
  - **react-hook-form**: Robust form handling.
  - **zod**: Schema validation for reporting and auth.
  - **Tailwind CSS**: Utility-first styling for a premium, responsive UI.

## Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python (3.11+)

### Steps to Run
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aaditya-Nepal00/protobytes-2.0-team--Xcaler-
   cd Sachet
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```