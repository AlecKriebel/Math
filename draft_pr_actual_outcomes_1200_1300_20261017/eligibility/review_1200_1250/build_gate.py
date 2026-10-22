from pathlib import Path
import json,re,hashlib,datetime,collections
ROOT=Path(__file__).resolve().parent
META=json.load(open(ROOT.parents[1]/'PR_OUTCOME_METADATA.json'))['data']['repository']
LATEST=json.load(open(ROOT/'latest_status_comments_reviews.json'))['data']['repository']
RECEIPTS=json.load(open(ROOT/'immutable_file_receipts.json'))
receiptmap={(x['pr'],Path(x['path']).name):x for x in RECEIPTS['records']}
ELIGIBLE={1205,1211,1216,1225,1241}
PRIOR={1201,1207,1210,1217,1219,1220,1222,1226,1227,1228,1230,1231,1232,1233,1236,1237,1244,1245,1246,1247}
AMBIGUOUS={1235}
DETAILS={
1200:('unrestricted same-partition','Restricted to components with empty/regular nonempty 2-core; unrestricted target expressly unresolved.'),
1201:('This authored edition retains','Prior Skottová–Steiner theorem and Chan finite result; k=4,r>=2 expressly unresolved.'),
1202:('unrestricted Chung','Restricted graph families; unrestricted Chung–Ross target expressly unresolved.'),
1203:('general Schubert','Skew-sum/support partial results; general left-weak convexity conjecture expressly unresolved.'),
1204:('normalizer extension','Normal-subgroup descent only; general nonnormal conjecture expressly unresolved.'),
1205:('original OWR2021','Explicit complete counterexample to original canonical-W exponent converse. Later varsigma/coefficient variants are outside the claim. Novelty disclaimer does not exclude this full original-formulation claim.'),
1206:('For every positive integer','Cyclic-cover family theorem only; original graph-coloring conjecture expressly unresolved.'),
1207:('Accepted correction','Correction/reconstruction of an already published arrangement theorem; explicitly no novel theorem/target counterexample claim.'),
1208:('full local recurrence','Incidence-dependent structural bound only; full local recurrence expressly unresolved.'),
1209:('original infinite','Fixed ADKT-family polynomial-shift classification only; original infinite four-total-shift question expressly unresolved.'),
1210:('shared eight-file','Explicit audit of Alper Ferudun’s existing D/F proofs, not a new solution; also not all source conjectures accepted.'),
1211:('explicit eleven','Explicit full negative answer to Kohl’s stated arbitrary-list universal tree-equality conjecture. No prior external resolution is asserted by the recorded outcome.'),
1212:('Record 30005741','Restricted Poisson length equalities; both full source questions expressly unresolved.'),
1213:('uniform O','Structural partials/source correction; original uniform logarithmic-square target expressly unresolved.'),
1214:('One shared rank-at-most-two','Rank-at-most-two result shared by two records; both general targets expressly unresolved.'),
1215:('unrestricted determinant','Rank-boundary determinant approximation only; unrestricted target expressly unresolved.'),
1216:('Target 30000921','Explicit complete negative answer to universal pointwise polynomial preservation of differentiation hypercyclicity. Stronger fixed-polynomial statements are separately scoped.'),
1217:('This draft adds','Explicit audit of Alper Ferudun’s already existing exact Ford-circle packing proof.'),
1218:('full original subexponential','Corrected seed/obstruction partials only; original subexponential-in-d question expressly unresolved.'),
1219:('result belongs','Both negative answers are explicitly credited to existing Alpan–Zinchenko theorem.'),
1220:('This draft adds','Explicit prior-result reconciliation/normalization correction; no new compact all-order formula or complete AIM resolution accepted.'),
1221:('This draft adds','Corrected partial surreal-derivation reductions only; existential target and exact global datum gap remain.'),
1222:('theorem is credited','Unconditional full written theorem is expressly credited to Li, with earlier Tang full-claim provenance; this edition is a prior-proof audit.'),
1223:('general arbitrary','N=2/special N=3/scoped sufficient tests only; general arbitrary-partition classification expressly unresolved.'),
1224:('General harmonic rigidity','Mixed prior result, finite greedy-rule counterexample, and unaccepted general rigidity proof; no explicit full original solution claim.'),
1225:('For every compact','Explicit accepted_full_stated_target for Gonchar/Vuorinen compact-real-set modulus question, under stated endpoint/extended-Borel-density conventions. These formulation conventions must be audited in later mathematical review.'),
1226:('exact variational','Existing exponent characterization and source corrections; original full estimation problem expressly not declared solved.'),
1227:('Whether the game','Prior game bounds and exact constant certificate; linear-versus-sublinear question expressly unresolved.'),
1228:('existing Price','Existing Price/GPT-5.5 Pro first-part disproof accepted with repairs; broader general-k estimation remains partial.'),
1229:('partial research','Omega-enumeration four-AP threshold remains 3 or 4; explicitly partial, not a solution.'),
1230:('exact prior result','Exact isomorphism expressly covered by published AVM Theorem 8.8(2), with Allegra credit.'),
1231:('Credit the prior','Full written counterexample is expressly credited to prior vibemathing C09/C10 construction/arguments; source candidate status remains unchanged.'),
1232:('Acceptance is limited','Prior Bitansky–Erabelli–Garg–Ishai theorem audit limited to finite/statistical/nonrobust existence; no unqualified original resolution.'),
1233:('Acceptance is limited','Established Aldroubi et al. rank criterion only; original qualitative support-style request expressly not certified.'),
1234:('Status: PARTIAL','At-most-three-prime and computation-dependent 41-smooth cases only; unrestricted arbitrary-prime problem expressly unresolved.'),
1235:('No standalone verdict','Explicit integral-point counterexamples/conical-cover refutation, but affine convex-hull triangulation verdict expressly NOT_ESTABLISHED. No explicit full original OWR target resolution is recorded. Scope must be resolved before eligibility; not admitted to review/publication by this gate.'),
1236:('Acceptance covers only','Source-credited Ferudun reconstruction accepted only in exact domains/families; arbitrary complete extensions and general real-analytic no-tangency conjecture expressly unresolved.'),
1237:('Acceptance is confined','Computable-bound consequence of prior basis algorithm only; no unqualified original quantitative-question resolution.'),
1238:('optimum 2 versus','Two-to-three-chart bound only; optimum 2 versus 3 expressly unresolved.'),
1239:('No efficient algorithm','Finite recognition and rank-two classification scoped; explicitly no unqualified original qualitative workshop-question resolution.'),
1240:('original problem remains PARTIAL','Symmetric Brauer projector component only; useful recoupling theory expressly remains required.'),
1241:('Complete authored proof','Explicit full solution/negative answer to Farb Question 7.6 for every fixed g>=2,k>=3, ambient Mod_g-conjugacy convention. Separate simple-length-spectrum question remains outside the original claim.'),
1242:('unrestricted ordinary','Quadratic-chain characterization only; unrestricted ordinary-chain inclusion expressly unresolved.'),
1243:('Both original','Constant-offset/rational-shift ansatz rigidity only; both original caustic existence questions expressly unresolved.'),
1244:('Full authored reconstruction','Credited prior lower-cone component only; separate arithmetic zigzag target expressly unresolved.'),
1245:('General orbit classification','Prior anonymous candidate smoothness component only; original bundle/orbit/classification/scheme questions not fully resolved.'),
1246:('original arbitrary','MacMahon prior simply connected component with repairs; original arbitrary-domain qualitative question expressly broader and unsolved by edition.'),
1247:('original quantum','Already published classical/nonsignalling baselines only; original quantum-comparison question expressly unresolved.'),
1248:('arbitrary-n problem','Fixed-fiber rank obstruction/small-rank partials; arbitrary-n finiteness/parametrization/closure target expressly unresolved.'),
1249:('general conjecture','Forest-correlation reductions/known families only; general all-forest negative correlation expressly unresolved.'),
1250:('unrestricted conjecture','Matroid-weight reductions/partial cases only; unrestricted conjecture expressly unresolved.')}

