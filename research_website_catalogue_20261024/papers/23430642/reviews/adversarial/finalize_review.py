from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23430642');R=P/'reviews/adversarial';S=P/'sources';t=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((S/'receipt.json').read_text());files=[]
for e in receipt['files']:
 b=(S/e['name']).read_bytes();z={'path':'sources/'+e['name'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'md5':hashlib.md5(b).hexdigest()};assert z['sha256']==e['sha256'] and z['bytes']==e['bytes'] and z['md5']==e['md5'];files.append(z)
for e in receipt['archives'][0]['members']:
 p=S/e['path'];assert p.stat().st_size==e['bytes'] and sha(p)==e['sha256']
(R/'final_source_verification.json').write_text(json.dumps({'verified_utc':t,'completion_percent':100,'status':'UNCHANGED_MATCH','files':files,'all_538_extracted_regular_files_rehashed':True,'receipt_sha256':sha(S/'receipt.json'),'record_sha256':sha(S/'record.json'),'original_sources_mutated':False},indent=2)+'\n')
for a,b in [('flow_source_01/CHECKS_NORMAL.json','published_flow_replay.json'),('game_certificate_01/EXACT_RESULTS.json','published_game_replay.json')]:shutil.copyfile(R/'cache/published-replay'/a,R/b)
f=json.loads((R/'published_flow_replay.json').read_text());g=json.loads((R/'published_game_replay.json').read_text());fresh=json.loads((R/'fresh_results.json').read_text());bound=json.loads((R/'boundary_results.json').read_text())
rep={'completed_utc':t,'completion_percent':100,'execution':'Unmodified standalone helper copies; normal Python mode; exit code 0 for each. No historical wrapper or report replay.','flow':{'helper_sha256':f['checker_sha256'],'cases':len(f['checks']),'augmentations':sum(z['iterations'] for z in f['checks']),'cycles':sum(z['simple_cycles_checked'] for z in f['checks']),'all_original_choice_searches':len(f['all_original_tie_execution_checks']),'negative_controls':f['negative_controls'],'result_file':'published_flow_replay.json'},'game':{'helper_sha256':g['source_code_sha256'],'complete_games':len(g['whole_games']),'auxiliary_pairs':sum(z['exact_auxiliary_optimum_checks'] for z in g['whole_games']),'certificate_controls':g['certificates'],'toy_penalty':g['toy_penalty'],'result_file':'published_game_replay.json'},'limits':'No full-package wrapper execution, no optimized-mode replay, no historical claim acceptance. Finite helpers do not prove universal source behavior or enumerate every equilibrium.'}
(R/'published_replay_summary.json').write_text(json.dumps(rep,indent=2)+'\n')
prim_scopes={
'disser-skutella-journal.pdf':'Journal pp.5:6–5:10, Section2 assumptions/Proposition2.1, complete Lemmas3.1–3.2 and Figures1–3 context; Figure1 visually inspected. Corollary1.7 statement checked. Printed first-level second-path constant and delta envelope checked against actual arc costs.',
'adsul-journal-nsf.pdf':'Journal rank reduction Section3, Lemmas3–5 and Theorem1, with exact best-response transformation and rank-one specialization; printed pp.615–616.',
'adsul-arxiv-v4.pdf':'Rank-reduction Theorem7 and equations8–12, including zero-sum specialization; this confirms the edition numbering distinction from journal Theorem1.',
'erickson-fox-lkhamsuren.pdf':'Section3 Lemma3.3 complete proof and Theorem3.4 statement, explicit real capacities/demands. Used for the claimed precedent, not imported as the proof of the manuscript-specific ternary perturbation.',
'gilboa-zemel-alternate.pdf':'Section3.13 complete membership argument, directly compared with the present closed support-product proof and rational vertex witnesses.',
'nash1951.pdf':'Equilibrium definitions, support best-response criterion and Theorem1 existence proof through its completion, printed pp.287–289.'}
primary=[]
for e in json.loads((P/'reviews/scope/primary_source_receipts.json').read_text()):
 if e['name'] in prim_scopes and e.get('status')=='saved':
  assert sha(Path(e['path']))==e['sha256'];primary.append({**e,'read_scope':prim_scopes[e['name']],'hash_reverified':True})
(R/'primary_sources.json').write_text(json.dumps({'completed_utc':t,'completion_percent':100,'sources':primary,'boundary':'Raw publications and acquisition receipts only were read from the scope folder. Scope/analytic/adversarial sibling findings were not read. No exhaustive novelty search or worldwide priority assertion.'},indent=2)+'\n')
review=f'''# Independent adversarial review — Zenodo 23430642

Completed {t}; assigned review 100%.

**Verdict: SUPPORTED AT THE STATED SCOPE.** No substantive defect was found in the nine-page published argument, the necessary primary interfaces, independently reconstructed exact controls, or fresh replay of the two supplied mathematical helpers. This is a mathematical review with explicit limits, not conventional human peer review or formal proof-assistant certification. It makes no worldwide novelty or priority determination.

## Bound inputs and coverage

The selected manuscript is `paper.pdf`, 9 pages, printed **13 October 2026, Version 1.0**, DOI [10.5281/zenodo.23430642](https://zenodo.org/records/23430642). Its SHA-256 is `3ba83c50a4a2369a70897ee165a43f56324aa31574cf9c199e664174cbce0449`. The complete published `supportkit-v1.0.tar.gz` has SHA-256 `cd20964fe478365bd9c2db9b6cd8f6032aea0168073e7da21149865ec2f6d34c`. Both original assets were independently size/MD5/SHA-checked at intake and completion, and all 538 safely extracted regular files were rehashed twice. The original sources remain unchanged. The archive's embedded output PDF is the same edition as the main PDF, as established by the acquisition receipt.

All nine pages were read: the ordinary-language definitions and theorem (p.1), source gadget (pp.2–3), all-real-demand isolation (p.4), injective simplex and uniform exact penalty (pp.5–6), rank-one game and exhaustive crossings (pp.6–7), encoding and certificate membership (pp.7–8), and disclosure/references (p.9). The supplied 179-line flow helper and 243-line game helper were read completely **after** the independent controls and checkpoint. No historical prose report or full-package status wrapper was used.

`DERIVATION.md` gives the complete independent argument and attacks; `fresh_controls.py` and `boundary_controls.py` are new standalone exact-arithmetic artifacts. Their results are recorded separately from the reproduced supplied checks. No source repairs were made.

## Exact claim assessed

For explicitly listed rational games of variable positive dimensions with **rank(A+B)=1 exactly**, deciding whether there is exactly one mixed-strategy **pair** is coNP-complete and deciding whether there are at least two is NP-complete. Arbitrary degeneracy and equilibrium continua are allowed. The reduction supplies a known strict pure equilibrium; Partition has a solution if and only if there is an additional equilibrium. Both ordinary languages reject malformed/rank-invalid inputs.

The theorem is not a claim of strong NP hardness, fixed-dimension hardness, nondegenerate-promise hardness, payoff uniqueness, or difficulty finding one equilibrium. No result about all rational bimatrix games is substituted for the exact-rank-one reduction.

## Adversarial findings by dependency

| Dependency | Attack and outcome |
|---|---|
| Signed source counter | Checked actual journal arc formulas, source normalization, unit bottlenecks, both even/odd bridge comparisons and the synchronized companion step. The candidate's arithmetic corrections agree with the displayed gadget. Fresh tests include n=1, no/yes cases, repeated weights, five weights, and 81-bit integer weights. No off-by-one demand or cap failure found. |
| Universal shortest-path choices | The strict comparison/state argument addresses all choices, not only one tie rule. Exhaustive small reachable-state searches confirm this. Removing the base delta makes a yes instance admit a missed bridge event, a meaningful negative control. |
| Perturbation and real demand | Same-state original shortest comparisons are preserved; nonzero projected cycles cannot remain zero. Sign-conformal circulation decomposition proves uniqueness even for irrational demand. Interpolation optimality is established by residual path/cycle costs, not integer integrality. |
| Positive normalization | A topological potential changes only the fixed-demand objective constant, preserving events and uniqueness. Every shifted arc cost is positive; the DAG gives zero as the only demand-zero flow. |
| Simplex injectivity and retention | Explicit inverse coordinates are unique; the slack row creates no multiplicity. Every no-instance unrestricted optimum and the required yes midpoint remain feasible in the restricted LP. The proof does not need all yes optima to survive. |
| Uniform exact penalty | A fixed rational pointed dual has an optimal vertex for each real parameter. Cramer bounds are independent of that parameter and remain valid with redundant constraints/lower-dimensional faces. M>C strictly excludes every infeasible minimizer. Numerical size does not imply exponential encoding size. |
| Exact rank one and scalar correspondence | Opposite parameter constraints make b nonzero and a_0 is nonzero. Both best-response sets agree at lambda=a^T x, including zero probabilities and all opposing optima. Fresh exact full-game matrices and payoff inequalities agree. |
| Negative/zero/boundary parameter cases | Negative parameters have unique row zero, consistency at −epsilon, and one strict diagnostic column. Lambda=0 admits only zero flow and no crossing. Every remaining candidate is inside the penalty-valid interval; a yes midpoint lies strictly below its top boundary. |
| No-case full-pair exhaustion | Every nonnegative candidate requires f_e=1/2, excluded for every no-instance optimum. The sole negative pair is strict for both players. No hidden column degeneracy survives in the no case. |
| Degenerate membership witnesses | Closed support-product cells add no false equilibria, cover all equilibria and have polynomial-bit rational vertices. A nonsingleton union must contain two distinct vertex pairs. Tests include rank-one continua and one-player-single-action boundaries. |
| Ordinary languages and bit complexity | Rank-invalid/malformed inputs are handled in the complement branch; the reduction outputs valid rank-one games. It constructs only polynomial-sized rational matrices and never executes its exponentially long SSP curve. |

No examined dependency was left as an unsupported claim equivalent to the main theorem. The actual universal reasoning is in `DERIVATION.md`; computation alone is not treated as a proof of these rows.

## Fresh independent controls

The initial reconstruction used only the current manuscript and primary publications; no supplied helper was imported or read. `independence_checkpoint.json` fixes that checkpoint.

- **14 source instances**, **280** unit augmentations and **840** fractional-demand controls at one-third, one-half and two-thirds of each segment. Exact residual reduced-cost certificates check optimality; capacity/conservation, original-shortest comparison preservation and complete bridge event locations are checked.
- **6 complete rank-one games**, with M reaching **7,560 binary bits**, **48** exact primal/dual auxiliary equilibrium pairs, and **12** explicitly verified additional Nash pairs. Matrices are rebuilt from the manuscript, and both players' inequalities are checked exactly.
- **12 exhaustive small original-shortest-choice searches**, including all one- and two-weight tuples over {{1,2,3}}. All terminal event flags agree with Partition.
- **300** rational boundary/grid strategy pairs check the complete best-response transformation, including zero supports. Moving the parameter away from a^T x changes the column response set in **140** of those pairs, confirming the scalar condition matters.
- Exact rank-one equilibrium continua are checked in dimensions 1x2, 2x1, 2x2 and 3x4. The zero-penalty control exhibits an infeasible origin of cost zero at demand one while a feasible flow costs 539/30 and every nonzero feasible flow has positive shifted cost.

The flow/game artifact records 112,577 individual assertions, many repeated residual feasibility inequalities; the boundary artifact records 677. These are finite check totals, not distinct theorems or an exhaustive equilibrium enumeration.

A first local harness execution failed because integer zero dual entries divided by M became floating-point zeros, causing conversion overflow when multiplied by huge rationals. Converting every dual entry explicitly to Fraction fixed this local harness error before any passing result was reported. No manuscript or published helper was changed. The final tests use exact integer/rational arithmetic only.

## Supplied mathematical helper replay

After the independent checkpoint, the two standalone helpers were copied byte-for-byte to ignored isolated directories and run in normal Python mode. Their source hashes are bound by `published_helper_bindings.json`; originals were not executed in place because the helpers write result files next to themselves.

Fresh execution reproduced **37 flow instances, 660 augmentations, 864 residual-cycle checks and 6 exhaustive original-choice searches**. Its four deliberate negative controls passed. The game helper freshly reconstructed **6 games** and **204 exact auxiliary pairs**, plus strict default checks, wrong-sign/default/invalid-certificate controls, degenerate continua and an exact penalty-threshold toy example.

These are outputs of the current executions, retained as `published_flow_replay.json` and `published_game_replay.json`; no archived results were adopted. Normal-mode game assertions were active. The full archive wrapper and optimized-mode replay were not run, and no such coverage is claimed. The standalone helpers do not exhaust all games, demands, source instances or equilibria; the universal claims rely on the proof.

## Direct primary interfaces

Raw primary files obtained by the scope agent were independently hash-checked; acquisition logistics alone were shared. `primary_sources.json` records URLs, SHA-256 values and exact reading scope.

- [Disser–Skutella, journal body](https://www2.mathematik.tu-darmstadt.de/~disser/pdfs/DisserSkutella18.pdf): Section2 normalization and Proposition2.1, complete Lemmas3.1–3.2, Figures1–3 context, and Corollary1.7. Figure1's edge labels were visually checked. The arithmetic clarifications correspond to the actual displayed edges; the exact SODA edition is not needed as a separate imported theorem.
- [Adsul et al., published article](https://par.nsf.gov/servlets/purl/10317978): Section3 rank reduction and complete best-response correspondence, journal Theorem1. [arXiv v4](https://arxiv.org/abs/1812.04611v4) Theorem7 and equations8–12 independently confirm the numbering and specialization. The manuscript also proves its needed instance directly.
- [Erickson–Fox–Lkhamsuren](https://ekfox.web.illinois.edu/publications/holiest/holiest.pdf): Lemma3.3 proof and Theorem3.4 confirm that uniqueness for real capacities/demands has precedent. The candidate's simpler ternary scheme is checked on its own cycle argument; it is not justified by silently importing this surface-graph theorem to arbitrary graphs.
- [Gilboa–Zemel](https://itzhakgilboa.weebly.com/uploads/8/3/6/3/8363317/gilboa_zemel_nash_complexity.pdf): Section3.13 directly supplies the established rational-support certificate idea. The candidate's explicit closed-cell bounds were reconstructed rather than assuming irrational initial equilibria are themselves short witnesses.
- [Nash (1951)](https://irving.vassar.edu/faculty/gj/FTU/io/literature/Nash51.pdf): equilibrium/support definitions and Theorem1 existence proof were read through completion. This justifies complementing uniqueness/nonuniqueness on valid finite games.

LP duality, pointed polyhedral faces and determinant estimates are standard ingredients reconstructed explicitly here. This review does not claim to have read every bibliography entry, every historical version, or priority-audit document. The paper's stated novelty gaps remain novelty gaps rather than missing hypotheses of the reduction.

## Independence and incidental status exposure

No current sibling review finding, historical dedicated verdict/report, status file, acceptance file or audit prose body was read. Acquisition manifests exposed historical filenames and hashes only. The current paper's p.9 necessarily exposes its authored historical check counts and AI-review disclosure; the supplied helper docstrings claim earlier independent authorship. Those assertions were not adopted as validation. Fresh helper output after execution is evidence of that execution, not authority over the universal proof.

The authored archive contains many historical and review files; they were rehashed for byte integrity but their opinion bodies remained opaque. Only the two mathematical checker source files were inspected and replayed after independent evidence existed.

No site, promotion, spreadsheet, Git, deployment, Zenodo or external communication action was taken. The review recommends no repair because no substantive defect was found. Publication disposition belongs to the parent after all independent gates.
'''
(R/'REVIEW.md').write_text(review)
verdict={'record_id':'23430642','review_type':'independent_adversarial_mathematical','completed_utc':t,'completion_percent':100,'status':'SUPPORTED_AT_STATED_SCOPE','substantive_defects':[],'main_claim':'coNP-completeness of exact equilibrium-pair uniqueness and NP-completeness of nonuniqueness for explicitly listed rational exact-rank-one bimatrix games of variable positive dimensions, arbitrary degeneracy allowed, with a supplied strict pure default equilibrium in the reduction.','source_binding':{'pdf_sha256':files[0]['sha256'],'support_sha256':files[1]['sha256'],'all_nine_pages_read':True,'all_538_extracted_members_unchanged':True},'fresh_controls':fresh['counts'],'additional_boundary_controls':{'assertions':bound['assertions'],'strategy_pairs':bound['scalar_correspondence_pairs'],'wrong_parameter_detections':bound['wrong_parameter_negative_control_detections']},'published_replay':rep,'proof_coverage':['signed counter and all-choice source event','real-demand isolation and interpolation','positive potential transformation','injective simplex and retention','uniform all-minimizer exact penalty','exact rank one and all best-response correspondence','strict negative default and complete crossing exhaustion','polynomial binary encoding','rational two-pair certificates and ordinary-language complement handling'],'independence':'Fresh reconstruction and controls checkpointed before supplied helper reading; no sibling or historical dedicated opinion bodies read. Required manuscript/helper incidental statuses disclosed.','remaining_limitations':['Finite computations do not replace universal proof.','No exhaustive priority/novelty certification.','No human peer review or formal proof-assistant validation.','Full archive wrapper and optimized-mode helper execution not performed.'],'artifacts':['REVIEW.md','DERIVATION.md','fresh_controls.py','fresh_results.json','boundary_controls.py','boundary_results.json','published_flow_replay.json','published_game_replay.json','primary_sources.json','final_source_verification.json']}
(R/'verdict.json').write_text(json.dumps(verdict,indent=2)+'\n')
with (R/'RESEARCH_LOG.md').open('a') as f:f.write(f'\n## {t} — 100%\n\nIndependent adversarial conclusion: supported at exact stated scope; no substantive defect identified. Complete derivation covers source event, all-real-demand isolation, injective simplex, uniform all-minimizer penalty, exact-rank-one correspondence, strict default/full-pair exhaustion, encoding and degenerate rational witness membership. Boundary controls and unmodified supplied standalone flow/game helper replays passed in normal Python mode. Primary interfaces and source hashes independently checked. Full original PDF/archive plus every extracted member rehashed unchanged. Final REVIEW, DERIVATION, verdict, fresh/replay results, bindings and evidence saved. No sibling or historical opinion bodies consulted; no repair or external/site/Git/sheet/publishing changes.\n')
names=['REVIEW.md','DERIVATION.md','verdict.json','RESEARCH_LOG.md','source_integrity.json','final_source_verification.json','fresh_controls.py','fresh_results.json','boundary_controls.py','boundary_results.json','independence_checkpoint.json','published_helper_bindings.json','published_flow_replay.json','published_game_replay.json','published_replay_summary.json','primary_sources.json','published-paper.txt']
(R/'evidence_manifest.json').write_text(json.dumps({'created_utc':t,'completion_percent':100,'files':[{'path':str((R/n).relative_to(P)),'bytes':(R/n).stat().st_size,'sha256':sha(R/n)} for n in names],'note':'No self-hash. Original source receipt binds all published/extracted members; final_source_verification confirms unchanged bytes.'},indent=2)+'\n')
print(json.dumps({'completed_utc':t,'status':'SUPPORTED_AT_STATED_SCOPE','review_sha256':sha(R/'REVIEW.md'),'derivation_sha256':sha(R/'DERIVATION.md'),'verdict_sha256':sha(R/'verdict.json')},indent=2))
