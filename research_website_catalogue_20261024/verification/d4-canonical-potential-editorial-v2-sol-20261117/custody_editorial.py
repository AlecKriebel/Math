"""Fresh passive fixed-input custody, with no Git, website, network or source execution."""
import datetime, hashlib, json, stat, sys
from pathlib import Path
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'verification/d4-canonical-potential-editorial-v2-sol-20261117'
OLD=P/'verification/d4-canonical-potential-editorial-sol-20261117'
SRC=P/'papers/23439776/sources'
assert sys.argv[1:] in (['before'],['after'])
phase=sys.argv[1]
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink()
    raw=p.read_bytes();b=p.lstat();key=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    assert key(a)==key(b) and len(raw)==a.st_size
    return {'bytes':len(raw),'SHA256':hashlib.sha256(raw).hexdigest(),'MD5':hashlib.md5(raw).hexdigest(),'mode':oct(stat.S_IMODE(a.st_mode))}
def census(root):
    assert root.is_dir() and not root.is_symlink()
    files={};dirs={'.':oct(stat.S_IMODE(root.lstat().st_mode))};todo=[root]
    while todo:
        here=todo.pop();a=here.lstat()
        for p in sorted(here.iterdir()):
            n=p.relative_to(root).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):dirs[n]=oct(stat.S_IMODE(s.st_mode));todo.append(p)
            else:files[n]=pin(p)
        b=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(b.st_dev,b.st_ino,b.st_mode,b.st_mtime_ns,b.st_ctime_ns)
    allpaths=set(files)|set(dirs)
    return {'root':str(root),'root_mode':dirs['.'],'files':files,'directories':{n:m for n,m in dirs.items() if n!='.'},'hidden_paths':sorted(n for n in allpaths if n!='.' and any(c.startswith('.') for c in n.split('/'))),'empty_files':sorted(n for n,v in files.items() if v['bytes']==0),'empty_directories':sorted(n for n in dirs if n!='.' and not any(x.startswith(n+'/') for x in allpaths))}
source=census(SRC)
assert len(source['files'])==72 and len(source['directories'])==7
assert source['files']['SOURCE_FINAL.json']['SHA256']=='e95d8717aee6b39ba23b73d85462a20340c823ff3ee5a09bc66470775a5b5a03'
assert source['files']['SOURCE_MANIFEST.json']['SHA256']=='d3041e24a1c481a2c4c9657edfa65a94c7db239be603d7b2a00c7fc0f560f6c0'
manifest=json.loads((SRC/'SOURCE_MANIFEST.json').read_bytes())
assert manifest['schema']=='opaque-native-source-manifest-v1'
assert manifest['ordinary_files_including_controls']==72 and manifest['child_directory_count']==7 and manifest['root_mode']==source['root_mode']
assert set(manifest['actual_file_paths_including_controls'])==set(source['files']) and len(manifest['actual_file_paths_including_controls'])==72
expected={r['path']:{k:r[k] for k in ('bytes','SHA256','mode')} for r in manifest['files']}
assert len(expected)==70 and expected=={n:{k:v[k] for k in ('bytes','SHA256','mode')} for n,v in source['files'].items() if n not in ('SOURCE_FINAL.json','SOURCE_MANIFEST.json')}
assert {r['path']:r['mode'] for r in manifest['directories']}==source['directories']
expected_inputs={
    'papers/23439776/reviews/root-continuation-20261117/ROOT_REVIEW.md':('4836979d83da2747da766a2defc76bc0e5bbd6b48b25025c0de434aefd580e62',11832),
    'verification/root-clearance-23439776-20261117.json':('d6a171c2f2a3b5480bd5bdc71e4c9fcb63bb2130bea2524e7e9df3cb9f6c6590',1831),
    'verification/binary-gram-locus-editorial-sol-20261117/private-page/research.css':('f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a',1170),
}
inputs={n:pin(P/n) for n in expected_inputs}
assert all(inputs[n]['SHA256']==v[0] and inputs[n]['bytes']==v[1] for n,v in expected_inputs.items())
plan_pins={'PLAN.md':'c11581975b0ecc630d6582c77cbbfaeaf275a4524502506f5f83de95cdf69cb7','RESEARCH_LOG.md':'d4c8d6999c0d3ade6c78449fe03d6ca4c2171633b2cd7698b5fe0d8e196289fa','DISCOVERY_LITERAL.txt':'905c7d3c68fb6386023572aa1494fc94b212cc9bd2f7ed1cff873e4bf474c568'}
plan={n:pin(OLD/n) for n in plan_pins}
assert all(plan[n]['SHA256']==v and plan[n]['mode']=='0o644' for n,v in plan_pins.items())
failed=census(OLD)
assert len(failed['files'])==22 and len(failed['directories'])==0
assert failed['files']['FINAL_MANIFEST.json']['SHA256']=='4f71ba0ba35c9e56c40dd7cb1f7604a51a6362ed33ba73f67e04c3522aa9313a'
assert failed['files']['FINAL.json']['SHA256']=='acb8535df05beb69ea59098769b2900f7f7cb8c12a311872a1e41fbfb9038ecd'
frozen=json.loads((OLD/'FINAL_MANIFEST.json').read_bytes())
assert frozen['payload_files']=={n:p for n,p in failed['files'].items() if n not in ('FINAL_MANIFEST.json','FINAL.json')}
assert frozen['directories']==failed['directories'] and frozen['root_mode']==failed['root_mode']
setup=pin(OWN/'ROOT_SETUP_DISPOSITION.json')
assert setup['bytes']==782 and setup['SHA256']=='73d8bf89943fbeb721688157cb45a9484383161195d27963c54dc399041a94ea'
result={'schema':'D4-V2-private-editorial-complete-fixed-input-custody-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':phase,'source':source,'fixed_inputs':inputs,'checkpointed_PLAN_three_files':plan,'immutable_failed_packet':failed,'root_setup_disposition':setup}
if phase=='after':
    before=json.loads((OWN/'CUSTODY_BEFORE.json').read_bytes())
    assert all(before[k]==result[k] for k in ('source','fixed_inputs','checkpointed_PLAN_three_files','immutable_failed_packet','root_setup_disposition'))
with (OWN/('CUSTODY_'+phase.upper()+'.json')).open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'phase':phase,'source_files_childdirs':[72,7],'whole_bytes_modes_hidden_empty_topology_authenticated':True,'fixed_root_review_clearance_CSS_exact':True,'checkpointed_PLAN_three_files_exact':True,'old_failed_packet_files_childdirs':[22,0],'old_failed_packet_and_root_setup_exact':True}))
