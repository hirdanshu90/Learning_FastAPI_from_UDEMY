from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

# Convert Book to a Pydantic Model
class Book(BaseModel):
    id: Optional[int]
    title: str
    author: str
    description: str
    rating: int
    published_date: int



class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    class Config:
        schema_extra = {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }


# In-memory list to hold book data
BOOKS = [
    Book(id=1, title='Computer Science Pro', author='codingwithroby', description='A very nice book!', rating=5, published_date=2030),
    Book(id=2, title='Be Fast with FastAPI', author='codingwithroby', description='A great book!', rating=5, published_date=2030),
    Book(id=3, title='Master Endpoints', author='codingwithroby', description='A awesome book!', rating=5, published_date=2029),
    Book(id=4, title='HP1', author='Author 1', description='Book Description', rating=2, published_date=2028),
    Book(id=5, title='HP2', author='Author 2', description='Book Description', rating=3, published_date=2027),
    Book(id=6, title='HP3', author='Author 3', description='Book Description', rating=1, published_date=2026)
]

# Get all books
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS




# Get a book by ID
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')

# Get books by rating
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = [book for book in BOOKS if book.rating == book_rating]
    return books_to_return

# Get books by publish date
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = [book for book in BOOKS if book.published_date == published_date]
    return books_to_return





# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////


# Create a new book
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book)) 
    return new_book


# Helper to find book ID
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Update a book
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = book_request
            return
    raise HTTPException(status_code=404, detail='Item not found')

# Delete a book
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return
    raise HTTPException(status_code=404, detail='Item not found')