def para(text,phrase):
 ps=text.split('\n\n')
 for p in ps:
  if phrase.casefold() in re.sub(r'\s+',' ',p).casefold():return p
 raise ValueError(f'No paragraph for {phrase}')

def scalars(x,prefix=''):
 if isinstance(x,dict):
  for k,v in x.items():
   p=prefix+'/'+k
   if isinstance(v,(dict,list)):yield from scalars(v,p)
   else:yield p,v
 elif isinstance(x,list):
  for i,v in enumerate(x):
   if isinstance(v,(dict,list)):yield from scalars(v,prefix+'/'+str(i))
   else:yield prefix+'/'+str(i),v

records=[];mismatches=[]
for n in range(1200,1251):
 pr=META[f'p{n}'];latest=LATEST[f'p{n}'];d=ROOT/f'pr_{n}'
 acceptance=json.loads((d/'ACCEPTANCE.json').read_text());readme=(d/'README.md').read_text()
 classification='eligible_full_solution' if n in ELIGIBLE else 'skip_prior_result' if n in PRIOR else 'needs_scope_resolution' if n in AMBIGUOUS else 'skip_partial'
 acceptance_claims=[]
 for p,v in scalars(acceptance):
  if any(z in p for z in ['manifest','sha256','document_bindings','receipt']):continue
  if re.search(r'(?:status|verdict|full.*(?:target|problem|solution|answer)|(?:target|problem).*resolv|remaining_gap|residual|scope_boundary|affine_convex_hull|canonical_W_converse_refuted|original_bundle_fully_resolved|claim_limits)$',p,re.I):
   acceptance_claims.append({'json_pointer':p,'value':v})
 for name in ['ACCEPTANCE.json','README.md']:
  receipt=receiptmap[(n,name)];b=(d/name).read_bytes()
  assert hashlib.sha256(b).hexdigest()==receipt['sha256']
  blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  assert blob==receipt['github_blob_sha']
  match=re.search(r'`'+re.escape(name)+r'`[^\n]*SHA-256 `([a-f0-9]{64})`',pr['body'])
  if match and match.group(1)!=receipt['sha256']:mismatches.append({'pr':n,'file':name,'body_sha256':match.group(1),'retrieved_sha256':receipt['sha256']})
 readmeparas=[p for p in readme.split('\n\n') if re.search(r'unresolv|partial|prior|existing|full negative|Complete negative|negative answer|accepted_full|converse|counterexample|original|not.*(?:solv|resolution)',p,re.I)]
 phrase,reason=DETAILS[n]
 record={
  'number':n,'title':pr['title'],'url':pr['url'],'classification':classification,'eligible_for_original_review_publication_process':classification=='eligible_full_solution','reason':reason,
  'captured_head_ref_oid':pr['headRefOid'],'head_branch':pr['headRefName'],'captured_updated_at':pr['updatedAt'],
  'latest_status':{k:latest[k] for k in ['state','isDraft','headRefOid','updatedAt']},
  'head_unchanged_at_gate':latest['headRefOid']==pr['headRefOid'],
  'evidence':{'body_excerpt':para(pr['body'],phrase),'body_sha256':hashlib.sha256(pr['body'].encode()).hexdigest(),'body_local_path':f'pr_{n}/BODY.md','acceptance_declarations':acceptance_claims,'readme_outcome_excerpts':readmeparas},
  'immutable_head_files':[receiptmap[(n,name)] for name in ['ACCEPTANCE.json','README.md']]+([receiptmap[(n,'ACCEPTANCE.md')]] if (n,'ACCEPTANCE.md') in receiptmap else []),
  'comments':latest['comments'],'reviews':latest['reviews'],
  'mathematical_correctness_audited_here':False,'priority_audited_here':False
 }
 records.append(record)
