class Node:
    level: int = None               # The node level in the tree
    identifier: str = None          # The node identifier
    reference: str = None           # The node reference value, if any
    value: str = None               # The node value, if any
    children: 'list[Node]' = []     # List of this nodes children

    
    def add_child(self, child: 'Node') -> None:
        self.children.append(child)