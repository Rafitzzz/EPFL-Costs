# scripts/dashboard.py
import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

from scripts.housing import housing_dict, housing_df
from scripts.financial_summary import BudgetCalculator

class SimpleBudgetDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Lausanne Housing Budget Dashboard")
        self.root.geometry("1000x600")
        
        # Initialize calculator
        self.calculator = BudgetCalculator()
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Create the UI
        self.create_ui()
        
        # Load the first housing option by default
        self.update_dashboard(0)
    
    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Housing options
        left_frame = ttk.LabelFrame(main_frame, text="Housing Options", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create treeview for housing options
        columns = ("Location", "Price (CHF/month)", "Size (m²)")
        self.housing_tree = ttk.Treeview(left_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            self.housing_tree.heading(col, text=col)
            self.housing_tree.column(col, width=120)
        
        # Add housing data
        for i, row in housing_df.iterrows():
            values = (row["Location"].split(",")[0], row["Price (CHF/month)"], row["Size (m²)"])
            self.housing_tree.insert("", tk.END, iid=i, values=values)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.housing_tree.yview)
        self.housing_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.housing_tree.pack(fill=tk.BOTH, expand=True)
        
        # Handle selection
        self.housing_tree.bind("<<TreeviewSelect>>", self.on_housing_select)
        
        # Right panel - Budget details
        right_frame = ttk.LabelFrame(main_frame, text="Budget Details", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Housing details section
        self.housing_details = ttk.LabelFrame(right_frame, text="Selected Housing", padding=10)
        self.housing_details.pack(fill=tk.X, padx=5, pady=5)
        
        self.location_label = ttk.Label(self.housing_details, text="Location: ")
        self.location_label.pack(anchor="w")
        
        self.price_label = ttk.Label(self.housing_details, text="Price: ")
        self.price_label.pack(anchor="w")
        
        self.size_label = ttk.Label(self.housing_details, text="Size: ")
        self.size_label.pack(anchor="w")
        
        # Budget summary section
        self.budget_summary = ttk.LabelFrame(right_frame, text="Budget Summary", padding=10)
        self.budget_summary.pack(fill=tk.X, padx=5, pady=5)
        
        self.monthly_label = ttk.Label(self.budget_summary, text="Monthly Total: ")
        self.monthly_label.pack(anchor="w")
        
        self.first_month_label = ttk.Label(self.budget_summary, text="First Month Total: ")
        self.first_month_label.pack(anchor="w")
        
        # Chart frame
        self.chart_frame = ttk.LabelFrame(right_frame, text="Budget Visualization", padding=10)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ##444444444444444444444444444444444444444444444444 New addition for txt
        # Report frame for displaying the text report
        self.report_frame = ttk.LabelFrame(right_frame, text="Budget Report", padding=10)
        self.report_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Text widget with scrollbar
        self.report_text = tk.Text(self.report_frame, wrap=tk.WORD, height=10)
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        report_scrollbar = ttk.Scrollbar(self.report_frame, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=report_scrollbar.set)
        report_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Actions frame
        actions_frame = ttk.Frame(right_frame, padding=10)
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        generate_report_btn = ttk.Button(actions_frame, text="Generate Report", command=self.generate_report)
        generate_report_btn.pack(side=tk.LEFT, padx=5)

    
    def on_housing_select(self, event):
        selected_id = self.housing_tree.selection()[0]
        self.update_dashboard(int(selected_id))
    
    def update_dashboard(self, housing_index):
        # Calculate budget
        monthly = self.calculator.calculate_monthly_budget(housing_index)
        first_month = self.calculator.calculate_first_month_expenses(housing_index)
        housing = monthly["selected_housing"]
        
        # Update housing details
        self.location_label.config(text=f"Location: {housing['Location']}")
        self.price_label.config(text=f"Price: {housing['Price (CHF/month)']} CHF/month")
        self.size_label.config(text=f"Size: {housing['Size (m²)']} m² ({housing['Price (CHF/month)'] / housing['Size (m²)']:.2f} CHF/m²)")
        
        # Update budget summary
        self.monthly_label.config(text=f"Monthly Total: {monthly['total_chf']:.2f} CHF ({monthly['total_mxn']:.2f} MXN)")
        self.first_month_label.config(text=f"First Month Total: {first_month['total_chf']:.2f} CHF ({first_month['total_mxn']:.2f} MXN)")
        
        # Update chart
        self.update_chart(monthly["expenses"])

        # Generate and display report
        report = self.calculator.generate_summary_report(housing_index)
        
        # Clear previous text and insert new report
        self.report_text.delete('1.0', tk.END)
        self.report_text.insert('1.0', report)
        self.root.geometry("1200x1200")  # Make window bigger
    
    def update_chart(self, expenses):
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(5, 4))
        
        # Create pie chart
        ax.pie(
            expenses.values(),
            labels=expenses.keys(),
            autopct='%1.1f%%',
            startangle=90
        )
        ax.set_title('Monthly Budget Distribution')
        ax.axis('equal')
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def generate_report(self):
        selected_id = self.housing_tree.selection()[0]
        # In __init__ method:
        report = self.calculator.generate_summary_report(int(selected_id))
        print("Report generated and saved to output/budget_report.txt")

def run_dashboard():
    root = tk.Tk()
    app = SimpleBudgetDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    # In __init__ method:
    run_dashboard()