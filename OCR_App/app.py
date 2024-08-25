from flask import Flask, render_template, request, redirect, flash, session, url_for
import mysql.connector
import pandas as pd
from datetime import datetime
import random
import smtplib
from email.mime.text import MIMEText


import smtplib
import getpass


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def send_otp_email(to_email, otp):
    try:
        smtp_server = 'Email.outlook.com'  # Update with your SMTP server
        smtp_port = 587  # Update if different
        smtp_user = 'numberplate22@outlook.com'  # Update with your email
        smtp_password = 'Your_Password'

        # Construct the email message
        subject = 'Password Reset OTP'
        body = f"Your OTP for password reset is {otp}"
        message = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, message)
        
        print("OTP sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        company_id = request.form['company_id']
        
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="numberplate"
            )
            cursor = connection.cursor()
            select_query = "SELECT email_id FROM company_master WHERE company_id=%s"
            cursor.execute(select_query, (company_id,))
            result = cursor.fetchone()
            
            if result:
                email = result[0]
                otp = random.randint(100000, 999999)
                session['otp'] = otp
                session['company_id'] = company_id
                send_otp_email(email, otp)
                return redirect(url_for('reset_password'))
            else:
                flash('Company ID not found', 'error')
        except mysql.connector.Error as error:
            flash(f"MySQL Error: {error}", 'error')
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        new_password = request.form['new_password']

        if int(entered_otp) == session.get('otp'):
            company_id = session.get('company_id')
            
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="1234",
                    database="numberplate"
                )
                cursor = connection.cursor()
                update_query = "UPDATE company_master SET password=%s WHERE company_id=%s"
                cursor.execute(update_query, (new_password, company_id))
                connection.commit()
                flash('Password reset successfully', 'success')
                return redirect('/')
            except mysql.connector.Error as error:
                flash(f"MySQL Error: {error}", 'error')
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            flash('Invalid OTP', 'error')

    return render_template('reset_password.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        company_id = request.form['company_id']
        password = request.form['password']

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="numberplate"
            )
            cursor = connection.cursor()
            select_query = "SELECT * FROM company_master WHERE company_id=%s AND password=%s"
            cursor.execute(select_query, (company_id, password))
            results = cursor.fetchall()

            if len(results) == 1:
                session['company_id'] = company_id
                return redirect(f'/main/{company_id}')
            else:
                flash('Invalid Login Credentials', 'error')
        except mysql.connector.Error as error:
            flash(f"MySQL Error: {error}", 'error')
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    return render_template('login.html')
@app.route('/main/<cid>', methods=['GET', 'POST'])
def main_page(cid):
    if 'company_id' not in session or session['company_id'] != cid:
        return redirect('/')

    company_name = ""
    plates = []
    search_query = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    active_tab = request.args.get('active_tab', 'add-details')  # Default to "Add Details"

    if request.method == 'POST':
        if 'search' in request.form:
            search_query = request.form['search']
            return redirect(f'/main/{cid}?search={search_query}&active_tab=manage-plates')
        elif 'add_user' in request.form:
            name = request.form['name']
            np = request.form['np']
            pno = request.form['pno']
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="1234",
                    database="numberplate"
                )
                cursor = connection.cursor()
                insert_query = "INSERT INTO numberplate (number_plate, name, companyid, date_added, phone_no) VALUES (%s, %s, %s, %s, %s)"
                current_date = datetime.now().date()
                cursor.execute(insert_query, (np, name, cid, current_date, pno))
                connection.commit()
                flash('Details added successfully', 'success')
            except mysql.connector.Error as error:
                flash(f"MySQL Error: {error}", 'error')
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
        elif 'bulk_upload' in request.form:
            file = request.files['upload_excel']
            try:
                df = pd.read_excel(file)
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="1234",
                    database="numberplate"
                )
                cursor = connection.cursor()
                for _, row in df.iterrows():
                    name = row['Name']
                    np = row['No. Plate']
                    pno = row['Phone No.']
                    insert_query = "INSERT INTO numberplate (number_plate, name, companyid, date_added, phone_no) VALUES (%s, %s, %s, %s, %s)"
                    current_date = datetime.now().date()
                    cursor.execute(insert_query, (np, name, cid, current_date, pno))
                connection.commit()
                flash('Bulk upload successful', 'success')
            except Exception as e:
                flash(f"Error during bulk upload: {e}", 'error')
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="numberplate"
        )
        cursor = connection.cursor()

        # Get company name
        company_name_query = "SELECT company_name FROM company_master WHERE company_id=%s"
        cursor.execute(company_name_query, (cid,))
        company_name = cursor.fetchone()[0]

        # Get number plates based on search query and pagination
        select_plates_query = """
            SELECT companyid, name, number_plate, phone_no, date_added
            FROM numberplate
            WHERE companyid=%s
              AND (number_plate LIKE %s OR name LIKE %s OR phone_no LIKE %s)
            LIMIT %s OFFSET %s
        """
        cursor.execute(select_plates_query, (cid, f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', per_page, offset))
        plates = cursor.fetchall()

        # Get total count for pagination
        count_query = "SELECT COUNT(*) FROM numberplate WHERE companyid=%s AND (number_plate LIKE %s OR name LIKE %s OR phone_no LIKE %s)"
        cursor.execute(count_query, (cid, f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        total_count = cursor.fetchone()[0]
        total_pages = (total_count + per_page - 1) // per_page

    except mysql.connector.Error as error:
        flash(f"MySQL Error: {error}", 'error')
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    return render_template(
        'main_page.html',
        company_name=company_name,
        cid=cid,
        plates=plates,
        search_query=search_query,
        page=page,
        total_pages=total_pages,
        active_tab=active_tab
    )


@app.route('/edit_plate/<plate_id>', methods=['GET', 'POST'])
def edit_plate(plate_id):
    if 'company_id' not in session:
        return redirect('/')

    plate_details = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="numberplate"
        )
        cursor = connection.cursor()

        # Fetch the current details of the number plate
        select_plate_query = "SELECT name, number_plate, phone_no FROM numberplate WHERE number_plate=%s"
        cursor.execute(select_plate_query, (plate_id,))
        plate_details = cursor.fetchone()

        if request.method == 'POST':
            name = request.form['name']
            np = request.form['np']
            pno = request.form['pno']

            # Update the number plate details
            update_query = "UPDATE numberplate SET name=%s, number_plate=%s, phone_no=%s WHERE number_plate=%s"
            cursor.execute(update_query, (name, np, pno, plate_id))
            connection.commit()
            flash('Plate details updated successfully', 'success')
            return redirect(url_for('main_page', cid=session['company_id']))

    except mysql.connector.Error as error:
        flash(f"MySQL Error: {error}", 'error')
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    return render_template('edit_plate.html', plate_details=plate_details)

@app.route('/delete_plate/<plate_id>', methods=['GET'])
def delete_plate(plate_id):
    if 'company_id' not in session:
        return redirect('/')

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="numberplate"
        )
        cursor = connection.cursor()

        delete_query = "DELETE FROM numberplate WHERE number_plate=%s"
        cursor.execute(delete_query, (plate_id,))
        connection.commit()
        flash('Plate deleted successfully', 'success')
    except mysql.connector.Error as error:
        flash(f"MySQL Error: {error}", 'error')
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    return redirect(url_for('main_page', cid=session['company_id']))

@app.route('/logout')
def logout():
    session.pop('company_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
