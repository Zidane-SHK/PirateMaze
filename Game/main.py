import pygame
import sys
import time

# Import configurations
from config import GRAPH as ADJACENCY_LIST, COORDS as NODES, START_NODE, MISSION_CHECKPOINTS, HUMAN_SOL_PATH, CANNON_NODES
from visual import Visualizer
from algo import a_star_search

FPS = 60
MOVE_DELAY = 500

def solve_mission():
    full_path = []
    current_start = START_NODE
    cannons_loaded = [] # List to track loaded cannons

    print(".....Starting Mission calculations.....")

    for target in MISSION_CHECKPOINTS:
        # Check if we are done with 4 cannons before going to Final Node
        if target == '42' and len(cannons_loaded) < 4:
            print("Wait! We haven't loaded all 4 cannons yet.")
            # In this specific path logic, the loop handles it, but this is a safety check.

        print(f"Calculating segment: {current_start} -> {target}")

        segment_path = a_star_search(
            start_node=current_start, 
            goal_node=target, 
            graph=ADJACENCY_LIST, 
            coords=NODES, 
            human_path=HUMAN_SOL_PATH
        )

        if not segment_path:
            print(f"Error: No path was found from {current_start} to {target}.")
            # Fallback: If A* fails due to strict graph, just jump to target to keep animation alive
            segment_path = [current_start, target]

        # Logic: If we reached a cannon, mark it as loaded
        if target in CANNON_NODES:
            if target not in cannons_loaded:
                cannons_loaded.append(target)
                print(f"*** Cannon Loaded! Total: {len(cannons_loaded)}/4 ***")

        if full_path:
            full_path.extend(segment_path[1:])
        else:
            full_path.extend(segment_path)

        current_start = target

    print(".....Mission calculated succesfully.....")
    return full_path

def main():
    pygame.init()
    viz = Visualizer()
    clock = pygame.time.Clock()

    calculated_path = solve_mission()

    path_index = 0
    last_move_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    path_index = 0

        if calculated_path and path_index < len(calculated_path) - 1:
            if current_time - last_move_time > MOVE_DELAY:
                path_index += 1
                last_move_time = current_time

        current_node_id = calculated_path[path_index] if calculated_path else START_NODE

        viz.draw_background()
        viz.draw_graph(NODES, ADJACENCY_LIST)
        
        # We can pass the human path to visualize the 'Ideal' ghost path
        # viz.draw_path_line(HUMAN_SOL_PATH, NODES, color=viz.GREY) 
        
        viz.draw_path_line(calculated_path, NODES)
        viz.draw_player(current_node_id, NODES)

        pygame.display.flip()
        clock.tick(FPS)

    viz.save_image("saved.png")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()