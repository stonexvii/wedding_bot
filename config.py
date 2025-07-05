import dotenv
import os

# dotenv.load_dotenv('.env')

ADMIN_TG_ID = int(os.getenv('ADMIN_TG_ID'))
ADMIN_EMAIL = os.getenv('EMAIL_ADDRESS')
ADMIN_EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

YADISK_TOKEN = os.getenv('YADISK_TOKEN')

FILE_NAME_STATIC = 'wedding_static.xlsx'
