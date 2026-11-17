"""Fresh passive terminal seal of the literal first failed attempt. No builder/source execution."""
import datetime, hashlib, json, stat
from pathlib import Path
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/d4-canonical-potential-editorial-sol-20261117')
NAMES=('FINAL_MANIFEST.json','FINAL.json')
def encoded(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink();raw=p.read_bytes();b=p.lstat()
    key=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    assert key(a)==key(b) and len(raw)==a.st_size
    return {'bytes':len(raw),'SHA256':hashlib.sha256(raw).hexdigest(),'MD5':hashlib.md5(raw).hexdigest(),'mode':oct(stat.S_IMODE(a.st_mode))}
def census():
    files={};dirs={'.':oct(stat.S_IMODE(OWN.lstat().st_mode))};todo=[OWN]
    while todo:
        here=todo.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            n=p.relative_to(OWN).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):dirs[n]=oct(stat.S_IMODE(s.st_mode));todo.append(p)
            else:files[n]=pin(p)
        b=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(b.st_dev,b.st_ino,b.st_mode,b.st_mtime_ns,b.st_ctime_ns)
    paths=set(files)|set(dirs)
    return files,dirs,sorted(n for n in paths if n!='.' and any(c.startswith('.') for c in n.split('/'))),sorted(n for n in dirs if n!='.' and not any(v.startswith(n+'/') for v in paths))
run=json.loads((OWN/'BUILDER_RUN.json').read_bytes())
assert run['attempt']==1 and run['exit']==1 and run['stdout_bytes']==0 and run['stderr_bytes']==680 and run['builder_unchanged_after'] is True
assert pin(OWN/'build_private.py')['SHA256']==run['builder_SHA256']=='f85eb79795a75f05460555f9bafdb687f17d7c591e7614573e065cae597faac6'
assert pin(OWN/'BUILDER.stdout.bin')['bytes']==0 and pin(OWN/'BUILDER.stderr.bin')['bytes']==680
assert b"SyntaxError: invalid character" in (OWN/'BUILDER.stderr.bin').read_bytes()
assert not (OWN/'private-page').exists() and not (OWN/'MODEL.json').exists() and not (OWN/'BUILD_RECEIPT.json').exists()
before=json.loads((OWN/'CUSTODY_BEFORE.json').read_bytes());after=json.loads((OWN/'CUSTODY_AFTER.json').read_bytes())
assert all(before[k]==after[k] for k in ('source','fixed_inputs','checkpointed_PLAN_three_files'))
for name in NAMES:
    with (OWN/name).open('xb'):pass
f,d,hidden,emptydirs=census();files={n:p for n,p in f.items() if n not in NAMES};now=datetime.datetime.now(datetime.timezone.utc).isoformat();modes={n:f[n]['mode'] for n in NAMES}
manifest={'schema':'finite-failed-private-editorial-whole-namespace-v1','UTC':now,'root':str(OWN),'root_mode':d['.'],'file_count':len(files)+2,'child_directory_count':len(d)-1,'payload_files':files,'directories':{n:m for n,m in d.items() if n!='.'},'hidden_paths':hidden,'empty_files':sorted(n for n,p in files.items() if p['bytes']==0),'empty_directories':emptydirs,'terminal_pair':[{'path':n,'bytes':0,'mode':modes[n],'recursive_hash_excluded':True} for n in NAMES]}
final={'schema':'failed-first-private-editorial-FINAL-v1','UTC':now,'record':'23439776','status':'FROZEN_FAILED_FIRST_BUILDER_ATTEMPT_NO_RETRY','private_editorial_completion_percent':20,'failure_and_custody_closure_percent':100,'builder_attempts':1,'builder_exit':1,'builder_stdout_bytes':0,'builder_stderr_bytes':680,'automatic_repairs_or_retries':0,'private_draft_exists':False,'manifest':{'bytes':0,'SHA256':'0'*64,'mode':modes[NAMES[0]]},'own_bytes':0,'own_mode':modes[NAMES[1]],'file_count':len(files)+2,'child_directory_count':len(d)-1,'failure_report':files['FAILURE_REPORT.md'],'literal_invocation':files['BUILDER_RUN.json'],'literal_stderr':files['BUILDER.stderr.bin'],'complete_source72_7_fixed_inputs_and_checkpointed_PLAN_exact':True,'canonical':None,'production_url':None,'AA':None,'publication_authority':False,'follow_up':None,'only_terminal_recursive_hash_exclusions':list(NAMES),'self_hash_supplied_externally':True,'stop_for_root_disposition':True}
for unused in range(20):
    lengths=(len(encoded(manifest)),len(encoded(final)))
    for row in manifest['terminal_pair']:row['bytes']=lengths[NAMES.index(row['path'])]
    final['manifest']['bytes']=lengths[0];final['own_bytes']=lengths[1]
    if lengths==(len(encoded(manifest)),len(encoded(final))):break
else:raise AssertionError('terminal length fixed point')
mb=encoded(manifest);final['manifest']['SHA256']=hashlib.sha256(mb).hexdigest();fb=encoded(final);assert lengths==(len(mb),len(fb))
(OWN/NAMES[0]).write_bytes(mb);(OWN/NAMES[1]).write_bytes(fb)
end,ed,eh,ee=census();assert {n:p for n,p in end.items() if n not in NAMES}==files and ed==d and eh==hidden and ee==emptydirs
assert end[NAMES[0]]['SHA256']==final['manifest']['SHA256'] and all(end[n]['bytes']==r['bytes'] and end[n]['mode']==r['mode'] for n,r in zip(NAMES,manifest['terminal_pair']))
print(json.dumps({'status':final['status'],'file_count':len(files)+2,'child_directory_count':len(d)-1,'FINAL_MANIFEST':pin(OWN/NAMES[0]),'FINAL':pin(OWN/NAMES[1]),'FAILURE_REPORT':pin(OWN/'FAILURE_REPORT.md'),'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
