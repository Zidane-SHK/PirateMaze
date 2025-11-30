from PIL import Image
import matplotlib.pyplot as plt

image_path = r'C:\Users\dell\Desktop\uni\ship.jpg'

def pick_coordinates(image_path):
    """Interactive coordinate picker"""
    img = Image.open(image_path)
    
    # Resize to target dimensions
    img = img.resize((1000, 1200))
    
    coords = {}
    
    def onclick(event):
        if event.xdata and event.ydata:
            node_id = input(f"Node ID for ({int(event.xdata)}, {int(event.ydata)}): ")
            coords[node_id] = (int(event.xdata), int(event.ydata))
            print(f"Saved: '{node_id}': ({int(event.xdata)}, {int(event.ydata)})")
    
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.imshow(img)
    ax.set_title("Click on each node (close window when done)")
    
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    
    return coords

# Usage
coordinates = pick_coordinates('C:\\Users\\dell\\Desktop\\uni\\ship.jpg')

# Print in config.py format
print("\nCOORDS = {")
for node, (x, y) in sorted(coordinates.items()):
    print(f"    '{node}': ({x}, {y}),")
print("}")