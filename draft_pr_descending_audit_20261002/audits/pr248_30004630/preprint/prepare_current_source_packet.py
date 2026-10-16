"""Prepare the current PR packet only after publication and tracker readback."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil

PRE=Path(__file__).resolve().parent
D=PRE.parent/'initial_review_20261013'
PUB=PRE.parent/'publication'
S=D/'submitted/unsolved_math_prioritization/attempts/30004630'
T=PRE/'pr_update/30004630'
utc=datetime.now(timezone.utc).isoformat()
clear=json.loads((PRE/'FINAL_CLEARANCE.json').read_text())
assert clear['mathematical_verdict']=='PASS' and clear['fresh_clean_reviews']>=3
z=json.loads((PUB/'ZENODO_VERIFIED_PUBLICATION.json').read_text())
t=json.loads((PUB/'TRACKER_VERIFIED_APPEND.json').read_text())
assert z['submitted'] and z['metadata_and_files_verified'] and t['verified'] and t['doi_url']==z['doi_url']
doi=z['doi_url']
assert not T.exists(), 'Current packet already exists; inspect before changing it'
shutil.copytree(S,T)

body=(S/'COUNTEREXAMPLE.md').read_text()
old='**First-turn full negative candidate, independent review pending.**'
assert body.count(old)==1
body=body.replace(old,'**Accepted after independent mathematical, source, bounded priority and sequential fresh manuscript audits.** Unrefereed preprint and verification package: '+doi+'. The original first-turn draft remains preserved at native head e9c5d10978764db2cf25fa7d49cf4bd14a82d604 and in the verification archive.')
old='4. Under terminal-target perturbations of H norm epsilon, every global optimizer u_epsilon satisfies'
assert body.count(old)==1
body=body.replace(old,'4. Under radial terminal-target perturbations y_d^epsilon=(pi+epsilon)e of H norm epsilon, every global optimizer u_epsilon satisfies')
old='The tangent cone is the whole L^r(0,1;H), with r=1 in the paper\'s beta_2=0 convention, or the whole L^2 if that topology is used. Therefore'
assert body.count(old)==1
body=body.replace(old,old[:-len('Therefore')]+'For a proof, truncate any direction by its pointwise Hilbert norm; each bounded truncation becomes feasible after sufficiently small scaling and the truncations converge in either norm. This is a dense tangent argument, not norm interiority in L^1 or L^2. Therefore')
old='The limit retains L^4L^12 and energy bounds, so y^5 belongs to L^1L^2 and the weak solution is the unique mild solution.'
assert body.count(old)==1
body=body.replace(old,'The limit retains L^4L^12 and energy bounds, so y^5 belongs to L^1L^2. Strong endpoint convergence retains zero initial traces. Subtract the linear Duhamel solution forced by u-y^5; the remainder satisfies the homogeneous Dirichlet wave equation with zero traces. Projection on every Dirichlet eigenmode gives the zero scalar solution, so the remainder vanishes. The limit is therefore the actual unique mild solution.')
body+='\n## 7. Current manuscript, weaker norm and provenance\n\nThe six-page research note supplies a precise full proof, including the compatible-state local residual y+L(y^5)-Lu with identity derivative, and the additional local L^1 quadratic growth and fixed-basepoint optimizer estimates. For arbitrary small H target perturbations, every global optimizer has L^1 norm O(epsilon) and L^2 norm O(sqrt(epsilon)), uniformly over finite nonnegative velocity weights. Along the positive radial ray, L^1 norm is Theta(epsilon) and c epsilon^(3/4)<=L^2 norm<=C sqrt(epsilon); the lower comparison neighborhood is for each fixed finite weight. No sharp exponent, pairwise Lipschitz selection, perturbed uniqueness or L-infinity optimizer convergence is asserted.\n\nAI tools were used extensively in solving, verification, priority research and writing. No external human peer review or proof-assistant formalization is claimed. Classical wave estimates, group-sparse threshold calculus and concentration/noncoercivity methods are credited. No covering predecessor was authenticated in the bounded accessible corpus; worldwide firstness is not certified. Historical pending labels and reviews refer to the preserved original bytes, not this updated presentation.\n'
(T/'COUNTEREXAMPLE.md').write_text(body)
(T/'README.md').write_text('''# 30004630 — quadratic growth without quadratic control regularization

**Claimed solved as a negative answer to the unchanged ordinary-critical-cone implication.** On the unit three-dimensional ball, the defocusing quintic-wave problem has a unique global zero optimizer for a sufficiently small positive constant Hilbert cap. Its ordinary critical cone is explicitly {0}, so strict positivity there is vacuous. Feasible controls converge in L-infinity with objective gap o(the squared control-L2 norm), refuting both source localizations. Every global optimizer under positive radial terminal-target perturbations has L2 displacement divided by target displacement tending to infinity, for each fixed finite nonnegative terminal-velocity weight.

The paper also proves local L1 quadratic growth and arbitrary-target fixed-basepoint weaker-norm upper bounds. This is not a complete unregularized replacement theory, a sharp-rate theorem, pairwise Lipschitz selection, perturbed uniqueness or L-infinity optimizer convergence. The full nonlinear state is controlled by compatible-space estimates; it is not truncated to one eigenmode.

Six-page preprint and 113-file portable verification archive: '''+doi+'''. Seven standalone scientific checksets reproduce 5,603 exact finite assertions plus five noncertified diagnostics. These verify finite algebra and controls; the analytic proof supplies PDE validity, compactness, universal inequalities and optimizer quantifiers. Additional fresh independent stress checks are in the repository review records.

Three sequential NEW full manuscript reviews passed, including a full review after the editorial refinements, with a separate revised-payload addendum by the first reviewer. Mathematical/source audits and independent bounded classical/recent priority families passed. Established concentration/noncoercivity, sparse threshold calculus and wave estimates are credited; no worldwide-firstness certificate is claimed.

AI tools were used extensively. This is an unrefereed research note without external human peer review or proof-assistant formalization. `original_submission/` in the archive and native commit e9c5d10978764db2cf25fa7d49cf4bd14a82d604 preserve all19 original files. Old independent-review reports remain historical audits of those original bytes. Current presentation and acceptance are bound by FINAL_ACCEPTANCE.json and the regenerated current manifests.
''')
sources=(S/'SOURCES.md').read_text()
sources+='''
## Current adversarial verification, attribution and bounded priority

The locally optimal standing premise preceding Theorem4.17 is explicitly present on inspected preprint printed24 and carries into the cone and sufficient condition; the counterexample proves global optimality, so also meets this premise. The source permits the zero cone. No unsupported theorem extension is assumed.

The inspected arXiv v1 Theorem4.3 proof writes, at zero, a derivative y -> -(y,y_t) into arbitrary continuous energy pairs, which is not onto that codomain (for instance (0,tg) with g nonzero). The note does not inherit this proof step: its compatible zero-data residual y+L(y^5)-Lu has identity derivative and its quintic is a bounded five-linear polynomial. Direct contraction also proves the full-space O(A^5) remainder. This concerns the inspected preprint proof, not an assertion about the inaccessible final journal proof.

Classical credits: Herzog–Stadler–Wachsmuth2012, DOI10.1137/100815037, established group-sparse thresholds; Casas–Tröltzsch2012, DOI10.1137/110840406, separated ordinary-cone positivity from weak-null coercivity; Casas–Tröltzsch2015, DOI10.1365/s13291-014-0109-3, reproduces Dunn's classical exact-cone counterexample at Example4.16. Dunn's original chapter was not obtained. Casas–Herzog–Wachsmuth2017, DOI10.1051/cocv/2015048, gives sparse parabolic second-order theory whose strong-growth proof uses the quadratic coefficient. Christof–Wachsmuth2018, DOI10.1137/17M1140418, and Borchard–Wachsmuth2024, DOI10.46298/jnsao-2024-12604 (original preprint arXiv2311.14538v1,2023), establish the weak-null NDC framework. D. Wachsmuth–G. Wachsmuth2022, DOI10.46298/jnsao-2022-8733, develops weaker L1/measure growth under distinct threshold transversality assumptions. Their nonzero-gradient assumption fails for this quadratic sine contact. Recent extended-cone/state-growth and BL/transport theories have different hypotheses and conclusions.

Applying an old conditional NDC theorem after constructing the present data does not date the wave construction to that theorem. A prior theorem covering genuine local optimality, ordinary-cone positivity and failure of strong control-L2 growth in the actual source wave model would count as prior coverage even without the global, target or weaker-norm extras. No such complete or automatically covering construction was authenticated in the bounded accessible corpus. The 2023 author slides still state beta2-zero SOSC as open; this is a dated status witness, not worldwide openness certification. Some original/final bodies and deposit-history searches were inaccessible. All exact byte objects, retrieved versions, chronology, bridge proofs and access limits are recorded in the independently authored source and priority reports.

Three sequential NEW full manuscript reviews and the separate final editorial-payload addendum found no mandatory remaining issue. The manuscript makes no worldwide-firstness claim. Publication: '''+doi+'.\n'
(T/'SOURCES.md').write_text(sources)
meta=json.loads((S/'metadata.json').read_text())
meta['original_author_metadata']=dict(meta)
meta.update(status='claimed_solved',scope='Negative answer to retaining ordinary-cone strict positivity and strong control-L2 growth unchanged at beta2=0; radial all-global-optimizer target instability; independently verified weaker-norm bounds.',
            novelty_claim='No worldwide-firstness claim; bounded priority found no covering predecessor.',
            publication_metadata=json.loads((PRE/'metadata.json').read_text()),doi=z['doi'],doi_url=doi,
            review_status='Independent internal AI-assisted mathematical, source, bounded priority and three sequential NEW full manuscript audits passed; final revised payload independently checked.',
            external_human_peer_review=False,unrefereed=True,extensive_AI_use=True)
(T/'metadata.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
(T/'PUBLICATION_STATUS.md').write_text('''# Publication status — 30004630

**Claimed solved, 1/5 original substantive author turns**, as a negative answer to the unchanged ordinary-cone strict-positivity implication to strong control-L2 quadratic growth when beta2=0. The genuine unique global optimizer, zero cone/vacuity, positive Hilbert cap, critical quintic wave, fixed finite optional velocity weight and both source localizations are explicit. The target-instability theorem concerns the positive radial terminal-target ray; weaker arbitrary-target upper estimates survive.

Published six-page unrefereed preprint and portable verification package: '''+doi+'''. Exact metadata and both uploaded files were read back against the frozen deposit. The requested Google Workspace tracker entry was appended once and read back at '''+t['updated_range']+'''.

Independent mathematical and source families, extensive bounded priority families and three sequential NEW full manuscript reviewers passed; the final editorial revision also received a separate independent payload addendum. All mandatory issues are absent. Seven portable full scientific receipts match 5,603 exact assertions plus five noncertified diagnostics; finite controls do not certify the nonlinear PDE or unknown analytic constants. The analytic proofs do that work.

Established wave estimates, group-sparse thresholds and concentration/noncoercivity are credited. No covering predecessor was authenticated in the bounded accessible corpus, with access/version gaps explicitly preserved. No worldwide-firstness, source-author acceptance or external human peer-review claim is made. AI tools were used extensively; no proof-assistant formalization is claimed. Broader replacement theory, pairwise selections and sharp rates remain outside this result.

All19 original submission bytes and the original reviews are preserved at native original head e9c5d10978764db2cf25fa7d49cf4bd14a82d604 and in the archive. Their pending labels and old SHA references are historical. Current manifests below bind the updated presentation. Native merge remains pending until exact current-packet readback.
''')
with (T/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+utc+' — Best guess95% current acceptance/publication completion. Independent math/source/priority and three sequential NEW manuscript reviews passed, with final revised-payload addendum. Exact unrefereed AI-assisted note and verification archive published at '+doi+'; tracker append read back at '+t['updated_range']+'. Current presentation clarifies radial scope, dense tangents and mild-limit identification, while preserving historical submission and executable science. Native readback/merge remains.\n')
accept={'utc':utc,'problem_id':30004630,'status':'claimed_solved','author_turns':1,
        'original_native_head':'e9c5d10978764db2cf25fa7d49cf4bd14a82d604',
        'strongest_verified_claim':'Actual capped critical-wave global optimizer with zero ordinary cone and feasible Linfinity-null controls whose gap is o(control-L2 squared); fixed finite nu>=0; all radial global optimizers non-Lipschitz.',
        'additional_result':'Local L1 quadratic growth; arbitrary-target uniform upper bounds; per-fixed-nu radial exponent bracket, no sharpness.',
        'priority':'Bounded no covering predecessor authenticated; old concentration/threshold/wave/NDC inputs credited; worldwide firstness uncertified.',
        'mathematical_verdict':'PASS','fresh_full_review_count':3,
        'final_revised_full_review':'fresh_review_03','final_revised_independent_payload_addendum':'editorial_delta_review_01',
        'preprint_candidate_files':clear['candidate_files'],
        'publication':z,'tracker':t,'native_merge':'pending exact readback',
        'limitations':['Unrefereed; extensive AI use; no external human peer review or proof-assistant formalization','Unknown analytic constants remain existential; finite controls do not certify them','No complete unregularized replacement theory, sharp rate or perturbed uniqueness','Radial lower neighborhoods are for fixed finite nu, not arbitrary unbounded varying weights','Final publisher/original-source/history access limits recorded'],
        'historical_review_scope':'Original19 bytes at original native head and in original_submission/ archive; not retrospectively current presentation.'}
(T/'FINAL_ACCEPTANCE.json').write_text(json.dumps(accept,indent=2,ensure_ascii=False)+'\n')
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(T).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
current=[pin(p) for p in sorted(T.rglob('*')) if p.is_file() and p.name not in {'FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json'}]
(T/'FROZEN_MANIFEST.json').write_text(json.dumps({'utc':utc,'problem_id':30004630,'status':'claimed_solved','author_turns':1,'scope':'Current accepted presentation; immutable original manifests remain at original head/archive','files':current,'self_hash_omitted':True},indent=2)+'\n')
current.append(pin(T/'FROZEN_MANIFEST.json'))
(T/'PUBLICATION_MANIFEST.json').write_text(json.dumps({'utc':utc,'problem_id':30004630,'status':'claimed_solved','author_turns':1,'doi_url':doi,'files':current,'self_hash_omitted':True},indent=2)+'\n')
for name in ['verify_algebra.py','exact_receipt.json','source_manifest.json']:
    assert (T/name).read_bytes()==(S/name).read_bytes()
for p in (S/'independent_review').rglob('*'):
    if p.is_file():assert p.read_bytes()==(T/'independent_review'/p.relative_to(S/'independent_review')).read_bytes()
print(json.dumps({'utc':utc,'prepared_source_files':sum(p.is_file() for p in T.rglob('*')),'doi_url':doi,'native_mutations':0},indent=2))
