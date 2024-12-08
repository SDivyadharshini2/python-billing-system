import tkinter as tk
from tkinter import ttk

# Function to update product details when selected
def on_product_select(event):
    selected_product = product_list_box.selection()
    if selected_product:
        product_info = product_list_box.item(selected_product[0], "values")
        product_name.set(product_info[0])
        product_price.set(product_info[1])
        product_gst.set(product_info[2])
        
        # Clear quantity and reset total price
        quantity.set("")  
        total_price.set(0)
        
        # Set the quantity label based on the product type
        if product_info[0].lower() in ['apple', 'orange', 'mango', 'banana', 'grapes', 'carrot', 'tomato', 'cucumber']:  # Fruits and vegetables: Weight (kg)
            quantity_label.config(text="Quantity (kg):")
        elif product_info[0].lower() in ['shampoo', 'soap', 'oil', 'rice', 'wheat flour', 'sugar', 'butter', 'cheese', 'yogurt', 'chips', 'cereal']:  # Non-fruits: Quantity (Units)
            quantity_label.config(text="Quantity (Units):")
        else:  # Beverages and packaged items: Quantity (Packs/Bottles)
            quantity_label.config(text="Quantity (Packs/Bottles):")
        
        update_total()

# Function to update total price based on quantity, product type, and GST
def update_total():
    try:
        qty = float(quantity.get())
        price = float(product_price.get())
        gst_rate = float(product_gst.get())
        
        # Calculate GST amount
        gst_amount = (price * qty * gst_rate) / 100
        
        # Total price with GST
        total_with_gst = (price * qty) + gst_amount
        total_price.set(f"{total_with_gst:.2f}")
    except ValueError:
        total_price.set(0)

# Function to calculate the total price and display the result
def calculate_price():
    update_total()

# Function to add selected product to the billing list
def add_to_billing():
    # First calculate the total price before adding to the billing list
    update_total()

    # Add the calculated details to the billing list
    product_details = (product_name.get(), product_price.get(), product_gst.get(), quantity.get(), total_price.get())
    billing_listbox.insert("", "end", values=product_details)
    separator = ("---------------------------------------", "---------------------------------------", "---------------------------------------",  "---------------------------------------",  "---------------------------------------")
    billing_listbox.insert("", "end", values=separator, tags="separator")
    product_price.set("")
    product_gst.set("")
    quantity.set("")
    total_price.set(0)

# Function to center the window
def center_window(root):
    # Get the screen's width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get the current window's width and height
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Calculate position to center the window on the screen
    position_top = int((screen_height - window_height) / 2)
    position_left = int((screen_width - window_width) / 2)

    # Set the window's geometry to center it
    root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

# Create main window
root = tk.Tk()
root.title("Billing System")
root.geometry("800x600")  # Set the initial size of the window (can adjust as needed)
center_window(root)

root.iconbitmap(r'F:\PYTHON\billingss\image\grocery.ico')  
# Shop name (title label) centered
title_label = tk.Label(root, text="Fresh Basket Grocery", font=("Arial",24,"bold"),fg="darkgreen")
title_label.grid(row=0,column=0,columnspan=3,pady=10,sticky="nsew")

# Set up style to change text color for Treeview widgets
style = ttk.Style()
style.configure("Treeview", foreground="blue")  # Change the text color for all items in the product list Treeview

# Set up a new style for the billing list with red color
style.configure("Billing.Treeview", foreground="red")  # Change the text color for the billing list Treeview

# Create frames and widgets as per your original layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=3)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_columnconfigure(2, weight=3)

# Left frame (for product details)
left_frame = tk.Frame(root, padx=40, pady=40, width=400, height=400, borderwidth=5, relief="solid")
left_frame.grid(row=1, column=1, padx=20, pady=20)

# Entry fields for product details
tk.Label(left_frame, text="Product Name:").grid(row=0, column=0, sticky="w")
product_name = tk.StringVar()
tk.Entry(left_frame, textvariable=product_name, state="readonly").grid(row=0, column=1)

