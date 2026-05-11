import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.database import DB_PATH, init_database  # noqa: E402


if __name__ == "__main__":
    init_database()
    print(f"Banco SQLite pronto em: {DB_PATH}")
