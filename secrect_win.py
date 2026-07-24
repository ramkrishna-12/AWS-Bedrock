import secrets
import tkinter as tk

# Generate random hex string
bust = secrets.token_hex(10000)   # Don't use 100000000 unless you enjoy waiting and running out of memory.

# Create window
root = tk.Tk()
root.title("Random Hex")

# Create text box
text = tk.Text(
    root,
    bg="black",        # Background color
    fg="lime",         # Text color
    font=("Consolas", 10),
    wrap="word"
)

text.pack(expand=True, fill="both")

# Insert text
text.insert("1.0", bust)

# Make read-only
text.config(state="disabled")

root.geometry("800x600")

root.mainloop()