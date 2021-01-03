import heapq


class Queue:

    def __init__(self):
        self.list = []

    def __bool__(self):
        return bool(self.list)


class PriorityQueue:
    REMOVED = []

    def __init__(self):
        self.list = []
        # super()
        self.entry_finder = {}
        self.count = 0

    def remove(self, element_repr):
        entry = self.entry_finder.pop(element_repr)
        entry[-1] = PriorityQueue.REMOVED

    def insert(self, element, priority):
        if repr(element) in self.entry_finder:
            if priority < self.entry_finder[repr(element)][0]:
                self.remove(repr(element))
                self.insert(element, priority)
        else:
            entry = [priority, self.count, element]
            self.count += 1
            self.entry_finder[repr(element)] = entry
            heapq.heappush(self.list, entry)

    def pop(self):
        while self.list:
            priority, count, element = heapq.heappop(self.list)
            if element is not PriorityQueue.REMOVED:
                del self.entry_finder[repr(element)]
                return element
        raise KeyError('pop from an empty priority queue')

    def __contains__(self, element):
        return element in self.entry_finder

    def __bool__(self):
        return bool(self.list)
