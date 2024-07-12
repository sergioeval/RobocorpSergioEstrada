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
    FailedCustomException,
    NEWS_URL
)


# Logging file configuration
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
log_file_name = f"{OUTPUT_BASE_PATH}{timestamp}.log"
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
        # Setup folders
        Initiate_Structure().setup_folders()

        # Get News Data
        get_news = Get_News_Data(wi=work_item_current)
        get_news.run_all()

    except FailedCustomException as e:
        logger.error(e)

    #
    #

    # Create Excel file with data

    # Clean and finish
