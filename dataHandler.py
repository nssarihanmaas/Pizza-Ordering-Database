import tkinter.messagebox as messagebox
from decimal import Decimal
from connection import create_connection

class PizzaDataHandler:
    def __init__(self):
        # Initialize the database connection
        self.connection = create_connection()
        if self.connection is None:
            messagebox.showerror("Connection Error", "Failed to connect to the database.")
        else:
            self.cursor = self.connection.cursor()

    def fetch_pizza_options(self):
        """Fetch pizza names from the database to populate the ComboBox."""
        try:
            self.cursor.execute("SELECT Name FROM pizza")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching pizza options: {str(e)}")
            return []

    def fetch_sideitem_options(self):
        """Fetch item names from the database to populate the ComboBox."""
        try:
            self.cursor.execute("SELECT Name FROM standartmenuitem")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching pizza options: {str(e)}")
            return []

    def get_pizza_id(self, pizza_name):
        """Fetches the Pizza ID based on the pizza name."""
        try:
            self.cursor.execute("SELECT PizzaID FROM pizza WHERE Name = %s", (pizza_name,))
            return self.cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching pizza ID: {str(e)}")
            return None
        
    def get_side_info(self, side_name):
        """Fetches the Side item ID based on the name."""
        try:
            self.cursor.execute("SELECT * FROM standartmenuitem WHERE Name = %s", (side_name,))
            return self.cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching pizza ID: {str(e)}")
            return None
        
    def get_ingredients(self, pizza_id):
        """Fetches the ingredients associated with the given Pizza ID."""
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
            # Step 1: Fetch all ingredients for the given pizza
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.ingredientId
                WHERE pi.PizzaID = %s
            """, (pizza_id,))
            total_ingredients = self.cursor.fetchone()[0]

            # Step 2: Fetch vegetarian ingredients for the given pizza
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.ingredientId
                WHERE i.isVegetarian = TRUE AND pi.PizzaID = %s
            """, (pizza_id,))
            vegetarian_ingredients = self.cursor.fetchone()[0]

            # Step 3: Check if all ingredients are vegetarian
            is_vegetarian = total_ingredients == vegetarian_ingredients
            return is_vegetarian

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking vegetarian status: {str(e)}")
            return False

    def get_vegeaninfo(self, pizza_id):
        try:
            # Step 1: Fetch all ingredients for the given pizza
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.ingredientId
                WHERE pi.PizzaID = %s
            """, (pizza_id,))
            total_ingredients = self.cursor.fetchone()[0]

            # Step 2: Fetch vegetarian ingredients for the given pizza
            self.cursor.execute("""
                SELECT COUNT(*)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.ingredientId
                WHERE i.isVegan = TRUE AND pi.PizzaID = %s
            """, (pizza_id,))
            vegan_ingredients = self.cursor.fetchone()[0]

            # Step 3: Check if all ingredients are vegetarian
            is_vegan = total_ingredients == vegan_ingredients
            return is_vegan

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking vegetarian status: {str(e)}")
            return False

    def calculate_pizza_price(self, pizza_id):
        """
        Calculates the final price of a pizza based on its base price, ingredient costs,
        quantities, a 40% profit margin, and 9% VAT.
        """
        try:
            # Step 1: Fetch the base price of the pizza
            self.cursor.execute("""
                SELECT BasePrice
                FROM pizza
                WHERE PizzaID = %s
            """, (pizza_id,))
            base_price = self.cursor.fetchone()[0]

            # Step 2: Fetch total ingredient cost for the given pizza
            self.cursor.execute("""
                SELECT SUM(i.CostPerUnit * pi.Quantity)
                FROM ingredient i
                JOIN pizza_ingredients pi ON i.IngredientID = pi.IngredientID
                WHERE pi.PizzaID = %s
            """, (pizza_id,))
            total_ingredient_cost = self.cursor.fetchone()[0] or 0  # Default to 0 if no ingredients

            # Ensure total_ingredient_cost is a Decimal
            total_ingredient_cost = Decimal(total_ingredient_cost)

            # Step 3: Calculate the final price
            final_price = (base_price + total_ingredient_cost) * Decimal('1.4') * Decimal(
                '1.09')  # 40% profit margin and 9% VAT
            return round(final_price, 2)  # Round to 2 decimal places

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating the pizza price: {str(e)}")
            return 0

    def close_connection(self):
        """Closes the cursor and the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()