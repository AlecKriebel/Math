"""Only targeted native directory metadata discovery; no unrelated body fetch."""
from pathlib import Path
import json,sys,types
HERE=Path(__file__).absolute().parent
p=HERE/'capture_native_custody.py'
m=types.ModuleType('capture');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
result={}
for tag,root in (('original',m.ORIGINAL_ROOT),('current',m.CURRENT_ROOT)):
 result[tag]={}
 for path in ('problems','unsolved_math_prioritization/review_v2'):
  node=m.lookup(root,path)
  result[tag][path]={'node':node,'names':sorted(m.tree(node['sha'])) if node is not None and node['type']=='tree' else []}
m.write(HERE/'SOURCE_DIRECTORY_DISCOVERY.json',m.encode(result))
m.write(HERE/'SOURCE_DIRECTORY_TREES.json',m.encode(m.TREES))
print(json.dumps({tag:{path:{'node':v['node'],'name_count':len(v['names']),'first20':v['names'][:20],'matching':[x for x in v['names'] if '30005244' in x or x.startswith('reviews_') or x in ('AGENTS.md','CLAUDE.md')]} for path,v in rows.items()} for tag,rows in result.items()},sort_keys=True))

