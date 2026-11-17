
import tkinter as tk
from tkinter import ttk, messagebox
from stack import Stack


class StackView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=25)

        # Initialize a Stack with a maximum capacity of 10 elements.
        self.stack = Stack(capacity=10)

        # Keep track of operations for the activity log.
        self.operation_count = 0

        self.create_widgets()
        self.refresh_stack()

    def create_widgets(self):
        # Main heading and description.
        ttk.Label(
            self,
            text="Stack Visualizer",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        ttk.Label(
            self,
            text="Last In, First Out (LIFO) - The last element added is the first removed."
        ).pack(anchor="w", pady=(5, 15))

        # ------------------------------------------------
        # SECTION 1: STACK OPERATIONS
        # ------------------------------------------------
        operation_frame = ttk.LabelFrame(
            self,
            text="Stack Operations",
            padding=12
        )
        operation_frame.pack(fill="x", pady=8)

        self.item_entry = ttk.Entry(
            operation_frame,
            width=30,
            font=("Segoe UI", 10)
        )
        self.item_entry.pack(side="left", padx=5)

        ttk.Button(
            operation_frame,
            text="Push",
            command=self.push_item
        ).pack(side="left", padx=5)

        ttk.Button(
            operation_frame,
            text="Pop",
            command=self.pop_item
        ).pack(side="left", padx=5)

        ttk.Button(
            operation_frame,
            text="Peek",
            command=self.peek_item
        ).pack(side="left", padx=5)

        # ------------------------------------------------
        # SECTION 2: VISUAL STACK
        # ------------------------------------------------
        visualization_frame = ttk.LabelFrame(
            self,
            text="Stack Visualization",
            padding=12
        )
        visualization_frame.pack(
            fill="both",
            expand=True,
            pady=8
        )

        # Canvas allows us to draw individual stack elements.
        self.stack_canvas = tk.Canvas(
            visualization_frame,
            background="white",
            highlightthickness=1,
            highlightbackground="#CCCCCC",
            height=330
        )
        self.stack_canvas.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ------------------------------------------------
        # SECTION 3: STACK INFORMATION
        # ------------------------------------------------
        self.status_label = ttk.Label(
            self,
            text="Elements: 0 / 10",
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(anchor="w", pady=5)

        # ------------------------------------------------
        # SECTION 4: OPERATION HISTORY
        # ------------------------------------------------
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

        # Initial explanation for the user.
        self.add_history("Stack initialized. Capacity: 10 elements.")

    def push_item(self):
        # PUSH: Insert a new element at the top of the stack.
        item = self.item_entry.get().strip()

        # Prevent empty entries.
        if not item:
            messagebox.showwarning(
                "Missing Input",
                "Please enter an item to push."
            )
            return

        try:
            self.stack.push(item)

            # Clear the input field after a successful push.
            self.item_entry.delete(0, tk.END)

            self.add_history(f"PUSH: Added {item}.")
            self.refresh_stack()

        except OverflowError as error:
            # Handle attempts to exceed the stack capacity.
            self.add_history("PUSH FAILED: Stack overflow.")
            messagebox.showerror("Stack Overflow", str(error))

    def pop_item(self):
        # POP: Remove the most recently added element.
        try:
            removed = self.stack.pop()

            self.add_history(f"POP: Removed {removed}.")
            self.refresh_stack()

        except IndexError as error:
            # Handle attempts to remove from an empty stack.
            self.add_history("POP FAILED: Stack underflow.")
            messagebox.showerror("Stack Underflow", str(error))

    def peek_item(self):
        # PEEK: View the top element without removing it.
        try:
            top = self.stack.peek()

            self.add_history(f"PEEK: Top element is {top}.")

            messagebox.showinfo(
                "Top Element",
                f"Current top element: {top}"
            )

        except IndexError as error:
            self.add_history("PEEK FAILED: Stack is empty.")
            messagebox.showwarning("Empty Stack", str(error))

    def refresh_stack(self):
        # Redraw the visualization after every stack modification.
        self.stack_canvas.delete("all")

        items = self.stack.display()

        canvas_width = self.stack_canvas.winfo_width()
        canvas_height = self.stack_canvas.winfo_height()

        # Use a minimum width before the Canvas is fully displayed.
        if canvas_width < 100:
            canvas_width = 700

        if canvas_height < 100:
            canvas_height = 330

        box_width = min(300, canvas_width - 40)
        box_height = 26
        gap = 5

        center_x = canvas_width / 2

        if not items:
            self.stack_canvas.create_text(
                center_x,
                canvas_height / 2,
                text="STACK IS EMPTY",
                fill="#777777",
                font=("Segoe UI", 14, "bold")
            )

        else:
            # Draw each element from bottom to top.
            for index, item in enumerate(items):
                x1 = center_x - box_width / 2
                x2 = center_x + box_width / 2

                y2 = canvas_height - 20 - index * (box_height + gap)
                y1 = y2 - box_height

                # Highlight the top element in green.
                if index == len(items) - 1:
                    fill_color = "#D9F2E3"
                    outline_color = "#23834B"
                    text_color = "#14532D"
                else:
                    fill_color = "#E5EAF2"
                    outline_color = "#8293AA"
                    text_color = "#24364B"

                self.stack_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=fill_color,
                    outline=outline_color,
                    width=2
                )

                self.stack_canvas.create_text(
                    center_x,
                    (y1 + y2) / 2,
                    text=str(item),
                    fill=text_color,
                    font=("Segoe UI", 10, "bold")
                )

                # Mark the most recently added element as TOP.
                if index == len(items) - 1:
                    self.stack_canvas.create_text(
                        x1 - 35,
                        (y1 + y2) / 2,
                        text="TOP",
                        fill="#23834B",
                        font=("Segoe UI", 9, "bold")
                    )

            # Mark the bottom of the stack.
            bottom_y = canvas_height - 8

            self.stack_canvas.create_text(
                center_x,
                bottom_y,
                text="BOTTOM",
                fill="#555555",
                font=("Segoe UI", 9)
            )

        # Update the element counter.
        self.status_label.config(
            text=f"Elements: {self.stack.size()} / {self.stack.capacity}"
        )

    def add_history(self, message):
        # Record successful and unsuccessful operations.
        self.operation_count += 1

        self.history_list.insert(
            tk.END,
            f"{self.operation_count}. {message}"
        )

        # Automatically show the most recent operation.
        self.history_list.see(tk.END)
