
import tkinter as tk
from tkinter import ttk, messagebox

# Import the actual inventory database and DSA algorithms.
import database
from search_sort import linear_search, binary_search, bubble_sort


class SearchSortView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=20)

        # Retrieve actual component records from SQLite.
        self.records = database.get_all_components()

        self.create_widgets()
        self.display_records(self.records)

    def create_widgets(self):

        # ------------------------------------------------
        # SECTION 1: PAGE HEADING
        # ------------------------------------------------

        ttk.Label(
            self,
            text="Search and Sorting",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        ttk.Label(
            self,
            text="Explore searching and sorting algorithms using laboratory components."
        ).pack(anchor="w", pady=(5, 15))

        # ------------------------------------------------
        # SECTION 2: ALGORITHM SELECTION
        # ------------------------------------------------

        control_frame = ttk.LabelFrame(
            self,
            text="Algorithm Controls",
            padding=12
        )
        control_frame.pack(fill="x", pady=8)

        ttk.Label(
            control_frame,
            text="Select Algorithm:"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.algorithm_var = tk.StringVar(
            value="Linear Search"
        )

        self.algorithm_menu = ttk.Combobox(
            control_frame,
            textvariable=self.algorithm_var,
            values=[
                "Linear Search",
                "Binary Search",
                "Bubble Sort"
            ],
            state="readonly",
            width=20
        )
        self.algorithm_menu.grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(
            control_frame,
            text="Search / Sort Value:"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.keyword_entry = ttk.Entry(
            control_frame,
            width=25
        )
        self.keyword_entry.grid(
            row=0, column=3, padx=5, pady=5
        )

        ttk.Label(
            control_frame,
            text="Sort By:"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.sort_var = tk.StringVar(value="name")

        self.sort_menu = ttk.Combobox(
            control_frame,
            textvariable=self.sort_var,
            values=[
                "name",
                "component_id",
                "quantity"
            ],
            state="readonly",
            width=20
        )
        self.sort_menu.grid(
            row=1, column=1, padx=5, pady=5
        )

        self.order_var = tk.StringVar(value="Ascending")

        ttk.Combobox(
            control_frame,
            textvariable=self.order_var,
            values=["Ascending", "Descending"],
            state="readonly",
            width=20
        ).grid(row=1, column=3, padx=5, pady=5)

        # Buttons execute the selected algorithm.
        ttk.Button(
            control_frame,
            text="Execute Algorithm",
            command=self.execute_algorithm
        ).grid(row=2, column=1, padx=5, pady=10)

        ttk.Button(
            control_frame,
            text="Refresh Inventory",
            command=self.refresh_inventory
        ).grid(row=2, column=2, padx=5, pady=10)

        # ------------------------------------------------
        # SECTION 3: ALGORITHM INFORMATION
        # ------------------------------------------------

        info_frame = ttk.LabelFrame(
            self,
            text="Algorithm Explanation",
            padding=12
        )
        info_frame.pack(fill="x", pady=8)

        self.explanation_label = ttk.Label(
            info_frame,
            text="Select an algorithm and execute it to see its explanation.",
            wraplength=850,
            justify="left"
        )
        self.explanation_label.pack(anchor="w")

        # ------------------------------------------------
        # SECTION 4: RESULTS TABLE
        # ------------------------------------------------

        result_frame = ttk.LabelFrame(
            self,
            text="Component Results",
            padding=10
        )
        result_frame.pack(
            fill="both",
            expand=True,
            pady=8
        )

        columns = (
            "component_id",
            "name",
            "category",
            "quantity",
            "location"
        )

        self.result_table = ttk.Treeview(
            result_frame,
            columns=columns,
            show="headings",
            height=10
        )

        # Define the column headings.
        self.result_table.heading(
            "component_id", text="Component ID"
        )
        self.result_table.heading(
            "name", text="Component Name"
        )
        self.result_table.heading(
            "category", text="Category"
        )
        self.result_table.heading(
            "quantity", text="Quantity"
        )
        self.result_table.heading(
            "location", text="Location"
        )

        # Set the column widths.
        self.result_table.column(
            "component_id", width=120
        )
        self.result_table.column(
            "name", width=180
        )
        self.result_table.column(
            "category", width=120
        )
        self.result_table.column(
            "quantity", width=90, anchor="center"
        )
        self.result_table.column(
            "location", width=140
        )

        # Add a vertical scrollbar.
        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.result_table.yview
        )

        self.result_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.result_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(side="right", fill="y")

        # ------------------------------------------------
        # SECTION 5: RESULT STATUS
        # ------------------------------------------------

        self.status_label = ttk.Label(
            self,
            text="Ready.",
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(anchor="w", pady=5)

    def execute_algorithm(self):

        # Retrieve the current algorithm selection.
        algorithm = self.algorithm_var.get()

        keyword = self.keyword_entry.get().strip()

        # Reload records to use the latest inventory data.
        self.records = database.get_all_components()

        # Prevent searching an empty inventory.
        if not self.records:
            messagebox.showinfo(
                "Empty Inventory",
                "There are no components to process."
            )
            self.display_records([])
            return

        # ------------------------------------------------
        # LINEAR SEARCH
        # ------------------------------------------------

        if algorithm == "Linear Search":

            if not keyword:
                messagebox.showwarning(
                    "Missing Search Value",
                    "Enter a component ID or name."
                )
                return

            results = linear_search(
                self.records,
                keyword
            )

            self.display_records(results)

            self.explanation_label.config(
                text=(
                    "LINEAR SEARCH\n"
                    "The algorithm examines each component one by one "
                    "and checks whether the search value appears in its "
                    "Component ID or Name.\n\n"
                    "Time Complexity: O(n)\n"
                    f"Matching records found: {len(results)}"
                )
            )

            self.status_label.config(
                text=f"Linear Search completed: {len(results)} result(s)."
            )

        # ------------------------------------------------
        # BINARY SEARCH
        # ------------------------------------------------

        elif algorithm == "Binary Search":

            if not keyword:
                messagebox.showwarning(
                    "Missing Component ID",
                    "Enter an exact Component ID."
                )
                return

            result = binary_search(
                self.records,
                keyword
            )

            if result:
                results = [result]
            else:
                results = []

            self.display_records(results)

            self.explanation_label.config(
                text=(
                    "BINARY SEARCH\n"
                    "The algorithm first sorts the records by Component ID, "
                    "then repeatedly divides the search interval in half "
                    "until the target is found or the interval is empty.\n\n"
                    "Search Complexity: O(log n) after sorting.\n"
                    "Note: This implementation uses Bubble Sort first, "
                    "so the complete operation is O(n²) in the worst case."
                )
            )

            self.status_label.config(
                text=(
                    "Binary Search: Component found."
                    if result
                    else "Binary Search: Component not found."
                )
            )

        # ------------------------------------------------
        # BUBBLE SORT
        # ------------------------------------------------

        elif algorithm == "Bubble Sort":

            sort_key = self.sort_var.get()

            descending = (
                self.order_var.get() == "Descending"
            )

            results = bubble_sort(
                self.records,
                key=sort_key,
                reverse=descending
            )

            self.display_records(results)

            self.explanation_label.config(
                text=(
                    "BUBBLE SORT\n"
                    "The algorithm repeatedly compares adjacent records "
                    "and swaps them when they are in the wrong order.\n\n"
                    f"Sorting Field: {sort_key}\n"
                    f"Order: {self.order_var.get()}\n"
                    "Average and Worst-Case Time Complexity: O(n²).\n"
                    "Best Case with early stopping: O(n)."
                )
            )

            self.status_label.config(
                text=f"Bubble Sort completed: {len(results)} record(s)."
            )

    def display_records(self, records):

        # Clear previous results before displaying new records.
        for row in self.result_table.get_children():
            self.result_table.delete(row)

        # Insert each record into the results table.
        for component in records:
            self.result_table.insert(
                "",
                tk.END,
                values=(
                    component["component_id"],
                    component["name"],
                    component["category"],
                    component["quantity"],
                    component["location"]
                )
            )

    def refresh_inventory(self):

        # Retrieve the latest records from the database.
        self.records = database.get_all_components()

        # Display all current inventory records.
        self.display_records(self.records)

        self.explanation_label.config(
            text="Inventory refreshed from the SQLite database."
        )

        self.status_label.config(
            text=f"Total components: {len(self.records)}"
        )
