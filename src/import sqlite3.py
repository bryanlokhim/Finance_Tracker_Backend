import sqlite3
from datetime import datetime
import csv
import os

class FinanceTracker:
    def __init__(self, db_name='transactions.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Initialize the database table if it doesn't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions 
                            (id INTEGER PRIMARY KEY, amount REAL, category TEXT, date TEXT)''')
        self.conn.commit()

    def add_transaction(self, amount, category):
        """Add a new transaction to the database with validation."""
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            if not category.strip():
                raise ValueError("Category cannot be empty.")
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO transactions (amount, category, date) VALUES (?, ?, ?)", 
                               (amount, category.strip(), date))
            self.conn.commit()
            print(f"Added: £{amount:.2f} to {category}")
        except ValueError as e:
            print(f"Error: {e}")

    def view_summary(self):
        """Display a summary of spending by category."""
        self.cursor.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
        data = self.cursor.fetchall()
        
        if not data:
            print("No transactions yet.")
        else:
            print("\nSpending Summary:")
            for category, total in data:
                print(f"{category}: £{total:.2f}")

    def export_to_csv(self, filename='spending_summary.csv'):
        """Export summary data to a CSV file."""
        self.cursor.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
        data = self.cursor.fetchall()
        
        if not data:
            print("No data to export.")
            return
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Category', 'Total Amount'])
            for category, total in data:
                writer.writerow([category, f"{total:.2f}"])
        print(f"Exported summary to {filename}")

    def close(self):
        """Close the database connection."""
        self.conn.close()

def main():
    tracker = FinanceTracker()
    
    while True:
        print("\n1. Add Transaction")
        print("2. View Summary")
        print("3. Export to CSV")
        print("4. Exit")
        choice = input("Enter choice (1-4): ")

        if choice == '1':
            amount = input("Enter amount (£): ")
            category = input("Enter category (e.g., food, rent): ")
            tracker.add_transaction(amount, category)
        
        elif choice == '2':
            tracker.view_summary()
        
        elif choice == '3':
            tracker.export_to_csv()
        
        elif choice == '4':
            tracker.close()
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()