tk.Label(left_frame, text="Price:").grid(row=1, column=0, sticky="w")
product_price = tk.StringVar()
tk.Entry(left_frame, textvariable=product_price, state="readonly").grid(row=1, column=1)

tk.Label(left_frame, text="GST Rate (%):").grid(row=2, column=0, sticky="w")
product_gst = tk.StringVar()
tk.Entry(left_frame, textvariable=product_gst, state="readonly").grid(row=2, column=1)

quantity_label = tk.Label(left_frame, text="Quantity:")
quantity_label.grid(row=3, column=0, sticky="w")
quantity = tk.StringVar()
quantity_entry = tk.Entry(left_frame, textvariable=quantity)
quantity_entry.grid(row=3, column=1)

tk.Label(left_frame, text="Total Price (incl. GST):").grid(row=4, column=0, sticky="w")
total_price = tk.StringVar()
tk.Label(left_frame, textvariable=total_price).grid(row=4, column=1)

# Buttons for calculation and adding to billing
calculate_button = tk.Button(left_frame, text="Calculate", command=calculate_price)
calculate_button.grid(row=5, column=0)

add_button = tk.Button(left_frame, text="Add to Billing", command=add_to_billing)
add_button.grid(row=5, column=1)

# Right frame (for product list)
right_frame = tk.Frame(root, padx=50, pady=50, width=300, height=400, borderwidth=5, relief="solid", bg="lightblue")
right_frame.grid(row=1, column=2, padx=20, pady=20)

# Create product list (Treeview)
columns = ("Product Name", "Price", "GST Rate (%)")
product_list_box = ttk.Treeview(right_frame, columns=columns, show="headings")
product_list_box.grid(row=0, column=0)

# Define the headings for the product list columns
for col in columns:
    product_list_box.heading(col, text=col)

# Sample products to populate in the table (30 products)
products = [
    ("Apple", 250, 18), ("Orange", 150, 12), ("Shampoo", 100, 18), ("Soap", 50, 12),
    ("Oil", 200, 18), ("Banana", 120, 5), ("Mango", 300, 12), ("Grapes", 350, 18),
    ("Carrot", 80, 5), ("Tomato", 60, 5), ("Cucumber", 50, 12), ("Rice", 80, 5),
    ("Wheat Flour", 40, 5), ("Milk", 50, 12), ("Tea", 150, 18), ("Coffee", 200, 18),
    ("Sugar", 45, 5), ("Butter", 250, 18), ("Cheese", 300, 18), ("Yogurt", 80, 12),
    ("Juice", 120, 12), ("Soda", 60, 18), ("Chips", 50, 12), ("Cereal", 180, 18),
    ("Butter", 250, 18), ("Pasta", 100, 18), ("Juice Box", 60, 12), ("Peanut Butter", 180, 18),
    ("Honey", 250, 18)
]

# Insert products into the treeview
for product in products:
    product_list_box.insert("", "end", values=product)

# Bind the selection event for product selection
product_list_box.bind("<<TreeviewSelect>>", on_product_select)

# Create a frame for the billing list (billing frame)
billing_frame = tk.Frame(root, padx=10, pady=10 ,width=600,height=400,borderwidth=5, relief="solid")
billing_frame.grid(row=3, column=0, columnspan=3, pady=20)

# Billing list (Treeview) with the red text color style
billing_columns = ("Product Name", "Price", "GST Rate (%)", "Quantity", "Total Price")
billing_listbox = ttk.Treeview(billing_frame, columns=billing_columns, show="headings", style="Billing.Treeview")
billing_listbox.grid(row=0, column=0)
# Set up the style for the separator row
style.configure("separator.Treeview", foreground="gray", font=("Arial", 10, "bold"), relief="sunken")

# Apply the separator style to the Treeview
billing_listbox.tag_configure("separator", background="lightgray")


# Define the headings for the billing columns
for col in billing_columns:
    billing_listbox.heading(col, text=col)

root.configure(bg='pink')
root.mainloop()
