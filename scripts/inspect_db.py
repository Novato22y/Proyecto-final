import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app, db
from app.models import PomodoroPreset

app = create_app()
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print('Tables in DB:', tables)
    if 'pomodoro_presets' in tables:
        cols = inspector.get_columns('pomodoro_presets')
        print('Columns in pomodoro_presets:')
        for c in cols:
            print(' -', c['name'], c.get('type'))
    else:
        print('Table pomodoro_presets not found')
