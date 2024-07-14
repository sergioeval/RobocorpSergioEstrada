from Utilities import FailedCustomException
from RPA.Excel.Files import Files
from RPA.Tables import Tables
import logging
from constants import FINAL_REPORT_FILE_PATH_TEMPLATE
from datetime import datetime
import inspect

logger = logging.getLogger()

now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")


class Create_Report:
    """
    Process to create the final report using the work items 
    """

    def __init__(self, work_items):
        self.work_items = work_items
        self.final_report_file_path = FINAL_REPORT_FILE_PATH_TEMPLATE.format(
            date=timestamp)
        self.file_name = inspect.currentframe().f_code.co_filename

    def run_all(self):
        """
        execute the whole process
        """
        # process all work items and save them in the report
        self.step_1_create_file_and_add_data()

    def step_1_create_file_and_add_data(self):
        """
        create the file for the final report 
        """
        try:
            tables = Tables()
            final_table = tables.create_table()
            excel = Files()
            workbook = excel.create_workbook(path=self.final_report_file_path)

            # iterate over the work items and save them

            for item in self.work_items:
                data = item.payload
                del data["accepted"]
                excel.append_rows_to_worksheet(content=data, header=True)
                item.done()
            workbook.save()

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)
