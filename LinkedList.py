class LinkListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkList:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        if self.head == None:
            return True

    def getLastValue(self):
        if self.head is None:
            return None
        currentNode = self.head
        while currentNode.next != None:
            currentNode = currentNode.next
        return currentNode.value

    def getFirstValue(self):
        if self.head is None:
            return None
        return self.head.value

    def insertNode(self,index,value):
        if index < 0 or index > self.length():
            raise IndexError("Index out of bounds.")
        nextNode = LinkListNode(value)
        if index == 0:
            nextNode.next = self.head
            self.head = nextNode
        else:
            current = self.head
            for i in range(index - 1):
                current = current.next
            nextNode.next = current.next

            current.next = nextNode
        return nextNode

    def insertAtHead(self,value):
        nextNode = LinkListNode(value)
        nextNode.next = self.head
        self.head = nextNode
        return nextNode

    def insertAtEnd(self,value):
        nextNode = LinkListNode(value)
        if self.head == None:
            self.head = nextNode
        else:
            currentNode = self.head
            while currentNode.next!=None:
                currentNode = currentNode.next
            currentNode.next = nextNode
        return nextNode

    def peekAtNode(self,index):
        current = self.head
        for i in range(index):
            current = current.next
        return  current.value

    def deleteNode(self, value):
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            return True
        currentNode = self.head
        while currentNode.next is not None:
            if currentNode.next.value == value:
                currentNode.next = currentNode.next.next
                return True
            currentNode = currentNode.next
        return False

    def deleteFromStart(self):
        if self.head is None:
            return None
        self.head = self.head.next

    def deleteFromEnd(self):
        if self.head is None:
            return None
        if self.head.next is None:
            self.head = None
            return None
        currentNode = self.head
        while currentNode.next.next is not None:
            currentNode = currentNode.next
        currentNode.next = None
