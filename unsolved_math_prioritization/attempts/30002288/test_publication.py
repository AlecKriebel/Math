#!/usr/bin/env python3
"""Adversarial publication tests; all edits remain in disposable copies."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use -I -S -B')
import argparse,hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
def need(ok,msg):
    if not ok:raise ValueError(msg)
def pin(root):return hashlib.sha256((root/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()
def refresh(root):
    p=root/'PUBLICATION_MANIFEST.json';m=json.loads(p.read_text())
    for n in m['files']:
        b=(root/n).read_bytes();m['files'][n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    p.write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);a=ap.parse_args();root=Path(__file__).absolute().parent;bootstrap=root/'bootstrap.py';expected=a.expected_manifest;tests=[];runs=0
    with tempfile.TemporaryDirectory(prefix='fractional infinity adversarial ') as td:
        t=Path(td);marker=t/'SENTINEL_EXECUTED';hostile=t/'hostile cwd';hostile.mkdir()
        sentinel='open('+repr(str(marker))+',"w").write("executed")\nraise RuntimeError("untrusted source executed")\n'
        for n in ['json.py','hashlib.py','subprocess.py','sitecustomize.py','usercustomize.py']:(hostile/n).write_text(sentinel)
        env=os.environ.copy();env['PYTHONPATH']=str(hostile)
        def run(r,pp,opt=False,entry='integrity',flags=None,boot=bootstrap):
            nonlocal runs
            command=[sys.executable,*(['-I','-S','-B'] if flags is None else flags),*(['-O'] if opt else []),str(boot),str(r),pp,entry]
            p=subprocess.run(command,cwd=hostile,env=env,text=True,capture_output=True,timeout=900);runs+=1
            need(not marker.exists(),'import or unverified source executed')
            return p
        for label,r in [('baseline',root),('relocated',t/'relocated package with spaces')]:
            if label=='relocated':shutil.copytree(root,r)
            for opt in (False,True):
                p=run(r,expected,opt,'verify_publication.py');need(p.returncode==0 and not p.stderr,label+' full replay: '+p.stderr)
                out=json.loads(p.stdout);need(out['status']=='PASS' and out['all_valid_checker_executions_isolated_no_site_no_bytecode'] is True,'bad positive output')
                tests.append(label+(' optimized' if opt else ' normal')+' full replay with hostile cwd and PYTHONPATH')
        for flags,label in [(['-S','-B'],'missing -I'),(['-I','-B'],'missing -S'),(['-I','-S'],'missing -B')]:
            p=run(root,expected,flags=flags);need(p.returncode!=0 and 'REJECT:' in p.stderr,label);tests.append(label)
        cases=['extra file','extra directory','root bytecode cache','nested bytecode cache','sourceless bytecode','missing file','unrehashed proof','changed unexecuted gate','fifo','hardlink','symlink proof','symlink bootstrap','symlink gate','symlink runner','symlink author verifier','symlink audit verifier','symlink manifest','symlink directory','wrong pin','duplicate manifest key','extra manifest key','manifest bool bytes','manifest missing record','manifest traversal record','corrupt archive rehashed','author source rehashed','audit source rehashed','external frozen manifest rehashed','shadow json','shadow hashlib','shadow subprocess','shadow sitecustomize','root file','root FIFO']
        for index,case in enumerate(cases):
            w=t/('mutation '+str(index));shutil.copytree(root,w);used=expected;mf=w/'PUBLICATION_MANIFEST.json'
            if case=='extra file':(w/'extra').write_text('extra')
            elif case=='extra directory':(w/'empty').mkdir()
            elif case=='root bytecode cache':(w/'__pycache__').mkdir()
            elif case=='nested bytecode cache':(w/'audit/__pycache__').mkdir()
            elif case=='sourceless bytecode':(w/'json.pyc').write_bytes(b'untrusted cached code')
            elif case=='missing file':(w/'original/PROOF.md').unlink()
            elif case=='unrehashed proof':(w/'original/PROOF.md').write_text('changed')
            elif case=='changed unexecuted gate':(w/'verify_publication.py').write_text(sentinel)
            elif case=='fifo':(w/'README.md').unlink();os.mkfifo(w/'README.md')
            elif case=='hardlink':(w/'README.md').unlink();os.link(root/'README.md',w/'README.md')
            elif case.startswith('symlink '):
                n={'proof':'original/PROOF.md','bootstrap':'bootstrap.py','gate':'verify_publication.py','runner':'isolated_runner.py','author verifier':'original/verify_math.py','audit verifier':'audit/independent_diagnostics.py','manifest':'PUBLICATION_MANIFEST.json','directory':'audit'}[case[8:]];p=w/n
                if p.is_dir():shutil.rmtree(p)
                else:p.unlink()
                p.symlink_to(root/n,target_is_directory=n=='audit')
            elif case=='wrong pin':used='0'*64
            elif case=='duplicate manifest key':mf.write_text(mf.read_text().replace('"schema":','"schema": "duplicate", "schema":'));used=pin(w)
            elif case=='extra manifest key':m=json.loads(mf.read_text());m['extra']=True;mf.write_text(json.dumps(m));used=pin(w)
            elif case.startswith('manifest '):
                m=json.loads(mf.read_text())
                if case=='manifest bool bytes':m['files']['README.md']['bytes']=True
                elif case=='manifest missing record':del m['files']['README.md']
                elif case=='manifest traversal record':m['files']['../escape.py']=m['files'].pop('README.md')
                mf.write_text(json.dumps(m));used=pin(w)
            elif case=='corrupt archive rehashed':p=w/'archives/FRACTIONAL_INFINITY_30002288_AUTHOR_SAFE_FREEZE.zip';p.write_bytes(p.read_bytes()+b'X');refresh(w);used=pin(w)
            elif case in ('author source rehashed','audit source rehashed','external frozen manifest rehashed'):
                n={'author source rehashed':'original/verify_math.py','audit source rehashed':'review2/review_diagnostics.py','external frozen manifest rehashed':'manifests/FRACTIONAL_INFINITY_30002288_AUTHOR_EXTERNAL_MANIFEST.json'}[case];p=w/n;p.write_bytes(p.read_bytes()+b'\n');refresh(w);used=pin(w)
            elif case.startswith('shadow '):(w/(case[7:]+'.py')).write_text(sentinel)
            elif case=='root file':
                shutil.rmtree(w);w.write_text('wrong root')
            elif case=='root FIFO':
                shutil.rmtree(w);os.mkfifo(w)
            else:raise ValueError(case)
            for opt in (False,True):
                p=run(w,used,opt);need(p.returncode!=0 and 'REJECT:' in p.stderr,'unexpected acceptance: '+case)
            tests.append(case+' rejected normal and optimized')
            if case=='hardlink':(w/'README.md').unlink()
        for case in ['root symlink','ancestor symlink','bootstrap entrypoint symlink']:
            w=t/case
            boot=bootstrap;r=root
            if case=='root symlink':w.symlink_to(root,target_is_directory=True);r=w
            elif case=='ancestor symlink':parent=t/'real parent';parent.mkdir();shutil.copytree(root,parent/'child');w.symlink_to(parent,target_is_directory=True);r=w/'child'
            else:w.symlink_to(bootstrap);boot=w
            for opt in (False,True):p=run(r,expected,opt,boot=boot);need(p.returncode!=0 and 'REJECT:' in p.stderr,'unexpected acceptance '+case)
            tests.append(case+' rejected normal and optimized')
    print(json.dumps({'status':'PASS','named_controls':len(tests),'bootstrap_invocations':runs,'full_replays':4,'exact_archived_controls_per_full_replay':72,'additional_packet_controls_per_full_replay':188,'all_sentinels_unexecuted':True,'tests':tests,'boundary':'Externally trusted bootstrap and publication manifest, trusted interpreter/stdlib/OS, and quiescent input filesystem. Hashes authenticate bytes, not mathematical truth.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
