"""Record provisional authoring and native controls; grant no publication gate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
P=Path(__file__).resolve().parent; A=P/'audits/pr329_20000450'
O=P.parent/'problems/20000450_pentagonal_torsion/preprint'
utc=datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes(); return dict(path=str(p.relative_to(P.parent)),bytes=len(b),sha256=sha(b))
assert not (A/'ROOT_PREPRINT_PROVISIONAL_01.json').exists()
assert json.loads((A/'ROOT_MATHEMATICAL_GATE.json').read_bytes())['status']=='PASS_ROOT_FULL_MATHEMATICAL_GATE_PR329'
native={}
for name in ['preprint_public_full_provisional001','preprint_public_arithmetic_bundled_provisional001',
             'preprint_public_guard_controls001','priority_morton_parameter_system001',
             'priority_morton_parameter_bundled001','priority_verdure_parameter_system001',
             'priority_verdure_parameter_bundled001','preprint_pdf_build004','preprint_pdf_render004']:
    D=A/'root_runs_private'/name; j=json.loads((D/'execution.json').read_bytes())
    assert j['exit_code']==0 and j['stderr_bytes']==0
    assert sha((D/'stdout.bin').read_bytes())==j['stdout_sha256']
    assert (D/'stderr.bin').read_bytes()==b''
    native[name]=j
binding=json.loads((A/'root_preprint_private/pdf_export_v4/source_pdf_binding.json').read_bytes())
assert binding['source_before']==binding['source_after']
assert binding['source_after']=={k:v for k,v in pin(O/'pentagonal-torsion-note.tex').items() if k!='path'}
assert binding['pdf']=={k:v for k,v in pin(O/'pentagonal-torsion-note.pdf').items() if k!='path'}
pages=sorted((A/'root_preprint_private/pdf_v04').glob('page-*.png')); assert len(pages)==7
j=dict(utc=utc,status='DRAFT_CONTROLS_PASS_PUBLICATION_GATES_PENDING',
    mathematical_verification_percent=100,workflow_percent=50,original_author_turn_count='1/5',
    current_artifacts={p.name:pin(p) for p in [O/'pentagonal-torsion-note.tex',O/'pentagonal-torsion-note.pdf',O/'zenodo-deposit.json',A/'preprint/README.md',A/'preprint/SUPPLEMENT.md']},
    native_reproductions=native,current_source_pdf_binding=binding,
    visual_review=dict(complete_original_rendered_pages=[1,2,3,4,5,6,7],
        finding='All current v04 pages visually inspected: legible equations/table, correct references, no clipping or overflow.',
        record_after_review_utc=utc,rendered_pages=[pin(p) for p in pages],
        earlier_render_failure='Initial direct rendering could not write to absent output directory; preserved tool failure, then created new directory and actually replayed native rendering successfully.'),
    public_verification=dict(version='PROVISIONAL_v01',payload_files=31,positive_programs=9,negative_arithmetic_mutants=4,
        additional_actual_negative_controls=8,manifest=pin(A/'preprint/verification_v01/MANIFEST.json'),
        limitation='Historical provisional bundle contains its then-current manuscript/metadata. Current attribution repairs are in the separate current note and must be exported into a new version and qualified before any publication.'),
    attribution=dict(Verdure='Prior universal full-torsion criterion and specialization, 2006, actual primary operative pages80–81 and84–88 read.',
        Morton='Prior same eleven-coefficient polynomial, full nonmarked Tate coordinates and radical; root read v4 pages5–9 and18, independent reviewer also witnessed actual v1 formulas in2016.',
        parameter_comparisons='All25 exact current comparisons reproduced on Python3.12 and3.14; previous21-comparison native records preserved.',
        current_global_repairs=['manuscript','supplement','public README','exact deposit metadata'],
        historical_originals_preserved=True),
    priority_complete=False,final_verification_archive_exists=False,preprint_ready=False,
    fresh_full_package_reviews_started=False,merged=False,published=False,tracker_updated=False,
    persistent_goal_complete=False)
(A/'ROOT_PREPRINT_PROVISIONAL_01.json').write_text(json.dumps(j,indent=2)+'\n')
(O/'READINESS.json').write_text(json.dumps(dict(utc=utc,status=j['status'],mathematical_verification_percent=100,
    workflow_percent=50,priority_complete=False,preprint_ready=False,merged=False,published=False,
    exact_remaining_gates=['Complete bounded priority audit and root external closure','Export and qualify current verification package','Successive fresh independent full-preprint adversarial reviews and global repairs','Exact merge','Production Zenodo publication and DOI tracker append']),indent=2)+'\n')
s=json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_bytes()); assert not s['shared_git_writes_paused']
s.update(utc=utc,descending_active_pr=329,descending_329_workflow_percent=50,
    descending_329_mathematical_verification_percent=100,descending_329_priority_complete=False,
    descending_329_preprint_ready=False,descending_git_checkpoint_preparing=False,
    descending_final_acceptance_preparing=False)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_bytes()); item=next(x for x in inv['items'] if x['number']==329)
item.update(audit_workflow_percent=50,priority_complete=False,preprint_ready=False,
    provisional_preprint_controls='PASS_CURRENT_DRAFT_AND_PORTABLE_v01_CONTROLS')
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
entry=f'\n{utc} — PR329 provisional preprint checkpoint: mathematics100%, workflow50%. Current seven-page note has both birational maps, full25-point and field proofs, explicit AI/unrefereed disclosure and exact metadata; native desktop compilation and bound PDF export passed, all7 rendered pages root-inspected. Public provisional v01 reproduced9 positive programs/four actual false arithmetic mutants; eight separate assertion/integrity controls rejected optimized/missing/changed/extra/mode/symlink cases. Root reproduced21 Morton and25 expanded Verdure/Morton/Fisher convention checks on both Python3.12/3.14. Older Verdure universal specialization/full-torsion criterion and Morton polynomial/coordinates/radical credited globally in current note/supplement/README/metadata. Historical source files, independent namespaces,1/5 and provisionalv01 preserved. Complete priority closure, new current archive qualification, fresh full-preprint review loop, exact merge, Zenodo and tracker still pending; no priority/preprint/publication clearance or firstness/current-openness certificate.\n'
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write(entry)
print(json.dumps({'utc':utc,'status':j['status'],'math_percent':100,'workflow_percent':50,'current_pdf':j['current_artifacts']['pentagonal-torsion-note.pdf']},indent=2))
