from pathlib import Path
import datetime, hashlib, json, shutil, zipfile

HERE=Path(__file__).resolve().parent
PAPER=HERE.parent.parent
SOURCE=PAPER/'sources'
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

receipt=json.loads((SOURCE/'receipt.json').read_text())
assets=[]
for f in receipt['files']:
    p=SOURCE/f['name']
    assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256']
    assets.append({'path':str(p.relative_to(PAPER)),'sha256':sha(p),'bytes':p.stat().st_size})
assert sha(SOURCE/'record.json')==receipt['record_sha256']
members=[]
for archive in receipt['archives']:
    with zipfile.ZipFile(SOURCE/archive['name']) as z:
        assert z.testzip() is None
        for m in archive['members']:
            name=m['member'];path=SOURCE/'published-source'/name
            assert path.is_file() and path.stat().st_size==m['bytes'] and sha(path)==m['sha256']
            assert z.read(name)==path.read_bytes()
            assert (HERE/'replay-work'/name).read_bytes()==path.read_bytes()
            members.append({'path':name,'sha256':m['sha256'],'bytes':m['bytes']})
assert len(members)==124
write('source-integrity-final.json',{'status':'PASS','completed_utc':stamp,'assets':assets,
    'source_receipt_sha256':sha(SOURCE/'receipt.json'),'record_sha256':sha(SOURCE/'record.json'),
    'full_archive_crc_checked':True,'all_originals_and_isolated_copy_unchanged':True,'members':members})

reading={
 'FL_v3':'PDF pp.1–2,4–7,10–13: model, least action, rooted tree/period vector, NP argument, simple-graph question and Table1. Relevant theorem interfaces checked; not entire paper proof certification.',
 'Abelian_logic_v2':'PDF p.15 full Lemma4.1 construction and p.32 Section8.3 conservative gates; primed toppler specialization derived independently.',
 'Stockmeyer_Meyer':'PDF pp.7–8 full relevant Theorem6.1 and SAT encoding proof, plus visual render of both scan pages.',
 'Gramlich_2003':'PDF pp.5–6 Fact3 and its full proof; classical invalid-variable/falsifying-clause encoding.',
 'Dusart_2010':'PDF p.4 Section4 equations4.1/4.2 and short proof; logarithm convention on p.2. Explicit prime supply only.',
 'Farrell_thesis':'Sections1.1 and4.1 in full, PDF pp.2–3 and9: model, root-last process and conserved-mass comparison.',
 'Eriksson_AMS':'All three PDF pages: simple directed construction, linear chip count and exponential convergent game context. Exact asymptotic formula not imported.',
 'GRM_journal':'Actual journal PDF pp.39–43: LR-GRMM input/target interface, Theorem21 and reduction through Lemmas22–23. No assertion of a chip-firing transfer or full paper certification.',
 'Abelian_II':'PDF pp.17–18 Definition6.5, Corollary6.6 and adjoining context. All-input quantifier only; no single-input transfer imported.',
 'Esparza_survey':'PDF pp.31–32 selected class/interface discussion; formula extraction has glyph limitations, no formula-level or full weighted-net theorem certification.'}
raw_receipt=json.loads((PAPER/'reviews/scope/primary_source_receipts.json').read_text())
cache=HERE/'primary-sources';cache.mkdir(exist_ok=True)
primary=[]
for r in raw_receipt:
    name=r['citation_id'];path=Path(r['path'])
    assert sha(path)==r['sha256']
    for ext in ['.pdf','.txt']:shutil.copyfile(path.with_suffix(ext),cache/(name+ext))
    primary.append({'citation_id':name,'url':r['url'],'edition':r['edition'],
        'pdf_sha256':r['sha256'],'pdf_bytes':r['bytes'],'pdf_pages':r['pages'],
        'saved_path':'primary-sources/'+name+'.pdf','reading_scope':reading[name]})
write('primary-source-bindings.json',{'bound_utc':stamp,'primary_sources':primary,
    'scope_raw_receipt_sha256':sha(PAPER/'reviews/scope/primary_source_receipts.json'),
    'priority_certified':False,'all_external_proofs_reproduced':False})

