import pandas as pd

CSV = r"C:\Users\Aman Karwal\Downloads\bluestock-mf-capstone\\"
fund_master = pd.read_csv(CSV + "01_fund_master.csv")
performance = pd.read_csv(CSV + "07_scheme_performance.csv")

def recommend_funds(risk_appetite, top_n=3):
    risk_map = {
        "Low"     : ["Low", "Low to Moderate"],
        "Moderate": ["Moderate", "Moderately High"],
        "High"    : ["High", "Very High"]
    }
    valid = risk_map.get(risk_appetite, ["Moderate"])
    eligible = fund_master[fund_master["risk_category"].isin(valid)]
    merged   = eligible.merge(performance, on="amfi_code")
    ranked   = merged.sort_values("sharpe_ratio", ascending=False)
    return ranked[["scheme_name","fund_house","sharpe_ratio",
                   "return_3yr_pct","expense_ratio_pct"]].head(top_n)

if __name__ == "__main__":
    for risk in ["Low", "Moderate", "High"]:
        print(f"\nTop 3 funds for {risk} risk:")
        print(recommend_funds(risk).to_string(index=False))
