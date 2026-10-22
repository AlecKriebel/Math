import json, pathlib, hashlib, datetime, collections
program=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(__file__).resolve().parent
captured=json.loads((program/'PR_OUTCOME_METADATA.json').read_text())['data']['repository']
latest=json.loads((root/'latest_metadata_comments_reviews.json').read_text())['data']['repository']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
# This table is a human reading of the complete PR bodies and the captured
# outcome/acceptance/README artifacts, not a mathematical or priority audit.
rows={
1251:('skip_partial','Universal triangle conjecture explicitly remains unresolved; only a triangle rectangle is covered.','The universal triangle conjecture remains unresolved by this work'),
1252:('skip_partial','General complete-host score-vector recognition explicitly remains unresolved.','General complete-host 3–1–0 recognition remains unresolved by this work'),
1253:('skip_prior_result','Explicit established-theorem coverage credited to Bagchi and Datta–Murai.','No new classification theorem is claimed.'),
1254:('skip_partial','All-knots full-signature question explicitly remains unresolved.','The all-knots full-signature approximation question remains unresolved by this work.'),
1255:('skip_partial','Exact all-n degree recurrences and bundled original target explicitly remain unresolved.','bundled original target remain unresolved.'),
1256:('skip_partial','Prior asymptotic theorem and finite partials do not solve original all-n target.','Original all-n target unresolved by this work.'),
1257:('skip_partial','Historical intended category unresolved; acceptance explicitly denies original-target resolution.','No novel unrestricted historical resolution is claimed.'),
1258:('skip_prior_result','Acceptance identifies prior-result scope with a literal-normalization hold; no new restriction theorem or unrestricted resolution is claimed.','No novelty, priority, new restriction theorem or whole-paper acceptance is claimed.'),
1259:('skip_prior_result','Complete alternative proof explicitly credited to previously announced Schnieper proof.','This is a complete alternative proof of a previously'),
1260:('skip_prior_result','Explicit prior negative resolution credited to Dubouloz–Palka.','Fully credited to Dubouloz–Palka'),
1261:('eligible_full_solution','Explicit complete O(r^-2) theorem removes the source-matched logarithmic loss for normalized Lebesgue global-SOS densities; no explicit original-target prior-resolution outcome.','satisfies 0 <= H_r - min_K f <= C_{K,f}/r^2 for every integer r >= 1.'),
1262:('skip_prior_result','Sharp modular result explicitly presented as credited coverage/corollary of prior quantitative LLT.','This is a credited consequence of Sah–Sawhney'),
1263:('skip_prior_result','Explicit audit of Ferudun prior negative answer and credited stronger nine-vertex claim.','prior negative answer to Heinig'),
1264:('skip_partial','Original Eremenko problem explicitly unresolved; all-height conclusion remains conditional.','Eremenko\'s original Problem 2 remains UNRESOLVED.'),
1265:('skip_prior_result','Original inverse-square result is explicitly prior Ferudun theorem; exponent extension beyond prior range is not a new resolution of the original inverse-square problem.','proves the prior range `1 < s <= 2`, including inverse-square repulsion.'),
1266:('skip_partial','Nonsharp bounds only; requested sharp coefficient remains unresolved.','The sharp coefficient −1/2 remains unresolved.'),
1267:('skip_prior_result','Target partition theorem explicitly credited to published Görtz theorem.','The partition theorem is credited to Ulrich Görtz'),
1268:('eligible_full_solution','Explicit complete counterexample to Long Question 7.2 in printed scope, with no explicit prior original-target resolution.','The accepted mathematical outcome is a complete negative counterexample'),
1269:('skip_partial','Standard algebra-group subcase only; broader original classification unresolved.','The broader classification remains unresolved.'),
1270:('skip_prior_result','Explicit credited published KSV disproof.','are credited for the disproof and primitive family'),
1271:('eligible_full_solution','Explicit negative resolution at n=8 derived from published ingredients; no explicit statement that prior work had already resolved original gamma-filtration conjecture. Priority remains for later audit.','negative resolution of problem 30003042'),
1272:('skip_prior_result','Explicit established rational-density mechanism credited to Dales–Davie through inspected sources.','This is an established mechanism'),
1273:('skip_prior_result','Explicit exposition and audit of He–Tang existing result, excluding independent discovery.','This is an authored exposition and analytic audit of their existing result'),
1274:('eligible_full_solution','Explicit full negative answers under printed definitions; historical Volberg attribution remains primary-unverified, which belongs to priority audit.','Adds a self-contained negative answer to Hayman–Lingham Problem 7.72'),
1275:('skip_prior_result','Explicit audit of Ho existing theorem/counterexample, not new disproof.','Ho\'s existing Theorem 1.6'),
1276:('skip_prior_result','Explicit checked rederivation of Ferudun prior interval/square construction.','This is a checked rederivation of Alper Ferudun\'s prior'),
1277:('skip_prior_result','Explicit prior published KSV disproof.','## Prior published disproof'),
1278:('skip_partial','Bounded density result explicitly does not fully resolve Erdős 1110.','This is not a full resolution of Erdős Problem 1110'),
1279:('skip_prior_result','Explicit known positive resolution due to Šámal.','a known positive resolution due to Robert Šámal'),
1280:('eligible_full_solution','Full authored theorem removes prior outerness and aperiodicity restrictions; broader conclusion explicitly not attributed to source theorem.','The broader conclusion is established by the authored reductions'),
1281:('skip_prior_result','Original cubic dichotomy explicitly already stated by Viro; only independent genus-one verification claimed.','fundamental-group dichotomy was already stated by'),
1282:('skip_partial','Bounded-congestion baseline/model correction only; original problem explicitly unresolved.','The original problem remains unresolved.'),
1283:('eligible_full_solution','Explicit complete existence classification under printed axioms and separately stated meet-identity convention; no explicit prior original-target resolution.','Complete existence classification for Problem 30005434'),
1284:('skip_partial','Sufficient criterion only; no full combinatorial classification.','does not give a full combinatorial classification.'),
1285:('skip_partial','Bounded ranks/H2 result explicitly not a resolution of full original question.','No novelty, arbitrary-rank obstruction, all-degree obstruction, or resolution of the full original question is claimed.'),
1286:('skip_prior_result','Explicit established prior-literature resolution credited to PSW and GM.','The construction is established prior literature'),
1287:('skip_prior_result','Prior Aggarwal–Andritsch theorem already states target finiteness; proof reconstruction only.','Theorem 1.9, already states this result.'),
1288:('skip_partial','Accepted finite-group partial result; unrestricted AIM question explicitly not declared solved.','The unrestricted AIM problem is not declared solved.'),
1289:('skip_prior_result','Explicit standard rank-one example with Doty–Henke/Martin credit; geometric result credited to OWR/Achar–Sobaje.','a standard rank-one example.'),
1290:('skip_partial','Known unrestricted extension obstruction explicitly does not settle all original Problem E.','This does not settle all of Ollivier’s Problem E'),
1291:('skip_partial','Local real-dimension-two characterization only; full original problem explicitly unsolved.','This result does not resolve other unspecified interpretations or the unrestricted-dimensional problem.'),
1292:('skip_prior_result','Explicit Ghimire prior negative phenomenon.','This negative phenomenon is prior work of Santosh Ghimire'),
1293:('skip_partial','Explicit ACCEPT-BOUNDED; unrestricted source problem not resolved.','not a resolution of the unrestricted source problem.'),
1294:('skip_prior_result','Explicit Ferudun prior construction and theorem for original knot existence question.','The construction is credited to Alper Ferudun'),
1295:('skip_prior_result','Explicit existing Rabinoff/ABBR negative answer.','counterexample already given in Rabinoff'),
1296:('skip_prior_result','Explicit Ferudun prior smooth theorem/construction; literal original numerical alternative also has norm-form witnesses.','The theorem and construction are attributed to Alper Ferudun'),
1297:('skip_partial','Decomposable-module scope correction explicitly does not resolve intended absolutely-simple conjecture.','This does not resolve the intended absolutely-simple conjecture.'),
1298:('skip_partial','Dimension-two threshold only; all-dimensional result explicitly unclaimed.','## Accepted result: dimension two only'),
1299:('skip_partial','Normalization-dependent obstruction explicitly not unconditional historical refutation.','not an unconditional refutation of the historical conjecture'),
1300:('skip_partial','Literal boundary-index defect only; intended corrected higher-dimensional conjecture not settled.','This does not prove or refute the intended corrected higher-dimensional conjecture'),
}
def paragraph(text,needle):
 i=text.find(needle)
 if i<0: raise ValueError(needle)
 a=text.rfind('\n\n',0,i)+2
 b=text.find('\n\n',i)
 return text[a:len(text) if b<0 else b]
