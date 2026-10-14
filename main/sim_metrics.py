import pandas as pd
import main.sim_config as cfg

def mm1_theory(lam: float, mean_service_min: float) -> dict:
    mu = 1.0 / mean_service_min
    rho = lam / mu
    if rho >= 1: 
        return {"lambda": lam, "mu": mu, "rho": rho, "stable": False}
    lq = rho**2 / (1 - rho)
    return {
        "lambda": lam,
        "mu": mu,
        "rho": rho,
        "Lq": lq,
        "Wq": lq / lam,
        "w": 1 / (mu - lam),
        "stable": True
    }
    
def stage_summary(df_manual: pd.DataFrame, df_digital: pd.DataFrame) -> pd.DataFrame:
    cols =[c for c in df_manual.columns if c.endswith("_min") and c != "arrival_min"]
    rows = []
    for c in cols:
        a, d = df_manual[c].mean(), df_digital[c].mean()
        rows.append(
            {
                "stage": c,
                "manual": round(a,2),
                "digital": round(d,2),
                "saved": round(a - d,2),
                "reduction_pct": round((a-d) / a * 100, 1) if a > 0 else 0.0
            }
        )
    return pd.DataFrame(rows)

def compliance(df: pd.DataFrame) -> dict:
    peak = df[df["arrival"] < 60]
    return {
        "within_150_pct": round((df["total_opd_min"] <= cfg.OPD_TARGET_MIN). mean() * 100, 1),
        "within_180_pct": round((df["total_opd_min"] <= cfg.WAITING_TARGET_MIN). mean() * 100, 1),
        "peak_within_150_pct": round((peak["total_opd_min"] <= cfg.OPD_TARGET_MIN). mean() * 100, 1),
        "n_peak": len(df)
    }