import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from re import findall
from puzzle import your_function  # Replace with your actual library and function

class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Creator")
        self.root.resizable(False, False)
        self.root.configure(background='lavender')

        self.rows_var = tk.IntVar(value=5)
        self.columns_var = tk.IntVar(value=5)

        self.create_input_fields()
        self.grid_frame = ttk.Frame(self.root)
        self.grid_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="nsew")

        self.compute_button = ttk.Button(self.root, text="Compute", command=self.compute)
        self.compute_button.grid(row=3, column=0, columnspan=5, pady=5)

        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.rows_var.trace_add('write', self.create_grid)
        self.columns_var.trace_add('write', self.create_grid)

        self.current_color = None
        self.create_grid()

    def create_input_fields(self):
        input_frame = ttk.Frame(self.root)
        input_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=5, sticky="ew")

        ttk.Label(input_frame, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        self.rows_entry = ttk.Entry(input_frame, textvariable=self.rows_var, width=5)
        self.rows_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="-", command=lambda: self.increment_decrement(self.rows_var, -1)).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(input_frame, text="+", command=lambda: self.increment_decrement(self.rows_var, 1)).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Columns:").grid(row=1, column=0, padx=5, pady=5)
        self.columns_entry = ttk.Entry(input_frame, textvariable=self.columns_var, width=5)
        self.columns_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="-", command=lambda: self.increment_decrement(self.columns_var, -1)).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(input_frame, text="+", command=lambda: self.increment_decrement(self.columns_var, 1)).grid(row=1, column=3, padx=5, pady=5)

    def increment_decrement(self, var, value):
        current_value = var.get()
        if current_value + value >= 0:
            var.set(current_value + value)

    def create_grid(self, *args):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        try:
            rows = self.rows_var.get()
            columns = self.columns_var.get()

            for r in range(rows):
                for c in range(columns):
                    cell_frame = ttk.Frame(self.grid_frame, width=50, height=50)
                    cell_frame.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")

                    cell = tk.Canvas(cell_frame, width=50, height=50, bg="SystemButtonFace",
                                     borderwidth=1, relief="solid", highlightthickness=1,
                                     highlightbackground="light grey")
                    cell.pack(fill=tk.BOTH, expand=True)

                    plus_button = ttk.Button(cell_frame, text="+", command=lambda r=r, c=c: self.add_text(r, c), width=3)
                    plus_button.place(relx=1.0, rely=0.0, anchor='ne')

                    cell.bind("<Button-1>", self.start_paint)
                    cell.bind("<B1-Motion>", self.paint)

            for r in range(rows):
                self.grid_frame.rowconfigure(r, weight=1, minsize=50)
            for c in range(columns):
                self.grid_frame.columnconfigure(c, weight=1, minsize=50)

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid integers for rows and columns.")

    def start_paint(self, event):
        self.current_color = self.get_next_color(event.widget.cget("bg"))
        self.paint(event)

    def paint(self, event):
        if self.current_color is not None:
            event.widget.config(bg=self.current_color)

            if self.current_color == "SystemButtonFace":
                event.widget.config(highlightbackground="light grey")
            else:
                event.widget.config(highlightbackground="black")


    def get_next_color(self, current_color):
        if current_color == "SystemButtonFace":
            return "black"
        elif current_color == "black":
            return "grey"
        elif current_color == "grey":
            return "white"
        elif current_color == "white":
            return "SystemButtonFace"
        return "SystemButtonFace"

    def add_text(self, r, c):
        text = simpledialog.askstring("Input", "Enter text:")
        if text:
            cell = self.grid_frame.grid_slaves(row=r, column=c)[0].children['!canvas']
            text_color = "blue"

            # Check for existing text items and update or create
            text_items = cell.find_withtag("text")
            if text_items:
                # Update the existing text
                cell.itemconfig(text_items[0], text=text)
            else:
                # Create new text if none exists
                cell.create_text(25, 25, text=text, fill=text_color, font=("Arial", 10), tags="text")


    def compute(self):
        result = your_function()  # Adjust this as needed
        #messagebox.showinfo("Result", f"The result is: {result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()
