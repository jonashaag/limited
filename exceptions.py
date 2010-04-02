class LimitedException(Exception):
    pass

class MissingPageIndex(LimitedException):
    pass

class WidgetNotFound(LimitedException):
    pass