controls=json.loads((HERE/'independent-controls.json').read_text())
assert sha(HERE/'independent_controls.py')==controls['script_sha256']
replays=json.loads((HERE/'published-replay-results.json').read_text())
assert replays[0]['diagnostics']==replays[1]['diagnostics']
assert all(row['exit_code']==0 for row in replays[:2])
assert all(row['exit_code']!=0 and row['expected_rejection'] for row in replays[2:])
with (HERE/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n## '+stamp+' — 100%\n\nIndependent analytic review finalized: PASS at the exact ordinary conservative simple/strongly-connected and oriented graph domains. No substantive gap identified. Fresh independent controls, both unmodified mathematical replay modes, expected invalid-command rejections, primary interfaces and all source/ZIP/isolated-copy hashes checked. Historical administrative code strings were incidental exposure and not evidence. No repair, publication or outreach.\n')

artifacts={str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*') if p.is_file()
    and 'replay-work' not in p.parts and '__pycache__' not in p.parts
    and p.name not in ['artifact-manifest.json','verdict.json']}
write('artifact-manifest.json',artifacts)
write('verdict.json',{'record_id':'23431716','role':'independent_analytic',
    'status':'PASS','completed_utc':stamp,'completion_percent':100,
    'manuscript':{'title':'A modular-storage proof of NP-completeness for chip-firing halting on simple digraphs','version':'1.0','date':'2026-10-16','pages':7},
    'claim_scope':{'graph':'finite loopless simple strongly connected digraph, N>=2, plus oriented subclass',
        'dynamics':'ordinary asynchronous conservative chip firing, every vertex fires at its actual outdegree, unit output on every outgoing arc, no sink',
        'input':'arbitrary nonnegative integral configuration encoded in binary',
        'halting':'existence of a legal finite word reaching any stable configuration; least action supplies arbitrary-schedule equivalence without fairness',
        'hardness':'deterministic polynomial-time many-one reduction from explicitly encoded 3-CNF; numerical total chips polynomial in source length, hence also unary hardness',
        'restriction':'specified root deletion leaves an acyclic graph with no directed two-arc path',
        'NP_certificate':'nonnegative firing vector f with 0<=x-Delta*f<d; f_u+1<=(N-1)^(2N-2), O(N log N) bits per coordinate'},
    'source_binding':{'assets':assets,'receipt_sha256':sha(SOURCE/'receipt.json'),'record_sha256':sha(SOURCE/'record.json'),
        'source_tex_sha256':sha(SOURCE/'published-source/paper.tex'),'all124_extracted_members_unchanged':True},
    'proof_status':'complete stated proof reconstructed; no substantive defect or unresolved central gap identified',
    'independent_evidence':{'assertions':controls['assertions'],'nonempty_bank_sets':2035,'formula_cases':264,'physical_graphs':528,
        'all_small_strongly_connected_graphs':19,'whole_small_graph_states':256,'extra_constructed_complete_state_spaces':8,
        'fresh_controls_completed_before_helper_reading':True,'finite_controls_are_not_universal_proof':True},
    'published_replay':{'normal':'PASS','optimized':'PASS','invalid_guard_normal':'REJECTED_AS_EXPECTED','invalid_guard_optimized':'REJECTED_AS_EXPECTED',
        'historical_programs_replayed':False,'administrative_adoption_checker_used_as_math_evidence':False},
    'independence':{'sibling_findings_or_code_read':False,'dedicated_historical_assessment_bodies_read':False,
        'incidental_exposure':'Current manuscript audit/status language and historical adoption strings embedded in current verify_kit.py after independent controls; not relied upon.'},
    'findings':[],'remaining_gaps':[],
    'limitations':['AI review, not human peer review or formal verification','No firstness, full-result priority or worldwide openness certification',
        'No polynomial simulation-time claim','No transfer to undirected, Eulerian, bidirected, coEulerian, dissipative-sink or generalized-rotor models',
        'Primary-source interface review is not certification of every outside proof'],
    'report_sha256':sha(HERE/'REVIEW.md'),'artifact_manifest_sha256':sha(HERE/'artifact-manifest.json'),
    'source_modified':False,'publication_actions':False,'outreach':False})
for name in ['REVIEW.md','verdict.json','artifact-manifest.json']:
    print(name,sha(HERE/name))
print('bound_artifacts',len(artifacts),'receipt',sha(SOURCE/'receipt.json'))
