# PrepaymentShekelCalc

A calculator for evaluating early loan repayment decisions.

## Setup

1. Ensure Python 3.6+ is installed on your system
2. Download all files, maintaining the folder structure
3. Run the application:
   ```
   python loan_calculator.py
   ```

## How to Use

1. Select your preferred language (English or Hebrew) from the dropdown menu
2. Enter your loan details in the input fields
3. Click the "Calculate" button
4. Review the results and recommendation

## Input Fields

| Field | Description |
|-------|-------------|
| Original Loan | The initial amount borrowed |
| Remaining Balance | Current unpaid balance of the loan |
| Months Left | Number of remaining monthly payments |
| Nominal Annual Interest | The stated interest rate on the loan (%) |
| Adjusted Annual Interest | The effective interest rate after accounting for compounding (%) |
| Market Nominal Interest | Current market interest rate for new loans (%) |
| Market Adjusted Interest | Current effective market rate after compounding (%) |

The calculator uses this expanded formula that explicitly shows the interest component:

```
Savings = (Monthly Payment × Months Left) - Remaining Balance - Admin Fee - Discount Fee

Where:
Monthly Payment = Remaining Balance × (Monthly Interest Rate / (1 - (1 + Monthly Interest Rate)^(-Months Left)))
Total Future Interest = (Monthly Payment × Months Left) - Remaining Balance
Discount Fee = max(0, Present Value at Market Rate - Present Value at Loan Rate)
```

This formula shows that:
1. The total future payments include both principal (Remaining Balance) and interest
2. By paying early, you avoid all future interest payments
3. This may be offset by any discount fee charged for early repayment

Admin Fee is a fixed ₪60.

## What the Results Mean

After calculating, you'll see:

- **Monthly Payment**: What you pay each month
- **Total Future Payments**: Total of all remaining payments
- **Remaining Interest**: How much interest is in your future payments (this is what you avoid by paying early)
- **Total Prepayment Cost**: Your loan balance plus the ₪60 fee
- **Discount Fee**: Any penalty for early repayment
- **Final Prepayment Cost**: The total amount to pay off your loan now

**Bottom Line**: If the savings number is positive, you'll save money by paying early. If it's negative, you're better off keeping your current payment schedule.
