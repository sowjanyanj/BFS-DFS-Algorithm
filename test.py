import tkinter as tk
from tkinter import ttk
import random
import time
from collections import deque

class BFSVisualization:
    def __init__(self, root):
        self.root = root
        self.root.title("BFS/DFS Shortest Path Visualization")
        self.root.geometry("1200x800")  # Set window size
        self.root.configure(bg="gray")

        main_heading = tk.Label(root, text="FINDING NEIGHBORING PLACES NEAR RV COLLEGE OF ENGINEERING",
                                font=("Helvetica", 20, "bold"), fg="black")
        main_heading.pack(pady=20)

        self.canvas_frame = tk.Frame(root, bd=5, relief="solid")
        self.canvas_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.info_frame = tk.Frame(root, bd=5, relief="solid")
        self.info_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        buttons_heading = tk.Label(self.info_frame, text="CHOOSE PLACE", font=("Helvetica", 14, "bold"))
        buttons_heading.pack()

        graph_heading = tk.Label(self.canvas_frame, text="NEIGHBORING PLACES", font=("Helvetica", 14, "bold"),
                                 fg="black")
        graph_heading.pack()

        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.text_box = tk.Text(self.info_frame, width=40, height=10, wrap=tk.WORD)
        self.text_box.pack(fill=tk.BOTH, expand=True)

        self.places = {
            'Mysore Road': (400, 100),  # Moving "Mysore Road" upwards
            'Kengeri': (100, 300),
            'Rajarajeshwari Nagar': (300, 400),  # Adjusted position
            'Jnanabharathi': (100, 100),
            'Nagarbhavi': (400, 300),
        }

        # Reduced the number of edges to fit the screen
        self.edges = [
            ('Mysore Road', 'Kengeri', 10), ('Mysore Road', 'Jnanabharathi', 8),
            ('Kengeri', 'Rajarajeshwari Nagar', 5), ('Kengeri', 'Nagarbhavi', 7),
            ('Rajarajeshwari Nagar', 'Nagarbhavi', 3),
        ]

        self.visited = set()
        self.delay = 1000

        self.current_place = None
        self.create_buttons()
        self.draw_graph()

        # Add a combobox to select the algorithm
        self.algorithm_label = tk.Label(self.info_frame, text="Select Algorithm", font=("Helvetica", 12, "bold"))
        self.algorithm_label.pack()
        self.algorithm_var = tk.StringVar()
        self.algorithm_combobox = ttk.Combobox(self.info_frame, textvariable=self.algorithm_var,
                                               values=["BFS", "DFS"])
        self.algorithm_combobox.pack()
        self.algorithm_combobox.set("BFS")  # Default selection

        # Labels for displaying execution times
        self.bfs_time_label = tk.Label(self.info_frame, text="BFS Execution Time:", font=("Helvetica", 12))
        self.bfs_time_label.pack()
        self.dfs_time_label = tk.Label(self.info_frame, text="DFS Execution Time:", font=("Helvetica", 12))
        self.dfs_time_label.pack()

    def random_color(self):
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw_graph(self):
        for edge in self.edges:
            start, end, distance = edge
            x1, y1 = self.places[start]
            x2, y2 = self.places[end]
            self.canvas.create_line(x1, y1, x2, y2, fill=self.random_color(), width=5)
            # Display the distance on the canvas
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(distance), fill='black',
                                    font=("Helvetica", 10), anchor='n')

        for place, coords in self.places.items():
            x, y = coords
            self.canvas.create_text(x, y, text=place, fill='black', font=("Helvetica", 10), anchor='n')

    def show_running_arrows(self, place):
        neighbors = [(neighbor[1], neighbor[2]) for neighbor in self.edges if neighbor[0] == place]

        if not neighbors:
            return

        for neighbor, distance in neighbors:
            x1, y1 = self.places[place]
            x2, y2 = self.places[neighbor]

            # Calculate arrow position above the edge
            arrow_x = (x1 + x2) / 2
            arrow_y = (y1 + y2) / 2 - 15  # Positioned above the edge

            # Draw the main edge
            self.canvas.create_line(x1, y1, x2, y2, fill='darkblue', width=3, smooth=True)

            # Draw the arrow line above the main edge
            arrow_id = self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=3, smooth=True)

            # Add shadow effect to the main edge
            self.canvas.create_line(x1, y1, x2, y2, fill='gray', width=5, smooth=True)

            # Display the distance on the arrow
            self.canvas.create_text(arrow_x, arrow_y, text=str(distance), fill='white',
                                    font=("Helvetica", 10), anchor='s')

            self.root.update()
            time.sleep(1)  # Sleep for 1 second to show the arrow animation
            self.canvas.delete(arrow_id)  # Remove the arrow

    def show_neighbors(self, place):
        visited_neighbors = [(neighbor[1], neighbor[2]) for neighbor in self.edges if neighbor[0] == place]

        if not visited_neighbors:
            neighbors_str = "No unvisited neighboring places"
        else:
            neighbors_str = ', '.join([f"{neighbor[0]} ({neighbor[1]} km)" for neighbor in visited_neighbors])

        # Clear the previous response in the text box
        self.text_box.delete(1.0, tk.END)

        # Display the new response in the text box
        self.text_box.insert(tk.END, f"Neighbors of {place}: {neighbors_str}")

        # Show running arrows to represent traversal
        self.show_running_arrows(place)

    def find_shortest_path_bfs(self, start, end):
        start_time = time.time()
        # Implement BFS to find the shortest path
        visited = set()
        queue = deque([(start, [])])

        while queue:
            current, path = queue.popleft()
            visited.add(current)

            if current == end:
                end_time = time.time()
                bfs_execution_time = end_time - start_time
                self.bfs_time_label.config(text=f"BFS Execution Time: {bfs_execution_time:.4f} seconds")
                return path + [current]

            neighbors = [neighbor[1] for neighbor in self.edges if neighbor[0] == current]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [current]))

    def find_shortest_path_dfs(self, start, end):
        start_time = time.time()
        # Implement DFS to find the shortest path
        visited = set()
        stack = [(start, [])]

        while stack:
            current, path = stack.pop()
            visited.add(current)

            if current == end:
                end_time = time.time()
                dfs_execution_time = end_time - start_time
                self.dfs_time_label.config(text=f"DFS Execution Time: {dfs_execution_time:.4f} seconds")
                return path + [current]

            neighbors = [neighbor[1] for neighbor in self.edges if neighbor[0] == current]
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, path + [current]))

    def find_shortest_path(self, start, end):
        selected_algorithm = self.algorithm_var.get()
        if selected_algorithm == "BFS":
            return self.find_shortest_path_bfs(start, end)
        elif selected_algorithm == "DFS":
            return self.find_shortest_path_dfs(start, end)

    def show_shortest_path(self, start, end):
        shortest_path = self.find_shortest_path(start, end)
        if not shortest_path:
            shortest_path_str = "No path found."
        else:
            shortest_path_str = " -> ".join(shortest_path)

        # Clear the previous response in the text box
        self.text_box.delete(1.0, tk.END)

        # Display the new response in the text box
        self.text_box.insert(tk.END, f"Shortest path from {start} to {end} using {self.algorithm_var.get()}: {shortest_path_str}")

    def create_buttons(self):
        for place in self.places:
            button = tk.Button(self.info_frame, text=place, width=20, command=lambda p=place: self.show_neighbors(p),
                               bg=self.random_color(), fg='white', font=("Helvetica", 12))
            button.pack(fill=tk.BOTH, expand=True)

        # Add a button to find the shortest path
        find_path_button = tk.Button(self.info_frame, text="Find Shortest Path", width=20,
                                     command=lambda: self.show_shortest_path("Mysore Road", "Nagarbhavi"),
                                     bg=self.random_color(), fg='white', font=("Helvetica", 12))
        find_path_button.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = BFSVisualization(root)
    app.run()
