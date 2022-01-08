class Node:
    level: int = None               # The node level in the tree
    identifier: str = None          # The node identifier
    reference: str = None           # The node reference value, if any
    value: str = None               # The node value, if any
    children: 'list[Node]' = []     # List of this nodes children

    _referenced_node: 'Node' = None # The node referenced by the value, if any


    def __str__(self) -> str:
        if self.identifier == 'INDI':
            return f"{self.get_value('NAME')}"



    def add_child(self, child: 'Node') -> None:
        self.children.append(child)


    def link_references(self, ref_dict: dict) -> None:
        """Link the references for itself and every of its children"""

        for key in ref_dict:
            if key == self.value: self._referenced_node = ref_dict[key]

        for child in self.children:
            child.link_references(ref_dict)


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


    def get_value(self, value_id: str = None):
        """Return the requested value.

        If value_id is not given, this method will return the value of this node.
        This value can be a referenced node or a string.

        If value_id is given, this method will return the value of the child node with
        the specified identifier. It is useful for example with a INDI node:
            If node.identifier == 'INDI', you can just use node.get_value('NAME') to get the name of the individual.

        Args:
            value_id (str): The identifier of the child node to return.

        Returns:
            The value of the child node with value_id as identifier if it exists.
            The value of this node if value_id is not given.
        """
        if value_id:
            child = self.get_children(value_id)
            if child: return child.get_value()
            else: return None

        if self.value == '': return self.value
        if self.value[0] == self.value[-1] == '@': return self._referenced_node
        return self.value