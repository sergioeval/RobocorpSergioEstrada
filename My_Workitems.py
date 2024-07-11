from RPA.Robocorp.WorkItems import WorkItems


class My_Workitems:
    """
    To always provide a work item generator
    """
    work_items = WorkItems().get_input_work_item().payload
    work_items_type = type(work_items)

    @classmethod
    def work_items_generate(cls):
        if cls.work_items_type == list:
            for i in cls.work_items:
                yield i
        if cls.work_items_type == dict:
            work = [cls.work_items]
            for i in work:
                yield i
