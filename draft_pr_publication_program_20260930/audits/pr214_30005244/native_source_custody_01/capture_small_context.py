"""Only bounded related-target metadata and instruction absence; no science."""
from pathlib import Path
import datetime,json,sys,types
HERE=Path(__file__).absolute().parent
p=HERE/'capture_native_custody.py'
m=types.ModuleType('capture');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
out={}
for tag,root in (('original',m.ORIGINAL_ROOT),('current',m.CURRENT_ROOT)):
 path='unsolved_math_prioritization/review_v2/related_target_groups.json';row=m.lookup(root,path)
 out[tag]={'path':path,'node':row}
 if row is not None:
  m.need(row['mode']=='100644' and row['type']=='blob','Regular related target metadata')
  j=m.fetch('git/blobs/'+row['sha']);m.need(type(j.get('size'))is int and 0<=j['size']<=1000000,'Small bounded related-target container only')
  raw=m.body(row['sha']);m.write(HERE/'_private/reading'/tag/path,raw);value=m.h.decode(raw)
  matches=[]
  def walk(x,path):
   if type(x) is dict:
    if any(v=='30005244' or type(v)is int and v==30005244 for v in x.values()):matches.append({'json_path':path,'entry':x})
    else:
     for k,v in x.items():walk(v,path+[k])
   elif type(x)is list:
    if any(v=='30005244' or type(v)is int and v==30005244 for v in x):matches.append({'json_path':path,'entry':x})
    else:
     for i,v in enumerate(x):walk(v,path+[i])
  walk(value,[]);out[tag].update({**m.pin(raw),'matching_entries':matches,'reading_copy':str((HERE/'_private/reading'/tag/path).relative_to(HERE))})
 for filename in ('AGENTS.md','CLAUDE.md'):
  r=m.lookup(root,'unsolved_math_prioritization/review_v2/'+filename)
  m.need(r is None,'Unexpected source-context nested instructions require read')
out['UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();out['full_primary_statement_not_read']=True
m.write(HERE/'RELATED_SOURCE_CONTEXT.json',m.encode(out));m.write(HERE/'RELATED_CONTEXT_TREES.json',m.encode(m.TREES))
print(json.dumps({'related_original':out['original']['node'],'related_current':out['current']['node'],'native_GETs':len(m.ledger())}))

