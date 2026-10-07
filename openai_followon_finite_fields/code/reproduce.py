#!/usr/bin/env python3
"""Reproduce the authored unpublished record in a clean directory; no external mutation."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys, tempfile, datetime

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--receipt',required=True);ap.add_argument('--compile-pdf',action='store_true');a=ap.parse_args()
    root=pathlib.Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'VERIFICATION_FILESET.json').read_text())
    changed=[]
    for entry in manifest['files']:
        p=root/entry['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:changed.append(entry['path'])
    if changed:raise SystemExit('Frozen source mismatch: '+', '.join(changed))
    commands=[['-m','unittest','-v','test_finite_fields.py'],['examples.py'],['extension_direct_verify.py'],['extension_crosscheck.py'],['construction_reduction_examples.py']]
    results=[]
    with tempfile.TemporaryDirectory(prefix='finite_fields_clean_') as tmp:
        clean=pathlib.Path(tmp)
        for entry in manifest['files']:
            rel=pathlib.Path(entry['path']);dest=clean/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/rel,dest)
        (clean/'data').mkdir(exist_ok=True);(clean/'receipts').mkdir(exist_ok=True)
        for args in commands:
            process=subprocess.run([sys.executable,*args],cwd=clean/'code',text=True,capture_output=True,timeout=90)
            results.append({'command':['python3',*args],'exit_code':process.returncode,'stdout':process.stdout,'stderr':process.stderr})
            if process.returncode:raise SystemExit('Clean reproduction failed: '+str(args)+'\n'+process.stderr)
        output_matches=results[1]['stdout']==(root/'code/examples-output.json').read_text()
        if not output_matches:raise SystemExit('Examples JSON differs from saved output')
        construction_matches=json.loads((clean/'data/construction_examples.json').read_text())==json.loads((root/'data/construction_examples.json').read_text())
        if not construction_matches:raise SystemExit('Construction JSON differs from saved output')
        compile_result=None
        if a.compile_pdf:
            version=subprocess.run(['tectonic','--version'],text=True,capture_output=True,check=True).stdout.strip()
            process=subprocess.run(['tectonic','-X','compile','manuscript/main.tex','--outdir','manuscript','--keep-logs'],cwd=clean,text=True,capture_output=True,timeout=90)
            compile_result={'version':version,'exit_code':process.returncode,'stdout':process.stdout,'stderr':process.stderr}
            if process.returncode or not (clean/'manuscript/main.pdf').is_file():raise SystemExit('Clean PDF build failed')
            info=subprocess.run(['pdfinfo',str(clean/'manuscript/main.pdf')],text=True,capture_output=True,check=True).stdout
            compile_result['pdfinfo']=info
            if 'Overfull' in (clean/'manuscript/main.log').read_text():raise SystemExit('PDF has overfull layout warnings')
        receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'fileset_sha256':hashlib.sha256((root/'VERIFICATION_FILESET.json').read_bytes()).hexdigest(),'source_hashes_verified':True,'clean_directory':True,'tests':results,'examples_byte_identical':output_matches,'construction_json_identical':construction_matches,'pdf_build':compile_result,'scope':'finite consistency checks and standalone build; not analytic proof or novelty certification'}
    (root/a.receipt).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'all_pass':True,'examples_byte_identical':output_matches,'construction_json_identical':construction_matches,'receipt':a.receipt},indent=2))
if __name__=='__main__':main()
