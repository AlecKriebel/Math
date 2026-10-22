from pathlib import Path
import json,datetime,hashlib
root=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1100_1200_20261017')
out=root/'gate_reviews/upper'
F='explicit_full_solution_claim';P='partial_or_unsolved';R='explicitly_prior_full_resolution'
raw='''1151|30003321||F|Every discrete initial ordered additive subgroup|Full affirmative resolution expressly claimed for the targeted discrete additive-group question. Generic novelty disclaimers do not attribute this resolution to prior work.
1152|30001214|OWR-3397-002|R|The essential existence theorem is prior work|The negative resolution expressly credits Bell–Launois–León Sánchez–Moosa; no new counterexample is claimed.
1153|30002950||P|The full single J-orbit assertion|Multiple-distinct-interior-slope single-orbit assertion explicitly remains unresolved.
1154|30001551|OWR-4425-006|P|Both bounded searches were reconstructed independently|Finite searches and erasing-witness reductions do not settle the exact target.
1155|30000214||F|The complete authored proof constructs a finite two-dimensional simplicial complex|An explicit negative answer to the unqualified homology-sphere-cover assertion is claimed. Characteristic-zero counterexamples suffice for this claimed negative answer.
1156|30003650||P|The combined two-question target is ACCEPT_AS_PARTIAL|Equality of maxima does not determine the second maximum-gap question in the combined target.
1157|102|GREEN-012|P|The stronger exact claim is F(r)|The high-density theorem and bounded-order cases leave the unrestricted target unresolved.
1158|30000879|OWR-1738-004|P|The original [Aljadeff problem source]|Splitting and dimension inequalities leave the exact conjecture unresolved in 2 <= r < n.
1159|1903|EP51|P|Repeated transport supplies no uniform control|Least-preimage divergence explicitly remains unresolved.
1160|1900013||P|The finite conductor quotient is a structural reduction|The arithmetic reduction leaves the full geometric classification unresolved.
1161|11000008|AMR-109-0008|P|In genus two, finitely generated witnesses|The genus-two list is not an upper classification and the full genus >=2 spectrum remains unresolved.
1162|1889|EP25|P|“Accepted” means the independent internal AI audit's stated partial scope|The finite affine-pattern theorem does not resolve the unrestricted singleton problem.
1163|1910|EP68|P|The result proves neither rationality nor irrationality|Reduced-denominator growth does not decide the series irrationality target.
1164|1954|EP143|P|The weighted-convergence question|The credited harmonic corollary does not supply weighted convergence or solve the two-part problem.
1165|20000970||P|remains unresolved by this work. Arbitrary large residual cores|The general efficient-sampling target remains unresolved; arbitrary cores have exponential fallback.
1166|1988|EP-197|P|For each prescribed nondecreasing unbounded|The bounded-deficit obstruction and dense construction do not decide the full two-set target.
1167|2000004|AMR-019-0004|P|No unqualified solution to Ball's connected-domain|The credited two-component CN result does not solve the original connected-domain boundary-only formulation.
1168|20000973||P|The precise scope is the minimum automorphism-equivariance requirement|The credited prior minimum-equivariance criterion is scoped; stronger original naturality is not established and no full original-problem solution is claimed.
1169|2066|EP-348|R|This is an AI-assisted, unrefereed audit of an existing arXiv preprint|The complete deletion-threshold classification is expressly a credited prior Geneson result.
1170|2009|EP252|R|k >= 0. Credit remains with the prior author.|The full irrationality argument is attributed to prior author Tokengrinder; the formal reproducibility hold does not create a new-solution claim.
1171|2041|EP312|P|assertion remain unresolved by this work.|The universal arbitrary-multiset exponential theorem and logarithmic-mass assertion remain unresolved.
1172|2020|EP-269|P|No fixed finite family of real polynomial corrections|The phase asymptotic and polynomial obstruction do not prove irrationality; arbitrary integer carries remain unresolved.
1173|2033|EP291|P|Neither fixed-set density nor pairwise independence settles full infinitude.|Fixed-prime control leaves growing-prime control and full coprimality infinitude unresolved.
1174|2071|EP-357|P|Here f(n) is the largest length|Credited partial bounds do not establish residual sublinearity.
1175|2037|EP302|P|No full resolution, convergence theorem, exact limiting density|Full resolution is expressly disclaimed; the lower improvement additionally has a verification hold.
1176|2070|EP354|P|it does not resolve the original fixed-base-2 question|The variable-base counterexample leaves the original fixed-base-two question unresolved.
1177|2083|EP377|P|reciprocal mass remains uncontrolled: sup_n f(n)<infinity is neither proved|The absolute bound is explicitly neither proved nor refuted.
1178|2087|EP385|P|natural density. Neither eventual positivity|Natural-density divergence does not establish eventual positivity or pointwise divergence.
1179|2112|EP423|P|The exact asymptotic, b_n=o(n), and even an O(n) upper bound|The plateau lower bound leaves the original exact asymptotic and upper estimates untouched.
1180|2104|EP413|P|Coefficient one remains unresolved.|The corrected credited logarithmic barrier does not resolve the original coefficient-one question.
1181|2129|EP-461|P|claim follows. A positive uniform lower coefficient remains unresolved.|The finite obstruction caps a possible coefficient but does not establish a positive uniform lower coefficient.
1182|2141|EP486|R|This is acceptance of an identified prior theorem|The arbitrary-residue counterexample expressly accepts the prior Wang theorem.
1183|2142|EP488|R|## Accepted prior full finite refutation|The original multiples inequality is refuted by an expressly credited prior complete proof of Declan Gessel.
1184|2166|EP538|R|This is an audit of a prior public claim|The full fixed-r matching-order result expressly credits the prior STARFLEET Math claim.
1185|2273|EP710|P|The fixed-start asymptotic question remains unresolved|The finite route obstruction does not resolve the fixed-start asymptotic target.
1186|2274|EP-711|P|The last lower bound and the known diagonal upper estimate imply|Credited interval-matching bounds leave the uniform exponent-one upper question unresolved.
1187|2150|EP509; alias 2304007 / AMR-022-4007|P|The full EP-509 question remains unresolved.|Binomial-family exact covers do not solve the unrestricted disk-cover problem.
1188|2249|EP677|P|The arbitrary-length, arbitrary-gap problem remains unresolved|Finite lengths/gaps and reductions leave the arbitrary-length arbitrary-gap target unresolved.
1189|2334|EP839|P|Both original EP-839 questions remain unresolved for arbitrary admissible|Separated-block estimates and a source repair leave both universal original questions unresolved.
1190|2283|EP730|R|This is an audit of prior work|The full binomial-prime-support result is expressly prior work with named attribution, not a new-solution claim.
1191|2291|EP757|P|The original universal problem remains unresolved by this work.|The all-real obstruction concerns extensions of one exact seed; the universal target remains unresolved.
1192|2364|EP885|P|Unrestricted k=5 and the universal arbitrary-k target remain unresolved|Fixed-seed saturation/support statements do not resolve unrestricted k=5 or arbitrary k.
1193|2503|EP1122|P|The unrestricted EP 1122 / 2503 problem remains unresolved|The periodic-residual premise is not derived from the original density-zero hypothesis.
1194|3100034||R|This is an audit of a prior published resolution|The complete balanced-permutation classification expressly credits the published Combinatorica resolution.
1195|2440|EP1016|P|log-star lower bound remain unresolved by this work.|Outerplanar and star-weak-dual results leave the unrestricted crossing-chord problem unresolved.
1196|3000017||P|the exact block definition; arbitrary Eulerian multigraph halting remains|The certifying algorithm covers weighted cacti, while arbitrary Eulerian multigraph halting remains unresolved.
1197|3000008||P|The unrestricted simultaneous additive Δ−1 guarantee remains unresolved|The fixed-rank sufficient criterion does not settle the unrestricted two-sided matroid target.
1198|2678|K3 Problem 1.19|P|The conclusion is a scoped prior-result audit. No novelty, priority,|The credited closed-oriented smooth 3-manifold result does not certify the broader literal K3 target; a full broader resolution is expressly disclaimed.
1199|2366|EP887|P|formulation therefore satisfies K≥5. The general EP887 question remains|The credited five-divisor construction gives K>=5 but leaves the general uniform-bound problem unresolved.
1200|3000065||P|The unrestricted same-partition target remains unresolved by this work.|The regular-or-empty 2-core sufficient class does not settle unrestricted bipartite proportional factors.'''
records=[]
for row in raw.splitlines():
 num,pid,code,c,marker,reason=row.split('|',5);num=int(num);category={'F':F,'P':P,'R':R}[c]
 p=root/f'evidence/pr{num}';meta=json.loads((p/'METADATA.json').read_text());lines=(p/'PR_BODY.md').read_text().splitlines()
 matches=[(i,s) for i,s in enumerate(lines,1) if marker in s]
 if len(matches)!=1:raise ValueError((num,marker,matches))
 i,s=matches[0];e=[{'path':str((p/'PR_BODY.md').relative_to(root)),'line_start':i,'line_end':i,'quote':s}]
 extra={1151:[(1,9)],1155:[(1,5)],1165:[(34,38)],1168:[(3,21)],1169:[(3,9)],1170:[(3,9)],1171:[(28,30)],1173:[(19,24)],1175:[(30,32)],1176:[(21,24)],1177:[(23,26)],1178:[(4,9)],1179:[(32,35)],1181:[(7,13)],1182:[(3,14)],1183:[(3,18)],1184:[(3,13)],1185:[(21,23)],1189:[(3,5)],1190:[(3,12)],1194:[(3,15)],1195:[(67,72)],1196:[(3,9)],1198:[(10,14),(34,48)],1199:[(3,12)]}
 for a,b in extra.get(num,[]):
  e.append({'path':str((p/'PR_BODY.md').relative_to(root)),'line_start':a,'line_end':b,'quote':'\n'.join(lines[a-1:b])})
 ambiguity=None
 if num in (1151,1155):ambiguity='Generic no-novelty/priority certification disclaimer does not negate the explicit full target-result claim; this gate performs no priority audit.'
 if num==1168:
  ambiguity='Minimum-equivariance interpretation has a complete credited prior criterion, while stronger unspecified original naturality is unestablished. Classified scoped/partial for the original target; either interpretation excludes a new full original-solution claim.'
  for name,a,b in [('ACCEPTANCE.json',4,10),('README.md',13,21)]:
   q=out/f'pr{num}/{name}';ls=q.read_text().splitlines();e.append({'path':str(q.relative_to(root)),'line_start':a,'line_end':b,'quote':'\n'.join(ls[a-1:b])})
 if num==1198:
  ambiguity='The exact accepted closed-oriented category has a prior treatment. Broader literal K3 variants are uncertified; this is scoped/partial rather than a full original-resolution claim.'
  q=out/'pr1198/ACCEPTANCE.json';ls=q.read_text().splitlines();e.append({'path':str(q.relative_to(root)),'line_start':4,'line_end':19,'quote':'\n'.join(ls[3:19])})
 records.append({'pr':num,'url':meta['url'],'title':meta['title'],'problem_id':pid,'problem_code':code or None,'pinned_head_sha':meta['headRefOid'],'category':category,'eligible_for_original_process':category==F,'outcome_evidence':e,'reason':reason,'ambiguity':ambiguity,'metadata_path':str((p/'METADATA.json').relative_to(root)),'pr_body_sha256':hashlib.sha256((p/'PR_BODY.md').read_bytes()).hexdigest()})
