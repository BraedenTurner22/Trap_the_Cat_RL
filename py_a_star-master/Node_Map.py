#All credit to goes to Thomas Rush, https://github.com/ThomasRush/py_a_star.git

from random import randint
from Node import Node
from Utilities import *


class Node_Map:

    # map is a dictionary of tuple/Node objects.
    # the tuple is an x/y coordinate
    node_map = {}

    cat_position = None
    edge_positions = None

    # size is a Size object
    # start and end are tuples
    # barrier_percent is a float
    def __init__(self,
                 size,
                 start,
                 edges,
                 barrier_percent):
        self.size = size

        assert (0.0 <= barrier_percent <= 1.0)
        # assert (terrain_min <= terrain_max)

        self.cat_position = start
        self.edge_positions = edges
        self.barrier_percent = barrier_percent
        self.adjacency_function = self.get_adjacent_hex_positions

        self.generate_random_map()

    def get_node_dict(self):
        return self.node_map

    def get_node_at(self, position):
        return self.node_map[position]

    def get_property_at(self, position):
        node = self.node_map[position]
        return node.get_property()

    def reset_map(self):
        for pos, node in self.node_map.items():
            node.set_parent(None)
            if node.node_property == Node.Property.PATH:
                node.node_property = Node.Property.NOTHING

    def get_random_position(self):
        w = self.size.width
        h = self.size.height
        return randint(0, w - 1), randint(0, h - 1)

    def generate_random_map(self):

        p = Node.Property

        # First, populate the entire map with default nodes
        for y in range(0, self.size.height):
            for x in range(0, self.size.width):
                self.node_map[(x, y)] = Node(p.NOTHING)

        # Assign random positions for cat and edge
        if self.random_start:
            self.cat_position = self.get_random_position()
        if self.random_end:
            self.edge_positions = self.get_random_position()

        # Ensure cat and edge are valid and distinct
        while self.cat_position == self.edge_positions or self.node_map[self.cat_position].get_property() == Node.Property.WALL:
            self.cat_position = self.get_random_position()
        while self.edge_positions == self.cat_position or self.node_map[self.edge_positions].get_property() == Node.Property.WALL:
            self.edge_positions = self.get_random_position()


        p = Node.Property
 
        for y in range(0, self.size.height):
            for x in range(0, self.size.width):

                if self.cat_position == (x, y):
                    node = Node(p.CAT)
                    self.node_map[(x, y)] = node

                elif self.edge_positions == (x, y):
                    node = Node(p.EDGE)
                    self.node_map[(x, y)] = node

                else:
                    # Determine whether this hex
                    # is a barrier or not
                    if randint(0, 100) < (self.barrier_percent * 100):
                        node = Node(p.WALL)
                        self.node_map[(x, y)] = node
                    else:
                        # If the node is not a barrier, determine
                        # whether it has a terrain value. If so,
                        # calculate and set the terrain value.

                        # TODO: fix terrain problems
                        terrain_val = 1
                        node = Node(p.NOTHING, terrain_val)

                        # if randint(0,100) < (self.terrain_percentage * 100):
                        #    terrain_val = randint(self.terrain_min * 100,self.terrain_max * 100)
                        #    terrain_val /= 100.0
                        #    node = Node(p.NOTHING,terrain_val)
                        # else:
                        #    node = Node(p.NOTHING)

                        self.node_map[(x, y)] = node

    def set_cat(self, pos_tuple):
        # Remove previous start property
        node = self.node_map[self.cat_position]
        node.set_property(Node.Property.NOTHING)

        # New start
        node = self.node_map[pos_tuple]
        node.set_property(Node.Property.CAT)
        self.cat_position = pos_tuple

    def set_edge(self, pos_tuple):

        # Remove previous edge property
        node = self.node_map[self.edge_positions]
        node.set_property(Node.Property.NOTHING)

        # New end
        node = self.node_map[pos_tuple]
        node.set_property(Node.Property.EDGE)
        self.edge_positions = pos_tuple

    def move(self, direction):
        d = Direction  # from Utilities module
        x = self.cat_position[0]
        y = self.cat_position[1]

        #Allows for y-axis movement if normal x-path has a wall but hexagons are still connected
        left_right_decider = None
        left_right_decider = y - 1 if x % 2 == 0 else y + 1

        cats_new_position = (x ,y)

        if direction == d.UP:
            if self.is_valid_move((x, y - 1)):
                cats_new_position = (x, y - 1)
            else:
                cats_new_position = (x, y)

        elif direction == d.DOWN:
            if self.is_valid_move((x, y + 1)):
                cats_new_position = (x, y + 1)
            else:
                cats_new_position = (x, y)

        elif direction == d.LEFT:
            if self.is_valid_move((x - 1, y)):
                cats_new_position = (x - 1, y)
            elif self.is_valid_move((x - 1, left_right_decider)):
                cats_new_position = (x - 1, left_right_decider)
            else:
                cats_new_position = (x, y)
            
        elif direction == d.RIGHT:
            if self.is_valid_move((x + 1, y)):
                cats_new_position = (x + 1, y)
            elif self.is_valid_move((x + 1, left_right_decider)):
                cats_new_position = (x + 1, left_right_decider)
            else:
                cats_new_position = (x, y)
        
        self.set_cat(cats_new_position)

    ''' Checks to see whether the new position is within
    the confines of the map and is not a barrier
    or the path end
    '''

    def is_valid_move(self, new_pos):

        # TODO: clean up this multiple-exit function

        np = Node.Property

        # Make sure the new position is within the
        # bounds of the map
        if not self.is_within_bounds(new_pos):
            return False

        # Check to see if the new position is a wall
        node = self.node_map[new_pos]
        if node.get_property() in (np.WALL, np.EDGE):
            return False

        return True

    ''' Checks to see whether the supplied position is
    within the confines of the map
    '''

    def is_within_bounds(self, pos_tuple):
        s = self.size
        x = pos_tuple[0]
        y = pos_tuple[1]
        return 0 <= x < s.width and 0 <= y < s.height

    def get_adjacent_hex_positions(self, current_pos):

        x = current_pos[0]
        y = current_pos[1]

        nodes = self.node_map

        # Four positions will be adjacent regardless of whether the
        # hex column is offset down or not. These happen to be the
        # cardinal directions (up,down,left,right) of a regular
        # coordinate grid, so we can use that function to get them.
        adjacent_positions = self.get_adjacent_grid_positions(current_pos)

        # If it's an even column, it's offset DOWN
        # (adding one because it's zero-based)
        if (x + 1) % 2 == 0:
            down_right = (x + 1, y + 1)
            if self.is_within_bounds(down_right):
                adjacent_positions.append(down_right)

            down_left = (x - 1, y + 1)
            if self.is_within_bounds(down_left):
                adjacent_positions.append(down_left)

        # Otherwise it's offset UP
        else:
            up_left = (x - 1, y - 1)
            if self.is_within_bounds(up_left):
                adjacent_positions.append(up_left)

            up_right = (x + 1, y - 1)
            if self.is_within_bounds(up_right):
                adjacent_positions.append(up_right)

        return adjacent_positions

    def get_adjacent_grid_positions(self, current_pos):

        adjacent_positions = []

        x = current_pos[0]
        y = current_pos[1]

        positions = [(x - 1, y),  # left
                     (x + 1, y),  # right
                     (x, y - 1),  # up
                     (x, y + 1)]  # down

        for position in positions:
            if self.is_within_bounds(position):
                adjacent_positions.append(position)

        return adjacent_positions
