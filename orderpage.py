from customtkinter import*
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkButton, CTkLabel, CTkComboBox
from connection import create_connection
from dataHandler import*

data_handler = PizzaDataHandler()

# Check connection status
if data_handler.connection is None:
    print("Failed to connect to the database.")
else:
    print("Connected to the database successfully.")




window=CTk()
window.geometry('500x500')
window.resizable(False,False)
window.title('Order')

leftFrame=CTkFrame(window)
leftFrame.grid(row=6,column=6)

pizzaPickingLabel=CTkLabel(leftFrame,text='Pick your pizza!',font=('Arial',18,'bold'),width=50)
pizzaPickingLabel.grid(row=0,column=2,padx=30,pady=15)

# Create the ComboBox with the fetched options
pizza_options = data_handler.fetch_pizza_options()
pizzaOptionsBox = CTkComboBox(leftFrame, values=pizza_options)
pizzaOptionsBox.grid(row=1, column=2, padx=30, pady=15)


ingredientsText = tk.Text(leftFrame, height=10, width=40, wrap="word")
ingredientsText.grid(row=4, column=2, padx=30, pady=15)

def showingredient():
    # Clear the text widget before updating
    ingredientsText.delete(1.0, tk.END)

    # Get the selected pizza from the ComboBox
    selected_pizza = pizzaOptionsBox.get()

    # Fetch the Pizza ID
    pizza_result = data_handler.get_pizza_id(selected_pizza)
    if not pizza_result:
        ingredientsText.insert(tk.END, f"No pizza found with the name '{selected_pizza}'.")
        return

    pizza_id = pizza_result[0]  # Extract the correct Pizza ID

    # Fetch and display the ingredients
    ingredients = data_handler.get_ingredients(pizza_id)
    if ingredients:
        # Display all ingredients
        ingredients_list = "\n".join(ingredients)  # Assuming ingredient[0] is the name
        ingredientsText.insert(tk.END, f"Ingredients for {selected_pizza}:\n{ingredients_list}\n")

        # Step 1: Check if the pizza is vegan
        is_vegan = data_handler.get_vegeaninfo(pizza_id)
        if is_vegan:
            ingredientsText.insert(tk.END, f"This pizza is vegan.\n")
        else:
            # Step 2: If not vegan, check if the pizza is vegetarian
            is_vegetarian = data_handler.get_vegetarianinfo(pizza_id)
            if is_vegetarian:
                ingredientsText.insert(tk.END, f"This pizza is vegetarian.\n")
            else:
                ingredientsText.insert(tk.END, f"This pizza is not vegetarian.\n")

        final_price = data_handler.calculate_pizza_price(pizza_id)
        ingredientsText.insert(tk.END, f"The final price for {selected_pizza} is: ${final_price:.2f}\n")
    else:
        ingredientsText.insert(tk.END, f"No ingredients found for '{selected_pizza}'.")

showIngredientButton=CTkButton(leftFrame, text='Ingredients',cursor='hand2', command=showingredient)
showIngredientButton.grid(row=2,column=2,padx=30,pady=15)

window.mainloop()