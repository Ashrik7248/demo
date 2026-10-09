import sqlite3
import sys

DB_FILE = "records.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def initialize_database():
    """Create the table if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_record():
    print("\n--- Create New Record ---")
    name = input("Enter Name: ").strip()
    category = input("Enter Category: ").strip()
    value = input("Enter Value/Details: ").strip()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (name, category, value) VALUES (?, ?, ?)", (name, category, value))
    conn.commit()
    conn.close()
    print("[+] Record added successfully!")

def read_records():
    print("\n--- All Records ---")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, value FROM records")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No records found.")
        return

    print(f"{'ID':<5} | {'Name':<20} | {'Category':<15} | {'Value'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<15} | {row[3]}")

def search_records():
    print("\n--- Search Records ---")
    keyword = input("Enter search term (Name or Category): ").strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, category, value FROM records 
        WHERE name LIKE ? OR category LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No matching records found.")
        return

    print(f"\n{'ID':<5} | {'Name':<20} | {'Category':<15} | {'Value'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<15} | {row[3]}")

def update_record():
    read_records()
    try:
        rec_id = int(input("\nEnter the ID of the record to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    print("Leave blank to keep existing value.")
    new_name = input("New Name: ").strip()
    new_category = input("New Category: ").strip()
    new_value = input("New Value: ").strip()

    conn = get_connection()
    cursor = conn.cursor()
    
    # Fetch existing record to retain old values if left blank
    cursor.execute("SELECT name, category, value FROM records WHERE id = ?", (rec_id,))
    existing = cursor.fetchone()
    if not existing:
        print("Record ID not found.")
        conn.close()
        return

    name = new_name if new_name else existing[0]
    category = new_category if new_category else existing[1]
    value = new_value if new_value else existing[2]

    cursor.execute("""
        UPDATE records 
        SET name = ?, category = ?, value = ? 
        WHERE id = ?
    """, (name, category, value, rec_id))
    conn.commit()
    conn.close()
    print("[+] Record updated successfully!")

def delete_record():
    read_records()
    try:
        rec_id = int(input("\nEnter the ID of the record to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (rec_id,))
    conn.commit()
    conn.close()
    print("[+] Record deleted successfully!")

def main():
    initialize_database()
    while True:
        print("\n=== CLI RECORD MANAGER ===")
        print("1. Create Record")
        print("2. Read / View All Records")
        print("3. Search Records")
        print("4. Update Record")
        print("5. Delete Record")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            create_record()
        elif choice == '2':
            read_records()
        elif choice == '3':
            search_records()
        elif choice == '4':
            update_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            print("Exiting Record Manager. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1 through 6.")

if __name__ == "__main__":
      main()
