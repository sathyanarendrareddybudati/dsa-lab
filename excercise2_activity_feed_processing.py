#!/usr/bin/env python3

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class ActivityStack:

    def __init__(self):
        self.top = None
        self._size = 0
        self.undo_stack = []

    def push(self, activity):
        new_node = Node(activity)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        if self.top is None:
            return None

        activity = self.top.data
        self.top = self.top.next
        self._size -= 1
        return activity

    def peek(self):
        return None if self.top is None else self.top.data

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size

    def display_recent(self, n):
        current = self.top
        count = 0

        while current and count < n:
            print(current.data)
            current = current.next
            count += 1

    def undo_last(self):
        activity = self.pop()
        if activity:
            self.undo_stack.append(activity)
        return activity


class NotificationQueue:

    def __init__(self):
        self.front_node = None
        self.rear = None
        self._size = 0

    def enqueue(self, notification):

        new_node = Node(notification)

        if self.rear is None:
            self.front_node = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

        self._size += 1

    def dequeue(self):

        if self.front_node is None:
            return None

        notification = self.front_node.data
        self.front_node = self.front_node.next

        if self.front_node is None:
            self.rear = None

        self._size -= 1
        return notification

    def front(self):
        return None if self.front_node is None else self.front_node.data

    def is_empty(self):
        return self.front_node is None

    def size(self):
        return self._size

    def display_pending(self):

        current = self.front_node

        while current:
            print(current.data)
            current = current.next

    def priority_enqueue(self, notification):

        new_node = Node(notification)

        if self.front_node is None:
            self.front_node = self.rear = new_node
        else:
            new_node.next = self.front_node
            self.front_node = new_node

        self._size += 1


class FeedProcessor:

    def __init__(self):
        self.recent_activities = ActivityStack()
        self.notification_queue = NotificationQueue()
        self.processed_log = NotificationQueue()

    def process_incoming(self):

        notification = self.notification_queue.dequeue()

        if notification:
            self.recent_activities.push(notification)

    def batch_process(self, k):

        for _ in range(k):

            if self.notification_queue.is_empty():
                break

            self.process_incoming()

    def clear_history(self):

        while not self.recent_activities.is_empty():

            activity = self.recent_activities.pop()
            self.processed_log.enqueue(activity)

    def get_stats(self):

        return {
            "recent_stack": self.recent_activities.size(),
            "notification_queue": self.notification_queue.size(),
            "processed_log": self.processed_log.size()
        }

if __name__ == "__main__":
    # 1. Test NotificationQueue
    print("--- Testing NotificationQueue ---")
    nq = NotificationQueue()
    nq.enqueue("Notification 1: Alice liked your photo")
    nq.enqueue("Notification 2: Bob commented on your post")
    nq.priority_enqueue("Notification 3: Urgent! Security alert")
    
    print("Pending Notifications:")
    nq.display_pending()
    
    print(f"\nDequeuing: {nq.dequeue()}")
    print("Pending Notifications after dequeue:")
    nq.display_pending()
    print("-" * 30 + "\n")

    # 2. Test ActivityStack
    print("--- Testing ActivityStack ---")
    as_stack = ActivityStack()
    as_stack.push("User opened app")
    as_stack.push("User browsed feed")
    as_stack.push("User liked a post")
    
    print("Recent Activities:")
    as_stack.display_recent(3)
    
    print(f"\nUndoing last activity: {as_stack.undo_last()}")
    print("Recent Activities after undo:")
    as_stack.display_recent(3)
    print("-" * 30 + "\n")

    # 3. Test FeedProcessor
    print("--- Testing FeedProcessor ---")
    processor = FeedProcessor()
    
    processor.notification_queue.enqueue("Update 1")
    processor.notification_queue.enqueue("Update 2")
    processor.notification_queue.enqueue("Update 3")
    
    print("Stats before processing:", processor.get_stats())
    
    print("\nProcessing a batch of 2 notifications...")
    processor.batch_process(2)
    print("Stats after processing batch:", processor.get_stats())
    
    print("\nClearing history to processed log...")
    processor.clear_history()
    print("Stats after clearing history:", processor.get_stats())
    print("-" * 30 + "\n")