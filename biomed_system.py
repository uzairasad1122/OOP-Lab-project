"""
+==============================================================+
|              UMed MANAGEMENT SYSTEM                          |
|     Biomedical Equipment Sales, Service & Marketing          |
+==============================================================+

A Python OOP project for managing biomedical equipment inventory,
sales transactions, and stock management.

Author : Biomedical Engineering Student (OOP Lab Project)
Domain : Biomedical Equipment Sales, Service & Marketing
"""

import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# --------------------------------------------------------------
# CLASS: Equipment
# Represents a single biomedical equipment item in inventory.
# Demonstrates: Classes, Objects, Constructors, Encapsulation
# --------------------------------------------------------------
class Equipment:
    """Represents a biomedical equipment item."""

    def __init__(self, equipment_id, name, category, price, quantity):
        self.__equipment_id = equipment_id
        self.__name = name
        self.__category = category
        self.__price = price
        self.__quantity = quantity

    def get_id(self):
        return self.__equipment_id

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    def set_price(self, price):
        if price > 0:
            self.__price = price

    def set_quantity(self, quantity):
        if quantity >= 0:
            self.__quantity = quantity

    def add_stock(self, amount):
        if amount > 0:
            self.__quantity += amount
            return True
        return False

    def reduce_stock(self, amount):
        if amount <= 0 or amount > self.__quantity:
            return False
        self.__quantity -= amount
        return True


# --------------------------------------------------------------
# CLASS: SaleRecord
# Represents a single sales transaction.
# --------------------------------------------------------------
class SaleRecord:
    """Represents a single sales transaction."""

    def __init__(self, sale_id, equipment_name, quantity_sold, unit_price):
        self.__sale_id = sale_id
        self.__equipment_name = equipment_name
        self.__quantity_sold = quantity_sold
        self.__unit_price = unit_price
        self.__total_amount = quantity_sold * unit_price

    def get_sale_id(self):
        return self.__sale_id

    def get_equipment_name(self):
        return self.__equipment_name

    def get_quantity_sold(self):
        return self.__quantity_sold

    def get_unit_price(self):
        return self.__unit_price

    def get_total_amount(self):
        return self.__total_amount


# --------------------------------------------------------------
# CLASS: BiomedSystem
# Core business logic — inventory & sales management.
# --------------------------------------------------------------
class BiomedSystem:
    """Core management logic for UMed."""

    COMPANY_NAME = "UMed"

    def __init__(self):
        self.__inventory = []
        self.__sales = []
        self.__next_equip_id = 1
        self.__next_sale_id = 1
        self.__load_sample_data()

    def __load_sample_data(self):
        samples = [
            ("ECG Machine", "Diagnostic", 2500.00, 10),
            ("Ventilator", "Life Support", 15000.00, 5),
            ("X-Ray Machine", "Imaging", 45000.00, 3),
            ("Patient Monitor", "Monitoring", 3500.00, 12),
            ("Defibrillator", "Emergency", 4200.00, 8),
            ("Ultrasound Scanner", "Imaging", 30000.00, 4),
            ("Infusion Pump", "Therapeutic", 1800.00, 15),
            ("Pulse Oximeter", "Monitoring", 350.00, 25),
        ]
        for name, cat, price, qty in samples:
            self.__inventory.append(Equipment(self.__next_equip_id, name, cat, price, qty))
            self.__next_equip_id += 1

    def find_equipment_by_id(self, equip_id):
        for item in self.__inventory:
            if item.get_id() == equip_id:
                return item
        return None

    def get_inventory(self):
        return list(self.__inventory)

    def get_sales(self):
        return list(self.__sales)

    def add_equipment(self, name, category, price, quantity):
        eq = Equipment(self.__next_equip_id, name, category, price, quantity)
        self.__inventory.append(eq)
        eid = self.__next_equip_id
        self.__next_equip_id += 1
        return eid

    def sell_equipment(self, equip_id, quantity):
        equipment = self.find_equipment_by_id(equip_id)
        if equipment is None:
            return None, "Equipment not found."
        if quantity <= 0:
            return None, "Quantity must be positive."
        if not equipment.reduce_stock(quantity):
            return None, "Insufficient stock. Available: {}".format(equipment.get_quantity())
        sale = SaleRecord(self.__next_sale_id, equipment.get_name(), quantity, equipment.get_price())
        self.__sales.append(sale)
        sid = self.__next_sale_id
        self.__next_sale_id += 1
        return sale, "Sale #{} completed!".format(sid)

    def add_stock(self, equip_id, amount):
        equipment = self.find_equipment_by_id(equip_id)
        if equipment is None:
            return False, "Equipment not found."
        if equipment.add_stock(amount):
            return True, "Added {} units to '{}'. New stock: {}".format(amount, equipment.get_name(), equipment.get_quantity())
        return False, "Amount must be positive."

    def search_equipment(self, keyword):
        kw = keyword.lower()
        return [i for i in self.__inventory if kw in i.get_name().lower() or kw in i.get_category().lower()]

    def get_revenue_summary(self):
        total_rev = sum(s.get_total_amount() for s in self.__sales)
        total_units = sum(s.get_quantity_sold() for s in self.__sales)
        return len(self.__sales), total_units, total_rev


