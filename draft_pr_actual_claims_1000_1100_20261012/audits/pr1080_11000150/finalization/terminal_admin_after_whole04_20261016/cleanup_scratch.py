#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,shutil,sys
W=Path(__file__).resolve().parent;S=W/'scratch'
if not S.is_dir() or S.is_symlink():raise RuntimeError('Own scratch absent or unsafe')
rows=[]
for p in sorted(S.rglob('*')):
 if p.is_symlink():rows.append({'path':str(p),'kind':'symlink','target':str(p.readlink())})
 elif p.is_file():rows.append({'path':str(p),'kind':'regular','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
ledger={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(S),'scope':'Only this worker newly created disposable unsealed scratch. Every recoverable exact identity recorded before own removal; canonical/source/history/other-worker files excluded.','files':rows}
name='OWNED_SCRATCH_CLEANUP'+('-'+sys.argv[1] if len(sys.argv)>1 else '')+'.json';p=W/name
if p.exists():raise RuntimeError('Never overwrite cleanup receipt')
p.write_text(json.dumps(ledger,indent=2)+'\n');shutil.rmtree(S);print(json.dumps({'status':'REMOVED_OWN_SCRATCH','files':len(rows),'bytes':sum(r.get('bytes',0) for r in rows),'ledger':str(p)}))
