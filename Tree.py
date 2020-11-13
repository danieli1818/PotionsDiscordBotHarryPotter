

class Tree:

    def __init__(self, root=None):
        if root is None:
            root = Node()
        elif type(root) is not Node:
            raise Exception("Invalid Type Exception: root isn't a Node!")
        self.root = root

    def get_root(self):
        return self.root

    def add_path(self, path, on_child_exist):
        current_node = self.get_root()
        for current_path_item in path:
            if type(current_path_item) is not tuple or current_path_item.__len__() != 2:
                raise Exception("Invalid path")
            child_id = current_path_item[0]
            child_info = current_path_item[1]
            if current_node.has_child(child_id):
                child_info = on_child_exist(current_node.get_child(child_id).get_info(), child_info)
                if child_info is None:
                    return
            old_child, new_child = current_node.set_child(child_info, child_id)
            current_node = new_child


class Node:

    def __init__(self, info=None, children=None):
        if children is None:
            children = {}
        self.info = info
        self.children = children

    def add_child(self, child_info, child_id=None):
        if child_info is None:
            raise Exception("None Child!")
        if child_id is None:
            child_id = self.children.__len__()
        self.children[child_id] = Node(child_info)
        return self.children[child_id]

    def remove_child(self, child_id):
        if not self.has_child(child_id):
            raise Exception("Child doesn't exist!")
        return self.children.pop(child_id)

    def get_child(self, child_id):
        if not self.has_child(child_id):
            raise Exception("Child doesn't exist!")
        return self.children[child_id]

    def get_info(self):
        return self.info

    def has_child(self, child_id):
        return child_id in self.children.keys()

    def set_child(self, child_info, child_id=None):
        if child_id is None:
            child = self.add_child(child_info)
            return None, child
        return_value = None
        if self.has_child(child_id):
            return_value = self.get_child(child_id)
        self.children[child_id] = Node(child_info)
        return return_value, self.children[child_id]
