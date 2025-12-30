from settings import *

class Brain:
    def __init__(self, blackboard):
        self.blackoard = blackboard

    def make_decision(blackboard):
        pass

class BehaviorNode:
    def __init__(self, branches):
        self.branches = branches

    def run(self):
        pass

class Fallback(BehaviorNode):
    def run(self):
        for branch in self.branches:
            if branch.run():
                return True
        return False

class Sequence(BehaviorNode):
    def run(self):
        for branch in self.branches:
            if not branch.run():
                return False
        return True
    
class Task:
    def __init__(self, function, blackboard):
        self.blackboard = blackboard
        self.run = function(blackboard)