from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Prathmesh312@',
    'database': 'travelling'
}

# Home page
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/top',methods=['GET', 'POST'])
def top():
    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Query to fetch top destinations with a rating of 4 or higher
    cursor.execute("SELECT * FROM Destination WHERE rating >= 4 ORDER BY rating DESC LIMIT 10")
    top_destinations = cursor.fetchall()
   
    if request.method == "POST":
        state=request.form.get("state")
        query=("select *from Destination where state = %s")
        cursor.execute(query,(state,))
        top_destinations=cursor.fetchall()
        

    # Close the connection
    cursor.close()
    connection.close()

    # Pass the top destinations to the template
    return render_template('top.html', top_destinations=top_destinations)

@app.route('/custom', methods=['GET', 'POST'])
def custom_recommendations():
    recommendations = []
    if request.method == 'POST':
        activity_type = request.form.get('activity_type')
        max_cost = request.form.get('max_cost')
        interests = request.form.get('interests')
        climate = request.form.get('climate')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM Activites
            WHERE activity_type = %s AND cost <= %s
        """
        cursor.execute(query, (activity_type, max_cost))
        recommendations = cursor.fetchall()
        cursor.close()
        connection.close()

    return render_template('custom.html', recommendations=recommendations)


 
    
@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    if request.method == 'POST':
        budget = request.form.get('budget')
        travel_style = request.form.get('travel_style')
        interests = request.form.get('interests')
        climate = request.form.get('climate')
        duration = request.form.get('duration')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM Destination
            WHERE avg_cost_per_day <= %s
            AND rating >= 4
            """
        cursor.execute(query, (budget,))
        recommendations = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return render_template('recommendations.html', recommendations=recommendations)

    return render_template('recommendations.html')

# Destination details page
@app.route('/destination/<int:destination_id>')
def destination_details(destination_id):
    # Fetch destination details from the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Destination WHERE destination_id = %s", (destination_id,))
    destination = cursor.fetchone()
    cursor.close()
    connection.close()

    return render_template('destination.html', destination=destination)

# User Feedback Page
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Get feedback data
        user_id = request.form.get('user_id')
        destination_id = request.form.get('destination_id')
        rating = request.form.get('rating')
        comments = request.form.get('comments')

        # Insert feedback into the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO User_Feedback (user_id, destination_id, rating, comments) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, destination_id, rating, comments))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('feedback'))

    return render_template('feedback.html')

@app.route('/update_delete')
def update_delete():
    # Render the update_delete.html template
    return render_template('update_delete.html')

@app.route('/update_user', methods=['POST'])
def update_user():
    # Get form data
    user_id = request.form.get('user_id')
    name = request.form.get('name')
    email = request.form.get('email')

    # Update user in the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "UPDATE User SET name = %s WHERE user_id = %s"
    cursor.execute(query, (name, user_id))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('update_delete'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    # Get form data
    user_id = request.form.get('user_id')

    # Delete user from the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "DELETE FROM User WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('update_delete'))


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
