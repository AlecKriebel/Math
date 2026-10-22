"""Stdlib-only final output validation and a safe complete-output SHA256 manifest."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
root=Path(__file__).resolve().parent
def check(test,label):
    if not test:raise RuntimeError(label)
def read(name):return json.loads((root/name).read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
exact=read('exact_certificates.json');numeric=read('independent_geometry_results.json')
legacy=read('reproduction_summary.json');negative=read('optimization_negative_control.json')
guards=read('independent_guard_replay.json');extreme=read('extreme_resonance_record.json')
check(exact['status']=='PASS' and exact['checks']==306,'exact suite incomplete')
check(numeric['status']=='PASS' and numeric['case_count']==44,'numerical grid incomplete')
check(sum(numeric['check_counts'].values())==34498,'unexpected numerical check count')
check((root/'exact_certificates_stdout.txt').read_bytes()==(root/'exact_certificates_optimized_stdout.txt').read_bytes(),'exact modes differ')
check(negative['runs']['normal']=={'returncode':1,'printed_PASS':False},'false legacy normal not rejected')
check(negative['runs']['optimized']=={'returncode':0,'printed_PASS':True},'false legacy optimized behavior changed')
for mode in ('normal','optimized'):
    check(guards[mode]=={'geometric_replay_returncode':0,'deliberate_false_check_returncode':1},'independent guards unsafe')
for name in ('independent_geometry_stderr.txt','exact_certificates_stderr.txt',
             'exact_certificates_optimized_stderr.txt','extreme_resonance_record_stderr.txt',
             'extreme_serialized_replay_stderr.txt','nonconfocal_negative_control_stderr.txt'):
    check((root/name).read_bytes()==b'','successful run stderr nonempty: '+name)
check('PASS extreme175digit serialization replay' in (root/'extreme_serialized_replay_stdout.txt').read_text(),'extreme serialized replay missing')
check(extreme['serialized_significant_digits']==175,'extreme serialization too short')
archive=root.parent/'original_submitted_head'
for filename,hashkey in [('verify.py','source_sha256'),('PROOF.md','proof_sha256')]:
    original=(archive/filename).read_bytes()
    check(sha(original)==legacy[hashkey],'archive source hash changed: '+filename)
    for mode in ('normal','optimized'):
        check((root/('submitted_replay_'+mode)/filename).read_bytes()==original,'replay copy mismatch')
stamp=datetime.now(timezone.utc).isoformat()
validation={'status':'PASS final family artifact validation','completed_utc':stamp,
            'exact_explicit_checks':306,'numerical_explicit_checks':34498,'target_cases':44,
            'exact_normal_optimized_stdout_identical':True,
            'legacy_false_check_normal_rejected_optimized_false_PASS':True,
            'independent_false_guard_rejected_in_both_modes':True,
            'extreme175digit_serialization_replayed':True,
            'bundled_runtime':'Python3.12.14, Clang22.1.3; SymPy1.14.0/mpmath1.3.0 installed locally',
            'original_archive_proof_and_verifier_byte_identical_to_replayed_inputs':True,
            'remaining_mathematical_gap_in_this_family':'None identified for the stated primitive theorem; analytic facts are classical, not formally machine-proved',
            'publication_or_priority_clearance':False}
(root/'validation_summary.json').write_text(json.dumps(validation,indent=2)+'\n')
with (root/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n* '+stamp+' — Final integrity checks pass: exact306 checks in both modes,\n'
                 '  numeric34,498 checks/44 target cases, expected legacy optimization\n'
                 '  failure and robust independent guards, successful175-digit extreme\n'
                 '  serialization replay, unchanged archive proof/verifier inputs.\n'
                 '  Completed safe complete-output SHA256 manifest; runtime dependency\n'
                 '  cache excluded. Completion:100% of this bounded family audit.\n')
files=[]
for p in sorted(root.rglob('*')):
    rel=p.relative_to(root)
    if rel.parts[0]=='runtime_packages' or str(rel)=='MANIFEST.json':continue
    check(not p.is_symlink(),'symlink disallowed in deliverables: '+str(rel))
    if not p.is_file():continue
    check(p.suffix.lower()!='.pdf','PDF disallowed in this family deliverable')
    data=p.read_bytes()
    files.append({'path':str(rel),'bytes':len(data),'sha256':sha(data)})
manifest={'schema':'safe-complete-output-sha256-v1','created_utc':stamp,
          'root':str(root),'scope':'Complete authored audit and replay output files in this assigned folder',
          'excluded':{'MANIFEST.json':'Self-reference avoided',
                      'runtime_packages/**':'Private locally installed third-party dependency cache; not findings or publication content'},
          'no_third_party_source_PDFs':True,'no_symlinks_in_deliverables':True,
          'file_count':len(files),'total_bytes':sum(x['bytes'] for x in files),'files':files}
(root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':'PASS','files':len(files),'bytes':manifest['total_bytes'],
                  'manifest_sha256':sha((root/'MANIFEST.json').read_bytes())},indent=2))
