from pathlib import Path
import datetime, hashlib, json

BASE = Path(__file__).parent
PARENT = BASE.parent
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
def save(name, value):
    (BASE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')

# Correct a discovery filename after primary metadata falsified the guessed identity.
old = BASE/'private_sources/khazraei_held_arxiv_abs.html'
new = BASE/'private_sources/excluded_time_cost_tradeoff_arxiv_2011_02446.html'
if old.exists():
    old.rename(new)
script = BASE/'retrieve_metadata.py'
script.write_text(script.read_text().replace('khazraei_held_arxiv_abs.html', new.name))
receipts = json.loads((BASE/'RETRIEVALS.json').read_text())
for item in receipts:
    if item['requested_url'] == 'https://arxiv.org/abs/2011.02446':
        item['file'] = str(new.relative_to(BASE))
        item['identity_check'] = 'Excluded: actual title is Approximating the discrete time-cost tradeoff problem with bounded depth; not the Khazraei–Held cost-distance theorem.'
save('RETRIEVALS.json', receipts)

queries = [json.loads(x) for x in (BASE/'QUERY_LOG.jsonl').read_text().splitlines()]
for query in queries[:58]:
    query['execution_period'] = '2026-10-06 04:18–04:24 UTC; logs recorded at checkpoint, not per-query clock readings'
if len(queries) == 58:
    queries.append({'number':59, 'batch':16, 'batch_query':1,
        'query':'"On packing time-respecting arborescences" "2022" "100702"',
        'method':'web.search_query', 'recorded_utc':NOW,
        'execution_period':'2026-10-06 04:27 UTC, after root supplied the lead',
        'result_file':'private_sources/web_search_batch_16_notes.json',
        'preservation':'Selected primary-result notes only; full raw tool response was not saved.',
        'interpretation_limit':'Search metadata is not theorem verification; full primary proof independently retrieved and read.'})
(BASE/'QUERY_LOG.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False)+'\n' for x in queries))
save('private_sources/web_search_batch_16_notes.json', {
    'recorded_utc':NOW, 'kind':'selected_result_notes_not_full_raw_output',
    'primary_hits':[
        {'url':'https://www.sciencedirect.com/science/article/pii/S1572528622000147','claim':'Discrete Optimization45,100702,August2022; DOI10.1016/j.disopt.2022.100702'},
        {'url':'https://pagesperso.g-scop.grenoble-inp.fr/~szigetiz/OCG/13.C-Szigeti.pdf','claim':'Accessible full author-hosted journal proof; read Theorem13pp11–12'},
        {'url':'https://pagesperso.g-scop.grenoble-inp.fr/~szigetiz/pub.html','claim':'Author publication record lists the2022 article'}]})

inputs = json.loads((BASE/'INPUT_MANIFEST.json').read_text())
rootfiles = ['ROOT_PRIOR_THEOREM_COMPARISON.md','PRIMARY_RETRIEVAL.json','ROOT_PRIOR_FINITE_CHECKS.json','private_sources/chapoullie_szigeti_2022.txt']
inputs['cross_family_read_after_independent_checkpoint_utc'] = '2026-10-06 04:27 UTC'
inputs['cross_family_inputs'] = [{'path':str(PARENT/'root_priority_20261006'/f), **digest(PARENT/'root_priority_20261006'/f)} for f in rootfiles]
inputs['independence'] = 'Initial16-query comparison and own58-query search completed before reading the root comparison; source proof subsequently fetched independently.'
save('INPUT_MANIFEST.json', inputs)

statuses = {
 'cable_trench_2025.pdf':'Full PDF retrieved; journal section2.2pp9–11 and references read; other analysis unread.',
 'cable_trench_arxiv_2312_13810v1.pdf':'Full v1 PDF retrieved; corresponding hardness discussion and references read; other analysis unread.',
 'optima85.pdf':'Full PDF retrieved; Kaibel spanning-tree/Wong discussion read; other contributions unread.',
 'combining_linear_nonlinear_preprint.pdf':'Full PDF retrieved; definitionspp2–3, X3C setup, Theorem4.1 construction and Theorem4.3 full proof read; Theorem4.3 scan visually checked; other sections not fully audited.',
 'khazraei_held_ucdg_preprint.pdf':'Full author PDF retrieved; objective equation 1, section 2/Theorem 1 full 3SAT construction and proof read; approximation proofs unread.',
 'kaibel_scale_free_2005_13703.pdf':'Full PDF retrieved; concrete degree-index objectives read and whole text term-searched; remaining proofs unread.',
 'kaibel_source_detection_9002.pdf':'Full PDF retrieved; concrete oracle-query definition read and whole text term-searched; remaining proofs unread.',
 'kaibel_steiner_cut_2209_14802.pdf':'Full PDF retrieved; introduction and concrete definitions read and whole text term-searched; remaining proofs unread.',
 'kaibel_rock_extensions_2307_05246.pdf':'Full PDF retrieved; introduction and concrete definitions read and whole text term-searched; remaining proofs unread.',
 'kaibel_ef_arxiv_1104_1023v1.pdf':'Full PDF retrieved; spanning-tree/Wong discussion read; generated title date not treated as submission date.',
 'foos_held_spitzley_2023.pdf':'Full PDF retrieved; objective definition and references read; approximation analysis unread.',
 'chapoullie_szigeti_2022.pdf':'Full author-hosted journal PDF retrieved independently; entireTheorem13pp11–12 including forward/converse proof read and visually checked.',
 'chapoullie_szigeti_arxiv_v1.pdf':'Full v1 PDF retrieved; entireTheorem13pp10–11 including forward/converse proof read.'}
ledger = []
for item in receipts:
    filename = Path(item['file']).name
    status = statuses.get(filename)
    if item.get('error'):
        status = 'Retrieval failed; theorem text unread.'
    elif item.get('identity_check'):
        status = item['identity_check']
    elif status is None:
        status = 'Metadata/page discovery record only; no theorem proof authenticated from this file.'
    ledger.append({'url':item['requested_url'], 'file':item['file'], 'reading_scope':status, 'private':True})
save('SOURCE_READING_LEDGER.json', {'recorded_utc':NOW, 'rule':'Full retrieval is distinct from full proof reading; no unread theorem is promoted.', 'pinned_source_reading':'Complete Kaibel contribution read: printed pages 3014–3015/PDF pages 46–47 of pinned owr.pdf; hash in INPUT_MANIFEST.json.', 'sources':ledger,
    'additional_unread_leads':[
        {'doi':'10.1016/j.procs.2021.11.009','scope':'Benedito–Pedrosa–Rosado2021: metadata/previews only; full proof unread.'},
        {'doi':'10.1016/j.dam.2023.07.010','scope':'Benedito–Pedrosa–Rosado2023: metadata/previews only; full proof unread.'},
        {'doi':'10.1023/A:1009854922371','scope':'2000 typeset journal article unread; accessible institutional preprint proof read.'},
        {'arxiv':'2305.03381','scope':'Foos–Held–Spitzley full-version lead not retrieved; proceedings definition and references read.'}]})

save('WEB_ACCESS_FAILURES.json', {'recorded_utc':NOW, 'failures':[
    {'url':'https://doi.org/10.1016/j.disopt.2022.100702','method':'web.open','result':'Internal error / URL inaccessible through that tool; full author-hosted proof independently retrieved.'},
    {'url':'https://discopt.ovgu.de/research/publications.php','method':'web.open','result':'Incorrectly guessed path, inaccessible; actual /publications/ subsequently inspected.'}],
    'scope':'Other direct HTTP failures are in RETRIEVALS.json; failure here does not imply inaccessible by every legitimate route.'})

verdict = {
 'target':{'pr':107,'record':30003997,'source_problem':'OWR-16633-014 Problem2'},
 'recorded_utc':NOW,'audit_cutoff_date':'2026-10-06',
 'novel_resolution_clearance':False,'restricted_strengthening_clearance':False,
 'mathematical_validity':'Accepted as pinned mathematically verified candidate; this is literature verification only.',
 'priority_classification':'No substantive new result established; general hardness is prior and complete restriction bundle is an elementary consequence of a 2022 published construction.',
 'bounded_basis':[
   {'source':'Dell’Amico–Maffioli report 186, cover August 1997; journal metadata 2000 DOI 10.1023/A:1009854922371','verified':'Accessible preprint Theorem 4.3 full proof plus exact tree/path objective embedding. Typeset journal theorem text unread.'},
   {'source':'Khazraei–Held 2021 DOI 10.1007/978-3-030-80879-2_13','verified':'Accessible author Theorem 1 full proof and bounded-cost objective embedding; publisher date checked.'},
   {'source':'Chapoullié–Szigeti 2022 DOI 10.1016/j.disopt.2022.100702; arXiv 2203.01096v1','verified':'Full Theorem 13 construction/proof independently retrieved/read/visually checked; explicit selector/cost-table comparison matches all candidate restrictions.'}],
 'restriction_comparison':{
   'same_unrestricted_objective':'Exact audit embeddings, not merely similar titles.',
   'same_restricted_theorem_bundle':True,
   'same_literal_published_destination_cost_table_theorem':False,
   'same_direct_3sat_gadget_claimed':False,
   'prior_graph_family':'RXC3 two-color DAG, selector subdivision',
   'matched':['simple','root-reachable','all vertices spanned','four consecutive layers','depth3','nonroot indegree≤3','binary destination costs','threshold0','nonzero coefficients only on root-first arcs','all positive costs1/2','constant4h+3m offset'],
   'comparison_is_audit_inference':True},
 'min_unsatisfied_identity_assessment':'Accurate accounting for the candidate direct3SAT construction; no separate developed gap/approximation theorem or substantive novelty established.',
 'required_corrections':[
   'Remove any new-general-resolution or2018-still-open claim based solely on curation.',
   'Cite exact prior objective embeddings and the2022 construction; do not promote the full restricted theorem as a novel strengthening.',
   'Describe the candidate as independently verified direct3SAT proof/exposition unless a separate substantive claim is independently established.',
   'Preserve workshop2018/reportpublished2019 distinction and fixed-root directed Problem2 scope.',
   'Do not imply the1996 original theorem,2000 typeset theorem, or unread2021/2023 cable-trench proofs were inspected.'],
 'unresolved_priority_concerns':[
   'Earliest priority remains unresolved;1996 original full text unread.',
   'Meaning of parenthetical(Why), private/oral knowledge and omitted author records cannot be authenticated from the report.',
   'No attributable explicit resolution of Kaibel’s named2018 question verified; this bibliographic gap does not create mathematical novelty.',
   'Unread cable-trench versions and originaltypeset2000article remain historical gaps; they do not invalidate the positive2022 prior-construction obstruction.',
   'No absolute claim that every possible refinement is old; no substantive new refinement is established by this candidate.'],
 'search':{'queries':59,'batches':16,'independent_queries_before_cross_family_read':58,'initial_independent_checkpoint_after_queries':16,'no_hit_is_not_novelty_evidence':True},
 'proof_budget':{'original_completed':1,'maximum':5,'added_central_proof_search_responses':0},
 'audit_completion_percent':100,'percentage_scope':'Completion of bounded literature audit, not probability of novelty.',
 'independence':'Frozen initial comparison before any other family; root comparison read only after own58queries, then prior source fetched and checked independently.',
 'privacy':'All third-party PDFs, extracts, images, raw web pages/results remain under private_sources and are not selected for public redistribution.',
 'prohibited_actions_performed':[]}
save('VERDICT.json', verdict)

with (BASE/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+NOW+': Final bounded-audit checkpoint. Independent58-query search and16-query frozen comparison completed before root cross-family input. Independently fetched/read/visually checked2022Theorem13 and arXivv1; verified full restriction bundle as source-bound corollary. SAT minimum-unsatisfied identity assessed as accounting, no independent substantive claim. Audit completion estimate100%; novelty/strengthening clearancefalse with positive prior evidence. Original proof1/5; added central proof-search0. Private sources retained; no prohibited mutation or external communication.\n')

# Validate provenance and input stability, then create the final self-excluding manifest.
assert len(queries)==59 and len({q['batch'] for q in queries})==16
for item in receipts:
    path = BASE/item['file']
    if item.get('sha256'):
        assert digest(path)=={'bytes':item['bytes'],'sha256':item['sha256']}, item['file']
    assert path.relative_to(BASE).parts[0]=='private_sources'
for item in inputs['inputs']+inputs['cross_family_inputs']:
    assert digest(Path(item['path']))=={'bytes':item['bytes'],'sha256':item['sha256']}, item['path']
save('AUDIT_VALIDATION.json', {'utc':NOW,'status':'PASS','checks':['59queries/16batches','saved successful retrieval hashes/bytes','all original and cross-family input hashes stable','all third-party retrieval files private'],'central_mathematical_computation_performed':False})
files = sorted(p for p in BASE.rglob('*') if p.is_file() and p.name!='OUTPUT_MANIFEST.json')
save('OUTPUT_MANIFEST.json', {'utc':NOW,'self_exclusion':'OUTPUT_MANIFEST.json excluded to avoid circular hash.','files':[{'path':str(p.relative_to(BASE)),**digest(p),'private':p.relative_to(BASE).parts[0]=='private_sources'} for p in files]})
print(json.dumps({'status':'PASS','queries':59,'source_requests':len(receipts),'manifest_files':len(files),'novel_resolution_clearance':False}))
