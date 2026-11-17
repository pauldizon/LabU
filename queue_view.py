
import tkinter as tk
from tkinter import ttk, messagebox
from queue_ds import Queue


class QueueView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=25)

        # Initialize the Queue with a maximum capacity of 10.
        self.queue = Queue(capacity=10)

        # Count operations for the activity history.
        self.operation_count = 0

        self.create_widgets()
        self.refresh_queue()

    def create_widgets(self):
        # Main heading and explanation of FIFO.
        ttk.Label(
            self,
            text="Queue Visualizer",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        ttk.Label(
            self,
            text="First In, First Out (FIFO) - The first element added is the first removed."
        ).pack(anchor="w", pady=(5, 15))

        # --------------------------------------------
        # SECTION 1: QUEUE OPERATIONS
        # --------------------------------------------
        operation_frame = ttk.LabelFrame(
            self,
            text="Queue Operations",
            padding=12
        )
        operation_frame.pack(fill="x", pady=8)

        # Input field for the element to be enqueued.
        self.item_entry = ttk.Entry(
            operation_frame,
            width=30,
            font=("Segoe UI", 10)
        )
        self.item_entry.pack(side="left", padx=5)

        ttk.Button(
            operation_frame,
            text="Enqueue",
            command=self.enqueue_item
        ).pack(side="left", padx=5)

        ttk.Button(
            operation_frame,
            text="Dequeue",
            command=self.dequeue_item
        ).pack(side="left", padx=5)

        ttk.Button(
            operation_frame,
            text="Peek",
            command=self.peek_item
        ).pack(side="left", padx=5)

        # --------------------------------------------
        # SECTION 2: QUEUE VISUALIZATION
        # --------------------------------------------
        visualization_frame = ttk.LabelFrame(
            self,
            text="Queue Visualization",
            padding=12
        )
        visualization_frame.pack(
            fill="both",
            expand=True,
            pady=8
        )

        # Canvas draws the queue elements horizontally.
        self.queue_canvas = tk.Canvas(
            visualization_frame,
            background="white",
            highlightthickness=1,
            highlightbackground="#CCCCCC",
            height=250
        )
        self.queue_canvas.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # --------------------------------------------
        # SECTION 3: QUEUE INFORMATION
        # --------------------------------------------
        self.status_label = ttk.Label(
            self,
            text="Elements: 0 / 10",
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(anchor="w", pady=5)

        # --------------------------------------------
        # SECTION 4: OPERATION HISTORY
        # --------------------------------------------
        history_frame = ttk.LabelFrame(
            self,
            text="Operation History",
            padding=8
        )
        history_frame.pack(fill="x", pady=8)

        self.history_list = tk.Listbox(
            history_frame,
            height=4,
            font=("Consolas", 9)
        )
        self.history_list.pack(fill="x")

        # Record the initial state.
        self.add_history("Queue initialized. Capacity: 10 elements.")

    def enqueue_item(self):
        # ENQUEUE: Add a new element at the rear of the queue.
        item = self.item_entry.get().strip()

        # Prevent empty entries.
        if not item:
            messagebox.showwarning(
                "Missing Input",
                "Please enter an item to enqueue."
            )
            return

        try:
            self.queue.enqueue(item)

            # Clear the input field after a successful operation.
            self.item_entry.delete(0, tk.END)

            self.add_history(f"ENQUEUE: Added {item}.")
            self.refresh_queue()

        except OverflowError as error:
            # Handle attempts to exceed queue capacity.
            self.add_history("ENQUEUE FAILED: Queue overflow.")
            messagebox.showerror("Queue Overflow", str(error))

    def dequeue_item(self):
        # DEQUEUE: Remove the oldest element from the front.
        try:
            removed = self.queue.dequeue()

            self.add_history(f"DEQUEUE: Removed {removed}.")
            self.refresh_queue()

        except IndexError as error:
            # Handle attempts to remove from an empty queue.
            self.add_history("DEQUEUE FAILED: Queue underflow.")
            messagebox.showerror("Queue Underflow", str(error))

    def peek_item(self):
        # PEEK: View the front element without removing it.
        try:
            front = self.queue.peek()

            self.add_history(f"PEEK: Front element is {front}.")

            messagebox.showinfo(
                "Front Element",
                f"Current front element: {front}"
            )

        except IndexError as error:
            self.add_history("PEEK FAILED: Queue is empty.")
            messagebox.showwarning("Empty Queue", str(error))

    def refresh_queue(self):
        # Redraw the queue whenever its contents change.
        self.queue_canvas.delete("all")

        items = self.queue.display()

        canvas_width = self.queue_canvas.winfo_width()
        canvas_height = self.queue_canvas.winfo_height()

        # Provide fallback dimensions before the Canvas is rendered.
        if canvas_width < 100:
            canvas_width = 700

        if canvas_height < 100:
            canvas_height = 250

        box_width = 100
        box_height = 45
        gap = 10

        total_width = len(items) * box_width + max(0, len(items) - 1) * gap

        # Center the queue horizontally.
        start_x = max(20, (canvas_width - total_width) / 2)
        center_y = canvas_height / 2

        if not items:
            self.queue_canvas.create_text(
                canvas_width / 2,
                center_y,
                text="QUEUE IS EMPTY",
                fill="#777777",
                font=("Segoe UI", 14, "bold")
            )

        else:
            for index, item in enumerate(items):
                x1 = start_x + index * (box_width + gap)
                x2 = x1 + box_width
                y1 = center_y - box_height / 2
                y2 = center_y + box_height / 2

                # Highlight the FRONT element in green.
                if index == 0:
                    fill_color = "#D9F2E3"
                    outline_color = "#23834B"
                    text_color = "#14532D"
                else:
                    fill_color = "#E5EAF2"
                    outline_color = "#8293AA"
                    text_color = "#24364B"

                self.queue_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_color,
                    outline=outline_color,
                    width=2
                )

                self.queue_canvas.create_text(
                    (x1 + x2) / 2,
                    center_y,
                    text=str(item),
                    fill=text_color,
                    font=("Segoe UI", 9, "bold")
                )

                # Label the oldest element as FRONT.
                if index == 0:
                    self.queue_canvas.create_text(
                        (x1 + x2) / 2,
                        y1 - 15,
                        text="FRONT",
                        fill="#23834B",
                        font=("Segoe UI", 9, "bold")
                    )

                # Label the newest element as REAR.
                if index == len(items) - 1:
                    self.queue_canvas.create_text(
                        (x1 + x2) / 2,
                        y2 + 15,
                        text="REAR",
                        fill="#245B9B",
                        font=("Segoe UI", 9, "bold")
                    )

        # Update the element counter.
        self.status_label.config(
            text=f"Elements: {self.queue.size()} / {self.queue.capacity}"
        )

    def add_history(self, message):
        # Record each successful or unsuccessful operation.
        self.operation_count += 1

        self.history_list.insert(
            tk.END,
            f"{self.operation_count}. {message}"
        )

        # Automatically scroll to the newest operation.
        self.history_list.see(tk.END)
