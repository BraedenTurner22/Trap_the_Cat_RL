#All credit to goes to Thomas Rush, https://github.com/ThomasRush/py_a_star.git

from Node import Node
from SortedDictionary import SortedDictionary
from Node_Map import Node_Map

class AStar:
    """ Class determines the best path between a starting and ending point
    on a map of nodes.

    Uses the Manhattan implementation to determine distance between nodes.

    Keyword arguments:
    node_dict -- a dict of tuple / Node object pairs where tuple is a coordinate
    start_node -- a tuple representing the x/y coordinates of the path start
    end_node -- a tuple representing the x/y coordinates of the path end
    adjacency_function -- adjacency function takes a single tuple coordinate
    parameter and returns a dictionary of tuple / Node objects

    """



    def __init__(self):
        def sort_function(item):
            return item[1].f

        self.sort_function = sort_function



    def find_path(self, nodes, cat_position, edge_positions, adjacency_function):
        """
        Applies the A* algorithm to determine a path, given the dictionary
        of nodes provided in the constructor.

        Arguments:
        - nodes: Dictionary of all nodes in the grid.
        - cat_position: The starting position (x, y) of the cat.
        - adjacency_function: Function to get adjacent positions for a given node.

        Returns:
        A list of tuple coordinates representing the resulting path. 
        If no path was found, returns an empty list.
        """
    
        open = SortedDictionary(sort_function=self.sort_function)
        closed = SortedDictionary()

        # Shortened names
        get_adjacent_positions = adjacency_function

        # node_at = self.get_node_at
        p = Node.Property

        # Determine closest edge node to starting position
        closest_edge = None
        closest_distance = float('inf')

        for edge in edge_positions:
            # Manhattan distance from cat_position to edge
            print("cat_position before calculation:", cat_position)
            h = abs(cat_position[0] - edge[0] + abs(cat_position[1]) - edge[1])
            if h < closest_distance:
                closest_distance = h
                closest_edge = edge

        # If no edge is found, return an empty path
        if closest_edge is None:
            return []

        # Initialize starting node
        current_pos = cat_position
        current_node = nodes[current_pos]  # node_at(current_pos)
        open[current_pos] = current_node

        # Main A* loop
        while not current_node.is_edge():

            # If no path is found, exit
            if len(open) == 0:
                return {}
            else:

                # Get the lowest f-score position/node
                current_pos, current_node = open.pop()

                adjacent_positions = get_adjacent_positions(current_pos)

                # Mark current node as closed
                closed[current_pos] = None

                # Make sure they are not walls, and not in the closed list
                for adjacent_pos in adjacent_positions:

                    adjacent_node = nodes[adjacent_pos]

                    # If it's not a wall and not closed
                    if (adjacent_node.get_property() != p.WALL and
                            adjacent_pos not in closed):

                        # If already in the open list, check if this path is better
                        if adjacent_pos in open:
                            if adjacent_node.g > current_node.g + adjacent_node.get_terrain_score():
                                adjacent_node.set_parent_and_score(current_pos, current_node.g, closest_edge)

                                open[adjacent_pos] = adjacent_node
                        else:
                            # Add to open list and set parent/score
                            adjacent_node.set_parent_and_score(current_pos, current_node.g, closest_edge)

                            open[adjacent_pos] = adjacent_node

        # If a path was found, return a list of tuple coordinates
        # by tracing it backwards.
        path_pos = nodes[closest_edge].parent
        path = []
        while path_pos is not None:
            path.append(path_pos)
            path_pos = nodes[path_pos].parent

        # Remove the starting node
        path.pop()

        return path
