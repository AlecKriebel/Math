"""Bind independent priority findings to retrieved public documents and hashes."""
import datetime, hashlib, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CANDIDATE = pathlib.Path('/Users/alec/Documents/Math/pr9_adversarial_review_20260929/source_snapshot/candidate.md')
manifest_names = ['download_manifest.json', 'additional_download_manifest.json', 'owr_2021_download_manifest.json', 'randomstrasse_download_manifest.json']
retrievals = []
for name in manifest_names:
    obj = json.loads((ROOT / name).read_text())
    retrievals.extend(obj if isinstance(obj, list) else [obj])
source_data = {
    'geometry_discotopes_publisher_2022.pdf': ('S01', 'The Geometry of Discotopes', '2022-06-27 publisher article record; 2022 journal issue', 'Complete article read; p. 167 visually checked', ['Definition 3.3', 'Remark 3.4', 'Theorem 4.3', 'Section 5', 'Theorem 6.1', 'Lemma 6.3 and Remark 6.4', 'Conjecture 8.2'], 'Original generic S conjecture, established partial cases, and support-gradient parametrization; no general E or S theorem.'),
    'geometry_discotopes_arxiv_v2.pdf': ('S02', 'The Geometry of Discotopes, arXiv v2', 'v1 2021-11-01; v2 2022-07-28', 'Latest complete file retrieved and compared with journal target', ['Sections 2, 3, 5, 6, 8'], 'Same target genealogy and partial-result framework; no later full solution in this version.'),
    'owr_2023_15.pdf': ('S03', 'Two convex conjectures for different flavours', '2023', 'Complete Meroni contribution pp. 829–832 read; full workshop screened; p. 830 visually checked', ['p. 830 Definition 1', 'p. 830 Theorem 2', 'p. 830 Conjecture 1'], 'Defines E as exposed-point closure; states generic irreducibility as conjecture; reports prior special cases.'),
    'meroni_thesis_2022.pdf': ('S04', 'Semialgebraic Convex Bodies', 'Submitted 2022-10; defense 2022-10-25', 'Complete file screened; discotope chapter definitions, proofs, partial cases, and conclusion inspected', ['Definition 2.2.1', 'Remark 2.2.2', 'Theorem 2.2.5', 'Proposition 2.2.10', 'Theorem 2.2.13', 'Conjecture 2.2.22 p. 54'], 'Reproduces generic S conjecture and article partial cases; no general resolution.'),
    'fiber_convex_bodies.pdf': ('S05', 'Fiber Convex Bodies', 'arXiv first 2021-05-26; journal online 2022; volume 2023', 'Complete file screened; complete Section 5.2 and related discotope context read', ['Definition 5.13', 'Definition 5.16', 'Proposition 5.18', 'Remark 5.19'], 'Round 2D discs in R3; connectivity of a smaller open real boundary surface is not target algebraic irreducibility.'),
    'meroni_semialgebraic_slides_2022.pdf': ('S06', 'Semialgebraic Convex Bodies seminar slides', '2022-03-01 seminar record', 'Complete 27-slide file inspected', ['Fiber and intersection body material'], 'No general target irreducibility theorem identified.'),
    'line_multiview_varieties_v2.pdf': ('S07', 'Line Multiview Varieties', 'arXiv first 2022-03-03; v2 2022-11-18; journal 2023', 'Complete file screened; relevant Section 3 read', ['Lemma 3.3 and following discussion', 'Use of GM Lemma 6.3'], 'Auxiliary row-constrained rank variety irreducibility; not discotope E, generic S=E, or general sphere-product critical locus.'),
    'operatopes_2026.pdf': ('S08', 'Operatopes, Operanoids, and Noncommutative Zonoids', 'arXiv first 2026-02-08; PDF 2026-02-10', 'Complete 23-page paper read', ['Section 2.1 equations (2)–(3)', 'Proposition 5', 'Sections 5–6'], 'Contains discotopes and an exposed-face closure result, but no exposed-point Zariski irreducibility or generic S=E theorem.'),
    'mathis_handbook_2022.pdf': ('S09', 'The Handbook of Zonoid Calculus', '2022 thesis', 'Complete file screened; relevant pp. 78–79 read', ['Definition 2.5.26', 'Proposition 2.5.27'], 'Dice/fiber-body example and citations; no general E or S irreducibility theorem.'),
    'meroni_defense_2022.pdf': ('S10', 'Semialgebraic Convex Bodies defense slides', '2022-10-25', 'Complete 24-slide file retrieved and screened', ['Slides 16–17'], 'Exposed-point closure conjecture retained; notation S differs from thesis S.'),
    'whitney_numbers_2016.pdf': ('S11', 'Whitney numbers of arrangements via measure concentration of intrinsic volumes', '2016-06-30 arXiv submission; PDF 2016-07-01', 'Complete file screened; introductory discotope construction read', ['Introduction', 'Section 1.1'], 'Intrinsic-volume/matroid ancestor; no algebraic exposed-point irreducibility theorem.'),
    'owr_2021_59.pdf': ('S12', 'Convex Algebraic Geometry (Meroni contribution)', '2021', 'Complete workshop screened; complete pp. 3212–3214 Meroni contribution read', ['pp. 3212–3214'], 'Advertises discotope project and cites forthcoming original paper; no general target theorem.'),
    'randomstrasse_2024.pdf': ('S13', 'Randomstrasse101: Open Problems of 2024', 'arXiv first 2025-04-29; latest PDF 2025-05-29', 'Complete text screened; introduction and contents checked', ['Introduction'], 'False-positive author lead: Meroni is a blog maintainer; no discotope occurrence.'),
}
sources = []
for record in retrievals:
    if record['status'] != 'downloaded_and_text_extracted':
        continue
    sid, title, publication, scope, locators, finding = source_data[record['filename']]
    content = (ROOT / 'documents' / record['filename']).read_bytes()
    if hashlib.sha256(content).hexdigest() != record['sha256']:
        raise ValueError('Hash mismatch for ' + record['filename'])
    text_path = ROOT / 'documents' / record['filename'].replace('.pdf', '.txt')
    full_text = text_path.read_text(errors='replace')
    source = dict(record)
    source.update(source_id=sid, title=title, publication_date_or_history=publication, read_scope=scope, locators=locators, finding=finding, prior_full_resolution=False, text_extraction_file=str(text_path.relative_to(ROOT)), text_sha256=hashlib.sha256(text_path.read_bytes()).hexdigest(), screening_counts={term:full_text.lower().count(term) for term in ['discotope', 'irreduc', 'exposed', 'zariski', 'critical', 'conjecture']})
    sources.append(source)