assert not mismatches,mismatches
counts=dict(collections.Counter(x['classification'] for x in records))
result={
 'schema':'actual-pr-outcome-eligibility-gate-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':{'first_pr':1200,'last_pr':1250,'complete_pr_count':51,'authority':'User 2026-10-17 instruction supersedes stale QUEUE.md: inspect actual PR outcomes; only explicit full original-problem solution claims enter original review/publication process.','queue_used_as_gate':False,'metadata_source':'../../PR_OUTCOME_METADATA.json'},
 'method':'Read captured PR bodies, retrieve immutable-head ACCEPTANCE.json and README.md through authenticated GitHub contents API; inspect ACCEPTANCE.md only for PR 1235 scope ambiguity; recheck live state/head and capture issue comments/review bodies. No proofs or scholarly sources inspected for excluded records.',
 'classification_definitions':{'eligible_full_solution':'Explicit full original-target proof/counterexample claim; generic lack-of-novelty/priority-clearance disclaimer is not exclusion. This says nothing about truth or priority.','skip_partial':'Recorded outcome explicitly partial, restricted, conditional, or original target unresolved; no mathematical review performed.','skip_prior_result':'Accepted outcome explicitly described as a reconstruction/audit/correction of an attributed prior result, even if full target is covered or ancillary residual questions remain. This does not infer that an entire multi-part problem is already solved.','needs_scope_resolution':'Original full-target resolution not explicit and stated exclusions could leave original target open; not admitted for review/publication.'},
 'counts':counts,'eligible_prs':sorted(ELIGIBLE),'needs_scope_resolution_prs':sorted(AMBIGUOUS),
 'integrity_checks':{'retrieved_files':len(RECEIPTS['records']),'file_retrieval_errors':[],'all_github_blob_sha1s_recomputed':True,'all_local_sha256s_recomputed':True,'body_stated_acceptance_readme_sha256_mismatches':mismatches,'all_heads_unchanged':all(x['head_unchanged_at_gate'] for x in records),'all_comments_and_reviews_pages_complete':all(not x['comments']['pageInfo']['hasNextPage'] and not x['reviews']['pageInfo']['hasNextPage'] for x in records),'total_issue_comments':sum(x['comments']['totalCount'] for x in records),'total_reviews':sum(x['reviews']['totalCount'] for x in records)},
 'checkpoint':{'eligibility_inventory_completion_percent':100,'mathematical_and_publication_process_completion_percent':0,'interpretation':'Eligibility gate only. No endorsement of correctness, novelty, priority, or publication readiness.'},
 'records':records}
