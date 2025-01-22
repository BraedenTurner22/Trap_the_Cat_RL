#All credit to goes to Thomas Rush, https://github.com/ThomasRush/py_a_star.git

from random import randint
from Node import Node
from Utilities import *


class Node_Map:

    # map is a dictionary of tuple/Node objects.
    # the tuple is an x/y coordinate
    node_map = {}

    #Tuple
    cat_coords = None

    #Tuples
    all_edge_node_coords = None

    # size is a Size object
    # start is tuple
    # barrier_percent is a float
    def __init__(self,
                 map_size: Size,
                 cat_coords,
                 barrier_percent):
        
        self.map_size = map_size
        self.cat_coords = cat_coords
        self.barrier_percent = barrier_percent

        # assert (terrain_min <= terrain_max)
        assert (0.0 <= barrier_percent <= 1.0)

        self.adjacency_function = self.get_adjacent_positions

        self.generate_random_map(self.cat_coords)



    def get_cat_coords(self):
        return self.cat_coords


    def get_all_edge_node_coords(self):
        return self.all_edge_node_coords



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
    


    def generate_random_map(self, cat_coords):

        node_properties = Node.Property

        # First, populate the entire map with default nodes
        for y in range(0, self.map_size.height):
            for x in range(0, self.map_size.width):
                self.node_map[(x, y)] = Node(node_properties.NOTHING)

        # Assign position for cat and edges
        self.cat_coords = self.set_cat(cat_coords)
        self.all_edge_node_coords = self.get_edge_coordinates(self.map_size)
 
        for y in range(0, self.map_size.height):
            for x in range(0, self.map_size.width):

                if self.cat_coords == (x, y):
                    node = Node(node_properties.CAT)
                    self.node_map[(x, y)] = node

                elif self.all_edge_node_coords == (x, y):
                    node = Node(node_properties.EDGE)
                    self.node_map[(x, y)] = node

                else:
                    # Determine whether this hex
                    # is a barrier or not
                    if randint(0, 100) < (self.barrier_percent * 100):
                        node = Node(node_properties.WALL)
                        self.node_map[(x, y)] = node
                    else:
                        # If the node is not a barrier, determine
                        # whether it has a terrain value. If so,
                        # calculate and set the terrain value.

                        # TODO: fix terrain problems
                        terrain_val = 1
                        node = Node(node_properties.NOTHING, terrain_val)

                        # if randint(0,100) < (self.terrain_percentage * 100):
                        #    terrain_val = randint(self.terrain_min * 100,self.terrain_max * 100)
                        #    terrain_val /= 100.0
                        #    node = Node(p.NOTHING,terrain_val)
                        # else:
                        #    node = Node(p.NOTHING)

                        self.node_map[(x, y)] = node



    def set_cat(self, pos_tuple):
        node = self.node_map[pos_tuple]
        node.set_property(Node.Property.CAT)
        self.cat_coords = pos_tuple



    def get_edge_coordinates(self, map_size: Size):
        self.all_edge_node_coords = set()

        for (x,y) in self.node_map.keys():
            # Check if the node is on the edge of the map
            if x == 0 or x == map_size.width - 1 or y == 0 or y == map_size.height - 1:
                self.all_edge_node_coords.add((x,y))

        return self.all_edge_node_coords



    def set_edge_property(self, map_size: Size):
        edge_coords = self.get_edge_coordinates(map_size)

        for coord in edge_coords:
            node = self.node_map.get(coord)
            if node:
                node.set_property(Node.Property.EDGE)



    def move(self, direction):
        d = Direction  # from Utilities module
        x = self.cat_coords[0]
        y = self.cat_coords[1]
        left_right_decider = None

        #Allows for y-axis movement if normal x-path has a wall but hexagons are still connected
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
    the confines of the map and is not a wall
    '''
    def is_valid_move(self, new_cat_position):

        np = Node.Property

        # Make sure the new position is within the
        # bounds of the map
        if not self.is_within_bounds(new_cat_position):
            return False

        # Check to see if the new position is a wall
        node = self.node_map[new_cat_position]
        if node.get_property() == (np.WALL):
            return False

        return True



    ''' Checks to see whether the supplied position is
    within the confines of the map
    '''
    def is_within_bounds(self, pos_tuple):
        s = self.map_size
        x = pos_tuple[0]
        y = pos_tuple[1]
        return 0 <= x < s.width and 0 <= y < s.height



    def get_adjacent_positions(self, cat_position):

        x = cat_position[0]
        y = cat_position[1]

        nodes = self.node_map

        # Four positions will be adjacent regardless of whether the
        # hex column is offset down or not. These happen to be the
        # cardinal directions (up,down,left,right) of a regular
        # coordinate grid, so we can use that function to get them.

        adjacent_positions = []

        positions = [(x - 1, y),  # left
                     (x + 1, y),  # right
                     (x, y - 1),  # up
                     (x, y + 1)]  # down

        for position in positions:
            if self.is_within_bounds(position):
                adjacent_positions.append(position)

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