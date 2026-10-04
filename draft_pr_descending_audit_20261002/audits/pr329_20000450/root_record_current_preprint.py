"""Record current root source references and observed PDF QA; no final clearance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
A=Path(__file__).resolve().parent;P=A.parents[1];R=A.parents[2]
O=R/'problems/20000450_pentagonal_torsion/preprint'
sha=lambda b:hashlib.sha256(b).hexdigest()
refs=json.loads((A/'preprint/verification_v01/SOURCE_REFERENCES.json').read_bytes())
S=A/'priority_audit/stage3_current_priority'
sources={x['id']:x for x in json.loads((S/'SOURCE_INVENTORY.json').read_bytes())['sources']}
for key,title,scope in [
 ('verdure2006','Verdure, Lagrange resolvents and torsion of elliptic curves, IJPAM33(1)(2006),75-92','Original printed75,80-88 visually read; operative Proposition3/Corollary1 and Theorem5/specialization proof.'),
 ('morton2016_v1','Morton, Product formulas for the5-division points, arXiv1612.06268v1, December19,2016','Original operative text/pixels3-5; old table, radical and complementary coordinate theorem.'),
 ('morton2018_v4','Morton, Product formulas for the5-division points, arXiv1612.06268v4, June11,2018; JNT200(2019),380-396','Original operative text5-9,18 and pixels5,6,7,18; publisher version-of-record identity not asserted.')]:
    v=sources[key];refs['primary_dependencies'].append(dict(title=title,url=v['canonical_url'],sha256=v['source_sha256'],root_read_scope=scope))
refs['priority_audit']='Root externally closed bounded investigation; no first-discovery/application or continuing-openness certificate. Full final public source/search/reading/version ledgers accompany the package.'
refs['priority_source_inventory_sha256']=sha((S/'SOURCE_INVENTORY.json').read_bytes())
refs['mathematical_scope']='Explicit characteristic-zero regular-pentagon equation normalization, including every elliptic member; separate source variants unproved.'
(A/'preprint/SOURCE_REFERENCES_CURRENT.json').write_text(json.dumps(refs,indent=2)+'\n')
binding=A/'root_preprint_private/pdf_export_v5/source_pdf_binding.json'
b=json.loads(binding.read_bytes())
assert b['source_before']==b['source_after']==dict(bytes=(O/'pentagonal-torsion-note.tex').stat().st_size,sha256=sha((O/'pentagonal-torsion-note.tex').read_bytes()))
assert b['pdf']==dict(bytes=(O/'pentagonal-torsion-note.pdf').stat().st_size,sha256=sha((O/'pentagonal-torsion-note.pdf').read_bytes()))
receipt=json.loads((A/'root_runs_private/preprint_pdf_render005/execution.json').read_bytes())
assert receipt['exit_code']==0 and receipt['stderr_bytes']==0
images=sorted((A/'root_preprint_private/pdf_v05').glob('page-*.png'));assert len(images)==7
utc=datetime.now(timezone.utc).isoformat()
qa=dict(utc=utc,status='PASS_ROOT_VISUAL_QA_CURRENT_SOURCE_PDF_PAIR',source=b['source_after'],pdf=b['pdf'],
    binding_sha256=sha(binding.read_bytes()),native_render_receipt_sha256=sha((A/'root_runs_private/preprint_pdf_render005/execution.json').read_bytes()),
    observed_scope='Root visually inspected all7rendered pages in the conversation after actual native rendering. No clipping, overflow, missing glyph, broken table or reference layout issue identified.',
    images=[dict(path=str(p.relative_to(A)),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in images],
    mathematical_verification_percent=100,priority_percent=100,workflow_percent=55,preprint_ready=False)
(A/'ROOT_PDF_QA005.json').write_text(json.dumps(qa,indent=2)+'\n')
note=f'\n* **{utc}.** PR329 current mathematical gate includes externally replayed uniform plane-primitivity addendum. Bounded priority audit externally closed:809held files/modes,50source-ledger rows,25exact comparisons on bothPython versions; classical Verdure/Morton inputs credited globally. Current source-bound7pagePDF visually inspected after native clean export/render. Mathematics100%, priority100%, publication workflow55%; full-preprint adversaries/merge/deposit/tracker remain pending.\n'
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write(note)
p=P/'inventory.json';j=json.loads(p.read_bytes());row=next(x for x in j['items'] if x['number']==329)
row.update(audit_workflow_percent=55,workflow_percent=55,mathematical_gate='PASS_ROOT_CURRENT_COMPLETE_MATHEMATICAL_GATE_PR329',priority_complete=True,priority_percent=100,preprint_ready=False,publication_ready=False)
p.write_text(json.dumps(j,indent=2)+'\n')
p=P/'SHARED_GIT_WINDOW_STATUS.json';j=json.loads(p.read_bytes())
j.update(utc=utc,descending_329_workflow_percent=55,descending_329_priority_complete=True,descending_329_priority_percent=100,descending_329_preprint_ready=False)
p.write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps(dict(utc=utc,status=qa['status'],priority_percent=100,workflow_percent=55),indent=2))
