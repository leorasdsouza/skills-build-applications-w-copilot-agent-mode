from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient()
        db = client[settings.DATABASES['default']['NAME']]

        # Clear existing data directly in MongoDB
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activity.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create users
        users = [
            User(email='user1@example.com', name='User One', password='password1'),
            User(email='user2@example.com', name='User Two', password='password2'),
            User(email='user3@example.com', name='User Three', password='password3'),
        ]

        # Save users to the database individually to ensure primary keys are assigned
        for user in users:
            user.save()

        # Create teams
        team1 = Team(name='Team Alpha')
        team1.save()
        team1.members.add(users[0])
        team1.members.add(users[1])

        team2 = Team(name='Team Beta')
        team2.save()
        team2.members.add(users[2])

        # Create activities
        activities = [
            Activity(user=users[0], type='Running', duration=30, date='2025-04-08'),
            Activity(user=users[1], type='Cycling', duration=60, date='2025-04-07'),
            Activity(user=users[2], type='Swimming', duration=45, date='2025-04-06'),
        ]

# Save activities individually
        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=team1, points=100),
            Leaderboard(team=team2, points=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Morning Run', description='A 5km run to start the day'),
            Workout(name='Evening Swim', description='A relaxing swim session'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
