"""Finalize only the root-cleared BV paper, preserving source and review bytes."""
from pathlib import Path
import datetime, hashlib, json, re, zipfile

R = Path(__file__).resolve().parents[4]
P = R / 'papers/23572690'
O = P / 'reviews/publication'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def save(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
c = read(O/'publication.draft.json')
cp = R/'verification/root-clearance-23572690-20261025.json'
clearance = read(cp)
receipt = read(P/'sources/receipt.json')
record = read(P/'sources/record.json')
assert clearance['record_id'] == '23572690' and clearance['status'] == 'PASS'
assert clearance['disposition_by'] == 'root'
assert sha(P/'sources/receipt.json') == clearance['source_receipt_sha256'] == c['source_binding']['receipt_sha256']
assert sha(P/'sources/record.json') == c['source_binding']['metadata_sha256']
assert all(c[k] == record['metadata'][k] for k in ['title','doi','publication_date','version'])
assert record['created'] == c['source_binding']['record_created_utc']
for asset in receipt['files']:
    path = P/'sources'/asset['name']; data = path.read_bytes()
    assert len(data) == asset['bytes'] and sha(path) == asset['sha256']
    assert hashlib.md5(data).hexdigest() == asset['md5']
    if path.suffix == '.zip':
        with zipfile.ZipFile(path) as z: assert z.testzip() is None
assert sha(P/'sources'/c['pdf_filename']) == clearance['pdf_sha256']
source_path = P/c['source_binding']['source_tex_path']
assert sha(source_path) == c['source_binding']['source_tex_sha256']
source = source_path.read_text()
raw = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1)
abstract = ' '.join(raw.split())
for old,new in {
    r'\(0\ne h\in k[x]\)':'0≠h∈k[x]',
    r'\(A_h=k\langle x,Y\rangle/(Yx-xY-h(x))\)':'A_h=k⟨x,Y⟩/(Yx−xY−h(x))',
    r'\(k\)':'k',r'\(h\)':'h','Batalin--Vilkovisky':'Batalin–Vilkovisky','~':' ',
}.items(): abstract = abstract.replace(old,new)
assert abstract == c['abstract'] == (O/'abstract_original.txt').read_text().strip()
assert len(abstract.split()) == 114
assert r'\date{22 October 2026\\\small Preprint, version 1.0.0}' in source
assert c['follow_up'] is None
reviews = {}
for family, binding in clearance['reviews'].items():
    report, verdict = R/binding['report'], R/binding['verdict']
    assert sha(report) == binding['report_sha256']
    assert sha(verdict) == binding['verdict_sha256']
    original = read(verdict)
    reviews[family] = {
        'report':str(report.relative_to(P)), 'sha256':sha(report),
        'verdict_file':str(verdict.relative_to(P)), 'verdict_sha256':sha(verdict),
        'verdict':original,
        'root_disposition':'SCOPE_COMPLETE' if family == 'scope' else 'PASS',
    }
for key in ['candidate_only','candidate_gate']: c.pop(key,None)
c['supplement_filename'] = 'bv-generators-source-and-verification.zip'
c['supplement_label'] = 'Source and verification package (ZIP)'
c['additional_assets'] = []
supplement_sha = sha(P/'sources'/c['supplement_filename'])
c['source_binding'].update({
    'files':receipt['files'], 'source_receipt_sha256':sha(P/'sources/receipt.json'),
    'supplement_sha256':supplement_sha,
    'publication_state':'ROOT_CLEARED_LOCAL_RENDER_AUTHORIZED',
    'review_boundary':'Original review verdicts remain unchanged and are embedded in promotion.json. The later root clearance resolves frozen scope-only pending wording. Internal AI review is not external human peer review or formal proof-assistant certification.',
})
c['review_metadata'] = {
    'prepared_utc':utc, 'completion_percent':100,
    'scientific_clearance_received':True,
    'root_clearance_file':str(cp.relative_to(R)), 'root_clearance_sha256':sha(cp),
    'publication_state':'ROOT_CLEARED_LOCAL_RENDER_AUTHORIZED',
    'editor_authorization':'Finalize publication and promotion, render locally and run source/content/preservation checks. Root must inspect public copy before deployment; no deployment, Git, Sheet, UI, redirect or outreach is authorized to this editor.',
}
save(P/'publication.json',c)
gate = {
    'record_id':'23572690','status':'PASS','disposition_by':'root','created_utc':utc,
    'approved_scope':clearance['approved_scope'],'root_clearance':clearance['authorization'],
    'root_clearance_file':str(cp.relative_to(R)),'root_clearance_sha256':sha(cp),'root_clearance_record':clearance,
    'pdf_sha256':clearance['pdf_sha256'],'supplement_sha256':supplement_sha,
    'publication_sha256':sha(P/'publication.json'),
    'source_receipt_sha256':sha(P/'sources/receipt.json'),'source_files':receipt['files'],
    'reviews':reviews,'scope_gate_resolution':clearance['scope_gate_resolution'],
    'source_repair':False,'human_peer_review':False,'formal_machine_verification':False,
    'follow_up':None,'preparation_state':'ROOT_CLEARED_LOCAL_RENDER_AUTHORIZED',
}
save(P/'promotion.json',gate)
save(O/'binding-check.json',{
    'utc':utc,'record_id':'23572690','status':'PASS_BINDINGS_ONLY',
    'original_draft_sha256':sha(O/'publication.draft.json'),
    'publication_sha256':sha(P/'publication.json'),'promotion_sha256':sha(P/'promotion.json'),
    'all_public_asset_size_md5_sha256_and_zip_crc_verified':True,
    'complete_original_abstract_text_match':True,'abstract_word_count':114,
    'printed_edition_and_metadata_match':True,'full_original_verdict_objects_preserved':True,
    'root_clearance_exact_object_and_hash_bound':True,
})
with (O/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n{utc} — 65% of local publication preparation: Root clearance and all three original verdict objects bound; all assets, complete 114-word abstract and printed edition rechecked. Draft and review/source bytes unchanged. Local rendering and content/preservation QA remain.\n')
print(json.dumps({'publication':sha(P/'publication.json'),'promotion':sha(P/'promotion.json')}))
