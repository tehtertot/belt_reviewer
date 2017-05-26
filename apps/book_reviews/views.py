# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Book, Author, BookReview, User
from django.contrib import messages

def index(request):
    context = { 'reviews': BookReview.objects.getMostRecentReviews(),
                'books': Book.objects.getBooksWithReviews() }
    return render(request, 'book_reviews/index.html', context)

def addBook(request):
    if request.method == "POST":
        if request.POST['author1'] == 0 or request.POST['author1'] == "":
            authorexists = False
            author = request.POST['author2']
        else:
            authorexists = True
            author = request.POST['author1']
        postData = { 'user': request.session['user_id'],
                     'title': request.POST['title'],
                     'authorexists': authorexists,
                     'author': author,
                     'review': request.POST['review'],
                     'rating': request.POST['rating'] }
        review = BookReview.objects.addBookAndReview(postData)
        if not isinstance(review, BookReview):
            messages.add_message(request, messages.ERROR, review)
            return redirect('books:add')
        return redirect('books:index')
    elif request.method == "GET":
        context = { 'authors': Author.objects.all() }
        return render(request, 'book_reviews/add.html', context)

def viewBook(request, id):
    context = { 'book': Book.objects.get(id=id) }
    return render(request, 'book_reviews/book.html', context)

def addReview(request, id):
    if request.method == "POST":
        postData = { 'user': request.session['user_id'],
                     'book_id': id,
                     'review': request.POST['review'],
                     'rating': request.POST['rating'] }
        review = BookReview.objects.addReview(postData)
        if not isinstance(review, BookReview):
            messages.add_message(request, messages.ERROR, review)
            return redirect('books:book', id=id)
        return redirect('books:index')

def viewUser(request, id):
    context = { 'user': User.objects.get(id=id) }
    return render(request, 'book_reviews/user.html', context)

def deleteReview(request, id):
    try:
        if request.method == "GET":
            context = { 'review': BookReview.objects.get(id=id) }
            if request.session['user_id'] != context['review'].user.id:
                return render(request, 'book_reviews/denyaccess.html')
            else:
                return render(request, 'book_reviews/delete.html', context)
        elif request.method == "POST":
            BookReview.objects.get(id=id).delete()
            return redirect('books:index')
    except:
        return render(request, 'book_reviews/denyaccess.html')
