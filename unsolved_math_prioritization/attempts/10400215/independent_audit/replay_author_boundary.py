"""Independent portable replay of the original author's pre-execution boundary.
Usage: python -I -S -B replay_author_boundary.py archive manifest bootstrap
The inputs must be the exact original 10400215 files; no input code is imported.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PINS={
 'archive':('5662c3bf4ce0dd4760f50a8c41a854f95bb7fbc1d4eacd7e9dadedf653809e66',12105),
 'manifest':('ee6af78fe87785c3c637986526987d6e07ec9c99e203bc8ae18ae10410044514',1405),
 'bootstrap':('c585c2d155f1c0d1cd158c9629aebd35f2abd0a6879b91c10996a26a8535e5c9',3107)}

def reject(message):
    raise SystemExit('AUDIT REJECT: '+message)
def sha(data):
    return hashlib.sha256(data).hexdigest()
def unique(pairs):
    out={}
    for key,value in pairs:
        if key in out: reject('duplicate JSON key')
        out[key]=value
    return out
if not sys.flags.isolated or not sys.flags.no_site:
    reject('isolated no-site interpreter required')
if len(sys.argv)!=4:
    reject('supply author archive, manifest, bootstrap')
paths={key:Path(arg).absolute() for key,arg in zip(('archive','manifest','bootstrap'),sys.argv[1:])}
blobs={}
for key,path in paths.items():
    if not stat.S_ISREG(path.lstat().st_mode): reject('nonregular external '+key)
    data=path.read_bytes()
    if (sha(data),len(data))!=PINS[key]: reject('external '+key+' authentication')
    blobs[key]=data
manifest=json.loads(blobs['manifest'],object_pairs_hook=unique)
records=[]
positive=[]
with tempfile.TemporaryDirectory(prefix='shadow-norm-independent-') as temp:
    temp=Path(temp)
    clean=temp/'author';clean.mkdir()
    with zipfile.ZipFile(paths['archive']) as archive:
        infos=archive.infolist()
        names=[entry.filename for entry in infos]
        if len(names)!=len(set(names)) or set(names)!=set(manifest['files']):reject('archive inventory')
        for entry in infos:
            if Path(entry.filename).name!=entry.filename or not stat.S_ISREG(entry.external_attr>>16):reject('archive member path or type')
            data=archive.read(entry);meta=manifest['files'][entry.filename]
            if len(data)!=meta['bytes'] or sha(data)!=meta['sha256']:reject('archive member authentication')
            (clean/entry.filename).write_bytes(data)
    hostile=temp/'hostile';hostile.mkdir();sentinel=temp/'EXECUTED'
    payload='from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("executed")\nraise RuntimeError("untrusted code")\n'
    for module in ('json','hashlib','fractions','itertools','pathlib','sitecustomize','usercustomize'):
        (hostile/(module+'.py')).write_text(payload)
    env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONSTARTUP=str(hostile/'sitecustomize.py'),PYTHONOPTIMIZE='2')
    relocated=temp/'relocated';shutil.copytree(clean,relocated)
    def invoke(root,opt,mp=None,entry=None,flags=('-I','-S','-B')):
        args=[sys.executable,*flags]+(['-O'] if opt else [])+[str(paths['bootstrap']),str(mp or paths['manifest']),str(root)]
        if entry is not None:args.append(entry)
        p=subprocess.run(args,cwd=hostile,env=env,capture_output=True,timeout=25)
        if sentinel.exists():reject('untrusted code executed')
        return p
    for optimized in (False,True):
        for label,root in (('archive_extraction',clean),('relocation',relocated)):
            p=invoke(root,optimized)
            if p.returncode or p.stderr:reject('positive author replay failed')
            output=json.loads(p.stdout)
            if output['diagnostics']['total_checks']!=45810:reject('unexpected author diagnostic count')
            positive.append(p.stdout)
            records.append({'case':label+'_hostile_environment','optimized':optimized,'result':'pass','stdout_sha256':sha(p.stdout)})
        cases=('extra_file','missing_file','proof_tamper','code_tamper','shadow_module','cache_directory','nested_directory','symlink_member','directory_member','fifo_member','root_symlink','ancestor_symlink','root_file','absent_root','entrypoint_override','resealed_manifest','manifest_symlink','manifest_directory','duplicate_key_manifest')
        for case in cases:
            root=temp/(case+str(optimized));shutil.copytree(clean,root)
            mp=paths['manifest'];entry=None
            if case=='extra_file':(root/'.extra').write_text('x')
            elif case=='missing_file':(root/'README.md').unlink()
            elif case=='proof_tamper':(root/'PROOFS.md').write_text('changed')
            elif case=='code_tamper':(root/'diagnostics.py').write_text(payload)
            elif case=='shadow_module':(root/'fractions.py').write_text(payload)
            elif case=='cache_directory':(root/'__pycache__').mkdir();(root/'__pycache__'/'diagnostics.pyc').write_text(payload)
            elif case=='nested_directory':(root/'nested').mkdir()
            elif case in ('symlink_member','directory_member','fifo_member'):
                member=root/'README.md';member.unlink()
                if case=='symlink_member':member.symlink_to(clean/'README.md')
                elif case=='directory_member':member.mkdir()
                else:os.mkfifo(member)
            elif case=='root_symlink':
                link=temp/('root-link'+str(optimized));link.symlink_to(root,target_is_directory=True);root=link
            elif case=='ancestor_symlink':
                parent=temp/('ancestor-link'+str(optimized));parent.symlink_to(temp,target_is_directory=True);root=parent/root.name
            elif case=='root_file':root=temp/('not-directory'+str(optimized));root.write_text('x')
            elif case=='absent_root':root=temp/('absent'+str(optimized))
            elif case=='entrypoint_override':entry='../hostile/sitecustomize.py'
            elif case=='resealed_manifest':
                (root/'diagnostics.py').write_text(payload)
                changed=json.loads(blobs['manifest']);data=(root/'diagnostics.py').read_bytes()
                changed['files']['diagnostics.py']={'bytes':len(data),'sha256':sha(data)}
                mp=temp/('resealed'+str(optimized)+'.json');mp.write_text(json.dumps(changed,sort_keys=True,indent=2)+'\n')
            elif case=='manifest_symlink':mp=temp/('manifest-link'+str(optimized));mp.symlink_to(paths['manifest'])
            elif case=='manifest_directory':mp=temp/('manifest-dir'+str(optimized));mp.mkdir()
            elif case=='duplicate_key_manifest':mp=temp/('duplicate'+str(optimized)+'.json');mp.write_bytes(b'{"schema":1,'+blobs['manifest'][1:])
            p=invoke(root,optimized,mp,entry)
            if p.returncode==0 or b'REJECT:' not in p.stderr:reject('negative author probe accepted: '+case)
            records.append({'case':case,'optimized':optimized,'result':'rejected_before_packet_execution','message':p.stderr.decode().strip()})
    # Test absence of each required interpreter restriction from a clean cwd and environment.
    for label,flags in (('missing_isolated',('-S','-B')),('missing_no_site',('-I','-B'))):
        p=subprocess.run([sys.executable,*flags,str(paths['bootstrap']),str(paths['manifest']),str(clean)],cwd=temp,env={'PATH':os.environ.get('PATH','')},capture_output=True,timeout=25)
        if p.returncode==0 or b'isolated no-site interpreter required' not in p.stderr:reject('unrestricted mode accepted')
        records.append({'case':label,'result':'rejected_before_packet_execution','message':p.stderr.decode().strip()})
    if len(set(positive))!=1:reject('positive outputs differ')
    if set(p.name for p in clean.iterdir())!=set(manifest['files']):reject('clean inventory changed')
    for name,meta in manifest['files'].items():
        if sha((clean/name).read_bytes())!=meta['sha256']:reject('clean packet changed')
print(json.dumps({'schema':1,'status':'pass','problem_id':10400215,'positive_replays':4,'negative_boundary_probes':40,'diagnostic_checks_per_replay':45810,'byte_identical_positive_outputs':True,'archive_authentication':'pass','original_immutable_inputs_match':True,'tests':records,'limitations':'Read-before-execution and strict static inventory tests; no claim against a concurrent hostile filesystem writer, compromised interpreter, or malicious trusted bootstrap. Finite diagnostics are not topological proof.'},sort_keys=True,indent=2))
