#All credit to goes to Thomas Rush, https://github.com/ThomasRush/py_a_star.git

"""
Implementation of A* using the "Manhattan" heuristic on hex or grid maps.
Uses Pygame for rendering to screen.
Uses SortedDictionary for faster lookups (speed bottleneck is rendering)

Usage:
Arrow keys move the "Start" node around the map
Spacebar generates a random map

Change settings to switch between hex/grid maps and map sizes.
"""
# Imports ==================================================

import sys  # gracefully handle exits
from Utilities import *  # helper classes and const definitions
from Renderer import Renderer  # draws graphics
from Node_Map import Node_Map  # holds map data
import pygame  # SDL wrapper
from pygame.locals import *  # for keyboard bindings
from AStar import AStar  # does the actual pathfinding

# Settings =================================================

map_size = Size(11, 11)  # X/Y dimensions of map
start =  None # path start point (set to None for random))
graphic_size = 60  # pixel size of each rendered node
background_color = pygame.Color(32, 32, 32)

# The percentage chance that any given node in the map
# will be a barrier when the map is randomly generated
# (barriers are not traversable)
barrier_percentage = .20

# Init =====================================================

pygame.init()

# Handle user-specified automatic display sizing
renderer = Renderer(graphic_size)

# Get the size of the map in pixels for setting the
# display size
fixed_width = 550
fixed_height = 725
map_size_pixels = (fixed_width, fixed_height)

screen = pygame.display.set_mode(map_size_pixels, pygame.RESIZABLE)
screen.fill(background_color)

# Create a randomly generated Node_Map map
node_map = Node_Map(map_size,
                    start,
                    edge_positions,
                    barrier_percentage)

#Set the start point explicitly
node_map.set_cat((5, 5))

astar = AStar()

# Main Loop ================================================

# render map up-front and only re-render
# when something changes
path = astar.find_path(node_map.get_node_dict(),
                       node_map.cat_position,
                       node_map.edge_position,
                       node_map.adjacency_function)
renderer.render(node_map, path, screen)

while True:

    for event in pygame.event.get():

        # User clicks on X to close window
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == K_ESCAPE:  # esc exits
                sys.exit(0)

            if event.key == K_UP:
                node_map.move(Direction.UP)

            if event.key == K_DOWN:
                node_map.move(Direction.DOWN)

            if event.key == K_LEFT:
                node_map.move(Direction.LEFT)

            if event.key == K_RIGHT:
                node_map.move(Direction.RIGHT)

            if event.key == K_SPACE:  # space generates a new random map
                node_map.generate_random_map()

            # Remove previous path data before re-running A*
            node_map.reset_map()

            path = astar.find_path(node_map.get_node_dict(),
                                   node_map.cat_position,
                                   node_map.edge_position,
                                   node_map.adjacency_function)

        # Adjust the display on user-resize
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.size)
            screen.fill(background_color)

        # Display the map
        renderer.render(node_map, path, screen)
