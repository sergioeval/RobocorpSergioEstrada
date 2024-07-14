from robot_code.utilities.base import Base
from robot_code.utilities.custom_exception import FailedCustomException
import inspect
import logging
logger = logging.getLogger()


class Create_Excel_Report(Base):
    """
    To create the final excel report 
    """
    file_name = inspect.currentframe().f_code.co_filename

    def __init__(self):
        self.excel_file_path = self.my_constanst.FINAL_REPORT_FILE_PATH_TEMPLATE.format(
            date=self.string_timestamp)

    def create_file_add_data(self, news_data):
        """
        create the excel file and add the data 
        """
        try:
            # CREATE THE TABLE
            table = self.tables_actions.create_table()
            # excel workbook
            workbook = self.excel_actions.create_workbook(
                path=self.excel_file_path)

            # save data and save file
            for item in news_data:
                del item["accepted"]
                self.excel_actions.append_rows_to_worksheet(
                    content=item, header=True)
            workbook.save()
        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            self.work_items.fail(exception_type="APPLICATION",
                                 code="CREATE_EXCEL_REPORT_FAILED", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)
