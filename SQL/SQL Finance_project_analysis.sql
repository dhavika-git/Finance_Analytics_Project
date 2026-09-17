create database finance_analytics;
Use finance_analytics;

-- How many customers are in the database?
select count(*) as total_customers from customers;   
-- total customers = 1076

-- How many accounts?
select count(*) as total_acc from accounts; 
-- total accounts = 1651

-- How many transactions?
select count(*) as total_transactions from transactions; 
-- total_transactions = 49500

-- How many loans?
select count(*) as total_loans from loans; 
-- total_loans = 330

-- What are the different account types?
select AccountTypeID from accounts
Group by AccountTypeID
order by AccountTypeID;

-- What are the different loan status?
select LoanStatusID from loans
Group by LoanStatusID
order by LoanStatusID;

-- What are the different transaction types?
select TransactionTypeID from transactions
Group by TransactionTypeID
order by TransactionTypeID;

-- Which customers are above a particular income level?
select * from customers
join accounts using(CustomerID)
join transactions
on accounts.AccountID = transactions.AccountOriginID
where transactions.amount > 1000;

-- Which loans are above a particular amount?
select LoanID from loans
where PrincipalAmount > 50000;

-- What are the highest-value transactions?
select max(Amount) from transactions;
-- highest-value transactions = 4999.59

-- What are the highest-value loans?
select max(PrincipalAmount) from loans;
-- highest-value loans = 99830.33

-- How many accounts does each customer have?
select c.CustomerID, count(AccountID) from customers as c
join accounts as a
on c.CustomerID = a.CustomerID
Group by c.CustomerID;

-- What is the total balance by account type?
select AccountTypeID, sum(Balance) from accounts
Group by AccountTypeID;

-- What is the average balance by account type?
select AccountTypeID, avg(Balance) from accounts
Group by AccountTypeID;

-- How many transactions occur by transaction type?
select TransactionTypeID, count(TransactionID) from transactions
Group by TransactionTypeID;

-- What is the total transaction value by transaction type?
select TransactionTypeID, sum(Amount) from transactions
Group by TransactionTypeID;

-- What is the transaction value by account?
select accounts.AccountID, sum(transactions.Amount) as transaction_value from transactions
join accounts
on accounts.AccountID = transactions.AccountOriginID
Group by accounts.AccountID;

-- What is the total loan amount by loan type?
select sum(PrincipalAmount) from loans;

-- What is the average loan amount by loan type?
select LoanStatusID,avg(PrincipalAmount) from loans
Group by LoanStatusID;

-- How many loans does each customer have?
select c.CustomerID, count(l.LoanID) from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by c.CustomerID;

-- What is the total loan exposure per customer?
select c.CustomerID, sum(l.PrincipalAmount) from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by c.CustomerID;

-- Which customers have accounts?
select customers.CustomerID from customers
join accounts on customers.CustomerID = accounts.CustomerID
Group by customers.CustomerID;

-- Which customers don't have accounts?
select CustomerID from customers where CustomerID not in (select CustomerID from accounts);

-- Which customers have loans?
select * from customers where CustomerID in (select CustomerID from accounts where AccountID in (select AccountID from loans));

-- Which customers don't have loans?
select * from customers where CustomerID not in (select CustomerID from accounts where AccountID in (select AccountID from loans));

-- What is each customer's total balance?
select CustomerID, sum(Balance) from accounts
Group by CustomerID;

-- What is each customer's total transaction value?
select customers.CustomerID, sum(transactions.Amount) from customers 
join accounts on customers.CustomerID = accounts.CustomerID
join transactions on accounts.AccountID = transactions.AccountOriginID
Group by customers.CustomerID;

-- What is each customer's total loan exposure?
select c.CustomerID,sum(l.PrincipalAmount) as TotalLoanExposure from customers AS c
join accounts AS a on c.CustomerID = a.CustomerIDa
join loans AS l on a.AccountID = l.AccountID
Group BY c.CustomerID;

-- Which customers have both accounts and loans?
select customers.CustomerID from customers 
join accounts on customers.CustomerID = accounts.CustomerID 
join loans  on accounts.AccountID = loans.AccountID ;

-- Which customers have high transaction activity and loans?
select customers.CustomerID, count(DISTINCT transactions.TransactionID) as Transaction, count(DISTINCT loans.LoanID) as loan from customers 
join accounts on customers.CustomerID = accounts.CustomerID
join transactions on accounts.AccountID = transactions.AccountOriginID
join loans on accounts.AccountID = loans.AccountID
Group by customers.CustomerID
Order by count(transactions.TransactionID) desc, count(loans.LoanID) desc;

-- Who are the top 10 customers by transaction value?
select customers.CustomerID, sum(transactions.Amount) from customers 
join accounts on customers.CustomerID = accounts.CustomerID
join transactions on accounts.AccountID = transactions.AccountOriginID
Group by customers.CustomerID
Order by sum(transactions.Amount) desc
Limit 10;

