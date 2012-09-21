from itree.itree import Node, Tree, uniq
from unittest import TestCase

class IntervalTreeTest(TestCase):
    def test_center_single_interval(self):
        self.assertEquals(Tree([]).center([slice(1,5)]),
                          1)

    def test_center_two_intervals(self):
        self.assertEquals(Tree([]).center([slice(1,5), slice(2,6)]),
                          2)

    def test_new(self):
        self.assertTrue(isinstance(Tree([slice(1,5)]), Tree))

    def test_top_node(self):
        intervals = [slice(1,5), slice(2,6), slice(3,7)]
        tree = Tree(intervals)
        self.assertEquals(tree.top_node.x_center, 2)

    def test_search(self):
        self.assertIntervals([(1,5)], 3)

    # Not sure I care to support the non-array behaivor
    # context 'given non-array full-closed "(1..4)" and a point query "3"' do
    #   it 'returns an array contains a half-open interval (1...5)]' do
    #     IntervalTree::Tree.new(1..4).search(3).should == [1...5]
    #   end
    # end

    def test_search_two_intervals(self):
        self.assertIntervals([(1,5), (2,6)], 3)

    def test_search_three_intervals(self):
        self.assertIntervals([(0,8), (1,5), (2,6)],
                                3)

    def test_search_three_intervals_for_interval(self):
        self.assertIntervals([(0,8), (1,5), (2,6)],
                             slice(1,4))

    def test_search_two_intervals_returns_one(self):
        self.assertIntervals([(1,3), (3,5)], 
                             (3,9),
                             [(3,5)])

    def test_search_three_intervals_return_two(self):
        self.assertIntervals([(1,3), (3,5), (4,8)],
                             (3,5),
                             [(3,5), (4,8)])

    def test_search_three_intervals_return_two(self):
        self.assertIntervals([(1,3), (3,5), (3,9), (4,8)],
                             (3,5),
                             [(3,5), (3,9), (4,8)])

    def assertIntervals(self, intervals, point, returns=None):
        intervals = [slice(*i) for i in  intervals]
        if returns is None:
            returns = intervals
        else:
            returns = [slice(*i) for i in returns]
        if isinstance(point, (tuple, list)):
            point = slice(*point)
        self.assertEquals(Tree(intervals).search(point),
                          returns)


class UniqueTest:
    @uniq
    def test(self):
        yield slice(1,2)
        yield slice(2,3)
        yield slice(1,3)
        yield slice(1,2)
        yield slice(3,4)

class TestUniq(TestCase):
    def test_uniq(self):
        self.assertEquals(list(UniqueTest().test()),
                          [slice(1,2),
                           slice(2,3),
                           slice(1,3),
                           slice(3,4)])
