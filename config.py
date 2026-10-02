import os
from pathlib import Path


def load_env(stand: str) -> dict:
    env_file = Path(__file__).parent / "envs" / f"{stand}.env"
    if not env_file.exists():
        raise FileNotFoundError(f"Не найден конфиг стенда: {env_file}")

    config = {}
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        config[key.strip()] = value.strip()
    return config


def get_base_url(stand: str) -> str:
    env = load_env(stand)
    base_url = env.get("BASE_URL") or os.getenv("BASE_URL")
    if not base_url:
        raise ValueError(f"BASE_URL не задан в envs/{stand}.env")
    return base_url