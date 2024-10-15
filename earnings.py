from connection import create_connection  


def print_earnings_by_area_code():
    
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

    query_earnings_by_age = """
    SELECT 
        CASE 
            WHEN c.age BETWEEN 0 AND 15 THEN '0-15'
            WHEN c.age BETWEEN 16 AND 25 THEN '16-25'
            WHEN c.age BETWEEN 26 AND 40 THEN '26-40'
            ELSE '41+' 
        END AS age_range,
        SUM(o.TotalPrice) AS total_earnings
    FROM orderticket o
    JOIN customer ct ON o.CustomerID = ct.CustomerID
    JOIN customer c ON ct.CustomerID = c.CustomerID
    WHERE o.IsCancelled = FALSE
    GROUP BY age_range;
    """

    cursor.execute(query_earnings_by_age)
    results2 = cursor.fetchall()

    # print it by age range
    print("Earnings by Age Range:")
    for row in results2:
        age_range, total_earnings = row

        if total_earnings is None:
            total_earnings = 0.0
            
        print(f"Age Range: {age_range}, Total Earnings: ${total_earnings:.2f}")
    # print by area code
    print("Earnings by Area Code:")
    for row in results:
        area_code, total_earnings = row

        if total_earnings is None:
            total_earnings = 0.0
            
        print(f"Area Code: {area_code}, Total Earnings: ${total_earnings:.2f}")

    
    cursor.close()
    conn.close()


print_earnings_by_area_code()
