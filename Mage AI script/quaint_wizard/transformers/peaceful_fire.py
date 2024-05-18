import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform_data(expensemaster, traveldata, holidayslist, employeemaster, cardmaster, suspiciouskeywords, flightclasses , *args, **kwargs):
    """
    Custom transformation block to integrate and process the loaded datasets.
    """
    import pandas as pd

    # Remove all empty columns
    expensemaster = expensemaster.dropna(axis=1, how='all')

    # Filter expense master data
    expensemaster_cleaned = expensemaster[(expensemaster['ReportingAmount'] != 0) | (expensemaster['ApprovalStatus'] != 'No')]
    expensemaster_cleaned['TransactionDate'] = pd.to_datetime(expensemaster_cleaned['TransactionDate'], errors='coerce')

    # Prepare travel data
    traveldata.rename(columns={'Transaction date': 'TransactionDate', 'Ticket number': 'TicketNumber'}, inplace=True)
    traveldata['TransactionDate'] = pd.to_datetime(traveldata['TransactionDate'], errors='coerce')

    def find_closest_transaction(row):
        same_ticket_df = traveldata[traveldata['TicketNumber'] == row['TicketNumber']]
        if same_ticket_df.empty:
            return pd.Series([None] * len(columns_to_keep), index=columns_to_keep)
        time_diff = (same_ticket_df['TransactionDate'] - row['TransactionDate']).abs()
        idx_min = time_diff.idxmin()
        return same_ticket_df.loc[idx_min, columns_to_keep]

    columns_to_keep = ['Booking Date', 'Transaction type', 'Domestic / International', 'Travel start date', 'Travel end date', 'Booking Reference/PNR', 'Origin city', 'Destination city', 'Class of service']
    closest_transactions = expensemaster_cleaned.apply(find_closest_transaction, axis=1, result_type='expand')
    expensemaster_cleaned = pd.concat([expensemaster_cleaned, closest_transactions], axis=1)

    # Merge holiday data
    holidayslist['Date'] = pd.to_datetime(holidayslist['Date'].astype(str).str.replace("/", "-"), errors='coerce')
    holidayslist = holidayslist.drop_duplicates(subset='Date', keep='first')
    expensemaster_cleaned = pd.merge(expensemaster_cleaned, holidayslist[['Date', 'HolidayCountry', 'HolidayName']], left_on='TransactionDate', right_on='Date', how='left')
    expensemaster_cleaned.drop('Date', axis=1, inplace=True)

    # Categorize suspicious transactions
    expensemaster_cleaned['Suspicion_Category'] = 'Not Suspicious'
    for index, row in suspiciouskeywords.iterrows():
        keyword = row['KeywordInEnglish']
        category = row['Category']
        mask = expensemaster_cleaned['ExpenseType'].str.contains(keyword, case=False, na=False)
        expensemaster_cleaned.loc[mask, 'Suspicion_Category'] = category

    # Merge employee data
    columns_to_merge = ['EmployeeID', 'EmployeeAddress', 'EmployeeStatus', 'EmploymentType', 'EmployeeDesignation', 'HireDate', 'TerminationDate', 'CostCenter', 'IsExecutive']
    expensemaster_cleaned = pd.merge(expensemaster_cleaned, employeemaster[columns_to_merge], on='EmployeeID', how='left')

    # Map flight class descriptions
    code_to_class_map = flightclasses.set_index('Code')['Class'].to_dict()
    expensemaster_cleaned['FlightClassDescription'] = expensemaster_cleaned['Class of service'].map(code_to_class_map)

    # Clean and merge card data
    cardmaster['IssuedDate'] = pd.to_datetime(cardmaster['IssuedDate'].astype(str).str.replace('/', '-'), errors='coerce')
    if 'EmployeeID/Number' in cardmaster.columns and 'EmployeeID' not in cardmaster.columns:
        cardmaster.rename(columns={'EmployeeID/Number': 'EmployeeID'}, inplace=True)
    cardmaster.sort_values(by=['EmployeeID', 'IssuedDate'], ascending=[True, False], inplace=True)
    cardmaster = cardmaster.drop_duplicates(subset='EmployeeID', keep='first')
    card_info_columns = ['EmployeeID', 'CardHolderFullName', 'IssuedDate', 'CardExpiryDate', 'CardCloseDate', 'CardStatus', 'CardStatusReason']
    expensemaster_cleaned = pd.merge(expensemaster_cleaned, cardmaster[card_info_columns], on='EmployeeID', how='left')

    # Clean date columns
    date_columns_to_clean = ['EntryDate', 'Booking Date', 'Travel start date', 'Travel end date', 'HireDate', 'CardExpiryDate', 'CardCloseDate']
    for col in date_columns_to_clean:
        if col in expensemaster_cleaned.columns:
            expensemaster_cleaned[col] = pd.to_datetime(expensemaster_cleaned[col].astype(str).str.replace('/', '-'), errors='coerce')

    # Ensure 'TransactionDate' is in datetime format
    expensemaster_cleaned['TransactionDate'] = pd.to_datetime(expensemaster_cleaned['TransactionDate'], errors='coerce')

    # Create the 'TransactionDay' column with the day name of the week
    expensemaster_cleaned['TransactionDay'] = expensemaster_cleaned['TransactionDate'].dt.day_name()

    # Drop any duplicate rows
    expensemaster_cleaned.drop_duplicates(inplace=True)

    return expensemaster_cleaned

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert isinstance(output, pd.DataFrame), 'The output is not a DataFrame'
    assert not output.empty, 'The DataFrame is empty'