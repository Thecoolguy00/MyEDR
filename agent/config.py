from dotenv import load_dotenv
load_dotenv()

import os

SERVER_URL=os.getenv("MYEDR_SERVER_URL", "http://localhost:8000")

REGISTER_ENDPOINT=(f"{SERVER_URL}/api/v1/devices/register")

REQUEST_TIMEOUT=15.0