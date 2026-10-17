from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,re,hashlib
base=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1100_1200_20261017')
out=base/'gate_reviews/lower'
F='explicit_full_solution_claim';P='partial_or_unsolved';R='explicitly_prior_full_resolution'
# Scope classification only. No claim below certifies mathematical validity or priority.
spec={
1100:(P,'general complexity unresolved','The actual outcome expressly leaves the general minimum-rigidity-cut complexity target unresolved.',''),
1101:(P,'general conjecture unresolved','Structural overlap hypotheses cover a proper subcase and the general conjecture is expressly unresolved.',''),
1102:(F,'Accepted complete theorem','The PR claims the full prime/field/compact-Lie theorem answering the originating target; related credited results are explicitly narrower.','No-novelty boilerplate is not an outcome exclusion; mathematical validity and priority require the later audit.'),
1103:(P,'remains unresolved here','The fixed-arity Rado target is expressly unresolved.',''),
1104:(P,'general linear-size question unresolved','The unconditional general circuit-size target remains unresolved; the stronger conclusion is conjecture-dependent.',''),
1105:(P,'global compensation inequality is unproved','The universal per-set counting inequality is not proved; the claimed injection has an explicit extra hypothesis.',''),
1106:(P,'No finite upper bound','No finite upper hegemony-time bound or counterexample is claimed for a full-plane start.',''),
1107:(P,'unrestricted problem remains unresolved','The unrestricted no-Steiner Hamiltonian-path tetrahedralization problem is expressly unresolved.',''),
1108:(F,'affirmatively answers','The recorded result explicitly claims to affirmatively answer the original existential question, with a specified cone and barrier.','The cone is credited prior work; the complete original-target construction remains an explicit claim. The broader every-cone question is distinct.'),
1109:(P,'original non-CI classification unresolved','The original non-complete-intersection classification is expressly unresolved.',''),
1110:(P,'does not solve','The recorded result explicitly does not solve the original unrestricted principal-series connection question.',''),
1111:(P,'arbitrary symmetrizable-Cartan conjecture remains unresolved','The A1/A2/B2 block theorem excludes G2 and arbitrary higher rank, leaving the original conjecture unresolved.',''),
1112:(P,'does not solve the original','The singular-ambient counterexample is outside the original smooth-ambient problem, which remains unresolved.',''),
1113:(P,'not a full solution','The general irrational dependent arithmetic classification is expressly unresolved.',''),
1114:(F,'Complete smooth construction','The pinned STATUS and ACCEPTANCE explicitly say full_resolution=true; the stated construction answers all original regularity questions.','Relevant Mann–Tshishiku smooth B3 realization on a three-marked disk is expressly credited. The records still claim a complete prescribed-surface construction, so the priority relationship must be decided by the later priority audit rather than excluded at the outcome gate.'),
1115:(P,'full cylinder-free','The full cylinder-free/all-automorphism-extension equivalence is expressly unsolved.',''),
1116:(R,'principal budget-2','The decisive budget-2 counterexample and its non-MRS property are explicitly credited to Dughmi–Roughgarden–Yan (2011); this edition adds representation and reconstruction.','The all-field representation is supplied here, but the body explicitly identifies the decisive counterexample as prior mathematics; the prior manuscript did not explicitly address the later OWR question.'),
1117:(P,'original constant-versus-unbounded','The original constant-versus-unbounded directed linear k-cut gap question remains open.',''),
1118:(F,'Complete negative resolution','The PR explicitly claims counterexamples resolving both printed assertions.','Alternative definitions or general-position variants are excluded; exact-target interpretation remains for later audit.'),
1119:(F,'Accepted complete negative','The PR explicitly claims a full negative answer to the original testing-complexity comparison.','The recorded query model distinctions must be checked in the later audit.'),
1120:(P,'It remains OPEN','The original broader initial-surface, fixed-flow oval-limit question remains open.',''),
1121:(F,'original Problem 9 negatively','The PR expressly claims a complete finite-brace counterexample answering Cedó Problem 9 negatively.','No historical-novelty claim is made; this generic disclaimer does not remove the explicit full-solution claim.'),
1122:(P,'original three-question bundle remains PARTIAL','The star theorem is source credited and the original three-question bundle expressly remains partial.','Partial classification takes precedence over the prior-credit label because the full original bundle is unresolved.'),
1123:(P,'remains OPEN','The construction-route obstruction leaves the actual irreducible-complex proper-point Harbourne target open.',''),
1124:(P,'remains OPEN','The original skyrmion non-staticity/quantitative-energy target remains open.',''),
1125:(P,'no example and no full','Neither an example nor a full impossibility theorem is claimed for the fat connected Hilbert-component target.',''),
1126:(R,'Credit belongs','The exact Laurent-polynomial negative resolution is explicitly credited to Patureau-Mirand Theorem 4 (2012).',''),
1127:(R,'Credit: Maja','The exact Gaussian target is explicitly credited to Gwóźdź arXiv:2609.04052v1 rather than a new solution.','The credited source is an unrefereed preprint; prior-credit classification does not certify its validity.'),
1128:(P,'arbitrary-degree target remains OPEN','The exact low-degree classifications leave the full arbitrary-degree target open in both prime regimes.',''),
1129:(F,'Full two-clause','The PR explicitly claims both original clauses, including the all-c<3 Motzkin odd-power conclusion and threshold limit.','One clause is expressly a published Blekherman–Kozhasov–Reznick theorem; the Motzkin clause is presented as a complete authored deduction from a broader Scheiderer input. The whole target is not expressly attributed as an existing prior resolution.'),
1130:(P,'all-parameter problem remains OPEN','The complete P3 dimension table and other regimes leave the all-parameter Weddle problem open.',''),
1131:(P,'full bundled target remains OPEN','The equal-rate whisker interval 4/3<alpha<17/4 remains unresolved, so the original bundled target is partial.',''),
1132:(R,'Credit for the example','The complete counterexample, module decomposition and computer-assisted argument are explicitly credited to Ferudun.',''),
1133:(R,'resolved by','The original strong-density target is explicitly recorded as resolved by Chandrasekaran–Chekuri–Kulkarni; this is their source-credit audit and corrections.',''),
1134:(R,'supplies the proof','Tang is explicitly credited with the proof of the full original divisibility conjecture.',''),
1135:(F,'universal continuous-generator','The PR explicitly claims analytic counterexamples resolving the universal expected p-th-power comparison negatively.','The expectation-of-norm variant is expressly distinct; the later audit must verify exact original-target matching.'),
1136:(F,'Complete affirmative deduction','The PR claims a complete affirmative result for the named Hayman–Lingham problem with simultaneous all-R control.','Existing sharp Beurling and quadrature theorems are credited inputs, not an explicit attribution of the full original-target answer to prior work.'),
1137:(P,'remains unresolved','The full Godeaux fundamental-group target remains unresolved despite finite-cover deductions.',''),
1138:(R,None,'The saved PR body preserves historical Hinkkanen credit, and the pinned README says the 2018 edition already reports independence; this is an authored reconstruction of that known outcome.','Historical unpublished proof is not recovered, but the saved PR body and pinned outcome records explicitly agree on the prior outcome; no mathematics was audited.'),
1139:(P,'remains unresolved','The ordinal-colored preorder target expressly remains unresolved.',''),
1140:(R,None,'The saved PR body, pinned STATUS and pinned README expressly label the full original outcome a prior published resolution by Geuenich–Labardini-Fragoso–Miranda-Olvera.','Saved PR body and pinned outcome records agree on the exact prior published resolution.'),
1141:(F,None,'The saved PR body and pinned README expressly claim a complete affirmative proof for the exact two-polynomial Boolean-cube question.','Source-credit is to a separator lemma and other proof ingredients; it is not an explicit attribution of the complete original target as a previously resolved theorem.'),
1142:(F,None,'The saved PR body and pinned README claim a negative answer for the stated original class using connected domains with two boundary components.','The connected-boundary variant remains unclaimed; the later audit must verify the original target allows disconnected boundary. STATUS records acceptance as stated.'),
1143:(P,'original problem remains unresolved','The full endpoint cyclicity question is expressly unresolved; a proper cutoff ideal is not the target counterexample.',''),
1144:(P,'original problem remains PARTIAL','Generic computability does not provide the structural higher-rank target and the original problem expressly remains partial.',''),
1145:(R,'prior published counterexample','The original unrestricted negative answer is explicitly a prior published counterexample with a reconstruction.',''),
1146:(R,'historical characteristic-zero prior resolution','The historical characteristic-zero ladder assertion is explicitly credited to the published Mitra–Offen–Sayag theorem.','Unqualified field ambiguity and unclaimed positive-characteristic extensions are explicit. The accepted historical target is prior resolved.'),
1147:(P,'neither direction of the global','The global homometric sublinearity question is expressly unresolved; exact flower-class bounds are partial.',''),
1148:(R,'as a consequence','The edition explicitly presents the exact all-degree threshold as a credited prior-result implication of BDIM Theorem 4.5; pinned README confirms that attribution.','The authored bridge is accepted, but the title and README frame the target as a consequence of credited prior work, not a new full original-target solution.'),
1149:(P,'original uniform','The uniform quadratic-length single face-simple dual-path target remains unresolved; disjoint cycle packing is partial.',''),
1150:(F,'full counterexample','The PR explicitly claims a full negative answer under the original arbitrary finite purely inseparable hypothesis at an allowed index.','The n=0 equality and exponent-one predecessor are separate boundaries; later audit must verify the original binary-quadric convention.'),
}

