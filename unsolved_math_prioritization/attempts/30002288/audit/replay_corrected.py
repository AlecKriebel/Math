"""Independent pinned replay and mutation controls for the viscosity-clarified derivative.
Usage: python -I -S replay_corrected.py AUTHOR_ZIP AUTHOR_MANIFEST AUTHOR_BOOTSTRAP
Only temporary disposable copies are mutated; input files are never changed.
"""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit('Use python -I -S')
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import zipfile

PINS={
'archive':('4acbfd16b42c4d155ae422823d4ea4937d542b8a574ca781a13aa58fa9193ec8',12405),
'manifest':('cb29a9d6228fba9c1daffbe6ef6e8fccbe8281abce5d0e20964769ba3f0a413c',1346),
'bootstrap':('e509bdc4ab88a6726574470df4a3a08e15ff865e2845e311d19caa4bb0b69490',2978)}
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
require(len(sys.argv)==4,'usage: replay_corrected.py ARCHIVE MANIFEST BOOTSTRAP')
Z,M,B=(pathlib.Path(x).absolute() for x in sys.argv[1:])
for label,p in zip(('archive','manifest','bootstrap'),(Z,M,B)):
    b=p.read_bytes();require((hashlib.sha256(b).hexdigest(),len(b))==PINS[label],label+' pin mismatch')
manifest=json.loads(M.read_bytes()); inventory=manifest['files']; cases=[]
with tempfile.TemporaryDirectory(prefix='fractional-independent-replay-') as temp:
    T=pathlib.Path(temp); original=T/'original';original.mkdir(); marker=T/'unexpected_execution'
    with zipfile.ZipFile(Z) as z:
        require(len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(inventory),'ZIP inventory')
        for name in z.namelist():
            require(pathlib.PurePosixPath(name).name==name,'unsafe ZIP name')
            data=z.read(name); record=inventory[name]
            require(len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256'],'member pin')
            (original/name).write_bytes(data)
    expected=(original/'RESULTS.json').read_bytes()
    def run(name,root=original,z=Z,m=M,opt=False,flags=('-I','-S'),cwd=None,env=None,diagnostic=None):
        command=[sys.executable,*flags,str(B),str(root),str(z),str(m)]+(['--optimized'] if opt else [])
        p=subprocess.run(command,cwd=cwd or T,env=env,capture_output=True,timeout=30)
        require(not marker.exists(),name+': untrusted code ran')
        if diagnostic is None:
            require(p.returncode==0 and p.stdout==expected and not p.stderr,name+': positive replay mismatch')
        else:
            require(p.returncode!=0 and p.stdout==b'' and diagnostic in p.stderr.decode(),name+': incorrect rejection')
        cases.append({'name':name,'result':'PASS','expected':'accept' if diagnostic is None else 'reject_before_checker','diagnostic':diagnostic or 'exact byte-identical expected output'})
    def fresh(name):
        p=T/name;shutil.copytree(original,p);return p
    payload='open('+repr(str(marker))+',"w").write("executed")\nraise RuntimeError("executed")\n'
    run('normal');run('optimized',opt=True)
    relocated=fresh('relocated')
    run('relocated',root=relocated);run('relocated_optimized',root=relocated,opt=True)
    poison=T/'poison';poison.mkdir()
    for name in ('json.py','hashlib.py','pathlib.py','zipfile.py','subprocess.py','fractions.py','math.py','sitecustomize.py','usercustomize.py'):
        (poison/name).write_text(payload)
    env=dict(os.environ);env['PYTHONPATH']=str(poison);env['PYTHONSTARTUP']=str(poison/'sitecustomize.py')
    run('poisoned_cwd_pythonpath',cwd=poison,env=env)
    run('poisoned_cwd_pythonpath_optimized',cwd=poison,env=env,opt=True)
    for flags,label in [((), 'no_flags'),(('-I',),'missing_no_site'),(('-S',),'missing_isolation')]:
        run(label,flags=flags,diagnostic='Use python -I -S')
    for name in ('json.py','hashlib.py','pathlib.py','fractions.py','math.py','sitecustomize.py','usercustomize.py'):
        p=fresh('root_'+name);(p/name).write_text(payload)
        run('root_shadow_'+name,root=p,diagnostic='strict root inventory mismatch')
    for extra in ('__pycache__','nested'):
        p=fresh('dir_'+extra);(p/extra).mkdir();(p/extra/'sentinel.py').write_text(payload)
        run('root_'+extra,root=p,diagnostic='strict root inventory mismatch')
    for name in ('verify_math.py','PROOF.md','RESULTS.json'):
        p=fresh('changed_'+name);(p/name).write_text(payload if name.endswith('.py') else 'changed\n')
        run('changed_'+name,root=p,diagnostic='member digest mismatch: '+name)
        run('changed_'+name+'_optimized',root=p,opt=True,diagnostic='member digest mismatch: '+name)
    p=fresh('missing');(p/'PROOF.md').unlink();run('missing_member',root=p,diagnostic='strict root inventory mismatch')
    p=fresh('link_member');(p/'verify_math.py').unlink();(p/'verify_math.py').symlink_to(original/'verify_math.py')
    run('symlink_member',root=p,diagnostic='symlink path forbidden')
    p=T/'link_root';p.symlink_to(original,target_is_directory=True)
    run('symlink_root',root=p,diagnostic='symlink path forbidden')
    parent=T/'linked_parent';parent.symlink_to(T,target_is_directory=True)
    run('symlink_parent',root=parent/'original',diagnostic='symlink path forbidden')
    p=T/'file_root';p.write_text('file')
    run('file_root',root=p,diagnostic='root is not a real directory')
    p=fresh('fifo');(p/'PROOF.md').unlink();os.mkfifo(p/'PROOF.md')
    run('fifo_member',root=p,diagnostic='non-regular file forbidden')
    badm=T/'altered_manifest';badm.write_bytes(M.read_bytes()+b' ')
    run('altered_external_manifest',m=badm,diagnostic='pinned manifest mismatch')
    badz=T/'altered_archive';badz.write_bytes(Z.read_bytes()+b'x')
    run('altered_archive',z=badz,diagnostic='archive digest mismatch')
    for source,label in ((Z,'archive'),(M,'manifest')):
        link=T/('link_'+label);link.symlink_to(source)
        run('symlink_'+label,z=link if label=='archive' else Z,m=link if label=='manifest' else M,diagnostic='symlink path forbidden')
    p=fresh('inside_manifest');shutil.copyfile(M,p/'manifest.json')
    run('manifest_inside_root',root=p,m=p/'manifest.json',diagnostic='archive and manifest must be external')
    p=fresh('inside_archive');shutil.copyfile(Z,p/'archive.zip')
    run('archive_inside_root',root=p,z=p/'archive.zip',diagnostic='archive and manifest must be external')
    require(set(p.name for p in original.iterdir())==set(inventory),'original inventory altered')
receipt={'schema':'independent-corrected-replay-v1','problem_id':30002288,'status':'PASS','case_count':len(cases),
'accepted_cases':sum(c['expected']=='accept' for c in cases),'rejected_cases':sum(c['expected']!='accept' for c in cases),
'cases':cases,'corrected_pins':{k:{'sha256':v[0],'bytes':v[1]} for k,v in PINS.items()},
'scope':'Artifact acceptance and finite checker replay; mathematical validity is established separately.',
'original_mutated':False,'publication_performed':False,
'limitations':'Trusted reviewed bootstrap, interpreter and standard library; stable filesystem during preflight/execution; no hostile concurrent OS guarantee.'}
sys.stdout.write(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
