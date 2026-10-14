import numpy as np
import pandas as pd

import main.sim_config as cfg
from main.sim_config import ScenarioConfig

def generate_daily_arrivals(rng: np.random.Generator, rate: float, horizon: float) -> np.ndarray:
    n = rng.poisson(rate * horizon)
    return np.sort(rng.uniform(0, horizon,n))

def simulate_fifo_queue(arrivals: np.ndarray, service_times: np.ndarray) -> pd.DataFrame:
    n = len(arrivals)
    start = np.zeros(n)
    depart = np.zeros(n)
    
    prev_depart = 0.0
    
    for i in range (n):
        start[i] = max(arrivals[i], prev_depart)
        depart[i] = start[i] + service_times[i]
        prev_depart = depart[i]
        
    return pd.DataFrame({
        "arrival": arrivals,
        "start": start,
        "wait": start - arrivals,
        "depart": depart,
    })
    
def simulate_day(day: int, scenario: ScenarioConfig, base_seed: int = cfg.RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(base_seed + day)
    arrivals = generate_daily_arrivals(rng, cfg.REG_ARRIVAL_RATE_PER_MIN, cfg.OPERATING_WINDOWS)
    n = len(arrivals)
    
    unit_reg = rng.exponential(1.0, n)
    unit_consult = rng.exponential(1.0, n)
    unit_checkint = rng.exponential(1.0, n)
    unit_announcement = rng.exponential(1.0, n)
    
    reg_service = unit_reg * scenario.reg_service_mean_min
    queue = simulate_fifo_queue(arrivals, reg_service)
    
    df = pd.DataFrame({
        "day": day,
        "arrival": arrivals,
        "check_min": unit_checkint * scenario.checkin_mean_min,
        "announcement_min": unit_announcement * scenario.announcement_mean_min,
        "reg_wait_min": queue["wait"].values,
        "reg_service_min": reg_service,
        "walk_min": unit_consult * cfg.WALK_TIME_MEAN,
        "post_consult_min": cfg.POST_CONSULT_MIN,
    })
    
    stage_cols = [c for c in df.columns if c.endswith("_min") and  c != "arrival_min"]
    df["total_opd_min"] = df[stage_cols].sum(axis=1)   
    return df

def run_replication(scenario: ScenarioConfig, n_days: int = cfg.N_DAYS) -> pd.DataFrame:
    out = pd.concat([simulate_day(d, scenario) for d in range(n_days)], ignore_index=True)
    out["scenario"] = scenario.name
    return out