def para(lines,needle):
 hits=[i for i,l in enumerate(lines) if needle.lower() in l.lower()]
 assert hits,(needle,lines)
 j=hits[0];a=j;b=j
 while a>0 and lines[a-1].strip():a-=1
 while b+1<len(lines) and lines[b+1].strip():b+=1
 return a+1,b+1,'\n'.join(lines[a:b+1])

def exact(path,a,b):
 lines=path.read_text().splitlines();return {'path':str(path.relative_to(base)), 'start_line':a,'end_line':b,'quote':'\n'.join(lines[a-1:b])}

ids={1136:2307037,1138:2302066,1140:30002450,1141:30006210,1142:30002112,1143:30001611,1144:30002009,1145:30002714,1146:30002482,1147:30002326,1148:30002562,1149:30002668,1150:30003045}
records=[]
for n,(cat,needle,reason,ambiguity) in spec.items():
 evidence=base/f'evidence/pr{n}'
 m=json.loads((evidence/'METADATA.json').read_text());body=(evidence/'PR_BODY.md').read_text()
 ID=ids.get(n) or int(re.search(r'\b(\d{4,})\b',m['title']).group(1))
 quotes=[]
 if needle:
  a,b,q=para(body.splitlines(),needle)
  quotes.append(exact(evidence/'PR_BODY.md',a,b))
  # Scope heads have a complete claim paragraph directly following.
  if q.startswith('## '):
   lines=body.splitlines();a=b+1
   while a<=len(lines) and not lines[a-1].strip():a+=1
   b=a
   while b<len(lines) and lines[b].strip():b+=1
   quotes.append(exact(evidence/'PR_BODY.md',a,b))
 if n==1114:
  quotes += [exact(out/'pr1114/STATUS.json',6,15),exact(out/'pr1114/README.md',15,18)]
 elif n==1138:quotes=[exact(evidence/'PR_BODY.md',1,9),exact(out/'pr1138/README.md',7,16)]
 elif n==1140:quotes=[exact(evidence/'PR_BODY.md',1,7),exact(out/'pr1140/README.md',3,9),exact(out/'pr1140/STATUS.json',5,15)]
 elif n==1141:quotes=[exact(evidence/'PR_BODY.md',1,9),exact(out/'pr1141/README.md',3,9)]
 elif n==1142:quotes=[exact(evidence/'PR_BODY.md',1,9),exact(out/'pr1142/README.md',3,17),exact(out/'pr1142/STATUS.json',5,15)]
 elif n==1148:quotes.append(exact(out/'pr1148/README.md',7,9))
 codes=sorted(set(re.findall(r'\b(?:AMR-\d+-\d+|OWR-\d+-\d+|GREEN-\d+)\b',body)))
 for q in quotes:codes+=re.findall(r'\b(?:AMR-\d+-\d+|OWR-\d+-\d+|GREEN-\d+)\b',q['quote'])
 records.append({'pr':n,'problem_id':ID,'problem_codes':sorted(set(codes)),'pinned_head_sha':m['headRefOid'],'category':cat,'outcome_evidence':quotes,'reason':reason,'ambiguity':ambiguity or None,'pr_url':m['url'],'scope_only_no_math_or_priority_validation':True})
