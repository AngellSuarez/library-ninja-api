from ninja import NinjaAPI
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .schemas import *
from .models import *

api = NinjaAPI()

# -----------------Author CRUD-------------------
@api.post("/authors/", response=AuthorSchemaOut)
def create_author(request, payload: AuthorSchemaIn):
    author_obj = Author.objects.create(**payload.dict())
    return author_obj

@api.get("/authors/", response=List[AuthorSchemaOut])
def get_authors(request):
    authors = Author.objects.all()
    return authors

@api.get("/authors/{author_id}", response=AuthorSchemaOut)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return author

@api.put("/authors/{author_id}", response=AuthorSchemaOut)
def update_author(request, author_id: int, payload: AuthorSchemaIn):
    author_obj = get_object_or_404(Author, id=author_id)
    for attr, value in payload.dict().items():
        setattr(author_obj, attr, value)
    author_obj.save()
    return author_obj

@api.delete("/authors/{author_id}")
def delete_author(request, author_id: int):
    author_obj = get_object_or_404(Author, id=author_id)
    author_obj.delete()
    return {"success": True}

# -----------------Publisher Crud -------------------
@api.post("/publishers/", response=PublisherSchemaOut)
def create_publisher(request, payload: PublisherSchemaIn):
    publisher_obj = Publisher.objects.create(**payload.dict())
    return publisher_obj

@api.get("/publishers/", response=List[PublisherSchemaOut])
def get_publishers(request):
    publishers = Publisher.objects.all()
    return publishers

@api.get("/publishers/{publisher_id}", response=PublisherSchemaOut)
def get_publisher(request, publisher_id: int):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    return publisher

@api.put("/publishers/{publisher_id}", response=PublisherSchemaOut)
def update_publisher(request, publisher_id: int, payload: PublisherSchemaIn):
    publisher_obj = get_object_or_404(Publisher, id=publisher_id)
    for attr, value in payload.dict().items():
        setattr(publisher_obj, attr, value)
    publisher_obj.save()
    return publisher_obj

@api.delete("/publishers/{publisher_id}")
def delete_publisher(request, publisher_id: int):
    publisher_obj = get_object_or_404(Publisher, id=publisher_id)
    publisher_obj.delete()
    return {"success": True}

# -----------------Genre CRUD ------------------------
@api.post("/genres/", response=GenreSchemaOut)
def create_genre(request, payload: GenreSchemaIn):
    genre_obj = Genre.objects.create(**payload.dict())
    return genre_obj

@api.get("/genres/", response=List[GenreSchemaOut])
def get_genres(request):
    genres = Genre.objects.all()
    return genres

@api.get("/genres/{genre_id}", response=GenreSchemaOut)
def get_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    return genre

@api.put("/genres/{genre_id}", response=GenreSchemaOut)
def update_genre(request, genre_id: int, payload: GenreSchemaIn):
    genre_obj = get_object_or_404(Genre, id=genre_id)
    for attr, value in payload.dict().items():
        setattr(genre_obj, attr, value)
    genre_obj.save()
    return genre_obj

@api.delete("/genres/{genre_id}")
def delete_genre(request, genre_id: int):
    genre_obj = get_object_or_404(Genre, id=genre_id)
    genre_obj.delete()
    return {"success": True}

# -----------------Book CRUD ------------------------
@api.post("/books/", response=BookSchemaOut)
def create_book(request, payload: BookSchemaIn):
    data = payload.dict()  # guardar una sola vez

    publisher_ids = data.pop("publisher_ids", [])
    genre_ids = data.pop("genre_ids", [])

    # Ahora data tiene solo los campos correctos
    book_obj = Book.objects.create(**data)

    # Luego seteas las relaciones ManyToMany
    if publisher_ids:
        book_obj.publishers.set(publisher_ids)
    if genre_ids:
        book_obj.genres.set(genre_ids)

    return book_obj


@api.get("/books/", response=List[BookSchemaOut])
def get_books(request,
              genre_id: Optional[int] = None,
              author_id: Optional[int] = None,
              publisher_id: Optional[int] = None):
    books = Book.objects.all()
    
    if genre_id:
        books = books.filter(genres__id=genre_id)
    
    if publisher_id:
        books = books.filter(publishers__id=publisher_id)
        
    if author_id:
        books = books.filter(author_id=author_id)
    
    return books

