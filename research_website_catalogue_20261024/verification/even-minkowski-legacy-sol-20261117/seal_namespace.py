"""Terminally inventory this owned lane only, without protected reads."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
A=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/even-minkowski-legacy-sol-20261117')
EXCLUSIONS=['FINAL_MANIFEST.json','FINAL_SEAL.json']
def sha(b):return hashlib.sha256(b).hexdigest()
def mode(p):return oct(stat.S_IMODE(p.lstat().st_mode))
def now():return datetime.now(timezone.utc).isoformat()
def encoded(x):return (json.dumps(x,indent=2,ensure_ascii=True)+'\n').encode()
assert all(not (A/n).exists() for n in EXCLUSIONS)
for n in EXCLUSIONS:(A/n).write_bytes(b'')
def inventory():
    entries=[{'path':'.','kind':'directory','mode':mode(A),'hidden_component':False,'empty':not any(A.iterdir())}]
    for p in sorted(A.rglob('*')):
        n=str(p.relative_to(A));s=p.lstat();row={'path':n,'mode':mode(p),'hidden_component':any(x.startswith('.') for x in p.relative_to(A).parts)}
        if stat.S_ISDIR(s.st_mode):row.update(kind='directory',empty=not any(p.iterdir()))
        elif stat.S_ISREG(s.st_mode):
            row['kind']='file'
            if n in EXCLUSIONS:row['content_hash_excluded_terminal_control']=True
            else:
                b=p.read_bytes();row.update(bytes=len(b),SHA256=sha(b),empty=len(b)==0)
        else:raise AssertionError('Unexpected nonregular namespace entry '+n)
        entries.append(row)
    return entries
entries=inventory();files=[r for r in entries if r['kind']=='file'];dirs=[r for r in entries if r['kind']=='directory']
manifest={'UTC':now(),'scope':str(A),'completion_percent':100,'entries':entries,
    'actual_file_count_including_terminal_controls':len(files),'actual_child_directory_count':len(dirs)-1,
    'hidden_entries':[r['path'] for r in entries if r['hidden_component']],
    'empty_regular_files':[r['path'] for r in files if r.get('empty')],
    'empty_directories':[r['path'] for r in dirs if r['empty']],
    'exact_recursive_content_hash_exclusions':EXCLUSIONS,
    'terminal_control_topology_and_modes_included':True,'namespace_frozen':True}
mb=encoded(manifest);(A/'FINAL_MANIFEST.json').write_bytes(mb)
pins={n:sha((A/n).read_bytes()) for n in ['FINAL.json','REPORT.md','GUARDS_BEFORE.json','GUARDS_AFTER.json','ATTEMPT_RESULT.json','collect_correspondence.py','derive_receipt.py']}
seal={'UTC':now(),'scope':str(A),'status':'FROZEN_COMPLETE','completion_percent':100,
    'FINAL_MANIFEST_SHA256':sha(mb),'pins':pins,'actual_file_count':len(files),'actual_child_directory_count':len(dirs)-1,
    'recursive_content_hash_exclusions':EXCLUSIONS,'further_work_authorized':False}
sb=encoded(seal);(A/'FINAL_SEAL.json').write_bytes(sb)
assert inventory()==entries
print(json.dumps({'FINAL_MANIFEST_SHA256':sha(mb),'FINAL_SEAL_SHA256':sha(sb),'actual_files':len(files),'actual_child_directories':len(dirs)-1,'hidden_entries':manifest['hidden_entries'],'empty_regular_file_count':len(manifest['empty_regular_files']),'empty_directories':manifest['empty_directories']}))
