import heapq


# this is a heap (an efficient form of a priority queue) that is set up
# to make processes like Dijkstra and ray casting more efficient
class Heap:
    def __init__(self):
        self.queue = []         # stored like so:   Q[0] = (weighting, (source, (x,y)) )
        heapq.heapify(self.queue)

    # checks if the heap is empty
    def empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    # checks if a value is in the heap
    def InQueue(self, node):
        for item in self.queue:
            if item[1][1] == node:
                return True
        return False

    # pushes a value onto the queue
    def push(self, weighting, node, source=None):
        heapq.heappush(self.queue, (weighting, (source, node)))

    # pulls a value from the queue
    def pull(self):
        return heapq.heappop(self.queue)

    # edits the weightings and source of an item in the heap
    def edit(self, weighting, node, source):
        for item in self.queue:
            if item[1][1] == node:
                if item[0] > weighting:
                    self.queue.remove(item)
                    heapq.heapify(self.queue)
                    self.push(weighting, node, source)
                break
