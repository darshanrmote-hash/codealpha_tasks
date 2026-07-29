import os
import csv

# Hardcoded dictionary defining base stock prices
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "MSFT": 420.00,
    "AMZN": 185.00,
    "GOOGL": 175.00,
    "NVDA": 125.00,
    "META": 480.00
}

# The user's portfolio holding (maps symbol -> quantity)
portfolio = {}

def clear_screen():
    """Clears the terminal screen for a cleaner interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_positive_float(prompt):
    """Helper to prompt and validate a positive floating-point number."""
    while True:
        try:
            val = float(input(prompt).strip())
            if val <= 0:
                print("  [!] Please enter a number greater than 0.")
            else:
                return val
        except ValueError:
            print("  [!] Invalid input. Please enter a valid number.")

def get_positive_int(prompt):
    """Helper to prompt and validate a positive integer."""
    while True:
        try:
            val = int(input(prompt).strip())
            if val <= 0:
                print("  [!] Please enter an integer greater than 0.")
            else:
                return val
        except ValueError:
            print("  [!] Invalid input. Please enter a valid integer.")

def display_available_stocks():
    """Displays the base stocks and their predefined prices."""
    print("  Available stocks and predefined prices:")
    for sym, val in sorted(STOCK_PRICES.items()):
        print(f"    - {sym:<6}: ${val:.2f}")

def view_portfolio():
    """Calculates and displays the portfolio value and stock breakdown."""
    clear_screen()
    print("=" * 60)
    print("                    PORTFOLIO STATUS                    ")
    print("=" * 60)
    
    if not portfolio:
        print("\n  Your portfolio is currently empty.")
        print("  Go back to the main menu and add some stocks!\n")
        print("=" * 60)
        return

    # Table Header
    print(f"  {'TICKER':<10} | {'SHARES':<10} | {'CURRENT PRICE':<15} | {'TOTAL VALUE':<15}")
    print("  " + "-" * 56)
    
    total_portfolio_value = 0.0
    
    for ticker, shares in sorted(portfolio.items()):
        price = STOCK_PRICES[ticker]
        total_stock_value = shares * price
        total_portfolio_value += total_stock_value
        print(f"  {ticker:<10} | {shares:<10} | ${price:<14.2f} | ${total_stock_value:<14.2f}")
        
    print("  " + "-" * 56)
    print(f"  {'TOTAL PORTFOLIO VALUE:':<38} | ${total_portfolio_value:<14.2f}")
    print("=" * 60)

def add_stock():
    """Prompts user to add a stock or increase shares of existing stock."""
    clear_screen()
    print("=" * 50)
    print("                   ADD STOCK                    ")
    print("=" * 50)
    display_available_stocks()
    print("-" * 50)
    
    ticker = input("  Enter stock ticker symbol (e.g., AAPL): ").strip().upper()
    if not ticker:
        print("  [!] Stock ticker cannot be empty.")
        return
        
    # Check if we have the price in our database. If not, allow user to add it.
    if ticker not in STOCK_PRICES:
        print(f"  [i] '{ticker}' is not in the predefined price list.")
        add_custom = input(f"  Would you like to define a custom price for {ticker}? (y/n): ").strip().lower()
        if add_custom in ('y', 'yes'):
            price = get_positive_float(f"  Enter price per share for {ticker}: $")
            STOCK_PRICES[ticker] = price
            print(f"  [+] Added {ticker} to price list at ${price:.2f}.")
        else:
            print("  [!] Action cancelled. Stock was not added.")
            return

    shares = get_positive_int(f"  Enter quantity of shares for {ticker}: ")
    
    # Update portfolio
    if ticker in portfolio:
        portfolio[ticker] += shares
    else:
        portfolio[ticker] = shares
        
    print(f"\n  [+] Successfully added {shares} shares of {ticker} to your portfolio.")

def remove_stock():
    """Prompts user to remove shares or a whole stock from the portfolio."""
    clear_screen()
    print("=" * 50)
    print("                 REMOVE STOCK                   ")
    print("=" * 50)
    
    if not portfolio:
        print("\n  Your portfolio is empty. Nothing to remove.\n")
        print("=" * 50)
        return
        
    ticker = input("  Enter stock ticker to remove/reduce: ").strip().upper()
    
    if ticker not in portfolio:
        print(f"  [!] '{ticker}' is not in your portfolio.")
        return
        
    current_shares = portfolio[ticker]
    print(f"  You currently own {current_shares} shares of {ticker}.")
    
    remove_all = input(f"  Remove ALL shares of {ticker}? (y/n): ").strip().lower()
    
    if remove_all in ('y', 'yes'):
        del portfolio[ticker]
        print(f"\n  [-] Removed {ticker} completely from your portfolio.")
    else:
        shares_to_remove = get_positive_int(f"  Enter number of shares to remove (max {current_shares}): ")
        if shares_to_remove >= current_shares:
            del portfolio[ticker]
            print(f"\n  [-] Removed {ticker} completely from your portfolio.")
        else:
            portfolio[ticker] -= shares_to_remove
            print(f"\n  [-] Reduced {ticker} by {shares_to_remove} shares. Remaining: {portfolio[ticker]} shares.")

def save_to_file():
    """Saves the current portfolio status to a file (CSV and TXT options)."""
    clear_screen()
    print("=" * 50)
    print("                 SAVE PORTFOLIO                 ")
    print("=" * 50)
    
    if not portfolio:
        print("\n  Your portfolio is empty. Nothing to save.\n")
        print("=" * 50)
        return
        
    print("  Choose format:")
    print("  1. Save as CSV file (portfolio.csv)")
    print("  2. Save as text report (portfolio_report.txt)")
    choice = input("\n  Enter option (1-2): ").strip()
    
    if choice == "1":
        filename = "portfolio.csv"
        try:
            with open(filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Ticker", "Shares", "Price Per Share", "Total Value"])
                total_val = 0.0
                for ticker, shares in sorted(portfolio.items()):
                    price = STOCK_PRICES[ticker]
                    total_stock_value = shares * price
                    total_val += total_stock_value
                    writer.writerow([ticker, shares, f"{price:.2f}", f"{total_stock_value:.2f}"])
                writer.writerow(["TOTAL", "", "", f"{total_val:.2f}"])
            print(f"\n  [+] Portfolio successfully saved to '{filename}'.")
        except Exception as e:
            print(f"  [!] Error writing file: {e}")
            
    elif choice == "2":
        filename = "portfolio_report.txt"
        try:
            with open(filename, mode='w') as f:
                f.write("=" * 60 + "\n")
                f.write("                 STOCK PORTFOLIO REPORT                 \n")
                f.write("=" * 60 + "\n\n")
                f.write(f"{'TICKER':<10} | {'SHARES':<10} | {'PRICE/SHARE':<15} | {'TOTAL VALUE':<15}\n")
                f.write("-" * 58 + "\n")
                total_val = 0.0
                for ticker, shares in sorted(portfolio.items()):
                    price = STOCK_PRICES[ticker]
                    total_stock_value = shares * price
                    total_val += total_stock_value
                    f.write(f"{ticker:<10} | {shares:<10} | ${price:<14.2f} | ${total_stock_value:<14.2f}\n")
                f.write("-" * 58 + "\n")
                f.write(f"{'TOTAL PORTFOLIO VALUE:':<36} | ${total_val:<14.2f}\n")
                f.write("=" * 60 + "\n")
            print(f"\n  [+] Portfolio successfully saved to '{filename}'.")
        except Exception as e:
            print(f"  [!] Error writing file: {e}")
    else:
        print("  [!] Invalid choice. Returning to main menu.")

def main():
    """Main dashboard interface."""
    while True:
        clear_screen()
        print("=" * 50)
        print("           CODEALPHA STOCK TRACKER              ")
        print("=" * 50)
        print("  1. View Portfolio Dashboard")
        print("  2. Add Stock Shares")
        print("  3. Remove/Reduce Stock Shares")
        print("  4. Save Portfolio to File")
        print("  5. Exit")
        print("=" * 50)
        
        choice = input("  Select an option (1-5): ").strip()
        
        if choice == "1":
            view_portfolio()
            input("  Press Enter to return to main menu...")
        elif choice == "2":
            add_stock()
            input("\n  Press Enter to return to main menu...")
        elif choice == "3":
            remove_stock()
            input("\n  Press Enter to return to main menu...")
        elif choice == "4":
            save_to_file()
            input("\n  Press Enter to return to main menu...")
        elif choice == "5":
            clear_screen()
            print("\n  Thank you for using CodeAlpha Stock Tracker! Goodbye.\n")
            break
        else:
            print("  [!] Invalid option. Please enter a number between 1 and 5.")
            input("  Press Enter to continue...")

if __name__ == "__main__":
    main()
