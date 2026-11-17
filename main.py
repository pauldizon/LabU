
from logging import root
import tkinter as tk
from tkinter import ttk
from inventory_view import InventoryView
from stack_view import StackView
from queue_view import QueueView
# Import the Search and Sorting interface.
from search_sort_view import SearchSortView
from transaction_view import TransactionView
from dashboard_view import DashboardView
import database


class LabUApplication:

    def __init__(self, root):
        self.root = root

        self.root.title("LabU | Component Laboratory")
        self.root.geometry("1200x750")
        self.root.minsize(950, 600)

        self.setup_style()
        self.create_layout()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Sidebar.TFrame",
            background="#14213D"
        )

        style.configure(
            "Main.TFrame",
            background="#F4F6FA"
        )

        style.configure(
            "Title.TLabel",
            background="#F4F6FA",
            foreground="#14213D",
            font=("Segoe UI", 22, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background="#F4F6FA",
            foreground="#64748B",
            font=("Segoe UI", 10)
        )

        style.configure(
            "SidebarTitle.TLabel",
            background="#14213D",
            foreground="white",
            font=("Segoe UI", 20, "bold")
        )

        style.configure(
            "Nav.TButton",
            background="#14213D",
            foreground="white",
            font=("Segoe UI", 11),
            padding=12,
            borderwidth=0
        )

        style.map(
            "Nav.TButton",
            background=[("active", "#23395D")]
        )

    def create_layout(self):
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ttk.Frame(
            self.container,
            style="Sidebar.TFrame",
            width=230
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ttk.Label(
            self.sidebar,
            text="LabU",
            style="SidebarTitle.TLabel"
        ).pack(anchor="w", padx=25, pady=(30, 5))

        navigation = [
            "Dashboard",
            "Component Inventory",
            "Stack Visualizer",
            "Queue Visualizer",
            "Search and Sorting",
            "Transaction History"
        ]

        for item in navigation:
            ttk.Button(
                self.sidebar,
                text=item,
                style="Nav.TButton",
                command=lambda name=item: self.show_page(name)
            ).pack(fill="x", padx=12, pady=4)

        # Main content
        self.content = ttk.Frame(
            self.container,
            style="Main.TFrame"
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_page("Dashboard")

    def show_page(self, page_name):

        
        # Clear the previous page
        for widget in self.content.winfo_children():
            widget.destroy()

        # Open Component Inventory
        if page_name == "Component Inventory":
            inventory_page = InventoryView(self.content)
            inventory_page.pack(fill="both", expand=True)
            return
        
        if page_name == "Stack Visualizer":
            stack_page = StackView(self.content)
            stack_page.pack(fill="both", expand=True)
            return
        
        if page_name == "Queue Visualizer":
            queue_page = QueueView(self.content)
            queue_page.pack(fill="both", expand=True)
            return
        
        # Load the Search and Sorting interface.
        if page_name == "Search and Sorting":
            search_sort_page = SearchSortView(self.content)
            search_sort_page.pack(fill="both", expand=True)
            return
        
        # Load the Transaction History interface.
        if page_name == "Transaction History":
            transaction_page = TransactionView(self.content)
            transaction_page.pack(fill="both", expand=True)
            return
        
        # Load the live Dashboard interface.
        if page_name == "Dashboard":
            dashboard_page = DashboardView(self.content)
            dashboard_page.pack(fill="both", expand=True)
            return

        # Display heading for other pages
        ttk.Label(
            self.content,
            text=page_name,
            style="Title.TLabel"
            ).pack(anchor="w", padx=35, pady=(35, 5))

        ttk.Label(
        self.content,
            text="Welcome to the LabU Component Laboratory.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", padx=35)


    
if __name__ == "__main__":

    print("Starting LabU...")
    database.initialize_database()

    root = tk.Tk()
    root.title("LabU | Component Laboratory")
    root.geometry("1200x750")

    root.lift()
    root.attributes("-topmost", True)
    root.after(500, lambda: root.attributes("-topmost", False))

    app = LabUApplication(root)

    print("LabU successfully initialized!")

    root.mainloop()

    print("LabU closed.")


