from flask import Flask, request, render_template_string, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Define the HTML form for users
form_html = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Issue Report Form</title>
</head>
<body>
    <h2>Issue Report Form</h2>
    <form method="post">
        Name: <input type="text" name="name"><br>
        Employee ID: <input type="text" name="employee_id"><br>
        Type of Issue: 
        <select name="issue_type">
            <option value="Hardware">Hardware</option>
            <option value="Software">Software</option>
            <option value="Network">Network</option>
        </select><br>
        Machine Details: <input type="text" name="machine_details"><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
'''

# Define the HTML template for the admin console
admin_html = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Console</title>
</head>
<body>
    <h2>Admin Console</h2>
    <table border="1">
        <tr>
            <th>Ticket ID</th>
            <th>Name</th>
            <th>Employee ID</th>
            <th>Issue Type</th>
            <th>Machine Details</th>
            <th>Timestamp</th>
            <th>Status</th>
            <th>Update Status</th>
        </tr>
        {% for row in rows %}
        <tr>
            <td>{{ row['ticket_id'] }}</td>
            <td>{{ row['name'] }}</td>
            <td>{{ row['employee_id'] }}</td>
            <td>{{ row['issue_type'] }}</td>
            <td>{{ row['machine_details'] }}</td>
            <td>{{ row['timestamp'] }}</td>
            <td>{{ row['status'] }}</td>
            <td>
                <form method="post" action="{{ url_for('update_status') }}">
                    <input type="hidden" name="ticket_id" value="{{ row['ticket_id'] }}">
                    <select name="status">
                        <option value="Pending" {% if row['status'] == 'Pending' %}selected{% endif %}>Pending</option>
                        <option value="In Progress" {% if row['status'] == 'In Progress' %}selected{% endif %}>In Progress</option>
                        <option value="Resolved" {% if row['status'] == 'Resolved' %}selected{% endif %}>Resolved</option>
                    </select>
                    <input type="submit" value="Update">
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        employee_id = request.form['employee_id']
        issue_type = request.form['issue_type']
        machine_details = request.form['machine_details']
        timestamp = datetime.now().isoformat()
        ticket_id = datetime.now().strftime('%Y%m%d%H%M%S')
        status = 'Pending'  # Default status

        # Save form data to CSV file
        file_exists = os.path.isfile('responses.csv')
        with open('responses.csv', 'a', newline='') as csvfile:
            fieldnames = ['ticket_id', 'name', 'employee_id', 'issue_type', 'machine_details', 'timestamp', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()  # Write header only once
            writer.writerow({
                'ticket_id': ticket_id,
                'name': name,
                'employee_id': employee_id,
                'issue_type': issue_type,
                'machine_details': machine_details,
                'timestamp': timestamp,
                'status': status
            })

        return 'Form submitted successfully!'
    return render_template_string(form_html)


@app.route('/admin', methods=['GET'])
def admin():
    # Read data from CSV file
    rows = []
    if os.path.isfile('responses.csv'):
        with open('responses.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(row)

    return render_template_string(admin_html, rows=rows)


@app.route('/update_status', methods=['POST'])
def update_status():
    ticket_id = request.form['ticket_id']
    new_status = request.form['status']

    # Read all data from CSV
    rows = []
    with open('responses.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['ticket_id'] == ticket_id:
                row['status'] = new_status
            rows.append(row)

    # Write updated data back to CSV
    with open('responses.csv', 'w', newline='') as csvfile:
        fieldnames = ['ticket_id', 'name', 'employee_id', 'issue_type', 'machine_details', 'timestamp', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run()
