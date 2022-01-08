class Node:
    level: int = None               # The node level in the tree
    identifier: str = None          # The node identifier
    reference: str = None           # The node reference value, if any
    value: str = None               # The node value, if any
    children: 'list[Node]' = []     # List of this nodes children

    
    def add_child(self, child: 'Node') -> None:
        self.children.append(child)


    def get_children(self, child_id: str) -> 'Node':
        """Return the first child node with the specified identifier.
        
        Args:
            child_id (str): The identifier of the child node to return.

        Returns:
            Node: The first child node with the specified identifier.
        """
        for child in self.children:
            if child.identifier == child_id:
                return child
        return None