import tkinter as tk

# Initialize the main window
window = tk.Tk()
window.title("Calculator")
window.resizable(False, False) # Prevent resizing for a fixed layout

# Global variable to manage the state of the calculator display.
# True means the last operation was '=' or 'Error', so the next digit should clear the display.
# False means we are currently building a number or an expression.
should_clear_display = False

def on_button_click(event):
    """
    Handles button clicks on the calculator.
    """
    global should_clear_display
    
    current_text = display.get() # Get the current text in the display
    button_label = event.widget.cget('text') # Get the text from the clicked button

    if button_label == 'C':
        # Clear button: clear the display and reset the state
        display.delete(0, tk.END)
        should_clear_display = False
    elif button_label == '=':
        # Equals button: evaluate the expression
        if current_text: # Only attempt to evaluate if the display is not empty
            try:
                # Replace common calculator symbols with Python's operators for eval()
                # This handles cases where 'x' or '÷' might be used in the UI
                expression = current_text.replace('×', '*').replace('÷', '/')
                
                # Evaluate the expression
                result = str(eval(expression))
                
                # Display the result
                display.delete(0, tk.END)
                display.insert(tk.END, result)
                
                # Set flag to clear display for the next number input
                should_clear_display = True
            except (SyntaxError, ZeroDivisionError, TypeError, NameError):
                # Catch specific common errors during evaluation
                display.delete(0, tk.END)
                display.insert(tk.END, "Error")
                should_clear_display = True # Keep flag true so next digit clears error
            except Exception as e:
                # Catch any other unexpected errors during evaluation
                display.delete(0, tk.END)
                display.insert(tk.END, "Error")
                should_clear_display = True
    else:
        # Other buttons (digits, operators)
        if should_clear_display:
            # If a calculation was just completed or an error occurred,
            # and the next input is a digit or decimal, start a new entry.
            if button_label.isdigit() or button_label == '.':
                display.delete(0, tk.END)
                display.insert(tk.END, button_label)
                should_clear_display = False # Reset flag as we are building a new number
            else:
                # If it's an operator after a calculation, append it to the result
                display.insert(tk.END, button_label)
                should_clear_display = False # Continue the calculation
        else:
            # Otherwise, just append the button's text to the current display
            display.insert(tk.END, button_label)

# Create the display entry widget
display = tk.Entry(window, width=16, font=('Arial', 24), justify='right', bd=5, relief='sunken')
display.pack(fill=tk.X, padx=10, pady=10, ipady=10) # ipady adds internal padding for height

# Create a frame to hold the buttons
button_frame = tk.Frame(window)
button_frame.pack()

# Define the labels for the calculator buttons
button_labels = [
    '7', '8', '9', '+',
    '4', '5', '6', '-',
    '1', '2', '3', '*',
    'C', '0', '=', '/'
]

# Create and place buttons in a grid
row_val = 0
col_val = 0
for label in button_labels:
    button = tk.Button(
        button_frame, 
        text=label, 
        width=5, 
        height=2, 
        font=('Arial', 18),
        bd=3, # Border thickness
        relief='raised' # 3D effect for buttons
    )
    # Place the button in the grid
    button.grid(row=row_val, column=col_val, padx=5, pady=5)
    
    # Bind the click event to the on_button_click function
    button.bind('<Button-1>', on_button_click)
    
    # Update row and column for the next button
    col_val += 1
    if col_val > 3: # Move to the next row after every 4 columns
        col_val = 0
        row_val += 1

# Start the Tkinter event loop
window.mainloop()
