# RSW Workout Automation System

Automated weekly workout plan generator with progressive overload tracking and 12-week training cycles.

## Overview

This system automatically generates personalized workout HTML files every Sunday morning. Each workout includes:
- **Progressive overload tracking** with localStorage
- **Mobile-responsive design** for easy gym use
- **RPE (Rate of Perceived Exertion) tracking**
- **Exercise notes** for form cues and PRs
- **Equipment selector** (home vs gym options)

## Training Phases

The system cycles through 3 phases every 12 weeks:

| Weeks | Phase | Focus | Reps | Sets | Rest |
|-------|-------|-------|------|------|------|
| 1-4 | **Endurance** | Muscular endurance & work capacity | 12-20 | 3-4 | 60s |
| 5-8 | **Strength** | Heavy loads & progressive overload | 6-10 | 4-5 | 90-120s |
| 9-12 | **Hypertrophy** | Muscle growth & volume | 8-12 | 4-5 | 60-90s |

### Weekly Structure
- **Monday**: Glutes
- **Tuesday**: Push (Upper Body)
- **Thursday**: Legs
- **Saturday**: Pull (Upper Body)

## Setup Instructions

### 1. Install Dependencies

```bash
# Python 3.8+ is required (you have Python 3.9.6)
python3 --version
```

### 2. Initialize Git Repository

```bash
cd "/Users/jeffstephens/Desktop/AI Apps/workout-app -4:x"

# Initialize git
git init

# Create .gitignore
echo "*.log
.DS_Store
__pycache__/
*.pyc" > .gitignore

# Add files
git add .
git commit -m "Initial commit: RSW Workout Automation System

🤖 Generated with Claude Code"

# Connect to GitHub
git remote add origin git@github.com:rswweeklyplans/rsw-workouts.git
git branch -M main
git push -u origin main
```

### 3. Set Up Automation (Optional)

To automatically generate workouts every Sunday at 6:00 AM:

```bash
chmod +x setup_automation.sh auto_commit_push.sh
./setup_automation.sh
```

This will:
- Set up a cron job to run every Sunday morning
- Automatically generate the next week's workout
- Commit and push to GitHub

## Usage

### Manual Generation

```bash
# Generate workout for next Monday
python3 generate_workout.py

# Generate workout for specific date
python3 generate_workout.py 2025-12-07

# Generate without auto-pushing to GitHub
python3 generate_workout.py 2025-12-07 --no-push
```

### View Your Workouts

Open the generated HTML files in your browser:

```bash
open 4xweek/2025-12-07.html
```

Or access via GitHub Pages (once deployed):
```
https://rswweeklyplans.github.io/rsw-workouts/4xweek/2025-12-07.html
```

## File Structure

```
workout-app/
├── generate_workout.py       # Main generation script
├── workouts_data.json        # Workout templates for all phases
├── setup_automation.sh       # Cron job setup script
├── auto_commit_push.sh       # Auto git commit/push script
├── README.md                 # This file
└── 4xweek/                   # Generated workout files
    ├── 2025-12-07.html
    ├── 2025-12-14.html
    └── ...
```

## Features

### Progressive Overload Tracking
Each exercise includes:
- Weight input (saved to localStorage)
- Rep counter
- RPE (1-10 scale)
- Set checkboxes for completion tracking
- Progression cues (e.g., "+5 lb next week")

### Equipment Flexibility
Each exercise has an equipment selector:
- **At home**: Dumbbell/Bands alternatives
- **At gym**: Barbell/Machines

### Data Persistence
All your workout data is stored in your browser's localStorage:
- Weights lifted
- Reps completed
- RPE ratings
- Exercise notes
- Set completions

**Note**: Clearing browser data will reset your logs.

## Customization

### Modify Workouts

Edit `workouts_data.json` to customize:
- Exercises
- Rep ranges
- Set counts
- Rest periods
- Progression cues

### Change Start Date

Edit the `START_DATE` in `generate_workout.py`:

```python
START_DATE = datetime(2024, 10, 26)  # Your start date
```

### Adjust Cron Schedule

Edit the cron job to change generation time:

```bash
crontab -e

# Change from 6:00 AM to 8:00 AM:
0 8 * * 0 cd "/path/to/workout-app" && python3 generate_workout.py
```

## Troubleshooting

### Cron Job Not Running

Check cron logs:
```bash
tail -f workout_generation.log
```

Verify cron job exists:
```bash
crontab -l
```

### Git Push Fails

Ensure SSH keys are set up:
```bash
ssh -T git@github.com
```

Or use HTTPS instead:
```bash
git remote set-url origin https://github.com/rswweeklyplans/rsw-workouts.git
```

### Wrong Week/Phase Calculation

Verify your start date in `generate_workout.py` matches your actual training start.

## Contributing

To add new exercises or modify phases:

1. Edit `workouts_data.json`
2. Test generation: `python3 generate_workout.py 2025-12-07 --no-push`
3. Commit changes
4. Push to GitHub

## License

Personal use for RSW training programs.

## Links

- **Phase Libraries**:
  - [Endurance Phase](https://rswweeklyplans.github.io/rsw-workouts/library/endurance)
  - [Strength Phase](https://rswweeklyplans.github.io/rsw-workouts/library/strength)
  - [Hypertrophy Phase](https://rswweeklyplans.github.io/rsw-workouts/library/hypertrophy)
- **GitHub Repo**: https://github.com/rswweeklyplans/rsw-workouts

---

**Generated with Claude Code** 🤖
