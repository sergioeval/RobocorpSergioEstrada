from robocorp.tasks import task
from Browser_Get_News import Browser_Get_News
from My_Workitems import My_Workitems
from RPA.Robocorp.WorkItems import WorkItems
from robocorp import workitems


@task
def get_the_news():
    """
    Task to get all news according to the work items parameters
    """
    work_item_current = workitems.inputs.current
    print(work_item_current)
    # crating work items
    workitems.outputs.create(payload={
        "Data": "this is awork item"
    })
