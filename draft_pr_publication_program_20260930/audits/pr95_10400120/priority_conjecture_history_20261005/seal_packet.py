from pathlib import Path
import datetime, hashlib, json, subprocess

BASE = Path(__file__).resolve().parent
assert BASE.name == 'priority_conjecture_history_20261005'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def save(name, obj):
    (BASE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

scopes = {
 'gp_1996_v1.pdf': {
  'title': 'Three-manifold invariants and their relation with the fundamental group',
  'authors': ['E. Guadagnini', 'L. Pilo'],
  'status': 'Primary preprint full text retrieved; selected sections read',
  'read_scope': 'Extracted text lines 1–230: cover, introduction and normalization/surgery passages; lines 700–784: end of SU(2) proof, SU(3) section 5 and conclusion section 6, printed pp. 12–14. Whole extracted text searched for relevant conjecture/group/level terms. Physical PDF page 2, printed p. 1, visually inspected. No claim to read all proof lines or all 22 pages.',
  'date_support': 'Cover November 1996; arXiv record v1 submitted 9 December 1996.'},
 'gp_published.pdf': {
  'title': 'Publisher HTML for Three-Manifold Invariants and Their Relation with the Fundamental Group',
  'authors': ['E. Guadagnini', 'L. Pilo'],
  'status': 'Primary publisher metadata and abstract only; PDF attempt returned HTML',
  'read_scope': 'HTML title, publication month March 1998, journal/volume/page metadata and abstract. Extracted metadata snippets read. Body HTML navigation not treated as journal full text. .pdf extension is misleading; magic bytes/HTTP Content-Type identify HTML.',
  'date_support': 'Publisher dates the article to March 1998.'},
 'ohtsuki_2003_draft.pdf': {
  'title': 'Problems on invariants of knots and 3-manifolds, February 2003 draft',
  'authors': ['T. Ohtsuki (editor)'],
  'status': 'Draft full text retrieved; targeted passages read',
  'read_scope': 'Extracted text lines 4450–4540 including draft p. 103 Conjecture 7.5 and nearby definition context. Whole extracted text searched for conjecture/GP/fundamental-group terms. Not a full 205-page read.',
  'date_support': 'February 2003 preface; draft volume placeholders.'},
 'ohtsuki_printed.pdf': {
  'title': 'Problems on invariants of knots and 3-manifolds, printed arXiv copy',
  'authors': ['T. Ohtsuki (editor)'],
  'status': 'Primary printed full text retrieved; targeted section read',
  'read_scope': 'Extracted text lines 4730–4975, printed pp. 469–474, including full section 7.1 on pp. 471–474, plus bibliography [158] and relevant term searches. Relevant physical PDF pages 99–102 extracted for whitespace-normalized comparison with MSP, with receipt. Publication/revision metadata inspected. Not a full 200-page read.',
  'date_support': 'Volume 4 (2002); printed publication 1 June 2004; revisions through 8 April 2004.'},
 'ohtsuki_msp.pdf': {
  'title': 'Problems on invariants of knots and 3-manifolds, MSP publisher copy',
  'authors': ['T. Ohtsuki (editor)'],
  'status': 'Primary publisher full text retrieved; corroborated target passage',
  'read_scope': 'Preface extracted lines 1–60 read; physical PDF page 102, printed p. 474, visually read. Physical page 98, printed p. 470, was also displayed during an initial page-offset check. Physical pages 99–102, printed 471–474, extracted and exactly agree with the already-read arXiv target text after whitespace removal. This is corroboration, not a separate complete reading of all pages.',
  'date_support': 'Printed volume/year and preface; source has publication/revision dates.'},
 'ohtsuki_solutions.html': {
  'title': "Ohtsuki's solutions to problem-list entries",
  'authors': ['T. Ohtsuki'],
  'status': 'Primary author HTML; full small body read',
  'read_scope': 'Entire 1717-byte HTML read. Entries 1.15, 5.3, 12.17 only. Absence of 7.5 is literal in these bytes, not current open-status evidence.',
  'date_support': 'HTTP Last-Modified 18 June 2009; retrieval date does not prove recent editorial update.'},
 'kuriya_institutional.html': {
  'title': 'Kyushu COE staff record for Takahito Kuriya',
  'authors': ['Kyushu University institutional staff record'],
  'status': 'Primary institutional HTML; decoded staff entry read',
  'read_scope': 'Entire decoded Shift-JIS staff text extracted/read including research works, exact-title preprint, degree date and homepage dash. Research narrative is not used as a proved theorem.',
  'date_support': 'HTTP Last-Modified 23 April 2007; degree March 2007.'},
 'kuriya_kyushu_report.pdf': {
  'title': 'Kyushu COE report, report-6.pdf',
  'authors': ['Kyushu University COE report'],
  'status': 'Primary scanned full report retrieved; Kuriya section visually read',
  'read_scope': 'Scanned four-up PDF, 99 physical pages. Four contact sheets showing all page thumbnails visually viewed for location only, not legible full-text reading. English OCR at 600 pixels searched all 99 pages with no Kuriya match; 1800-pixel OCR of physical pages 1–41 located physical page 32. Physical page 32, printed pp. 120–123, displayed; Kuriya pp. 120–122 visually read, especially exact-title talk/date on p. 121 and preprint list. OCR text for page 32 read; Japanese OCR is noisy and was not used instead of visual reading. Other report pages not fully read.',
  'date_support': 'Printed p. 121 records 21 February 2003 talk retrospectively; PDF creation metadata August 2008.'},
 'topology_symposium_2004.pdf': {
  'title': '2004 Topology Symposium collected proceedings, ts2004all.pdf',
  'authors': ['Mathematical Society of Japan Topology Symposium proceedings'],
  'status': 'Primary scanned full proceedings retrieved; selected pages visually inspected',
  'read_scope': 'Physical pages 49, 54, 59 rendered/displayed, corresponding to printed pp. 44, 49, 54. Printed p. 44 introduction and p. 54 bibliography visually read; bibliography [12] authenticates exact Kuriya preprint. Printed p. 49 was displayed during page-offset check, not relied on for new mathematical conclusions. pdftotext yielded page separators only; not a complete proceedings read.',
  'date_support': '2004 proceedings file/collection context; preprint cited by that proceedings.'},
 'kuriya_lmo_2008.pdf': {
  'title': 'On the LMO conjecture',
  'authors': ['Takahito Kuriya'],
  'status': 'Primary preprint full text retrieved; introduction/reference scope read',
  'read_scope': 'Extracted lines 1–110, approximately pp. 1–2, plus bibliography lines 576–605. Whole text searched for GP/lens/conjecture/theorem references. Missing preprint [12] and Theorem 5.1 reduction identified. Full proof not audited.',
  'date_support': 'arXiv v1 12 March 2008.'},
 'kuriya_le_ohtsuki_2012.pdf': {
  'title': 'The perturbative invariants of rational homology 3-spheres can be recovered from the LMO invariant',
  'authors': ['T. Kuriya', 'T. T. Q. Le', 'T. Ohtsuki'],
  'status': 'Primary author-hosted journal full text retrieved; introduction/remarks read',
  'read_scope': 'Extracted lines 70–147, printed pp. 459–460: Theorem 1.1, incomplete earlier proof remark, rational-homology coprime SO(3) finite-root remark. Whole extracted text searched for lens, GP and conjecture. Abstract and metadata read. No claim to verify its entire theorem proof.',
  'date_support': 'Journal of Topology 5 (2012), 458–484, DOI 10.1112/jtopol/jts010.'},
 'guadagnini_thuillier_2010.pdf': {
  'title': 'Abelian link invariants and homology',
  'authors': ['Enore Guadagnini', 'Francesco Mancarella'],
  'status': 'Primary preprint full text retrieved; counterexample passages read',
  'read_scope': 'Extracted lines 825–940, printed pp. 15–17, plus bibliography [32] and whole-text searches for counterexamples/pi1. Displayed lens-space complex values have equal magnitudes. Stem erroneously says Thuillier; the actual cover authors control this manifest.',
  'date_support': 'arXiv 1004.5211 v1, 2010.'},
 'hikami_spherical_seifert_2005.pdf': {
  'title': 'On the quantum invariant for the spherical Seifert manifold',
  'authors': ['Kazuhiro Hikami'],
  'status': 'Primary preprint full text retrieved; targeted GP passages read',
  'read_scope': 'Whole extracted text searched for GP/pi1/conjecture, and associated introduction/concluding passages read with context; the long grep output was partially truncated, so no complete-paper read is claimed. Relevant conclusion on printed p. 34 and bibliography [13], [56] inspected. Earlier Yamada text not obtained.',
  'date_support': 'arXiv v1 28 April 2005; retrieved current PDF is v2 revised 8 May 2006.'},
 'lens_handlebodies_1998.pdf': {
  'title': 'Lens spaces and handlebodies in 3D quantum gravity',
  'authors': ['Radu Ionicioiu', 'Ruth M. Williams'],
  'status': 'Primary preprint full text retrieved; beginning/lens formulas read',
  'read_scope': 'Extracted lines 1–226, approximately cover and pp. 1–4, including L(5,1)/L(5,2) formulas. Whole text searched for GP/pi1/conjecture. No GP name found in this retrieved v1; index-level citation attribution not promoted to a primary textual citation. Not a full proof read.',
  'date_support': 'arXiv v1 5 June 1998.'},
 'garoufalidis_le_marino_2008.pdf': {
  'title': 'Analyticity of the free energy of a closed 3-manifold',
  'authors': ['Stavros Garoufalidis', 'Thang T. Q. Le', 'Marcos Marino'],
  'status': 'Primary journal full text retrieved; lens-series passages read',
  'read_scope': 'Extracted lines 581–626, printed pp. 11–12, including Proposition 6.1 lens-space formal series, and relevant references [40], [52]. Whole text searched for Kuriya/lens/Proposition 6.1. No finite-level SU(5) calculation performed.',
  'date_support': 'SIGMA 4 (2008), 080.'},
 'spinfoam_survey_2003.pdf': {
  'title': 'Spin Foam Models of Quantum Spacetime',
  'authors': ['Daniele Oriti'],
  'status': 'Primary thesis full text retrieved; targeted historical testimony read',
  'read_scope': 'Cover lines 1–30 read and author/title verified. Extracted lines 4860–4990, printed pp. 123–126, read, plus targeted grep snippets on p. 128 and bibliography [149]. Whole extracted text searched for GP/fundamental group/conjecture; output truncated outside relevant focus. This is not a 300-plus-page read and not a primary independent proof of global unresolved status.',
  'date_support': 'Cover 2003; arXiv v1 20 November 2003.'},
 'inspire_gp_citations.json': {
  'title': 'INSPIRE GP citing-record lookup',
  'authors': ['INSPIRE discovery index'],
  'status': 'Citation metadata only; not mathematical evidence',
  'read_scope': 'Four returned records examined in processed selection JSON. Mathematical citing texts fetched where accessible. A closed 2000 6j article and an anyon-thermodynamics thesis entry remain unread background leads; no exhaustive citation coverage claimed.'},
 'semantic_gp_citations.json': {
  'title': 'Semantic Scholar GP DOI citations',
  'authors': ['Semantic Scholar discovery index'],
  'status': 'Citation metadata only; not mathematical evidence',
  'read_scope': 'All five returned entries read. No next page in returned JSON; this does not prove exhaustive worldwide citation coverage.'},
 'kuriya_wayback_index.json': {
  'title': 'Wayback CDX lookup of inferred Kyushu author user path',
  'authors': ['Internet Archive CDX discovery index'],
  'status': 'Empty public index response, not a preprint source',
  'read_scope': 'Entire three-byte response read: []. Path inferred from institutional account name, not verified homepage. Other paths/hosts not exhaustively checked.'},
 'cinii_kuriya_search.xml': {
  'title': 'Old CiNII search endpoint response',
  'authors': ['CiNII public site'],
  'status': 'Uninformative redirect to generic HTML home page, not XML search results',
  'read_scope': 'HTTP final URL and true content type inspected. Generic 117243-byte HTML not treated as an exact-title result set or fully read. .xml extension misleading.'},
}

started = now()
records = []
for rp in sorted((BASE / 'receipts').glob('*.retrieval.json')):
    r = json.loads(rp.read_text())
    row = {'retrieval_receipt': str(rp.relative_to(BASE)), 'retrieval': r}
    saved = r.get('saved_as')
    if saved:
        p = BASE / saved
        assert p.exists()
        data = p.read_bytes()
        assert len(data) == r['bytes'] and hashlib.sha256(data).hexdigest() == r['sha256']
        row.update(scopes[p.name])
        row['bytes_verified_at_seal'] = len(data)
        row['sha256_verified_at_seal'] = digest(p)
        row['true_content_format'] = 'PDF' if data.startswith(b'%PDF') else ('HTML' if b'<html' in data[:4096].lower() or p.suffix == '.html' else 'JSON')
        if data.startswith(b'%PDF'):
            info = subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True,check=True).stdout
            row['pdfinfo'] = {line.split(':',1)[0].strip():line.split(':',1)[1].strip() for line in info.splitlines() if ':' in line}
            row['physical_pdf_pages'] = int(row['pdfinfo']['Pages'])
    else:
        row['status'] = 'Retrieval failed; no source bytes obtained'
        row['read_scope'] = 'HTTP 429 error only. Not a negative title result.'
    records.append(row)

