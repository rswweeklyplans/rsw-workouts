# Quick Start Guide

## Test the System

```bash
cd "/Users/jeffstephens/Desktop/AI Apps/workout-app -4:x"

# Generate a test workout
python3 generate_workout.py 2024-12-07 --no-push

# View the generated file
open 4xweek/2024-12-07.html
```

## Connect to GitHub

```bash
# Add GitHub remote (make sure repo exists first!)
git remote add origin git@github.com:rswweeklyplans/rsw-workouts.git

# Or use HTTPS if you prefer:
# git remote add origin https://github.com/rswweeklyplans/rsw-workouts.git

# Push to GitHub
git push -u origin main
```

## Set Up Automation

```bash
# Run the setup script
./setup_automation.sh

# This will:
# ✓ Create cron job for Sunday 6:00 AM
# ✓ Auto-generate workouts
# ✓ Auto-commit to git
# ✓ Auto-push to GitHub
```

## Manual Workout Generation

```bash
# Next Monday's workout
python3 generate_workout.py

# Specific date
python3 generate_workout.py 2024-12-14

# Without auto-push
python3 generate_workout.py 2024-12-14 --no-push
```

## Verify Cron Job

```bash
# List all cron jobs
crontab -l

# Check generation logs
tail -f workout_generation.log
```

## What's Next?

1. **Create GitHub repo**: Go to https://github.com/rswweeklyplans and create `rsw-workouts` repo
2. **Connect and push**: Follow "Connect to GitHub" steps above
3. **Enable GitHub Pages**: In repo settings, enable Pages from `main` branch
4. **Set up automation**: Run `./setup_automation.sh`
5. **Done!** Your workouts will generate every Sunday at 6 AM

## File Overview

- `generate_workout.py` - Main generation script
- `workouts_data.json` - All workout templates
- `setup_automation.sh` - Cron job installer
- `auto_commit_push.sh` - Git automation
- `4xweek/` - Generated HTML files
- `README.md` - Full documentation

## Current Status

- **Start Date**: October 26, 2024
- **Current Week**: Week 5 (as of Nov 30, 2024)
- **Current Phase**: Strength (Weeks 5-8)
- **Next Phase**: Hypertrophy (Weeks 9-12)

## Training Cycle

| Weeks | Phase | Reps | Sets | Rest |
|-------|-------|------|------|------|
| 1-4 | Endurance | 12-20 | 3-4 | 60s |
| 5-8 | Strength | 6-10 | 4-5 | 90-120s |
| 9-12 | Hypertrophy | 8-12 | 4-5 | 60-90s |

Cycle repeats every 12 weeks!
