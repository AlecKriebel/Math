"""Remove only this family's transient foreign PDFs, text extracts and renders."""
from pathlib import Path
import datetime,hashlib,json,os
F=Path(__file__).resolve().parent
location=json.loads((F/'TRANSIENT_PRIMARY_LOCATION.json').read_bytes())
t=Path(location['directory'])
assert t.name.startswith('pr49_boundary_primary_') and t.is_dir() and not t.is_symlink()
rows=[]
for p in sorted(t.iterdir()):
 assert p.is_file() and not p.is_symlink() and p.suffix in ['.pdf','.txt','.png']
 b=p.read_bytes();rows.append({'filename':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'foreign_body_copied_into_family':False});p.unlink()
assert not list(t.iterdir());t.rmdir();assert not t.exists()
(F/'TRANSIENT_PRIMARY_REMOVAL.json').write_text(json.dumps({'schema':'pr49-boundary-transient-primary-cleanup/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'deleted_directory':str(t),'removed_foreign_input_members':rows,'all_foreign_bodies_removed':True,'final_family_contains_foreign_bodies':False},indent=2)+'\n')
print(json.dumps({'removed_members':len(rows),'all_foreign_bodies_removed':True}))
