"""Fresh passive complete original-source and immutable-INITIAL custody, no Git/website access."""
import datetime, hashlib, json, os, stat, sys
from pathlib import Path

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'papers/23204212/reviews/scope-continuation-20261117'
SRC=P/'papers/23204212/sources'
INITIAL=P/'papers/23204212/reviews/scope-sol'
assert sys.argv[1:] in (['before'],['after'])
phase=sys.argv[1]
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink()
    raw=p.read_bytes();z=p.lstat();fields=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)
    assert fields(a)==fields(z) and len(raw)==z.st_size
    return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest(),mode=oct(stat.S_IMODE(a.st_mode)))
def census(root):
    files,dirs={},{'.':oct(stat.S_IMODE(root.lstat().st_mode))};todo=[root]
    while todo:
        here=todo.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            n=p.relative_to(root).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):dirs[n]=oct(stat.S_IMODE(s.st_mode));todo.append(p)
            else:files[n]=pin(p)
        z=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(root=str(root),root_mode=dirs['.'],files=files,directories={n:m for n,m in dirs.items() if n!='.'},hidden_paths=[n for n in sorted(set(files)|set(dirs)) if n!='.' and any(x.startswith('.') for x in n.split('/'))],empty_files=[n for n,v in sorted(files.items()) if v['bytes']==0],empty_directories=[n for n in sorted(dirs) if n!='.' and not any(x.startswith(n+'/') for x in set(files)|set(dirs))])
result=dict(schema='continuation-original-and-INITIAL-custody-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),phase=phase,sources=census(SRC),INITIAL=census(INITIAL))
assert len(result['sources']['files'])==55 and len(result['sources']['directories'])==14
assert len(result['INITIAL']['files'])==37 and len(result['INITIAL']['directories'])==1
expected={'sources':{'SOURCE_FINAL.json':'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5','SOURCE_MANIFEST.json':'afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be'},'INITIAL':{'INITIAL_MANIFEST.json':'fa6bb1278a64cc254daf3d8e06ca05b6707cc24e4784b5752b901dcb0bd10550','INITIAL_SEAL.json':'43cf3fa2f6135f43581e09fef77ce811d481d535eaf23f2827a443c2c9b746a9'}}
for label,pins in expected.items():
    assert all(result[label]['files'][n]['SHA256']==digest for n,digest in pins.items())
im=json.loads((INITIAL/'INITIAL_MANIFEST.json').read_bytes())
assert {r['path']:{k:v for k,v in r.items() if k!='path'} for r in im['payload_files']}=={n:v for n,v in result['INITIAL']['files'].items() if n not in expected['INITIAL']}
assert {r['path']:r['mode'] for r in im['directories']}==result['INITIAL']['directories']
source_frozen=json.loads((INITIAL/'SOURCE_FINAL_GUARD.json').read_bytes())
assert result['sources']==source_frozen
if phase=='after':
    before=json.loads((OWN/'CUSTODY_BEFORE.json').read_bytes())
    assert all(result[k]==before[k] for k in ('sources','INITIAL'))
with (OWN/('CUSTODY_'+phase.upper()+'.json')).open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(phase=phase,source_files_childdirs=[55,14],INITIAL_files_childdirs=[37,1],all_controls_manifest_payloads_bytes_modes_hidden_empty_exact=True)))
