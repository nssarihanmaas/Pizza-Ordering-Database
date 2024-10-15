import tkinter.messagebox as messagebox
from decimal import Decimal
from connection import create_connection

class PizzaDataHandler:
    def __init__(self):
        # making the database connection
        self.connection = create_connection()
        if self.connection is None:
            messagebox.showerror("Connection Error", "Failed to connect to the database.")
        else:
            self.cursor = self.connection.cursor()

    def fetch_pizza_options(self):
        """Fetch the pizza names for the combobox"""
        try:
            self.cursor.execute("SELECT Name FROM pizza")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching pizza options: {str(e)}")
            return []

    def fetch_sideitem_options(self):
        """Fetch the extra items for the combobox"""
        try:
            self.cursor.execute("SELECT Name FROM standartmenuitem")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching pizza options: {str(e)}")
            return []

    def get_pizza_id(self, pizza_name):
        """Fetches the pizza id on the pizza name"""
        try:
            self.cursor.execute("SELECT PizzaID FROM pizza WHERE Name = %s", (pizza_name,))
            return self.cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching pizza ID: {str(e)}")
            return None
        
    def get_side_info(self, side_name):
        """Fetches the extra item id"""
        try:
            self.cursor.execute("SELECT * FROM standartmenuitem WHERE Name = %s", (side_name,))
            return self.cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching pizza ID: {str(e)}")
            return None
        
    def get_ingredients(self, pizza_id):
        """Fetches the ingredients for the picked pizza"""
        try:
            self.cursor.execute("""
                SELECT i.Name
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.ingredientId
                WHERE pi.PizzaID = %s
            """, (pizza_id,))
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching ingredients: {str(e)}")
            return []

    def get_vegetarianinfo(self, pizza_id):
        try:
            # gets the pizza ingredient information and checks every ingredient vegetarian info 
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.ingredientId
                WHERE pi.PizzaID = %s
            """, (pizza_id,))
            total_ingredients = self.cursor.fetchone()[0]

            
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.ingredientId
                WHERE i.isVegetarian = TRUE AND pi.PizzaID = %s
            """, (pizza_id,))
            vegetarian_ingredients = self.cursor.fetchone()[0]

            
            is_vegetarian = total_ingredients == vegetarian_ingredients
            return is_vegetarian

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking vegetarian status: {str(e)}")
            return False

    def get_vegeaninfo(self, pizza_id):
        try:
            # gets the pizza ingredient information and checks every ingredient vegan info 
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.ingredientId
                WHERE pi.PizzaID = %s
            """, (pizza_id,))
            total_ingredients = self.cursor.fetchone()[0]

            
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.ingredientId
                WHERE i.isVegan = TRUE AND pi.PizzaID = %s
            """, (pizza_id,))
            vegan_ingredients = self.cursor.fetchone()[0]

            
            is_vegan = total_ingredients == vegan_ingredients
            return is_vegan

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking vegetarian status: {str(e)}")
            return False

    def calculate_pizza_price(self, pizza_id):
        """
        the final price of a pizza based on its base price plus ingredient and
        quantities calculated with 40% profit margin, and 9% VAT.
        """
        try:
            #gets the bace price fot the pizza and adds it with the total ingredient cost of that pizza
            self.cursor.execute("""
                SELECT BasePrice
                FROM pizza
                WHERE PizzaID = %s
            """, (pizza_id,))
            base_price = self.cursor.fetchone()[0]

            
            self.cursor.execute("""
                SELECT SUM(i.CostPerUnit * pi.Quantity)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.IngredientID
                WHERE pi.PizzaID = %s
            """, (pizza_id,))
            total_ingredient_cost = self.cursor.fetchone()[0] or 0 

           
            total_ingredient_cost = Decimal(total_ingredient_cost)

            # 40% profit margin and 9% VAT
            final_price = (base_price + total_ingredient_cost) * Decimal('1.4') * Decimal(
                '1.09') 
            return round(final_price, 2)  

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating the pizza price: {str(e)}")
            return 0

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()