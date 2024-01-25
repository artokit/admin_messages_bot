from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config['TOKEN']
ADMIN_GROUP_ID = config['ADMIN_GROUP_ID']