-- Rank customers by total loan exposure.
select RANK() over (order by sum(l.PrincipalAmount) desc) as rnk, c.CustomerID, sum(l.PrincipalAmount) as loanAmount from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by c.CustomerID;

-- Rank customers within each loan type.
select RANK() over (order by sum(l.PrincipalAmount) desc) as rnk, l.LoanStatusID, sum(l.PrincipalAmount) as loanAmount from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by l.LoanStatusID;

-- Find customers with more than one loan.
select c.CustomerID, count(l.LoanID) from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by c.CustomerID
having count(l.LoanID) > 1;

-- Find customers whose loan exposure is above the average. ????
select customers.CustomerID,sum(loans.PrincipalAmount) from customers 
join accounts on customers.CustomerID = accounts.CustomerID 
join loans  on accounts.AccountID = loans.AccountID 
Group by customers.CustomerID
having sum(loans.PrincipalAmount) > avg(loans.PrincipalAmount) ;

-- Find customers whose transaction activity is above average.????
select customers.CustomerID,sum(transactions.Amount) from customers 
join accounts on customers.CustomerID = accounts.CustomerID 
join transactions  on accounts.AccountID = transactions.AccountOriginID 
Group by customers.CustomerID
having sum(transactions.Amount) > avg(transactions.Amount) ;

-- Find each customer's previous transaction.
select a.CustomerID, t.TransactionID, t.Amount, t.TransactionDate, LAG(t.Amount) OVER 
(PARTITION by a.CustomerID ORDER BY t.TransactionDate) AS Previous_Transaction
FROM accounts AS a JOIN transactions AS t
ON a.AccountID = t.AccountOriginID;

-- Calculate changes in transaction activity over time.
select TransactionID, Amount, LAG(Amount) over(ORDER by TransactionDate) as date,  (Amount - LAG(Amount) over(ORDER by TransactionDate)) as Diff
from transactions;

-- Calculate running transaction totals.
select TransactionID, Amount, sum(Amount)over(ORDER by TransactionDate) as total, LAG(Amount) over(ORDER by TransactionDate) as date
from transactions;

-- Find the highest transaction for each customer.???
select accounts.CustomerID, transactions.TransactionID, max(transactions.Amount) from accounts
JOIN transactions ON accounts.AccountID = transactions.AccountOriginID
Group by accounts.CustomerID, transactions.TransactionID;

-- Find the second-highest loan/customer exposure.
select * from ( select c.CustomerID, max(l.PrincipalAmount) , RANK() over(order by max(l.PrincipalAmount) desc) as rnk from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by c.CustomerID) as customer_exposure
where rnk = 2;

-- Identify customers falling into the top 10% of loan exposure.
select c.CustomerID, max(l.PrincipalAmount) as maz_amount, NTILE(10) over(order by max(l.PrincipalAmount) desc) as grp from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by c.CustomerID
order by max(l.PrincipalAmount) desc
Limit  1;

-- Which customers have high loan exposure?
select * from ( select c.CustomerID, max(l.PrincipalAmount) , RANK() over(order by max(l.PrincipalAmount) desc) as rnk from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by c.CustomerID) as customer_exposure;

-- Which customers have high loans but low balances?
select c.CustomerID, a.AccountID, max(l.PrincipalAmount), a.Balance from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by c.CustomerID, a.Balance,  a.AccountID
Order by max(l.PrincipalAmount) desc ,  a.Balance asc;

-- Which customers have unusually high transaction activity?
select customers.CustomerID, count(DISTINCT transactions.TransactionID) as Transaction from customers 
join accounts on customers.CustomerID = accounts.CustomerID
join transactions on accounts.AccountID = transactions.AccountOriginID
Group by customers.CustomerID
Order by count(transactions.TransactionID) desc;

-- Which customers have multiple risk indicators?
select customers.CustomerID, count(DISTINCT transactions.TransactionID) as Transaction, count(DISTINCT loans.LoanID) as loan from customers 
join accounts on customers.CustomerID = accounts.CustomerID
join transactions on accounts.AccountID = transactions.AccountOriginID
join loans on accounts.AccountID = loans.AccountID
Group by customers.CustomerID
Order by count(transactions.TransactionID) desc, count(loans.LoanID) desc;

-- Which loan types contribute most to exposure?
select LoanStatusID, sum(PrincipalAmount) from loans
Group by LoanStatusID
order by LoanStatusID;

-- Which customer segment has the highest loan exposure?
select sum(l.PrincipalAmount), c.CustomerTypeID from customers as c
join accounts as a on c.CustomerID = a.CustomerID
join loans as l on a.AccountID = l.AccountID
Group by c.CustomerTypeID;


select * from accounts;
select * from customers;
select * from loans;
select * from transactions;
