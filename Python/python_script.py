import pandas as pd
import numpy as np

accounts = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/accounts.csv')
customers = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/customers.csv')
lones = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/loans.csv')
transaction = pd.read_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/transactions.csv')


# print(np.shape(accounts))
# print(np.size(accounts))
# print(np.ndim(accounts))

# print(accounts.info())
# print(accounts.describe())
# print(accounts.info())
# print(accounts.head())
# print(accounts.tail())

''' data cleaning '''

'''Check data types and convert them to the correct format'''

# print(accounts.dtypes)                                    # accounts dataset

# accounts['OpeningDate'] = pd.to_datetime(accounts['OpeningDate']) 
# # print(accounts.dtypes)

# print(customers.info())                                   # customer dataset
# print(customers.describe())
# print(customers.dtypes)

customers['DateOfBirth'] = pd.to_datetime(customers['DateOfBirth'], format= 'mixed', errors= 'coerce')  # tha data_column is having invalid date which is not possible

# print(lones.info())                                     # lones dataset
# print(lones.describe())                                 

# lones['StartDate'] = pd.to_datetime(lones['StartDate'], format= 'mixed', errors= 'coerce')

# print(transaction.info())                                     # transaction dataset
# print(transaction.describe())                                 

# transaction['TransactionDate'] = pd.to_datetime(transaction['TransactionDate'], format= 'mixed', errors= 'coerce')

'''check null values in all datasets (in %)'''

# print((pd.isnull(accounts).sum() / len(accounts) * 100).round(2))
# print(f"\n")
# print((pd.isnull(lones).sum()/ len(lones) * 100).round(2))
# print(f"\n")
# print((pd.isnull(transaction).sum()/ len(transaction) * 100).round(2))

# accounts = accounts.fillna(0)                      # flag the null values using '0'
# customers = customers.fillna(0)
# lones = lones.fillna(0)
# transaction = transaction.fillna(0)

''' Handeling Duplicate values '''

# print(accounts.duplicated().sum())
# print(customers.duplicated().sum())
# print(lones.duplicated().sum())
# print(transaction.duplicated().sum())

# accounts = accounts.drop_duplicates()
# lones = lones.drop_duplicates()
# customers = customers.drop_duplicates()
# transaction = transaction.drop_duplicates()

''' check data consistency '''
# print(customers['FirstName'].str.istitle())
# print(customers['LastName'].str.istitle())

# print((lones['InterestRate'] < 0).any())
# print((accounts['Balance'] < 0).any())              # have some negative balance
# print((transaction['Amount'] < 0).any())
# print((accounts['Balance'] < 0).sum())

# save the changed data
# customers.to_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/customers.csv', index=False)

# print(customers['CustomerID'].unique().sum())

customers['Age'] = (pd.Timestamp.today() - customers['DateOfBirth']).dt.days // 365
customers.to_csv('/Users/utsavsharma/Desktop/Analytics_Projects/Finance_Analytics_Project/datasets/customers.csv', index=False)

# print((customers['Age']).head(5)) 
# print(customers['Age'].mean())            # avg age = 45.677509293680295
# print(customers['Age'].median())            # median = 46.0

''' Which CustomerTypeID is most common? '''
print(customers.groupby(customers['CustomerTypeID']).size())            # ID 3 -   397


''' Accounts EDA '''
# How many accounts exist?
accounts['AccountID'].unique()

# How many unique customers have accounts?
# What account types exist?
# Which account type is most common?
# What is the total account balance?
# What is the average account balance?
# What is the median balance?
# Which customers have multiple accounts?
# What is the average number of accounts per customer?
# Which account type has the highest average balance?
# Which account type holds the largest total balance?
