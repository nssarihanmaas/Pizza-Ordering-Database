from customtkinter import*
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkButton, CTkLabel, CTkComboBox
from connection import create_connection
from dataHandler import*
from orderHandler import*
from discountChecker import*

data_handler = PizzaDataHandler()

if data_handler.connection is None:
    print("Failed to connect to the database.")
else:
    print("Connected to the database successfully.")

# Check for discounts
is_birthday = check_if_birthday()
is_discounted = check_if_11th_order()


window=CTk()
window.geometry('700x430')
window.resizable(False,False)
window.title('Order')

leftFrame=CTkFrame(window)
leftFrame.grid(row=6,column=5)

rightFrame=CTkFrame(window)
rightFrame.grid(row=6,column=8)

orderReviewLabel=CTkLabel(rightFrame,text='Your Order Review:',font=('Arial',18,'bold'),width=50)
orderReviewLabel.grid(row=0,column=0,padx=10,pady=10)

if(is_birthday):
    birthdayLabel = CTkLabel(rightFrame,text='Happy birthday! Have a free side!',font=('Arial',15,'bold'),width=50)
    birthdayLabel.grid(row=1,column=0,padx=10,pady=10)

if(is_discounted):
    birthdayLabel = CTkLabel(rightFrame,text='You have a 10% discount on this order!',font=('Arial',15,'bold'),width=50)
    birthdayLabel.grid(row=2,column=0,padx=10,pady=10)

orderReviewText = tk.Text(rightFrame, height=10, width=37, wrap="word")
orderReviewText.grid(row=3, column=0, padx=10, pady=10)

pizzaPickingLabel=CTkLabel(leftFrame,text='Pick your pizza!',font=('Arial',18,'bold'),width=50)
pizzaPickingLabel.grid(row=0,column=2,padx=30,pady=10)

pizza_options = data_handler.fetch_pizza_options()
pizzaOptionsBox = CTkComboBox(leftFrame, values=pizza_options)
pizzaOptionsBox.grid(row=1, column=2, padx=30, pady=10)

sideitem_options = data_handler.fetch_sideitem_options()
sideOptionsBox = CTkComboBox(leftFrame, values=sideitem_options)
sideOptionsBox.grid(row=2, column=2, padx=30, pady=10)

ingredientsText = tk.Text(leftFrame, height=10, width=40, wrap="word")
ingredientsText.grid(row=4, column=2, padx=30, pady=10)



def showingredient():
    #this function gets the pizza id and checks the ingredients that pizza id has checks if its vegetarian or vegan and displays the final price
    ingredientsText.delete(1.0, tk.END)

    selected_pizza = pizzaOptionsBox.get()

    pizza_result = data_handler.get_pizza_id(selected_pizza)
    if not pizza_result:
        ingredientsText.insert(tk.END, f"No pizza found with the name '{selected_pizza}'.")
        return

    pizza_id = pizza_result[0]  

    
    ingredients = data_handler.get_ingredients(pizza_id)
    if ingredients:
        
        ingredients_list = "\n".join(ingredients)  
        ingredientsText.insert(tk.END, f"Ingredients for {selected_pizza}:\n{ingredients_list}\n")

        
        is_vegan = data_handler.get_vegeaninfo(pizza_id)
        if is_vegan:
            ingredientsText.insert(tk.END, f"This pizza is vegan.\n")
        else:
            
            is_vegetarian = data_handler.get_vegetarianinfo(pizza_id)
            if is_vegetarian:
                ingredientsText.insert(tk.END, f"This pizza is vegetarian.\n")
            else:
                ingredientsText.insert(tk.END, f"This pizza is not vegetarian.\n")

        final_price = data_handler.calculate_pizza_price(pizza_id)
        ingredientsText.insert(tk.END, f"The final price for {selected_pizza} is: €{final_price:.2f}\n")
    else:
        ingredientsText.insert(tk.END, f"No ingredients found for '{selected_pizza}'.")

def add_to_order_review():
    #this function adds the picked pizza and if ther is the side item and adds it to the order
    selected_pizza = pizzaOptionsBox.get()
    selected_sideitem = sideOptionsBox.get()

    
    if not selected_pizza and not selected_sideitem:
        messagebox.showerror("Error", "Please select at least one item to add to the order.")
        return

    
    orderReviewText.insert(tk.END, f"Pizza: {selected_pizza}\n")
    orderReviewText.insert(tk.END, f"Side Item: {selected_sideitem}\n")
    orderReviewText.insert(tk.END, "-"*37 + "\n") 

    
    pizza_result = data_handler.get_pizza_id(selected_pizza)
    if not pizza_result:
        ingredientsText.insert(tk.END, f"No pizza found with the name '{selected_pizza}'.")
        return

    
    pizza_id = pizza_result[0]  
    final_price = data_handler.calculate_pizza_price(pizza_id) 
    orderHandlder.addOrderItem(pizza_id, "'Pizza'", final_price)

    
    side_result = data_handler.get_side_info(selected_sideitem)
    side_id = side_result[0]
    side_price = side_result[2]
    if selected_sideitem != sideitem_options[-1]:
        orderHandlder.addOrderItem(side_id, "'Dessert'", side_price)
    


def reset_order_review():
    #this resets the order review
    orderReviewText.delete(1.0, tk.END)
    orderHandlder.clear_query()


def place_order():
    #this calls the placeOrder function and opens the new window for order review
    orderHandlder.placeOrder()
    window.destroy()
    import orderReview

resetButton=CTkButton(rightFrame, text='Reset',cursor='hand2', command=reset_order_review)
resetButton.grid(row=4,column=0,padx=30,pady=10)

placeButton=CTkButton(rightFrame, text='Place Order',cursor='hand2', command=place_order)
placeButton.grid(row=5,column=0,padx=30,pady=10)

showIngredientButton=CTkButton(leftFrame, text='Ingredients',cursor='hand2', command=showingredient)
showIngredientButton.grid(row=3,column=2,padx=30,pady=10)


addButton=CTkButton(leftFrame, text='Add',cursor='hand2', command=add_to_order_review)
addButton.grid(row=5,column=2,padx=30,pady=10)

window.mainloop()