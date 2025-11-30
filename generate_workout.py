#!/usr/bin/env python3
"""
RSW Workout Generator
Automatically generates weekly workout HTML files based on 12-week training cycles.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
START_DATE = datetime(2024, 10, 26)  # Oct 26, 2024
REPO_PATH = Path("/Users/jeffstephens/Desktop/AI Apps/workout-app -4:x")
CYCLE_WEEKS = 12
GITHUB_REPO = "rswweeklyplans/rsw-workouts"


def calculate_week_and_phase(target_date):
    """
    Calculate the week number and phase for a given date.

    Args:
        target_date: datetime object for the target date

    Returns:
        tuple: (week_in_cycle, phase_name, phase_obj)
    """
    days_since_start = (target_date - START_DATE).days
    weeks_since_start = days_since_start // 7
    week_in_cycle = (weeks_since_start % CYCLE_WEEKS) + 1

    # Determine phase based on week in cycle
    if 1 <= week_in_cycle <= 4:
        phase_name = "endurance"
    elif 5 <= week_in_cycle <= 8:
        phase_name = "strength"
    elif 9 <= week_in_cycle <= 12:
        phase_name = "hypertrophy"
    else:
        phase_name = "endurance"  # fallback

    return week_in_cycle, phase_name


def load_workout_data():
    """Load workout data from JSON file."""
    json_path = REPO_PATH / "workouts_data.json"
    with open(json_path, 'r') as f:
        return json.load(f)


def sanitize_exercise_name(name):
    """Convert exercise name to URL-safe format."""
    return name.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '')


def generate_exercise_html(exercise, day_key, date_key):
    """Generate HTML for a single exercise."""
    ex_name_sanitized = sanitize_exercise_name(exercise['name'])
    sets = exercise['sets']
    reps = exercise['reps']
    rest = exercise['rest']
    pattern = exercise['pattern']
    progression = exercise['progression']

    # Generate set checkboxes
    sets_html = ""
    for i in range(1, sets + 1):
        sets_html += f'<label class="setbox"><input type="checkbox" data-key="{date_key}__{day_key}__{ex_name_sanitized}__set_{i}"><span>Set {i}</span></label>'

    # Determine reps label (could be reps, time, or distance)
    reps_label = "Reps"
    reps_placeholder = f"e.g., {reps}"
    if 's' in str(reps).lower() or 'sec' in str(reps).lower():
        reps_label = "Time (sec)"

    html = f'''
    <div class="exercise">
      <div class="ex-head">
        <div class="ex-title"><strong>{exercise['name']}</strong> <span class="badge">{reps} • Rest {rest}</span></div>
        <div class="equip">
          <label>Equipment</label>
          <select data-key="{date_key}__{day_key}__{ex_name_sanitized}__equip">
            <option value="home">At home: Dumbbell/Bands</option>
            <option value="gym">At gym: Barbell/Machines</option>
          </select>
        </div>
      </div>

      <div class="trackers">
        <label>Weight <input type="text" inputmode="decimal" placeholder="e.g., 135 lb" data-key="{date_key}__{day_key}__{ex_name_sanitized}__weight"></label>
        <label>{reps_label} <input type="number" min="1" step="1" placeholder="{reps_placeholder}" data-key="{date_key}__{day_key}__{ex_name_sanitized}__reps"></label>
        <label>RPE <input type="number" min="1" max="10" step="1" placeholder="1–10" data-key="{date_key}__{day_key}__{ex_name_sanitized}__rpe"></label>
      </div>

      <div class="sets">{sets_html}</div>

      <label class="notes">Notes
        <textarea rows="2" placeholder="Form cues, PRs, adjustments…" data-key="{date_key}__{day_key}__{ex_name_sanitized}__notes"></textarea>
      </label>

      <div class="cue">Progression cue: {progression}</div>
      <div class="pattern">Pattern: {pattern}</div>
    </div>
'''
    return html


def generate_workout_html(target_date, week_in_cycle, phase_name, workout_data):
    """Generate complete workout HTML for a given date."""
    phase = workout_data[phase_name]
    date_str = target_date.strftime("%b %d, %Y")
    date_key = target_date.strftime("%b %d, %Y")

    # Generate exercises for each day
    monday_html = ""
    for ex in phase['workouts']['monday_glutes']['exercises']:
        monday_html += generate_exercise_html(ex, 'day1', date_key)

    tuesday_html = ""
    for ex in phase['workouts']['tuesday_push']['exercises']:
        tuesday_html += generate_exercise_html(ex, 'day2', date_key)

    thursday_html = ""
    for ex in phase['workouts']['thursday_legs']['exercises']:
        thursday_html += generate_exercise_html(ex, 'day3', date_key)

    saturday_html = ""
    for ex in phase['workouts']['saturday_pull']['exercises']:
        saturday_html += generate_exercise_html(ex, 'day4', date_key)

    # Mini session exercises
    mini_exercises = "".join([f"<li>{ex}</li>" for ex in workout_data['mini_session']['exercises']])

    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RSW Weekly Plan — {date_str} — {phase['phase_name']}</title>
<style>
  :root{{ --olive:#6C7653; --cream:#F1F0EC; --gold:#C28511; --ink:#1b1b1b; --mid:#6b7280; }}
  *{{box-sizing:border-box}}
  body{{margin:0; font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial; color:var(--ink); background:var(--cream)}}
  .wrap{{max-width:960px; margin:0 auto; padding:24px 16px}}
  header{{background:linear-gradient(180deg,var(--olive),#536043); color:white; padding:24px; border-radius:16px}}
  header h1{{margin:0 0 6px 0; font-size:1.5rem; letter-spacing:0.2px}}
  .meta{{opacity:.95; font-size:.95rem}}
  .goal{{margin-top:12px; background:white; color:var(--ink); border-left:6px solid var(--gold); padding:12px 14px; border-radius:12px}}
  .intro{{margin:16px 0 0 0; font-size:1rem}}
  h2{{font-size:1.1rem; margin:18px 0 8px}}
  .workout, .mini, .walk, .footer{{ background:white; border-radius:16px; padding:16px; margin:16px 0; box-shadow:0 1px 0 rgba(0,0,0,.03) }}
  .exercise{{border:1px solid #e5e7eb; border-radius:12px; padding:12px; margin:12px 0; background:#fafafa}}
  .ex-head{{display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap}}
  .ex-title{{font-size:1rem}}
  .badge{{background:var(--cream); color:#333; padding:2px 8px; border-radius:999px; font-size:.8rem; margin-left:8px}}
  .equip label{{font-size:.8rem; color:#374151; display:block; margin-bottom:4px}}
  .equip select{{padding:8px; border-radius:10px; border:1px solid #d1d5db; background:white}}
  .trackers{{display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; margin:10px 0}}
  .trackers label{{display:flex; flex-direction:column; font-size:.85rem; gap:6px}}
  .trackers input{{padding:10px; border-radius:10px; border:1px solid #d1d5db; background:white}}
  .sets{{display:flex; flex-wrap:wrap; gap:10px; margin:6px 0 10px}}
  .setbox{{display:flex; align-items:center; gap:6px; font-size:.9rem; background:#fff; border:1px dashed #e5e7eb; border-radius:999px; padding:6px 10px}}
  .notes{{display:flex; flex-direction:column; gap:6px; font-size:.85rem}}
  textarea{{border:1px solid #d1d5db; border-radius:10px; padding:10px; background:white}}
  .cue,.pattern{{font-size:.85rem; color:#374151; margin-top:6px}}
  .mini ul{{margin:8px 0 0 18px}}
  .footer a{{color:var(--olive); text-decoration:underline}}
  .liblinks a{{margin-right:12px}}
  @media (max-width:640px){{ .trackers{{grid-template-columns:1fr}} }}
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>RSW Weekly Plan — {date_str}</h1>
      <div class="meta"><strong>Phase:</strong> {phase['phase_name']} (Weeks {phase['phase_weeks']}) — {phase['goal']} • Week {week_in_cycle}</div>
      <div class="goal"><strong>Goal of the week:</strong> {phase['goal']}</div>
      <p class="intro">{phase['intro']}</p>
    </header>


    <section class="workout">
      <h2>Monday: Glutes</h2>
      {monday_html}
    </section>

    <section class="workout">
      <h2>Tuesday: Push (Upper Body)</h2>
      {tuesday_html}
    </section>

    <section class="workout">
      <h2>Thursday: Legs</h2>
      {thursday_html}
    </section>

    <section class="workout">
      <h2>Saturday: Pull (Upper Body)</h2>
      {saturday_html}
    </section>

    <section class="mini">
      <h2>{workout_data['mini_session']['title']}</h2>
      <p>{workout_data['mini_session']['description']}</p>
      <ul>{mini_exercises}</ul>
    </section>

    <section class="walk">
      <h2>{workout_data['daily_walk']['title']}</h2>
      <p>{workout_data['daily_walk']['description']}</p>
    </section>

    <section class="footer">
      <p class="liblinks">
        New or jumping in mid-cycle? Explore the phase libraries:
        <a href="https://rswweeklyplans.github.io/{GITHUB_REPO}/library/endurance">Endurance</a> |
        <a href="https://rswweeklyplans.github.io/{GITHUB_REPO}/library/strength">Strength</a> |
        <a href="https://rswweeklyplans.github.io/{GITHUB_REPO}/library/hypertrophy">Hypertrophy</a>
      </p>
      <p style="color:#4b5563;font-size:.85rem">Tip: your entries are stored on your device (localStorage). Clearing site data will reset your logs.</p>
    </section>
  </div>

  <script>
    const restore = () => {{
      document.querySelectorAll('[data-key]').forEach(el=>{{
        const key = el.getAttribute('data-key');
        if (el.type === 'checkbox') {{
          el.checked = localStorage.getItem(key) === '1';
        }} else {{
          const v = localStorage.getItem(key);
          if (v !== null) el.value = v;
        }}
      }});
    }};
    const persist = (e) => {{
      const el = e.target;
      if (!el || !el.hasAttribute('data-key')) return;
      const key = el.getAttribute('data-key');
      const val = (el.type === 'checkbox') ? (el.checked ? '1':'0') : el.value;
      localStorage.setItem(key, val);
    }};
    window.addEventListener('change', persist, true);
    window.addEventListener('DOMContentLoaded', restore);
  </script>
</body>
</html>'''

    return html


def save_workout_file(target_date, html_content):
    """Save workout HTML to the appropriate file path."""
    # Create directory structure: 4xweek/YYYY-MM-DD.html
    workouts_dir = REPO_PATH / "4xweek"
    workouts_dir.mkdir(exist_ok=True)

    filename = target_date.strftime("%Y-%m-%d.html")
    filepath = workouts_dir / filename

    with open(filepath, 'w') as f:
        f.write(html_content)

    return filepath


def generate_for_date(target_date):
    """Generate workout for a specific date."""
    week_in_cycle, phase_name = calculate_week_and_phase(target_date)
    workout_data = load_workout_data()

    print(f"Generating workout for {target_date.strftime('%Y-%m-%d')}...")
    print(f"  Week {week_in_cycle} of 12-week cycle")
    print(f"  Phase: {phase_name.capitalize()}")

    html_content = generate_workout_html(target_date, week_in_cycle, phase_name, workout_data)
    filepath = save_workout_file(target_date, html_content)

    print(f"  ✓ Saved to: {filepath}")
    return filepath


def generate_for_next_week():
    """Generate workout for the upcoming Monday."""
    today = datetime.now()
    # Find next Monday
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7  # If today is Monday, get next Monday

    next_monday = today + timedelta(days=days_until_monday)
    return generate_for_date(next_monday)


def auto_commit_and_push():
    """Automatically commit and push changes to GitHub."""
    import subprocess

    script_path = REPO_PATH / "auto_commit_push.sh"
    if script_path.exists():
        try:
            subprocess.run(['bash', str(script_path)], check=True)
            print("\n✓ Changes committed and pushed to GitHub")
        except subprocess.CalledProcessError as e:
            print(f"\n⚠️  Warning: Could not commit/push to GitHub: {e}")
            print("   You may need to commit and push manually")
    else:
        print("\n⚠️  auto_commit_push.sh not found. Skipping git operations.")


if __name__ == "__main__":
    import sys

    auto_push = True  # Default: auto-commit and push

    if len(sys.argv) > 1:
        # Check for --no-push flag
        if '--no-push' in sys.argv:
            auto_push = False
            sys.argv.remove('--no-push')

        if len(sys.argv) > 1 and sys.argv[1] != '--no-push':
            # Generate for specific date (format: YYYY-MM-DD)
            target_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
            generate_for_date(target_date)
        else:
            # Generate for next Monday
            generate_for_next_week()
    else:
        # Generate for next Monday
        generate_for_next_week()

    # Auto-commit and push if enabled
    if auto_push:
        auto_commit_and_push()