counts=Counter(r['category'] for r in records)
now=datetime.now(timezone.utc).isoformat()
report={'schema':'actual-pr-outcome-gate-v1','reviewer':'independent lower-range outcome classifier','created_utc':now,'range':[1100,1150],'completion_estimate_percent':100,'scope':'Actual recorded outcome identification only; QUEUE.md not read or used. Mathematical validity, priority, repair, publication and PR disposition are unassessed.','rules':['Explicit full-original-target claim is eligible for later review.','Complete special cases with an explicitly unresolved full original target are partial.','Generic no-novelty/no-priority disclaimers do not exclude a complete original-target claim.','Explicitly attributed prior full resolutions are classified separately and not forwarded as claimed new full solutions.'],'counts':dict(counts),'eligible_prs':[r['pr'] for r in records if r['category']==F],'records':records}
(out/'OUTCOME_GATE.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
# Bind outcome statements fetched from pinned heads. Error records retain absent-path evidence.
fetch=[]
for p in sorted(out.glob('pr*/*')):
 n=int(p.parent.name[2:]);m=json.loads((base/f'evidence/pr{n}/METADATA.json').read_text())
 fetch.append({'pr':n,'pinned_head_sha':m['headRefOid'],'local_path':str(p.relative_to(base)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'requested_repository_path':f'unsolved_math_prioritization/attempts/{ids.get(n,30003952)}/{p.name.removesuffix(".error.txt")}', 'retrieval':'GitHub contents API, raw body at pinned head SHA' if not p.name.endswith('.error.txt') else 'HTTP 404 retained; no content available at requested path'})
if not (out/'FETCH_PROVENANCE.json').exists():
 (out/'FETCH_PROVENANCE.json').write_text(json.dumps({'created_utc':now,'records':fetch},indent=2,ensure_ascii=False)+'\n')
md=[f'# Actual-outcome gate, PRs #1100–#1150\n',f'Recorded at {now}. Outcome-gate completion estimate: **100%**. This estimate applies only to identifying the recorded outcome, not to the overall mathematical review/publication program.\n','All 51 pinned PR records were examined. QUEUE.md was not used. No mathematical or priority audit, repair, PR mutation, external comment, merge or publication was performed.\n',f'Explicit full-solution claims forwarded for later review: **{", ".join("#"+str(x) for x in report["eligible_prs"])}**.\n',f'Counts: {counts[F]} explicit full-solution claims; {counts[P]} partial/unsolved; {counts[R]} explicitly credited prior full resolutions; 0 unresolved outcome records.\n','A full claim is a claim to be rigorously audited, not an endorsement. Existing foundational ingredients and generic no-novelty language do not by themselves make a complete theorem ineligible. Explicit attribution of the full result to prior work does.\n','The important boundary cases are #1114 (full construction, directly relevant prior B3 realization; priority remains for later audit), #1129 (published first clause and complete authored deduction for second clause), #1136 (complete deduction from credited ingredients), #1141 (complete exact two-polynomial result from credited ingredients), #1142 (negative answer as stated with two boundary components), and #1148 (explicitly framed as a credited prior-result implication).\n','The nonempty saved PR bodies at #1138, #1140, #1141 and #1142 agree with the pinned outcome records retained here; both are quoted below. Pinned outcome records for #1114 and #1148 are also retained. See FETCH_PROVENANCE.json for exact hashes and absent-path records.\n']
for r in records:
 md.append(f'## PR #{r["pr"]} — {r["category"]}\n')
 md.append(f'Problem {r["problem_id"]}; head `{r["pinned_head_sha"]}`.\n')
 md.append(r['reason']+'\n')
 if r['ambiguity']:md.append('Boundary/ambiguity: '+r['ambiguity']+'\n')
 for e in r['outcome_evidence']:
  md.append(f'Outcome evidence: `{e["path"]}` lines {e["start_line"]}–{e["end_line"]}.\n')
  md.append('\n'.join('> '+x for x in e['quote'].splitlines())+'\n')
(out/'REVIEW.md').write_text('\n'.join(md))
print(json.dumps({'created_utc':now,'counts':dict(counts),'eligible_prs':report['eligible_prs'],'files':[str(out/'OUTCOME_GATE.json'),str(out/'REVIEW.md'),str(out/'FETCH_PROVENANCE.json')]},indent=2))
