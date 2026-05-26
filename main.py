from fastapi import FastAPI, HTTPException
import psycopg2

from models import Book, PatchBook

app = FastAPI()

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="sheikh456"
)

cursor = conn.cursor()


# HOME
@app.get("/")
def home():
    return {"message": "Library Management System"}


# ADD BOOK
@app.post("/books")
def add_book(book: Book):

    cursor.execute(
        "INSERT INTO books (id, title, author, genre, year) VALUES (%s, %s, %s, %s, %s)",
        (book.id, book.title, book.author, book.genre, book.year)
    )

    conn.commit()

    return {"message": "Book added successfully"}


# GET ALL BOOKS
@app.get("/books")
def get_books():

    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "genre": row[3],
            "year": row[4]
        })

    return result


# GET BOOK BY ID
@app.get("/books/{id}")
def get_book(id: int):

    cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "id": row[0],
        "title": row[1],
        "author": row[2],
        "genre": row[3],
        "year": row[4]
    }


# UPDATE BOOK (PUT)
@app.put("/books/{id}")
def update_book(id: int, book: Book):

    cursor.execute(
        """
        UPDATE books
        SET title=%s, author=%s, genre=%s, year=%s
        WHERE id=%s
        """,
        (book.title, book.author, book.genre, book.year, id)
    )

    conn.commit()

    return {"message": "Book updated successfully"}


# PATCH BOOK (PARTIAL UPDATE)
@app.patch("/books/{id}")
def patch_book(id: int, book: PatchBook):

    if book.title:
        cursor.execute("UPDATE books SET title=%s WHERE id=%s", (book.title, id))

    if book.author:
        cursor.execute("UPDATE books SET author=%s WHERE id=%s", (book.author, id))

    if book.genre:
        cursor.execute("UPDATE books SET genre=%s WHERE id=%s", (book.genre, id))

    if book.year:
        cursor.execute("UPDATE books SET year=%s WHERE id=%s", (book.year, id))

    conn.commit()

    return {"message": "Book partially updated"}


# DELETE BOOK
@app.delete("/books/{id}")
def delete_book(id: int):

    cursor.execute("DELETE FROM books WHERE id=%s", (id,))
    conn.commit()

    return {"message": "Book deleted successfully"}