from dataclasses import dataclass

OPEN_HOURS: float = 7.0
OPERATING_WINDOWS: float = OPEN_HOURS * 60.0
REG_PATIENTS_PER_DAY: float = 66.0
REG_ARRIVAL_RATE_PER_MIN: float = REG_PATIENTS_PER_DAY / OPERATING_WINDOWS
CONSULT_MEAN_MIN: float = 15.0
WALK_TIME_MEAN: float = 2.0
POST_CONSULT_MIN: float = 15.0
N_DAYS: int = 25
RANDOM_SEED: int = 42

OPD_TARGET_MIN: float = 150.0
WAITING_TARGET_MIN: float = 180.0

@dataclass(frozen=True)
class ScenarioConfig:
    name: str
    checkin_mean_min: float
    announcement_mean_min: float
    reg_service_mean_min: float
    
SCENARIO_MANUAL = ScenarioConfig(
    name="manual",
    checkin_mean_min= 3.5,
    announcement_mean_min= 1.5,
    reg_service_mean_min= 5.0
)

SCENARIO_DIGITAL = ScenarioConfig(
    name="digital",
    checkin_mean_min= 0.67,
    announcement_mean_min= 0.0,
    reg_service_mean_min= 3.0
)