gate = BASE.parent / 'ROOT_MATHEMATICAL_GATE_20261005.json'
gate_record = {'path': str(gate), 'bytes':gate.stat().st_size,'sha256':digest(gate),'read_scope':'Entire parent mathematical gate JSON read as intake; no prior priority reviews read.'}
save('SOURCE_READ_MANIFEST.json',{
 'created_utc':now(),
 'policy':'Raw source URL/time/bytes/hash authenticated; access and human read scope distinct. Full text retrieval or OCR never implies full text human reading. Source bytes remain private.',
 'intake':gate_record,
 'sources':records,
 'not_obtained':[{
  'title':'The LMO invariant and the Guadagnini-Pilo conjecture for lens spaces',
  'author':'Takahito Kuriya',
  'classification':'Directly relevant full-text gap',
  'authenticated_primary_bibliographic_sources':['kuriya_institutional.html','kuriya_kyushu_report.pdf printed p. 121','topology_symposium_2004.pdf printed p. 54, reference [12]','kuriya_lmo_2008.pdf reference [12]'],
  'aggregator_only':'ResearchGate exact-title page: abstract only, no full text. Actual web tool text retained in receipts/web_open_18.json; primary bibliographic authentication does not authenticate that abstract.',
  'no_outreach':True
 },{
  'title':'The absolute value of the Chern-Simons-Witten invariants of lens spaces',
  'author':'S. Yamada', 'date':'1995',
  'classification':'Unread earlier rank-one background source; title/journal/page bibliography authenticated in inspected primary works, full text not obtained'
 }],
 'web_tool_read_policy':'Actual returned search/open/find text retained in receipts/web_*.json. Metadata and selected snippets reviewed; returned linked documents are not automatically full-text reads. Older literal query arguments not separately persisted; see SEARCH_LEDGER.md.'
})

