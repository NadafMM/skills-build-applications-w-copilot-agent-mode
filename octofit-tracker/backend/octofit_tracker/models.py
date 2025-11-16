from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    team = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    members = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    calories = models.IntegerField()
    date = models.DateField()
    team = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activities'
    
    def __str__(self):
        return f"{self.user_name} - {self.activity_type}"


class Leaderboard(models.Model):
    team_name = models.CharField(max_length=200)
    total_calories = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['-total_calories']
    
    def __str__(self):
        return f"{self.team_name} - Rank {self.rank}"


class Workout(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()  # in minutes
    calories_per_session = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    recommended_for = models.JSONField(default=list)
    
    class Meta:
        db_table = 'workouts'
    
    def __str__(self):
        return self.name
