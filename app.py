import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.presentation.http.server import run_server

if __name__ == "__main__":
    run_server()