disposition = {
 'closed_utc':now(), 'family':'Original conjecture scope, history, updates and citing resolutions',
 'target_scope_confirmed':True,
 'earlier_finite_full_su5_refutation_authenticated_in_this_family':False,
 'novelty_cleared':False,
 'reason':'Directly relevant Kuriya preprint full text not obtained; bounded negative search is not proof of absence; explicit higher-rank priority family separate.',
 'publication_authority':False,
 'original_author_budget':'2/5, unchanged',
 'new_central_proof_search_turns':0,
 'outside_outreach':False,
 'git_or_service_mutations':False,
 'bounded_audit_completion_estimate_percent':100,
 'worldwide_novelty_status':'Unestablished',
 'report':'REPORT.md','source_read_manifest':'SOURCE_READ_MANIFEST.json','search_ledger':'SEARCH_LEDGER.md','file_manifest':'FILE_MANIFEST.json'
}
save('FINAL_DISPOSITION.json',disposition)
log = BASE / 'RESEARCH_LOG.md'
log.write_text(log.read_text() + '\n- ' + disposition['closed_utc'] + ' closure checkpoint: bounded historical priority audit 100% complete within its declared stop rule. Printed target scope confirmed; no earlier finite full SU(5) magnitude refutation authenticated in inspected family; worldwide novelty remains unestablished and is not cleared. Direct Kuriya full-text gap retained. Kyushu physical PDF p. 32, printed p. 121, visually verifies retrospective 21 February 2003 exact-title talk. Oriti cover verified and report attribution corrected to sole author Daniele Oriti. Ohtsuki target copies agree after whitespace removal. Every retrieved raw source rehashed against HTTP receipt; source/read and full file manifests sealed. Original author budget 2/5; zero new central proof-search turns; no outreach, Git, service, PR, UI or publication action.\n')

