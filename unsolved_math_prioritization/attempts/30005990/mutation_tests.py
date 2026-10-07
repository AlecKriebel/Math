#!/usr/bin/env python3
"""Adversarial publication-integrity tests under ordinary and optimized Python."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);args=ap.parse_args()
    require(digest(ROOT/'PUBLIC_MANIFEST.json')==args.manifest_sha256,'External anchor mismatch')
    targets={'author_proof':'author/PROOF.md','author_realization':'author/REALIZATION_APPROACHES.md','audit_a':'audit_a/INDEPENDENT_AUDIT.md','audit_b':'audit_b/reports/AUDIT.md','author_results':'author/check_results.json','audit_a_results':'audit_a/AUDIT_MATH_RESULTS.json','audit_b_results':'audit_b/checks/results.json','author_manifest':'author/MANIFEST.json','audit_a_manifest':'audit_a/AUDIT_MANIFEST.json','audit_b_manifest':'audit_b/reports/MANIFEST.json','public_manifest':'PUBLIC_MANIFEST.json','archive':'AUTHOR_FREEZE.zip','reading_copy':'reading/PROOF.md','optional_patch':'audit_b/reports/OPTIONAL_CLARIFICATIONS.patch','portable_script':'replay/audit_b_controls.py'}
    cases=list(targets)+['missing_file','extra_file','extra_directory','symlink','coherent_rehash','false_solved_reanchored','unsafe_path_reanchored','duplicate_key_reanchored']
    tests=[]
    for name in cases:
        with tempfile.TemporaryDirectory(prefix='boundary-frequency-mutation-') as td:
            copy=Path(td)/'packet';shutil.copytree(ROOT,copy);anchor=args.manifest_sha256
            if name in targets:
                p=copy/targets[name];b=p.read_bytes();p.write_bytes(bytes([b[0]^1])+b[1:])
            elif name=='missing_file':(copy/'reading/PROOF.md').unlink()
            elif name=='extra_file':(copy/'unexpected.txt').write_text('unexpected')
            elif name=='extra_directory':(copy/'unexpected').mkdir()
            elif name=='symlink':
                p=copy/'reading/PROOF.md';p.unlink();p.symlink_to(ROOT/'reading/PROOF.md')
            elif name=='coherent_rehash':
                p=copy/'author/PROOF.md';p.write_bytes(p.read_bytes()+b' ');meta={'bytes':p.stat().st_size,'sha256':digest(p)}
                p=copy/'author/MANIFEST.json';obj=json.loads(p.read_bytes())
                for rec in obj['files']:
                    if rec['path']=='PROOF.md':rec.update(meta)
                p.write_text(json.dumps(obj,indent=2)+'\n');manifest=json.loads((copy/'PUBLIC_MANIFEST.json').read_bytes());manifest['files']['author/PROOF.md']=meta;manifest['files']['author/MANIFEST.json']={'bytes':p.stat().st_size,'sha256':digest(p)};(copy/'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
            elif name in ['false_solved_reanchored','unsafe_path_reanchored']:
                p=copy/'PUBLIC_MANIFEST.json';obj=json.loads(p.read_bytes())
                if name=='false_solved_reanchored':obj['status']='solved'
                else:obj['files']['../escape']=obj['files'].pop('README.md')
                p.write_text(json.dumps(obj,indent=2)+'\n');anchor=digest(p)
            elif name=='duplicate_key_reanchored':
                p=copy/'PUBLIC_MANIFEST.json';text=p.read_text();p.write_text(text.replace('"problem_id": 30005990,','"problem_id": 30005990, "problem_id": 30005990,',1));anchor=digest(p)
            for optimized in (False,True):
                cp=subprocess.run([sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(copy/'verify_publication.py'),'--manifest-sha256',anchor],cwd=td,capture_output=True,timeout=180)
                require(cp.returncode!=0 and cp.stderr.startswith(b'FAIL: '),'Mutation not explicitly rejected: '+name)
                tests.append({'case':name,'optimized':optimized,'rejected':True})
    print(json.dumps({'status':'PASS_MUTATION_CONTROLS','rejected':len(tests),'cases':len(cases),'tests':tests},sort_keys=True,indent=2))
if __name__=='__main__':main()