def sha256(data):return hashlib.sha256(data).hexdigest()
def file_evidence(folder):
 out=[]
 for receipt in sorted(folder.glob('*.receipt.json')):
  r=json.loads(receipt.read_text());data=(folder/r['name']).read_bytes()
  assert len(data)==r['size']
  assert sha256(data)==r['sha256']
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert blob==r['sha']
  out.append({'path':r['path'],'head_ref':r['ref'],'git_blob_sha':blob,'sha256':r['sha256'],'bytes':len(data),'capture':str((folder/r['name']).relative_to(program))})
 return out
records=[]
for n in range(1251,1301):
 p=captured['p'+str(n)];l=latest['p'+str(n)];folder=root/str(n)
 assert l['headRefOid']==p['headRefOid'] and l['body']==p['body']
 assert (folder/'PR_BODY.md').read_text()==p['body']
 assert l['comments']['totalCount']==len(l['comments']['nodes'])==0
 assert l['reviews']['totalCount']==len(l['reviews']['nodes'])==0
 assert not l['comments']['pageInfo']['hasNextPage'] and not l['reviews']['pageInfo']['hasNextPage']
 classification,reason,needle=rows[n]
 files=file_evidence(folder)
 evidence=[{'source':'PR body','exact_snippet':paragraph(p['body'],needle)}]
 for f in files:
  if f['path'].endswith('/README.md'):
   text=(program/f['capture']).read_text()
   paras=[z for z in text.split('\n\n') if z.strip() and not z.startswith('#')]
   evidence.append({'source':f['path'],'git_blob_sha':f['git_blob_sha'],'exact_snippet':'\n\n'.join(paras[:2])})
  elif 'ACCEPTANCE' in pathlib.Path(f['path']).name:
   text=(program/f['capture']).read_text()
   if f['path'].endswith('.json'):
    a=json.loads(text)
    selected={k:v for k,v in a.items() if any(z in k.lower() for z in ['verdict','decision','disposition','target_resolv','problem_solv','original_target','first_resolution','prior_announcement','prior_credit','accepted_result','original_cubic_status','claim_type'])}
    evidence.append({'source':f['path'],'git_blob_sha':f['git_blob_sha'],'exact_json_fields':selected})
   else:
    paragraphs=[z for z in text.split('\n\n') if z.strip() and not z.startswith('#')]
    evidence.append({'source':f['path'],'git_blob_sha':f['git_blob_sha'],'exact_snippet':'\n\n'.join(paragraphs[:2])})
 r={'pr':n,'url':p['url'],'title':p['title'],'problem_paths':sorted({str(pathlib.PurePosixPath(z['path']).parent) for z in p['files']['nodes']}),'captured_head_oid':p['headRefOid'],'latest_status':{k:l[k] for k in ['state','isDraft','headRefOid','updatedAt']},'latest_comments_count':0,'latest_reviews_count':0,'outcome_supersession_observed':False,'body_and_head_unchanged_at_refresh':True,'classification':classification,'reason':reason,'evidence':evidence,'captured_outcome_files':files,'named_outcome_files_absent_from_pr_diff':[name for name in ['ACCEPTANCE.json','README.md'] if not any(z['path'].endswith('/'+name) for z in p['files']['nodes'])],'full_body_read':True,'proof_or_priority_audit_performed':False,'mathematical_or_novelty_verdict':None}
 records.append(r)
