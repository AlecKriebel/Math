#!/usr/bin/env python3
"""Disposable-copy corruption controls. Does not modify the frozen source."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parent
MODES=[[],['-O'],['-OO']]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def inventory(root):
    return {p.relative_to(root).as_posix():(p.stat().st_mode & 0o777,hashlib.sha256(p.read_bytes()).hexdigest()) for p in root.rglob('*') if p.is_file()}
def writable(root):
    # Only call on a newly created disposable copy, never ROOT.
    need(root.resolve()!=ROOT.resolve(),'refuse to modify original freeze')
    os.chmod(root,0o755)
    for p in root.rglob('*'):
        if not p.is_symlink():os.chmod(p,0o755 if p.is_dir() else 0o644)
def readonly(root):
    for p in root.rglob('*'):
        if not p.is_symlink():os.chmod(p,0o555 if p.is_dir() else 0o444)
    os.chmod(root,0o555)
def run(root,flags,cwd,launcher=None):
    return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(launcher or ROOT/'bootstrap.py'),'--root',str(root)],cwd=cwd,capture_output=True,text=True,timeout=90)
def main():
    before=inventory(ROOT);results=[];baseline=None
    with tempfile.TemporaryDirectory(prefix='short-geodesics-controls-') as temp:
        tmp=Path(temp)
        for flags in MODES:
            mode='normal' if not flags else flags[0]
            p=run(ROOT,flags,tmp);need(p.returncode==0 and not p.stderr,'baseline failure '+mode)
            if baseline is None:baseline=p.stdout
            need(p.stdout==baseline,'mode output difference');results.append({'mode':mode,'case':'baseline','pass':True})
            ro=tmp/('read_only_'+mode);shutil.copytree(ROOT,ro);readonly(ro);snap=inventory(ro)
            try:
                p=run(ro,flags,tmp,launcher=ro/'bootstrap.py');need(p.returncode==0 and p.stdout==baseline and not p.stderr,'read-only relocation failed');need(inventory(ro)==snap,'read-only bytes/modes changed')
                results.append({'mode':mode,'case':'read_only_relocated','pass':True})
            finally:writable(ro);shutil.rmtree(ro)
            cases=['proof_byte','code_before_authentication','wrong_manifest_pin','missing_file','extra_file','extra_directory','file_symlink','directory_symlink','root_symlink','malformed_manifest','duplicate_manifest_key','changed_bootstrap','renamed_member','nonregular_fifo']
            for case in cases:
                dst=tmp/('candidate_'+mode+'_'+case);shutil.copytree(ROOT,dst);writable(dst);target=dst;sentinel=tmp/('EXECUTED_'+mode+'_'+case)
                if case=='proof_byte':
                    with (dst/'packet/PROOF.md').open('ab') as f:f.write(b'\nchanged\n')
                elif case=='code_before_authentication':(dst/'packet/verify.py').write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("executed")\nprint("{}")\n')
                elif case=='wrong_manifest_pin':(dst/'MANIFEST.json').write_text((dst/'MANIFEST.json').read_text()+' ')
                elif case=='missing_file':(dst/'packet/PROOF.md').unlink()
                elif case=='extra_file':(dst/'packet/extra.txt').write_text('extra')
                elif case=='extra_directory':(dst/'packet/extra').mkdir()
                elif case=='file_symlink':
                    (dst/'packet/PROOF.md').unlink();(dst/'packet/PROOF.md').symlink_to(ROOT/'packet/PROOF.md')
                elif case=='directory_symlink':(dst/'packet/link').symlink_to(ROOT/'packet',target_is_directory=True)
                elif case=='root_symlink':
                    target=tmp/('link_'+mode);target.symlink_to(dst,target_is_directory=True)
                elif case=='malformed_manifest':(dst/'MANIFEST.json').write_bytes(b'\xff{')
                elif case=='duplicate_manifest_key':(dst/'MANIFEST.json').write_text('{"schema":1,"schema":2}')
                elif case=='changed_bootstrap':
                    with (dst/'bootstrap.py').open('a') as f:f.write('\n# altered launcher\n')
                elif case=='renamed_member':(dst/'packet/PROOF.md').rename(dst/'packet/PROOF2.md')
                elif case=='nonregular_fifo':os.mkfifo(dst/'packet/pipe')
                p=run(target,flags,tmp);need(p.returncode!=0 and not p.stdout,'mutation accepted: '+case);need(not sentinel.exists(),'payload ran before authentication')
                results.append({'mode':mode,'case':case,'pass':True})
                if target!=dst:target.unlink()
                shutil.rmtree(dst)
            claims=json.loads((ROOT/'packet/CLAIMS.json').read_text())
            malformed=[]
            for k,v in [('problem_id',True),('problem_id',10300043.0),('turns_used',6),('status','solved'),('universal_homotopy_solution',True)]:
                c=claims.copy();c[k]=v;malformed.append((k+'_'+str(v),json.dumps(c).encode()))
            c=claims.copy();c.pop('rank');malformed.append(('missing_key',json.dumps(c).encode()))
            c=claims.copy();c['extra']=0;malformed.append(('extra_key',json.dumps(c).encode()))
            malformed.extend([('list',b'[]'),('duplicate_key',b'{"x":1,"x":2}'),('nonfinite',b'{"x":NaN}'),('trailing',json.dumps(claims).encode()+b' x'),('invalid_utf8',b'\xff')])
            for case,data in malformed:
                inp=tmp/'malformed.json';inp.write_bytes(data)
                p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(ROOT/'packet/verify.py'),'--input',str(inp)],cwd=tmp,capture_output=True,text=True,timeout=90)
                need(p.returncode!=0 and not p.stdout,'malformed claims accepted: '+case);results.append({'mode':mode,'case':'claims_'+case,'pass':True})
    need(inventory(ROOT)==before,'original freeze was modified')
    print(json.dumps({'status':'PASS_FREEZE_CONTROLS','case_count':len(results),'modes':['normal','-O','-OO'],'source_unchanged':True,'effective_uid':os.geteuid(),'cases':results},sort_keys=True))
if __name__=='__main__':
    try:main()
    except (ValueError,TypeError,KeyError,UnicodeError,OSError,subprocess.SubprocessError) as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(2)
