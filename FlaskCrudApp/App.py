from flask import Flask , render_template, request, redirect, url_for, flash
from sql_connection import get_sql_connection

app=Flask(__name__)
app.secret_key="flash message"

connection=get_sql_connection()


@app.route('/')
def Index():
    # Fetch data from MYSQL to pass to HTML table insha2allah
    cursor=connection.cursor()
    cursor.execute("Select * FROM students.students")
    data=cursor.fetchall()
    cursor.close()
    return render_template('index.html', students=data)

@app.route('/insert',methods=['POST'])
def insert():
    if request.method=="POST":
        flash("Data Inserted Successfully!")
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cursor=connection.cursor()
        cursor.execute("INSERT INTO students.students (name,email,phone) Values (%s,%s,%s)",(name,email,phone))
        connection.commit()
        return redirect(url_for('Index'))

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method=='POST':
        id_data= request.form['id']
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cursor=connection.cursor()
        cursor.execute("UPDATE students.students SET name=%s,email=%s,phone=%s WHERE id=%s",(name,email,phone,id_data))
        flash("Data Updated Successfully")
        connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>',methods=['POST','GET'])
def delete(id_data):
    
    cursor=connection.cursor()
    cursor.execute("DELETE FROM `students`.`students` WHERE id = %s",(id_data,))
    flash("Data Deleted Successfully")
    connection.commit()
    return redirect(url_for('Index'))


if __name__=="__main__":
    app.run(debug=True)