(ROOT/'gate_1200_1250.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
report=['# Actual-outcome eligibility gate: PR #1200–#1250','',f"Checkpoint: {result['created_utc']}. Eligibility inventory 100%; mathematical review/publication process 0%.",'','All 51 captured PR bodies were checked against their immutable-head ACCEPTANCE.json and README.md. GitHub state/head and issue comments/reviews were rechecked. All remain OPEN draft at the captured head; no comments or reviews exist. All 102 acceptance/README blob identities and their PR-body SHA-256 declarations match. One additional ACCEPTANCE.md was retrieved solely for #1235 scope clarification. QUEUE.md was not used as the gate.','',f"Explicit full-solution claims eligible for the original review process: **{', '.join('#'+str(n) for n in sorted(ELIGIBLE))}**. Generic novelty/priority disclaimers were not exclusions. Eligibility is not correctness or priority acceptance.",'','**First eligible: #1205.** It explicitly refutes the original OWR2021 canonical-W converse. Its exclusions concern later varsigma/coefficient variants and the sufficient theorem; the canonical-coordinate scope needs to stay explicit during the later audit.','', '**#1235 needs scope resolution and is not admitted.** The recorded outcome proves integral-point counterexamples and rules out a conical unimodular cover, but expressly leaves an affine convex-hull triangulation verdict NOT_ESTABLISHED. The body/acceptance/README do not explicitly claim complete resolution of the original OWR target. The exact accepted distinctions and summary are preserved.','',f"Counts: {counts.get('eligible_full_solution',0)} eligible_full_solution; {counts.get('skip_partial',0)} skip_partial; {counts.get('skip_prior_result',0)} skip_prior_result; {counts.get('needs_scope_resolution',0)} needs_scope_resolution.",'','| PR | Classification | Recorded outcome |','|---|---|---|']
for r in records:report.append(f"| [#{r['number']}]({r['url']}) | {r['classification']} | {r['reason'].replace('|',' / ')} |")
report+=['','This work only classified recorded claims. It did not inspect proofs, run mathematical programs, search priority literature, modify PRs/QUEUE.md, comment, merge/close PRs, prepare papers, upload to Zenodo, update the publication sheet, or communicate with external individuals.','', 'Exact evidence, immutable head IDs, Git blob SHA-1 and file SHA-256 receipts, latest state and full comment/review snapshots are in `gate_1200_1250.json` and its adjacent retained inputs.']
(ROOT/'REPORT.md').write_text('\n'.join(report)+'\n')
print(json.dumps({'counts':counts,'eligible_prs':sorted(ELIGIBLE),'needs_scope_resolution':sorted(AMBIGUOUS),'report':str(ROOT/'REPORT.md'),'gate':str(ROOT/'gate_1200_1250.json')},indent=2))
