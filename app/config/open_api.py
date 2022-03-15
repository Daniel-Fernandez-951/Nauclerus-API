
# OpenAPI and Doc settings
import os

from dotenv import load_dotenv

load_dotenv()

# Moesif settings
MOESIF_API_KEY = os.getenv('MOESIF_API')
# Elastic settings
SERVICE_NAME = os.getenv('ELASTIC_SERVICE_NAME')
SECRET_TOKEN = os.getenv('ELASTIC_SECRET_TOKEN')
SERVER_URL = os.getenv('ELASTIC_SERVER_URL')
ELASTIC_ENV = os.getenv('ELASTIC_ENV')


MOESIF_ON = os.getenv('MOESIF_ON')
ELASTIC_ON = os.getenv('ELASTIC_ON')

# Check for API Mon. conflict
if MOESIF_ON and ELASTIC_ON == '1':
    MOESIF_ON, ELASTIC_ON = '0', '0'
    print(f"MOE = {type(MOESIF_ON)}, {MOESIF_ON}\nELASTIC = {type(ELASTIC_ON)}, {ELASTIC_ON}")


LOGO_PATH = "/app/logo/logo2-nauclerusAPIV1_dark.png"
API_VERSION = "0.2.5"
TAGS_METADATA = [
    {"name": "Pilot", "description": "Pilot POST and GET endpoints"},
    {"name": "Aircraft", "description": "Aircraft POST and GET endpoints"},
    {"name": "Logbook", "description": "Logbook POST and GET endpoints"},
    {"name": "Flight", "description": "Flight POST and GET endpoints"},
    {"name": "Upload", "description": "Upload logbook file"}
]

MOESIF_SETTINGS = {
    'APPLICATION_ID': MOESIF_API_KEY,
    'LOG_BODY': True,
    'CAPTURE_OUTGOING_REQUESTS': True
}
