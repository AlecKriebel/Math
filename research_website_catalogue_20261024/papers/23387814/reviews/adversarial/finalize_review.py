from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23387814');S=P/'sources';R=P/'reviews/adversarial';t=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((S/'receipt.json').read_text());checked=[]
for x in receipt['files']:
 b=(S/x['name']).read_bytes();z={'path':str((S/x['name']).relative_to(P)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'md5':hashlib.md5(b).hexdigest()};assert z['bytes']==x['bytes'] and z['sha256']==x['sha256'] and z['md5']==x['md5'];checked.append(z)
members=[]
for a in json.loads((S/'extraction-integrity.json').read_text()):
 for x in a['members']:
  p=S/'published-source'/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'];members.append({'path':str(p.relative_to(P)),'sha256':x['sha256']})
(R/'final_source_verification.json').write_text(json.dumps({'verified_utc':t,'completion_percent':100,'status':'UNCHANGED_MATCH','published_assets':checked,'extracted_members_checked':len(members),'all_extracted_members_match':True,'extraction_receipt_sha256':sha(S/'extraction-integrity.json'),'receipt_sha256':sha(S/'receipt.json'),'record_sha256':sha(S/'record.json'),'sources_mutated':False},indent=2)+'\n')
scopes={
 'szemberg0711v1':'Section4 final remarks and final question, p.7, with the exact minimal polarized-surface and arbitrary-point formulation. No implicit Picard-rank-one condition imported from the preceding theorem.',
 'owr2009-21-publisher':'Szemberg contribution printed p.1124: definitions, Theorem1 context, complete Conjecture2 and following very-general-point distinction. Printed p.1124 (PDF p.24) visually inspected to fix the fourth-root placement.',
 'primer0810v2':'Question6.1.6 and neighboring discussion on preprint p.17, including arbitrary minimal surfaces and contrast with very-general-point lower bounds.',
 'ein-lazarsfeld1993':'Introduction theorem/context and Example3.1 in full, printed p.182, identifying Miranda pencil/section construction; not the full article proof.',
 'bauer9903v1':'Proposition3.3 statement, complete construction portion of proof(a), and the finite-degree/asymptotic opening of proof(b). Checked that d=m+1 there is an asymptotic assertion, not a proved d=7 threshold.',
 'adjoint1011v1':'Proposition2.1 and its complete construction/proof of arbitrary rational constants on nonminimal blowups, with integral polarization E+2C.',
 'fuentes0511v2':'Section2 cyclic-cover setup and the ramification/canonical line-bundle identities, p.3. Only this interface is used; broader Picard-rank/very-general-point theorems are not imported.',
 'canonical0801v1':'Introductory canonical-polarization lower-bound discussion only; no independent verification of every example or full paper. The candidate uses an arbitrary ample L, not K.'}
pr=[]
for e in json.loads((P/'reviews/scope/primary-source-receipts.json').read_text()):
 if e.get('status')=='retrieved' and e['name'] in scopes:
  path=Path(e['cached_path']);assert sha(path)==e['sha256'];pr.append({**e,'read_scope':scopes[e['name']],'hash_reverified':True})
(R/'primary_sources.json').write_text(json.dumps({'completed_utc':t,'completion_percent':100,'sources':pr,'boundary':'Raw publications and acquisition receipts only shared from scope. No sibling or historical reviewer conclusions consulted. This is a proof-interface check, not exhaustive historical priority clearance.'},indent=2)+'\n')
geo=json.loads((R/'published_geometry_replay.json').read_text());pen=json.loads((R/'published_pencil_replay.json').read_text());fo=json.loads((R/'published_formula_replay.json').read_text());it=json.loads((R/'published_intersection_replay.json').read_text());fresh=json.loads((R/'fresh_results.json').read_text())
replay={'completed_utc':t,'completion_percent':100,'runtime':'/Users/alec/Documents/Math/.venv/bin/python','sympy_version':'1.14.0','mpmath_version':'1.3.0','mode':'normal Python, assertions enabled','all_four_exit_codes':0,'geometry_controls':geo['total_controls'],'pencil_controls':pen['total_checks'],'formula_degrees':len(fo['results']),'intersection_degrees':len(it['results']),'source_bindings':'published_helper_bindings.json','limits':'Only four standalone mathematical helpers were read and replayed in byte-identical isolated copies. Full package/integrity wrappers, historical audit code/reports, and prior outputs were not replayed or treated as independent proof.'}
(R/'published_replay_summary.json').write_text(json.dumps(replay,indent=2)+'\n')
review=f'''# Independent adversarial review — Zenodo 23387814

Completed {t}; assigned task 100%.

**Verdict: SUPPORTED AT THE STATED SCOPE.** No substantive defect was found. The construction does give smooth minimal complex projective surfaces, integral ample polarizations and special points contradicting the exact arbitrary-point lower bound, for every integer d>=7. The proof uses standard algebraic-geometric existence and ampleness theorems, not only numerical controls. This is an independent AI review, not human peer review or formal proof-assistant certification, and it does not establish historical firstness.

## Bound edition and coverage

The actual [Zenodo23387814](https://zenodo.org/records/23387814) PDF is `seshadri_counterexample.pdf`, all **five pages** read, printed **October14,2026**, Zenodo version1.0. SHA-256: `8f50f329fac5b30ffea3d98f82e36ec71af0d3d5df44e38a21f992eb45aa4c48`. The actual `verification_package.zip` SHA-256 is `6af7c815f863d44ba4b24708d5ae70bec4d5e0fd55789114083a605c08a27a20`. Both public assets were independently checked against size/MD5/SHA receipts at intake and completion. All **102** safely extracted files were rehashed at both checkpoints and remain unchanged. There is no additional embedded reader PDF.

Coverage includes the exact question, theorem, explicit singular member and entire-pencil existence argument, blowup and ampleness, smooth connected integral cover, canonical formula/minimality, split-fibre multiplicity/intersections, exact inequality and all stated limitations, followed by disclosure and references. `DERIVATION.md` reconstructs every mathematical stage and boundary. The published mathematical helpers were read only after a recorded independent reconstruction/control checkpoint.

## Exact primary target

The target is epsilon(S,L;x)>=1/(2+|K_S^2|^(1/4)), with **2 outside the fourth root**, a minimal smooth complex projective surface, an ample integral line bundle, and an **arbitrary point**, without a Picard-rank restriction. This was checked directly in [Szemberg's 2007 final question](https://arxiv.org/abs/0711.0584v1), [OWR2009 Conjecture2, printed p.1124](https://doi.org/10.4171/OWR/2009/21), and [Primer Question6.1.6, v2 p.17](https://arxiv.org/abs/0810.0728v2). The OWR equation and surrounding hypotheses were visually inspected, not inferred from imperfect OCR or a catalogue transcription.

The proposed example satisfies this target. It does not refute the neighboring very-general-point result, a Picard-rank-one result, or a canonical-polarization bound. The special point is permitted. The surfaces vary with d, so no assertion about the infimum over all polarizations and points of one fixed surface follows.

## Geometric attacks and outcomes

| Potential failure | Independent resolution |
|---|---|
| Reducible singular member or unseen projective singularity | The equation is primitive linear in Z, so Gauss's lemma proves integrality. The first partials exclude all singular points except [0:0:1], and the tangent polynomial has d−1 distinct factors. The multiplicity is exactly d−1. |
| Only a generic pencil member is integral | The full reducible/nonreduced locus has codimension at least d−1. Its join with the chosen integral member is proper for d>=3. A companion outside the join makes **every** pencil member integral and reduced. |
| Simultaneous genericity conditions incompatible | Smoothness, avoiding the marked singular point, and transversality are nonempty opens for the complete degree-d system. Their intersection with the nonempty join complement exists in the irreducible parameter space. The proof works at d=7 and does not borrow an unproved finite threshold from an asymptotic source. |
| Basepoint multiplicities or hidden exceptional fibre components | At a transverse basepoint, the two defining forms are local coordinates. Each pencil member is simple there, one blowup resolves the map, and every exceptional curve is a section. Bezout gives d^2 distinct basepoints away from the singular point. |
| A=2F+E_1 not ample | The full curve argument distinguishes the section, all horizontal curves, and vertical curves. The last class consists of whole integral reduced fibres, of degree one against A. Together with A^2=3, Nakai–Moishezon applies. |
| Cover singular over a bad fibre | The four branch fibres are smooth and avoid the marked one. Away from them, the cover is etale even where the original fibration has singular fibres. At branch fibres it is locally t=v^2 in smooth coordinates. Thus the entire covering surface is smooth. |
| Disconnected or reducible fibre product | Proper connected fibres over connected B prove connectedness; smoothness then gives integrality. Odd branch valuations also exclude a split quadratic extension over C(Y). Projectivity and finite flat degree two are preserved by the base change. |
| Incorrect canonical correction or overlooked (−1)-curve | The half-branch bundle is 2F, giving K_S=pi^*(K_Y+2F). N=(d−3)H+F has positive degree on every exceptional curve and every other integral curve, with N^2>0 for d>=4. Hence K_S is ample and adjunction excludes rational (−1)-curves. |
| Degree-two rather than degree-one curve upstairs | Because this is a base change and the special base value is unbranched, its inverse image is C x {{b_1,b_2}}, two disjoint copies of C. One chosen component has L.C'=1 and unchanged multiplicity d−1. A generic etale curve cover need not split, but that invalid inference is not used. |
| Wrong radical/domain or threshold | For d>=4, fourth powers preserve the positive comparison and reduce it to (d−3)^3>6(d−1). The margin starts positive at d=7 and increases. d=4,5,6 fail for this witness as explicitly stated. |

At d=7 the verified identities are K_S^2=144, L^2=6 and L.C'/mult_x(C')=1/6. Since 144<4^4, 1/6 is strictly less than 1/(2+144^(1/4)). Only an upper bound on epsilon is required; an exact value is not claimed.

The preimage of an old exceptional section is a genus-one curve of self-intersection −2 and canonical degree2, not a rational exceptional curve. The marked fibre can have rational normalization while positive arithmetic genus, so it does not contradict the adjunction argument for minimality. These checks address plausible but incorrect objections to the construction.

## Fresh independent evidence

`fresh_controls.py` was written and executed before reading any supplied helper. It imports no supplied code and uses exact integer/Fraction arithmetic. It passed **5,387** assertions, including:

- Degree cases d=3 through40: sparse polynomial Euler identities, exact multiplicity, squarefree tangent gcds, reducible-locus dimension formulas and proper-join bounds.
- Full blowup-lattice calculations of F, A, K_Y, N and cover degrees, including individual exceptional intersections and the single-fibre quotient. A topological Euler/Noether consistency check is recorded separately as a consistency check, not an existence proof.
- **1,999** exact integer inequality parameters, including d=10^20 and10^100, checking the forward-difference formula and strict threshold without floating-point radicals.
- Negative construction controls: F+E has zero degree on E; using only two branch fibres gives zero canonical degree on the lifted section; omitting the cover retains K_Y.E=−1; d=6 fails the strict comparison; branching at the singular fibre has vanishing gradient, while the smooth-fibre local cover has a nonzero derivative.

Finite checks do not certify the existence of a generic companion g, Bertini/transversality, Nakai–Moishezon, connectedness, or priority. Those logical steps are reconstructed in `DERIVATION.md`. The construction is explicit in its singular curve and numerical family, while its companion is chosen from a proved nonempty open set; no single fully enumerated companion polynomial was computed or needed for the existential theorem.

## Fresh replay of supplied mathematical support

After the independence checkpoint, four standalone mathematical helpers were read completely and copied byte-for-byte into an ignored isolated replay directory. Their hashes and original paths are in `published_helper_bindings.json`. They were run with the existing project Python runtime, confirmed **SymPy1.14.0/mpmath1.3.0**, in normal mode with assertions enabled. All exited zero:

- `reviews/geometry01/geometry_controls.py`: **1,183** exact controls, including rank-two cover algebra, split special fibre, local smoothness/branch failure and cover intersection lattice.
- `reviews/pencil01/fresh_controls.py`: **28,945** exact controls, including primitive-polynomial and singular-chart computations, parametrization, dimensions, jet/transverse-basepoint models and threshold controls.
- Original author `verify_formulas.py`: **97** degree cases d=4 through100.
- Original author `verify_intersections.py`: **27** degree cases d=4 through30.

The new outputs are saved in the four `published_*_replay.json` files. They are results of this execution, not adopted archived totals. Full package wrappers, historical audit prose, historical audit checkers and stored replay outputs were not run/read, and no full-package semantic audit is claimed. The helpers themselves explicitly limit their finite computations; they cannot establish the geometric existence proof or historical priority.

## Primary interfaces and attribution boundaries

`primary_sources.json` binds the actual primary PDFs, hashes, URLs and precise reading scopes. Raw files and acquisition receipts only were shared from the scope agent; no review conclusions were exchanged.

- The exact target was checked in Szemberg, OWR and the Primer as above.
- [Ein–Lazarsfeld, Example3.1](https://www.numdam.org/item/AST_1993__218__177_0.pdf) directly records Miranda's integral pencil and section polarization. Its introduction also distinguishes special small-constant points from the general-point lower bound.
- [Bauer, Proposition3.3](https://arxiv.org/abs/math/9903072v1) gives the related blowup construction and an asymptotic d=m+1 use. The candidate independently supplies the finite-degree integral pencil, so it does not silently convert that asymptotic assertion into d=7 existence.
- [Bauer–Szemberg, Proposition2.1](https://arxiv.org/abs/1011.0979v1) explicitly uses the integral polarization E+2C on a nonminimal pencil blowup. This ingredient is prior work.
- [Fuentes Garcia, Section2](https://arxiv.org/abs/math/0511547v2) gives the reduced ramification and canonical line-bundle formulas for a cyclic cover of a smooth surface branched over a smooth reduced divisor. Four disjoint smooth fibres meet these hypotheses. No unrelated rank-one or very-general-point lower bound from that source is imported.
- [Bauer–Szemberg's canonical-polarization paper](https://arxiv.org/abs/0801.3245v1) was checked only at its introductory lower-bound discussion; no complete example audit or firstness inference is claimed.

Standard characteristic-zero Bertini/transversality, intersection theory, Nakai–Moishezon and finite ample pullback are essential inputs. Their hypotheses were checked in the reconstructed proof. The bounded primary reading is not a full literature search and does not resolve the manuscript's stated priority gaps.

## Independence and action boundary

No current sibling mathematical report, historical dedicated verdict, acceptance document, audit prose or status body was read. Source manifests exposed only file names and hashes. Required manuscript section5 and its AI disclosure contain historical internal-review assertions, and required helper docstrings describe earlier independence; these were incidentally encountered and not adopted as evidence. Original support files were only hashed for inventory except for the selected mathematical helper bodies.

All authored results and logs are confined to `reviews/adversarial`. No website, spreadsheet, Git, Zenodo, publishing, repair or external outreach action was performed. No substantive defect warrants deferral from this independent gate; the parent retains the overall publication decision after all gates.
'''
(R/'REVIEW.md').write_text(review)
verdict={'record_id':'23387814','review_type':'independent_adversarial_mathematical','completed_utc':t,'completion_percent':100,'status':'SUPPORTED_AT_STATED_SCOPE','substantive_defects':[],'main_claim':'For every integer d>=7, existence of a smooth integral minimal complex projective surface with ample canonical bundle, K^2=6(d-1)(d-3), an ample integral L with L^2=6, and a special point with epsilon<=1/(d-1)<1/(2+(K^2)^(1/4)).','source_binding':{'pdf_sha256':checked[0]['sha256'],'verification_zip_sha256':checked[1]['sha256'],'all_five_pages_read':True,'all_102_extracted_members_unchanged':True},'fresh_controls':{'assertions':fresh['assertions'],'degree_cases':len(fresh['degree_cases']),'inequality_parameters':fresh['inequality_control_count'],'negative_controls':fresh['negative_controls']},'published_replay':replay,'proof_coverage':['exact original lower bound and arbitrary-point/no-rank restriction','integral explicit plane curve and unique ordinary singularity','proper join and simultaneous generic companion choice','transverse distinct basepoints and all reduced integral fibres','integral polarization ampleness for every curve','smooth finite flat connected integral projective double base change','canonical line bundle and global ampleness/minimality','split unbranched fibre and degree-one component','intersection numbers and strict inequality for all d>=7'],'independence':'Own reconstruction and exact controls checkpointed before helper reading. No sibling/historical opinion bodies read; necessary manuscript/helper status exposure disclosed.','limitations':['Standard geometric existence and ampleness theorems are not replaced by finite computations.','No explicit generic companion polynomial computed; proved nonempty open choice establishes existence.','No exhaustive historical priority or firstness claim.','No full package wrapper or historical audit checker replay.','Not human peer review or formal proof-assistant certification.'],'artifacts':['REVIEW.md','DERIVATION.md','fresh_controls.py','fresh_results.json','published_helper_bindings.json','published_replay_summary.json','primary_sources.json','final_source_verification.json']}
(R/'verdict.json').write_text(json.dumps(verdict,indent=2)+'\n')
with (R/'RESEARCH_LOG.md').open('a') as f:f.write(f'\n## {t} — 100%\n\nIndependent adversarial verdict finalized: supported at stated scope, no substantive defect. Full proof reconstruction and original arbitrary-point formula checked; fresh exact controls and all four selected unmodified mathematical-helper replays passed with pinned SymPy/mpmath versions. Original PDF/ZIP and all102 extracted files rehashed unchanged. Reports, source interfaces, result JSONs, bindings and evidence saved. Historical opinion bodies and sibling conclusions remain unread; manuscript/helper incidental assertions disclosed. No repair, site, sheet, Git, publishing or outreach action taken.\n')
names=['REVIEW.md','DERIVATION.md','verdict.json','RESEARCH_LOG.md','source_integrity.json','final_source_verification.json','fresh_controls.py','fresh_results.json','independence_checkpoint.json','published_helper_bindings.json','published_geometry_replay.json','published_pencil_replay.json','published_formula_replay.json','published_intersection_replay.json','published_replay_summary.json','primary_sources.json','published-paper.txt']
(R/'evidence_manifest.json').write_text(json.dumps({'created_utc':t,'completion_percent':100,'files':[{'path':str((R/n).relative_to(P)),'bytes':(R/n).stat().st_size,'sha256':sha(R/n)} for n in names],'note':'No self-hash. Source acquisition/extraction receipts bind original assets; final_source_verification confirms unchanged bytes.'},indent=2)+'\n')
print(json.dumps({'status':verdict['status'],'completed_utc':t,'review_sha256':sha(R/'REVIEW.md'),'derivation_sha256':sha(R/'DERIVATION.md'),'verdict_sha256':sha(R/'verdict.json')},indent=2))
