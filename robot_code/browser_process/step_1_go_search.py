from robot_code.utilities.base import Base
from robot_code.utilities.custom_exception import FailedCustomException
import inspect


class Go_Search_Phrase(Base):
    """
    Go to url and search phrase from work item
    """
    file_name = inspect.currentframe().f_code.co_filename

    def run(self):
        """
        run the whole process
        """
        self.go_to_page()
        self.search_phrase()

    def go_to_page(self):
        try:
            self.page.goto(
                url=self.my_constanst.NEWS_URL
            )
            # wait for hamburguer menu
            self.page.wait_for_selector(
                selector=self.my_constanst.SELECTOR_HAMBURGER_MENU,
                timeout=40000)

        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            self.work_items.fail(exception_type="APPLICATION",
                                 code="GOTO_PAGE_FAILED", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)

    def search_phrase(self):
        """
        to search the phrase from the work item
        """
        try:
            search_phrase = self.work_items.payload['search_phrase']
            # Need to click on the hamburger menu
            self.page.wait_for_selector(
                selector=self.my_constanst.SELECTOR_HAMBURGER_MENU,
                timeout=40000).click()

            # clicking in the search bar and enter searchphrase
            self.page.wait_for_selector(
                selector=self.my_constanst.SELECTOR_SEARCH_FIELD,
                timeout=40000
            ).fill(value=search_phrase)

            self.page.keyboard.press('Enter')

            self.wait_this(time_seconds=2)
        except Exception as e:
            source = inspect.currentframe().f_code.co_name
            self.work_items.fail(exception_type="APPLICATION",
                                 code="SEARCH_PHRASE_FAILED", message=e)
            raise FailedCustomException(
                message=e, source=source, file_name=self.file_name)
