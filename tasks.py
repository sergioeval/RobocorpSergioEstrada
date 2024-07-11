from robocorp.tasks import task
from Browser_Get_News import Browser_Get_News
from RPA.Robocorp.WorkItems import WorkItems
from robocorp import workitems
import logging
from RPA.Archive import Archive


@task
def get_the_news():
    """
    Task to get all news according to the work items parameters
    """
    work_item_current = workitems.inputs.current

    get_news = Browser_Get_News()
    logging.info(work_item_current)

    print(work_item_current)
    logging.shutdown()
    get_news.archive_all()
    # crating work items
