"""Bind actual archive replays and current artifacts for fresh adversarial review."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, stat, zipfile
A=Path(__file__).resolve().parent.parent; R=A.parents[2]
O=R/'problems/20000450_pentagonal_torsion/preprint'
sha=lambda b:hashlib.sha256(b).hexdigest()
parser=argparse.ArgumentParser();parser.add_argument('version',type=int)
parser.add_argument('--pdf-export',required=True);args=parser.parse_args()
V=f'v{args.version:02d}';B=A/'preprint'/('verification_'+V)
Q=A/'preprint'/('qualification_'+V);assert not Q.exists()
archive=O/'pentagonal-torsion-verification.zip'
math=json.loads((A/'ROOT_CURRENT_MATHEMATICAL_GATE.json').read_bytes())
priority=json.loads((A/'ROOT_PRIORITY_CLOSURE.json').read_bytes())
assert math['status']=='PASS_ROOT_CURRENT_COMPLETE_MATHEMATICAL_GATE_PR329'
assert priority['status']=='PASS_ROOT_EXTERNALLY_CLOSED_PRIORITY_AUDIT_PR329'
with zipfile.ZipFile(archive) as z:
    names=z.namelist();assert len(names)==len(set(names))
    disk={str(p.relative_to(B))+('/' if p.is_dir() else ''):p for p in B.rglob('*')}
    assert set(names)==set(disk) and z.testzip() is None
    for info in z.infolist():
        p=disk[info.filename];assert not p.is_symlink()
        expected=(stat.S_IFDIR|0o755) if p.is_dir() else (stat.S_IFREG|0o644)
        assert info.external_attr>>16==expected
        assert z.read(info.filename)==(b'' if p.is_dir() else p.read_bytes())
manifest=json.loads((B/'MANIFEST.json').read_bytes())
extracted=A/'root_preprint_private'/('archive_replay_'+V)
def inventory(directory):
    result={}
    for p in directory.rglob('*'):
        assert not p.is_symlink()
        result[str(p.relative_to(directory))]=dict(kind='directory' if p.is_dir() else 'file',
            mode=stat.S_IMODE(p.stat().st_mode),
            sha256=None if p.is_dir() else sha(p.read_bytes()))
    return result
assert inventory(extracted)==inventory(B)
G=A/'root_runs_private'/('preprint_current_guard_controls_'+V)
guard_receipt=json.loads((G/'execution.json').read_bytes());guard_out=(G/'stdout.bin').read_bytes()
assert guard_receipt['exit_code']==0 and (G/'stderr.bin').read_bytes()==b''
assert sha(guard_out)==guard_receipt['stdout_sha256']
guard_result=json.loads(guard_out)
assert guard_result['status']=='PASS_EXPECTED_NEGATIVE_CONTROLS' and guard_result['controls']==9
assert guard_result['original_bundle_unchanged']
assert len(guard_result['actual_results'])==9 and all(t['actual_exit']!=0 for t in guard_result['actual_results'])
native={}
for name,suite,count in [('preprint_archive_full_'+V,'all',11),
                         ('preprint_archive_arithmetic_bundled_'+V,'arithmetic',2)]:
    D=A/'root_runs_private'/name;r=json.loads((D/'execution.json').read_bytes())
    out=(D/'stdout.bin').read_bytes();assert r['exit_code']==0 and (D/'stderr.bin').read_bytes()==b''
    assert sha(out)==r['stdout_sha256']
    assert r['argv'][2]==str(extracted/'verify.py')
    assert r['programs']==[dict(path=str(extracted/'verify.py'),bytes=(B/'verify.py').stat().st_size,
        sha256=sha((B/'verify.py').read_bytes()))]
    result=json.loads(out)
    assert result['status']=='PASS' and result['suite']==suite and result['positive_programs']==count
    assert result['negative_mutants']==4 and result['payload_files']==len(manifest['files'])
    assert result['manifest_sha256']==sha((B/'MANIFEST.json').read_bytes())
    assert result['all_bodies_modes_inventory_unchanged']
    assert len(result['results'])==count+4
    assert all(t['complete_mathematical_output_equal'] and t['stderr_bytes']==0 for t in result['results'])
    assert sum(t['actual_exit']==1 for t in result['results'])==4
    native[name]=dict(execution=r,complete_result=result)
assert inventory(extracted)==inventory(B)
D=A/'root_runs_private'/('preprint_archive_priority_public_'+V)
r=json.loads((D/'execution.json').read_bytes());out=(D/'stdout.bin').read_bytes()
assert r['exit_code']==0 and (D/'stderr.bin').read_bytes()==b'' and sha(out)==r['stdout_sha256']
assert r['argv'][2]==str(extracted/'priority_evidence/verify_public_package.py')
public_priority=json.loads(out)
assert public_priority['result']=='PASS' and public_priority['public_payloads']==11 and public_priority['exact_comparisons']==25
native['preprint_archive_priority_public_'+V]=dict(execution=r,complete_result=public_priority)
binding_path=A/'root_preprint_private'/('pdf_export_v'+args.pdf_export)/'source_pdf_binding.json'
binding=json.loads(binding_path.read_bytes())
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b))
assert binding['source_before']==binding['source_after']==pin(O/'pentagonal-torsion-note.tex')
assert binding['pdf']==pin(O/'pentagonal-torsion-note.pdf')
assert binding['actual_exit']==0 and binding['stderr_bytes']==0
qa_path=A/('ROOT_PDF_QA'+args.pdf_export.zfill(3)+'.json')
qa=json.loads(qa_path.read_bytes())
assert qa['status']=='PASS_ROOT_VISUAL_QA_CURRENT_SOURCE_PDF_PAIR' and qa['source']==binding['source_after'] and qa['pdf']==binding['pdf']
assert (B/'manuscript.tex').read_bytes()==(O/'pentagonal-torsion-note.tex').read_bytes()
assert (B/'manuscript.pdf').read_bytes()==(O/'pentagonal-torsion-note.pdf').read_bytes()
assert (B/'zenodo-deposit.json').read_bytes()==(O/'zenodo-deposit.json').read_bytes()
deposit=json.loads((O/'zenodo-deposit.json').read_bytes())
assert [x['path'] for x in deposit['files']]==['pentagonal-torsion-note.pdf','pentagonal-torsion-verification.zip']
Q.mkdir();(Q/'inputs').mkdir()
inputs=[('snapshot_manifest.json',A/'snapshot_manifest.json'),
        ('ROOT_CURRENT_MATHEMATICAL_GATE.json',A/'ROOT_CURRENT_MATHEMATICAL_GATE.json'),
        ('ROOT_PRIORITY_CLOSURE.json',A/'ROOT_PRIORITY_CLOSURE.json'),
        ('manuscript.tex',O/'pentagonal-torsion-note.tex'),('manuscript.pdf',O/'pentagonal-torsion-note.pdf'),
        ('verification.zip',archive),('zenodo-deposit.json',O/'zenodo-deposit.json'),
        ('source_pdf_binding.json',binding_path)]
records={}
for name,p in inputs:
    q=Q/'inputs'/name;q.write_bytes(p.read_bytes());q.chmod(0o644)
    records[name]=dict(original_path=str(p.relative_to(R)),**pin(q),mode='0644')
j=dict(utc=datetime.now(timezone.utc).isoformat(),status='NATIVELY_QUALIFIED_FOR_FRESH_ADVERSARIAL_REVIEW',
    version=args.version,inputs=records,input_count=8,source_pdf_pair_bound=True,
    all_archive_members_bytes_and_modes_equal=True,archive_manifest_sha256=sha((B/'MANIFEST.json').read_bytes()),
    archive_payload_files=len(manifest['files']),actual_native_replays=native,
    additional_actual_guard_controls=dict(execution=guard_receipt,complete_result=guard_result),
    root_visual_qa=pin(qa_path),
    mathematical_verification_percent=100,priority_percent=100,
    preprint_ready=False,merge_ready=False,publication_ready=False,persistent_goal_complete=False)
(Q/'QUALIFICATION.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(dict(utc=j['utc'],status=j['status'],input_count=8,archive_payload_files=j['archive_payload_files'],
    archive_sha256=records['verification.zip']['sha256'],qualification_sha256=sha((Q/'QUALIFICATION.json').read_bytes())),indent=2))
