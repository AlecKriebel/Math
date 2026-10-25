from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess
b=Path(__file__).resolve().parents[2];s=b/'reviews/scope';src=b/'sources';now=datetime.now(timezone.utc).isoformat()
archive='simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz'
pdf='simultaneous_amplification_beyond_three_halves.pdf'
record=json.load(open(src/'record.json'));receipt=json.load(open(src/'receipt.json'));outer=json.load(open(s/'archive_inventory.json'))
prefix='universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/'
abstract=('We study fixation from a uniformly random single mutant on finite connected loopless undirected weighted graphs under both Birth–death (Bd) and death–Birth (dB) Moran updating. Let R_sim be the supremum of R for which one fitness-independent graph family eventually amplifies fixation under both rules for every fixed r ∈ (1,R). Let R_hyb be the unique root in (3/2,151/100) of R⁶ − 8R⁵ + 22R⁴ − 30R³ + 21R² − 6R + 1. We construct one fitness-independent family that simultaneously amplifies every fixed 1 < r < R_hyb for all sufficiently large members of the sequence. Therefore R_sim ≥ R_hyb = 1.5028569127905696… > 3/2. The construction combines a large clique with dilute hub pendants and dilute, internally heavy two-vertex satellites. An exact finite-state derivation of the weak-cut limiting trace, together with uniform establishment, cleanup, and reciprocal-invasion estimates at the scale of the eventual gain, reduces the two normalized fixation corrections to explicit response functions. Optimizing their common positivity interval yields the displayed sextic. The same analysis proves that R_hyb is optimal among fixed positive (σ,λ) in the displayed first-order dilute pair–pendant response model; a specialization with entirely rational edge weights already crosses 3/2. Thus 3/2 is not the exact simultaneous-amplification threshold. The unrestricted value of R_sim, and even a finite universal upper bound, remain open.')
content={
 'title':record['metadata']['title'],
 'slug':'simultaneous-amplifiers-beyond-three-halves',
 'description':'A fitness-independent weighted graph family raises Moran fixation probability under both Birth–death and death–Birth updating for fixed fitness below 1.5028569.',
 'abstract':abstract,
 'plain_language':[
  'In a structured population, a new mutation can disappear or eventually replace every resident. The probability of taking over depends on which individuals can replace which others. It also depends on whether reproduction is chosen before a replacement site, or a vacancy is chosen before its neighbors compete to fill it.',
  'This paper constructs a single sequence of weighted population graphs that improves takeover probability under both of these pure update rules. The graph sequence is chosen before the beneficial mutation’s relative fitness is known. For each fixed fitness between 1 and about 1.5028569, all sufficiently large graphs in the sequence improve on a well-mixed population of the same size.',
  'The graph combines a large well-mixed clique with two sparse kinds of peripheral structure. Heavy pairs favor death–Birth fixation, while leaves attached to one hub favor Birth–death fixation. Their small contributions can be balanced to make both improvements positive. Earlier work by Svoboda and colleagues established simultaneous amplification below relative fitness 1.2; a separate earlier construction by the author reached the open interval below 1.5.',
  'The improvement above 1.5 changes what thresholds are possible, although the advantage becomes small as the population grows. This is a mathematical construction with highly separated edge weights. It supplies no empirical prediction or practical population-size requirement.'
 ],
 'result':[
  'Let R_hyb be the unique root in (3/2,151/100) of R⁶ − 8R⁵ + 22R⁴ − 30R³ + 21R² − 6R + 1. The main theorem constructs a fitness-independent sequence of finite connected loopless undirected weighted graphs G_t such that, for every fixed 1 < r < R_hyb, uniformly initialized single-mutant fixation exceeds the corresponding complete-graph probability under both Bd and dB updating for every sufficiently large t. Hence R_sim ≥ R_hyb = 1.5028569127905696… > 3/2.',
  'The sequence uses a unit clique of C_t = t⁴ vertices, m_t = floor(λ_* t) unit hub leaves, and q_t = t two-vertex satellites with internal weight C_t/σ_*. Every satellite vertex connects to every clique vertex by a common positive dyadic weight selected by an exact compact-interval decision procedure. All weights are fixed before r is quantified.',
  'At scale q_t/C_t, the two normalized fixation corrections are B(r) = 2(σ−1)/(1+σ(r²−1)) + λ/(r−1) and D(r) = 2{r(2−r)−σ}/(σ+2r(r−1)) − λ. Their simultaneous positivity produces the sextic threshold. The optimal parameters are approximately σ_* = 0.1306772822870484 and λ_* = 0.7508064830318805.',
  'Within this displayed first-order dilute response model, R_hyb is optimal among fixed positive σ and λ. The rational choice σ = 19/137 and λ = 20/27 already yields an entirely rational-edge graph sequence with threshold (5069 + 12√147001)/6439 = 1.50176815223369… > 3/2.'
 ],
 'why_it_works':[
  'For fixed finite module sizes, an exact finite-state Schur complement resolves rare migration between the center and satellites. It uses local fixation probabilities to obtain a limiting macro chain while retaining possible reversals of a partially completed sweep.',
  'The center-module argument controls initial establishment, later cleanup, and reciprocal invasion to errors smaller than the eventual gain q_t/C_t. An ordinary approximation with an unspecified error tending to zero would not suffice because the claimed gain itself tends to zero.',
  'The two module types have opposite response signs under the two update rules. The proof balances their densities, optimizes the shared positivity interval, and then selects one positive weak-edge weight for each t on an expanding compact fitness interval. This supplies the required order: one family, then every fixed fitness, then a fitness-dependent size threshold.'
 ],
 'limitations':[
  'The model assumes finite connected loopless undirected weighted graphs, uniform initialization of exactly one mutant, mutant fitness r > 1, and the two specified pure Bd and dB update rules. It does not cover arbitrary initialization, directed or unweighted graphs, empirical evolutionary dynamics, or a process that randomly mixes the update rules.',
  'The statement is eventual positivity for each fixed r in the open interval (1,R_hyb). It supplies neither strict amplification at r = R_hyb nor a size bound uniform near either endpoint; it does not cover a fitness that varies with population size.',
  'The threshold is exact only for fixed positive parameters in the displayed first-order dilute pair–pendant response model. It is a lower bound for unrestricted R_sim. No universal upper bound or optimality over all growing graph families is proved.',
  'The normalized fixation gain is of order t⁻³ = Θ(n_t⁻³/⁴) and tends to zero. Pair weights grow with the clique size, and the compact-interval construction may require very small positive weak edges. No useful finite-size onset, fixation-time bound, bounded weight ratio, or practical optimality is claimed.',
  'The archived exact verifiers check finite labelled transition aggregation, symbolic response identities, rational margins, root isolation, and tangency. They do not machine-verify the manuscript’s weak-cut convergence or population asymptotics.',
  'This is an unrefereed preprint developed with substantial generative-AI assistance in mathematical exploration, derivation, adversarial analysis, programming, and writing. The author accepts responsibility for its claims.'
 ],
 'background':[
  {'title':'Svoboda, Joshi, Tkadlec and Chatterjee (2024), Amplifiers of selection for the Moran process with both Birth-death and death-Birth updating','url':'https://doi.org/10.1371/journal.pcbi.1012008','note':'Established simultaneous amplification on 1 < r < 1.2 using weakly connected weighted modules. Its uniform singleton initialization, update rules, and same-order complete-graph benchmarks agree with this paper’s model. The present construction improves the fitness interval.'},
  {'title':'Tkadlec, Pavlogiannis, Chatterjee and Nowak (2020), Limits on amplifiers of natural selection under death-Birth updating','url':'https://doi.org/10.1371/journal.pcbi.1007494','note':'Proved boundedness and fixed-graph transience for noncomplete structures, including weighted and directed edges. A graph-dependent strong-selection threshold does not impose one bound on every growing graph family.'},
  {'title':'Kriebel (2026), No universal death–Birth amplifier on a finite weighted population structure','url':'https://doi.org/10.5281/zenodo.21753405','note':'An earlier unrefereed release extends the fixed-graph obstruction to complete directed weighted support and identifies the exact baseline equality class. It addresses a different quantifier order.'},
  {'title':'Kriebel (2026), A fitness-independent family of simultaneous amplifiers below fitness three halves','url':'https://doi.org/10.5281/zenodo.21850042','note':'The separate center–triangle construction establishes R_sim ≥ 3/2 and suppresses at its own endpoint. The present result crosses that endpoint with a different family.'},
  {'title':'Brewster, Huang, Mitzenmacher and Nowak (2026), The Mixed Birth-Death/death-Birth Moran Process','url':'https://doi.org/10.4230/LIPIcs.ITCS.2026.29','note':'Studies a process that independently chooses an update rule at each step. Simultaneous amplification under each pure rule does not by itself prove amplification for every mixture.'}
 ],
 'collaboration':'I welcome substantive collaboration on independent verification of the stochastic comparison and weak-cut arguments, assessment of the gain-scale error estimates, or development of a journal submission. Authorship would reflect actual research and writing contributions.',
 'follow_up':None,
 'followup_rationale':'No follow-up is proposed. The unrestricted threshold, different modules, changing parameter scales, and useful finite-size or time bounds are substantial directions, but this focused reading supplies no new precise mechanism or evidence-supported conjecture that clears the requested publication bar. A bounded literature search cannot certify worldwide openness.',
 'publication_date':'2026-08-25',
 'publication_date_label':'Reviewed edition published',
 'edition_label':'Version 2.0.4; first named Zenodo release 8 August 2026',
 'original_publication_date':'2026-08-08',
 'reviewed_publication_date':'2026-08-25',
 'version':'2.0.4','doi':'10.5281/zenodo.22089807','author':'Alec Kriebel',
 'pdf_filename':pdf,'supplement_filename':archive,
 'status':'Unrefereed preprint, reviewed edition 2.0.4. Initially released on Zenodo on 8 August 2026; this edition was published on 25 August 2026. Developed with substantial generative-AI assistance.',
 'ai_disclosure':'Generative AI assisted substantially with mathematical exploration, derivation, adversarial analysis, programming, and manuscript preparation. The author is responsible for the work; this is an unrefereed preprint.',
 'source_binding':{
  'record_id':'22089807','record_url':'https://zenodo.org/records/22089807','doi':'10.5281/zenodo.22089807','concept_doi':'10.5281/zenodo.22089806','version':'2.0.4','zenodo_publication_date':'2026-08-25','original_named_release':{'record_id':21852072,'date':'2026-08-08','doi':'10.5281/zenodo.21852072','same_work_version_not_additional_completion':True},'standalone_manuscript_date':'August 2026','embedded_manuscript_date':'August 22, 2026','record_created_utc':record['created'],'record_updated_utc':record['updated'],'source_retrieved_utc':receipt['retrieved_utc'],'pdf_sha256':receipt['files'][0]['sha256'],'supplement_sha256':receipt['files'][1]['sha256'],'files':receipt['files'],'reviewed_documents':json.load(open(s/'reader_asset_ledger.json')),'abstract_source':'Standalone deposited PDF page 1, cross-checked against complete abstract in released main.tex; full text preserved with mathematical typography and whitespace normalization. No metadata-only substitute.','embedded_pdf_difference':'Embedded PDF is not byte-identical to standalone PDF. Complete text comparison shows only title-page date, Figure 1 label positioning/extracted order and whitespace differences; no mathematical claim or proof text difference found.'
 },
 'held_candidate':True,
 'publication_gate':'Held pending independent analytic and adversarial verdicts; this scope candidate grants no promotion or deployment approval.'
}
(s/'content.json').write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
# Each deposited support member receives an explicit reading disposition.
dispositions={
 'BUNDLE_METADATA.txt':('metadata','Full text read; archival no-new-DOI statement is stale relative to public API.'),
 'MANIFEST.sha256':('integrity','Full manifest parsed; exact 22-member payload set and every SHA-256 verified.'),
 'universal_simultaneous_amplification/LICENSE':('license','MIT license read; separate upstream wheel licenses retained.'),
 'README.md':('reader/replay guide','Full text read; scope and tool boundaries inspected, claims not accepted on authority.'),
 'RELEASE_NOTES.md':('historical package description','Full text read solely for version/package scope; favorable historical review claims not treated as proof.'),
 'RESEARCH_LOG.md':('historical research log','Inventory/hash only; intentionally not consulted as scientific support or prior favorable audit.'),
 'all.sh':('wrapper','Full script read; calls replay and build sequentially.'),
 'bootstrap_replay.sh':('runtime/replay wrapper','Full script read; rejects optimized Python, requires Python 3.14.6, installs hash-pinned local wheels, checks versions, runs replay and failure tests.'),
 'build.sh':('document build','Full script read; invokes external Tectonic, installs generated PDF, runs pdfinfo and Poppler. Not run by this scope reviewer.'),
 'bundle_manifest.py':('package generator/checker','Full code read; explicit public whitelist, deterministic tar/gzip, mode/path checks, exact manifest set/hash and excluded-path validation. Independently checked current archive rather than rebuilding.'),
 'verify_hybrid_coefficients.py':('finite symbolic certificate','Full code read; checks response identities, rational specialization, margins, discriminant, Sturm counts and algebraic tangency, plus decimal sanity checks. Does not derive analytic gain-scale estimates.'),
 'verify_hybrid_lumping.py':('finite transition certificate','Full code read; exact Fraction enumeration of C=3, q=2, m=2, r=3/2, sigma=19/137, epsilon=1/100. Compares all 512 labelled states against 108 five-coordinate transition rows for both rules. Does not enumerate the asymptotic sequence.'),
 'verify_leading_algebra.py':('finite symbolic certificate','Full code read; exact sextic interval/root counts, endpoint signs, gap quadratic, minimum, parameter positivity and derivative identities. This verifies algebra conditional on response formulas.'),
 'main.tex':('analytic manuscript source','Abstract, declarations, source interfaces and inputs inspected; complete mathematical content read in both published 21-page readers through full text comparison. No external input/include source files; current analytic proof is in main.tex, not historical notes.'),
 'simultaneous_amplification_beyond_three_halves.pdf':('embedded reader','All 21 pages covered by full extracted comparison to fully read standalone reader; every difference inspected. Distinct bytes/date from standalone.'),
 'release_bundle.sh':('release build wrapper','Full script read; calls replay/build and deterministic package generation. Not executed; no source or release mutation.'),
 'replay.sh':('replay wrapper','Full script read; rejects optimized Python then invokes three certifiers and integration checker with fail-fast shell behavior.'),
 'requirements.txt':('dependency pins','Full text read; no-index local wheel installation with exact version/hash pins.'),
 'test_verifier_fail_closed.py':('failure-propagation regression','Full code read; AST rejects bare asserts; ordinary/-O comparisons, optimized wrappers and disposable early/late mutations verify fail-closed behavior. It is not an independent mathematical proof.'),
 'vendor/README.md':('dependency guide','Full text read; wheel hashes/upstream identities/license and external tool boundaries. Refers to absent submission/ENVIRONMENT.md; main README contains sufficient tool-boundary description.'),
 'mpmath-1.3.0-py3-none-any.whl':('third-party dependency','All 92 members enumerated, CRC and 91 hashed RECORD entries verified; metadata/WHEEL/license inspected. Library implementation not independently audited; not a manuscript proof or additional reader.'),
 'sympy-1.14.0-py3-none-any.whl':('third-party dependency','All 1570 members enumerated, CRC and 1569 hashed RECORD entries verified; metadata/WHEEL/license interfaces inspected. Library implementation not independently audited; not a manuscript proof or additional reader.'),
 'verify_paper_claims.py':('integration/algebra checker','Full code read; reconstructs responses, checks feasibility and rational algebra, and searches main.tex for scope/proof strings and absence of retired artifact names. String presence does not verify the mathematical content of those proofs.')
}
ledger=[]
for x in outer:
 n=x['name'];key=n if n in dispositions else n.removeprefix(prefix)
 if key not in dispositions:key=Path(key).name
 kind,extent=dispositions[key]
 ledger.append({**x,'kind':kind,'read_extent':extent,'execution_by_scope_reviewer':'not run; independent static meaning/integrity only','used_as_proof_authority':False})
