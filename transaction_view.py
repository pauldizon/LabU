
import tkinter as tk
from tkinter import ttk, messagebox
import database


class TransactionView(ttk.Frame):
    """
    Transaction History interface.

    Displays inventory activities recorded in SQLite.
    Supports searching and refreshing transaction records.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(padding=25)

        self.create_widgets()
        self.load_transactions()

    def create_widgets(self):
        # Page heading
        ttk.Label(
            self,
            text="Transaction History",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", pady=(0, 5))

        ttk.Label(
            self,
            text="Review and search recorded inventory activities."
        ).pack(anchor="w", pady=(0, 20))

        # Search controls
        search_frame = ttk.LabelFrame(
            self,
            text="Search Transactions",
            padding=12
        )
        search_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            search_frame,
            text="Search by ID, name, or action:"
        ).pack(side="left", padx=(0, 10))

        self.search_var = tk.StringVar()

        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
        )
        self.search_entry.pack(side="left", padx=5)

        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_transactions
        ).pack(side="left", padx=5)

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.clear_search
        ).pack(side="left", padx=5)

        ttk.Button(
            search_frame,
            text="Refresh",
            command=self.load_transactions
        ).pack(side="left", padx=5)

        # Transaction table
        table_frame = ttk.LabelFrame(
            self,
            text="Recorded Activities",
            padding=10
        )
        table_frame.pack(fill="both", expand=True)

        columns = (
            "transaction_id",
            "component_id",
            "component_name",
            "action",
            "details",
            "timestamp"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # Table headings
        headings = {
            "transaction_id": "Transaction ID",
            "component_id": "Component ID",
            "component_name": "Component Name",
            "action": "Action",
            "details": "Details",
            "timestamp": "Date and Time"
        }

        widths = {
            "transaction_id": 100,
            "component_id": 120,
            "component_name": 150,
            "action": 90,
            "details": 280,
            "timestamp": 160
        }

        for column in columns:
            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                minwidth=80,
                anchor="center"
            )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Status label
        self.status_label = ttk.Label(
            self,
            text="Transactions: 0"
        )
        self.status_label.pack(anchor="w", pady=(10, 0))

    def display_transactions(self, records):
        """Display database records in the transaction table."""

        # Remove previous rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert retrieved records
        for record in records:
            self.tree.insert(
                "",
                "end",
                values=(
                    record["transaction_id"],
                    record["component_id"],
                    record["component_name"],
                    record["action"],
                    record["details"] or "",
                    record["timestamp"]
                )
            )

        self.status_label.config(
            text=f"Transactions: {len(records)}"
        )

    def load_transactions(self):
        """Load all transactions, newest first."""

        try:
            records = database.get_all_transactions()
            self.display_transactions(records)

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Unable to load transactions:\n{error}"
            )

    def search_transactions(self):
        """Search transactions using the entered keyword."""

        keyword = self.search_var.get().strip()

        if not keyword:
            self.load_transactions()
            return

        try:
            records = database.search_transactions(keyword)
            self.display_transactions(records)

        except Exception as error:
            messagebox.showerror(
                "Search Error",
                f"Unable to search transactions:\n{error}"
            )

    def clear_search(self):
        """Clear the search field and display all records."""

        self.search_var.set("")
        self.load_transactions()
