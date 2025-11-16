#!/bin/bash

# OctoFit Tracker Database Setup Script

echo "=========================================="
echo "OctoFit Tracker Database Setup"
echo "=========================================="

# Navigate to workspace root
cd /workspaces/skills-build-applications-w-copilot-agent-mode

# Check if MongoDB is running
echo "Checking MongoDB service..."
if pgrep -x "mongod" > /dev/null; then
    echo "✓ MongoDB is running"
else
    echo "✗ MongoDB is not running"
    echo "Starting MongoDB..."
    sudo systemctl start mongod || mongod --fork --logpath /var/log/mongodb.log --dbpath /var/lib/mongodb
fi

# Activate virtual environment
echo "Activating virtual environment..."
source octofit-tracker/backend/venv/bin/activate

# Run makemigrations
echo "Running makemigrations..."
python octofit-tracker/backend/manage.py makemigrations

# Run migrate
echo "Running migrate..."
python octofit-tracker/backend/manage.py migrate

# Create unique index on email field
echo "Creating unique index on email field..."
mongosh octofit_db --eval 'db.users.createIndex({ "email": 1 }, { unique: true })'

# Populate database
echo "Populating database with test data..."
python octofit-tracker/backend/manage.py populate_db

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To verify the database, run:"
echo "  mongosh octofit_db --eval 'db.getCollectionNames()'"
echo ""
echo "To view sample data:"
echo "  mongosh octofit_db --eval 'db.users.find().limit(3)'"
echo "  mongosh octofit_db --eval 'db.teams.find()'"
echo "  mongosh octofit_db --eval 'db.activities.find().limit(3)'"
echo "  mongosh octofit_db --eval 'db.leaderboard.find()'"
echo "  mongosh octofit_db --eval 'db.workouts.find().limit(3)'"
echo ""
