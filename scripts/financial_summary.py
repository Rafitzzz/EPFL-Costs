# scripts/financial_summary.py
import pandas as pd
import matplotlib.pyplot as plt
from scripts.housing import housing_dict, housing_df

class BudgetCalculator:
    """Simple budget calculator for Lausanne housing"""
    
    def __init__(self, exchange_rate=24.44):
        self.exchange_rate = exchange_rate
        
        # Monthly expenses from PDF (in CHF)
        self.monthly_expenses = {
            "housing": 3000,
            "maintenance": 400,
            "water": 200,
            "electricity": 80,
            "wifi": 70,
            "groceries": 1000,
            "transportation": 150 * 2,  # for two people
            "mobile": 100 * 2,  # for two people
            "social": 200 * 2,  # for two people
            "trips": 300 * 2,  # for two people
            "health_insurance": 600 * 2  # for two people
        }
        
        # One-time settlement expenses
        self.settlement_expenses = {
            "housing_deposit": 9000,  # 3 months rent
            "supplies": 3000
        }
        
        # College expenses
        self.college_expenses = {
            "tuition_per_semester": 1460,
            "registration_fee_per_semester": 138
        }
        
        # Housing options (from housing_df)
        self.housing_options = housing_df
    
    def calculate_monthly_budget(self, housing_index=0, include_utilities=False):
        """Calculate monthly budget with selected housing option"""
        # Get selected housing
        selected_housing = self.housing_options.iloc[housing_index]
        housing_price = selected_housing["Price (CHF/month)"]
        
        # Copy base expenses and update housing
        expenses = {}
        
        # Always include housing
        expenses["housing"] = housing_price
        
        # Add utilities only if requested
        if include_utilities:
            expenses["maintenance"] = self.monthly_expenses["maintenance"]
            expenses["water"] = self.monthly_expenses["water"]
            expenses["electricity"] = self.monthly_expenses["electricity"]
            expenses["wifi"] = self.monthly_expenses["wifi"]
        
        # Always include these other expenses
        expenses["groceries"] = self.monthly_expenses["groceries"]
        expenses["transportation"] = self.monthly_expenses["transportation"]
        expenses["mobile"] = self.monthly_expenses["mobile"]
        expenses["social"] = self.monthly_expenses["social"]
        expenses["trips"] = self.monthly_expenses["trips"]
        expenses["health_insurance"] = self.monthly_expenses["health_insurance"]
        
        # Calculate total
        total_chf = sum(expenses.values())
        total_mxn = total_chf * self.exchange_rate
        
        return {
            "expenses": expenses,
            "total_chf": total_chf,
            "total_mxn": total_mxn,
            "selected_housing": selected_housing
        }
    
    def calculate_first_month_expenses(self, housing_index=0, include_utilities=False):
        """Calculate first month expenses including settlement costs"""
        monthly = self.calculate_monthly_budget(housing_index, include_utilities)
        
        # Add settlement expenses
        first_month = {
            "monthly": monthly["expenses"],
            "settlement": self.settlement_expenses,
            "college": {
                "tuition": self.college_expenses["tuition_per_semester"],
                "registration_fee": self.college_expenses["registration_fee_per_semester"]
            }
        }
        
        # Calculate totals
        total_chf = sum(monthly["expenses"].values()) + sum(self.settlement_expenses.values()) + sum(first_month["college"].values())
        total_mxn = total_chf * self.exchange_rate
        
        return {
            "expenses": first_month,
            "total_chf": total_chf,
            "total_mxn": total_mxn,
            "selected_housing": monthly["selected_housing"]
        }
    
    def visualize_monthly_budget(self, housing_index=0, include_utilities=False):
        """Create a simple visualization of the monthly budget"""
        # Set the non-interactive backend to avoid GUI issues
        import matplotlib
        matplotlib.use('Agg')  # Use the Agg backend (non-interactive)
        
        budget = self.calculate_monthly_budget(housing_index, include_utilities)
        expenses = budget["expenses"]
        
        # Create pie chart
        plt.figure(figsize=(10, 6))
        plt.pie(
            list(expenses.values()),
            labels=list(expenses.keys()),
            autopct='%1.1f%%',
            startangle=90
        )
        plt.title(f'Monthly Budget Distribution - {budget["total_chf"]:,.2f} CHF')
        plt.axis('equal')
        
        # Save the chart
        output_path = "output/monthly_budget.png"
        plt.savefig(output_path)
        plt.close()
        
        return output_path
    
    def generate_summary_report(self, housing_index=0, include_utilities=False):
        """Generate a text summary report for the selected housing option"""
        monthly = self.calculate_monthly_budget(housing_index, include_utilities)
        first_month = self.calculate_first_month_expenses(housing_index, include_utilities)
        housing = monthly["selected_housing"]
        
        report = f"""
        LAUSANNE BUDGET SUMMARY
        ==============================================
        
        SELECTED HOUSING:
        Location: {housing['Location']}
        Price: {housing['Price (CHF/month)']} CHF/month
        Size: {housing['Size (m²)']} m²
        Price per m²: {housing['Price (CHF/month)'] / housing['Size (m²)']:,.2f} CHF
        
        MONTHLY EXPENSES (CHF):
        {'-' * 45}
        """
        
        for category, amount in monthly["expenses"].items():
            report += f"{category.title()}: {amount:.2f} CHF\n"
        
        report += f"{'-' * 45}\n"
        report += f"Total Monthly: {monthly['total_chf']:,.2f} CHF ({monthly['total_mxn']:,.2f} MXN)\n\n"
        
        report += f"""
        FIRST MONTH EXPENSES (including settlement):
        {'-' * 45}
        Monthly expenses: {sum(monthly['expenses'].values()):,.2f} CHF
        Settlement costs: {sum(first_month['expenses']['settlement'].values()):,.2f} CHF
        College fees: {sum(first_month['expenses']['college'].values()):,.2f} CHF
        {'-' * 45}
        Total First Month: {first_month['total_chf']:,.2f} CHF ({first_month['total_mxn']:,.2f} MXN)
        """
        
        # Write report to file
        with open("output/budget_report.txt", "w") as f:
            f.write(report)
        
        return report

# Example usage
if __name__ == "__main__":
    calculator = BudgetCalculator()
    
    # Calculate budget with first housing option
    monthly = calculator.calculate_monthly_budget(0)
    print(f"Monthly budget: {monthly['total_chf']:,.2f} CHF")
    
    # Generate visualization
    chart_path = calculator.visualize_monthly_budget(0)
    print(f"Chart saved to: {chart_path}")
    
    # Generate report
    report = calculator.generate_summary_report(0)
    print("\nReport generated!")