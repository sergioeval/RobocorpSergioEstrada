from robocorp.tasks import task
from Get_News_Data import Get_News_Data
from Initiate_Structure import Initiate_Structure
from robocorp import workitems
from RPA.Archive import Archive
import logging
import time
from datetime import datetime
from constants import (
    OUTPUT_BASE_PATH,
    NEWS_URL,
    LOGGING_PATH
)
from Utilities import FailedCustomException, save_work_items

# Setup folders
Initiate_Structure().setup_folders()

# Logging file configuration
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
log_file_name = f"{LOGGING_PATH}task_1_{timestamp}.log"
logging.basicConfig(filename=log_file_name, filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.info(f"URL: {NEWS_URL}")


@task
def get_the_news():
    """
    Task to get all news according to the work items parameters
    """
    work_item_current = workitems.inputs.current

    try:
        # Get News Data and create work items
        get_news = Get_News_Data(wi=work_item_current)
        work_items_search_results = get_news.run_all()
        save_work_items(payloads=work_items_search_results)
        work_item_current.done()

    except FailedCustomException as e:
        logger.error(e)
