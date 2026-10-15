"""Read schema only from the native catalog; no problem bodies or mutation."""
import datetime
import json
from pathlib import Path
import sqlite3

P = Path('/Users/alec/Documents/Math/unsolved_math_prioritization/cache/catalog.sqlite')
c = sqlite3.connect(P.as_uri() + '?mode=ro&immutable=1', uri=True)
rows = c.execute("SELECT type,name,sql FROM sqlite_master WHERE type IN ('table','view') ORDER BY name").fetchall()
print(json.dumps({'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'database_path': str(P), 'database_bytes': P.stat().st_size,
                  'readonly_immutable': True,
                  'tables': [{'type': t, 'name': n, 'sql': s} for t,n,s in rows]}, indent=2))
c.close()