counts=dict(collections.Counter(x['classification'] for x in records))
result={'schema':'actual-pr-outcome-eligibility-v1','reviewed_at_utc':now,'scope':{'repo':'AlecKriebel/Math','first_pr':1251,'last_pr':1300,'count':50},'basis':'Actual full PR bodies, immutable-head outcome/acceptance and README artifacts, and refreshed PR metadata/comments/reviews. QUEUE.md was not used as decisive evidence.','selection_rule':'An explicit complete solution or counterexample to the original target is eligible even when novelty is unconfirmed or only prior ingredients are credited. Explicit original-target prior/already-solved outcomes and incomplete/conditional/restricted-only outcomes are skipped.','counts':counts,'eligible_prs':[x['pr'] for x in records if x['classification']=='eligible_full_solution'],'needs_scope_resolution_prs':[],'review_limit':'Eligibility only. No proof correctness, empirical reproduction, literature priority, publication, merge, close, comment, or queue mutation was performed. Eligible means proceed to the authorized later review gates, not accepted mathematics.','checks':{'all_50_full_bodies_read':True,'all_50_heads_and_bodies_unchanged_at_refresh':True,'all_50_open_and_draft':all(x['latest_status']['state']=='OPEN' and x['latest_status']['isDraft'] for x in records),'all_comments_and_reviews_complete_empty':True,'all_captured_file_native_blob_and_sha256_checks_pass':True},'records':records}
(root/'gate_1251_1300.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
lines=['# Actual-outcome eligibility: PRs #1251–#1300','',f'Checkpoint: {now}. Eligibility classification 100% complete; mathematical review/publication completion 0% for the six selected candidates.','', 'All 50 complete PR bodies were read. Immutable-head acceptance/outcome and README files were captured where present, with alternate acceptance summaries for nonstandard packet layouts. Their Git blob SHA and SHA-256 identities were independently checked. Refreshed metadata confirms every PR remains OPEN and draft, with the same head and body, zero comments and zero reviews. No superseding outcome was found. QUEUE.md was not decisive.','',f"Eligible for later full review: {', '.join('#'+str(x) for x in result['eligible_prs'])}.",'',f"Skipped: {counts['skip_partial']} partial/conditional/restricted-only outcomes and {counts['skip_prior_result']} explicit credited-prior outcomes. No PRs require an unresolved eligibility classification.",'','The six selections are claims, not mathematical acceptance:','', '- #1261: complete O(r^-2) normalized Lebesgue global-SOS convex-body convergence theorem. The incomplete normalization in the historical display and distinction from original-objective pushforward densities must be checked during problem matching. It does not explicitly say the original target was previously solved.','- #1268: complete Long 7.2 counterexample over Q(sqrt(10)); source conventions for prime elements versus irreducibles and prime-ideal versus principal-ideal minima require the later source-matching audit.','- #1271: explicit literature-derived gamma-filtration refutation at n=8. Published ingredients are credited, but no explicit prior resolution of the original target is recorded. This is eligible for priority audit, including its unreplayed published computation dependency.','- #1274: complete Beurling-annihilator negative answers under printed definitions. Primary-unverified secondary Volberg attribution is a priority issue; it is not treated as an established prior-result outcome.','- #1280: full strong-approximate-innerness theorem with authored reductions removing prior outerness/aperiodicity restrictions. No approximate-representability or group-law claim is included.','- #1283: complete semibrace existence classification under printed axioms and the separate meet-identity convention. Existence is the claimed target; all multiplications are not classified.','', 'Special skip: #1265 explicitly credits the original inverse-square theorem to Ferudun; its further exponent extension is not a new original-target resolution. #1259 explicitly acknowledges the prior Schnieper proof announcement. The generic no-novelty disclaimers on the six eligible candidates did not cause exclusion.','', 'No excluded PR was mathematically audited or otherwise processed. No proof, PR, queue, shared index, or unrelated folder was changed; no Git commits were made.','', '## Per-PR classifications','', '| PR | Classification | Recorded reason |','| --- | --- | --- |']
lines.extend(f"| #{x['pr']} | {x['classification']} | {x['reason']} |" for x in records)
(root/'REPORT.md').write_text('\n'.join(lines)+'\n')
(root/'RESEARCH_LOG.md').write_text(f'''# Eligibility research log\n\n- {now}: Completed actual-outcome gate for all PRs #1251–#1300. Read every full PR body; retrieved immutable-head acceptance/outcome and README artifacts where present, plus alternate outcome summaries; refreshed status/comments/reviews; independently validated native Git blob and SHA-256 identities. Eligibility completion estimate: 100%. Mathematical review/publication completion estimate for selected candidates: 0%.\n- Strongest verified result: six PRs explicitly claim complete original-target resolutions without an explicit established-prior original-target outcome: #1261, #1268, #1271, #1274, #1280, #1283. This verifies recorded claims only. It does not verify the mathematics, priority, or preprint readiness.\n- Exact remaining gap: apply the user's full problem-matching, mathematical reproduction/adversarial review, priority audit, preprint/review loop, and authorized publication process to eligible candidates. No excluded PR is authorized for those steps.\n- No mathematical or literature audit of excluded PRs, no PR changes, no queue edits, no commits, no external-person communication.\n''')
print(json.dumps({'counts':counts,'eligible':result['eligible_prs'],'captured_files':sum(len(x['captured_outcome_files']) for x in records),'output':str(root/'gate_1251_1300.json')},indent=2))
