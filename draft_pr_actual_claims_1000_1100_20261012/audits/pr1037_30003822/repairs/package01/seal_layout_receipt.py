#!/usr/bin/env python3
"""Record completed individual page inspection; no compilation or network."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
ROOT=Path(__file__).resolve().parents[2]
OWN=Path(__file__).resolve().parent
PRE=ROOT/'preprint'
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
now=datetime.now(timezone.utc).isoformat()
pdf=pin(PRE/'paper/forest_transfer_catalan.pdf')
tex=pin(PRE/'paper/forest_transfer_catalan.tex')
pages=sorted((OWN/'render').glob('page-*.png'));assert len(pages)==12
notes=[
 'Title, sole author/ORCID, abstract, exact Ferudun credit, extensive AI/unrefereed disclosure and introduction legible.',
 'Qualified chronology, full Bell normalization and theorem with same-conclusion credit legible.',
 'Incidence/tree proof, integer lattice and paired extraction convention fit cleanly.',
 'Subset transfer proof, coefficient +1, fixed-tree scope and constant image setup legible.',
 'Weight-space calculation and epsilon tensor basis display cleanly.',
 'Leading-word proof, antisymmetrization, quadratic identities, surjection and dimension formula legible.',
 'Catalan sum, degree symmetry, determinant character and Gaussian setup fit cleanly.',
 'Completion, normalized lowering and raising definitions legible.',
 'Raising conclusion, row hyperplane, ordered factorization and lifting setup legible.',
 'Constant-kernel and integral descent, n=1 boundary and source interfaces legible.',
 'Dated addendum and Section7 stable review history/frozen-input wording are fully visible, including both filenames; no footer overlap.',
 'All twelve bibliography entries and license footer fit cleanly; no clipping or overlap.'
]
inspection={'utc':now,'scope':'Repair layout verification; every actual new exported page individually viewed via view_image, not contact sheets. Not independent mathematical or NEW whole-package review.',
 'render_command':['pdftoppm','-r','110','-png','preprint/paper/forest_transfer_catalan.pdf','repairs/package01/render/page'],
 'pdf':pdf,'tex':tex,'pages':[{'page':i+1,'path':p.relative_to(ROOT).as_posix(),**pin(p),'individually_viewed':True,'finding':notes[i]} for i,p in enumerate(pages)],
 'visual_defects':[],'all_pages_rendered':True,'all_pages_individually_viewed':True}
write(OWN/'PAGE_INSPECTION.json',inspection)
compile=json.loads((OWN/'COMPILE_EXPORT_RECEIPT.json').read_text())
assert compile['exit_code']==0 and compile['built_in_saved_source_compile']['source_sha256']==tex['sha256']
write(PRE/'BUILD_RECEIPT.json',{
 'utc':now,'stage':'repair_20261013_package01','saved_tex':'paper/forest_transfer_catalan.tex','pdf':'paper/forest_transfer_catalan.pdf',
 'built_in_compile':'success on repaired saved source; no artifact marker repeated',
 'built_in_compile_source_sha256':tex['sha256'],'export_command':compile['command'],'export_exit_code':0,
 'disk_export_then_byte_exact_copy':True,'export_log_has_overfull_or_undefined':False,
 'pages':12,'render_command':inspection['render_command'],'all_pages_rendered':True,'all_pages_individually_viewed':True,
 'visual_inspection':'All twelve 110-dpi rendered pages individually viewed. No clipping, overlap, missing glyph, blank page, numbering defect or displaced license footer. Section7 stable review-history/frozen-input wording is complete and legible on page11.',
 'paper_bytes':pdf['bytes'],'paper_sha256':pdf['sha256'],'tex_bytes':tex['bytes'],'tex_sha256':tex['sha256'],
 'previous_exact_receipt':{'path':'history/preparation_20261013_01/BUILD_RECEIPT.json',**pin(PRE/'history/preparation_20261013_01/BUILD_RECEIPT.json'),'byte_identical_to_pre_repair_receipt':True},
 'local_export_and_page_receipts':['../repairs/package01/COMPILE_EXPORT_RECEIPT.json','../repairs/package01/PAGE_INSPECTION.json'],
 'skill_marker':'Earlier preparation marker completed exactly once; not repeated during this repair.',
 'review_scope':'Dated repair layout verification only; not independent mathematical or NEW whole-package clearance. Current candidate requires NEW whole review02.'
})
with (OWN/'REPAIR_LOG.md').open('a') as f:f.write(f'\n{now} — Repaired saved source compiled successfully with the built-in compiler; Tectonic disk export succeeded with no overfull/undefined-reference warning. All twelve new pages individually rendered and viewed, with clean page11 review-history wording and unchanged visible proof/source framing. Preserved byte-exact previous BUILD_RECEIPT. Completion estimate for assigned P3 repair: 85%.\n')
print(json.dumps({'pdf':pdf,'tex':tex,'pages':len(pages),'visual_defects':[]},indent=2))
