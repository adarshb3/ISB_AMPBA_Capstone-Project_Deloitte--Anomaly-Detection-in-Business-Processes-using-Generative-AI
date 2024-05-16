import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import OpenAI
from langchain_community.callbacks import StreamlitCallbackHandler

# Load environment variables
load_dotenv()
FROM_EMAIL = os.getenv('FROM_EMAIL')
FROM_PASSWORD = os.getenv('FROM_PASSWORD')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Cache data loading and processing
@st.cache_data
def load_and_process_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    date_columns = [
        'TransactionDate', 'EntryDate', 'Booking Date', 'Travel start date',
        'Travel end date', 'HireDate', 'TerminationDate', 'IssuedDate',
        'CardExpiryDate', 'CardCloseDate'
    ]
    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors='coerce')
    return df

# Cache OpenAI client initialization
@st.cache_resource
def init_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY, temperature=0, verbose=True)

# Cache CSV agent initialization
@st.cache_resource
def init_csv_agent(_openai_client, df_path):
    return create_csv_agent(
        _openai_client,
        df_path,
        verbose=True,
        model="gpt-4o",
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

# Cache the prompts
@st.cache_resource
def get_prompts():
    return [
        "Employees with a lot of cash/out of pocket expenses",
            "Identify duplicate claims with same emp ID, same amount, same transaction date and same merchant",
            "Identify duplicate claims with same date, same vendor, same amount charged, by more than one employee",
            "Identify duplicate claims with same emp ID, same amount, same transaction date and same expense type",
            "Identify employees with frequent duplicate claim submissions (X no. of duplicates Z times)",
            "Identify duplicate expenses present in both card & out of pocket expenses(exclude hotel related expenses)",
            "Identify Entertainment related expenses based on expense type/description/spend category",
            "Identify expenses per attendee for seminars and client meetings >$X",
            "Identify gifts  expenses to employees/customers",
            "Identify costs outside of policy or costly late bookings (Ex: purchasing air tickets for family etc)",
            "Duplicate tickets purchase- Same employee, same origin, same destination, and the same travel date",
            "Identify whether appropriate seat class is used (Ex: less than VP - economy for domestic, VP or up - business class with approval, Executives - can fly any class)",
            "Identify employees claiming to travel to multiple cities on the same day",
            "Match claims for personal vehicle usage and rental car for same time period",
            "Duplicates on expense type - Identify where mileage, gas, and/or rental care reimbursements were sought on the same day",
            "Identify transactions where an Employee claimed for both gas and mileage expense",
            "Identify instances where mileage claims were made for the same time period as car rental/gas/other transport",
            "Compare mileage claims to distances reported",
            "Identify lodging expenses that are greater than $X per night",
            "Meal Expenses per attendee >$X beyond company limits",
            "Identify lodging expenses that are outside the norm (by location, month, etc.)",
            "Expenses claimed for Accommocation even after Employee return",
            "Identify duplicate claims for meals (i.e. multiple persons, same day, same location)",
            "Identify expense claims for periods when the employee is on vacation/holiday/weekend",
            "Time Series Analysis of Per diem expense and identify records which crossed the per diem limit by X%",
            "Expense reports made by employees with both cash and card transactions in a single report",
            "To identify the expense reports with travel on a Friday/Saturday for a conference in the next week",
            "High Dollar/Expensive purchases beyond certain limit (Ex: Booking first class to avoid luggage fees, expensive furniture from new store etc)",
            "Identify airfare payments/claims for which there are no corresponding hotel or meal charges",
            "Transactions where the employee name does not exist in the Employee Master",
            "Identify  'miscellaneous' expense over $X (per person, if multiple attendees)",
            "Employee Name is same/similar as Merchant Name",
            "Identify travel and entertainment claims that never materialized (i.e. canceled airline tickets, seminars, conferences, conventions, tuition, professional dues)",
            "Expenses incurred in multiple states or currencies on the same day",
            "Search for keywords of Audit Interest and/or phrases in expense descriptions and reports to Identify invalid claims(FCPA,Charitable etc)",
            "Employees/Merchants are on the Fraud watch list/ Restricted List/ FCPA",
            "Employees/Merchants are on the PEP list",
            "Merchants/Vendors on the OFAC watch list",
            "Identify high-risk transactions (i.e. consulting fees, etc.) and/or high- risk personnel (i.e. government officials, agents, consultants, facilitators, etc.)",
            "Segregation of Duties-Identify transactions authorized by same requester",
            "Examine travel expense data to identify employees who consistently claim amounts just below approval thresholds",
            "Late Expense Submission-Submitted date is greater than  or equal to X days after the Transaction date",
            "Expenses Submitted Date before Transaction Date",
            "Identify expenses with no approval",
            "Purchases not on Corporate Card(Out of Pocket Expenses)",
            "Purchases which should be on Corporate Card (Based on Expense type/Description)",
            "Identify personal expenses charged to corporate card",
            "Delay in Approving the report(by X days threshold)",
            "Identify employees who does frequent travels outside the countries of origin",
            "Identify expenses beyond $75 without receipts and summary of corresponding employees,items & service",
            "Transactions where the cardholder has more than one T&E Card in the Card Master file based on exact or similar name matching",
            "Potential Fraud/Invalid transactions: To Identify T&E transactions after the card was reported as lost/stolen or Fraud",
            "Identify non reimbursable expenses(as per the company policy) based on expense type/ spend category/ description based on the policy",
            "All adjustments to employee payments that are created on a weekend",
            'Identify employee IDs that have payment records dated before their hire date or after termination date',
            "Identify employees who don't return credit",
            "Identify reversals/adjusments expenses",
            "Detect merchant with frequent credit transactions",
            "Identify potential split transactions to circumvent card limits (i.e. same or multiple employee(s), merchant and date)",
            "Identify transactions just below approval limits (i.e. within X% of spend limits)",
            "Identify expenses without reciept exceeding a certain limit",
            "Identify expenses that have exceeded the limit by $X",
            "Identify employees exceeding spending limits",
            "Unusual increase in the cardholder’s average spend and/or highest spend amount",
            "Identify patterns of unusually large T&E claims compared to employees in a similar role",
            "Benchmark employee spend against peers",
            "Identify vendors with high number of cash transactions.",
            "Identify vendors with higher activity than others in same MCC",
            "Identify transactions where the MCC is included in Restricted Merchant MCC List",
            "Unauthorized Merchants: Identify transactions where the Merchant Category Code is included in the restricted list ",
            "Identify vendors with similar name and/or address as employee",
            "Identify potential personal expenses flagged under non personal category based on description",
            "Corporate Card expenses made by employees that do not appear in the card holder listing ",
            "Round $ Expense Amount (min amt. 1000, precision =3)",
            "All expenses greater than @amount/High dollar transactions",
            "Identify expenses with missing vendor name/merchant name",
            "Identify transactions with missing crtical information",
            "Mischaracterized expense based on the description",
            "Employees with similar names"
            # Add more prompts here...
    ]

# Main function to handle UI and processing
def main():
    st.set_page_config(layout="wide")
    st.title("Anomaly Detection in Business Processes using Generative AI")
    
    # Initialize session state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'email_sent' not in st.session_state:
        st.session_state.email_sent = False
    if 'query' not in st.session_state:
        st.session_state.query = ""
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        df = load_and_process_data(uploaded_file)

        df_path = 'tagged_anomalies.csv'
        df.to_csv(df_path, index=False)

    openai_client = init_openai_client()
    agent = init_csv_agent(openai_client, 'tagged_anomalies.csv')

    prompts = get_prompts()

    prompt_choice = st.selectbox("Choose a prompt or KRI:", [""] + prompts)
    
    if prompt_choice:
        st.session_state.query = prompt_choice
    
    user_query = st.text_input("Edit or type your query:", value=st.session_state.query)
    
    if st.button("Get Insights"):
        query = user_query + """ Please provide the final command and its output. "Command:" followed by "Output:" """
        st.session_state.query = user_query
        st.write(f"You entered: {user_query}")

        if query:
            try:
                st_callback = StreamlitCallbackHandler(st.container())
                response = agent.run(input={'query': query}, callbacks=[st_callback], handle_parsing_errors=True)
                response_str = str(response)
                
                start_index = response_str.find("Command:") + len("Command:")
                end_index = response_str.find("Output:", start_index)
                
                if start_index != -1 and end_index != -1:
                    command = response_str[start_index:end_index].strip()
                    output = response_str[end_index + len("Output:"):].strip()
                    
                    st.write("Response:", output)

                    if 'command' in locals():
                        try:
                            st.write("Resulting DataFrame:")
                            result = eval(command)
                            st.write(result)
                        except Exception as e:
                            st.error("Failed to execute the command on the DataFrame: " + str(e))
                    else:
                        st.error("No command to execute.")
                else:
                    st.error("Failed to parse the response.")
            
            except Exception as e:
                st.error("Error processing the query: " + str(e))
        else:
            st.warning("Please enter a query to get insights.")

if __name__ == "__main__":
    main()