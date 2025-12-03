import pygame
import sys
import time

# importing from the other files
# Note: We alias GRAPH to ADJACENCY_LIST and COORDS to NODES to match usage
from config import GRAPH as ADJACENCY_LIST, COORDS as NODES, START_NODE, MISSION_CHECKPOINTS
from visual import Visualizer
from algo import a_star_search

# animation speed
FPS = 60
MOVE_DELAY = 500  # 500ms delay between nodes

def solve_mission():
    full_path = []
    current_start = START_NODE

    print(".....Starting Mission calculations.....")

    for target in MISSION_CHECKPOINTS:
        # moving to a mission target
        print(f"Calculating segment: {current_start} -> {target}")

        # Run A*
        segment_path = a_star_search(current_start, target, ADJACENCY_LIST, NODES)

        if not segment_path:
            print(f"Error: No path was found from {current_start} to {target}. Try again")
            return []

        # Avoid duplicating connection nodes (end of prev is start of next)
        if full_path:
            full_path.extend(segment_path[1:])
        else:
            full_path.extend(segment_path)

        current_start = target

    print(".....Mission calculated successfully.....")
    return full_path


def main():
    # initializing the visualizer
    pygame.init() # Ensure pygame is initialized first
    viz = Visualizer()
    clock = pygame.time.Clock()

    # running algorithm
    calculated_path = solve_mission()

    # animation setup
    path_index = 0
    last_move_time = pygame.time.get_ticks() # Fixed .get.ticks()

    # game loop
    running = True
    while running:
        current_time = pygame.time.get_ticks() # Fixed pygames typo

        # use of controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    path_index = 0

        # animation logic
        if calculated_path and path_index < len(calculated_path) - 1:
            if current_time - last_move_time > MOVE_DELAY:
                path_index += 1
                last_move_time = current_time

        # id of the current node
        current_node_id = calculated_path[path_index] if calculated_path else START_NODE

        # drawing program
        viz.draw_background()
        viz.draw_graph(NODES, ADJACENCY_LIST)
        viz.draw_path_line(calculated_path, NODES)
        viz.draw_player(current_node_id, NODES)

        # updating display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit() # Fixed sys.exist()

if __name__ == "__main__":
    main()