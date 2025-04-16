# Lausanne Budget Calculator

A simple tool to calculate and visualize the cost of living in Lausanne, Switzerland for students or professionals planning to move there. This application helps users estimate their 24-month budget based on housing choices and other living expenses.

- **Housing Selection**: Browse and select from real Lausanne housing options
- **Expense Patterns**: Visualize how expenses distribute over 24 months
- **Interactive Budget**: Toggle expenses on/off to customize your budget
- **Multi-Person Support**: Calculate costs when sharing with others (1-4 people)
- **First Month Calculation**: Special calculation for first month including deposit and setup costs
- **Visual Charts**: See your monthly expenses on a 24-month timeline

## Installation

1. Clone this repository:
```
git clone https://github.com/your-username/lausanne-budget.git
cd lausanne-budget
```

2. Make sure you have the required Python packages:
```
pip install pandas matplotlib
```

## Usage

Run the main application:
```
python main.py
```


## How It Works

The calculator uses actual housing data from Lausanne and combines it with expense patterns to give you a comprehensive 24-month view of your budget. Key expenses include:

- Rent and housing deposit (2x monthly rent)
- Utilities (water, electricity, internet)
- Food and groceries
- Transportation
- Tuition and registration fees
- Health insurance
- Social activities and trips

The first month calculation includes the security deposit (typically 3 months' rent) and initial setup costs.

## Keep enlarging the database
You can add more living locations in `scripts/housing.py` inside the housing DB: `housing_dict`

You can customize the expense patterns in `scripts/housing.py` by modifying the `get_monthly_expense_patterns()` function. This allows you to:

- Change expense amounts
- Adjust expense timing (e.g., when tuition is due)
- Add new expense categories

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.