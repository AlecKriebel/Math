"""Pinned-verifier damage controls in temporary directories, standard library only."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def dump(path,obj):
    path.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')


def rehash(root,name):
    manifest=json.loads((root/'MANIFEST.json').read_text())
    b=(root/name).read_bytes()
    for row in manifest['files']:
        if row['name']==name:
            row['bytes']=len(b); row['sha256']=hashlib.sha256(b).hexdigest()
    dump(root/'MANIFEST.json',manifest)


def run_tests():
    root=Path(__file__).resolve().parent
    verifier=(root/'VERIFY.py').read_bytes()
    results=[]
    with tempfile.TemporaryDirectory(prefix='wu-second-review-') as tmp:
        temp=Path(tmp); pin=temp/'pinned_verifier.py'; pin.write_bytes(verifier)
        def check(label,mutate,expected,optimized=False):
            dst=temp/label; shutil.copytree(root,dst)
            if mutate:
                mutate(dst)
            command=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(pin),str(dst)]
            completed=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=120)
            passed=completed.returncode==0
            if passed!=expected:
                raise ValueError(label+': unexpected result: '+completed.stdout+completed.stderr)
            results.append({'name':label,'expected_acceptance':expected,'observed_acceptance':passed,'passed':True})
        check('baseline_normal',None,True)
        check('baseline_optimized',None,True,True)
        check('relocated_packet',None,True)
        check('missing_proof',lambda p:(p/'REVIEW.md').unlink(),False)
        check('extra_file',lambda p:(p/'EXTRA').write_text('extra'),False)
        check('extra_directory',lambda p:(p/'EXTRA').mkdir(),False)
        check('tampered_proof',lambda p:(p/'REVIEW.md').write_text('changed'),False)
        check('tampered_verifier',lambda p:(p/'VERIFY.py').write_text('pass\n'),False)
        def symlink(p):
            (p/'README.md').unlink(); (p/'README.md').symlink_to(root/'README.md')
        check('symlink_payload',symlink,False)
        def manifest_link(p):
            (p/'MANIFEST.json').unlink(); (p/'MANIFEST.json').symlink_to(root/'MANIFEST.json')
        check('symlink_manifest',manifest_link,False)
        def duplicate(p):
            b=(p/'MANIFEST.json').read_text(); (p/'MANIFEST.json').write_text(b.replace('{','{"format":"bad",',1))
        check('duplicate_json_key',duplicate,False)
        def bad_bytes(p):
            m=json.loads((p/'MANIFEST.json').read_text()); m['files'][0]['bytes']=True; dump(p/'MANIFEST.json',m)
        check('boolean_byte_count',bad_bytes,False)
        def bad_digest(p):
            m=json.loads((p/'MANIFEST.json').read_text()); m['files'][0]['sha256']='q'*64; dump(p/'MANIFEST.json',m)
        check('invalid_digest',bad_digest,False)
        def rehashed_binding(p):
            m=json.loads((p/'INPUT_BINDINGS.json').read_text()); m['archives'][0]['sha256']='0'*64; dump(p/'INPUT_BINDINGS.json',m); rehash(p,'INPUT_BINDINGS.json')
        check('rehashed_input_binding',rehashed_binding,False)
        def rehashed_rank(p):
            m=json.loads((p/'ACCEPTANCE.json').read_text()); m['free_toral_rank']=1; dump(p/'ACCEPTANCE.json',m); rehash(p,'ACCEPTANCE.json')
        check('rehashed_rank',rehashed_rank,False)
        def rehashed_result(p):
            m=json.loads((p/'DIAGNOSTIC_RESULTS.json').read_text()); m['loop_parity_mod_two']=0; dump(p/'DIAGNOSTIC_RESULTS.json',m); rehash(p,'DIAGNOSTIC_RESULTS.json')
        check('rehashed_diagnostic_result',rehashed_result,False)
        def prose_rehash(p):
            (p/'REVIEW.md').write_text('This is an unauthenticated replacement.\n'); rehash(p,'REVIEW.md')
        check('rehash_only_integrity_limitation',prose_rehash,True)
    return {'status':'PASS','pinned_verifier_sha256':hashlib.sha256(verifier).hexdigest(),'controls':results,
            'limitation':'A consistently rehashed prose replacement can pass; use a trusted external archive digest. No formal topology certification.'}


if __name__=='__main__':
    print(json.dumps(run_tests(),sort_keys=True,indent=2))
