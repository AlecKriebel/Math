"""Small completion-only adapter retiring stale skip aliases; scientific bytes unchanged."""
from pathlib import Path
import hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent
p=D/'finish195.py'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='2826de94c05ce15b181e007b95712519139c26ad57fd253ee36fe9d31aee4ad5'
s=importlib.util.spec_from_file_location('frozen195lifecycle',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
original_overlay=m.overlay
def completion_overlay(c,h,n,parent,stamp,phase):
 assert phase=='completion'
 out=original_overlay(c,h,n,parent,stamp,phase)
 path=m.PREFIX+'CURRENT_PROGRESS.json';p=json.loads(out[path])
 assert p['current_PR']==p['last_completed_PR']==195 and (p['fully_completed_count'],p['published_count'])==(42,26)
 p.setdefault('retired_skip_alias_snapshots',[]).append({'UTC':stamp,'PR':195,'values':{k:p.get(k) for k in ['skipped_since_last_completion','skipped_before_last_completion']},'reason':'Current last-completed record is now195; old192 skip belonged to an earlier interval. Immutable ordered intake evidence records194 as sole skip between193 and195.'})
 assert p['skipped_PR194_status_only'] is not None
 p['skipped_since_last_completion']=[];p['skipped_before_last_completion']=[194]
 out[path]=m.enc(p);out[m.CASE+'publication_lifecycle_01/complete195.py']=Path(__file__).read_bytes()
 return out
m.overlay=completion_overlay
if __name__=='__main__':
 assert sys.dont_write_bytecode
 c,h,n=m.load();{'prepare':m.prepare,'accept':m.accept}[sys.argv[1]](c,h,n,'completion',sys.argv[2])