now=datetime.datetime.now(datetime.timezone.utc).isoformat();counts={c:sum(x['category']==c for x in records) for c in [F,P,R,'needs_outcome_record']}
data={'schema':'actual-outcome-gate-v1','reviewed_at_utc':now,'scope':'PR #1151–#1200 inclusive; actual PR outcomes only; QUEUE.md not used','completion_estimate_percent':100,'independence':'No other classifier work read. No mathematical or priority audit, PR mutation, repair, publication, commit, or outreach performed.','counts':counts,'eligible_prs':[x['pr'] for x in records if x['eligible_for_original_process']],'remote_outcome_fetches':{'1168':['ACCEPTANCE.json','README.md'],'1198':['ACCEPTANCE.json','README.md']},'records':records}
(out/'OUTCOME_GATE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
md=['# Independent actual-outcome gate: PRs 1151–1200','',f'Recorded {now}. Completion estimate: 100% for this outcome-identification subtask.','', 'Read every pinned local PR body and metadata record in this range without consulting QUEUE.md or another classifier. This gate identifies recorded claims only; it does not validate mathematics, priority, or publication readiness. No PR mutation, external message, publication, commit, or mathematical audit was performed.','', '**Eligible explicit full-solution claims: #1151 and #1155.** Generic novelty/priority disclaimers do not negate their full target claims. Their mathematics and priority still require independent auditing.','',f'Counts: {counts[F]} explicit full claims; {counts[P]} scoped/partial/unresolved outcomes; {counts[R]} credited prior full resolutions; {counts["needs_outcome_record"]} missing outcome records.','', 'Scoped-prior boundary cases #1168 and #1198 were checked against pinned ACCEPTANCE.json and README.md. Both exclude a newly claimed full original solution. Each also credits prior work for the accepted scope. STATUS.json was absent at each pinned problem path; retained fetch errors document that absence.','', '## Per-PR evidence','']
for x in records:
 md.extend([f'### PR #{x["pr"]}: {x["category"]}','',f'Problem {x["problem_id"]}'+(f' / {x["problem_code"]}' if x['problem_code'] else '')+f'; pinned head `{x["pinned_head_sha"]}`.','',x['reason'],''])
 for e in x['outcome_evidence']:
  md.append(f'`{e["path"]}:{e["line_start"]}'+(f'–{e["line_end"]}' if e['line_end']!=e['line_start'] else '')+'`:');md.extend(['',*['> '+s for s in e['quote'].splitlines()],''])
 if x['ambiguity']:md.extend(['Scope note: '+x['ambiguity'],''])
(out/'REVIEW.md').write_text('\n'.join(md)+'\n')
print(json.dumps({'records':len(records),'counts':counts,'eligible_prs':data['eligible_prs'],'out':str(out)},indent=2))
