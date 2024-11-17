import typing
class Node():
    def __init__(self, prefix: str = None, value: any = None, children: list['Node'] = None) -> None:
        self.prefix = prefix
        self.value = value
        self.children = children if children is not None else [None, None]
        
    def is_leaf(self) -> bool:
        return not any(self.children)

class Dictionary():
    def __init__(self) -> None:
        self.root = Node('', None, [Node("0", 0), Node("1", 1)])
    
    def _prefix_match(self, s1: str, s2: str) -> int:
        """Returns the length of the largest common prefix of s1 and s2"""
        i = 0
        for c1, c2 in zip(s1, s2):
            if c1 != c2:
                break
            i += 1
        return i
    
    def search(self, bit_str: str):
        """Searches a bit string in the dictionary and returns the value on success, or None if not found."""

        node = self.root
        i = 0
        length = len(bit_str)

        while i < length:
            bit = int(bit_str[i])

            # Search reached a leaf without fully matching bit_str
            if node.children[bit] is None:
                return None
            
            # Child diverges from bit_str -> there can't be a leaf that matches bit_str fully
            child = node.children[bit]
            if not bit_str.startswith(child.prefix, i):
                return None
            
            node = child
            i += len(child.prefix)
        return node.value
            
    def insert(self, bit_str: str, value: any):
        """
        Inserts a new value, with bit_str as the key, and updates the value if it already exists.
        Returns False if the key was updated, or True if it was inserted fresh.
        """

        node = self.root
        i = 0
        length = len(bit_str)

        while i < length:
            bit = int(bit_str[i])
            if node.children[bit] is None:
                # Creates a new node with the rest of bit_str as the key
                new_node = Node(bit_str[i:], value)
                node.children[bit] = new_node
                return True
            
            child = node.children[bit]
            common_prefix_length = self._prefix_match(child.prefix, bit_str[i:])

            if common_prefix_length == len(child.prefix):
                # The whole prefix matched -> move to the apropriate child
                node = child
                i += common_prefix_length
            else:
                # The strings diverge at this node -> separate into 2 subtrees
                new_prefix = child.prefix[:common_prefix_length]
                existing_suffix = child.prefix[common_prefix_length:]
                new_suffix = bit_str[i + common_prefix_length:]

                # Create new intermediary node for common prefix
                new_node = Node(new_prefix)

                # Transform old node and add it as child to the new node
                child.prefix = existing_suffix
                existing_suffix_bit = int(existing_suffix[0])
                new_node.children[existing_suffix_bit] = child

                # Adds a leaf to the new node if there is a suffix left in bit_str
                if len(new_suffix) > 0:
                    leaf_node = Node(new_suffix, value)
                    leaf_node_bit = int(new_suffix[0])
                    new_node.children[leaf_node_bit] = leaf_node
                else:
                    new_node.value = value
                
                # Adds new intermediary node to the tree 
                node.children[bit] = new_node
                return True

        # The key already existed in the trie -> update its value
        node.value = value
        return False
    
    def remove(self, bit_str: str) -> bool:
        """
        Removes key from dictionary, returning True on success and False on failure
        (ex. if the key isn't in the dictionary)
        """

        def _remove(node: Node, bit_str: str, depth: int) -> tuple[bool, bool]:
            """
            Recursive method for removing key.
            Returns a tuple (bool, bool) indicating if the removal was successful
            and if the child can be removed, respectively.
            """
            # Node doesn't exist
            if node is None:
                return (False, False)

            # When the corresponding node is found
            if depth == len(bit_str):
                if node.value is not None:
                    node.value = None  # Delete value
                    return (True, node.is_leaf()) # Node is leaf -> can be deleted
                
                return (True, False)

            bit = int(bit_str[depth])
            if node.children[bit] is None:
                return (False, False)  # String is not in trie
            
            child = node.children[bit]

            common_prefix_length = self._prefix_match(child.prefix, bit_str[depth:])

            # bit_str diverges from the prefix, so it can't be on the trie
            if common_prefix_length < len(child.prefix):
                return (False, False)
            
            success, can_remove_child = _remove(child, bit_str, depth + common_prefix_length)
            if can_remove_child:
                node.children[bit] = None

                # If node now became an empty leaf, it can be removed too
                if node.is_leaf() and node.value is None:
                    return (success, True)

                # Node is not root and stil has another child that can be compacted into it
                if node.prefix != '' and node.children.count(None) == 1:
                    remaining_child = node.children[1 - bit]
                    node.prefix += remaining_child.prefix
                    node.value = remaining_child.value
                    node.children = remaining_child.children
                    return (success, False)

            # Child couldn't be removed. Assuming tree was valid before, it should remain valid.
            return (success, False)

        # Starts recursive removal from root
        success, _ = _remove(self.root, bit_str, 0)
        return success

        