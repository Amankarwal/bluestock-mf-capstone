
-- Bluestock MF Database Schema
-- Aman Karwal | Bluestock Fintech Capstone

CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code         TEXT PRIMARY KEY,
    fund_house        TEXT,
    scheme_name       TEXT,
    category          TEXT,
    sub_category      TEXT,
    plan              TEXT,
    benchmark         TEXT,
    expense_ratio_pct REAL,
    risk_category     TEXT,
    fund_manager      TEXT
);

CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code  TEXT,
    date       DATE,
    nav        REAL,
    PRIMARY KEY (amfi_code, date)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    investor_id      TEXT,
    transaction_date DATE,
    amfi_code        TEXT,
    transaction_type TEXT,
    amount_inr       REAL,
    state            TEXT,
    city_tier        TEXT,
    age_group        TEXT,
    gender           TEXT
);

CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code        TEXT PRIMARY KEY,
    return_1yr_pct   REAL,
    return_3yr_pct   REAL,
    sharpe_ratio     REAL,
    alpha            REAL,
    beta             REAL,
    max_drawdown_pct REAL,
    aum_crore        REAL
);
