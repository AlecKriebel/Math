"""Read-only actual four-original timestamp and ingress supplement.
This does not convert a date into a guarantee against subsequent changes.
"""
from pathlib import Path
import hashlib,sys,json,datetime,base64
W=Path(__file__).resolve().parent
p=W/'independent_checks.py';b=p.read_bytes()
if hashlib.sha256(b).hexdigest()!='63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a':raise RuntimeError('Independent checker input drift')
I={'__file__':str(p),'__name__':'_strict_independent_final_input'}
exec(compile(b,str(p),'exec',optimize=0),I)
def check(pin):
 result=I['final_ingress'](pin)
 env=I['objpin'](pin);l=env['payload']['final_ledger'];roles=l['original_transports']
 ordered=['metadata_before','values','formulas','metadata_after'];prior=None;events=[];paths=[];inodes=[]
 def date(x):
  if type(x)is not str:raise RuntimeError('Original aware UTC timestamp absent')
  t=datetime.datetime.fromisoformat(x)
  if t.tzinfo is None or t.utcoffset()!=datetime.timedelta(0):raise RuntimeError('Original timestamp is not UTC aware')
  return t
 for role in ordered:
  p=roles[role];e=I['objpin'](p);start=date(e['before']);end=date(e['after'])
  if end<start or prior is not None and start<prior:raise RuntimeError('Four original observations not chronological metadata brackets')
  prior=end;path=Path(p['path']);path=path if path.is_absolute()else I['R']/path;st=path.lstat();paths.append(str(path));inodes.append((st.st_dev,st.st_ino))
  events.append({'role':role,'before':e['before'],'after':e['after'],'duration_seconds':(end-start).total_seconds(),'original_pin':p})
 if len(set(paths))!=4 or len(set(inodes))!=4:raise RuntimeError('Four distinct physical original captures required')
 observed=date(l['observed_at'])
 if observed<prior or observed>datetime.datetime.now(datetime.timezone.utc):raise RuntimeError('Final observation date precedes original completion or is future dated')
 result.update(original_chronology=events,explicit_observation_end=l['observed_at'],strict_original_brackets_verified=True)
 return result
if __name__=='__main__':
 if len(sys.argv)!=3:raise RuntimeError('Need absolute actual overlay path and external SHA256')
 q=Path(sys.argv[1])
 print(json.dumps(check({'path':str(q),'bytes':q.stat().st_size,'sha256':sys.argv[2]}),sort_keys=True,ensure_ascii=False,indent=2))
