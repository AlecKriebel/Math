#!/usr/bin/env python3
"""Reproduce the attributed research record in a clean directory; no external mutation."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys, tempfile, datetime

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--receipt',required=True);ap.add_argument('--compile-pdf',action='store_true');ap.add_argument('--fileset',default='VERIFICATION_FILESET.json');a=ap.parse_args()
    root=pathlib.Path(__file__).resolve().parents[1]
    fileset_path=root/a.fileset
    manifest=json.loads(fileset_path.read_text())
    changed=[]
    for entry in manifest['files']:
        p=root/entry['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:changed.append(entry['path'])
    if changed:raise SystemExit('Frozen source mismatch: '+', '.join(changed))
    commands=[['-m','unittest','-v','test_finite_fields.py'],['examples.py'],['extension_direct_verify.py'],['extension_crosscheck.py'],['construction_reduction_examples.py','--output','../data/construction_examples.json'],['coherence_counterexample.py']]
    results=[]
    with tempfile.TemporaryDirectory(prefix='finite_fields_clean_') as tmp:
        clean=pathlib.Path(tmp)
        for entry in manifest['files']:
            rel=pathlib.Path(entry['path']);dest=clean/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/rel,dest)
        (clean/'data').mkdir(exist_ok=True);(clean/'receipts').mkdir(exist_ok=True)
        # A copied fixture is not evidence of regeneration.  Remove it before
        # running the constructor so a missing writer cannot pass by equality.
        generated_construction=clean/'data/construction_examples.json'
        generated_construction.unlink()
        for args in commands:
            process=subprocess.run([sys.executable,*args],cwd=clean/'code',text=True,capture_output=True,timeout=90)
            results.append({'command':['python3',*args],'exit_code':process.returncode,'stdout':process.stdout,'stderr':process.stderr})
            if process.returncode:raise SystemExit('Clean reproduction failed: '+str(args)+'\n'+process.stderr)
        output_matches=results[1]['stdout']==(root/'code/examples-output.json').read_text()
        if not output_matches:raise SystemExit('Examples JSON differs from saved output')
        if not generated_construction.is_file():raise SystemExit('Construction command did not regenerate data')
        construction_matches=json.loads(generated_construction.read_text())==json.loads((root/'data/construction_examples.json').read_text())
        if not construction_matches:raise SystemExit('Construction JSON differs from saved output')
        def without_runtime_metadata(value):
            if isinstance(value,dict):return {k:without_runtime_metadata(v) for k,v in value.items() if k not in ('python','elapsed_seconds')}
            if isinstance(value,list):return [without_runtime_metadata(v) for v in value]
            return value
        for result_index,saved in [(2,'receipts/extension_direct_examples.json'),(3,'receipts/extension_independent_crosscheck.json')]:
            actual=json.loads(results[result_index]['stdout']);expected=json.loads((root/saved).read_text())
            if without_runtime_metadata(actual)!=without_runtime_metadata(expected):raise SystemExit('Saved direct/cross-check data differs: '+saved)
        coherence_matches=json.loads(results[5]['stdout'])==json.loads((root/'data/coherence_counterexample.json').read_text())
        if not coherence_matches:raise SystemExit('Coherence counterexample differs from saved certificate')
        audit_results=[]
        audit_specs=[('prime_audit_table_checks.py','prime_audit_table_checks.jsonl'),
                     ('analytic_audit_local_checks.py','analytic_audit_local_checks_results.json'),
                     ('geometric_checks.py','geometric_checks_results.json')]
        def without_errors(value):
            if isinstance(value,dict):return {k:without_errors(v) for k,v in value.items() if k!='max_error'}
            if isinstance(value,list):return [without_errors(v) for v in value]
            return value
        for script,saved in audit_specs:
            process=subprocess.run([sys.executable,script],cwd=clean/'agent_notes',text=True,capture_output=True,timeout=90)
            if process.returncode:raise SystemExit('Finite source audit failed: '+script+'\n'+process.stderr)
            if saved.endswith('.jsonl'):
                actual=[json.loads(line) for line in process.stdout.splitlines() if line.strip()]
                expected=[json.loads(line) for line in (root/'agent_notes'/saved).read_text().splitlines() if line.strip()]
            else:
                actual=json.loads(process.stdout);expected=json.loads((root/'agent_notes'/saved).read_text())
            if without_errors(actual)!=without_errors(expected):raise SystemExit('Saved finite source audit differs: '+script)
            if script=='analytic_audit_local_checks.py':
                for key,bound in [('phase_checks',1e-10),('residue_extension_checks',1e-10),('C_value_checks',1e-8)]:
                    if any(not 0<=row['max_error']<bound for row in actual[key]):raise SystemExit('Numerical local tolerance failed: '+key)
            audit_results.append({'script':script,'exit_code':0,'saved_result_structure_equal':True,'result':actual,'comparison':'exact after removing numerical max_error fields; actual numerical tolerances checked'})
        sparse_results=[]
        if (clean/'code/sparse_cartier.py').is_file():
            process=subprocess.run([sys.executable,'-m','unittest','-v','test_sparse_cartier.py'],cwd=clean/'code',text=True,capture_output=True,timeout=90)
            if process.returncode:raise SystemExit('Sparse reduction tests failed\n'+process.stderr)
            sparse_results.append({'script':'test_sparse_cartier.py','exit_code':0,'stderr':process.stderr})
            sparse_scripts=['sparse_extension_independent_checks.py','sparse_rational_independent_checks.py','sparse_adversarial_checks.py','sparse_adversarial_recurrence_checks.py','sparse_adversarial_frobenius_checks.py']
            for script in sparse_scripts:
                generated=clean/'agent_notes'/pathlib.Path(script).with_suffix('.json')
                generated.unlink()
                process=subprocess.run([sys.executable,script],cwd=clean/'agent_notes',text=True,capture_output=True,timeout=90)
                if process.returncode or not generated.is_file():raise SystemExit('Independent sparse check failed: '+script+'\n'+process.stderr)
                actual=json.loads(generated.read_text());expected=json.loads((root/'agent_notes'/generated.name).read_text())
                if actual!=expected:raise SystemExit('Regenerated sparse JSON differs: '+script)
                sparse_results.append({'script':script,'exit_code':0,'data_regenerated':True,'saved_result_exactly_equal':True,'generated_sha256':hashlib.sha256(generated.read_bytes()).hexdigest()})
        compile_result=None
        if a.compile_pdf:
            version=subprocess.run(['tectonic','--version'],text=True,capture_output=True,check=True).stdout.strip()
            process=subprocess.run(['tectonic','-X','compile','manuscript/main.tex','--outdir','manuscript','--keep-logs'],cwd=clean,text=True,capture_output=True,timeout=90)
            compile_result={'version':version,'exit_code':process.returncode,'stdout':process.stdout,'stderr':process.stderr}
            if process.returncode or not (clean/'manuscript/main.pdf').is_file():raise SystemExit('Clean PDF build failed')
            info=subprocess.run(['pdfinfo',str(clean/'manuscript/main.pdf')],text=True,capture_output=True,check=True).stdout
            compile_result['pdfinfo']=info
            if 'Overfull' in (clean/'manuscript/main.log').read_text():raise SystemExit('PDF has overfull layout warnings')
            if (root/'manuscript/paper.pdf').is_file():
                def pdf_text(path):return subprocess.run(['pdftotext','-layout',str(path),'-'],text=True,capture_output=True,check=True).stdout
                if pdf_text(clean/'manuscript/main.pdf')!=pdf_text(root/'manuscript/paper.pdf'):raise SystemExit('Clean PDF text differs from exported paper.pdf')
                compile_result['exported_pdf_text_equal']=True
        receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'fileset_sha256':hashlib.sha256(fileset_path.read_bytes()).hexdigest(),'source_hashes_verified':True,'clean_directory':True,'tests':results,'examples_byte_identical':output_matches,'construction_data_regenerated':True,'construction_json_identical':construction_matches,'direct_saved_results_equal_except_runtime_metadata':True,'coherence_certificate_equal':coherence_matches,'additional_source_audit_checks':audit_results,'sparse_checks':sparse_results,'pdf_build':compile_result,'scope':'finite consistency checks and standalone build; not analytic proof or novelty certification'}
    (root/a.receipt).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'all_pass':True,'examples_byte_identical':output_matches,'construction_data_regenerated':True,'construction_json_identical':construction_matches,'receipt':a.receipt},indent=2))
if __name__=='__main__':main()