(s/'support_read_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
# Exact external interfaces, with honest bounded coverage.
primary=json.load(open(s/'primary_acquisition_ledger.json'));prior=json.load(open(s/'prior_archive_interface_ledger.json'))
readscopes={
 'svoboda2024':'Primary main-paper introduction pp. 2–4, complete Model section pp. 4–5, positive result/Theorem 3 and explanation pp. 7–9, discussion pp. 9–10. Not a full independent reproof of its negative theorems.',
 'svoboda2024si':'Section 4 introduction, model/construction interfaces, Section 4.3 theorem statement/proof at pp. 8–9; sampled surrounding mechanism text. Full original technical appendix not independently audited.',
 'tkadlec2020':'Main primary abstract and publication/version metadata; model and exact theorem/proof interfaces read in SI rather than claiming all main-paper prose read.',
 'tkadlec2020si':'Complete Section 2 model, Section 3 theorem statements pp. 2–4, and transience/boundedness proof on pp. 7–8. No full proof audit of mixed-rule theorems.',
 'brewster2026':'Entire two-page primary extended abstract, including category and pointer to full arXiv version. Full 2511.18252 not acquired/read; no technical dependency on it.',
 'zenodo21753405':'Full public API metadata/file descriptors. Named paper member additionally acquired below; not an audit of the repository-wide release.',
 'zenodo21850042':'Full public API metadata/file descriptors. Named paper member additionally acquired below; not an audit of the repository-wide release.',
 'zenodo21852072':'Full public API metadata/file descriptors. Named paper member additionally acquired below; establishes release history, not validity of older proof.',
 'current_versions':'Full API versions response; reports one published version for current concept, exact selected record 22089807, metadata version 2.0.4.'
}
for x in primary:x['read_extent']=readscopes[x['id']]
for x in prior:
 for f in x['selected_interfaces']:
  if x['record_id']==21753405:f['read_extent']='Paper abstract and Sections 1–2/Corollary 3/quantifier discussion (pp. 1–3); source model and theorem statements cross-checked. No full independent proof audit of this separate work.'
  elif x['record_id']==21850042:f['read_extent']='Abstract, author summary, introduction, model and Definition 1 (pp. 1–3): exact earlier interval, endpoint limitation and quantifier order; no full separate-work proof audit.'
  else:f['read_extent']='Abstract, author summary, model, Definition 1, construction and Theorem 2 (pp. 1–4): same-work earlier theorem and version relationship; no older favorable audit or historical proof treated as current evidence.'
(s/'primary_read_ledger.json').write_text(json.dumps({'primary_sources':primary,'prior_member_interfaces':prior,'literature_limits':['Focused direct-predecessor and model/quantifier interface review, not an exhaustive novelty or priority search.','No outside communication or outreach preparation.','Prior repository ZIPs were range-read only; selected member CRC/size and SHA-256 are checked, but whole-archive MD5 was not reverified.','No external manuscript supplies the current analytic gain-scale proof; it must stand or fail on its own.']},indent=2)+'\n')
claims=[
 {'id':'H1','claim':'Theorem 3: R_sim >= R_hyb > 3/2 with one fitness-independent graph sequence','assumptions':['finite connected loopless undirected weighted graph','uniformly random single initial mutant','resident fitness 1, fixed mutant fitness 1<r<R_hyb','pure Bd and pure dB, separately','same-order complete-graph baselines','t increases, threshold t0 may depend on r'],'mechanism':'Proposition 5 weak-cut Schur trace; Proposition 6 gain-scale center estimates; Proposition 12 macro sweep; Proposition 13 responses; Lemma 14 positivity; Lemma 2 dyadic diagonal.','boundary_cases':['r=1 excluded; average neutral fixation is 1/n','r=R_hyb excluded; first-order corrections vanish and endpoint sign is not proved','no uniform t0 near endpoints or for r_t','one growing sequence does not contradict fixed-graph transience'],'required_falsification':'Independently verify establishment/cleanup and reciprocal estimates at o(q/C), generator time changes, stopped comparisons and limit order. Finite code replay alone cannot close this gate.','status':'hypothesis under independent analytic/adversarial gates'},
 {'id':'H2','claim':'Proposition 15 exact threshold within fixed-positive-parameter first-order dilute response model','assumptions':['response formulas (41)–(42)','fixed sigma>0 and lambda>0','positivity on an interval starting at 1'],'mechanism':'Quadratic feasibility and sextic discriminant/tangency.','boundary_cases':['not optimality over all graphs','not size-dependent or singular parameters, second-order zero-boundary gains, other density scales, or other modules'],'required_falsification':'Check positive denominators, exact root interval, and immediate infeasibility beyond R_hyb.','status':'finite algebra checkable; interpretation restricted'},
 {'id':'H3','claim':'Corollary 16 rational-edge graph family crosses 3/2','assumptions':['sigma=19/137, lambda=20/27','same weak-cut and gain-scale analytic assumptions','positive dyadic weak edges'],'mechanism':'Exact margins 232/17361 and 65/12123 at r=3/2; dB threshold quadratic.','boundary_cases':['rational weighted does not mean unweighted','no claim at rational-family endpoint','does not remove small weak-edge requirement'],'required_falsification':'Check algebraic threshold and both response signs over entire open interval, then current analytic theorem inputs.','status':'conditional analytic construction plus exact finite algebra'},
 {'id':'H4','claim':'Supplied certificates replay finite code assertions','assumptions':['unoptimized compatible Python','SymPy 1.14.0, mpmath 1.3.0 for symbolic paths','unaltered archived code and source'],'mechanism':'Three certifiers plus integration and failure-propagation scripts.','boundary_cases':['single n=9 labelled transition test, not universal enumeration','scope-string tests do not validate prose proofs','no formal proof assistant or complete computer-assisted asymptotic certificate'],'required_falsification':'Independent replay and meaningful mutation tests assigned to separate reviewer; scope independently checked all archive/wheel hash sets.','status':'static semantics established; execution deliberately left to independent family'}
]
(s/'claim_boundary_map.json').write_text(json.dumps({'record_id':22089807,'claims':claims,'follow_up':None},indent=2)+'\n')
verdict={
 'record_id':'22089807','role':'independent_source_acquisition_publication_scope_and_primary_interface_review','status':'COMPLETE','completed_utc':now,'completion_percent':100,
 'scope_verdict':'content_ready_subject_to_separate_mathematical_gate','mathematical_gate':'not_decided_by_this_scope_verdict','substantive_scope_defect_found':False,'substantive_mathematical_defect_found':'not_certified_by_scope_review','novelty_certified':False,'peer_review_certified':False,'follow_up':None,
 'read_scope':{'current_standalone_reader':'all 21 pages','current_embedded_reader':'all 21 pages through complete extracted comparison; every difference inspected','current_support':'23-member exhaustive inventory, paper certifiers/wrappers/tests/manifester statically read; 1662 nested wheel members inventoried and CRC/RECORD checked','primary_interfaces':'exact extents and honest gaps in primary_read_ledger.json'},
 'independence':'No current analytic/adversarial reports or prior favorable audit bodies used. Archived RESEARCH_LOG.md intentionally inventory/hash only. Release notes read only for package/version scope; not accepted as proof.',
 'non_substantive_source_caveats':['Standalone and embedded PDF bytes/date differ as recorded; no mathematical text difference found.','Stale no-new-DOI prose and v2.0.3 source-link text are preserved as historical source; public metadata binds reviewed record/version 2.0.4.','vendor/README.md points to absent submission/ENVIRONMENT.md; document runtime requirements are also stated in top README.'],
 'publication_conditions':['Wait for independent analytic and adversarial scientific gate.','Keep exact quantifier order, uniform singleton initialization, loopless undirected weighted hypotheses and both finite-n baselines.','State that gain vanishes and onset/endpoint are not established.','Restrict exact optimality to displayed first-order response model with fixed positive parameters.','Credit Svoboda 2024 and earlier fixed-graph/three-halves releases.','Use standalone deposited PDF bytes unchanged; retain complete tar archive.','Record original named release 2026-08-08 separately from reviewed edition 2026-08-25.','Retain unrefereed status, AI disclosure and no follow-up by default.'],
 'held_content':'content.json','promotion_authorized':False,
 'files':['REVIEW.md','content.json','verdict.json','RESEARCH_LOG.md','archive_inventory.json','nested_member_inventory.json','asset_inspection_summary.json','reader_asset_ledger.json','reader_diff.patch','extraction_receipt.json','support_read_ledger.json','primary_acquisition_ledger.json','primary_read_ledger.json','prior_archive_interface_ledger.json','claim_boundary_map.json','SCOPE_SHA256SUMS']
}
(s/'verdict.json').write_text(json.dumps(verdict,indent=2)+'\n')
print('Wrote held content, verdict, support and primary read ledgers, claim map.')
