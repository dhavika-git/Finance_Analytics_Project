import pandas as pd
import numpy as np

accounts = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/accounts.csv')
customers = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/customers.csv')
loans = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/loans.csv')
transaction = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/transactions.csv')

# Calculate total balance per customer?
Total_Balance_per_cus = accounts.groupby('CustomerID')['Balance'].sum()

# Calculate total transaction value per customer?
transaction_customer = pd.merge(transaction,accounts, left_on= 'AccountOriginID', right_on='AccountID', how='inner')
Total_transaction_value_per_cus = transaction_customer.groupby('CustomerID')['Amount'].sum()


# Calculate transaction frequency per customer?
transaction_frequency_per_cus = transaction_customer.groupby('CustomerID')['TransactionID'].size()

# Calculate average transaction value per customer?
avg_transaction_per_cus = transaction_customer.groupby('CustomerID')['Amount'].mean()

# Calculate number of accounts per customer?
merge_acc_customer = pd.merge(accounts,customers, on= 'CustomerID', how='right')
Acc_per_customer = merge_acc_customer.groupby('CustomerID')['AccountID'].size()

# Calculate number of loans per customer?
merge_loan_customer = pd.merge(accounts,loans, on='AccountID', how='right')
Loans_per_customer = merge_loan_customer.groupby('CustomerID')['LoanID'].size()

# Calculate total loan amount per customer?
Total_loan_amt_per_cus = merge_loan_customer.groupby('CustomerID')['PrincipalAmount'].sum()


# create new dataset for adding these customers features 
customer_features = pd.DataFrame(
    {'Total_Balance_per_cus': Total_Balance_per_cus,
     'Total_transaction_value_per_cus': Total_transaction_value_per_cus,
     'transaction_frequency_per_cus': transaction_frequency_per_cus,
     'avg_transaction_per_cus': avg_transaction_per_cus,
     'Acc_per_customer': Acc_per_customer,
     'Loans_per_customer':Loans_per_customer,
     'Total_loan_amt_per_cus': Total_loan_amt_per_cus}
)

# print(customer_features.head())

# reset CustomerID index in customer_feature table
customer_features = customer_features.reset_index()

customer_features.to_csv('')