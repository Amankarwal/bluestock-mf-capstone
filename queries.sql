
-- Bluestock MF - 10 Analytical Queries
-- Aman Karwal | Bluestock Fintech Capstone

-- Q1: Top 5 funds by AUM
SELECT scheme_name, fund_house, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC LIMIT 5;

-- Q2: Cheap funds (expense ratio < 1%)
SELECT scheme_name, expense_ratio_pct
FROM dim_fund WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct;

-- Q3: Transaction count by type
SELECT transaction_type, COUNT(*) as count,
       ROUND(SUM(amount_inr)/100000,2) as total_lakh
FROM fact_transactions GROUP BY transaction_type;

-- Q4: Top 5 states by SIP amount
SELECT state, ROUND(SUM(amount_inr)/100000,2) as total_lakh
FROM fact_transactions WHERE transaction_type='SIP'
GROUP BY state ORDER BY total_lakh DESC LIMIT 5;

-- Q5: Funds with Sharpe > 1
SELECT scheme_name, sharpe_ratio, return_3yr_pct
FROM fact_performance WHERE sharpe_ratio > 1
ORDER BY sharpe_ratio DESC;

-- Q6: Monthly avg NAV for SBI Bluechip
SELECT SUBSTR(date,1,7) as month, ROUND(AVG(nav),2) as avg_nav
FROM fact_nav WHERE amfi_code=119551
GROUP BY month ORDER BY month DESC LIMIT 12;

-- Q7: AUM by fund house
SELECT fund_house, ROUND(SUM(aum_crore),0) as total_aum
FROM fact_performance GROUP BY fund_house
ORDER BY total_aum DESC;

-- Q8: Gender wise avg SIP
SELECT gender, ROUND(AVG(amount_inr),0) as avg_sip
FROM fact_transactions WHERE transaction_type='SIP'
GROUP BY gender;

-- Q9: T30 vs B30
SELECT city_tier, COUNT(*) as count,
       ROUND(AVG(amount_inr),0) as avg_amount
FROM fact_transactions GROUP BY city_tier;

-- Q10: Fund name + performance JOIN
SELECT d.scheme_name, p.return_3yr_pct, p.sharpe_ratio
FROM dim_fund d JOIN fact_performance p
ON d.amfi_code = p.amfi_code
ORDER BY p.return_3yr_pct DESC LIMIT 10;
