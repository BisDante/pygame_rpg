from settings import *

class TaskStatus:
    FAIL = -1
    RUNNING = 0
    SUCCESS = 1


class Brain:
    def __init__(self, blackboard, children):
        self.blackoard = blackboard
        self.children = children

    def make_decision(self):
        for child in self.children:
            child.run()

    def init_children():
        pass

# behaviors
class BehaviorNode:
    def __init__(self, children, blackboard):
        self.blackboard = blackboard
        self.children = children

    def run(self):
        pass

class Fallback(BehaviorNode):
    def run(self):
        for child in self.children:
            return TaskStatus.SUCCESS if child.run(self.blackboard) else TaskStatus.FAIL

class Sequence(BehaviorNode):
    def run(self):
        for branch in self.branches:
            if not branch.run():
                return False
        return True

class Condition(BehaviorNode):
    pass

# leaf
class Task:
    def __init__(self, function, blackboard):
        self.blackboard = blackboard
        self.run = function(blackboard)
