from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Principal tables
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    
    def __str__(self):
        return f"{self.name}-{self.birth_date}"
    
class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    website = models.URLField()
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.name}-{self.address}-{self.email}"
    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name}"
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publishers = models.ManyToManyField(Publisher, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    isbn = models.CharField(max_length=13, unique=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}-{self.author.name}-{self.isbn}"
    
class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.book.title} - {self.rating}/5 - {self.user.username}"
    
class Sale(models.Model):
    STATUS_CHOICES = [
        ("completed", "Completed"), 
        ("pending", "Pending"), 
        ("canceled", "Canceled")
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    created_at = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at} - {self.total}"
    
class BookSale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sales_items")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    book_quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.book.title} - {self.sale.id} - {self.book_quantity}"