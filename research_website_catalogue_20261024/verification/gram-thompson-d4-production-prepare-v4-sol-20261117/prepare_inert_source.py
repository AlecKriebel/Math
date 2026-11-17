#!/usr/bin/env python3
"""One raw-byte inert-source preparation; never load or execute a release helper."""
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import os
import stat

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'verification/gram-thompson-d4-production-prepare-v4-sol-20261117'
BASE=P/'verification/gram-thompson-d4-production-prepare-v3-sol-20261117'
FIXED=[BASE,P/'verification/root-protected-math-entries-disposition-20261117.json',
       P/'verification/root-checkpoint-436ec-adoption-20261117.json',
       P/'verification/root-gram-thompson-d4-overlay-adoption-20261117.json']

def need(value,reason):
    if not value:
        raise RuntimeError(reason)

def snapshot():
    rows=[]
    def visit(path):
        first=path.lstat()
        need(not any(p.is_symlink() for p in (path,*path.parents)),'no symbolic input paths')
        row={'path':str(path),'mode':format(stat.S_IMODE(first.st_mode),'04o'),
             'device':first.st_dev,'inode':first.st_ino,'mtime_ns':first.st_mtime_ns,'ctime_ns':first.st_ctime_ns}
        if stat.S_ISDIR(first.st_mode):
            children=sorted(path.iterdir())
            row.update(kind='directory',empty=not children)
            rows.append(row)
            for child in children:
                visit(child)
        else:
            need(stat.S_ISREG(first.st_mode),'ordinary fixed file')
            raw=path.read_bytes()
            row.update(kind='file',bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest())
            rows.append(row)
        last=path.lstat()
        need((first.st_dev,first.st_ino,first.st_mode,first.st_size,first.st_mtime_ns,first.st_ctime_ns)==
             (last.st_dev,last.st_ino,last.st_mode,last.st_size,last.st_mtime_ns,last.st_ctime_ns),'stable whole fixed input')
    for root in FIXED:
        visit(root)
    return rows

def write_new(name,raw):
    fd=os.open(OWN/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:
        os.fchmod(fd,0o644)
        offset=0
        while offset<len(raw):
            count=os.write(fd,raw[offset:])
            need(count>0,'complete owned write')
            offset+=count
        os.fsync(fd)
    finally:
        os.close(fd)

def replace_one(raw,old,new):
    need(raw.count(old)==1,'one exact authorized literal replacement')
    return raw.replace(old,new,1)

need(Path(__file__).absolute()==OWN/'prepare_inert_source.py','exact administrative authoring path')
before=snapshot()
old_source=(BASE/'release_overlay.py').read_bytes()
old_plan=(BASE/'PLAN.json').read_bytes()
need(hashlib.sha256(old_source).hexdigest()=='db93c08a28775a06c3925e60dac8d2732724c71ec62d2752083a56e1bf65c038','exact complete frozen V3 source')
need(hashlib.sha256(old_plan).hexdigest()=='f01b666bfd446e7ea10c1a8694bacd2d2046af1800c77ead0ecb25b620492137','exact complete frozen V3 PLAN')
disposition=(P/'verification/root-protected-math-entries-disposition-20261117.json').read_bytes()
need(hashlib.sha256(disposition).hexdigest()=='9c7aa016dc2907d75e6d5935a7f386296aa881c9fb4b45b20b1e35b292b98247','exact personally read root disposition')
plan=replace_one(old_plan,b'production-prepare-v3-sol-20261117',b'production-prepare-v4-sol-20261117')
plan=replace_one(plan,b'"Math_remote_root_sibling_directories": 159,',b'"Math_remote_root_sibling_directories": 148,\n  "Math_remote_protected_nonprogramme_entries": 159,')
plan=replace_one(plan,b'preserve its159 sibling directory and docs tree OIDs.',b'preserve all159 protected non-programme root entries (148 directory siblings and11 root files), including the docs tree, with exact name/mode/type/OID maps.')
plan_sha=hashlib.sha256(plan).hexdigest()
changes=[
 (b'production-prepare-v3-sol-20261117',b'production-prepare-v4-sol-20261117'),
 (b"PLAN_SHA='f01b666bfd446e7ea10c1a8694bacd2d2046af1800c77ead0ecb25b620492137'",("PLAN_SHA='"+plan_sha+"'").encode()),
 (b"need(len(siblings)==159 and siblings == proof['protected_159_directory_siblings'],'all159 exact remote sibling tree OIDs')",b"need(len(siblings)==148 and siblings == proof['protected_148_directory_siblings'],'all148 exact remote directory sibling tree OIDs')"),
 (b'all159 siblings and docs unchanged from436ec base while P checkpoints may advance',b'all148 directory siblings and docs unchanged from436ec base while P checkpoints may advance'),
 (b"need({name:header for name,header in base_map.items() if name!=P.name}=={name:header for name,header in mapping.items() if name!=P.name},'all untargeted Math root files/directories unchanged from436ec')",b"need(len(set(mapping)-{P.name})==159 and {name:header for name,header in base_map.items() if name!=P.name}=={name:header for name,header in mapping.items() if name!=P.name},'all159 protected non-programme Math root entries including11 files unchanged from436ec')"),
 (b"'root_listing':pin(raw),'siblings':159,'docs':pin(docs)",b"'root_listing':pin(raw),'directory_siblings':148,'protected_nonprogramme_entries':159,'docs':pin(docs)"),
]
source=old_source
for old,new in changes:
    source=replace_one(source,old,new)
write_new('release_overlay.py',source)
write_new('PLAN.json',plan)
for name,old,new in [('SOURCE.diff',old_source,source),('PLAN.diff',old_plan,plan)]:
    unit='release_overlay.py' if name=='SOURCE.diff' else 'PLAN.json'
    raw=''.join(difflib.unified_diff(old.decode().splitlines(keepends=True),new.decode().splitlines(keepends=True),fromfile='V3/'+unit,tofile='V4/'+unit)).encode()
    write_new(name,raw)
after=snapshot()
need(before==after,'all fixed V3/adoption/disposition inputs unchanged')
write_new('INPUT_PINS.json',(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'roots':[str(p) for p in FIXED],'before':before,'after':after,'whole_fixed_inputs_identical':True,
          'exact_source_byte_replacements':[{'old':a.decode(),'new':b.decode()} for a,b in changes],
          'all_release_helper_modes_import_AST_compile_help_test':0},indent=2,sort_keys=True)+'\n').encode())
print(json.dumps({'status':'INERT_V4_SOURCE_PREPARED_PENDING_FULL_SAVED_READ',
                  'source':{'bytes':len(source),'lines':source.count(b'\n'),'SHA256':hashlib.sha256(source).hexdigest()},
                  'PLAN':{'bytes':len(plan),'lines':plan.count(b'\n'),'SHA256':plan_sha},
                  'release_helper_invocations':0,'future_action_authority':False},sort_keys=True))
