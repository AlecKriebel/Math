"""Passive complete finite V2 seal; no source/builder execution or writes outside own lane."""
import datetime, hashlib, json, stat
from pathlib import Path
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'verification/d4-canonical-potential-editorial-v2-sol-20261117'
OLD=P/'verification/d4-canonical-potential-editorial-sol-20261117'
NAMES=('FINAL_MANIFEST.json','FINAL.json')
def encoded(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink();raw=p.read_bytes();b=p.lstat();key=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
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
run=json.loads((OWN/'BUILDER_RUN.json').read_bytes());receipt=json.loads((OWN/'BUILD_RECEIPT.json').read_bytes());model=json.loads((OWN/'MODEL.json').read_bytes())
assert run['attempt']==1 and run['exit']==0 and run['stdout_bytes']==228 and run['stderr_bytes']==0 and run['builder_unchanged_after'] is True
assert pin(OWN/'build_private.py')['SHA256']==run['builder_SHA256']=='cf44edb2fb5bc478e8e72ec2b13867f52a2a5af6b8a35241fb48b0cdf69172ad'
old=(OLD/'build_private.py').read_bytes();new=(OWN/'build_private.py').read_bytes()
oldpath=b"OWN=P/'verification/d4-canonical-potential-editorial-sol-20261117'";newpath=b"OWN=P/'verification/d4-canonical-potential-editorial-v2-sol-20261117'"
oldset='lies in {−1, 0, 1}.</p>'.encode();newset='lies in &#123;−1, 0, 1&#125;.</p>'.encode()
assert old.count(oldpath)==old.count(oldset)==1 and old.replace(oldpath,newpath).replace(oldset,newset)==new
assert receipt['status']=='PRIVATE_PREPARED_STATIC_CHECKS_PASSED' and receipt['page_SHA256']==pin(OWN/'private-page/index.html')['SHA256']=='24bff5057a9f09fdfbc85020bb48c676c7940bf622cac8728dfb0dcb0f47ea0a'
assert receipt['model_SHA256']==pin(OWN/'MODEL.json')['SHA256']=='b6143b34a0d45cf5b3a8c7af64887d8bbc03ccf6463355b372fba7a7056d8444'
assert all(model[k] is None for k in ('actual_canonical','base_url','production_url','page_publication_date','AA','legacy_redirect','follow_up'))
assert pin(OWN/'BUILDER.stdout.bin')['bytes']==228 and pin(OWN/'BUILDER.stderr.bin')['bytes']==0
before=json.loads((OWN/'CUSTODY_BEFORE.json').read_bytes());after=json.loads((OWN/'CUSTODY_AFTER.json').read_bytes())
assert all(before[k]==after[k] for k in ('source','fixed_inputs','checkpointed_PLAN_three_files','immutable_failed_packet','root_setup_disposition'))
for name in NAMES:
    with (OWN/name).open('xb'):pass
f,d,hidden,emptydirs=census();files={n:v for n,v in f.items() if n not in NAMES};now=datetime.datetime.now(datetime.timezone.utc).isoformat();modes={n:f[n]['mode'] for n in NAMES}
manifest={'schema':'finite-private-D4-V2-complete-namespace-v1','UTC':now,'root':str(OWN),'root_mode':d['.'],'file_count':len(files)+2,'child_directory_count':len(d)-1,'payload_files':files,'directories':{n:m for n,m in d.items() if n!='.'},'hidden_paths':hidden,'empty_files':sorted(n for n,p in files.items() if p['bytes']==0),'empty_directories':emptydirs,'terminal_pair':[{'path':n,'bytes':0,'mode':modes[n],'recursive_hash_excluded':True} for n in NAMES]}
final={'schema':'private-D4-V2-FINAL-v1','UTC':now,'record':'23439776','status':'FROZEN_PRIVATE_EDITORIAL_V2_AWAITING_ROOT_FACT_REVIEW','completion_percent_private_editorial':100,'publication_authority':False,'canonical':None,'base_url':None,'production_url':None,'page_publication_date':None,'AA':None,'redirect':None,'follow_up':None,'file_count':len(files)+2,'child_directory_count':len(d)-1,'manifest':{'bytes':0,'SHA256':'0'*64,'mode':modes[NAMES[0]]},'own_bytes':0,'own_mode':modes[NAMES[1]],'page':files['private-page/index.html'],'model':files['MODEL.json'],'report':files['EDITORIAL_REPORT.md'],'literal_invocation':files['BUILDER_RUN.json'],'source_files_childdirs':[72,7],'old_failed_packet_files_childdirs':[22,0],'whole_before_after_custody_exact':True,'original_failed_FINAL':after['immutable_failed_packet']['files']['FINAL.json'],'original_failed_manifest':after['immutable_failed_packet']['files']['FINAL_MANIFEST.json'],'root_setup_disposition':files['ROOT_SETUP_DISPOSITION.json'],'V2_builder_attempts':1,'V2_builder_exit':0,'V2_builder_stdout_bytes':228,'V2_builder_stderr_bytes':0,'total_separately_authorized_builder_invocations':2,'original_builder_failures_retained':1,'original_planning_filename_error_retained':True,'generic_setup_failure_and_root_disposition_retained':True,'expected_diff_exit_one_is_data_difference':True,'automatic_repairs_or_retries':0,'browser_live_UI_collision_legacy_independent_fact_certificate':False,'only_terminal_recursive_hash_exclusions':list(NAMES),'self_hash_delivered_externally':True,'stop':True}
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
print(json.dumps({'status':final['status'],'file_count':len(files)+2,'child_directory_count':len(d)-1,'FINAL_MANIFEST':pin(OWN/NAMES[0]),'FINAL':pin(OWN/NAMES[1]),'page':pin(OWN/'private-page/index.html'),'model':pin(OWN/'MODEL.json'),'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
