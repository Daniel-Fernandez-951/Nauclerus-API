
# OpenAPI and Doc settings
import os

MOESIF_API_KEY = os.getenv('MOESIF_API')
LOGO_PATH = "/app/logo/logo2-nauclerusAPIV1_dark.png"
API_VERSION = "0.1.0"
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
