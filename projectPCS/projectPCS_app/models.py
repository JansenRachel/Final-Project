from django.db import models
import re

#   VALIDATORS
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['firstname']) < 2:
            errors['first_name'] = "Your name must contain letters only and be at least 2 characters in length."
        
        if len(postData['lastname']) < 2:
            errors['last_name'] = "Your name must contain letters only and be at least 2 characters in length."
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_match'] = ("Invalid email address")
        
        email_check = self.filter(email=postData['email'])
        if email_check:
            errors['email_unique'] = "Email already exists"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        
        if postData['password'] != postData['confirmPw']:
            errors['password_match'] = "Check that your passwords match"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_match'] = ("Invalid email address")
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        return errors

    def edit_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['firstname']) < 2:
            errors['first_name'] = "Your name must contain letters only and be at least 2 characters in length."
        
        if len(postData['lastname']) < 2:
            errors['last_name'] = "Your name must contain letters only and be at least 2 characters in length."
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_match'] = ("Invalid email address")
        return errors

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if len(postData['postContent']) < 9:
            errors['messagePost'] = "Please submit a message that is at least 10 characters."
        return errors



#   MODELS
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # move_info = list of moving data per user
    # messages = list of messages user posted
    # comments = list of comments user posted

class Move_Info(models.Model):
    user_moving = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)
    orig_address = models.CharField(max_length=255)
    orig_citybase = models.CharField(max_length=255)
    orig_state = models.CharField(max_length=255)
    dest_address = models.CharField(max_length=255)
    dest_citybase = models.CharField(max_length=255)
    dest_state = models.CharField(max_length=255)
    upload = models.FileField(upload_to=None, max_length=255, null=True)
    move_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

# class Upload(models.Model):
    # move_upload = models.ForeignKey
#     upload = models.FileField(upload_to=None, max_length=255, null=True)
    


class Message(models.Model):
    poster = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comment(models.Model):
    comment_content = models.TextField()
    poster = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name= "comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


