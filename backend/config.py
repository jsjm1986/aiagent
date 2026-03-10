import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM - 支持自定义端点
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.4")
    API_KEY = os.getenv("API_KEY", "sk-55PqCVa01WgoCGtM1")
    API_BASE = os.getenv("API_BASE", "http://api.xszwo.com:8080/v1")

    # 兼容旧配置
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # Engine
    LOOP_INTERVAL = 5
    MAX_STEPS = 10

    # Value Assessment
    VALUE_THRESHOLD = 0.6

    # Curiosity
    EXPLORATION_IDLE_THRESHOLD = 300

    # Drives
    DRIVE_DECAY_RATE = 0.95
    DRIVE_ACTIVE_THRESHOLD = 0.3

    # Database
    DATABASE_URL = "sqlite+aiosqlite:///./data/autonomous.db"

    # Paths
    DATA_DIR = "./data"
    CONSCIOUSNESS_DIR = "./data/consciousness"
    CREATIONS_DIR = "./data/creations"
