from pathlib import Path
import datetime, hashlib, json, re, zipfile

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]
SRC=BASE/'sources'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def writej(name,data): (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
receipt=json.loads((SRC/'receipt.json').read_text())
record=json.loads((SRC/'record.json').read_text())
tex=SRC/'published-source/main.tex'
abstract=tex.read_text().split('\\begin{abstract}\n',1)[1].split('\\end{abstract}',1)[0]
(ROOT/'abstract_original.tex').write_text(abstract)
plain=' '.join(abstract.split())
plain=plain.replace('$','').replace('\\alpha','α').replace('\\ge','≥').replace('\\sec^2','sec²').replace('\\pi','π')
(ROOT/'abstract_original.txt').write_text(plain+'\n')
writej('abstract_receipt.json',{'source':'sources/published-source/main.tex','source_sha256':digest(tex)['sha256'],'pdf_page':1,'main_pdf_sha256':receipt['files'][0]['sha256'],'extraction':'Complete literal abstract environment, with full original TeX retained. Plain copy collapses whitespace and converts only displayed math notation; no sentence omitted.','tex':digest(ROOT/'abstract_original.tex'),'plain':digest(ROOT/'abstract_original.txt'),'plain_whitespace_word_count':len(plain.split())})
(ROOT/'ORIGINAL_ABSTRACT.md').write_text('# Complete original abstract\n\n'+plain+'\n\nSource: main.tex abstract environment, published PDF page 1. See abstract_receipt.json for exact source and output hashes.\n')

primary=json.loads((ROOT/'primary-source-receipts.json').read_text())
interfaces=[
 {'source':'owr-2023-12.pdf','read':'PDF pages15–18, printed653–656; complete Kleptsyn contribution and references','interface':'Open Problems1–2 on printed655 concern finite graphs: improve forest bound α>2 and equal-rate whisker bound α>25. The next paragraph suggests sharpness at4/3, a stronger target. Infinite graphs and possible infinite components are discussed separately.','use':'Authenticates the original request and separates an improvement from resolving the sharper suggested whisker statement.','limit':'No infinite-graph conclusion or independent current-openness/priority certification.'},
 {'source':'hhk-2023-published.pdf','read':'PDF pages3–5 (printed3014–3016),9–10 (3020–3021),25 (3036); model, Conditions1–3, Theorem1, Proposition1, construction/Remark2, Lemma2 proof','interface':'Theorem1: finite G, α>1, all finite positive rates; normalized counts converge almost surely to a linearly stable or critical equilibrium; each strictly stable equilibrium has positive attainment probability. Proposition1 under bounded degrees and rates0<λv≤L excludes unbounded counts with zero lower growth rate. Unit initialization is the default; arbitrary integer starts appear in the construction. Disconnected components evolve independently. Lemma2 proves even-cycle instability in the equal-rate setting.','use':'Finite stochastic convergence/support bridge; strongest fully general convergence result used here, including critical limits. Even-cycle perturbation method credited.','limit':'No replacement of stable-or-critical by strictly stable. No inference that conditioning on a finite component of an infinite graph preserves a standalone finite WARM law. The paper itself supplies positive-integer tail transfer and unequal-rate even-cycle extension.'},
 {'source':'warm-2016-published.pdf','read':'PDF pages3–10 (printed2495–2502), model and Conditions1–3, Examples4–5, Definitions1–2, Theorem1, Proposition2(iv)–(v), Theorem4(ii)','interface':'Unit-count discrete-time graph WARM uses uniform vertex selection. Theorem1(ii) gives positive probability of convergence to every linearly stable equilibrium. Proposition2 gives uniform odd-cycle stability iff α<sec²(π/(2m)), and triangle uniform stability iff α<4/3. Theorem4(ii) excludes fully supported linearly stable triangle equilibria for α>4/3.','use':'Credits known uniform-cycle threshold and below-threshold triangle obstruction. Published2016 attainment supports the same unit-start obstruction also supplied by HHK2023.','limit':'Theorem4(ii) is not a positive-attainment statement; it is an above-threshold stability exclusion. Uniform bare-cycle calculation alone is not a universal arbitrary-weight, attached-cycle instability theorem.'},
 {'source':'hk-2017-author.pdf','read':'Author pages3–10 and21–24; model, ConditionG/generalized graph setting, stable/critical definitions, Theorems0–3, Corollary1, Example1, complete §5.1 Lemmas5–8 and proofs','interface':'Theorem3 excludes leaf-free support subsets for α>2 in the general selection model, yielding arbitrary-rate finite graph forests. Theorem2(a) under uniform vertex selection gives a graph-independent whisker threshold≤25. Example1 permits stable four-edge paths with unequal rates for sufficiently large α. §5.1 gives constants2.25,4.5,20.25 and champion/least-weight steps; the small-edge leaf estimate requires α>2.25(exp(2.25)+1).','use':'Credits deterministic prior bounds and the least-weight/champion method; authenticates the manuscript’s conservative >24 consequence of the displayed old constants.','limit':'This downloaded copy is the author manuscript dated March2017, not claimed to be the publisher PDF. The manuscript’s >24 consequence is retained; metadata’s ≥24 wording is not silently substituted. The old convergence conjecture is superseded for the present use by HHK2023.'}
]
for x in interfaces:
 r=next(t for t in primary if t['name']==x['source']);x.update({k:r[k] for k in ['url','sha256','version','pages']})
writej('primary_interfaces.json',interfaces)

support_names=[('main.tex','All481 lines read and compared with complete seven-page PDF'),('original/PROOF.md','Full mathematical proof and unequal-rate path appendix read; historical partial label treated only as authored status'),('README.md','Full current scope and reproduction instructions read; author prior-review summaries incidental'),('audit/forest/verify_forest.py','Full261-line source read; finite_controls and custody entrypoint distinguished; not executed'),('audit/whisker/VERIFY.py','Full170-line source read; exact finite arithmetic and source-interface limits mapped; not executed'),('audit/whisker/EXACT_CERTIFICATE.json','Full rational rows, interval/domain flags and exponential certificate read; stored historical input hashes do not constitute opinions'),('verification/run_checks.py','Full82-line runner read; closed inventory, disposable read-only mirror, normal/-O/-OO behavior mapped; not executed'),('verification/forest_controls.py','Full8-line mathematical wrapper read; not executed')]
supports=[]
for name,reading in support_names:
 p=SRC/'published-source'/name;supports.append({'path':str(p.relative_to(BASE)),**digest(p),'reading':reading})
claims=[
 {'pages':'1–2','claim':'Theorem1 forest','quantifiers':'Every finite simple undirected loopless G, every fixed strictly positive vertex-rate vector, every fixed positive integer initial edge-count vector; every exponent α>4/3; with probability one (V,E∞) is a forest. Isolated vertices are harmless.','mechanism':'Exclude even cycles at all α>1 and odd cycles by weighted Hessian estimate, then apply imported finite convergence/support and integer-start tail transfer.'},
 {'pages':'2,4','claim':'Sharp strict forest constant','quantifiers':'For each1<α<4/3, the equal-rate triangle with unit initial counts retains all three edges with positive probability. Therefore no lower strict universal threshold works. No claim atα=4/3.','mechanism':'Known uniform triangle equilibrium: Jacobian eigenvalues−1 and3α/4−1 twice; known positive attainment for strictly stable equilibria.'},
 {'pages':'2,4–6','claim':'Theorem1 whiskers','quantifiers':'Same finite/simple/loopless/integer model, with equal positive firing rates; every α≥17/4; with probability one every surviving component is a tree of diameter≤3. A star is allowed; no bound on number of leaves.','mechanism':'Least positive edge≥1; internal edge≤3/2 contradicts a necessary diagonal stability inequality, by five closed rational intervals and analytic tail; heavier internal edges form a matching.'},
 {'pages':'3–4','claim':'Theorem3 weighted cycle instability','quantifiers':'Every valid equilibrium whose positive support contains an even cycle is linearly unstable forα>1. For an odd support cycle lengthm, instability holds forα>sec²(π/(2m)). Arbitrary positive rates, unequal equilibrium weights, chords and attachments allowed.','mechanism':'Potential Hessian in y=a^α coordinates, bound4Σc≤ΣD, alternating even perturbation or summed sine/cosine odd perturbations.'},
 {'pages':'2–3','claim':'Lemma2 initialization and boundary interface','quantifiers':'One-way transfer of almost-sure tail assertions from unit counts to any fixed positive integer counts by a positive-probability finite prefix. No transfer of positive attainment of a specified stable equilibrium to every start. At limiting support every nonisolated vertex has a positive incident edge; zero coordinates form a−I Jacobian block.','mechanism':'Embedded jump chain, Poisson memorylessness, finite time-shift invariance; α>1 makes derivative of zero coordinate power vanish.'},
 {'pages':'6–7','claim':'Attribution and unresolved scope','quantifiers':'Earlier stated whisker25 can already be conservatively improved to>24 using its displayed constants and the later stochastic bridge. Current contribution claims17/4 plus arbitrary-rate forest4/3; suggested whisker interval4/3<α<17/4 and stochastic equality4/3 remain unresolved here.','mechanism':'Exact exponential cap and old least-weight/champion inequalities; no new convergence theorem, even-cycle mechanism, uniform-cycle threshold or triangle obstruction claimed.'}
]
limitations=[
 'Finite graphs only. No theorem for infinite WARM graphs, no claim that all infinite-graph surviving components are finite, and no conditioning shortcut from an infinite component to a finite process.',
 'Forest conclusion permits unequal positive rates; whisker conclusion requires equal rates. Unequal-rate long-path stable examples are known.',
 'Initial counts are fixed positive integers. Zero counts, positive noninteger offsets, loops and multigraph extensions are not asserted.',
 'α=4/3 is excluded from the forest theorem and its attainment argument. The equal-rate whisker threshold17/4 is sufficient and inclusive, not claimed optimal.',
 'Survival means infinitely many reinforcements E∞; its identification with positive limiting linear growth uses the imported support theorem. This is not merely a statement about a deterministic support.',
 'Almost sure universal structural conclusions differ from the positive-probability unit-triangle obstruction. No realization probabilities, convergence rates or finite observation times are supplied.',
 'Whisker means tree of diameter at most3, including arbitrarily large stars; no vertex-count bound or unique survivor graph follows.',
 'No claim about empirically observed neural networks or biological validity follows from the stochastic graph model.',
 'The paper is an AI-assisted unrefereed preprint. No external human peer review, journal acceptance, proof-assistant certification or exhaustive novelty/priority claim is established.',
 'Scope reviewer inspected mathematical code but did not run published controls or independently certify the universal proofs. Historical priority/correctness verdict bodies remained unread.'
]

reader=json.loads((ROOT/'reader_document_map.json').read_text())
reader.update({'distinct_reader_documents':1,'distinct_reader_pages':7,'additional_reader_pdfs':0,'all_reader_pdfs_read':True,'all7_main_pages_visually_inspected':True,'magic_scan_all45_members':True,'nested_archives':0,'notes':'Archive PDF is byte-identical to the top-level reader. All other members are authored support, code, metadata or historical wrappers; no additional reader hiding behind a non-PDF suffix found.'})
writej('reader_document_map.json',reader)
scope={'record_id':'23592692','work_id':'Z-23592691','sheet_row':61,'title':record['metadata']['title'],'version':'1.0.0','publication_date':'2026-10-21','doi':'10.5281/zenodo.23592692','record_url':'https://zenodo.org/records/23592692','eligibility':'published_paper_record_with_manuscript','review_type':'acquisition_and_scope','status':'SCOPE_COMPLETE','mathematical_verdict':None,'completion_percent':100,'completed_utc':now,'bound_assets':receipt['files'],'record_sha256':digest(SRC/'record.json')['sha256'],'receipt_sha256':digest(SRC/'receipt.json')['sha256'],'main_pdf_sha256':receipt['files'][0]['sha256'],'main_tex_sha256':digest(tex)['sha256'],'source_support':supports,'reader_map':'reader_document_map.json','reader_pages':7,'archive_regular_files':45,'nested_archives':0,'additional_reader_pdfs':0,'original_abstract':'abstract_original.txt','abstract_receipt':'abstract_receipt.json','content_candidate':'CONTENT_CANDIDATE.md','report':'SCOPE_REVIEW.md','primary_interfaces':'primary_interfaces.json','claim_map':claims,'limitations':limitations,'follow_up':None,'follow_up_rationale':'Existing endpoint and sharp-whisker gaps are substantive and already stated by the literature/paper. Scope has not established a new well-supported conjecture or research direction beyond restating them; do not create a page follow-up section by default.','scope_verification':{'all_public_assets_size_md5_sha256_match':True,'all45_extracted_files_final_rehashed_unchanged':True,'complete_main_paper_read':True,'all7_main_pages_visually_inspected':True,'original_primary_question_authenticated':True,'four_primary_pdf_downloads_successful':True,'submitted_diagnostics_executed':False},'independence':{'sibling_reviews_read':False,'historical_dedicated_verdict_or_acceptance_bodies_read':False,'incidental_status_exposure':['Current Zenodo metadata, current README and mainSection6 summarize historical mathematical/priority audits and partial-status reconciliation.','Original PROOF.md has an authored opening partial label and closing stronger-whisker gap; these are not adopted as a current verdict.','Mathematical code includes literal PASS templates; certificate lists hashes/names of historical acceptance and audit artifacts without opening those bodies.'],'interpretation':'No historical conclusion or stored checker output used as fresh evidence; raw hashing is not substantive opinion reading.'},'strongest_verified_scope_result':'Exact seven-page edition and all45 archived members authenticated; full paper and necessary mathematical support read, primary original questions and theorem interfaces mapped with finite/equal-rate/critical-boundary distinctions.','remaining_gap':'Independent analytic and adversarial reviewers must validate universal weighted-cycle instability, the whisker scalar estimates and the initialization/stochastic imports and run meaningful controls. Scope issues no mathematical approval or priority certification.','publication_actions':[]}
writej('scope.json',scope)

(ROOT/'CONTENT_CANDIDATE.md').write_text('''# Conditional page content — finite WARM graphs

This is an editorial candidate only, pending independent mathematical clearance and the parent publication gate. No page has been created or published by this scope task.

Suggested slug: `finite-warm-forest-whisker-bounds`

Suggested search title: `When reinforced graphs become forests | Alec Kriebel`

Suggested description: `A finite WARM graph preprint gives the sharp strict forest bound α > 4/3 and an equal-rate whisker bound α ≥ 17/4, with source files and limitations.`

Paper title: **A sharp forest bound and an improved whisker bound for finite WARM graphs**

Status: Unrefereed preprint · Version 1.0.0 · 21 October 2026. AI tools were extensively involved; internal AI review is not independent human peer review.

## In plain language

Imagine a finite network in which each vertex has its own clock. When a clock rings, one neighboring edge is reinforced. An edge that has been chosen often becomes more likely to be chosen again; the exponent α controls how strongly past choices are favored.

The paper studies the edges that continue to be reinforced forever. It shows that when α is greater than 4/3, those surviving edges almost surely contain no cycles, even when vertices fire at different rates. This strict threshold cannot be lowered: for 1 < α < 4/3, a triangle can keep all three edges with positive probability.

When all vertices fire at the same rate and α is at least 17/4, the surviving pieces have an even simpler shape. Each is a tree whose farthest vertices are at most three edges apart—a shape called a whisker. A whisker can still have many leaves; this is a bound on diameter, not on its number of vertices.

## What is interesting

A triangle already gives the obstruction for 1 < α < 4/3. The main cycle estimate shows that this small example sets the strict universal forest threshold even for much larger finite graphs with unequal rates, unequal edge weights and extra attached edges. The paper extends a known calculation for uniform bare cycles to arbitrary equilibrium weights and surrounding graph structure.

## Relation to earlier work

The question comes from Viktor Kleptsyn’s finite-graph improvement requests in [Oberwolfach Reports 12/2023](https://doi.org/10.4171/owr/2023/12). The paper uses established convergence and survival-support theorems of [Hirsch, Holmes and Kleptsyn](https://doi.org/10.1088/1361-6544/acc9a0), the uniform-cycle and triangle results of [van der Hofstad, Holmes, Kuznetsov and Ruszel](https://doi.org/10.1214/16-AAP1153), and the least-weight/champion arguments of [Holmes and Kleptsyn](https://doi.org/10.1063/1.4978683). The earlier stated whisker bound was 25; its displayed proof already yields a weaker improvement above 24. The contribution presented here is the stronger 17/4 bound together with the sharp strict forest bound, without a worldwide-firstness claim.

## Scope and limitations

The model uses finite simple undirected graphs, positive firing rates and fixed positive integer initial edge counts. The whisker conclusion requires equal rates. The paper does not settle what happens at α = 4/3 or establish the suggested sharp whisker conclusion throughout 4/3 < α < 17/4. It makes no infinite-graph, loop, noninteger-initialization or empirical biological claim.

## Paper and supporting files

- [Version-specific Zenodo record and DOI](https://doi.org/10.5281/zenodo.23592692)
- [Published paper PDF](https://zenodo.org/records/23592692/files/finite-warm-thresholds.pdf)
- [Source and verification archive](https://zenodo.org/records/23592692/files/finite-warm-thresholds-source-and-verification.zip)

The existing template may embed the authenticated PDF and retain a direct-download fallback. Use the complete original abstract in `abstract_original.txt`, preserving every qualification and the AI/unrefereed disclosure; do not substitute the summary above for the abstract.

## Collaboration

Researchers familiar with reinforced stochastic processes, stochastic approximation or dynamical systems are welcome to examine the arguments, identify corrections and discuss substantive further work or a journal submission. Any coauthorship would reflect a meaningful contribution and mutual agreement.

No new follow-up question or conjecture is proposed for this page. Existing unresolved endpoints belong in the limitations, without implying that a new route has been established.
''')

(ROOT/'SCOPE_REVIEW.md').write_text(f'''# Acquisition and scope — Zenodo23592692

Completed {now}; scope100%. Mathematical verdict: **not issued**. No site, spreadsheet, Git, deploy, UI or outreach actions.

## Exact edition and custody

Frozen reconciliation row61 identifies workZ-23592691 and version-specific record23592692, *A sharp forest bound and an improved whisker bound for finite WARM graphs*, version1.0.0,21October2026. This is an expressly published preprint with its own seven-page PDF, not an incidental manuscript in an unrelated release archive. Author Alec Kriebel, ORCID0009-0001-9320-500X; CC BY4.0. The record’s concept DOI is23592691; cite version DOI10.5281/zenodo.23592692 for this review.

Fresh Zenodo API metadata and every public file were acquired and authenticated against exact API size and MD5; SHA256 identities were calculated. Top-level PDF SHA256 `{receipt['files'][0]['sha256']}`; source ZIP SHA256 `{receipt['files'][1]['sha256']}`. Detailed URLs, timestamps and sizes are in sources/receipt.json. The mainPDF matches the frozen queue identity. All45 regular ZIP members had safe path/type and CRC validation before extraction, followed by full final digest comparison. No nested archives, hidden additional PDF readers or distinct reader supplements were found. The archive’s output/pdf copy is byte-identical to the public mainPDF. Original assets and extracted bytes remain unchanged.

## Coverage and independence

Read the complete seven-page published PDF, all481 lines of main.tex, the complete original PROOF.md including its unequal-rate path appendix, the current README, the complete forest/whisker mathematical programs, the whisker exact certificate, and the portable runner/wrapper. All seven reader pages were rendered and visually inspected. The abstract is captured completely, both exact TeX and a whitespace-normalized plain mathematical rendering, with source/output hashes and a word count.

The core analytic proof is in the current paper. The historical PROOF adds useful derivation context and an exact unequal-rate four-edge-path control; the current paper changes the initialization discussion and makes the whisker proof independent of the new cycle theorem. A finite exploratory tree search mentioned in old support does not supply a universal theorem. Mathematical finite-control code covers equilibrium/Hessian relations, weighted and attached cycles, the critical triangle, zero-edge boundary, integer reachability, five rational whisker intervals, and the unbounded exponential tail. I read those interfaces but executed no submitted checker and make no claim that its stored expected outputs were reproduced. The priority runner depends on old report statements; neither it nor historical opinion reports was read for a verdict or used as a proof.

Dedicated archived acceptance, audit, priority-verdict and historical status bodies remained opaque. Necessary current metadata, README and Section6 summarize earlier internal reviews and reconcile old partial labels. Original PROOF’s opening partial label and closing stronger-target gap were visible while reading its mathematics. Code has literal PASS output templates and the exact certificate lists historical input names/hashes. These incidental author statements are disclosed, not adopted as fresh correctness evidence. No sibling report or mathematical conclusion was read. Only raw primary paths/versions/hash receipts were sent to the independent reviewers.

## Exact stochastic model and quantifiers

G is finite, simple, undirected and loopless. Each nonisolated vertex has an independent Poisson clock of fixed rateλv>0. Each edge starts with a fixed integer ne≥1. At a firing of v, edge e is chosen with probability proportional to Nt(e)^α among the incident edges and its count increases by1. α>1; isolated vertices have no effect. This is an interacting reinforced-urn model, not a directed random walk or a statement about measured biological networks.

E∞ is the set of edges whose counts diverge; E+ uses positive lower asymptotic count per unit time. Their almost-sure identification is an imported theorem, not a definition. The finite graph implies finitely many firing clocks, bounded degrees and an upper rate bound automatically. In the probability normalization Λ=Σλv, x=a/Λ and pv=λv/Λ, the drift scales as Fλ(a)=ΛFp(a/Λ) and its Jacobian is unchanged.

Theorem1 has two different universal almost-sure conclusions: α>4/3 gives a forest for arbitrary positive rates; equal rates and α≥17/4 give components of diameter≤3. A whisker includes stars and has no vertex-count bound. Sharpness means no smaller strict forest constant works: for every1<α<4/3 the equal-rate unit-initialized triangle has a positive probability of retaining all three edges. It does not claim almost-sure triangle survival, arbitrary-initialization attainment, or a theorem at the equality endpoint4/3.

The finite-prefix Lemma2 transfers almost-sure tail assertions one way from unit counts to arbitrary fixed positive integer counts. It does not reverse the implication for positive probability of convergence to a specified equilibrium. The paper explicitly uses stable attainment only for the unit triangle. Positive real noninteger offsets and initially zero counts are outside this paper’s theorem, regardless of what related constructions may permit.

At a stochastic limit each positive-rate vertex has a positive incident edge, so the denominators stay nonzero on the relevant face. Forα>1, the derivative of a zero coordinate’s power vanishes and the omitted-edge Jacobian block is−I. Stable and critical equilibria are both allowed by the convergence theorem; the deterministic exclusions need a strictly positive eigenvalue, not merely failure of strict stability.

## Claimed deterministic contributions

Theorem3 excludes every positive-support even cycle atα>1 and every odd cycle of lengthm atα>sec²(π/(2m)). The statement permits unequal positive rates, arbitrary equilibrium weights, chords and attachments. Its mechanism changes to y=a^α, uses the potential Hessian and 4Σcycle c≤Σcycle D, then tests an alternating even direction or a pair of real sine/cosine odd directions. Since the maximum odd-cycle threshold is4/3 at the triangle, it leads to the universal forest claim. It is not merely a restatement of the previously known uniform bare-cycle spectrum.

The equal-rate whisker argument uses the necessary diagonal inequality q²+r²≥(1−1/α)(q+r), with a=q+r. It is expressly necessary rather than sufficient for stability. The least-weight lemma gives all positive weights≥1 forα>2. An internal edge of weight≤3/2 is then excluded by exact caps over five closed intervals spanning[17/4,7] and an analytic tailα≥7. The first interval’s strict margin is1/1734, including the lower endpoint17/4; the infinite tail uses C=3−√2 and an exact rational bound for exp(8/5). Internal edges above3/2 form a matching, excluding cycles and paths of four edges. This proof is explicitly independent of the new odd-cycle theorem.

The code and certificate are finite corroboration. A self-contained analytic chain and correctly imported stochastic foundations remain necessary; hashes prove custody rather than mathematical truth. Scope has mapped these claims, not independently approved them.

## Fresh primary-source interfaces

All four cited works were freshly downloaded from original publisher/institutional/author hosts, with URLs, versions, hashes and receipts. Exact read locations and limits are in primary_interfaces.json.

- OWR12/2023: the complete Kleptsyn contribution, printed653–656, including original Problems1–2 on655. The finite forest improvement and equal-rate whisker improvement are separate from the stronger suggestion of a sharp4/3 whisker threshold and from the subsequent infinite-graph discussion.
- HHK2023, published Nonlinearity36: model/Conditions1–3, Theorem1 printed3016, Proposition1 printed3021, construction/Remark2 and Lemma2 printed3036. The main theorem includes critical equilibria; positive attainment is for strictly stable equilibria. Proposition1 needs rates bounded above and positive, not a uniform positive lower bound. All are satisfied by each finite positive-rate instance. The paper’s integer-initialization conditioning is identified separately. The source expressly warns that conditioning on an infinite graph’s finite surviving component changes the law.
- VHHKR2016, published Annals of Applied Probability26: unit initialization, uniform graph sampling, Theorem1(ii), Proposition2(iv)–(v), and Theorem4(ii), printed2495–2502. The uniform odd-cycle threshold and triangle spectrum are known. Positive attainment is from Theorem1(ii) (or HHK2023); Theorem4(ii) instead excludes fully supported strictly stable triangle equilibria above4/3. This distinction is preserved.
- HK2017: author-hosted manuscript dated March2017, pages3–10 and21–24. The generalized graph setting allows unequal selection probabilities. Theorem3 and Corollary1 supply the earlier forest bound2; Theorem2(a) gives the equal-rate whisker bound25. Example1 is an unequal-rate long-path obstruction. The full least-weight/champion proof and displayed constants were inspected. This is an author manuscript, not mislabelled as a publisher PDF.

No additional comprehensive novelty search or firstness verification is claimed. The current paper already credits all these mechanisms. The original reference entry shortens the OWR contribution to653–655; the actual contribution continues through656, which was also read. This is a bibliographic scope detail, not a change to the located questions on655.

## Attribution, edition details and limitations

The earlier published stated whisker bound is25, but the paper explains that its displayed constants already give a conservative >24 consequence once combined with the later stochastic bridge. Fresh Zenodo metadata says≥24 while the operative PDF/TeX says>24; candidate prose follows the PDF’s conservative strict statement. Neither wording affects the claimed new17/4 theorem, and no numerical-first-improvement claim should be made.

The paper does not settleα=4/3, nor the suggested equal-rate whisker interval4/3<α<17/4. Unequal-rate whisker conclusions fail in general; infinite-graph extensions are not asserted. It provides no finite-time convergence rate, survivor probabilities or unique limiting shape. AI assistance and unrefereed status are explicit. Existing unresolved gaps are listed as limitations, not inflated into a newly proposed conjecture. Follow-up candidate:null.

Complete original abstract: abstract_original.txt and abstract_original.tex. Conditional explanatory copy: CONTENT_CANDIDATE.md. No public page was modified. Prior final Nevo scope and chip-firing editor evidence remained unchanged.

## Strongest verified result and remaining gap

The complete exact published edition and its45-file support archive are authenticated, fully mapped and unchanged; the full manuscript and necessary mathematical support were read; the original question and cited load-bearing interfaces are tied to fresh primary texts with precise finite/rate/initialization/probability/endpoint scope. This completes acquisition and editorial scope only.

Independent analytic and adversarial reviewers still own the correctness decision: the universal cycle estimate, all whisker scalar deductions and the stochastic/initialization interface must be validated and controls replayed as appropriate. There is no mathematical PASS, proof repair, journal-readiness verdict, priority certificate or publication permission in this report.
''')

# Reauthenticate actual sources, independently of the prior extraction's result.
checks=[]
for a in receipt['files']:
 b=(SRC/a['name']).read_bytes()
 assert len(b)==a['bytes'] and hashlib.md5(b).hexdigest()==a['md5'] and hashlib.sha256(b).hexdigest()==a['sha256']
 checks.append({'name':a['name'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'matches_receipt':True})
members=[];magicpdf=[];nested=[]
for ar in receipt['archives']:
 with zipfile.ZipFile(SRC/ar['name']) as z:
  for m in ar['members']:
   p=SRC/'published-source'/m['member'];b=p.read_bytes()
   assert b==z.read(m['member']) and len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
   members.append(m['member'])
   if b'%PDF-' in b[:1024]:magicpdf.append(m['member'])
   if zipfile.is_zipfile(p) or b.startswith((b'\x1f\x8b',b'7z\xbc\xaf\x27\x1c',b'Rar!')) or (len(b)>262 and b[257:262]==b'ustar'):nested.append(m['member'])
assert len(members)==45 and not nested and magicpdf==['output/pdf/finite-warm-thresholds.pdf']
assert digest(SRC/'record.json')['sha256']==receipt['record_sha256']
writej('final_integrity_check.json',{'checked_utc':now,'public_assets':checks,'record_unchanged':True,'zip_extracted_members_compared_byte_for_byte':45,'all_unchanged':True,'pdf_magic_members':magicpdf,'nested_archives':nested,'submitted_checker_executions':0,'scientific_verdict':None})
with (ROOT/'RESEARCH_LOG.md').open('a') as f:
 f.write(f'\n## {now} — 100%\nScope complete. Full exact abstract, source-bound report, precise claim/limitation map and conditional explanatory copy saved. Four primary interfaces authenticated; all45 source members and both public assets rechecked unchanged. No extra reader or nested archive found. Independent mathematical review remains separate; no mathematical PASS, proof repair, new follow-up, publication or external communication. Prior final effort evidence unchanged.\n')
freeze={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_percent':100,'mathematical_verdict':None,'files':{str(p.relative_to(ROOT)):digest(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and 'cache' not in p.relative_to(ROOT).parts and p.name!='SCOPE_FREEZE.json' and '__pycache__' not in p.relative_to(ROOT).parts}}
writej('SCOPE_FREEZE.json',freeze)
print(json.dumps({'status':'SCOPE_COMPLETE','mathematical_verdict':None,'abstract_words':len(plain.split()),'frozen_artifacts':len(freeze['files']),'source_members_unchanged':len(members)},indent=2))