@api.get("/books/{book_id}", response=BookDetailSchema)  # Usando el schema de detalle
def get_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    return book

@api.put("/books/{book_id}", response=BookSchemaOut)
def update_book(request, book_id: int, payload: BookSchemaIn):
    book_obj = get_object_or_404(Book, id=book_id)
    
    # Extraer los IDs de publishers y genres
    publisher_ids = payload.dict().pop("publisher_ids", None)
    genre_ids = payload.dict().pop("genre_ids", None)
    
    # Actualizar campos
    for attr, value in payload.dict().items():
        setattr(book_obj, attr, value)
    book_obj.save()
    
    # Actualizar publishers y genres
    if publisher_ids is not None:
        book_obj.publishers.set(publisher_ids)
    if genre_ids is not None:
        book_obj.genres.set(genre_ids)
    
    return book_obj

@api.delete("/books/{book_id}")
def delete_book(request, book_id: int):
    book_obj = get_object_or_404(Book, id=book_id)
    book_obj.delete()
    return {"success": True}

# ------------------Sales CRUD ------------------------
@api.post("/sales/", response=SaleSchemaOut)
def create_sale(request, payload: SaleSchemaIn):
    sale_obj = Sale.objects.create(**payload.dict())
    return sale_obj

@api.get("/sales/", response=List[SaleSchemaOut])
def get_sales(request, user_id: Optional[int] = None):
    sales = Sale.objects.all()
    
    if user_id:
        sales = sales.filter(user_id=user_id)
    return sales

@api.get("/sales/{sale_id}", response=SaleSchemaOut)
def get_sale(request, sale_id: int):
    sale = get_object_or_404(Sale, id=sale_id)
    return sale

@api.patch("/sales/{sale_id}", response=SaleSchemaOut)
def change_status_sale(request, sale_id: int, payload: SaleSchemaIn):
    sale_obj = get_object_or_404(Sale, id=sale_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(sale_obj, attr, value)
    sale_obj.save()
    return sale_obj

# ------------------Review CRUD -----------------------
@api.post("/reviews/", response=ReviewSchemaOut)
def create_review(request, payload: ReviewSchemaIn):
    review_obj = Review.objects.create(**payload.dict())
    return review_obj

@api.get("/reviews/", response=List[ReviewSchemaOut])
def get_reviews(request, book_id: Optional[int] = None):
    reviews = Review.objects.all()
    
    if book_id:
        reviews = reviews.filter(book_id=book_id)
    
    return reviews

@api.get("/reviews/{review_id}", response=ReviewSchemaOut)
def get_review(request, review_id: int):
    review = get_object_or_404(Review, id=review_id)
    return review

@api.put("/reviews/{review_id}", response=ReviewSchemaOut)
def update_review(request, review_id: int, payload: ReviewSchemaIn):
    review_obj = get_object_or_404(Review, id=review_id)
    for attr, value in payload.dict().items():
        setattr(review_obj, attr, value)
    review_obj.save()
    return review_obj

@api.delete("/reviews/{review_id}")
def delete_review(request, review_id: int):
    review_obj = get_object_or_404(Review, id=review_id)
    review_obj.delete()
    return {"success": True}

# ------------------BookSale CRUD -----------------------
@api.post("/book-sales/batch/", response=List[BookSaleSchemaOut])
def add_books_to_sale(request, payload: List[BookSaleSchemaIn]):
    book_sales_created = []
    
    for book_sale_data in payload:
        book_sale_obj = BookSale.objects.create(**book_sale_data.dict())
        book_sales_created.append(book_sale_obj)
    
    # Recalcular el total de la venta
    if book_sales_created:
        sale_id = book_sales_created[0].sale_id
        sale = get_object_or_404(Sale, id=sale_id)
        
        # Calcular el total basado en todos los items de la venta
        total = BookSale.objects.filter(sale_id=sale_id).aggregate(
            total=Sum('subtotal')
        )['total'] or 0
        
        sale.total = total
        sale.save()
    
    return book_sales_created

@api.get("/book-sales/{sale_id}", response=List[BookSaleSchemaOut])
def get_book_sales(request, sale_id: int):
    book_sales = BookSale.objects.filter(sale_id=sale_id)
    return book_sales