#All credit to goes to Thomas Rush, https://github.com/ThomasRush/py_a_star.git

import pygame
from Node import Node

class Renderer:
    START_HEX_COLOR = pygame.Color(0, 255, 0)
    END_HEX_COLOR = pygame.Color(255, 0, 0)
    PATH_COLOR = pygame.Color(192, 192, 0)
    BARRIER_COLOR = pygame.Color(0, 0, 255)

    def __init__(self, graphic_size):
        self.graphic_size = graphic_size

        try:
            create_graphic = self.create_hex_gfx
            self.render = self.render_hex_map
        except:
            raise Exception("Map type not found")

        self.empty_node_gfx = create_graphic(None)
        self.start_node_gfx = create_graphic(self.START_HEX_COLOR)
        self.end_node_gfx = create_graphic(self.END_HEX_COLOR)
        self.path_node_gfx = create_graphic(self.PATH_COLOR)
        self.barrier_node_gfx = create_graphic(self.BARRIER_COLOR)

    def create_hex_gfx(self, color):
        hex_size = self.graphic_size

        s = pygame.Surface((hex_size, hex_size))
        magenta = pygame.Color(255, 0, 255)
        s.fill(magenta)
        white = pygame.Color(255, 255, 255, 0)

        half = hex_size / 2
        quarter = hex_size / 4

        # Hexagon points
        #
        #   1___2
        #   /   \
        # 6/     \3
        #  \     /
        #   \___/
        #   5   4

        # Color the hex region
        if color is not None:
            points = []
            points.append((quarter, 0))  # 1
            points.append((3 * quarter, 0))  # 2
            points.append((4 * quarter - 1, half))  # 3
            points.append((3 * quarter, 4 * quarter - 1))  # 4
            points.append((quarter, 4 * quarter - 1))  # 5
            points.append((0, half))  # 6

            pygame.draw.polygon(s, color, points)

        # Draw outlines
        pygame.draw.line(s, white, (0, half), (quarter, 0), 1)
        pygame.draw.line(s, white, (quarter, 0), (3 * quarter, 0), 1)
        pygame.draw.line(s, white, (3 * quarter, 0), (4 * quarter - 1, half), 1)
        pygame.draw.line(s, white, (4 * quarter - 1, half), (3 * quarter, 2 * half), 1)
        pygame.draw.line(s, white, (3 * quarter, 2 * half - 1), (quarter, 2 * half - 1), 1)
        pygame.draw.line(s, white, (quarter, 2 * half - 1), (0, half), 1)

        # Set color key to magenta for transparency
        s.set_colorkey(magenta)

        return s

    def render_hex_map(self, node_map, path, screen):

        # Get some short names to work with
        m_width = node_map.size.width
        m_height = node_map.size.height
        g = self.graphic_size  # hex size

        grid_padding_x = 20 #Horizontal padding
        grid_padding_y = 20 #Vertical padding
        grid_padding_bottom = 80  # Extra bottom padding to prevent cut-off
    
        magenta = pygame.Color(255, 0, 255)

        p = Node.Property

        # Map graphics buffer; account for extra
        # space required by staggered hexagons
        h = int(m_height * g) + grid_padding_bottom
        w = int(m_width * g) + grid_padding_x

        b = pygame.Surface((w, h))

        # Magenta is the transparency color
        b.set_colorkey(magenta)

        for y in range(0, m_height):
            for x in range(0, m_width):

                x_blit = (x * g) + grid_padding_x
                y_blit = (y * g) + grid_padding_y

                # Offset even rows downward
                if x % 2 != 0:
                    y_blit += (g / 2)

                # Account for the fact that each
                # column will be "pulled back" by a
                # quarter of a hex so they interlock.
                if x > 0:
                    x_blit -= ((g / 4) + 1) * x

                node_property = node_map.get_property_at((x, y))

                if (x, y) in path:
                    b.blit(self.path_node_gfx, (x_blit, y_blit))
                elif node_property == p.CAT:
                    b.blit(self.start_node_gfx, (x_blit, y_blit))
                elif node_property == p.EDGE:
                    b.blit(self.end_node_gfx, (x_blit, y_blit))
                elif node_property == p.WALL:
                    b.blit(self.barrier_node_gfx, (x_blit, y_blit))
                else:
                    b.blit(self.empty_node_gfx, (x_blit, y_blit))

        # Show the screen buffer
        screen.blit(b, (0,0))
        pygame.display.flip()
