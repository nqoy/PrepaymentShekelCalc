import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
from pathlib import Path
from enums.Field import Field
from enums.Language import Language

class LoanCalculator:
    ADMIN_FEE = 60
    PADDING = 10
    ENTRY_WIDTH = 30
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 600

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Early Loan Repayment Calculator")
        
        # Set window size and center it
        self.center_window()
        
        # Create main frame with padding and center it
        self.main_frame = ttk.Frame(self.root, padding=self.PADDING)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weight to center the frame
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)  # Center the content horizontally
        
        self.setup_variables()
        self.load_languages()
        self.create_ui()
        self.change_language()

    def center_window(self):
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate center position
        x = (screen_width - self.WINDOW_WIDTH) // 2
        y = (screen_height - self.WINDOW_HEIGHT) // 2
        
        # Set window size and position
        self.root.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}')
        self.root.minsize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def setup_variables(self):
        self.lang_var = tk.StringVar(value=Language.ENGLISH.value)
        self.button_text = tk.StringVar()
        self.result_text = tk.StringVar()
        self.result_text_label = tk.StringVar()
        self.explanation_text = tk.StringVar()
        self.label_widgets = []
        self.entries = {}

    def load_languages(self):
        self.translations = {}
        for lang in Language:
            file_path = Path(__file__).parent / 'languages' / f'{lang.value}.json'
            with open(file_path, 'r', encoding='utf-8') as f:
                self.translations[lang.value] = json.load(f)

    def create_ui(self):
        # Create centered container for all elements
        content_frame = ttk.Frame(self.main_frame)
        content_frame.grid(row=0, column=0, columnspan=2, sticky="n")
        
        # Language selector centered at the top
        lang_frame = ttk.Frame(content_frame)
        lang_frame.pack(pady=(0, self.PADDING), fill="x")
        
        lang_label = ttk.Label(lang_frame, text="Language / שפה:")
        lang_label.pack(side=tk.LEFT, padx=(0, self.PADDING))
        
        lang_menu = ttk.Combobox(
            lang_frame, 
            textvariable=self.lang_var,
            values=[lang.value for lang in Language],
            state="readonly",
            width=15
        )
        lang_menu.pack(side=tk.LEFT)
        lang_menu.bind("<<ComboboxSelected>>", lambda _: self.change_language())

        # Input fields frame
        fields_frame = ttk.Frame(content_frame)
        fields_frame.pack(pady=self.PADDING, fill="x")
        
        # Create input fields
        for i, field in enumerate(Field):
            if field not in {Field.CALCULATE, Field.RESULTS, Field.EXPLANATION}:
                field_frame = ttk.Frame(fields_frame)
                field_frame.pack(pady=5, fill="x")
                
                label = ttk.Label(field_frame, text="", width=20, anchor="e")
                label.pack(side=tk.LEFT, padx=(0, self.PADDING))
                self.label_widgets.append((field, label))
                
                entry = ttk.Entry(field_frame, width=self.ENTRY_WIDTH)
                entry.pack(side=tk.LEFT)
                self.entries[field] = entry

        # Calculate button centered
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=self.PADDING, fill="x")
        
        calculate_button = ttk.Button(
            button_frame,
            textvariable=self.button_text,
            command=self.calculate_prepayment,
            width=20
        )
        calculate_button.pack()

        # Results frame
        results_frame = ttk.Frame(content_frame)
        results_frame.pack(pady=self.PADDING, fill="x")
        
        ttk.Label(
            results_frame,
            textvariable=self.result_text_label,
            font=('TkDefaultFont', 10, 'bold')
        ).pack(pady=(0, 5))
        
        ttk.Label(
            results_frame,
            textvariable=self.result_text,
            justify=tk.CENTER
        ).pack(pady=5)
        
        ttk.Label(
            results_frame,
            textvariable=self.explanation_text,
            foreground="blue",
            font=('TkDefaultFont', 10, 'bold')
        ).pack(pady=5)

    def change_language(self):
        current_lang = self.lang_var.get()
        translations = self.translations[current_lang]['fields']
        
        for field, label in self.label_widgets:
            label.config(text=translations[field.name])
        
        self.button_text.set(translations['CALCULATE'])
        self.result_text_label.set(translations['RESULTS'])
        self.explanation_text.set(translations['EXPLANATION'])

    def calculate_prepayment(self):
        try:
            values = self.get_input_values()
            results = self.perform_calculations(values)
            self.display_results(results)
        except ValueError:
            current_lang = self.lang_var.get()
            error_msg = self.translations[current_lang]['messages']['error']
            messagebox.showerror("Error", error_msg)

    def get_input_values(self):
        return {
            'original': float(self.entries[Field.ORIGINAL_LOAN].get()),
            'remaining': float(self.entries[Field.REMAINING_BALANCE].get()),
            'months_left': int(self.entries[Field.MONTHS_LEFT].get()),
            'nominal_rate': float(self.entries[Field.NOMINAL_ANNUAL_INTEREST].get()) / 100,
            'adjusted_rate': float(self.entries[Field.ADJUSTED_ANNUAL_INTEREST].get()) / 100,
            'market_nominal_rate': float(self.entries[Field.MARKET_NOMINAL_INTEREST].get()) / 100,
            'market_adjusted_rate': float(self.entries[Field.MARKET_ADJUSTED_INTEREST].get()) / 100
        }

    def perform_calculations(self, values):
        # Use adjusted rates for calculations
        monthly_rate = values['adjusted_rate'] / 12
        market_monthly_rate = values['market_adjusted_rate'] / 12
        
        monthly_payment = values['remaining'] * (
            monthly_rate / (1 - (1 + monthly_rate) ** -values['months_left'])
        )
        
        total_future_payments = monthly_payment * values['months_left']
        remaining_interest = total_future_payments - values['remaining']
        total_prepayment_cost = values['remaining'] + self.ADMIN_FEE
        
        present_value_loan = sum(
            monthly_payment / ((1 + monthly_rate) ** t)
            for t in range(1, values['months_left'] + 1)
        )
        present_value_market = sum(
            monthly_payment / ((1 + market_monthly_rate) ** t)
            for t in range(1, values['months_left'] + 1)
        )
        
        discount_fee = max(0, present_value_market - present_value_loan)
        total_prepayment_cost_with_fee = total_prepayment_cost + discount_fee
        savings = total_future_payments - total_prepayment_cost_with_fee
        
        return {
            'monthly_payment': monthly_payment,
            'total_future_payments': total_future_payments,
            'remaining_interest': remaining_interest,
            'total_prepayment_cost': total_prepayment_cost,
            'discount_fee': discount_fee,
            'total_prepayment_cost_with_fee': total_prepayment_cost_with_fee,
            'savings': savings
        }

    def display_results(self, results):
        current_lang = self.lang_var.get()
        messages = self.translations[current_lang]['messages']
        
        if results['savings'] > 0:
            decision = messages['save']
        elif results['savings'] == 0:
            decision = messages['break_even']
        else:
            decision = messages['lose']
        
        # Format the results text with better spacing
        self.result_text.set(
            f"{self.translations[current_lang]['fields']['RESULTS']}\n\n"
            f"Monthly Payment: {results['monthly_payment']:.2f}\n"
            f"Total Future Payments: {results['total_future_payments']:.2f}\n"
            f"Remaining Interest: {results['remaining_interest']:.2f}\n"
            f"Total Prepayment Cost: {results['total_prepayment_cost']:.2f}\n"
            f"Discount Fee: {results['discount_fee']:.2f}\n"
            f"Final Prepayment Cost: {results['total_prepayment_cost_with_fee']:.2f}\n"
        )
        
        # Format the explanation text
        self.explanation_text.set(
            f"{decision} (Savings: {results['savings']:.2f})"
        )

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoanCalculator()
    app.run()