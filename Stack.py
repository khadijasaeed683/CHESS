from LinkedList import LinkList

class myStack:
    def __init__(self):
        self.list = LinkList()
        
    def isEmpty(self):
        if self.list.isEmpty():
            return True
        return False

    def PUSH(self, value):
        self.list.insertAtEnd(value)
        print(f"Move pushed: {value}")

    def POP(self):
        if self.isEmpty():
            print("Stack Underflow: Stack is Empty")
            return None
        popped_value = self.list.getLastValue()
        self.list.deleteFromEnd()
        print(f"Move popped: {popped_value}")
        return popped_value


    def Peek(self):
        if not self.isEmpty():
            return self.list.getLastValue()

        