# ================================================================
# GUI APPLICATION
# ================================================================

# --- Color Palette ---
BG = "#0f1923"
SIDEBAR_BG = "#162a3a"
CARD_BG = "#1a3247"
ACCENT = "#00d4aa"
ACCENT_HOVER = "#00f0c0"
TEXT = "#e8f0f8"
TEXT_DIM = "#7a9bb5"
DANGER = "#ff6b6b"
WARNING = "#ffc857"
HEADER_BG = "#122535"
ENTRY_BG = "#0d1f2d"
ENTRY_BORDER = "#254a64"


class BiomedApp(tk.Tk):
    """Main GUI application for the UMed system."""

    def __init__(self):
        super().__init__()
        self.system = BiomedSystem()
        self.title("UMed — Equipment Management System")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg=BG)

        # Try to set icon (skip if fails)
        try:
            self.iconbitmap(default="")
        except Exception:
            pass

        self._build_ui()
        self.show_inventory()

    # ---------- UI Construction ----------

    def _build_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo area
        logo_frame = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        logo_frame.pack(fill="x", pady=(25, 30), padx=15)
        tk.Label(logo_frame, text="⚕", font=("Segoe UI", 28), bg=SIDEBAR_BG, fg=ACCENT).pack()
        tk.Label(logo_frame, text="UMed", font=("Segoe UI", 16, "bold"), bg=SIDEBAR_BG, fg=TEXT).pack()
        tk.Label(logo_frame, text="Equipment Management", font=("Segoe UI", 9), bg=SIDEBAR_BG, fg=TEXT_DIM).pack()

        # Separator
        tk.Frame(self.sidebar, bg=ENTRY_BORDER, height=1).pack(fill="x", padx=20, pady=(0, 15))

        # Menu buttons
        menu_items = [
            ("📋  Inventory", self.show_inventory),
            ("➕  Add Equipment", self.show_add_equipment),
            ("📦  Update Stock", self.show_update_stock),
            ("💰  Sell Equipment", self.show_sell_equipment),
            ("📊  Sales History", self.show_sales_history),
            ("🔍  Search", self.show_search),
        ]
        self.menu_buttons = []
        for text, cmd in menu_items:
            btn = tk.Button(
                self.sidebar, text=text, font=("Segoe UI", 11),
                bg=SIDEBAR_BG, fg=TEXT_DIM, bd=0, anchor="w",
                padx=20, pady=10, activebackground=CARD_BG,
                activeforeground=ACCENT, cursor="hand2", command=cmd
            )
            btn.pack(fill="x", padx=8, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=CARD_BG, fg=TEXT))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=SIDEBAR_BG, fg=TEXT_DIM) if b != getattr(self, '_active_btn', None) else None)
            self.menu_buttons.append(btn)

        # Exit button at bottom
        tk.Button(
            self.sidebar, text="⏻  Exit", font=("Segoe UI", 11),
            bg=SIDEBAR_BG, fg=DANGER, bd=0, anchor="w",
            padx=20, pady=10, cursor="hand2",
            activebackground=CARD_BG, activeforeground=DANGER,
            command=self.quit
        ).pack(side="bottom", fill="x", padx=8, pady=(0, 20))

        # Main content area
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)

    def _set_active(self, idx):
        """Highlight the active sidebar button."""
        for i, btn in enumerate(self.menu_buttons):
            if i == idx:
                btn.config(bg=CARD_BG, fg=ACCENT)
                self._active_btn = btn
            else:
                btn.config(bg=SIDEBAR_BG, fg=TEXT_DIM)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _make_header(self, title, subtitle=""):
        hdr = tk.Frame(self.content, bg=HEADER_BG)
        hdr.pack(fill="x", padx=0, pady=0)
        inner = tk.Frame(hdr, bg=HEADER_BG)
        inner.pack(fill="x", padx=30, pady=18)
        tk.Label(inner, text=title, font=("Segoe UI", 20, "bold"), bg=HEADER_BG, fg=TEXT).pack(anchor="w")
        if subtitle:
            tk.Label(inner, text=subtitle, font=("Segoe UI", 10), bg=HEADER_BG, fg=TEXT_DIM).pack(anchor="w", pady=(2, 0))

    def _make_card(self, parent, **kwargs):
        card = tk.Frame(parent, bg=CARD_BG, **kwargs)
        return card

    def _styled_entry(self, parent, **kwargs):
        e = tk.Entry(parent, font=("Segoe UI", 11), bg=ENTRY_BG, fg=TEXT,
                     insertbackground=ACCENT, bd=0, highlightthickness=1,
                     highlightbackground=ENTRY_BORDER, highlightcolor=ACCENT, **kwargs)
        return e

    def _styled_button(self, parent, text, command, color=ACCENT, fg_color=BG):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 11, "bold"),
                        bg=color, fg=fg_color, bd=0, padx=25, pady=8,
                        cursor="hand2", activebackground=ACCENT_HOVER,
                        activeforeground=BG, command=command)
        return btn

    def _build_tree(self, parent, columns, headings, widths):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background=CARD_BG, foreground=TEXT,
                        fieldbackground=CARD_BG, font=("Segoe UI", 10),
                        rowheight=32, borderwidth=0)
        style.configure("Custom.Treeview.Heading", background=HEADER_BG,
                        foreground=ACCENT, font=("Segoe UI", 10, "bold"),
                        borderwidth=0)
        style.map("Custom.Treeview", background=[("selected", ENTRY_BORDER)],
                  foreground=[("selected", ACCENT)])

        tree_frame = tk.Frame(parent, bg=CARD_BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                            style="Custom.Treeview", selectmode="browse")
        for col, hd, w in zip(columns, headings, widths):
            tree.heading(col, text=hd, anchor="w")
            tree.column(col, width=w, anchor="w")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return tree

    # ---------- Pages ----------

    def show_inventory(self):
        self._clear_content()
        self._set_active(0)
        items = self.system.get_inventory()
        self._make_header("Equipment Inventory", "Total items: {}".format(len(items)))

        # Stats row
        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", padx=30, pady=(15, 5))
        total_val = sum(i.get_price() * i.get_quantity() for i in items)
        total_units = sum(i.get_quantity() for i in items)
        cats = len(set(i.get_category() for i in items))
        for label, value, clr in [("Total Value", "PKR {:,.0f}".format(total_val), ACCENT),
                                   ("Total Units", str(total_units), WARNING),
                                   ("Categories", str(cats), "#a78bfa")]:
            card = self._make_card(stats)
            card.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=12)
            tk.Label(card, text=label, font=("Segoe UI", 9), bg=CARD_BG, fg=TEXT_DIM).pack(pady=(10, 0))
            tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), bg=CARD_BG, fg=clr).pack(pady=(0, 10))

        cols = ("id", "name", "category", "price", "stock")
        heads = ("ID", "Equipment Name", "Category", "Price", "Stock")
        widths = (50, 200, 120, 120, 80)
        tree = self._build_tree(self.content, cols, heads, widths)
        for item in items:
            tree.insert("", "end", values=(
                item.get_id(), item.get_name(), item.get_category(),
                "PKR {:,.2f}".format(item.get_price()), item.get_quantity()
            ))

    def show_add_equipment(self):
        self._clear_content()
        self._set_active(1)
        self._make_header("Add New Equipment", "Enter equipment details below")

        card = self._make_card(self.content)
        card.pack(fill="x", padx=30, pady=20)
        fields = {}
        for i, (label, key) in enumerate([("Equipment Name", "name"), ("Category", "category"),
                                           ("Unit Price (PKR)", "price"), ("Initial Stock Qty", "quantity")]):
            tk.Label(card, text=label, font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_DIM).grid(
                row=i, column=0, sticky="w", padx=(25, 15), pady=(15 if i == 0 else 8, 0))
            entry = self._styled_entry(card, width=35)
            entry.grid(row=i, column=1, padx=(0, 25), pady=(15 if i == 0 else 8, 0), ipady=5)
            fields[key] = entry

        def do_add():
            try:
                name = fields["name"].get().strip()
                cat = fields["category"].get().strip()
                price = float(fields["price"].get())
                qty = int(fields["quantity"].get())
                if not name or not cat:
                    messagebox.showwarning("Missing Info", "Name and category are required.")
                    return
                if price <= 0:
                    messagebox.showwarning("Invalid", "Price must be > 0.")
                    return
                if qty < 0:
                    messagebox.showwarning("Invalid", "Quantity cannot be negative.")
                    return
                eid = self.system.add_equipment(name, cat, price, qty)
                messagebox.showinfo("Success", "'{}' added! (ID: {})".format(name, eid))
                for e in fields.values():
                    e.delete(0, "end")
            except ValueError:
                messagebox.showerror("Error", "Enter valid numbers for price and quantity.")

        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(20, 25))
        self._styled_button(btn_frame, "  Add Equipment  ", do_add).pack()

    def show_update_stock(self):
        self._clear_content()
        self._set_active(2)
        self._make_header("Update Stock", "Select equipment and add stock")

        card = self._make_card(self.content)
        card.pack(fill="x", padx=30, pady=20)

        tk.Label(card, text="Equipment ID", font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_DIM).grid(
            row=0, column=0, sticky="w", padx=(25, 15), pady=(20, 0))
        id_entry = self._styled_entry(card, width=20)
        id_entry.grid(row=0, column=1, padx=(0, 25), pady=(20, 0), ipady=5)

        tk.Label(card, text="Quantity to Add", font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_DIM).grid(
            row=1, column=0, sticky="w", padx=(25, 15), pady=(10, 0))
        qty_entry = self._styled_entry(card, width=20)
        qty_entry.grid(row=1, column=1, padx=(0, 25), pady=(10, 0), ipady=5)

        def do_update():
            try:
                eid = int(id_entry.get())
                amt = int(qty_entry.get())
                ok, msg = self.system.add_stock(eid, amt)
                if ok:
                    messagebox.showinfo("Success", msg)
                    id_entry.delete(0, "end")
                    qty_entry.delete(0, "end")
                else:
                    messagebox.showwarning("Error", msg)
            except ValueError:
                messagebox.showerror("Error", "Enter valid numbers.")

        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(20, 25))
        self._styled_button(btn_frame, "  Update Stock  ", do_update).pack()

        # Show inventory below for reference
        tk.Label(self.content, text="Current Inventory (for reference)", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT_DIM).pack(anchor="w", padx=30, pady=(10, 0))
        cols = ("id", "name", "stock")
        tree = self._build_tree(self.content, cols, ("ID", "Name", "Stock"), (60, 250, 100))
        for item in self.system.get_inventory():
            tree.insert("", "end", values=(item.get_id(), item.get_name(), item.get_quantity()))

    def show_sell_equipment(self):
        self._clear_content()
        self._set_active(3)
        self._make_header("Sell Equipment", "Process a sale transaction")

        card = self._make_card(self.content)
        card.pack(fill="x", padx=30, pady=20)

        tk.Label(card, text="Equipment ID", font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_DIM).grid(
            row=0, column=0, sticky="w", padx=(25, 15), pady=(20, 0))
        id_entry = self._styled_entry(card, width=20)
        id_entry.grid(row=0, column=1, padx=(0, 25), pady=(20, 0), ipady=5)

        tk.Label(card, text="Quantity to Sell", font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_DIM).grid(
            row=1, column=0, sticky="w", padx=(25, 15), pady=(10, 0))
        qty_entry = self._styled_entry(card, width=20)
        qty_entry.grid(row=1, column=1, padx=(0, 25), pady=(10, 0), ipady=5)

        def do_sell():
            try:
                eid = int(id_entry.get())
                qty = int(qty_entry.get())
                sale, msg = self.system.sell_equipment(eid, qty)
                if sale:
                    info = "{}\n\nEquipment: {}\nQty Sold: {}\nTotal: PKR {:,.2f}".format(
                        msg, sale.get_equipment_name(), sale.get_quantity_sold(), sale.get_total_amount())
                    messagebox.showinfo("Sale Complete", info)
                    id_entry.delete(0, "end")
                    qty_entry.delete(0, "end")
                    # Refresh the reference table
                    self.show_sell_equipment()
                else:
                    messagebox.showwarning("Error", msg)
            except ValueError:
                messagebox.showerror("Error", "Enter valid numbers.")

        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(20, 25))
        self._styled_button(btn_frame, "  Process Sale  ", do_sell, color=WARNING, fg_color=BG).pack()

        tk.Label(self.content, text="Available Inventory", font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=TEXT_DIM).pack(anchor="w", padx=30, pady=(10, 0))
        cols = ("id", "name", "price", "stock")
        tree = self._build_tree(self.content, cols, ("ID", "Name", "Price", "Stock"), (50, 220, 120, 80))
        for item in self.system.get_inventory():
            tree.insert("", "end", values=(
                item.get_id(), item.get_name(),
                "PKR {:,.2f}".format(item.get_price()), item.get_quantity()
            ))

    def show_sales_history(self):
        self._clear_content()
        self._set_active(4)
        sales = self.system.get_sales()
        count, units, revenue = self.system.get_revenue_summary()
        self._make_header("Sales History", "Total transactions: {}".format(count))

        # Stats row
        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", padx=30, pady=(15, 5))
        for label, value, clr in [("Transactions", str(count), ACCENT),
                                   ("Units Sold", str(units), WARNING),
                                   ("Revenue", "PKR {:,.2f}".format(revenue), "#34d399")]:
            card = self._make_card(stats)
            card.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=12)
            tk.Label(card, text=label, font=("Segoe UI", 9), bg=CARD_BG, fg=TEXT_DIM).pack(pady=(10, 0))
            tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), bg=CARD_BG, fg=clr).pack(pady=(0, 10))

        # Toggle button bar
        toggle_bar = tk.Frame(self.content, bg=BG)
        toggle_bar.pack(fill="x", padx=30, pady=(10, 0))

        # Container that switches between table and graph
        display_frame = tk.Frame(self.content, bg=BG)
        display_frame.pack(fill="both", expand=True)

        def show_table_view():
            for w in display_frame.winfo_children():
                w.destroy()
            btn_table.config(bg=ACCENT, fg=BG)
            btn_graph.config(bg=CARD_BG, fg=TEXT_DIM)
            if sales:
                cols = ("sid", "equip", "qty", "unit", "total")
                heads = ("Sale #", "Equipment", "Qty", "Unit Price", "Total")
                widths = (60, 200, 60, 120, 130)
                tree = self._build_tree(display_frame, cols, heads, widths)
                for s in sales:
                    tree.insert("", "end", values=(
                        s.get_sale_id(), s.get_equipment_name(), s.get_quantity_sold(),
                        "PKR {:,.2f}".format(s.get_unit_price()), "PKR {:,.2f}".format(s.get_total_amount())
                    ))
            else:
                tk.Label(display_frame, text="No sales recorded yet.", font=("Segoe UI", 12),
                         bg=BG, fg=TEXT_DIM).pack(pady=40)

        def show_graph_view():
            for w in display_frame.winfo_children():
                w.destroy()
            btn_graph.config(bg=ACCENT, fg=BG)
            btn_table.config(bg=CARD_BG, fg=TEXT_DIM)
            if not sales:
                tk.Label(display_frame, text="No sales data to graph yet.\nMake some sales first!",
                         font=("Segoe UI", 13), bg=BG, fg=TEXT_DIM, justify="center").pack(pady=50)
                return

            # Aggregate sales data by equipment name
            rev_by_equip = {}
            qty_by_equip = {}
            for s in sales:
                name = s.get_equipment_name()
                rev_by_equip[name] = rev_by_equip.get(name, 0) + s.get_total_amount()
                qty_by_equip[name] = qty_by_equip.get(name, 0) + s.get_quantity_sold()

            names = list(rev_by_equip.keys())
            revenues = [rev_by_equip[n] for n in names]
            quantities = [qty_by_equip[n] for n in names]

            # Create matplotlib figure with dark theme
            fig = Figure(figsize=(8, 4), dpi=100, facecolor=BG)

            # Revenue bar chart
            ax1 = fig.add_subplot(121)
            ax1.set_facecolor(CARD_BG)
            bars1 = ax1.barh(names, revenues, color=ACCENT, edgecolor="none", height=0.5)
            ax1.set_title("Revenue by Equipment", color=TEXT, fontsize=11, fontweight="bold", pad=10)
            ax1.set_xlabel("Revenue (PKR)", color=TEXT_DIM, fontsize=9)
            ax1.tick_params(colors=TEXT_DIM, labelsize=8)
            for spine in ax1.spines.values():
                spine.set_color(ENTRY_BORDER)
            # Add value labels on bars
            for bar, val in zip(bars1, revenues):
                ax1.text(bar.get_width() + max(revenues) * 0.02, bar.get_y() + bar.get_height() / 2,
                         "PKR {:,.0f}".format(val), va="center", color=ACCENT, fontsize=8)

            # Quantity bar chart
            ax2 = fig.add_subplot(122)
            ax2.set_facecolor(CARD_BG)
            bars2 = ax2.barh(names, quantities, color=WARNING, edgecolor="none", height=0.5)
            ax2.set_title("Units Sold by Equipment", color=TEXT, fontsize=11, fontweight="bold", pad=10)
            ax2.set_xlabel("Units Sold", color=TEXT_DIM, fontsize=9)
            ax2.tick_params(colors=TEXT_DIM, labelsize=8)
            for spine in ax2.spines.values():
                spine.set_color(ENTRY_BORDER)
            for bar, val in zip(bars2, quantities):
                ax2.text(bar.get_width() + max(quantities) * 0.05, bar.get_y() + bar.get_height() / 2,
                         str(val), va="center", color=WARNING, fontsize=9)

            fig.tight_layout(pad=2.0)

            # Embed in tkinter
            canvas_widget = FigureCanvasTkAgg(fig, master=display_frame)
            canvas_widget.draw()
            canvas_widget.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(5, 20))

        # Create toggle buttons
        btn_table = tk.Button(toggle_bar, text="📋  Table View", font=("Segoe UI", 10, "bold"),
                              bg=ACCENT, fg=BG, bd=0, padx=18, pady=6, cursor="hand2",
                              activebackground=ACCENT_HOVER, command=show_table_view)
        btn_table.pack(side="left", padx=(0, 6))

        btn_graph = tk.Button(toggle_bar, text="📊  Graph View", font=("Segoe UI", 10, "bold"),
                              bg=CARD_BG, fg=TEXT_DIM, bd=0, padx=18, pady=6, cursor="hand2",
                              activebackground=ACCENT_HOVER, command=show_graph_view)
        btn_graph.pack(side="left")

        # Default to table view
        show_table_view()

    def show_search(self):
        self._clear_content()
        self._set_active(5)
        self._make_header("Search Equipment", "Search by name or category")

        search_bar = tk.Frame(self.content, bg=BG)
        search_bar.pack(fill="x", padx=30, pady=20)
        entry = self._styled_entry(search_bar, width=40)
        entry.pack(side="left", ipady=6, padx=(0, 10))
        entry.focus_set()

        result_frame = tk.Frame(self.content, bg=BG)
        result_frame.pack(fill="both", expand=True)

        def do_search(*_args):
            for w in result_frame.winfo_children():
                w.destroy()
            keyword = entry.get().strip()
            if not keyword:
                return
            results = self.system.search_equipment(keyword)
            tk.Label(result_frame, text="Found {} result(s)".format(len(results)),
                     font=("Segoe UI", 11, "bold"), bg=BG, fg=TEXT_DIM).pack(anchor="w", padx=30, pady=(0, 5))
            if results:
                cols = ("id", "name", "category", "price", "stock")
                heads = ("ID", "Name", "Category", "Price", "Stock")
                widths = (50, 200, 120, 120, 80)
                tree = self._build_tree(result_frame, cols, heads, widths)
                for item in results:
                    tree.insert("", "end", values=(
                        item.get_id(), item.get_name(), item.get_category(),
                        "PKR {:,.2f}".format(item.get_price()), item.get_quantity()
                    ))

        self._styled_button(search_bar, "  Search  ", do_search).pack(side="left")
        entry.bind("<Return>", do_search)


# --------------------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------------------
if __name__ == "__main__":
    app = BiomedApp()
    app.mainloop()
