import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Visualizer:
    def __init__(self):
        # 1. Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cannon Challenge - 4 Color Visualization")
        
        # 2. Define Colors
        self.WHITE = (255, 255, 255)
        self.GREY = (200, 200, 200)
        
        self.PATH_COLORS = [
            (0, 0, 0),       # Black
            (0, 0, 255),     # Blue
            (255, 20, 147),  # Deep Pink
            (50, 205, 50)    # Lime Green
        ]
        
        # We switch colors ONLY when we reach the Cannons on the Top Deck
        self.SWITCH_NODES = {'49', '50'}
        
        # 3. Load Background Image
        self.bg_image = None
        try:
            raw_image = pygame.image.load("maze.jpg")
            self.bg_image = pygame.transform.scale(raw_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError:
            print("ERROR: Image not found. Please check filename.")
            self.bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_image.fill(self.WHITE)

    def draw_background(self):
        """Draw the ship image."""
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))

    def draw_graph(self, nodes, adjacency_list):
        """
        Draw the underlying graph (faint grey lines).
        """
        for node_id, neighbors in adjacency_list.items():
            if node_id in nodes:
                start_pos = nodes[node_id]
                for neighbor_info in neighbors:
                    # neighbor_info is usually (id, weight)
                    neighbor_id = neighbor_info[0]
                    if neighbor_id in nodes:
                        end_pos = nodes[neighbor_id]
                        # Draw thin grey line
                        pygame.draw.line(self.screen, self.GREY, start_pos, end_pos, 2)
                        
        # Draw Nodes (White dots)
        for pos in nodes.values():
            pygame.draw.circle(self.screen, self.WHITE, pos, 3)

    def draw_path_line(self, full_path, nodes_dict):
        """
        Draws the path.
        """
        if not full_path or len(full_path) < 2:
            return

        current_color_idx = 0
        
        # Iterate through every step of the path
        for i in range(len(full_path) - 1):
            node_a = full_path[i]
            node_b = full_path[i+1]

            if node_a in nodes_dict and node_b in nodes_dict:
                p1 = nodes_dict[node_a]
                p2 = nodes_dict[node_b]

                # 1. Pick the color
                color = self.PATH_COLORS[current_color_idx % len(self.PATH_COLORS)]

                # 2. Draw the line segment
                pygame.draw.line(self.screen, color, p1, p2, width=6)
                pygame.draw.circle(self.screen, color, p1, 3) # Smooth joint

                # 3. Check if we need to switch colors
                if node_b in self.SWITCH_NODES:
                    current_color_idx += 1

    def draw_player(self, current_node_id, nodes):
        """Draws Lethal Luke."""
        if current_node_id in nodes:
            pos = nodes[current_node_id]
            
            # Yellow
            pygame.draw.circle(self.screen, (255, 255, 0), pos, 14, 0)
            # Red Body
            pygame.draw.circle(self.screen, (255, 0, 0), pos, 8, 0)
            # Outline
            pygame.draw.circle(self.screen, (0, 0, 0), pos, 8, 2)