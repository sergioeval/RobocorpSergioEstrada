from robocorp import workitems
from robocorp.tasks import task
from Utilities import FailedCustomException
from Create_Report import Create_Report
import logging
from datetime import datetime
from constants import LOGGING_PATH

now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
log_file_name = f"{LOGGING_PATH}task_2_{timestamp}.log"
logging.basicConfig(filename=log_file_name, filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


@task
def create_report():
    """
    Task to create report according to the search process
    """
    work_items = workitems.inputs

    try:
        # execute create report process
        report = Create_Report(work_items=work_items)
        report.run_all()

    except FailedCustomException as e:
        logger.error(e)
