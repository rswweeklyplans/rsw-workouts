#!/bin/bash
# RSW Workout Automation Setup Script
# This script sets up the cron job to automatically generate workouts every Sunday

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/generate_workout.py"
LOG_FILE="$SCRIPT_DIR/workout_generation.log"

echo "RSW Workout Automation Setup"
echo "============================="
echo ""
echo "This will set up automatic workout generation every Sunday at 6:00 AM"
echo ""

# Make the Python script executable
chmod +x "$PYTHON_SCRIPT"

# Create the cron job command
CRON_CMD="0 6 * * 0 cd \"$SCRIPT_DIR\" && /usr/bin/python3 \"$PYTHON_SCRIPT\" >> \"$LOG_FILE\" 2>&1"

echo "The following cron job will be added:"
echo "$CRON_CMD"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "generate_workout.py"; then
    echo "⚠️  A cron job for generate_workout.py already exists!"
    echo "Existing cron jobs:"
    crontab -l | grep "generate_workout.py"
    echo ""
    read -p "Do you want to replace it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
    # Remove existing cron job
    crontab -l | grep -v "generate_workout.py" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo "✓ Cron job installed successfully!"
echo ""
echo "Workout generation will run every Sunday at 6:00 AM"
echo "Logs will be saved to: $LOG_FILE"
echo ""
echo "To verify the cron job, run: crontab -l"
echo "To remove the cron job, run: crontab -e"
echo ""
echo "You can also manually generate workouts with:"
echo "  python3 generate_workout.py              # Generate for next Monday"
echo "  python3 generate_workout.py 2025-12-07   # Generate for specific date"
