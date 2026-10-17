#!/usr/bin/env python3
"""Verify authored archive bindings and replay exact finite algebra, stdlib only."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys,tempfile,shutil
ROOT=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def check_binding(p,e):
    b=p.read_bytes();need(len(b)==e['bytes'],'size '+str(p));need(hashlib.sha256(b).hexdigest()==e['sha256'],'digest '+str(p))
def replay(script,flags):
    with tempfile.TemporaryDirectory(prefix='hypercyclic-exact-') as folder:
        target=Path(folder)/script.name;shutil.copyfile(script,target)
        run=subprocess.run([sys.executable,'-B',*flags,str(target)],capture_output=True,text=True)
        need(run.returncode==0,'exact run failed: '+run.stderr)
        return json.loads(run.stdout)
def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text());seen=set()
    for e in manifest['files']:
        rel=PurePosixPath(e['path']);need(not rel.is_absolute() and '..' not in rel.parts,'unsafe path');need(str(rel) not in seen,'duplicate path');seen.add(str(rel));check_binding(ROOT/str(rel),e)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    need(actual==seen|{'MANIFEST.json'},'unlisted/missing archive member')
    for edition in ['original_submitted','current_edition']:
        m=json.loads((ROOT/edition/'MANIFEST.json').read_text())
        for e in m['entries']:check_binding(ROOT/edition/e['file'],e)
    original=json.loads((ROOT/'provenance/SUBMITTED_SNAPSHOT.json').read_text())
    for e in original['files']:
        p=ROOT/'original_submitted'/Path(e['path']).name;b=p.read_bytes()
        need(hashlib.sha256(b).hexdigest()==e['sha256'] and len(b)==e['size'],'submitted identity')
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'],'submitted Git object identity')
    f=ROOT/'reviews/source_question_family/freeze_20261017T182054Z'
    frozen=json.loads((f/'MANIFEST.json').read_text())
    for e in frozen['files']:check_binding(f/e['path'],e)
    # External third-party source_files are receipts only and deliberately absent.
    external={e['path']:e for e in frozen['external_source_files']}
    for line in (f/'SHA256SUMS').read_text().splitlines():
        digest,rel=line.split(None,1);rel=rel.lstrip('*')
        if rel in external:
            need(digest==external[rel]['sha256'],'external source receipt disagrees');continue
        need(not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts,'unsafe frozen member')
        need(hashlib.sha256((f/rel).read_bytes()).hexdigest()==digest,'reconstruction freeze checksum')
    analytical=ROOT/'reviews/analytic_source_adversary'
    for e in json.loads((analytical/'EVIDENCE.json').read_text())['entries']:check_binding(analytical/e['file'],e)
    priority=ROOT/'priority/independent/freeze_20261017T183121Z'
    for e in json.loads((priority/'MANIFEST.json').read_text())['files']:check_binding(priority/e['path'],e)
    pf=ROOT/'priority/adversary';freeze=json.loads((pf/'FREEZE.json').read_text())
    need(hashlib.sha256((pf/'REPORT.md').read_bytes()).hexdigest()==freeze['report_sha256'],'priority adversary report freeze')
    need(hashlib.sha256((pf/'VERDICT.json').read_bytes()).hexdigest()==freeze['verdict_sha256'],'priority adversary verdict freeze')
    expected=json.loads((ROOT/'EXPECTED_DIAGNOSTICS.json').read_text());runs=[]
    for flags in [[],['-O'],['-OO']]:
        primary=replay(ROOT/'diagnostics/root_diagnostics.py',flags)
        independent=replay(analytical/'exact_checks.py',flags)
        need(primary==expected['root'],'fresh root exact result differs')
        need(independent==expected['analytic'],'fresh independent exact result differs')
        runs.append({'flags':flags,'root_match':True,'analytic_match':True})
    result={'status':'PASS','authenticated_members':len(seen),'submitted_files':len(original['files']),'current_and_original_nested_manifests':True,'source_question_freeze_files':len(frozen['files']),'external_source_receipt_only_not_reauthenticated':len(external),'analytic_evidence_files':len(json.loads((analytical/'EVIDENCE.json').read_text())['entries']),'exact_modes':runs,'root_executed_mutated_algorithms':3,'analytic_fixed_fixture_fault_model_predicates':5,'limits':'Checks archive byte identities, original object identities and finite coefficient algebra only. Infinite conclusions and prior implications rest on written analytic proofs. External source bodies are not included or reauthenticated by this replay; unavailable historical receipts are not certified.'}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
