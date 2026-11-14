#Make another file and paste                                                        
import sqlite3
import csv

# Connect to your attendance database
conn = sqlite3.connect('attendance.db')  # Change path if needed
cursor = conn.cursor()

# Fetch all records
cursor.execute("SELECT * FROM attendance")
rows = cursor.fetchall()

# Export to CSV
with open("attendance.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "Name", "Date", "Time"])  # Header row
    writer.writerows(rows)

conn.close()
print("Attendance exported to attendance.csv")