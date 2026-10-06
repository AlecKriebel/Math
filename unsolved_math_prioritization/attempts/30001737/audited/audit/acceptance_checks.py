#!/usr/bin/env python3
"""Independent acceptance and hostile import controls, no disabled assertions.
Arguments: ORIGINAL CORRECTED CATALOG PROBLEMS REPORTS. External pins below.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('Use python -I -S -B')
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ORIGINAL_PIN='af800982c8e6c93edf6780d20ad59d2a7ca4396303ac8b1dc1d07b9ac69381b0'
CORRECTED_PIN='4999825da91af80be0b889143a86ed98181e4ed9aa1489ce5a831c6d23b5b703'
BOOTSTRAP_PIN='1f1dae9e6a5123d86febe4d485dc5b29e7a43d1ff484a0915816acb4f18f0032'

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    original,corrected,catalog,problems,reports=map(lambda x:Path(x).absolute(),sys.argv[1:])
    bootstrap=Path(__file__).with_name('isolated_bootstrap.py').absolute()
    need(hashlib.sha256(bootstrap.read_bytes()).hexdigest()==BOOTSTRAP_PIN,'External bootstrap pin mismatch')
    result={'schema':'unitary-independent-acceptance-v1','original_manifest':ORIGINAL_PIN,'corrected_manifest':CORRECTED_PIN,'bootstrap_sha256':BOOTSTRAP_PIN,'replays':[],'hostile_controls':[],'corpus_controls':[]}
    def call(root,pin,opt,entry=None,extra=(),env=None,cwd='/tmp'):
        cmd=[sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+[str(bootstrap),str(root),pin]
        if entry:cmd += [entry]+list(extra)
        return subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=240)
    for kind,root,pin in [('original',original,ORIGINAL_PIN),('corrected',corrected,CORRECTED_PIN)]:
        for opt in (False,True):
            r=call(root,pin,opt);need(r.returncode==0,r.stderr)
            result['replays'].append({'kind':kind,'optimized':opt,'result':json.loads(r.stdout)})
    with tempfile.TemporaryDirectory(prefix='independent unitary controls ') as td:
        temp=Path(td);relocated=temp/'relocated payload with spaces';shutil.copytree(corrected,relocated)
        for opt in (False,True):
            r=call(relocated,CORRECTED_PIN,opt);need(r.returncode==0,r.stderr)
            result['replays'].append({'kind':'corrected_relocated','optimized':opt,'result':json.loads(r.stdout)})
        attacks=['extra_argparse','extra_json','extra_hashlib','extra_pathlib','extra_importlib_package','extra_sitecustomize','tampered_verifier','tampered_math','extra_directory','cache_directory','missing_file','symlink','hardlink','fifo','duplicate_manifest','parent_symlink','root_symlink']
        for label in attacks:
            root=temp/label;shutil.copytree(corrected,root);marker=temp/(label+'_EXECUTED')
            hostile='open('+repr(str(marker))+',"w").write("unexpected execution")\nraise RuntimeError("benign hostile import control")\n'
            if label.startswith('extra_') and label not in ('extra_importlib_package','extra_directory'):
                (root/(label[6:]+'.py')).write_text(hostile)
            elif label=='extra_importlib_package':
                (root/'importlib').mkdir();(root/'importlib/__init__.py').write_text(hostile)
            elif label=='tampered_verifier':(root/'verify.py').write_text(hostile)
            elif label=='tampered_math':(root/'math_checks.py').write_text(hostile)
            elif label=='extra_directory':(root/'unknown').mkdir()
            elif label=='cache_directory':(root/'__pycache__').mkdir()
            elif label=='missing_file':(root/'REPORT.md').unlink()
            elif label=='symlink':(root/'REPORT.md').unlink();(root/'REPORT.md').symlink_to(corrected/'REPORT.md')
            elif label=='hardlink':
                external=temp/'hardlink_source';external.write_bytes((root/'REPORT.md').read_bytes());(root/'REPORT.md').unlink();os.link(external,root/'REPORT.md')
            elif label=='fifo':(root/'REPORT.md').unlink();os.mkfifo(root/'REPORT.md')
            elif label=='duplicate_manifest':(root/'MANIFEST.json').write_bytes(b'{"schema":"bad",'+(root/'MANIFEST.json').read_bytes()[1:])
            elif label=='root_symlink':
                linked=temp/'linked_root';linked.symlink_to(root,target_is_directory=True);root=linked
            elif label=='parent_symlink':
                linked=temp/'linked_parent';linked.symlink_to(temp,target_is_directory=True);root=linked/label
            outcomes=[]
            for opt in (False,True):
                r=call(root,CORRECTED_PIN,opt);need(r.returncode!=0,'Attack accepted '+label);need(not marker.exists(),'Untrusted code executed '+label)
                outcomes.append({'optimized':opt,'rejected':True,'untrusted_code_executed':False})
            result['hostile_controls'].append({'name':label,'outcomes':outcomes})
        # The corrected direct entry points refuse nonisolated execution before
        # ordinary imports. -S here prevents interpreter-startup customization.
        direct=temp/'direct_guard';shutil.copytree(corrected,direct);marker=temp/'direct_EXECUTED'
        (direct/'argparse.py').write_text('open('+repr(str(marker))+',"w").write("bad")\n')
        for entry in ['verify.py','audit_checks.py','math_checks.py','verify_corpora.py']:
            for opt in (False,True):
                r=subprocess.run([sys.executable,'-S','-B']+(['-O'] if opt else [])+[str(direct/entry)],cwd=temp,capture_output=True,text=True)
                need(r.returncode!=0 and 'startup is not isolated' in r.stderr and not marker.exists(),'Direct guard failed')
            result['hostile_controls'].append({'name':'direct_isolation_guard_'+entry,'normal_rejected':True,'optimized_rejected':True,'untrusted_code_executed':False})
        hostile_env=temp/'hostile_environment';hostile_env.mkdir();marker=temp/'environment_EXECUTED'
        for name in ['sitecustomize.py','usercustomize.py','argparse.py','json.py']:(hostile_env/name).write_text('open('+repr(str(marker))+',"w").write("bad")\nraise RuntimeError("startup poison")\n')
        env=os.environ.copy();env['PYTHONPATH']=str(hostile_env);env['PYTHONHOME']=str(hostile_env);env['PYTHONSTARTUP']=str(hostile_env/'sitecustomize.py')
        for opt in (False,True):
            r=call(corrected,CORRECTED_PIN,opt,env=env,cwd=hostile_env);need(r.returncode==0,r.stderr);need(not marker.exists(),'Environment executed')
        result['hostile_controls'].append({'name':'hostile_PYTHONPATH_PYTHONHOME_PYTHONSTARTUP_and_cwd','normal_pass':True,'optimized_pass':True,'untrusted_code_executed':False})
        corpus_args=['--catalog',str(catalog),'--problems',str(problems),'--reports',str(reports)]
        for opt in (False,True):
            r=call(corrected,CORRECTED_PIN,opt,'verify_corpora.py',corpus_args);need(r.returncode==0,r.stderr)
            result['corpus_controls'].append({'name':'complete_corpora','optimized':opt,'result':json.loads(r.stdout)})
        for ix,label in enumerate(['catalog','problems','reports']):
            corrupted=temp/(label+'.json');p=[catalog,problems,reports][ix];content=p.read_bytes();corrupted.write_bytes(content+b' ')
            args=corpus_args.copy();args[2*ix+1]=str(corrupted)
            for opt in (False,True):
                r=call(corrected,CORRECTED_PIN,opt,'verify_corpora.py',args);need(r.returncode!=0,'Corrupt corpus accepted')
            result['corpus_controls'].append({'name':'byte_mutation_'+label,'normal_rejected':True,'optimized_rejected':True})
    result['status']='pass'
    result['scope']='Integrity and finite arithmetic acceptance only. Original direct startup fails; corrected isolated bootstrap passes. No general-converse solution or exhaustive literature-status claim.'
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
