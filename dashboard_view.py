
import tkinter as tk
from tkinter import ttk, messagebox
from zipfile import Path
import database
from pathlib import Path

class DashboardView(ttk.Frame):
    """
    LabU Dashboard.

    Displays live inventory statistics, low-stock alerts,
    and recent inventory transactions.
    """

    # Components with quantity at or below this value
    # will appear in the low-stock section.
    LOW_STOCK_THRESHOLD = 5

    def __init__(self, parent):
        super().__init__(parent, padding=25)

        self.configure(style="Main.TFrame")

        self.create_widgets()
        self.refresh_dashboard()

    def create_widgets(self):
        # Load the AUF ASCII seal from the text file.
        banner_path = Path(__file__).resolve().parent / "auf_seal_ascii.txt"

        with open(banner_path, "r", encoding="utf-8") as file:
            banner = file.read()

        # Display the ASCII seal.
        self.banner_label = tk.Label(
            self,
            text=banner,
            font=("Consolas", 2),
            bg="#14213D",
            fg="#FFFFFF",
            justify="center",
            padx=10,
            pady=10
        )
        self.banner_label.pack(fill="x", pady=(0, 20))
 

        # Dashboard heading and refresh button.
        heading_frame = ttk.Frame(self)
        heading_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            heading_frame,
            text="Dashboard Overview",
            style="Title.TLabel"
        ).pack(side="left")

        ttk.Button(
            heading_frame,
            text="Refresh Dashboard",
            command=self.refresh_dashboard
        ).pack(side="right")

        # Statistics cards.
        self.stats_frame = ttk.Frame(self)
        self.stats_frame.pack(fill="x", pady=(0, 20))

        self.stat_labels = {}

        statistics = [
            ("components", "Registered Components"),
            ("units", "Total Units in Stock"),
            ("categories", "Component Categories"),
            ("transactions", "Total Transactions")
        ]

        for key, title in statistics:
            card = ttk.LabelFrame(
                self.stats_frame,
                text=title,
                padding=15
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            value_label = ttk.Label(
                card,
                text="0",
                font=("Segoe UI", 22, "bold")
            )
            value_label.pack()

            self.stat_labels[key] = value_label

        # Lower dashboard sections.
        lower_frame = ttk.Frame(self)
        lower_frame.pack(fill="both", expand=True)

        # Low-stock section.
        stock_frame = ttk.LabelFrame(
            lower_frame,
            text=f"Low-Stock Alerts (Quantity <= {self.LOW_STOCK_THRESHOLD})",
            padding=10
        )
        stock_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        self.stock_tree = ttk.Treeview(
            stock_frame,
            columns=("id", "name", "quantity"),
            show="headings",
            height=8
        )

        self.stock_tree.heading("id", text="Component ID")
        self.stock_tree.heading("name", text="Component Name")
        self.stock_tree.heading("quantity", text="Quantity")

        self.stock_tree.column("id", width=110, anchor="center")
        self.stock_tree.column("name", width=150, anchor="w")
        self.stock_tree.column("quantity", width=80, anchor="center")

        self.stock_tree.pack(fill="both", expand=True)

        # Recent transactions section.
        recent_frame = ttk.LabelFrame(
            lower_frame,
            text="Recent Activities",
            padding=10
        )
        recent_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        self.recent_tree = ttk.Treeview(
            recent_frame,
            columns=("component", "action", "timestamp"),
            show="headings",
            height=8
        )

        self.recent_tree.heading("component", text="Component")
        self.recent_tree.heading("action", text="Action")
        self.recent_tree.heading("timestamp", text="Date and Time")

        self.recent_tree.column("component", width=140, anchor="w")
        self.recent_tree.column("action", width=80, anchor="center")
        self.recent_tree.column("timestamp", width=140, anchor="center")

        self.recent_tree.pack(fill="both", expand=True)

        # Dashboard status message.
        self.status_label = ttk.Label(
            self,
            text="Dashboard ready."
        )
        self.status_label.pack(anchor="w", pady=(12, 0))

    def refresh_dashboard(self):
        """Retrieve database records and update dashboard sections."""

        try:
            components = database.get_all_components()
            transactions = database.get_all_transactions()

            # Calculate inventory statistics.
            total_components = len(components)

            total_units = sum(
                component["quantity"] for component in components
            )

            total_categories = len({
                component["category"] for component in components
            })

            total_transactions = len(transactions)

            # Update statistics cards.
            self.stat_labels["components"].config(
                text=str(total_components)
            )

            self.stat_labels["units"].config(
                text=str(total_units)
            )

            self.stat_labels["categories"].config(
                text=str(total_categories)
            )

            self.stat_labels["transactions"].config(
                text=str(total_transactions)
            )

            # Update low-stock table.
            for item in self.stock_tree.get_children():
                self.stock_tree.delete(item)

            low_stock_items = [
                component for component in components
                if component["quantity"] <= self.LOW_STOCK_THRESHOLD
            ]

            for component in low_stock_items:
                self.stock_tree.insert(
                    "",
                    "end",
                    values=(
                        component["component_id"],
                        component["name"],
                        component["quantity"]
                    )
                )

            # Update recent transaction table.
            for item in self.recent_tree.get_children():
                self.recent_tree.delete(item)

            # Show the five newest activities.
            for transaction in transactions[:5]:
                self.recent_tree.insert(
                    "",
                    "end",
                    values=(
                        transaction["component_name"],
                        transaction["action"],
                        transaction["timestamp"]
                    )
                )

            self.status_label.config(
                text=(
                    f"Dashboard updated successfully. "
                    f"{total_components} components and "
                    f"{total_transactions} transactions loaded."
                )
            )

        except Exception as error:
            messagebox.showerror(
                "Dashboard Error",
                f"Unable to load dashboard data:\n{error}"
            )

            self.status_label.config(
                text="Dashboard could not be updated."
            )
