####
# Script to fake book data and user data. Only used once for the DB.
# - CLY 11-03-2024 -
####
# Imports
import os
import sqlite3
from faker import Faker
import random
import datetime


# Definiton of allowed genres
allowed_genres = ['Fiction', 'Non-Fiction', 'Science Fiction', 'Mystery', 'Thriller', 'Romance', 'Fantasy', 'Biography', 'History']


# Function to generate fake user data
def generate_user(fake):
    username = fake.user_name()
    name = fake.name()
    address = fake.address()
    password = fake.password()
    return username, password, name, address

# Function to insert user data into the database
def insert_users(conn, cursor, num_users):
    fake = Faker()
    for _ in range(num_users):
        creation_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_date = creation_date
        user_data = generate_user(fake)
        cursor.execute("INSERT INTO users (username, password, name, address, lastUpdated) VALUES (?, ?, ?, ?, ?)", (*user_data, updated_date))
    conn.commit()
    print(f"{num_users} users inserted successfully.")


# Function to generate fake book data
def generate_book(fake):
    title = fake.catch_phrase()
    author = fake.name()
    genre = random.choice(allowed_genres)
    publication_year = fake.random_int(min=1900, max=2022)
    description = fake.text()
    return title, author, genre, publication_year, description

# Function to insert book data into the database
def insert_books(conn, cursor, num_books):
    fake = Faker()
    for _ in range(num_books):
        book_data = generate_book(fake)
        creation_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_date = creation_date
        cursor.execute("INSERT INTO books (title, author, genre, publicationYear, description, creationDate, updatedDate) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (*book_data, creation_date, updated_date))
    conn.commit()
    print(f"{num_books} books inserted successfully.")

# Connect to SQLite database
db_path = "C:/Users/KOM/Documents/Uge 6 - Case 1 - Niveau 2/LibrarySystem/LibraryDB.sqlite3"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Number of users and books to generate and insert
num_users = 9
num_books = 200

# Insert fake users and books into the database
insert_users(conn, cursor, num_users)
insert_books(conn, cursor, num_books)

# Close database connection
conn.close()
