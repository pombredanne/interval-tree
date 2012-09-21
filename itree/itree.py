import bisect

def uniq(meth):
    def _make_unique(*args, **kwargs):
        history = set()
        for interval in meth(*args, **kwargs):
            if (interval.start, interval.stop) in history:
                continue
            history.add((interval.start, interval.stop))
            yield interval
    return _make_unique


class Tree:
    def __init__(self, ranges):
        self.ranges = ranges

        points = set()
        for interval in self.ranges:
            points.add(interval.start)
            points.add(interval.stop)
        self.points = list(sorted(points))

        self.top_node = self.divide_intervals(self.ranges)

    def divide_intervals(self, intervals):
        if not intervals: return
        x_center = self.center(intervals)
        s_center = []
        s_left = []
        s_right = []

        for interval in intervals:
            if interval.start < x_center:
                s_left.append(interval)
            elif interval.start > x_center:
                s_right.append(interval)
            else:
                s_center.append(interval)
        return Node(x_center, s_center, self.divide_intervals(s_left), self.divide_intervals(s_right))

    @staticmethod
    def sort(seq):
        return sorted(seq, key=lambda x:(x.start, x.stop))

    def search(self, interval):
        if isinstance(interval, (tuple, list)):
            interval = slice(*interval)
        if isinstance(interval, slice):
            return Tree.sort(self.search_interval(interval.start, interval.stop))
        else:
            return Tree.sort(self.point_search(self.top_node, interval))

    @uniq
    def search_interval(self, first, last):
        seen_before = set()
        first = bisect.bisect_left(self.points, first)
        last = bisect.bisect_right(self.points, last)
        for j in range(first, last):
            for element in self.point_search(self.top_node, self.points[j]):
                yield element

    def center(self, intervals):
        #TODO: A median finder will have much better performance
        return sorted(intervals, key=lambda x:x.start)[(len(intervals))/2].start

    @uniq
    def point_search(self, node, point):
        for k in node.s_center:
            if k.start <= point and point < k.stop:
                yield k
        if node.left_node and point < node.left_node.s_max:
            for k in self.point_search(node.left_node, point):
                yield k
        if node.right_node and node.right_node.x_center <= point:
            for k in self.point_search(node.right_node, point):
                yield k

class Node:
    def __init__(self, x_center, s_center, left_node, right_node):
        self.x_center = x_center
        self.s_center = list(sorted(s_center, key=lambda x:x.start))
        self.left_node = left_node
        self.right_node = right_node
        self.s_max = max(x.stop for x in self.s_center)
