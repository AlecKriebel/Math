#!/usr/bin/env python3
"""Clean-layout replay for the public mathematical packet."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parent

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    manifest=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
    for rel,info in manifest['files'].items():
        b=(ROOT/rel).read_bytes()
        assert len(b)==info['bytes'] and hashlib.sha256(b).hexdigest()==info['sha256'],rel
    frozen_review=json.loads((ROOT/'review/INDEPENDENT_CHECKS.json').read_text())
    author=[]
    with tempfile.TemporaryDirectory(prefix='congestion-public-replay-') as td:
        clean=Path(td)/'packet'
        shutil.copytree(ROOT,clean,ignore=shutil.ignore_patterns('__pycache__'))
        for turn in ['turn_01','turn_02']:
            expected=digest(ROOT/'turns'/turn/'CHECKS.json')
            run=subprocess.run([sys.executable,str(clean/'turns'/turn/'check_model.py')],cwd=clean,text=True,capture_output=True)
            assert run.returncode==0,run.stderr
            assert digest(clean/'turns'/turn/'CHECKS.json')==expected
            author.append({'turn':turn,'all_assertions_passed':True,'result_byte_matches_frozen':True})
        run=subprocess.run([sys.executable,str(clean/'review/portable_independent_checks.py')],cwd=clean,text=True,capture_output=True)
        assert run.returncode==0,run.stderr
        independent=json.loads((clean/'review/PORTABLE_INDEPENDENT_CHECKS.json').read_text())
        assert independent['all_assertions_passed']
        assert independent['checks'][1:]==frozen_review['checks'][1:]
        for key in ['review_seed','independent_of_author_code','scope']:
            assert independent[key]==frozen_review[key]
        assert independent['checks'][0]=={'name':'Public frozen author inputs verified','files':8,'pass':True}
        assert not (clean/'source').exists()
        assert not list(clean.rglob('*.pdf'))
        assert not list(clean.rglob('*.png'))
    result={'id':9700002,'public_hash_verification_passed':True,
            'clean_public_layout_only':True,'third_party_source_documents_required':False,
            'frozen_public_files_modified':False,'author_reruns':author,
            'portable_independent_all_assertions_passed':True,
            'mathematical_check_records_match_original_independent_review':True,
            'portable_input_binding':{'name':'Public frozen author inputs verified','files':8},
            'limitations':['Omitted original administrative/source files are not revalidated by the portable derivative.',
                           'The derivative is not byte-identical to the original review program.',
                           'Replay does not establish historical novelty or replace the proof/source-fidelity audit.']}
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
