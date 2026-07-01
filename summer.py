import tkinter as tk
from tkinter import ttk, messagebox

class SummerSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Summer Flow & Token Bank")
        self.root.geometry("600x550")
        
        # --- Core Variables (The Economy) ---
        self.checking_balance = tk.DoubleVar(value=0.00)
        self.savings_balance = tk.DoubleVar(value=0.00)
        self.daily_earnings = tk.DoubleVar(value=0.00)
        
        # --- Setup Tabs ---
        self.notebook = ttk.Notebook(root)
        
        self.tab_schedule = ttk.Frame(self.notebook)
        self.tab_bank = ttk.Frame(self.notebook)
        self.tab_store = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_schedule, text="🗓️ Daily Schedule")
        self.notebook.add(self.tab_bank, text="🏦 Banking")
        self.notebook.add(self.tab_store, text="🛍️ Reward Store")
        
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Build the interfaces
        self.build_schedule_tab()
        self.build_bank_tab()
        self.build_store_tab()

    # --- TAB 1: DAILY SCHEDULE ---
    def build_schedule_tab(self):
        # Editable text area for the day's flexible schedule
        ttk.Label(self.tab_schedule, text="Today's Flexible Blocks:", font=("Arial", 12, "bold")).pack(pady=5)
        self.schedule_text = tk.Text(self.tab_schedule, height=8, width=65)
        self.schedule_text.pack(pady=5)
        
        # Pre-fill the cozy rhythm
        default_schedule = (
            "🌅 9AM-10AM: Coffee & Journaling\n"
            "🧠 Block 1 (11AM-2PM): Review+1 Python / German / Piano\n"
            "🚶‍♀️ Block 2 (2PM-5PM): Exercise / Errands\n"
            "☕ Block 3 (5PM-9PM): Unwind, Games, Reading (Free time!)\n"
            "🌌 10PM+: Meds, Call Wesley, Sleep"
        )
        self.schedule_text.insert(tk.END, default_schedule)
        
        # Daily Earning Checkboxes
        ttk.Label(self.tab_schedule, text="Daily Earnings Checklist:", font=("Arial", 12, "bold")).pack(pady=10)
        
        self.check_vars = []
        tasks = [
            ("Morning Anchor ($1.00)", 1.00),
            ("Task 1 Started ($0.50)", 0.50),
            ("Task 2 Started ($0.50)", 0.50),
            ("Task 3 Started ($0.50)", 0.50),
            ("Task 4 Started ($0.50)", 0.50),
            ("Clean Sweep Bonus ($1.00)", 1.00),
            ("Evening Anchor ($1.00)", 1.00)
        ]
        
        self.checklist_frame = ttk.Frame(self.tab_schedule)
        self.checklist_frame.pack()
        
        for text, value in tasks:
            var = tk.DoubleVar()
            chk = ttk.Checkbutton(self.checklist_frame, text=text, variable=var, onvalue=value, offvalue=0.0)
            chk.pack(anchor="w", pady=2)
            self.check_vars.append(var)
            
        # Deposit Button
        ttk.Button(self.tab_schedule, text="💰 Deposit Checked Items to Checking", command=self.deposit_earnings).pack(pady=15)

    # --- TAB 2: BANKING ---
    def build_bank_tab(self):
        # Display Balances
        self.lbl_checking = ttk.Label(self.tab_bank, text="$0.00", font=("Arial", 24, "bold"), foreground="green")
        self.lbl_savings = ttk.Label(self.tab_bank, text="$0.00", font=("Arial", 24, "bold"), foreground="blue")
        
        ttk.Label(self.tab_bank, text="Checking Account", font=("Arial", 12)).pack(pady=(20, 0))
        self.lbl_checking.pack()
        
        ttk.Label(self.tab_bank, text="Savings Account (Interest Yielding)", font=("Arial", 12)).pack(pady=(20, 0))
        self.lbl_savings.pack()
        
        # Transfer Section
        transfer_frame = ttk.Frame(self.tab_bank)
        transfer_frame.pack(pady=30)
        
        ttk.Label(transfer_frame, text="Transfer Amount: $").grid(row=0, column=0, padx=5)
        self.transfer_entry = ttk.Entry(transfer_frame, width=10)
        self.transfer_entry.grid(row=0, column=1, padx=5)
        
        ttk.Button(transfer_frame, text="Checking ➔ Savings", command=lambda: self.transfer("to_savings")).grid(row=1, column=0, pady=10)
        ttk.Button(transfer_frame, text="Savings ➔ Checking", command=lambda: self.transfer("to_checking")).grid(row=1, column=1, pady=10)
        
        # End of Day Interest Button
        ttk.Button(self.tab_bank, text="🌙 End Day: Calculate Daily Interest", command=self.calculate_interest).pack(pady=20)

    # --- TAB 3: REWARD STORE ---
    def build_store_tab(self):
        ttk.Label(self.tab_store, text="The Frugal Dopamine Vault", font=("Arial", 14, "bold")).pack(pady=15)
        
        # Store items (Name, Cost)
        store_items = [
            ("Digital Etsy Asset / Planner Guide", 5.00),
            ("The Premium Sip (Drive-thru drink)", 6.00),
            ("The Takeout Pass (Veggie Bowl)", 12.00),
            ("The Next Chapter (New Book)", 15.00),
            ("The Indie Side-Quest (Game)", 20.00),
            ("Mobile Command Center (Behind-seat desk)", 50.00),
            ("Stillwater Date Weekend Fund", 100.00)
        ]
        
        for item, price in store_items:
            btn_text = f"Buy: {item} (${price:.2f})"
            ttk.Button(self.tab_store, text=btn_text, command=lambda p=price, n=item: self.buy_item(n, p)).pack(pady=5, fill="x", padx=40)

    # --- APP LOGIC ---
    def update_displays(self):
        self.lbl_checking.config(text=f"${self.checking_balance.get():.2f}")
        self.lbl_savings.config(text=f"${self.savings_balance.get():.2f}")
        
    def deposit_earnings(self):
        today_total = sum(var.get() for var in self.check_vars)
        if today_total == 0:
            return
            
        self.checking_balance.set(self.checking_balance.get() + today_total)
        self.daily_earnings.set(today_total) # Save for interest calc
        
        # Uncheck boxes after deposit
        for var in self.check_vars:
            var.set(0.0)
            
        self.update_displays()
        messagebox.showinfo("Deposited!", f"${today_total:.2f} deposited to Checking!")

    def transfer(self, direction):
        try:
            amount = float(self.transfer_entry.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")
            return
            
        if direction == "to_savings":
            if amount > self.checking_balance.get():
                messagebox.showerror("Error", "Insufficient funds in Checking.")
                return
            self.checking_balance.set(self.checking_balance.get() - amount)
            self.savings_balance.set(self.savings_balance.get() + amount)
            
        elif direction == "to_checking":
            if amount > self.savings_balance.get():
                messagebox.showerror("Error", "Insufficient funds in Savings.")
                return
            self.savings_balance.set(self.savings_balance.get() - amount)
            self.checking_balance.set(self.checking_balance.get() + amount)
            
        self.transfer_entry.delete(0, tk.END)
        self.update_displays()

    def calculate_interest(self):
        savings = self.savings_balance.get()
        if savings <= 0:
            messagebox.showinfo("Interest", "No funds in Savings to earn interest.")
            return
            
        earnings = self.daily_earnings.get()
        
        # Brackets: Hyper-Focus ($5+), Steady Flow ($3.50+), Recovery (Under $3.50)
        if earnings >= 5.00:
            rate = 0.02  # 2.0%
            level_name = "Hyper-Focus Day (2.0%)"
        elif earnings >= 3.50:
            rate = 0.015 # 1.5%
            level_name = "Steady Flow Day (1.5%)"
        else:
            rate = 0.005 # 0.5%
            level_name = "Recovery Day (0.5%)"
            
        interest_earned = savings * rate
        self.savings_balance.set(savings + interest_earned)
        
        # Reset daily earnings for tomorrow
        self.daily_earnings.set(0.0)
        self.update_displays()
        
        messagebox.showinfo("Interest Payout", f"{level_name}\n\nYou earned ${interest_earned:.2f} in passive interest!")

    def buy_item(self, item_name, price):
        if self.checking_balance.get() >= price:
            self.checking_balance.set(self.checking_balance.get() - price)
            self.update_displays()
            messagebox.showinfo("Purchase Successful!", f"Enjoy your reward: {item_name}!")
        else:
            messagebox.showwarning("Insufficient Funds", "Not enough cash in Checking. Keep building those daily anchors!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SummerSystemApp(root)
    root.mainloop()