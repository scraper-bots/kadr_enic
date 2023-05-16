import time
import tkinter as tk
from tkinter import messagebox

class TypingTestApp:
    def __init__(self, master):
        self.master = master
        master.title("Typing Test")

        # Initialize variables
        self.text = "The quick brown fox jumps over the lazy dog."
        self.index = 0
        self.start_time = None
        self.elapsed_time = None

        # Create GUI elements
        self.text_label = tk.Label(master, text=self.text, font=("Arial", 16))
        self.text_label.pack()

        self.input_entry = tk.Entry(master, font=("Arial", 16))
        self.input_entry.pack()
        self.input_entry.focus()

        self.start_button = tk.Button(master, text="Start", command=self.start_test)
        self.start_button.pack()

    def start_test(self):
        """Starts the typing test."""
        self.index = 0
        self.start_time = time.time()
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(state="normal")
        self.input_entry.focus()

        self.master.bind("<Return>", self.check_input)
        self.master.bind("<Escape>", self.cancel_test)

    def check_input(self, event):
        """Checks the user's input against the test text."""
        input_text = self.input_entry.get()
        if input_text == self.text:
            self.end_test()
        else:
            correct_char = self.text[self.index]
            if input_text[-1] == correct_char:
                self.index += 1
                self.text_label.config(fg="black")
            else:
                self.text_label.config(fg="red")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.text[:self.index+1])

    def cancel_test(self, event):
        """Cancels the typing test."""
        self.master.unbind("<Return>")
        self.master.unbind("<Escape>")
        self.input_entry.config(state="disabled")

    def end_test(self):
        """Ends the typing test and displays the results."""
        self.elapsed_time = time.time() - self.start_time
        wpm = len(self.text) / 5 / (self.elapsed_time / 60)
        messagebox.showinfo("Typing Test", f"Your typing speed is {wpm:.2f} WPM!")
        self.cancel_test(None)

# Create the GUI window
root = tk.Tk()
app = TypingTestApp(root)
root.mainloop()
