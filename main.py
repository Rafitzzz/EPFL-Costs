
# main.py
import os
from scripts.housing import housing_df
from scripts.simple_dashboard import run_dashboard

def main():
    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Print info about available housing options
    print(f"Loaded {len(housing_df)} housing options")
    print(f"Price range: {housing_df['Price (CHF/month)'].min():,.0f} - {housing_df['Price (CHF/month)'].max():,.0f} CHF/month")
    
    # Launch simplified dashboard
    print("Starting Lausanne Budget Calculator...")
    run_dashboard()

if __name__ == "__main__":
    main()