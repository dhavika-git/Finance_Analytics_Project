import pandas as pd
import numpy as np

accounts = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/accounts.csv')
customers = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/customers.csv')
loans = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/loans.csv')
transaction = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/transactions.csv')


print(np.shape(accounts))
print(np.size(accounts))
print(np.ndim(accounts))

print(accounts.info())
print(accounts.describe())
print(accounts.head())
print(accounts.tail())

''' data cleaning '''

'''Check data types and convert them to the correct format'''

print(accounts.dtypes)                                    # accounts dataset

accounts['OpeningDate'] = pd.to_datetime(accounts['OpeningDate']) 
# print(accounts.dtypes)

print(customers.info())                                   # customer dataset
print(customers.describe())
print(customers.dtypes)

customers['DateOfBirth'] = pd.to_datetime(customers['DateOfBirth'], format= 'mixed', errors= 'coerce')  # tha data_column is having invalid date which is not possible

print(loans.info())                                     # loans dataset
print(loans.describe())                                 

loans['StartDate'] = pd.to_datetime(loans['StartDate'], format= 'mixed', errors= 'coerce')
loans['EstimatedEndDate'] = pd.to_datetime(loans['EstimatedEndDate'], format='mixed', errors='coerce')

print(transaction.info())                                     # transaction dataset
print(transaction.describe())                                 

transaction['TransactionDate'] = pd.to_datetime(transaction['TransactionDate'], format= 'mixed', errors= 'coerce')

'''check null values in all datasets (in %)'''

print((pd.isnull(accounts).sum() / len(accounts) * 100).round(2))
print(f"\n")
print((pd.isnull(loans).sum()/ len(loans) * 100).round(2))
print(f"\n")
print((pd.isnull(transaction).sum()/ len(transaction) * 100).round(2))



''' Handeling Duplicate values '''

print(accounts.duplicated().sum())
print(customers.duplicated().sum())
print(loans.duplicated().sum())
print(transaction.duplicated().sum())


''' check data consistency '''
print(customers['FirstName'].str.istitle())
print(customers['LastName'].str.istitle())

print((loans['InterestRate'] < 0).any())
print((accounts['Balance'] < 0).any())              # have some negative balance
print((transaction['Amount'] < 0).any())
print((accounts['Balance'] < 0).sum())


print(customers['CustomerID'].nunique())            # unique customers

customers['Age'] = (pd.Timestamp.today() - customers['DateOfBirth']).dt.days // 365

# save the changed data
customers.to_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/customers.csv', index=False)

print((customers['Age']).head(5)) 
print(customers['Age'].mean())            # avg age = 45.677509293680295
print(customers['Age'].median())            # median = 46.0

''' Which CustomerTypeID is most common? '''
print(customers.groupby(customers['CustomerTypeID']).size())            # ID 3 -   397


''' Accounts EDA Process'''
# How many accounts exist?
accounts['AccountID'].unique()

# How many unique customers have accounts?
unique_customers_have_accounts = customers[customers['CustomerID'].isin(accounts['CustomerID'])]['CustomerID'].unique()
# print(unique_customers_have_accounts)


# What account types exist?
account_types = sorted(accounts['AccountTypeID'].unique())
# print(account_types)

# Which account type is most common?
comman_account_type = accounts.groupby(accounts['AccountTypeID']).size()
# print(comman_account_type)

# What is the total account balance?
# print("Total Balance = ",accounts['Balance'].sum())

# What is the average account balance?
# print("Avg Balance = ",accounts['Balance'].mean())

# What is the median balance?
# print("Avg Balance = ",accounts['Balance'].median())

# Which customers have multiple accounts?
customer_multiple_account = (accounts['CustomerID']).value_counts() > 1
# print(customer_multiple_account.count())

# What is the average number of accounts per customer?
avg_acc_per_customer = accounts.groupby(accounts['CustomerID']).size()
# print(avg_acc_per_customer.mean())

# Which account type has the highest average balance?
acc_type_has_highest_avg_balance = accounts.groupby('AccountTypeID')['Balance'].mean()
# print(acc_type_has_highest_avg_balance.sort_values(ascending=False))

# Which account type holds the largest total balance?
acc_type_has_highest_balance = accounts.groupby('AccountTypeID')['Balance'].sum()
# print(acc_type_has_highest_balance.sort_values(ascending=False))

''' Transaction EDA Process '''
# Transaction count
# print('Total Transaction Count: ',transaction['TransactionID'].count())

# Total/average transaction amount
# print('Total Transaction Amount: ',transaction['Amount'].sum(),' & Avg Transaction Amount: ', transaction['Amount'].mean())

# Transaction type distribution
# print('Transaction type distribution: ',transaction.groupby('TransactionTypeID').size())

# High-value transactions
# print((transaction['Amount'].sort_values(ascending=False)).head(1))

# Transaction trends over time
transaction['Month'] = transaction['TransactionDate'].dt.to_period('M')
print(transaction['Month'].sort_values())

''' Loan EDA Process'''
# Number of loans
# print('No of loans: ', loans['LoanID'].count())

# Average loan amount
# print('Avg loan amount: ', loans['PrincipalAmount'].mean())

# Average interest rate
# print('Avg interest rate: ', loans['InterestRate'].mean())

# Loan status distribution
# print('Loan status distribution: ', loans.groupby('LoanStatusID').size())

# Loan amount by status
# print('Loan amount by status: ', loans.groupby('LoanStatusID')['PrincipalAmount'].sum() )

''' check IDs uniqueness '''
print(accounts['AccountID'].nunique())
print(customers['CustomerID'].nunique())
print(loans['LoanID'].nunique())
print(transaction['TransactionID'].nunique())

print(accounts['AccountID'].is_unique)
print(customers['CustomerID'].is_unique)
print(loans['LoanID'].is_unique)
print(transaction['TransactionID'].is_unique)

''' drop duplicates '''
accounts = accounts.drop_duplicates()
loans = loans.drop_duplicates()
customers = customers.drop_duplicates()
transaction = transaction.drop_duplicates()

print(accounts['AccountID'].is_unique)
print(customers['CustomerID'].is_unique)
print(loans['LoanID'].is_unique)
print(transaction['TransactionID'].is_unique)

#  save the chnages
accounts.to_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/accounts.csv', index=False)
customers.to_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/customers.csv', index=False)
loans.to_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/loans.csv', index=False)
transaction.to_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/transactions.csv', index=False)
