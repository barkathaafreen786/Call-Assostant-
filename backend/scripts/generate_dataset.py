
import json
import random

def generate_dataset():
    loan_types = ["Personal Loan", "Home Loan", "Car Loan", "Education Loan", "Business Loan", "Gold Loan"]
    amounts = ["₹5 Lakhs", "₹10 Lakhs", "₹50 Lakhs", "₹1 Crore", "₹2 Lakhs"]
    tenures = ["12 months", "36 months", "5 years", "10 years", "20 years"]
    interest_rates = {
        "Personal Loan": "10.5% - 14%",
        "Home Loan": "8.5% - 9.5%",
        "Car Loan": "9% - 11%",
        "Education Loan": "9.5% - 12%",
        "Business Loan": "11% - 16%",
        "Gold Loan": "7% - 9%"
    }
    
    eligibility_criteria = {
        "Personal Loan": "Age 21-60, Minimum Income ₹25,000/month, Credit Score 750+",
        "Home Loan": "Age 23-65, Salaried/Self-employed, Stable Income for 2 years",
        "Car Loan": "Age 21-65, Minimum Annual Income ₹3 Lakhs",
        "Education Loan": "Indian Resident, Admission in recognized institution, Co-applicant required",
        "Business Loan": "Business vintage 3 years, Profitable for last 2 years",
        "Gold Loan": "Age 18-70, Own gold ornaments/coins"
    }

    documents_required = {
        "Personal Loan": "ID Proof, Address Proof, Last 3 months Salary Slips, Bank Statements",
        "Home Loan": "Property Papers, Income Proof (ITR/Salary Slips), ID & Address Proof",
        "Car Loan": "Vehicle Quotation, ID Proof, Income Proof, Bank Statement",
        "Education Loan": "Admission Letter, Fee Structure, KYC of Student & Co-applicant",
        "Business Loan": "Business Registration, GST Returns, Bank Statements (6 months), ITR",
        "Gold Loan": "ID Proof, Address Proof, Photos"
    }

    dataset = []

    # 1. Eligibility Queries
    for loan in loan_types:
        questions = [
            f"What is the eligibility for a {loan}?",
            f"Am I eligible for a {loan}?",
            f"Attributes required for {loan} approval.",
            f"Who can apply for a {loan}?"
        ]
        for q in questions:
            dataset.append({
                "instruction": q,
                "input": "",
                "output": f"Eligibility for {loan}: {eligibility_criteria[loan]}. Ensure you meet these criteria before applying."
            })

    # 2. Interest Rate Queries
    for loan in loan_types:
        questions = [
            f"What is the interest rate for a {loan}?",
            f"Current {loan} interest rates.",
            f"How much interest do you charge for {loan}?",
            f"Is the {loan} interest rate fixed or floating?"
        ]
        for q in questions:
            dataset.append({
                "instruction": q,
                "input": "",
                "output": f"The current interest rate for {loan} ranges from {interest_rates[loan]}. Rates may vary based on your credit score and relationship with the bank."
            })

    # 3. Documents Required Queries
    for loan in loan_types:
        questions = [
            f"Documents needed for {loan}?",
            f"What paperwork is required for {loan}?",
            f"List of documents for {loan} application.",
            f"Do I need ITR for {loan}?"
        ]
        for q in questions:
            dataset.append({
                "instruction": q,
                "input": "",
                "output": f"To apply for a {loan}, please submit: {documents_required[loan]}."
            })

    # 4. EMI & Repayment Queries
    for loan in loan_types:
        questions = [
            f"Can I prepay my {loan}?",
            f"Is there a penalty for {loan} foreclosure?",
            f"What is the maximum tenure for {loan}?",
            f"How is {loan} EMI calculated?"
        ]
        dataset.append({
            "instruction": questions[0],
            "input": "",
            "output": f"Yes, you can prepay your {loan} after a lock-in period of 6-12 months. Prepayment charges differ based on the loan type (usually 0% for floating rate loans)."
        })
        dataset.append({
            "instruction": questions[1],
            "input": "",
            "output": f"Foreclosure charges for {loan} typically range from 2% to 4% of the outstanding principal. No charges for individual borrowers on floating rate loans."
        })
        dataset.append({
            "instruction": questions[2],
            "input": "",
            "output": f"The maximum tenure for a {loan} is typically up to {tenures[random.randint(0, len(tenures)-1)]}, depending on the bank's policy."
        })
        dataset.append({
            "instruction": questions[3],
            "input": "",
            "output": f"{loan} EMI is calculated based on Principal amount, Interest rate, and Tenure. You can use our online EMI calculator for precise figures."
        })

    # 5. General Banking Queries
    general_queries = [
        ("How do I check my account balance?", "You can check your balance via Mobile Banking App, NetBanking, SMS 'BAL' to 56767, or by visiting the nearest ATM."),
        ("What is the customer care number?", "Our 24/7 customer care number is 1800-123-4567. You can also email us at support@bank.com."),
        ("How to block my lost debit card?", "To block your debit card immediately, log in to NetBanking/Mobile App > Cards > Block Card, or call customer care at 1800-123-4567."),
        ("What are the branch working hours?", "Our branches are open Monday to Saturday (except 2nd & 4th Saturdays) from 10:00 AM to 4:00 PM."),
        ("How to change my registered mobile number?", "Visit your nearest branch with a valid ID proof and fill out the 'Change of Contact Details' form. Update takes 24-48 hours."),
        ("What is NEFT and RTGS timing?", "NEFT transactions are available 24x7. RTGS is available from 7:00 AM to 6:00 PM strictly for high-value transactions (above ₹2 Lakhs)."),
        ("How to apply for a credit card?", "You can apply for a credit card through our website, mobile app, or by visiting a branch. Eligibility depends on income and credit score."),
        ("What is the minimum balance requirement?", "For a regular savings account, the minimum average monthly balance (MAB) is ₹10,000 for metro branches and ₹5,000 for rural branches."),
        ("How to activate net banking?", "Go to our website, click 'New User Registration', enter your Customer ID and Account Number, and verify using OTP sent to your registered mobile."),
        ("What is UPI transaction limit?", "The standard UPI transaction limit is ₹1 Lakh per day, but it may vary for specific apps or first-time users.")
    ]
    
    for q, a in general_queries:
        dataset.append({
            "instruction": q,
            "input": "",
            "output": a
        })

    # Ensure we reach at least 150 items by adding variations
    while len(dataset) < 160:
        loan = random.choice(loan_types)
        topic = random.choice(["interest", "eligibility", "documents"])
        
        if topic == "interest":
            dataset.append({
                "instruction": f"Tell me about the interest for {loan}.", 
                "input": "",
                "output": f"{loan} interest rates are currently {interest_rates[loan]}. Check the website for the latest offers."
            })
        elif topic == "eligibility":
             dataset.append({
                "instruction": f"Can I get a {loan}?", 
                "input": "",
                "output": f"To get a {loan}, you generally need: {eligibility_criteria[loan]}."
            })
        elif topic == "documents":
             dataset.append({
                "instruction": f"Papers for {loan} application.",
                "input": "",
                "output": f"Required documents for {loan}: {documents_required[loan]}."
            })

    with open("../data/dataset.json", "w") as f:
        json.dump(dataset, f, indent=4)
        print(f"Dataset generated with {len(dataset)} items.")

if __name__ == "__main__":
    generate_dataset()
