from django.test import TestCase
from .models import User, Team, Activity, Leaderboard, Workout

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(name='Test', email='test@example.com', password='pass')
        self.assertEqual(user.name, 'Test')
        self.assertEqual(user.email, 'test@example.com')

class TeamModelTest(TestCase):
    def test_create_team(self):
        team = Team.objects.create(name='Test Team', description='desc', members=[])
        self.assertEqual(team.name, 'Test Team')

class ActivityModelTest(TestCase):
    def test_create_activity(self):
        activity = Activity.objects.create(user_id=1, user_name='Test', activity_type='Running', duration=30, calories=300, date='2025-01-01', team='Test Team')
        self.assertEqual(activity.activity_type, 'Running')

class LeaderboardModelTest(TestCase):
    def test_create_leaderboard(self):
        lb = Leaderboard.objects.create(team_name='Test Team', total_calories=1000, total_activities=10, rank=1)
        self.assertEqual(lb.rank, 1)

class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        workout = Workout.objects.create(name='Test Workout', category='Strength', description='desc', duration=60, calories_per_session=500, difficulty='Intermediate', recommended_for=['Test Team'])
        self.assertEqual(workout.name, 'Test Workout')
