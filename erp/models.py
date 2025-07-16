from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

class Role(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M','Male'),('F','Female')], blank=True)

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