prior_results = [
    {'id':'P01','source_id':'S01','location':'Remark 3.4, pp. 149–150','hypotheses':['all summand discs full-dimensional'],'conclusion':'S identified with exposed-point closure and irreducibility asserted','scope':'prior special case'},
    {'id':'P02','source_id':'S01','location':'Theorem 4.3, p. 152','hypotheses':['generic discotope','dim(D_i)>=2','sum_i(dim(D_i)-1)<=d-1'],'conclusion':'S irreducible; degree 2^N','scope':'prior special case'},
    {'id':'P03','source_id':'S01','location':'Theorem 6.1, p. 157','hypotheses':['generic discotope','all dim(D_i)=2','N>=d-1'],'conclusion':'S irreducible and equals extreme/exposed-point closure; degree upper bound','scope':'prior special case; lower N covered by P02'},
    {'id':'P04','source_id':'S01','location':'Section 5, especially Proposition 5.4','hypotheses':['generic discotope where stated'],'conclusion':'Support-gradient parametrization; generic injectivity and analysis of a component','scope':'prior mechanism, not full resolution'},
]
web_sources = [
    {'id':'W01','url':'https://merochia.wixsite.com/chiara-meroni/research','role':'author primary bibliography','read_scope':'complete retrieved page','finding':'Current through 2026 material; no later discotope resolution identified'},
    {'id':'W02','url':'https://merochia.wixsite.com/chiara-meroni/talks','role':'author primary talk list','read_scope':'complete retrieved page','finding':'Current and future 2026 talks; exact conjecture/defense and old discotope talks found'},
    {'id':'W03','url':'https://fulges.github.io/publications.html','role':'author primary bibliography','read_scope':'complete retrieved page','finding':'Current 2026 material; original article is only identified discotope item'},
    {'id':'W04','url':'https://www.mis.mpg.de/events/event/discotopes','role':'official 2021 talk record','read_scope':'complete relevant event page','finding':'Original face/algebraic-boundary project'},
    {'id':'W05','url':'https://www.math.uni-bielefeld.de/geocomb/program/','role':'official 2022 workshop program','read_scope':'Meroni entry and links','finding':'Discotope project abstract; linked slides unavailable (404)'},
    {'id':'W06','url':'https://leomathis.wordpress.com/research/','role':'author primary research list','read_scope':'complete retrieved page','finding':'Handbook and zonoid work discovered; no general resolution identified'},
    {'id':'W07','url':'https://arxiv.org/abs/2111.01241','role':'primary version history','read_scope':'complete metadata page','finding':'v1 2021-11-01 and v2 2022-07-28'},
    {'id':'W08','url':'https://arxiv.org/abs/2602.08103','role':'primary version history','read_scope':'complete metadata page','finding':'Recent 2026 citing work followed to full primary PDF'},
]
queries=json.loads((ROOT/'search_queries.json').read_text())
evidence = {
    'schema_version':'1.0',
    'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'audit_route':'independent exact target genealogy, author trail, and citing primary papers',
    'scope':{'pr':9,'problem':'30005473','source_problem':'OWR-12697711-006','reviewed_head':'a29887ed0e341851d02fa992c26500d4089267be','candidate_path':str(CANDIDATE),'candidate_sha256':hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()},
    'verdict':{'prior_full_resolution_found':False,'status':'no_checkable_prior_full_resolution_found_in_inspected_route','priority_certified':False,'publication_blocker_found':False,'confidence_interpretation':'bounded negative evidence, not proof of universal absence or current open status','route_completion_percent':100},
    'targets':[
        {'id':'T2023','source_id':'S03','location':'p. 830, Definition 1 and Conjecture 1','variety':'E = complex Zariski closure of exposed points','hypotheses':['generic discotope','all summand dimensions at least two'],'claim':'E irreducible'},
        {'id':'T2022','source_id':'S01','location':'Definition 3.3 and p. 167 Conjecture 8.2','variety':'S = complex Zariski closure of sums of relative summand boundary points lying on total boundary','hypotheses':['generic discotope','no one-dimensional summands','full-dimensional convention after reducing to span'],'claim':'S irreducible'},
    ],
    'candidate_claims':[
        {'id':'C1','claim':'E irreducible','hypotheses':['finite nonempty sum','all ellipsoidal summand dimensions at least two'],'genericity_required':False,'full_dimension_required':False,'relationship':'stronger than T2023'},
        {'id':'C2','claim':'S=E and hence S irreducible','hypotheses':['full-dimensional sum','all summand dimensions at least two','for every subset J, dim(sum spans)=min(d,sum summand dimensions)'],'relationship':'bridges C1 to T2022; maximal-span condition holds on nonempty Zariski-open parameter set'},
    ],
    'prior_results':prior_results,
    'sources':sorted(sources,key=lambda s:s['source_id']),
    'web_sources':web_sources,
    'searches':queries,
    'citation_discovery':{'apis_manifest':'citation_index_manifest.json','semantic_scholar_discovered_citing_works':['S05','S07','S08'],'openalex_citing_works':0,'crossref_journal_doi_status':'404','openalex_journal_doi_status':'404','mardi':'Disagrees and includes irrelevant older disk-related false positives; used only for discovery','inference':'No citation-index count guarantees coverage'},
    'failed_retrievals':[record for record in retrievals if record['status']!='downloaded_and_text_extracted']+[
        {'url':'https://www.math.uni-bielefeld.de/geocomb/program/assets/Slides_Meroni.pdf','status':'404'},
        {'url':'https://www.mis.mpg.de/nonlinear-algebra/publications/by-type-1','status':'web internal error'},
        {'url':'https://nbn-resolving.org/urn:nbn:de:bsz:15-qucosa2-819717','status':'landing access challenge; public linked institutional PDF used instead'},
    ],
    'limits':['No theorem of absence is implied by search','Indexes incomplete and inconsistent','Unpublished, unindexed, inaccessible, or differently phrased work may be missed','No outside people contacted','General analytic-lemma genealogy handled by a separate route, not certified here','Latest/publisher original checked but arXiv v1 download failed'],
    'falsifiable_priority_blocker':'A primary result predating this candidate with matching discotope definition and general E irreducibility, or generic S irreducibility/equality covering the missing higher-dimensional regime, would overturn this negative conclusion. Stronger degree/critical-locus results are relevant only if they imply the exact target under checkable hypotheses.',
    'manuscript_review':{'path':'/Users/alec/Documents/Math/discotope_irreducibility_30005473/paper.tex','intro_targets_accurate':True,'needed_correction':'Earlier Theorems 4.3 and 6.1 require genericity; Theorem 6.1 requires N>=d-1; smaller all-2D cases covered by Theorem 4.3','parent_confirmed_correction_applied':True,'manuscript_modified_by_this_route':False},
    'safe_framing':'Proves Meroni 2023 Conjecture 1 in a stronger nongeneric form and, using generic S=E, proves Gesmundo–Meroni 2022 Conjecture 8.2; credit partial cases and existing support-gradient parametrization. Do not assert first-ever proof or verified present openness.',
    'distinct_unsettled_questions':['irreducibility of entire complex critical locus','birationality of addition map','general degree formulas'],
    'artifact_policy':'Retrieved source cache is local inspection material, ignored by this folder .gitignore; report and evidence point to public primary URLs',
}
(ROOT/'priority_evidence.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'sources':len(sources),'queries':queries['search_count'],'prior_full_resolution_found':False,'candidate_sha256':evidence['scope']['candidate_sha256'],'json_valid':True},indent=2))
