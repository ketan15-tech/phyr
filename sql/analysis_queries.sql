-- Phyr Studios Internship Assessment - SQL Analysis
-- Load sales_cleaned.csv into a SQL table named `sales`.

SELECT SUM(Sales) AS Total_Sales FROM sales;

SELECT SUM(Profit) AS Total_Profit FROM sales;

SELECT Category, SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC;

SELECT Region, SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC;

SELECT Product, SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Product
ORDER BY Total_Sales DESC
LIMIT 5;

SELECT AVG(Sales) AS Average_Order_Value
FROM sales;

SELECT Customer, COUNT(DISTINCT Order_ID) AS Number_of_Orders,
       SUM(Sales) AS Customer_Sales
FROM sales
GROUP BY Customer
ORDER BY Customer_Sales DESC
LIMIT 10;

-- JOIN example (when a separate customers table is available):
-- SELECT s.Order_ID, s.Customer, c.Customer_Segment
-- FROM sales s
-- LEFT JOIN customers c ON s.Customer = c.Customer;
