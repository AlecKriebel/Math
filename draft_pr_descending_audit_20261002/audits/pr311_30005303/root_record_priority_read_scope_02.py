"""Record completed root primary reads in NEW files while tracked bodies are held."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,stat
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent;sha=lambda b:hashlib.sha256(b).hexdigest()
held=json.loads((P/'private_shared_pause_pr66_math_20261004/PAUSE_ACKNOWLEDGEMENT.json').read_bytes())
for rel,pin in held['dirty_tracked_body_mode_pins_after_status_acknowledgement'].items():
    if rel.startswith('draft_pr_descending_audit_20261002/'):
        p=R/rel;assert sha(p.read_bytes())==pin['sha256'] and stat.S_IMODE(p.stat().st_mode)==pin['mode']
renders=json.loads((A/'ROOT_PRIORITY_PAGE_RENDERS.json').read_bytes())
for item in renders['renders']:assert sha(Path(item['image_path']).read_bytes())==item['image_sha256']
stamp=datetime.now(timezone.utc).isoformat()
law=json.loads((A/'ROOT_PRIORITY_LAW_CHECKS.json').read_bytes());assert law['status']=='PASS_PRIOR_LAWS_AND_EXACT_SUBMITTED_ROTATION'
j=dict(actual_utc=stamp,status='ROOT_PRIMARY_LAW_COMPARISON_AND_VISUAL_SCOPE_RECORDED',
    mathematical_percent=100,priority_percent=60,workflow_percent=40,priority_complete=False,publication_ready=False,
    root_independent_law_verification=dict(path='ROOT_PRIORITY_LAW_CHECKS.json',sha256=sha((A/'ROOT_PRIORITY_LAW_CHECKS.json').read_bytes())),
    actually_visually_read_pages=[dict(label=Path(x['image_path']).stem,png_sha256=x['image_sha256'],source_pdf_sha256=x['source_sha256']) for x in renders['renders']],
    primary_body_read_scope={
        'GMS2006':'Definitions/A-feasibility lemmas and Theorems3.1/3.2/3.3/3.4; C4 quartet list, Examples7/8 and surrounding context through start of4.6; printed1480 visual. Not entire30-page paper.',
        'LUZ1905v3':'Introduction/definitions, Example4.7, all section4.4 through Corollary4.14 and reference list. Not entire33-page paper.',
        'Fallat1510v2':'Introduction/definitions, support conditions/Proposition3.4/3.5/Example3.6, selected section5 independence context, all section7.1 through positive-only Theorem7.5, selected discussion and beginning refs. Not entire35-page paper.',
        'KS2411v1':'Introduction/definitions through section3 C4 ideals; full sections4/5 through Theorem5.5; Example6.5 and section7/references. Visualp7/p13. Section6 main proof not yet fully read; not claiming full15-page read.',
        'GL2016':'Decisive Lemmas5.1/5.2 full proof printed415–417, surrounding section6 through Example6.3 start and preceding context. Visual415/416/417. Publisher date page title/authors/DOI/date metadata and received/accepted/published milestones only.',
        'KZ2004':'Theorem4.1 and full section4.1 construction; section6 residual-graph argument and surrounding definitions/lemma, printed151 visual. Not entire13-page paper.',
        'PQ1979':'Institutional cover metadata, section2 definitions, TheoremI full proof and propositions/contraction discussion through printed6. Not full24-page report.',
        'KR2007':'PDF authenticated and downloaded; source body not yet root-read.'},
    publisher_date_capture=dict(path='root_runs_private/pr311_priority_GL_publisher_date_actual001/stdout.bin',bytes=22522,sha256='38defe83c24930f1ef77d5516e983deebf46b016e52b5c7be36f4c4fa7684d81',publication_date='2017-04-13',issue_year='2016',scope='metadata and milestones only'),
    staged_independent_priority_families=['priority_factorization','priority_closure','closure_priority_adversary'],
    current_exact_gap='C1 historical novelty/routine-specialization judgment; all whole final priority reports still to be root-read/authenticated.',
    shared_git_writes_paused=True,owned_dirty_tracked_bodies_modes_unchanged_since_ack=True,outbound_message_sent=False)
for name in ['ROOT_PRIORITY_READ_SCOPE_02.json','READ_ONLY_PRIORITY_CHECKPOINT_02.md']:assert not (A/name).exists()
(A/'ROOT_PRIORITY_READ_SCOPE_02.json').write_text(json.dumps(j,indent=2)+'\n')
(A/'READ_ONLY_PRIORITY_CHECKPOINT_02.md').write_text(stamp+' — ROOT read-only checkpoint during exclusive PR66 shared Git window. Exact prior C4 law comparison, publication13April2017, seven primary page visual reads and precise limited source-body scope recorded. Mathematics100%, priority60%, workflow40%. The whole C1 historical judgment remains pending; a fresh adversary independently tests whether a prior-framework derivation contains a substantive new bridge. No Git/index/QUEUE/history writes, publication, merge or outside communication; held owned tracked bytes/modes authenticated unchanged.\n')
print(json.dumps(j,indent=2))
