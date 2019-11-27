import random
import Stack
import heapq
import time
from itertools import *


class Heap:
    def __init__(self):
        self.queue = []         # stored like so:   Q[0] = (weighting, (source, (x,y)) )
        heapq.heapify(self.queue)

    def empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def push(self, weighting, node, source=None):
        heapq.heappush(self.queue, (weighting, (source, node)))

    def pull(self):
        return heapq.heappop(self.queue)

    def edit(self, weighting, node, source):
        for item in self.queue:
            if item[1][1] == node:            # perhaps add a raise statement to raise error if new eight higher than previous
                self.queue.remove(item)
                self.push(weighting, node, source)
                break

