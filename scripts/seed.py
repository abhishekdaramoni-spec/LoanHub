import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from datetime import datetime, timedelta
from decimal import Decimal
from app import create_app
from app.extensions import db
from app.models import User, LoanType, LoanApplication, EMIHistory, InterestRate, FAQ, Notification, ContactMessage

# Initialize App context
app = create_app()

def seed_database():
    with app.app_context():
        # Ensure database tables exist
        db.create_all()
        print("Ensuring tables are initialized...")

        # -------------------------------------------------------------
        # 1. SEED FAQ CONTENT
        # -------------------------------------------------------------
        if FAQ.query.count() == 0:
            print("Seeding FAQs...")
            faqs = [
                FAQ(question="What documents do I need to apply for a Personal Loan?",
                    answer="You will need: (1) Identity Proof (Aadhar/PAN Card), (2) Address Proof (Electricity bill/Aadhar), (3) Last 3 months Salary Slips, and (4) Last 6 months bank statement.",
                    category="Documents"),
                FAQ(question="How is my EMI calculated?",
                    answer="EMIs are calculated using the formula: [P x r x (1+r)^n]/[((1+r)^n)-1] where P is Principal, r is Monthly Interest Rate, and n is Tenure in months.",
                    category="Calculator"),
                FAQ(question="What is the minimum credit score required for loan approval?",
                    answer="For premium interest rates, we recommend a credit score of 750 or above. However, we consider applicants with credit scores of 600 or higher.",
                    category="Eligibility"),
                FAQ(question="How long does it take for a loan to be disbursed?",
                    answer="Once all documents are uploaded and verified, approval takes 24 to 48 hours. Funds are usually disbursed to your account within 24 hours of approval.",
                    category="Process"),
                FAQ(question="Can I prepay my loan early?",
                    answer="Yes, LoanSphere offers pre-payment options. Personal loans have a lock-in period of 6 months, after which you can foreclose with minimal processing fees.",
                    category="Payment"),
                FAQ(question="Are there any hidden processing charges?",
                    answer="No, LoanSphere believes in complete transparency. Our processing fees range from 1% to 2.5% depending on the loan type, disclosed upfront in the agreement.",
                    category="General"),
                FAQ(question="What is a Loan Against Property (LAP)?",
                    answer="Loan Against Property is a secured loan where you pledge your residential or commercial property as collateral to secure funding for business or personal needs.",
                    category="General"),
                FAQ(question="How do I check my loan application status?",
                    answer="Simply log into your dashboard, click on 'My Applications', and you can track the active state (Pending, In Review, Approved, or Rejected) and admin feedback in real-time.",
                    category="Process")
            ]
            db.session.add_all(faqs)
            db.session.commit()

        # -------------------------------------------------------------
        # 2. SEED 20 LOAN TYPES
        # -------------------------------------------------------------
        if LoanType.query.count() == 0:
            print("Seeding 20 Loan Types...")
            loan_types_data = [
                # 1. Personal Loan
                {
                    "name": "Personal Loan", "slug": "personal-loan", "category": "Retail",
                    "description": "Flexible and unsecured personal loans for weddings, travel, emergencies, or shopping with quick 24-hour approvals.",
                    "min_amount": 50000.0, "max_amount": 1500000.0, "min_interest_rate": 10.50, "max_interest_rate": 18.00,
                    "processing_fee_pct": 1.50, "min_tenure_months": 12, "max_tenure_months": 60,
                    "eligibility_criteria": "Age 21-58, Minimum Income: INR 25,000/month, Credit Score: 650+",
                    "approval_time": "24 Hours", "icon_class": "fa-user-tie"
                },
                # 2. Home Loan
                {
                    "name": "Home Loan", "slug": "home-loan", "category": "Retail",
                    "description": "Fulfill your dream of owning a home with low interest rates, flexible tenures, and door-step service.",
                    "min_amount": 500000.0, "max_amount": 50000000.0, "min_interest_rate": 8.40, "max_interest_rate": 12.00,
                    "processing_fee_pct": 0.50, "min_tenure_months": 36, "max_tenure_months": 360,
                    "eligibility_criteria": "Age 21-65, Minimum Income: INR 35,000/month, Property documents clearance, Credit Score: 700+",
                    "approval_time": "3-5 Working Days", "icon_class": "fa-home"
                },
                # 3. Car Loan
                {
                    "name": "Car Loan", "slug": "car-loan", "category": "Retail",
                    "description": "Get up to 90% financing for your brand new car or pre-owned vehicles with competitive interest rates.",
                    "min_amount": 200000.0, "max_amount": 5000000.0, "min_interest_rate": 8.75, "max_interest_rate": 11.50,
                    "processing_fee_pct": 1.00, "min_tenure_months": 12, "max_tenure_months": 84,
                    "eligibility_criteria": "Age 21-60, Minimum Income: INR 20,000/month, Credit Score: 650+",
                    "approval_time": "48 Hours", "icon_class": "fa-car"
                },
                # 4. Education Loan
                {
                    "name": "Education Loan", "slug": "education-loan", "category": "Special",
                    "description": "Finance your higher education in premier institutions worldwide. Enjoys tax benefits and flexible repayment holidays.",
                    "min_amount": 100000.0, "max_amount": 10000000.0, "min_interest_rate": 9.50, "max_interest_rate": 13.50,
                    "processing_fee_pct": 0.00, "min_tenure_months": 36, "max_tenure_months": 180,
                    "eligibility_criteria": "Student with secured admission letter, Co-borrower income proof, Credit Score: 600+",
                    "approval_time": "3 Working Days", "icon_class": "fa-graduation-cap"
                },
                # 5. Business Loan
                {
                    "name": "Business Loan", "slug": "business-loan", "category": "Commercial",
                    "description": "Scale up your operations, buy machinery, or manage working capital with LoanSphere's customized business credit lines.",
                    "min_amount": 300000.0, "max_amount": 20000000.0, "min_interest_rate": 12.50, "max_interest_rate": 22.00,
                    "processing_fee_pct": 2.00, "min_tenure_months": 12, "max_tenure_months": 60,
                    "eligibility_criteria": "Business vintage >= 3 years, Audited financials, Annual turnover > 15 Lakhs, Credit Score: 700+",
                    "approval_time": "4 Working Days", "icon_class": "fa-briefcase"
                },
                # 6. Gold Loan
                {
                    "name": "Gold Loan", "slug": "gold-loan", "category": "Special",
                    "description": "Instant liquid cash against your gold jewelry with minimum paperwork and maximum per-gram valuation.",
                    "min_amount": 20000.0, "max_amount": 5000000.0, "min_interest_rate": 7.90, "max_interest_rate": 12.00,
                    "processing_fee_pct": 0.25, "min_tenure_months": 3, "max_tenure_months": 24,
                    "eligibility_criteria": "Age 18+, Gold purity 18-24 Karats, Valuation done at Bank branch",
                    "approval_time": "45 Minutes", "icon_class": "fa-coins"
                },
                # 7. Agriculture Loan
                {
                    "name": "Agriculture Loan", "slug": "agriculture-loan", "category": "Agriculture",
                    "description": "Tailored credit facilities for purchasing seeds, tractors, solar pumps, or modernizing storage setups.",
                    "min_amount": 30000.0, "max_amount": 3000000.0, "min_interest_rate": 6.50, "max_interest_rate": 9.50,
                    "processing_fee_pct": 0.50, "min_tenure_months": 6, "max_tenure_months": 120,
                    "eligibility_criteria": "Land holding ownership documents, Farming income verification",
                    "approval_time": "3 Working Days", "icon_class": "fa-seedling"
                },
                # 8. Loan Against Property
                {
                    "name": "Loan Against Property", "slug": "loan-against-property", "category": "Commercial",
                    "description": "Unlock the hidden monetary value of your property to secure funding for personal, medical, or business purposes.",
                    "min_amount": 1000000.0, "max_amount": 100000000.0, "min_interest_rate": 9.00, "max_interest_rate": 13.00,
                    "processing_fee_pct": 1.00, "min_tenure_months": 36, "max_tenure_months": 180,
                    "eligibility_criteria": "Age 21-65, Commercial or Residential property clearance docs, Credit Score: 700+",
                    "approval_time": "5 Working Days", "icon_class": "fa-building"
                },
                # 9. Credit Card Loan
                {
                    "name": "Credit Card Loan", "slug": "credit-card-loan", "category": "Retail",
                    "description": "Instant pre-approved cash loans linked to your existing Credit Card limit, no document uploads needed.",
                    "min_amount": 10000.0, "max_amount": 500000.0, "min_interest_rate": 14.00, "max_interest_rate": 20.00,
                    "processing_fee_pct": 2.00, "min_tenure_months": 6, "max_tenure_months": 36,
                    "eligibility_criteria": "Active LoanSphere Credit Card holder with clean repayment record.",
                    "approval_time": "Instant", "icon_class": "fa-credit-card"
                },
                # 10. Medical Emergency Loan
                {
                    "name": "Medical Emergency Loan", "slug": "medical-loan", "category": "Special",
                    "description": "Quick emergency funding to cover hospitalization, surgeries, and critical care procedures.",
                    "min_amount": 50000.0, "max_amount": 800000.0, "min_interest_rate": 9.99, "max_interest_rate": 15.00,
                    "processing_fee_pct": 0.75, "min_tenure_months": 12, "max_tenure_months": 48,
                    "eligibility_criteria": "Income: INR 20,000/month, Hospital admission/cost estimation, Credit Score: 600+",
                    "approval_time": "4 Hours", "icon_class": "fa-heartbeat"
                },
                # 11. Travel Loan
                {
                    "name": "Travel Loan", "slug": "travel-loan", "category": "Retail",
                    "description": "Vacations are simple now. Secure a travel loan to fund your dream destination holidays, bookings and visas.",
                    "min_amount": 50000.0, "max_amount": 500000.0, "min_interest_rate": 11.50, "max_interest_rate": 17.50,
                    "processing_fee_pct": 1.50, "min_tenure_months": 12, "max_tenure_months": 36,
                    "eligibility_criteria": "Age 21-60, Stable income proof, Credit Score: 650+",
                    "approval_time": "24 Hours", "icon_class": "fa-plane"
                },
                # 12. Wedding Loan
                {
                    "name": "Wedding Loan", "slug": "wedding-loan", "category": "Retail",
                    "description": "Create memories for a lifetime. Finance your wedding venue, decoration, catering, and jewelry.",
                    "min_amount": 100000.0, "max_amount": 2000000.0, "min_interest_rate": 10.99, "max_interest_rate": 16.50,
                    "processing_fee_pct": 1.25, "min_tenure_months": 12, "max_tenure_months": 60,
                    "eligibility_criteria": "Age 21-60, Joint income details optional, Credit Score: 680+",
                    "approval_time": "24 Hours", "icon_class": "fa-ring"
                },
                # 13. Two Wheeler Loan
                {
                    "name": "Two Wheeler Loan", "slug": "two-wheeler-loan", "category": "Retail",
                    "description": "Quick funding for scooters and motorbikes with up to 95% on-road price coverage.",
                    "min_amount": 40000.0, "max_amount": 300000.0, "min_interest_rate": 9.25, "max_interest_rate": 13.00,
                    "processing_fee_pct": 1.00, "min_tenure_months": 6, "max_tenure_months": 48,
                    "eligibility_criteria": "Age 18-60, Salaried or Self employed, Credit Score: 620+",
                    "approval_time": "12 Hours", "icon_class": "fa-motorcycle"
                },
                # 14. Commercial Vehicle Loan
                {
                    "name": "Commercial Vehicle Loan", "slug": "commercial-vehicle-loan", "category": "Commercial",
                    "description": "Finance trucks, buses, tankers, and delivery vans to keep your supply chain rolling.",
                    "min_amount": 500000.0, "max_amount": 15000000.0, "min_interest_rate": 10.20, "max_interest_rate": 14.50,
                    "processing_fee_pct": 1.50, "min_tenure_months": 12, "max_tenure_months": 84,
                    "eligibility_criteria": "Valid commercial license/business registry, transport contracts, Credit Score: 650+",
                    "approval_time": "3 Working Days", "icon_class": "fa-truck"
                },
                # 15. Microfinance Loan
                {
                    "name": "Microfinance Loan", "slug": "microfinance-loan", "category": "Special",
                    "description": "Small collateral-free credits targeting rural micro-enterprises and self-help groups.",
                    "min_amount": 10000.0, "max_amount": 100000.0, "min_interest_rate": 12.00, "max_interest_rate": 15.00,
                    "processing_fee_pct": 0.50, "min_tenure_months": 6, "max_tenure_months": 24,
                    "eligibility_criteria": "Group recommendation, Aadhaar card KYC",
                    "approval_time": "2 Working Days", "icon_class": "fa-users"
                },
                # 16. Machinery Loan
                {
                    "name": "Machinery Loan", "slug": "machinery-loan", "category": "Commercial",
                    "description": "Finance modern toolings, manufacturing assembly lines, or medical diagnostic devices.",
                    "min_amount": 1000000.0, "max_amount": 50000000.0, "min_interest_rate": 9.80, "max_interest_rate": 13.20,
                    "processing_fee_pct": 1.00, "min_tenure_months": 12, "max_tenure_months": 72,
                    "eligibility_criteria": "Purchase quote, business cashflow statement, Credit Score: 700+",
                    "approval_time": "5 Working Days", "icon_class": "fa-cogs"
                },
                # 17. MSME Loan
                {
                    "name": "MSME Loan", "slug": "msme-loan", "category": "Commercial",
                    "description": "Accelerate growth of small/medium enterprises. Government scheme subsidies applicable.",
                    "min_amount": 500000.0, "max_amount": 10000000.0, "min_interest_rate": 8.99, "max_interest_rate": 11.99,
                    "processing_fee_pct": 0.75, "min_tenure_months": 12, "max_tenure_months": 120,
                    "eligibility_criteria": "MSME Udyam registration, active business account, Credit Score: 680+",
                    "approval_time": "3 Working Days", "icon_class": "fa-industry"
                },
                # 18. Land Purchase Loan
                {
                    "name": "Land Purchase Loan", "slug": "land-loan", "category": "Agriculture",
                    "description": "Finance purchase of agricultural lands or residential plots for development.",
                    "min_amount": 500000.0, "max_amount": 20000000.0, "min_interest_rate": 9.50, "max_interest_rate": 13.00,
                    "processing_fee_pct": 1.00, "min_tenure_months": 36, "max_tenure_months": 180,
                    "eligibility_criteria": "Clear property title, boundary survey reports, Credit Score: 700+",
                    "approval_time": "7 Working Days", "icon_class": "fa-map-marked-alt"
                },
                # 19. Pensioner Loan
                {
                    "name": "Pensioner Loan", "slug": "pensioner-loan", "category": "Special",
                    "description": "Specially designed for retired govt/defence employees drawing pension through LoanSphere.",
                    "min_amount": 30000.0, "max_amount": 1000000.0, "min_interest_rate": 9.00, "max_interest_rate": 11.50,
                    "processing_fee_pct": 0.50, "min_tenure_months": 12, "max_tenure_months": 60,
                    "eligibility_criteria": "Pension draw records from treasury accounts, max age 76 at loan end",
                    "approval_time": "24 Hours", "icon_class": "fa-blind"
                },
                # 20. Renovation Loan
                {
                    "name": "Renovation Loan", "slug": "renovation-loan", "category": "Retail",
                    "description": "Remodel your kitchen, repaint, or expand your house with customized home improvement funding.",
                    "min_amount": 100000.0, "max_amount": 2000000.0, "min_interest_rate": 8.90, "max_interest_rate": 12.50,
                    "processing_fee_pct": 1.00, "min_tenure_months": 12, "max_tenure_months": 120,
                    "eligibility_criteria": "Ownership of home property, renovation estimates, Credit Score: 680+",
                    "approval_time": "48 Hours", "icon_class": "fa-paint-roller"
                }
            ]
            
            for lt in loan_types_data:
                loan_type = LoanType(
                    name=lt["name"],
                    slug=lt["slug"],
                    category=lt["category"],
                    description=lt["description"],
                    min_amount=Decimal(str(lt["min_amount"])),
                    max_amount=Decimal(str(lt["max_amount"])),
                    min_interest_rate=Decimal(str(lt["min_interest_rate"])),
                    max_interest_rate=Decimal(str(lt["max_interest_rate"])),
                    processing_fee_pct=Decimal(str(lt["processing_fee_pct"])),
                    min_tenure_months=lt["min_tenure_months"],
                    max_tenure_months=lt["max_tenure_months"],
                    eligibility_criteria=lt["eligibility_criteria"],
                    approval_time=lt["approval_time"],
                    icon_class=lt["icon_class"]
                )
                db.session.add(loan_type)
            db.session.commit()
            print("Successfully seeded 20 Loan Types.")

        # -------------------------------------------------------------
        # 3. SEED 5 ADMIN ACCOUNTS
        # -------------------------------------------------------------
        if User.query.filter_by(is_admin=True).count() == 0:
            print("Seeding 5 Admin Accounts...")
            for i in range(1, 6):
                admin = User(
                    name=f"LoanSphere Admin {i}",
                    email=f"admin{i}@loansphere.bank",
                    phone=f"+91987654321{i}",
                    address=f"LoanSphere Headquarters, Tower {i}, Mumbai",
                    is_admin=True,
                    email_verified=True,
                    verification_token=None
                )
                admin.set_password(f"adminPass{i}!")
                db.session.add(admin)
            db.session.commit()
            print("Successfully seeded 5 admin accounts.")

        # -------------------------------------------------------------
        # 4. SEED 100 DUMMY USERS
        # -------------------------------------------------------------
        if User.query.filter_by(is_admin=False).count() == 0:
            print("Seeding 100 Dummy Users...")
            first_names = ["Arjun", "Aditya", "Amit", "Alok", "Aarav", "Bhavna", "Chitra", "Deepak", "Divya", "Esha",
                           "Ganesh", "Hari", "Isha", "Jay", "Karan", "Kirti", "Lokesh", "Manoj", "Meera", "Neha",
                           "Omkar", "Pooja", "Rahul", "Rohan", "Sanjay", "Suresh", "Tanvi", "Vijay", "Yash", "Zoya"]
            last_names = ["Sharma", "Verma", "Gupta", "Kumar", "Singh", "Patel", "Joshi", "Mehta", "Nair", "Rao",
                          "Das", "Choudhury", "Iyer", "Reddy", "Banerjee", "Sinha", "Mishra", "Pillai", "Kapoor", "Sen"]
            
            cities = ["Mumbai", "Delhi", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]
            
            for i in range(1, 101):
                fname = random.choice(first_names)
                lname = random.choice(last_names)
                name = f"{fname} {lname}"
                email = f"user{i}@gmail.com"
                phone = f"+919{random.randint(10000000, 99999999)}"
                address = f"Flat {random.randint(101, 909)}, Building {random.choice(['A','B','C','D'])}, {random.choice(cities)}, India"
                
                user = User(
                    name=name,
                    email=email.lower(),
                    phone=phone,
                    address=address,
                    is_admin=False,
                    email_verified=random.choice([True, True, True, False]) # 75% verified
                )
                user.set_password("userpass123")
                db.session.add(user)
                
                # Commit in batches of 25 to optimize SQL executions
                if i % 25 == 0:
                    db.session.commit()
            print("Successfully seeded 100 users.")

        # -------------------------------------------------------------
        # 5. SEED 100 DUMMY LOAN APPLICATIONS
        # -------------------------------------------------------------
        if LoanApplication.query.count() == 0:
            print("Seeding 100 Dummy Loan Applications...")
            
            users = User.query.filter_by(is_admin=False).all()
            loan_types = LoanType.query.all()
            
            occupations = ['Salaried', 'Self Employed Business', 'Self Employed Professional', 'Retired', 'Agriculture']
            employers = ['Tata Consultancy Services', 'Infosys Ltd', 'Reliance Industries', 'ICICI Bank', 'State Health Dept', 'Self business proprietorship', 'HDFC Bank']
            statuses = ['Pending', 'In Review', 'Approved', 'Rejected']
            genders = ['Male', 'Female', 'Other']
            
            # Generate exactly 100 applications
            for i in range(1, 101):
                user = random.choice(users)
                loan_type = random.choice(loan_types)
                
                status = random.choices(statuses, weights=[30, 20, 40, 10], k=1)[0] # Bias towards approvals & pending
                
                # Date applied (distributed over the last 6 months)
                days_ago = random.randint(5, 180)
                applied_date = datetime.utcnow() - timedelta(days=days_ago)
                
                income = Decimal(str(random.randint(25000, 150000)))
                # Pick loan amount between min & max limits
                min_amt = float(loan_type.min_amount)
                max_amt = float(loan_type.max_amount)
                # Cap the maximum amount to keep stats realistic
                max_amt_cap = min(max_amt, 5000000.0)
                loan_amount = Decimal(str(round(random.uniform(min_amt, max_amt_cap), 2)))
                
                tenure = random.randint(loan_type.min_tenure_months, min(loan_type.max_tenure_months, 120))
                
                pan = f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))}{random.randint(1000, 9999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
                aadhar = f"{random.randint(100000000000, 999999999999)}"
                
                loan_app = LoanApplication(
                    user_id=user.id,
                    loan_type_id=loan_type.id,
                    full_name=user.name,
                    dob=datetime.utcnow().date() - timedelta(days=random.randint(8000, 20000)),
                    gender=random.choice(genders),
                    email=user.email,
                    phone=user.phone,
                    address=user.address,
                    occupation=random.choice(occupations),
                    employer=random.choice(employers),
                    monthly_income=income,
                    loan_amount=loan_amount,
                    tenure_months=tenure,
                    pan_number=pan,
                    aadhar_number=aadhar,
                    # Placeholder file names
                    pan_doc="sample_pan.pdf",
                    aadhar_doc="sample_aadhar.pdf",
                    salary_slip_doc="sample_salary.pdf",
                    bank_statement_doc="sample_statement.pdf",
                    status=status,
                    remarks=f"Auto seeded application. Repayments tracked." if status == 'Approved' else (f"Under Verification processes." if status == 'In Review' else None),
                    applied_at=applied_date,
                    updated_at=applied_date + timedelta(days=random.randint(1, 4))
                )
                
                db.session.add(loan_app)
                db.session.flush() # Flush to get application ID
                
                # Create historical notifications for the application status
                notif = Notification(
                    user_id=user.id,
                    message=f"Your loan application for {loan_type.name} (Amount: INR {loan_amount:,.2f}) status is {status}.",
                    is_read=random.choice([True, False]),
                    created_at=loan_app.updated_at
                )
                db.session.add(notif)
                
                # If application is Approved, seed some historical EMI payments
                if status == 'Approved':
                    # Calculate monthly EMI
                    rate_annual = loan_type.min_interest_rate
                    r = (rate_annual / 100) / 12
                    n = tenure
                    power = (1 + r) ** n
                    
                    try:
                        emi = loan_amount * r * power / (power - 1)
                        
                        # Add 1 to 3 months of paid EMIs
                        months_passed = min(int(days_ago / 30), 3)
                        rem_bal = loan_amount
                        
                        for m in range(1, months_passed + 1):
                            interest_paid = rem_bal * r
                            principal_paid = emi - interest_paid
                            rem_bal -= principal_paid
                            
                            emi_pay = EMIHistory(
                                user_id=user.id,
                                loan_application_id=loan_app.id,
                                amount_paid=emi,
                                principal_paid=principal_paid,
                                interest_paid=interest_paid,
                                balance_remaining=rem_bal,
                                payment_date=applied_date + timedelta(days=m * 30),
                                status='Paid'
                            )
                            db.session.add(emi_pay)
                    except Exception as calc_err:
                        print(f"Error seeding emi for app {loan_app.id}: {calc_err}")
                
                if i % 20 == 0:
                    db.session.commit()
            
            db.session.commit()
            print("Successfully seeded 100 Dummy Loan Applications and corresponding EMIs/Notifications.")
            
        # -------------------------------------------------------------
        # 6. SEED GENERAL CONTACT MESSAGES
        # -------------------------------------------------------------
        if ContactMessage.query.count() == 0:
            print("Seeding contact messages...")
            subjects = ["Loan processing status query", "Interest rates negotiable?", "Need corporate lending information", "FAQ update request", "Appreciation for fast approval"]
            for i in range(10):
                msg = ContactMessage(
                    name=f"Inquirer {i+1}",
                    email=f"inquirer{i+1}@example.com",
                    phone=f"+91900000000{i}",
                    subject=random.choice(subjects),
                    message="Hello, I would like to get more information about the eligibility criteria for home loans for Non-Resident Indians. Thanks.",
                    is_read=random.choice([True, False])
                )
                db.session.add(msg)
            db.session.commit()
            print("Contact messages seeded.")
            
        print("\n--- DATABASE SEEDING COMPLETED SUCCESSFULLY ---")

if __name__ == '__main__':
    seed_database()
