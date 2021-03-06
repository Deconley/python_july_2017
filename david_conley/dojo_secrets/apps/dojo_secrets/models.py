from __future__ import unicode_literals
from django.db import models
import bcrypt, re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def currentUser(self, request):
        id = request.session['user_id']

        return User.objects.get(id=id)
    def validateRegistration(self, form_data):
        errors = []
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('An email in valid email format is required.')
        else:
            reg_check = User.objects.filter(email = form_data['email'])
            if reg_check:
                errors.append('The email you are trying to create an account with has already been used.')
        if len(form_data['first_name']) < 2:
            errors.append("First Name is required.")
        if len(form_data['last_name']) < 2:
            errors.append("Last Name is required.")
        if len(form_data['email']) == 0:
            errors.append("Email is required.")
        if len(form_data['password']) < 8:
            errors.append("Password is required.")
        if form_data['password'] != form_data['password_confirmation']:
            errors.append("Passwords do not match.")

        return errors

    def validateLogin(self, form_data):
            errors = []

            user = User.objects.filter(email = form_data['email']).first()
            if len(form_data['email']) == 0:
                    errors.append("Email is required.")
            if len(form_data['password']) == 0:
                errors.append('Password is required.')
            # if user ==[]:
            #     errors.append("Account does not exist. Please register first.")

            return errors

    def createUser(self, form_data):
        password = str(form_data['password'])
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        user = User.objects.create(
            first_name = form_data['first_name'],
            last_name = form_data['last_name'],
            email = form_data['email'],
            password = hashed_pw,
            )
        return user
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    friends = models.ManyToManyField('self', related_name="friend_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
# class Friend(models.Model):
#     user = models.ForeignKey(User)
#     friend = models.ForeignKey(User)
