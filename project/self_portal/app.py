from flask import Flask, render_template, request, redirect, url_for, flash
import getpass
import pyotp
import re
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Replace with your AD server details
AD_SERVERS = {
    'domain1': {
        'server': 'ad_server_domain1',
        'base_dn': 'DC=domain1,DC=com'
    },
    'domain2': {
        'server': 'ad_server_domain2',
        'base_dn': 'DC=domain2,DC=com'
    },
    'domain3': {
        'server': 'ad_server_domain3',
        'base_dn': 'DC=domain3,DC=com'
    }
}

def authenticate_with_2fa(username, old_password, otp_code, domain):
    server_info = AD_SERVERS[domain]
    server = Server(server_info['server'], get_info=ALL)
    user_dn = f"CN={username},{server_info['base_dn']}"

    try:
        # Bind using old credentials
        conn = Connection(server, user=user_dn, password=old_password, auto_bind=True)

        # Verify OTP
        if verify_otp(username, otp_code):
            return True
        else:
            return False

    except Exception as e:
        return False
    finally:
        conn.unbind()

def verify_otp(username, otp_code):
    # Retrieve the shared secret for the user from the database
    totp_secret = get_totp_secret(username)
    if totp_secret:
        totp = pyotp.TOTP(totp_secret)
        return totp.verify(otp_code)
    return False

def get_totp_secret(username):
    # Dummy function to fetch TOTP secret from database, replace with your implementation
    # Example: return totp_secret_from_db
    return None

def change_password(username, old_password, new_password, domain):
    server_info = AD_SERVERS[domain]
    server = Server(server_info['server'], get_info=ALL)
    user_dn = f"CN={username},{server_info['base_dn']}"

    try:
        # Bind using old credentials
        conn = Connection(server, user=user_dn, password=old_password, auto_bind=True)

        # Change the password
        conn.extend.microsoft.modify_password(user_dn, new_password, old_password)
        
        if conn.result['result'] == 0:
            return True
        else:
            return False

    except Exception as e:
        return False
    finally:
        conn.unbind()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        old_password = request.form['old_password']
        otp_code = request.form['otp_code']
        domain = request.form['domain']

        if authenticate_with_2fa(username, old_password, otp_code, domain):
            return redirect(url_for('change_password', username=username, old_password=old_password, domain=domain))
        else:
            flash('Authentication failed.', 'error')

    return render_template('login.html')

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        domain = request.form['domain']

        if not is_valid_password(new_password):
            flash('Password must contain at least 4 alphabets, 3 numbers, one symbol, and not exceed 10 characters.', 'error')
            return redirect(url_for('change_password'))

        if change_password(username, old_password, new_password, domain):
            return redirect(url_for('success'))
        else:
            return redirect(url_for('failed'))

    username = request.args.get('username')
    old_password = request.args.get('old_password')
    domain = request.args.get('domain')

    return render_template('change_password.html', username=username, old_password=old_password, domain=domain)

def is_valid_password(password):
    if len(password) > 10:
        return False

    if not re.search(r'[A-Za-z]{4,}', password):
        return False

    if not re.search(r'\d{3,}', password):
        return False

    if not re.search(r'[!@#$%^&*()_+}{":?><,./;\'\[\]]', password):
        return False

    return True

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failed')
def failed():
    return render_template('failed.html')

if __name__ == '__main__':
    app.run(debug=True)
