from collections import defaultdict

class Year(object):
    """ Wrapper class for archive handling """
    def __init__(self, year):
        self.year = year
        self._months = defaultdict(int)

    @staticmethod
    def sort_years(this, other):
        # helper function to sort Year objects by their year attributes
        return this.year - other.year

    def __cmp__(self, other):
        return cmp(self.year, other.year)

    def __str__(self):
        return str(self.year)

    def human_readable(self):
        return "Year %s  with %s months" % (self.year, len(
            [key for key, value in self._months.iteritems() if value]))

    def add_month(self, month):
        self._months[month] += 1

    @property
    def months(self):
        """ Returns a sorted list of months appended to this year """
        return reversed(sorted([(month, count) for month, count in
            self._months.iteritems() if count]))
