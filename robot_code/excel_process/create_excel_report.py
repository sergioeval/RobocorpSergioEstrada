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
        source = inspect.currentframe().f_code.co_name
        try:
            # CREATE THE TABLE

            table = self.tables_actions.create_table()
            # excel workbook
            workbook = self.excel_actions.create_workbook(
                path=self.excel_file_path)

            # save data and save file
            if len(news_data) == 0:
                self.excel_actions.append_rows_to_worksheet(
                    content={
                        "INFORMATION": "No news results from search parameters"},
                    header=True
                )
                workbook.save()
                logger.info(
                    self.my_constanst.LOG_INFO_TEMPLATE.format(
                        message="There is no news data available for the requested parameters.",
                        function_name=source,
                        file_name=self.get_file_name(self.file_name)
                    )
                )
                return

            for item in news_data:
                del item["accepted"]
                del item["image_source"]
                self.excel_actions.append_rows_to_worksheet(
                    content=item, header=True)
            workbook.save()

            logger.info(
                self.my_constanst.LOG_INFO_TEMPLATE.format(
                    message=f"File report saved correctly: {self.excel_file_path}",
                    function_name=source,
                    file_name=self.get_file_name(self.file_name)
                )
            )

        except Exception as e:
            # self.work_items.fail(exception_type="APPLICATION",
            #                      code="CREATE_EXCEL_REPORT_FAILED", message=e)
            fail_message = self.my_constanst.LOG_FAILED_TEMPLATE.format(
                message=e,
                function_name=source,
                file_name=self.get_file_name(self.file_name)
            )
            raise FailedCustomException(message=fail_message)
