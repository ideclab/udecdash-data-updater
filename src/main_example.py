import os
import logging
from Dashboard.DataUpdater import *
from Dashboard.Helpers.Directory import Directory
from Dashboard.Helpers.Notification import Notification

logging.basicConfig(level=logging.DEBUG)
mails = ['example@example.cl']

os.environ['DB_HOST'] = '127.0.0.1'
os.environ['DB_PORT'] = '5432'
os.environ['DB_NAME'] = ''
os.environ['DB_USERNAME'] = ''
os.environ['DB_PASSWORD'] = ''

os.environ['PATH_DATA_FILES'] = ''
os.environ['PATH_CONCAT'] = '/'
os.environ['PATH_CANVAS_CONFIG'] = ''

os.environ['SMTP_USER']= ''
os.environ['SMTP_PASS']= ''
os.environ['SMTP_HOST']= ''
os.environ['SMTP_PORT']= ''

os.environ['NOTIFICATION_EMAILS'] = os.pathsep.join(mails)

os.environ['FIRST_DATA_UPDATE']= 'True'

# This not include requests folder, is recommended True.
os.environ['CLEAR_DIRECTORIES_BEFORE_DOWNLOAD']= 'True'
os.environ['ENABLE_DOWNLOAD']= 'False'

os.environ['FILE_EXTENSION']='gz'

os.environ['SERVER_SUDO_PASSWORD']= ''

# absolute path to canvasDataCli command
os.environ['SERVER_CANVAS_DATA_CLI_COMMAND_PATH']= '/usr/local/bin/canvasDataCli'

# absolute path to supervisord command
os.environ['SERVER_SUPERVISORD_COMMAND_PATH']= '/usr/bin/supervisorctl'

os.environ['FRONTEND_DIR']= ''

dataUpdater = DataUpdater()
dataUpdater.launch()
