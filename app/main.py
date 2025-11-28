import threading
import subprocess
from time import sleep
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
import time
from dotenv import load_dotenv

load_dotenv()

logger = get_logger(__name__)


def run_backend():
    try:
        subprocess.run(['uvicorn', 'app.backend.api:app',
                        '--host', '127.0.0.1', '--port', '9999'], check=True)
        logger.info("Backend server started in a separate thread.")
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")
        raise CustomException("Error starting backend") from e


def run_frontend():
    try:
        subprocess.run(['streamlit', 'run', 'app/frontend/ui.py'], check=True)
        logger.info("Frontend server started in a separate thread.")
    except Exception as e:
        logger.error(f"Failed to start frontend: {e}")
        raise CustomException("Error starting frontend") from e


if __name__ == '__main__':
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        logger.info("Backend started")
        run_frontend()
        logger.info("Frontend started")

    except CustomException as e:
        logger.error(f"error in running the service")
        raise CustomException(f"failed the run the service")
