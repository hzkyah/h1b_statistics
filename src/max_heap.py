class MaxHeap:
    def __init__(self, items=[]):
        super().__init__()
        self.heap = [('', 0)]
        for i in items:
            self.heap.append(i)
            self.__floatUp(len(self.heap) - 1)

    def length(self):
        return len(self.heap) - 1

    def push(self, data):
        self.heap.append(data)
        self.__floatUp(len(self.heap) - 1)

    def peek(self):
        if self.heap[1]:
            return self.heap[1]
        else:
            return False

    def pop(self):
        if len(self.heap) > 2:
            self.__swap(1, len(self.heap) - 1)
            maximum = self.heap.pop()
            self.__bubbleDown(1)
        elif len(self.heap) == 2:
            maximum = self.heap.pop()
        else:
            maximum = False
        return maximum

    def __swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def __floatUp(self, index):
        parent = index // 2
        if index <= 1:
            return
        elif self.heap[index][1] > self.heap[parent][1]:
            self.__swap(index, parent)
            self.__floatUp(parent)
        if self.heap[index][1] == self.heap[parent][1] and self.heap[index][0] < self.heap[parent][0]:
            self.__swap(index, parent)
            self.__floatUp(parent)

    def __bubbleDown(self, index):
        left = index * 2
        right = index * 2 + 1
        largest = index
        if len(self.heap) > left and self.heap[largest][1] < self.heap[left][1]:
            largest = left
        if len(self.heap) > right and self.heap[largest][1] < self.heap[right][1]:
            largest = right
        if len(self.heap) > left:
            if self.heap[largest][1] == self.heap[left][1] and self.heap[largest][0] > self.heap[left][0]:
                largest = left
        if len(self.heap) > right:
            if self.heap[largest][1] == self.heap[right][1] and self.heap[largest][0] > self.heap[right][0]:
                largest = right
        if largest != index:
            self.__swap(index, largest)
            self.__bubbleDown(largest)
