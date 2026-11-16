"""Recheck only the 107 bound article files and their bound index; no W writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(__file__).resolve().parent
inventory = json.loads((root / 'ARTICLE_INVENTORY.json').read_text())
changes = []
records = [inventory['index']] + inventory['articles']
for record in records:
    data = Path(record['path']).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != record['bytes'] or digest != record['SHA256']:
        changes.append({'path':record['path'],'actual_bytes':len(data),'actual_SHA256':digest})
result = {'schema':'bounded-public-copy-unchanged-check-v1','UTC':datetime.now(timezone.utc).isoformat(),'indexed_articles':len(inventory['articles']),'bound_files_checked':len(records),'changed_files':changes,'no_W_writes':True,'no_Git_actions':True}
(root / 'UNCHANGED_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
raise SystemExit(bool(changes))
