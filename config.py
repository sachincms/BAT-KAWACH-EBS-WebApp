from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv

load_dotenv()

current_file_path = os.getcwd()

#Images
BAT_LOGO_PATH = os.path.join('app', 'static', 'images', 'BAT.png')
CMS_LOGO_PATH = os.path.join('app', 'static', 'images', 'CMS.png')

#HTML File Paths
CONTAINER_STYLE_HTML = os.path.join(current_file_path, 'app',  'static', 'html', 'container_style.html')
LINK_BUTTON_STYLE_HTML = os.path.join(current_file_path, 'app',  'static', 'html', 'link_button_style.html')
LOGO_STYLE_HTML = os.path.join(current_file_path, 'app', 'static',  'html', 'logo_style.html')
SEVERITY_LEGEND_HTML = os.path.join(current_file_path, 'app', 'static', 'html', 'severity_legend.html')
IN_CONTAINER_DIVIDER_HTML = os.path.join(current_file_path, 'app', 'static', 'html', 'in_container_divider.html')

#Opened HTML Files
CONTAINER_STYLE = open(CONTAINER_STYLE_HTML).read()
LINK_BUTTON_STYLE = open(LINK_BUTTON_STYLE_HTML).read()
IN_CONTAINER_DIVIDER = open(IN_CONTAINER_DIVIDER_HTML).read()

#MongoDB
MONGODB_PROCESSED_COLLECTION = os.environ.get('MONGODB_PROCESSED_COLLECTION')

#Application
PAGE_TITLE = 'Kawach News'
INTRO_MESSAGE = 'An Automated Tool To Gather And Document Latest Intelligence On Child Protection Events For Proactive Decision-Making.'
# CATEGORY_LIST = ['All', 'Suspected Outbreak', 'Confirmed Outbreak', 'Disease Information', 'Climate', 'Others']
SEVERITY_LIST = ['All', 'High', 'Medium', 'Low']

TIMESPAN_DICT = {
    'This week': datetime.now() - relativedelta(days=7),
    'This month': datetime.now().replace(day=1),
    'Past 3 months': datetime.now() - relativedelta(months=3),
    'Past 6 months': datetime.now() - relativedelta(months=6),
    'Past 1 year': datetime.now() - relativedelta(years=1),
    'All Time': datetime.now() - relativedelta(years=100),
}