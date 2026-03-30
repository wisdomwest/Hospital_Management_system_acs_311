import mysql.connector


def connect_db():

    try:
        connection = mysql.connector.connect(
            # create db named hd and add correct user and password
            host="localhost",
            user="admin",
            password="",
            database="hd",
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: Could not connect to database. {err}")
        exit()


db = connect_db()
cursor = db.cursor()


def add_patient():
    print("\n--- Add New Patient ---")
    name = input("Enter name: ")
    try:
        age = int(input("Enter age: "))
    except ValueError:
        print("Invalid age. Please enter a number.")
        return

    gender = input("Enter gender: ")
    disease = input("Enter disease: ")

    sql = "INSERT INTO patients (name, age, gender, disease) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, age, gender, disease))
    db.commit()
    print("Patient added successfully!\n")


def search_patient():
    print("\n--- Search Patient ---")
    name = input("Enter name to search: ")
    cursor.execute("SELECT * FROM patients WHERE LOWER(name) = LOWER(%s)", (name,))
    result = cursor.fetchone()

    if result:
        print("Patient Found:", result)
    else:
        print("Patient not found.\n")


def update_patient():
    print("\n--- Update Patient ---")
    name = input("Enter name of patient to update: ")

    cursor.execute("SELECT * FROM patients WHERE LOWER(name) = LOWER(%s)", (name,))
    if cursor.fetchone():
        try:
            new_age = int(input("Enter new age: "))
            new_gender = input("Enter new gender: ")
            new_disease = input("Enter new disease: ")

            sql = "UPDATE patients SET age=%s, gender=%s, disease=%s WHERE name=%s"
            cursor.execute(sql, (new_age, new_gender, new_disease, name))
            db.commit()
            print("Patient updated successfully!\n")
        except ValueError:
            print("Invalid input. Update failed.\n")
    else:
        print("Patient not found.\n")


def delete_patient():
    print("\n--- Delete Patient ---")
    name = input("Enter name of patient to delete: ")

    cursor.execute("SELECT * FROM patients WHERE LOWER(name) = LOWER(%s)", (name,))
    if cursor.fetchone():
        confirm = input(f"Confirm delete for {name} (yes/no): ")
        if confirm.lower() == "yes":
            cursor.execute("DELETE FROM patients WHERE name=%s", (name,))
            db.commit()
            print("Patient deleted successfully!\n")
        else:
            print("Delete cancelled.\n")
    else:
        print("Patient not found.\n")


def main():
    while True:
        print("\n=== Hospital Management System ===")
        print("1. Add Patient")
        print("2. Search Patient")
        print("3. Update Patient")
        print("4. Delete Patient")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            search_patient()
        elif choice == "3":
            update_patient()
        elif choice == "4":
            delete_patient()
        elif choice == "5":
            print("Exiting system...")
            cursor.close()
            db.close()
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
