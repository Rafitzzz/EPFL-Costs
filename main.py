# main.py
import os
from scripts.financial_summary import BudgetCalculator
from scripts.dashboard import run_dashboard

def main():
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    print("LAUSANNE HOUSING BUDGET CALCULATOR")
    print("="*40)
    
    # Create calculator
    calculator = BudgetCalculator()
    
    # Generate report for first housing option
    print("\nGenerating budget report for first housing option...")
    report = calculator.generate_summary_report(0)
    print("Report saved to: output/budget_report.txt")
    
    # Generate visualization
    print("\nGenerating budget visualization...")
    chart_path = calculator.visualize_monthly_budget(0)
    print(f"Chart saved to: {chart_path}")
    
    # Run dashboard
    print("\nStarting dashboard...")
    run_dashboard()

if __name__ == "__main__":
    main()