from robocorp.tasks import task
from robocorp import workitems
# from Get_News_Data import Get_News_Data
# from Initiate_Structure import Initiate_Structure
import logging
# from Utilities import FailedCustomException, save_work_items
from robot_code.utilities.initiate_structure import Initiate_Structure
from robot_code.utilities.base import Base
from robot_code.browser_process.step_1_go_search import Go_Search_Phrase
from robot_code.browser_process.step_2_sort_data_get_pagination import Sort_Get_Pagination
from robot_code.browser_process.step_3_get_data import Get_News_Data
from robot_code.excel_process.create_excel_report import Create_Excel_Report

from robot_code.utilities.custom_exception import FailedCustomException
import inspect

# Setup folders
Initiate_Structure().setup_folders()

# Logging file configuration
log_file_name = f"{Base.my_constanst.LOGGING_PATH}task_1_{Base.string_timestamp}.log"
logging.basicConfig(filename=log_file_name, filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s ################################## %(levelname)s ##################################\n%(message)s')
logger = logging.getLogger()


@task
def get_the_news():
    """
    Task to get all news according to the work items parameters
    """
    source = inspect.currentframe().f_code.co_name
    file_name = inspect.currentframe().f_code.co_filename
    for item in workitems.inputs:
        print(item)
        try:
            # Search news data
            Go_Search_Phrase(search_phrase=item.payload["search_phrase"]).run()
            pagination = Sort_Get_Pagination().run()
            print(pagination)
            valid_time_params = Base().get_valid_time_parameters(item=item)
            print(valid_time_params)

            # Get the news data
            news_data = Get_News_Data(
                pagination=pagination,
                accepted_time_params=valid_time_params,
                item=item).get_all_data()

            # creating excel report
            Create_Excel_Report().create_file_add_data(news_data=news_data)

            # archive and clean
            Base.archive_to_zip()
            Base.clean_output_folder()
            item.done()

        except FailedCustomException as e:
            logger.info(
                Base.my_constanst.LOG_INFO_TEMPLATE.format(
                    message=e,
                    function_name=source,
                    file_name=file_name
                )
            )
            Base.file_system_actions.copy_file(
                source=log_file_name,
                destination=Base.my_constanst.OUTPUT_BASE_PATH +
                log_file_name.split("/")[-1]
            )
            item.fail(exception_type="APPLICATION",
                      code="SORT_DATA_FAILED", message=e)
