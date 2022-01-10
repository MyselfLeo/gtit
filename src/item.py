class Item:


    NAME_HR_CHANGES: dict = {'/': '', '_': ' '}


    level: int = None               # The item level in the tree
    identifier: str = None          # The item identifier
    reference: str = None           # The item reference value, if any
    value: str = None               # The item value, if any
    children: 'list[Item]' = []     # List of this item's children

    _referenced_item: 'Item' = None # The item referenced by the value, if any


    def __str__(self) -> str:
        if self.identifier == 'INDI':
            return f"{self.get_value('NAME')}"



    def add_child(self, child: 'Item') -> None:
        self.children.append(child)


    def link_references(self, ref_dict: dict) -> None:
        """Link the references for itself and every of its children"""

        for key in ref_dict:
            if key == self.value: self._referenced_item = ref_dict[key]

        for child in self.children:
            child.link_references(ref_dict)



    def get_child(self, child_id: str) -> 'Item':
        """Return the first child item with the specified identifier.
        
        Args:
            child_id (str): The identifier of the child item to return.

        Returns:
            Item: The first child item with the specified identifier.
        """
        for child in self.children:
            if child.identifier == child_id:
                return child
        return None




    def get_children(self, child_id: str) -> 'list[Item]':
        """Return a list of child item with the specified identifier.

        Args:
            child_id (str): The identifier of the child items to return.

        Returns:
            list[Item]: The list of child items with the specified identifier.
        """
        return [child for child in self.children if child.identifier == child_id]





    def get_value(self, value_id: str = None, hr: bool = False) -> str:
        """Return the requested value.

        If value_id is not given, this method will return the value of this item.
        This value can be a referenced item or a string.

        If value_id is given, this method will return the value of the child item with
        the specified identifier. It is useful for example with a INDI item:
            If item.identifier == 'INDI', you can just use item.get_value('NAME') to get the name of the individual.

        Args:
            value_id (str): The identifier of the child item to return.
            hr (bool): If True, the returned value will be in human-readable format.
                       In example, if the value_id is NAME, the returned value won't have the '/' character.

        Returns:
            The value of the child item with value_id as identifier if it exists.
            The value of this item if value_id is not given.
        """
        if value_id:
            child = self.get_child(value_id)
            if child: return child.get_value(hr=hr)
            else: return None

        if self.value != '':
            if self.value[0] == self.value[-1] == '@': return self._referenced_item

        # Case specific for hr format
        if hr:

            # Remove every '/' and '_' from the name to make it prettier to read
            if self.identifier == 'NAME':
                returned_value: str = self.value
                for key, value in self.NAME_HR_CHANGES.items():
                    returned_value = returned_value.replace(key, value).strip()
                return returned_value
        

        
        # Non specific case, return raw value
        return self.value