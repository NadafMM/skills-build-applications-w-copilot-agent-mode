from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared!'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes united to protect the world',
            members=[]
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League defenders of truth and justice',
            members=[]
        )
        
        self.stdout.write(self.style.SUCCESS('Teams created!'))
        
        # Create Users (Superheroes)
        self.stdout.write('Creating users...')
        
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com', 'team': 'Team Marvel'},
        ]
        
        dc_heroes = [
            {'name': 'Superman', 'email': 'clark.kent@dc.com', 'team': 'Team DC'},
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com', 'team': 'Team DC'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com', 'team': 'Team DC'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com', 'team': 'Team DC'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com', 'team': 'Team DC'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com', 'team': 'Team DC'},
        ]
        
        all_heroes = marvel_heroes + dc_heroes
        users = []
        
        for hero in all_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                password=make_password('password123'),
                team=hero['team']
            )
            users.append(user)
        
        # Update team members
        team_marvel.members = [u.id for u in users if u.team == 'Team Marvel']
        team_marvel.save()
        
        team_dc.members = [u.id for u in users if u.team == 'Team DC']
        team_dc.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users!'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'HIIT']
        activities = []
        
        for user in users:
            # Create 5-10 activities per user
            for _ in range(random.randint(5, 10)):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                calories = duration * random.randint(5, 12)
                days_ago = random.randint(0, 30)
                
                activity = Activity.objects.create(
                    user_id=user.id,
                    user_name=user.name,
                    activity_type=activity_type,
                    duration=duration,
                    calories=calories,
                    date=date.today() - timedelta(days=days_ago),
                    team=user.team
                )
                activities.append(activity)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(activities)} activities!'))
        
        # Create Leaderboard
        self.stdout.write('Creating leaderboard...')
        
        marvel_calories = sum(a.calories for a in activities if a.team == 'Team Marvel')
        marvel_count = len([a for a in activities if a.team == 'Team Marvel'])
        
        dc_calories = sum(a.calories for a in activities if a.team == 'Team DC')
        dc_count = len([a for a in activities if a.team == 'Team DC'])
        
        if marvel_calories > dc_calories:
            Leaderboard.objects.create(
                team_name='Team Marvel',
                total_calories=marvel_calories,
                total_activities=marvel_count,
                rank=1
            )
            Leaderboard.objects.create(
                team_name='Team DC',
                total_calories=dc_calories,
                total_activities=dc_count,
                rank=2
            )
        else:
            Leaderboard.objects.create(
                team_name='Team DC',
                total_calories=dc_calories,
                total_activities=dc_count,
                rank=1
            )
            Leaderboard.objects.create(
                team_name='Team Marvel',
                total_calories=marvel_calories,
                total_activities=marvel_count,
                rank=2
            )
        
        self.stdout.write(self.style.SUCCESS('Leaderboard created!'))
        
        # Create Workouts
        self.stdout.write('Creating workouts...')
        
        workouts_data = [
            {
                'name': 'Super Soldier Training',
                'category': 'Strength',
                'description': 'Intense full-body strength training inspired by Captain America',
                'duration': 60,
                'calories_per_session': 500,
                'difficulty': 'Advanced',
                'recommended_for': ['Team Marvel', 'Team DC']
            },
            {
                'name': 'Speed Force Cardio',
                'category': 'Cardio',
                'description': 'High-intensity interval training for maximum speed',
                'duration': 45,
                'calories_per_session': 600,
                'difficulty': 'Intermediate',
                'recommended_for': ['Team DC']
            },
            {
                'name': 'Asgardian Power Lift',
                'category': 'Strength',
                'description': 'Heavy lifting routine worthy of Thor',
                'duration': 90,
                'calories_per_session': 700,
                'difficulty': 'Advanced',
                'recommended_for': ['Team Marvel']
            },
            {
                'name': 'Web-Slinger Agility',
                'category': 'Flexibility',
                'description': 'Improve flexibility and agility like Spider-Man',
                'duration': 30,
                'calories_per_session': 250,
                'difficulty': 'Beginner',
                'recommended_for': ['Team Marvel', 'Team DC']
            },
            {
                'name': 'Bat-Cave Circuit',
                'category': 'HIIT',
                'description': 'Batman\'s legendary training circuit',
                'duration': 75,
                'calories_per_session': 650,
                'difficulty': 'Advanced',
                'recommended_for': ['Team DC']
            },
            {
                'name': 'Widow\'s Core Workout',
                'category': 'Core',
                'description': 'Core strengthening routine from Black Widow',
                'duration': 40,
                'calories_per_session': 350,
                'difficulty': 'Intermediate',
                'recommended_for': ['Team Marvel', 'Team DC']
            },
            {
                'name': 'Hulk Smash HIIT',
                'category': 'HIIT',
                'description': 'Explosive high-intensity workout',
                'duration': 30,
                'calories_per_session': 450,
                'difficulty': 'Advanced',
                'recommended_for': ['Team Marvel']
            },
            {
                'name': 'Wonder Yoga',
                'category': 'Yoga',
                'description': 'Calming yet powerful yoga session',
                'duration': 60,
                'calories_per_session': 300,
                'difficulty': 'Beginner',
                'recommended_for': ['Team DC', 'Team Marvel']
            }
        ]
        
        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts_data)} workouts!'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
