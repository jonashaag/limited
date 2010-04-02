import datetime

class Access(object):
    def __init__(self, timestamp, address, url, status):
        self.timestamp = timestamp
        self.address = address
        self.url = url
        self.status = status
        self.datetime = datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def grouped_by_month(objects):
        from gpyconf._internal.dicts import ordereddefaultdict
        grouped = ordereddefaultdict(list)

        for obj in objects:
            grouped[obj.datetime.month].append(obj)

        return grouped

    @staticmethod
    def grouped_by_url(objects):
        from collections import defaultdict
        grouped = defaultdict(list)
        for obj in objects:
            grouped[obj.url].append(obj)

        return grouped


if __name__ == '__main__':
    accesses = []
    with open('access.log') as fobj:
        for line in fobj:
            tm, adr, url, st = line.split(' || ')
            accesses.append(Access(int(float(tm)), adr, url, int(st)))

        for month, objects in Access.grouped_by_month(accesses).iteritems():
            print month, len(objects)
            print "QUERIES PER DAY: %f" % (len(objects)/30.0)
            byurl = Access.grouped_by_url(objects)
            byurl = sorted(byurl.iteritems(), key=lambda x:len(x[1]), reverse=True)
            for url, objects in byurl[:10]:
                print '    %s: %d' % (url, len(objects))
