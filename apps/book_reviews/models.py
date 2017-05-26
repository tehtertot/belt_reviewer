# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from ..login_registration.models import User
from django.db.models import F

class BookReviewManager(models.Manager):
    def getMostRecentReviews(self):
        return BookReview.objects.order_by('-created_at')[:3]
    def addBookAndReview(self, postData):
        if postData['authorexists']:
            author = Author.objects.get(id=postData['author'])
        else:
            # check if author actually exists already
            try:
                author = Author.objects.get(name=postData['author'])
            except:
                author = Author.objects.create(name=postData['author'])
        #check if book exists already
        try:
            book = Book.objects.get(title=postData['title'])
            # error = "Did you mean {} by {}?".format(book.title, ", ".join(book.authors.all()))
            error = "This book is already in the system."
            return error
        except ObjectDoesNotExist:
            book = Book.objects.create(title=postData['title'])
            book.authors.add(author)
        # user = User.objects.get(id=postData['user'])
        # return BookReview.objects.create(book=book,review=postData['review'],user=user, rating=postData['rating'])
    def addReview(self, postData):
        book = Book.objects.get(id=postData['book_id'])
        user = User.objects.get(id=postData['user'])
        #see if user has already reviewed this book
        try:
            br = BookReview.objects.get(user=user, book=book)
            return "You already reviewed this book."
        except:
            return BookReview.objects.create(book=book, review=postData['review'], user=user, rating=postData['rating'])
    def getUserReviews(self, user_id):
        return BookReview.objects.filter(user=User.objects.get(id=user_id))

class BookManager(models.Manager):
    def getBooksWithReviews(self):
        return Book.objects.all()
    def getBookReviews(self, id):
        b = Book.objects.get(id=id)
        return b.reviews.all()
    def getAuthors(self, id):
        b = Book.objects.get(id=id)
        return b.authors.all()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class BookReview(models.Model):
    book = models.ForeignKey(Book, related_name="reviews")
    review = models.TextField()
    user = models.ForeignKey(User, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookReviewManager()
