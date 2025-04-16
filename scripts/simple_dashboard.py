import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

from scripts.housing import housing_df, get_monthly_expense_patterns

class SimpleBudgetCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Lausanne Budget Calculator")
        self.root.geometry("1200x1000")
        
        # Number of people (default: 2)
        self.persons = 2
        
        # Get expense patterns
        self.expense_patterns = get_monthly_expense_patterns()
        
        # Dictionary to track expense inclusion
        self.expense_included = {expense: True for expense in self.expense_patterns}
        
        # Create the UI
        self.create_ui()
        
        # Select first housing option by default
        self.housing_tree.selection_set("0")
        self.update_budget(0)
    
    def create_ui(self):
        # Main split - housing on left, expense view on right
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Housing options and summary
        left_panel = ttk.Frame(main_frame)
        
        # Housing options section
        housing_frame = ttk.LabelFrame(left_panel, text="Select Housing")
        housing_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create simple housing list
        columns = ("Location", "Price", "Size", "Link")
        self.housing_tree = ttk.Treeview(housing_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.housing_tree.column("Location", width=100)
        self.housing_tree.column("Price", width= 60)
        self.housing_tree.column("Size", width= 30)
        self.housing_tree.column("Link", width=100)
        
        for col in columns:
            self.housing_tree.heading(col, text=col)
        
        # Add housing data
        for i, row in housing_df.iterrows():
            values = (
                row["Location"].split(",")[0], 
                f"{row['Price (CHF/month)']:,.0f} CHF", 
                f"{row['Size (m²)']} m²",
                row["Link"]
            )
            self.housing_tree.insert("", tk.END, iid=str(i), values=values)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(housing_frame, orient=tk.VERTICAL, command=self.housing_tree.yview)
        self.housing_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.housing_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add the double-click binding HERE
        self.housing_tree.bind("<Double-1>", self.open_housing_link)
        
        # Bind selection
        self.housing_tree.bind("<<TreeviewSelect>>", self.on_housing_select)
        
        # Number of people selector
        people_frame = ttk.Frame(left_panel)
        people_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(people_frame, text="Number of people:").pack(side=tk.LEFT, padx=5)
        
        # Spinbox for people selection
        self.people_var = tk.IntVar(value=self.persons)
        people_spinbox = ttk.Spinbox(
            people_frame, 
            from_=1, 
            to=4, 
            width=3, 
            textvariable=self.people_var,
            command=self.update_persons
        )
        people_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Update button
        update_btn = ttk.Button(people_frame, text="Update", command=self.update_persons)
        update_btn.pack(side=tk.LEFT, padx=5)
        
        # Budget summary frame
        summary_frame = ttk.LabelFrame(left_panel, text="Budget Summary")
        summary_frame.pack(fill=tk.X, pady=10)
        
        # Summary labels
        summary_grid = ttk.Frame(summary_frame, padding=10)
        summary_grid.pack(fill=tk.X)
        
        # Monthly summary
        ttk.Label(summary_grid, text="Monthly Rent:", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.rent_label = ttk.Label(summary_grid, text="0 CHF")
        self.rent_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(summary_grid, text="Monthly Total:", font=("TkDefaultFont", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.monthly_label = ttk.Label(summary_grid, text="0 CHF")
        self.monthly_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(summary_grid, text="Per Person:", font=("TkDefaultFont", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.pp_label = ttk.Label(summary_grid, text="0 CHF")
        self.pp_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # 24-month summary
        ttk.Label(summary_grid, text="Total (24 months):", font=("TkDefaultFont", 12, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=10)
        self.total_label = ttk.Label(summary_grid, text="0 CHF", font=("TkDefaultFont", 12, "bold"))
        self.total_label.grid(row=3, column=1, sticky=tk.W, padx=5, pady=10)
        
        ttk.Label(summary_grid, text="Per Person (24 months):", font=("TkDefaultFont", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.total_pp_label = ttk.Label(summary_grid, text="0 CHF")
        self.total_pp_label.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        # First month costs
        first_month_frame = ttk.LabelFrame(left_panel, text="First Month Costs")
        first_month_frame.pack(fill=tk.X, pady=10)
        
        # First month details
        first_month_grid = ttk.Frame(first_month_frame, padding=10)
        first_month_grid.pack(fill=tk.X)
        
        ttk.Label(first_month_grid, text="Monthly expenses:", font=("TkDefaultFont", 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.first_monthly_label = ttk.Label(first_month_grid, text="0 CHF")
        self.first_monthly_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(first_month_grid, text="Security deposit (3x rent):", font=("TkDefaultFont", 10)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.deposit_label = ttk.Label(first_month_grid, text="0 CHF")
        self.deposit_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(first_month_grid, text="Registration:", font=("TkDefaultFont", 10)).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.registration_label = ttk.Label(first_month_grid, text="0 CHF")
        self.registration_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(first_month_grid, text="Initial supplies:", font=("TkDefaultFont", 10)).grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.supplies_label = ttk.Label(first_month_grid, text="1,500 CHF")
        self.supplies_label.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(first_month_grid, text="First month total:", font=("TkDefaultFont", 10, "bold")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.first_total_label = ttk.Label(first_month_grid, text="0 CHF", font=("TkDefaultFont", 10, "bold"))
        self.first_total_label.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Add left panel to main frame
        main_frame.add(left_panel, weight=30)
        
        # Right panel - Expense view
        right_panel = ttk.Frame(main_frame)
        
        # Expense table
        expense_frame = ttk.LabelFrame(right_panel, text="Expense Details")
        expense_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Add a scrollable area for expenses
        expense_canvas = tk.Canvas(expense_frame)
        expense_scrollbar = ttk.Scrollbar(expense_frame, orient=tk.VERTICAL, command=expense_canvas.yview)
        
        # Configure canvas
        expense_canvas.configure(yscrollcommand=expense_scrollbar.set)
        expense_canvas.bind('<Configure>', lambda e: expense_canvas.configure(scrollregion=expense_canvas.bbox("all")))
        
        # Create interior frame for expense items
        self.expense_interior = ttk.Frame(expense_canvas)
        expense_canvas.create_window((0, 0), window=self.expense_interior, anchor="nw")
        
        # Pack everything
        expense_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        expense_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a frame for expense headers
        headers_frame = ttk.Frame(self.expense_interior)
        headers_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create headers
        ttk.Label(headers_frame, text="Expense", width=20, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, padx=5)
        ttk.Label(headers_frame, text="Monthly Cost", width=15, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=1, padx=5)
        ttk.Label(headers_frame, text="24-Month Total", width=15, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, padx=5)
        ttk.Label(headers_frame, text="Include", width=10, font=("TkDefaultFont", 10, "bold")).grid(row=0, column=3, padx=5)
        
        # Expense items will be added dynamically
        self.expense_checkboxes = {}
        
        # Monthly expenses chart
        chart_frame = ttk.LabelFrame(right_panel, text="Monthly Expenses")
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.chart_area = ttk.Frame(chart_frame)
        self.chart_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add right panel to main frame
        main_frame.add(right_panel, weight=70)
    
    def on_housing_select(self, event):
        """Handle housing selection"""
        if self.housing_tree.selection():
            selected_id = self.housing_tree.selection()[0]
            self.update_budget(int(selected_id))
    
    # Add this method to the SimpleBudgetCalculator class
    def open_housing_link(self, event):
        """Open the link for the selected housing option"""
        if self.housing_tree.selection():
            selected_id = self.housing_tree.selection()[0]
            selected_item = self.housing_tree.item(selected_id)
            link = selected_item["values"][3]  # Link is the 4th value
            import webbrowser
            webbrowser.open(link)

    def update_persons(self):
        """Update number of persons"""
        self.persons = self.people_var.get()
        if self.housing_tree.selection():
            selected_id = int(self.housing_tree.selection()[0])
            self.update_budget(selected_id)
    
    def update_budget(self, housing_index):
        """Update budget with selected housing"""
        # Get housing data
        housing = housing_df.iloc[housing_index]
        rent = housing["Price (CHF/month)"]
        
        # Update rent in expense patterns
        self.expense_patterns["rent"]["monthly_values"] = [rent] * 24
        self.expense_patterns["rent"]["total_chf"] = rent * 24
        
        # Update housing deposit (only in first month)
        deposit = rent * 2
        self.expense_patterns["housing_deposit"]["monthly_values"] = [deposit] + [0] * 23
        self.expense_patterns["housing_deposit"]["total_chf"] = deposit
        
        # Calculate monthly totals and update the UI
        self.update_monthly_totals()
        
        # Update expense details
        self.update_expense_details()
        
        # Update chart
        self.update_expense_chart()
    
    def update_monthly_totals(self):
        """Calculate and update monthly expense totals"""
        # Get housing data
        if not self.housing_tree.selection():
            return
            
        selected_id = int(self.housing_tree.selection()[0])
        housing = housing_df.iloc[selected_id]
        rent = housing["Price (CHF/month)"]
        
        # Calculate monthly total (first month)
        first_month_total = 0
        for expense, details in self.expense_patterns.items():
            if self.expense_included.get(expense, True):  # Only include selected expenses
                # Get the first month value
                if details["monthly_values"]:
                    first_month_total += details["monthly_values"][0]
        
        # Calculate average monthly total (excluding first month special costs)
        monthly_values = []
        for month in range(1, 24):  # Skip first month
            month_total = 0
            for expense, details in self.expense_patterns.items():
                if self.expense_included.get(expense, True) and len(details["monthly_values"]) > month:
                    month_total += details["monthly_values"][month]
            monthly_values.append(month_total)
        
        # Average monthly expense (excluding first month)
        avg_monthly = sum(monthly_values) / len(monthly_values) if monthly_values else 0
        
        # Calculate per-person values
        avg_monthly_pp = avg_monthly / self.persons
        
        # Calculate 24-month total
        total_24m = 0
        for expense, details in self.expense_patterns.items():
            if self.expense_included.get(expense, True):
                total_24m += sum(details["monthly_values"])
        
        total_24m_pp = total_24m / self.persons
        
        # First month special costs
        registration = self.expense_patterns["registration_fee"]["monthly_values"][0] * self.persons
        supplies = self.expense_patterns["supplies"]["monthly_values"][0]
        deposit = self.expense_patterns["housing_deposit"]["monthly_values"][0]
        
        # Update summary labels
        self.rent_label.config(text=f"{rent:,.0f} CHF")
        self.monthly_label.config(text=f"{avg_monthly:,.0f} CHF")
        self.pp_label.config(text=f"{avg_monthly_pp:,.0f} CHF")
        
        self.total_label.config(text=f"{total_24m:,.0f} CHF")
        self.total_pp_label.config(text=f"{total_24m_pp:,.0f} CHF")
        
        # Update first month labels
        self.first_monthly_label.config(text=f"{first_month_total:,.0f} CHF")
        self.deposit_label.config(text=f"{deposit:,.0f} CHF")
        self.registration_label.config(text=f"{registration:,.0f} CHF")
        self.supplies_label.config(text=f"{supplies:,.0f} CHF")
        
        # First month total
        first_month_with_extras = first_month_total + deposit + supplies
        self.first_total_label.config(text=f"{first_month_with_extras:,.0f} CHF")
    
    def update_expense_details(self):
        """Update the expense details display"""
        # Clear existing expense widgets
        for widget in self.expense_interior.winfo_children()[1:]:  # Skip the header row
            widget.destroy()
        
        # Clear existing checkboxes
        self.expense_checkboxes = {}
        
        # Create expense rows
        row = 1  # Start after the header row
        for expense, details in self.expense_patterns.items():
            # Monthly value (either average or first month)
            monthly_value = sum(details["monthly_values"]) / 24 if expense not in ["housing_deposit", "supplies"] else details["monthly_values"][0] / 24
            
            # Scale person-specific expenses
            if expense in ["groceries", "transportation", "mobile", "social", "health_insurance"]:
                monthly_value = monthly_value * self.persons
            
            # Total value across 24 months
            total_value = sum(details["monthly_values"])
            
            # Create a frame for this expense row
            expense_row = ttk.Frame(self.expense_interior)
            expense_row.pack(fill=tk.X, padx=10, pady=2)
            
            # Expense name (nicely formatted)
            display_name = expense.replace("_", " ").title()
            ttk.Label(expense_row, text=display_name, width=20).grid(row=0, column=0, padx=5)
            
            # Monthly cost
            ttk.Label(expense_row, text=f"{monthly_value:,.0f} CHF", width=15).grid(row=0, column=1, padx=5)
            
            # 24-month total
            ttk.Label(expense_row, text=f"{total_value:,.0f} CHF", width=15).grid(row=0, column=2, padx=5)
            
            # Include checkbox
            var = tk.BooleanVar(value=self.expense_included.get(expense, True))
            checkbox = ttk.Checkbutton(expense_row, variable=var, command=self.on_expense_toggle)
            checkbox.grid(row=0, column=3, padx=5)
            
            # Store reference to the checkbox
            self.expense_checkboxes[expense] = var
            
            row += 1
    
    def on_expense_toggle(self):
        """Handle toggling expense inclusion"""
        # Update expense inclusion status
        for expense, var in self.expense_checkboxes.items():
            self.expense_included[expense] = var.get()
        
        # Update totals and chart
        self.update_monthly_totals()
        self.update_expense_chart()
    
    def update_expense_chart(self):
        """Update the monthly expense chart"""
        # Clear previous chart
        for widget in self.chart_area.winfo_children():
            widget.destroy()
        
        # Create figure
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)
        
        # Calculate monthly totals for all 24 months
        monthly_totals = [0] * 24
        for expense, details in self.expense_patterns.items():
            if self.expense_included.get(expense, True):  # Only include selected expenses
                for month in range(24):
                    if month < len(details["monthly_values"]):
                        # Apply person scaling for relevant expenses
                        value = details["monthly_values"][month]
                        if expense in ["groceries", "transportation", "mobile", "social", "health_insurance"]:
                            value *= self.persons
                        monthly_totals[month] += value
        
        # Plot the line chart of monthly totals
        ax.plot(range(1, 25), monthly_totals, marker='o', linewidth=2, 
                color='blue', label='Total Monthly Expenses')
        
        # Add rent reference line
        if self.expense_included.get("rent", True):
            rent = self.expense_patterns["rent"]["monthly_values"][0]
            ax.axhline(y=rent, color='r', linestyle='--', alpha=0.7, 
                      label=f'Rent: {rent:,.0f} CHF')
        
        # Calculate and show average
        avg = sum(monthly_totals[1:]) / 23  # Exclude first month as it has special costs
        ax.axhline(y=avg, color='g', linestyle=':', alpha=0.7, 
                  label=f'Average: {avg:,.0f} CHF')
        
        # Labels and formatting
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount (CHF)')
        ax.set_title(f'Monthly Expenses for {self.persons} People')
        ax.set_xticks(range(1, 25, 2))  # Show every other month for clarity
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add legend
        ax.legend()
        
        # Format y-axis with commas
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x):,}"))
        
        fig.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def run_dashboard():
    root = tk.Tk()
    app = SimpleBudgetCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    run_dashboard()