seal_names = ['OBLIGATIONS.md','REPORT.md','RESEARCH_LOG.md','SEARCH_LEDGER.md','SOURCE_READ_MANIFEST.json','FINAL_DISPOSITION.json','retrieve.py','seal_packet.py']
save('SEAL.json',{'sealed_utc':now(),'started_verification_utc':started,'status':'PRIVATE_BOUNDED_PRIORITY_PACKET_CLOSED_NOVELTY_NOT_CLEARED','core_artifacts':[{'path':n,'bytes':(BASE/n).stat().st_size,'sha256':digest(BASE/n)} for n in seal_names],'file_manifest_note':'FILE_MANIFEST.json is written after SEAL.json and includes SEAL.json. It excludes itself to avoid a self-hash cycle; its external SHA-256 is reported to ROOT.'})

viewed = {'gp_page_2.png','ohtsuki_msp_page_98.png','ohtsuki_msp_page_102.png','topology_symposium_page_54.png','topology_symposium_page_49.png','topology_symposium_page_59.png','kyushu_readable-32.png'}
files = []
for p in sorted(BASE.rglob('*')):
    if not p.is_file() or p.name == 'FILE_MANIFEST.json': continue
    rel = str(p.relative_to(BASE))
    if p.name in viewed:
        role = 'Source PDF raster displayed to model; specific human read scope in source manifest'
    elif p.name.startswith('kyushu_contact_'):
        role = 'Contact sheet visually inspected for page location only, not legible full-text read'
    elif p.suffix in ['.png','.jpg']:
        role = 'Generated PDF raster; not individually displayed or human-read unless listed in source manifest'
    elif '.ocr.' in p.name:
        role = 'Machine English OCR output; searched as locator, no human full-page read except page 32 output'
    elif p.name in scopes:
        role = scopes[p.name]['status']
    elif rel.startswith('receipts/web_'):
        role = 'Actual web tool result receipt; search/open/find scope and limitations in ledger'
    elif rel.startswith('receipts/'):
        role = 'Retrieval/extraction/comparison/OCR receipt; tool metadata, not additional full-paper reading'
    elif p.suffix == '.txt' and rel.startswith('sources/'):
        role = 'Derived PDF/HTML text extraction; actual selected read scope recorded for raw source'
    else:
        role = 'Private audit document or reproducible local retrieval/seal code'
    files.append({'path':rel,'bytes':p.stat().st_size,'sha256':digest(p),'role_and_read_scope':role})
save('FILE_MANIFEST.json',{'sealed_utc':now(),'base':str(BASE),'excluded_self':'FILE_MANIFEST.json','file_count':len(files),'total_retained_bytes_excluding_self':sum(x['bytes'] for x in files),'files':files})
print(json.dumps({'sealed_utc':now(),'source_records':len(records),'files':len(files),'core_hashes':[{'path':n,'bytes':(BASE/n).stat().st_size,'sha256':digest(BASE/n)} for n in ['REPORT.md','SOURCE_READ_MANIFEST.json','FILE_MANIFEST.json','FINAL_DISPOSITION.json','SEARCH_LEDGER.md','RESEARCH_LOG.md','SEAL.json']]},indent=2))
