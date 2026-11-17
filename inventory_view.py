
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

import database


class InventoryView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.selected_id = None

        self.setup_styles()
        self.create_widgets()
        self.load_inventory()

    def setup_styles(self):
        style = ttk.Style()

        style.configure(
            "Inventory.Treeview",
            rowheight=32,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Inventory.Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )

    def create_widgets(self):

        # Main heading
        heading = ttk.Label(
            self,
            text="Component Inventory",
            font=("Segoe UI", 22, "bold"),
            foreground="#14213D"
        )
        heading.pack(anchor="w", padx=25, pady=(20, 5))

        ttk.Label(
            self,
            text="Manage and monitor your electronic laboratory components.",
            foreground="#64748B"
        ).pack(anchor="w", padx=25, pady=(0, 20))

        # Form container
        form = ttk.LabelFrame(
            self,
            text="Component Details",
            padding=15
        )
        form.pack(fill="x", padx=25, pady=5)

        self.component_id = tk.StringVar()
        self.name = tk.StringVar()
        self.category = tk.StringVar()
        self.quantity = tk.StringVar()
        self.location = tk.StringVar()

        fields = [
            ("Component ID", self.component_id),
            ("Component Name", self.name),
            ("Category", self.category),
            ("Quantity", self.quantity),
            ("Storage Location", self.location)
        ]

        self.entries = {}

        for index, (label, variable) in enumerate(fields):

            row = index // 2
            column = (index % 2) * 2

            ttk.Label(
                form,
                text=label
            ).grid(
                row=row,
                column=column,
                sticky="w",
                padx=8,
                pady=7
            )

            entry = ttk.Entry(
                form,
                textvariable=variable,
                width=30
            )

            entry.grid(
                row=row,
                column=column + 1,
                sticky="ew",
                padx=8,
                pady=7
            )

            self.entries[label] = entry

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        # Action buttons
        actions = ttk.Frame(self)
        actions.pack(fill="x", padx=25, pady=12)

        ttk.Button(
            actions,
            text="Add Component",
            command=self.add_component
        ).pack(side="left", padx=4)

        ttk.Button(
            actions,
            text="Update Selected",
            command=self.update_component
        ).pack(side="left", padx=4)

        ttk.Button(
            actions,
            text="Delete Selected",
            command=self.delete_component
        ).pack(side="left", padx=4)

        ttk.Button(
            actions,
            text="Clear Form",
            command=self.clear_form
        ).pack(side="left", padx=4)

        # Search section
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=25, pady=8)

        ttk.Label(
            search_frame,
            text="Search:"
        ).pack(side="left", padx=(0, 8))

        self.search_text = tk.StringVar()

        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_text,
            width=35
        )
        search_entry.pack(side="left", padx=5)

        search_entry.bind(
            "<Return>",
            lambda event: self.search_inventory()
        )

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_inventory
        ).pack(side="left", padx=4)

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.load_inventory
        ).pack(side="left", padx=4)

        # Inventory table
        table_frame = ttk.Frame(self)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=12
        )

        columns = (
            "id",
            "name",
            "category",
            "quantity",
            "location"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Inventory.Treeview"
        )

        headings = {
            "id": "Component ID",
            "name": "Component Name",
            "category": "Category",
            "quantity": "Quantity",
            "location": "Location"
        }

        widths = {
            "id": 110,
            "name": 180,
            "category": 130,
            "quantity": 90,
            "location": 150
        }

        for column in columns:
            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_component
        )

        # Status bar
        self.status = ttk.Label(
            self,
            text="Ready",
            foreground="#64748B"
        )

        self.status.pack(anchor="w", padx=25, pady=8)

    def validate_form(self):

        component_id = self.component_id.get().strip()
        name = self.name.get().strip()
        category = self.category.get().strip()
        location = self.location.get().strip()

        if not all([component_id, name, category, location]):
            messagebox.showwarning(
                "Missing Information",
                "Please complete all component fields."
            )
            return None

        try:
            quantity = int(self.quantity.get())

            if quantity < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a nonnegative whole number."
            )
            return None

        return (
            component_id,
            name,
            category,
            quantity,
            location
        )

    def add_component(self):

        data = self.validate_form()

        if data is None:
            return

        try:
            database.add_component(*data)
            # Record the successful addition in transaction history.
            database.log_transaction(
                data[0],
                data[1],
                "ADD",
                f"Added {data[3]} unit(s), stored at {data[4]}."
)

            messagebox.showinfo(
                "Success",
                "Component added successfully."
            )

            self.clear_form()
            self.load_inventory()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Duplicate ID",
                "That component ID already exists."
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Unable to add component:\n{error}"
            )

    def load_inventory(self):

        try:
            records = database.get_all_components()

            self.display_records(records)

            self.status.config(
                text=f"Total components: {len(records)}"
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def display_records(self, records):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for record in records:
            self.tree.insert(
                "",
                "end",
                values=(
                    record["component_id"],
                    record["name"],
                    record["category"],
                    record["quantity"],
                    record["location"]
                )
            )

    def select_component(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.selected_id = values[0]

        self.component_id.set(values[0])
        self.name.set(values[1])
        self.category.set(values[2])
        self.quantity.set(values[3])
        self.location.set(values[4])

        # Do not allow changing the primary key during editing
        self.entries["Component ID"].config(state="disabled")

        self.status.config(
            text=f"Selected component: {self.selected_id}"
        )

    def update_component(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection",
                "Select a component from the table first."
            )
            return

        data = self.validate_form()

        if data is None:
            return

        try:
            updated = database.update_component(
                self.selected_id,
                data[1],
                data[2],
                data[3],
                data[4]
            )

            if updated:
                # Record the successful component update.
                database.log_transaction(
                    self.selected_id,
                    data[1],
                    "UPDATE",
                    f"Updated category to {data[2]}, quantity to {data[3]}, "
                    f"and location to {data[4]}."
                )

                messagebox.showinfo(
                    "Success",
                    "Component updated successfully."
                )

            self.clear_form()
            self.load_inventory()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def delete_component(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "No Selection",
                "Select a component first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Delete component {self.selected_id}?"
        )

        if not confirm:
            return

        try:
            deleted = database.delete_component(
                self.selected_id
            )

            if deleted:
            # Record the deletion before clearing the selected component.
                database.log_transaction(
                    self.selected_id,
                    self.name.get(),
                    "DELETE",
                    "Component removed from inventory."
            )
                messagebox.showinfo(
                    "Deleted",
                    "Component removed successfully."
                )
            else:
                messagebox.showwarning(
                    "Not Found",
                    "The selected component no longer exists."
                )

            self.clear_form()
            self.load_inventory()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def search_inventory(self):

        keyword = self.search_text.get().strip()

        if not keyword:
            self.load_inventory()
            return

        try:
            records = database.search_components(keyword)

            self.display_records(records)

            self.status.config(
                text=f"Search results: {len(records)}"
            )

            if not records:
                self.status.config(
                    text="No matching components found."
                )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def clear_form(self):

        self.selected_id = None

        self.component_id.set("")
        self.name.set("")
        self.category.set("")
        self.quantity.set("")
        self.location.set("")

        self.entries["Component ID"].config(state="normal")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.status.config(text="Ready")
