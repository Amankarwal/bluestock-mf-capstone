# Data Dictionary — Bluestock MF Capstone
## Aman Karwal | Bluestock Fintech 2026

## dim_fund
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Unique fund code from AMFI |
| fund_house | TEXT | AMC name (SBI, HDFC etc.) |
| scheme_name | TEXT | Full fund name |
| category | TEXT | Equity / Debt / Hybrid |
| expense_ratio_pct | REAL | Annual fee % charged to investor |
| risk_category | TEXT | Low / Moderate / High / Very High |

## fact_nav
| Column | Type | Description |
|--------|------|-------------|
| amfi_code | TEXT | Foreign key to dim_fund |
| date | DATE | Trading date |
| nav | REAL | Net Asset Value in Rs. |

## fact_transactions
| Column | Type | Description |
|--------|------|-------------|
| investor_id | TEXT | Unique investor ID |
| transaction_date | DATE | Date of SIP/Lumpsum/Redemption |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | REAL | Transaction amount in Rupees |
| state | TEXT | Investor state |
| city_tier | TEXT | T30 or B30 city |
| age_group | TEXT | 18-25 / 26-35 / 36-45 / 46-55 / 56+ |

## fact_performance
| Column | Type | Description |
|--------|------|-------------|
| return_3yr_pct | REAL | 3 year CAGR return % |
| sharpe_ratio | REAL | Risk adjusted return (>1 = good) |
| alpha | REAL | Extra return above benchmark |
| beta | REAL | Market sensitivity (1=same as market) |
| max_drawdown_pct | REAL | Worst peak to trough loss % |
| aum_crore | REAL | Assets under management in crore |
