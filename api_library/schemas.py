from ninja import Schema
from datetime import date, datetime
from typing import List, Optional

# Author Schema
class AuthorSchemaIn(Schema):
    name: str
    birth_date: Optional[date] = None

class AuthorSchemaOut(Schema):
    id: int
    name: str
    birth_date: Optional[date] = None
    
    class Config:
        from_attributes = True  # versión moderna de orm_mode

# Publisher Schema
class PublisherSchemaIn(Schema):
    name: str
    address: str
    email: str
    website: str
    phone: str

class PublisherSchemaOut(Schema):
    id: int
    name: str
    address: str
    email: str
    website: str
    phone: str
    
    class Config:
        from_attributes = True

# Genre Schema
class GenreSchemaIn(Schema):
    name: str
    description: str

class GenreSchemaOut(Schema):
    id: int
    name: str
    description: str
    
    class Config:
        from_attributes = True

# Book Schema
class BookSchemaIn(Schema):
    title: str
    author_id: int
    stock: int
    price: float
    isbn: str
    image_url: Optional[str] = None
    # Si usaste ManyToMany en el modelo:
    publisher_ids: Optional[List[int]] = None
    genre_ids: Optional[List[int]] = None

class BookSchemaOut(Schema):
    id: int
    title: str
    author_id: int
    stock: int
    price: float
    isbn: str
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True

# Book Detail Schema (para incluir relaciones)
class BookDetailSchema(BookSchemaOut):
    author: AuthorSchemaOut
    publishers: List[PublisherSchemaOut] = []
    genres: List[GenreSchemaOut] = []
    
    class Config:
        from_attributes = True

# Review Schema
class ReviewSchemaIn(Schema):
    review: str
    rating: int
    book_id: int  # Adaptado a la revisión del modelo

class ReviewSchemaOut(Schema):
    id: int
    review: str
    rating: int
    user_id: int
    book_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Sale Schema
class SaleSchemaIn(Schema):
    status: str = "pending"  # valor por defecto

class SaleSchemaOut(Schema):
    id: int
    user_id: int
    created_at: date
    total: float
    status: str
    
    class Config:
        from_attributes = True

# BookSale Schema
class BookSaleSchemaIn(Schema):
    book_id: int
    sale_id: int
    book_quantity: int = 1
    discount: float = 0.0
    subtotal: float

class BookSaleSchemaOut(Schema):
    id: int
    book_id: int
    sale_id: int
    book_quantity: int
    discount: float
    subtotal: float
    
    class Config:
        from_attributes = True