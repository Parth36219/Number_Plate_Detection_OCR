from flask import Flask, render_template, request, redirect, flash, session, url_for
import mysql.connector
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    if request.method == 'POST':
        if 'add_user' in request.form:
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
                    name = row['name']
                    np = row['number_plate']
                    pno = row['phone_no']
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

        select_query = "SELECT company_name FROM company_master WHERE company_id=%s"
        cursor.execute(select_query, (cid,))
        company_name = cursor.fetchone()[0]

        select_plates_query = "SELECT companyid, name, number_plate, phone_no, date_added FROM numberplate WHERE companyid=%s"
        cursor.execute(select_plates_query, (cid,))
        plates = cursor.fetchall()

    except mysql.connector.Error as error:
        flash(f"MySQL Error: {error}", 'error')
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

    return render_template('main_page.html', company_name=company_name, cid=cid, plates=plates)

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
