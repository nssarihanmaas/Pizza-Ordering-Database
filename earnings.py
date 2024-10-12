from connection import create_connection  # Importing the connection from the separate file

# Function to print total earnings by customer area codes
def print_earnings_by_area_code():
    # Use the connection from the imported file
    conn = create_connection()
    cursor = conn.cursor()

    # Query to calculate total earnings grouped by customer area codes
    query_earnings_by_area_code = """
    SELECT c.areaCode, SUM(o.TotalPrice) AS total_earnings
    FROM orderticket o
    JOIN customer ct ON o.CustomerID = ct.CustomerID
    JOIN customer c ON ct.CustomerID = c.CustomerID
    WHERE o.IsCancelled = FALSE
    GROUP BY c.areaCode;
    """
    
    cursor.execute(query_earnings_by_area_code)
    results = cursor.fetchall()
    
    # Print the total earnings by area code
    print("Earnings by Area Code:")
    for row in results:
        area_code, total_earnings = row

        if total_earnings is None:
            total_earnings = 0.0  # Default to 0.0 if no earnings
            
        print(f"Area Code: {area_code}, Total Earnings: ${total_earnings:.2f}")

    # Close the cursor and connection after the query
    cursor.close()
    conn.close()

# Call the function to print earnings by area code
print_earnings_by_area_code()
