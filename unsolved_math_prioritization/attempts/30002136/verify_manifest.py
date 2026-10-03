"""Verify current public files against FINAL_MANIFEST.json, not historical snapshots."""
import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
m=json.loads((p/'FINAL_MANIFEST.json').read_text())
bad=[]
for name,want in m['files'].items():
    f=p/name
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=want:bad.append(name)
assert not bad,bad
print(json.dumps({'status':'PASS','files':len(m['files']),'problem_id':m['problem_id'],'turns_used':m['turns_used']},indent=2))
