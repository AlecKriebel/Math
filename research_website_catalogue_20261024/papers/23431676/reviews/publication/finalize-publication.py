"""Finalize root-cleared editorial bindings only; never render or alter sources."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import hashlib, json, re, zipfile

ROOT = Path(__file__).resolve().parents[4]
P = ROOT / 'papers/23431676'
O = P / 'reviews/publication'
NOW = datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def out(name, value):
    (O/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
checks=[]
def check(name, value):
    checks.append({'name':name,'passed':bool(value)})
    if not value: raise ValueError(name)

# Snapshot all immutable sources and all three scientific review families.
frozen={}
for base in [P/'sources', *(P/'reviews'/r for r in ['analytic','adversarial','scope'])]:
    for path in sorted(base.rglob('*')):
        if path.is_file(): frozen[str(path.relative_to(P))]={'bytes':path.stat().st_size,'sha256':sha(path)}
out('finalization-preservation-before.json', {'utc':NOW,'files':frozen})
receipt_path=P/'sources/receipt.json'; receipt=json.loads(receipt_path.read_text())
record=json.loads((P/'sources/record.json').read_text())
clearance_path=ROOT/'verification/root-clearance-23431676-20261025.json'
clearance=json.loads(clearance_path.read_text()); clearance_hash=sha(clearance_path)
c=json.loads((O/'publication.draft.json').read_text())
check('root_PASS_exact_record',clearance['status']=='PASS' and clearance['record_id']=='23431676' and clearance['disposition_by']=='root')
check('raw_receipt_bound_and_unmodified_shape',sha(receipt_path)==clearance['source_receipt_sha256'] and 'assets' in receipt and 'files' not in receipt)
check('metadata_identity',sha(P/'sources/record.json')==receipt['record_sha256']==c['source_binding']['metadata_sha256'])
assets=receipt['assets']
check('all_published_assets_listed', {a['name'] for a in assets}=={c['pdf_filename'],*(x['filename'] for x in c['additional_assets'])})
for a in assets:
    data=(P/'sources'/a['name']).read_bytes()
    check('asset_'+a['name'],len(data)==a['bytes'] and hashlib.sha256(data).hexdigest()==a['sha256'] and hashlib.md5(data).hexdigest()==a['md5'])
extraction=json.loads((P/'sources/extraction-integrity.json').read_text())
with zipfile.ZipFile(P/'sources/pr1097_support_v1_0.zip') as z:
    check('ZIP_CRC',z.testzip() is None)
    check('all_198_archive_members',len(z.infolist())==len(extraction['regular_files'])==198)
    for m in extraction['regular_files']:
        raw=z.read(m['member']); disk=Path(m['path']).read_bytes()
        check('member_'+m['member'],raw==disk and len(raw)==m['bytes'] and hashlib.sha256(raw).hexdigest()==m['sha256'])
tex_path=P/c['source_binding']['source_tex_path']; tex=tex_path.read_text()
check('tex_bound',sha(tex_path)==c['source_binding']['source_tex_sha256'])
raw_abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
normalized=' '.join(raw_abstract.replace("T\\'othm\\'er\\'esz",'Tóthmérész').split())
check('full_actual_source_abstract',normalized==c['abstract'])
check('abstract_125_words',len(normalized.split())==125)
check('printed_date_version',r'\date{15 October 2026, version 1.0}' in tex)
policy=clearance['publication_date_policy']
check('exact_date_policy',c['publication_date']==record['metadata']['publication_date']==policy['publication_date']=='2026-10-15' and c['publication_date_label']==policy['publication_date_label']=='Manuscript dated' and c['source_binding']['record_created_utc']==record['created']==policy['record_created_utc']=='2026-10-17T05:45:36.045033+00:00')
check('version_matches',c['version']==record['metadata']['version']=='1.0')
check('followup_null',c['follow_up'] is None and clearance['follow_up'] is None)

# Preserve source-bound public wording; add the explicit singleton convention.
c['result'][1]+=' In the one-vertex loopless case, reachability is exactly equality of the two configurations.'
for k in ['candidate_only','candidate_gate']: c.pop(k,None)
c['source_binding']['files']=deepcopy(assets)
c['source_binding']['receipt_asset_field']='assets'
c['source_binding']['source_receipt_sha256']=sha(receipt_path)
c['source_binding']['review_boundary']='Exact unchanged scientific verdict objects are preserved in promotion.json. The frozen scope verdict predates root clearance and remains unchanged; the later root decision clears the exact stated theorem. These are AI reviews, not external human peer review or proof-assistant certification.'
c['source_binding']['publication_state']='BINDINGS_READY_RENDERING_PENDING'
c['review_metadata']={
    'prepared_utc':NOW,'completion_percent':100,'scientific_clearance_received':True,
    'root_clearance_file':str(clearance_path.relative_to(ROOT)), 'root_clearance_sha256':clearance_hash,
    'publication_state':'BINDINGS_READY_RENDERING_PENDING','rendered':False,'deployed':False,
    'editor_authorization':'Root authorized paper-specific publication and promotion bindings only. Shared rendering, checker changes, deployment, browser checks, redirects and spreadsheet tracking remain with the designated editor/root.'}
write(P/'publication.json',c)
reviews={}
for role,b in clearance['reviews'].items():
    report=ROOT/b['report']; verdict=ROOT/b['verdict']
    check(role+'_complete_report_hash',sha(report)==b['report_sha256'])
    check(role+'_complete_verdict_hash',sha(verdict)==b['verdict_sha256'])
    reviews[role]={'report':str(report.relative_to(P)),'sha256':sha(report),
        'verdict_file':str(verdict.relative_to(P)),'verdict_sha256':sha(verdict),
        'verdict':json.loads(verdict.read_text()),
        'root_disposition':'SCOPE_COMPLETE' if role=='scope' else 'PASS'}
gate={
    'record_id':'23431676','status':'PASS','disposition_by':'root','created_utc':NOW,
    'approved_scope':clearance['approved_scope'],
    'root_clearance':clearance['authorization'],
    'root_clearance_file':str(clearance_path.relative_to(ROOT)),
    'root_clearance_sha256':clearance_hash,'root_clearance_record':clearance,
    'pdf_sha256':clearance['pdf_sha256'],'supplement_sha256':None,
    'publication_sha256':sha(P/'publication.json'),
    'source_receipt_sha256':sha(receipt_path),'source_receipt_asset_field':'assets',
    'source_files':deepcopy(assets),'reviews':reviews,
    'scope_gate_resolution':clearance['scope_gate_resolution'],
    'source_repair':False,'human_peer_review':False,'formal_machine_verification':False,
    'follow_up':None,'preparation_state':'BINDINGS_READY_RENDERING_PENDING',
    'editorial_change_from_draft':'No abstract or theorem-scope change. Removed stale draft-only state, bound later root clearance and complete unchanged verdict objects, added the manuscript\'s explicit singleton-equality convention, and supplied an in-memory-compatible asset view while preserving the frozen receipt.'}
write(P/'promotion.json',gate)
check('complete_unchanged_verdict_objects',all(v['verdict']==json.loads((P/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
check('scope_frozen_pending_preserved',gate['reviews']['scope']['verdict']['status']=='SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING' and not gate['reviews']['scope']['verdict']['publication_authorized'])
check('publication_root_binding',gate['publication_sha256']==sha(P/'publication.json') and gate['root_clearance_sha256']==sha(clearance_path))
check('full_multigraph_scope','finite nonempty loopless strongly connected directed multigraphs' in c['result'][0].lower() and all(w in ' '.join(c['result']) for w in ['nonnegative','binary','empty firing word','may stop','Malformed inputs','one-vertex']))
check('HKT_credit',any('Hujter, Kiss and Tóthmérész supplies coNP membership' in x for x in c['result']))
check('no_extended_model',all(x in ' '.join(c['limitations']) for x in ['simple graphs','unary encodings','bounded degrees','bounded total chip counts','Signed intermediate']))
check('date_qualification',all(x in c['edition_note'] for x in ['15 October 2026','created on 17 October 2026','not verified public availability','Neither date establishes first priority']))
check('AI_unrefereed_scope','Unrefereed preprint' in c['status'] and 'external human peer review' in c['ai_disclosure'])
check('all_frozen_sources_reviews_unchanged',all((P/name).stat().st_size==b['bytes'] and sha(P/name)==b['sha256'] for name,b in frozen.items()))
qa={'utc':NOW,'status':'EDITORIAL_BINDINGS_READY','all_checks_passed':all(x['passed'] for x in checks),'checks':checks,
    'math_helpers_executed':False,'new_mathematical_verdict':False,'rendered':False,
    'source_asset_count':len(assets),'archive_members_rehashed':198,'preserved_input_files':len(frozen),
    'independent_editorial_qa':{'agent':'/root/nmsc_adversarial/publication_crosscheck/reach_editorial_qa','draft_sha256':sha(O/'publication.draft.json'),'result':'PASS: full125-word actual-source abstract, binary/nonnegative loopless strongly connected multigraph scope, credited HKT membership, exact date/version/record timestamp, null follow-up. Read-only QA; no helpers executed.'},
    'raw_receipt_sha256':sha(receipt_path),'root_clearance_sha256':clearance_hash,
    'publication_sha256':sha(P/'publication.json'),'promotion_sha256':sha(P/'promotion.json')}
out('finalization-checks.json',qa)
print(json.dumps({'checks':len(checks),'all_passed':qa['all_checks_passed'],'publication_sha256':sha(P/'publication.json'),'promotion_sha256':sha(P/'promotion.json'),'preserved_files':len(frozen)},indent=2))
