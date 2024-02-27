import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='' 
    )
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version", db_info)
        cursor = connection.cursor()
     
        cursor.execute("CREATE DATABASE IF NOT EXISTS db_est")
        cursor.execute("USE db_est")
        create_table_query1 = """
        CREATE TABLE IF NOT EXISTS etudient (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            prenom VARCHAR(255) NOT NULL,
            niveau VARCHAR(255) NOT NULL
        )
        """
        create_table_query2 = """
        CREATE TABLE IF NOT EXISTS cours (
            code INT AUTO_INCREMENT PRIMARY KEY,
            nom_de_cours VARCHAR(255) NOT NULL,
            enseignement VARCHAR(255) NOT NULL
        )
        """
        create_table_query3 = """
        CREATE TABLE IF NOT EXISTS examen (
            code INT,
            id INT,
            note FLOAT,
            PRIMARY KEY (code, id),
            FOREIGN KEY (code) REFERENCES cours(code),
            FOREIGN KEY (id) REFERENCES etudient(id)
        )
        """
        # Execute the create table queries
        cursor.execute(create_table_query1)
        cursor.execute(create_table_query2)
        cursor.execute(create_table_query3)
        try:
            cursor = connection.cursor()
            insert_etudient_query = """
            INSERT INTO etudient (nom, prenom, niveau) VALUES (%s, %s, %s)
            """
            etudient_data = [
            ('kamal', 'essaih', 'Licence 1'),
            ('mouad', 'khatbi', 'Licence 2'),
            ('amir', 'karboubi', 'Master 1'),
            ('ali', 'bahri', 'Licence 1'),
            ('reda', 'aloui', 'Licence 2'),
            ('amin', 'aaloini', 'Master 1'),
            ('souad', 'fridi', 'Licence 1'),
            ('sanae', 'rouichk', 'Licence 2'),
            ('adul', 'bouhmidi', 'Master 1'),
            ('zakariya', 'mouridi', 'Licence 1'),
            ('ayoub', 'khalidi', 'Licence 2'),
            ('mouna', 'zaimi', 'Master 1'),
                            ]
            cursor.executemany(insert_etudient_query, etudient_data)
            connection.commit()
            print(cursor.rowcount, "rows inserted into etudient table.")
           

        except Error as e:
                          print("Failed to insert data into etudient table", e)
        try:
                insert_cours_query = """
                INSERT INTO cours (nom_de_cours, enseignement) VALUES (%s, %s)
                 """
                cours_data = [
                  
                   ('python', 'Dr. laroussi'),
                   ('web', 'Dr. toumi'),
                   ('DATAbase', 'Prof. abatal'),
                             ]
                
                cursor.executemany(insert_cours_query, cours_data)
                connection.commit()
                print(cursor.rowcount, "rows inserted into cours table.")
        except Error as e:
                print("Failed to insert data into cours table", e)
        try:
            insert_examen_query = """
            INSERT INTO examen (code, id, note) VALUES (%s, %s, %s)
            """
            examen_data = [
             (1, 1, 10.0),  
             (2, 1, 16.0), 
             (3, 1, 11.0),

             (1, 2, 12.0),  
             (2, 2, 18.0), 
             (3, 2, 15.0),

             (1, 3, 12.0),  
             (2, 3, 14.0), 
             (3, 3, 17.0),

             (1, 4, 11.0),  
             (2, 4, 16.0), 
             (3, 4, 19.0),

             (1, 5, 13.0),  
             (2, 5, 14.0), 
             (3, 5, 16.0),
                 
             (1, 6, 16.0),  
             (2, 6, 12.0), 
             (3, 6, 17.0),

             (1, 7, 15.0),  
             (2, 7, 15.0), 
             (3, 7, 18.0),

             (1, 8, 10.0),  
             (2, 8, 11.0), 
             (3, 8, 14.0),

             (1, 9, 14.0),  
             (2, 9, 18.0), 
             (3, 9, 19.0),

             (1, 10, 12.0),  
             (2, 10, 13.0), 
             (3, 10, 15.0),
                          ] 
            cursor.executemany(insert_examen_query, examen_data)
            connection.commit()
            print(cursor.rowcount, "rows inserted into examen table.")
        except Error as e:
             print("Failed to insert data into examen table", e)

except Error as e:
    print("Error while connecting to MySQL or creating the database", e)
finally:
    if connection.is_connected():
        cursor.close()  # Ensure the cursor is closed as well
        connection.close()
        print("MySQL connection is closed")
