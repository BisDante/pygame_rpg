from settings import *
from actor import *
from random import sample

def load_map(map_name):
    map_data = pytmx.util_pygame.load_pygame(os.path.join(MAP_FOLDER, map_name))
    return map_data

def load_game(name='save.json'):
    data = {}
    path = os.path.join(SAVE_FOLDER, name)
    with open(path, 'r') as rf:
        read = json.load(rf)
    
    for key in read.keys():
        data[key] = read[key]
    data['characters'] = [PlayerCharacter(attributes) for attributes in data['characters']]
    data['surfaces'] = load_surfaces()
    return data

def load_surfaces():
    surfaces = {}
        
    for root, dirs, files in os.walk('images'):
        for filename in files:
            new_surf = pygame.image.load(os.path.join(root, filename)).convert_alpha()
            surfaces[filename.split('.')[0]] = new_surf
       
    return surfaces

def create_encounter():
    pass

def create_enemy():
    pass

def create_save_data(character_list, name='save.json'):
    path = os.path.join(SAVE_FOLDER, name)
    
    new_save = START_SAVE.copy()
    new_save['characters'] = character_list
    with open (path, 'w') as wf:
        json.dump(new_save, wf, indent=2)

class MapData:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __str__(self):
        return f"name: {self.name} id: {self.id}"

class Node:
    def __init__(self, data: MapData):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class MapTree:
    def __init__(self):
        self.root = None
        map_list = self.get_map_list()
        
        for map in map_list:
            self.root = self.insert(self.root, Node(map))
        
        self.current = self.root

    def get_height(self, node):
        if node:
            return node.height
        return 0
    
    def get_balance_factor(self, node):
        return self.get_height(node.left) - self.get_height(node.right)
    
    def rebalance(self, node):
        balance = self.get_balance_factor(node)

        if balance > 1:
            if self.get_balance_factor(node.left) < 0:
                return self.left_right_rotate(node)
            return self.right_rotate(node)
        
        if balance < -1:
            if self.get_balance_factor(node.right) > 0:
                return self.right_left_rotate(node)
            return self.left_rotate(node)
        
        return node
    
    def right_rotate(self, root):
        child = root.left
        grandchild = child.right

        child.right = root
        root.left = grandchild

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        return child
    
    def left_rotate(self, root):
        child = root.right
        grandchild = child.left

        child.left = root
        root.right = grandchild

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        return child
    
    def left_right_rotate(self, root):
        root.left = self.left_rotate(root.left)
        root = self.right_rotate(root)

        return root
    
    def right_left_rotate(self, root):
        root.right = self.right_rotate(root.right)
        root = self.left_rotate(root)

        return root
        
    def in_order(self, root):
        if root.left:
            self.in_order(root.left)
        
        print(f"{root.data} height:{root.height}")
        
        if root.right:
            self.in_order(root.right)

    def post_order(self, root):
        if root.right:
            self.post_order(root.right)

        print(root)

        if root.left:
            self.post_order(root.left)

    def pre_order(self, root):
        print(root)

        if root.left:
            self.pre_order(root.left)

        if root.right:
            self.pre_order(root.right)

    def insert(self, root, node):
        if not root:
            root = node
            return root

        elif node.data.id < root.data.id:
            root.left = self.insert(root.left, node)
        
        elif node.data.id > root.data.id:
            root.right = self.insert(root.right, node)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.rebalance(root)
        
    def remove(self, root, id):
        if not root:
            root = None
            return root
        
        elif id < root.id:
            root.left = self.remove(root.left, id)

        elif id > root.id:
            root.right = self.remove(root.right, id)

        elif root.right:
            root.data = self.successor(root.right)
            root.right = self.remove(root.right, root.data.id)

        elif root.left:
            root.data = self.predecessor(root.left)
            root.left = self.remove(root.left, root.data.id)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.rebalance(root)
    
    def successor(self, root):
        successor = root
        while successor.left:
            successor = successor.left
        
        return successor.data
    
    def predecessor(self, root):
        predecessor = root
        while predecessor.right:
            predecessor = predecessor.right

        return predecessor.data

    def get_map_list(self):
        map_list = []
        for root, dirs, files in os.walk(os.path.join('data', 'maps')):
            for filename in files:
                map_list.append(MapData(filename, 0))

        map_ids = sample(range(len(map_list)), len(map_list))
        
        for i, map in enumerate(map_list):
            map.id = map_ids[i]
                
        return map_list
    
if __name__ == '__main__':
    tree = MapTree()
    tree.in_order(tree.root)