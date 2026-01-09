from flask import Flask,request,jsonify
import psycopg2

from psycopg2 import sql

app=Flask(__name__)



#database configuration
DB_HOST='localhost'
DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='1355'

def get_db_connection():
    connection=psycopg2.connect(
     host=DB_HOST,
     database=DB_NAME,
     user=DB_USER,
     password=DB_PASSWORD
    )
    return connection
def create_tb_if_not_exist():
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_db(
                student_id SERIAL PRIMARY KEY,
                studentname TEXT NOT NULL,
                rollno TEXT NOT NULL,
                email TEXT NOT NULL,
                coursename TEXT NOT NULL,
                coursecode TEXT NOT NULL
        );
    """)
    connection.commit()
    cursor.close()
    connection.close()
create_tb_if_not_exist()

@app.route("/student_register",methods=['POST'])
def student_register():
    studentname=request.json['studentname']
    rollno=request.json['rollno']
    email=request.json['email']
    coursename=request.json['coursename']
    coursecode=request.json['coursecode']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
        INSERT INTO student_db (studentname,rollno,email,coursename,coursecode)
        VALUES(%s,%s,%s,%s,%s)
    """, (studentname,rollno,email,coursename,coursecode))
    

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "student registered successfully"}),200
@app.route("/get_student", methods=['GET'])
def get_student():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM student_db;
    """)

    student_db = cursor.fetchall()
    cursor.close()
    connection.close()

    result = [
        {
            "studentname": user[0],
            "rollno":user[1],
            "course name": user[2],
            "email": user[3],
        }
        for user in student_db
    ]

    return jsonify(result), 200
@app.route('/student_update',methods=['PUT'])
def student_update():
    studentname=request.json['studentname']
    rollno=request.json['rollno']
    email=request.json['email']
    coursename=request.json['coursename']
    coursecode=request.json['coursecode']
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute( """
    UPDATE student_db
    SET studentname=%s,coursename=%s,email=%s,rollno=%s where student_id = %s;
    """,(studentname,rollno,email,coursename,coursecode))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message':'student update successfully'}),200
@app.route('/delete_user',methods=['DELETE'])
def delete_student():
    student_id=request.args.get('student_id')
    connection=get_db_connection()
    cursor=connection.cursor()
    cursor.execute("""
    DELETE FROM student_db WHERE student_id=%s;
    """,(student_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"student deleted successfully"}),200
    
if __name__ =='__main__':
        app.run(debug=True)
