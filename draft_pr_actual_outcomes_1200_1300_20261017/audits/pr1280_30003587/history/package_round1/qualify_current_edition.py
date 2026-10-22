from pathlib import Path
from datetime import datetime,timezone
import difflib,hashlib,json
A=Path(__file__).resolve().parents[1];S=A/'submitted';C=A/'current_edition'
now=datetime.now(timezone.utc).isoformat()
def dig(b):return hashlib.sha256(b).hexdigest()
def bind(b):return {'bytes':len(b),'sha256':dig(b)}
def js(obj):return (json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode()
old={p.name:p.read_bytes()for p in S.iterdir()if p.is_file()}
if len(old)!=9:raise RuntimeError('Original must have nine files')
new=dict(old)
proof=old['PROOF.md'].decode()
before='This proves the edge-diagonal theorem with neither extra hypothesis. Notice that the pinch/polar step is necessary: strong approximate innerness cannot simply be claimed invariant under arbitrary exterior equivalence.'
after='This proves the edge-diagonal theorem with neither extra hypothesis. Pinching and polar decomposition supply the original fixed-algebra membership in this proof. An alternative is available for genuine cocycle perturbations of finite abelian actions: if alpha_g=Ad(d_g) beta_g and d is an honest beta-cocycle, beta-fixed implementers v_n for beta_g give t_n=d_g v_n with ||alpha_h(t_n)-t_n||=||beta_g(d_h)-v_n d_h v_n*|| tending to zero. Finite averaging over alpha, followed by polar decomposition, gives exactly alpha-fixed implementers. This alternative requires the genuine cocycle law; a projective family of pointwise inner implementers does not supply it.'
if proof.count(before)!=1:raise RuntimeError('Exact proof qualification anchor differs')
proof=proof.replace(before,after)
proof+='\n## Current review qualification (17 October 2026 local date)\n\nThe complete deduction above is retained. The claim that one specific pinch/polar construction is necessary has been replaced by the explicit alternative for genuine finite abelian cocycles. This changes no theorem, graph reduction, or implementing sequence used in the original proof. Matsumoto\'s 2000 diagonal-coboundary and periodic-point arguments precede the inner-phase mechanism (Lemma 5.14 and Proposition 6.4), and the return corner is a special case of Crisp–Gow\'s 2004 preprint Theorem 3.1. These mechanisms are credited prior work. The current audit does not establish firstness of the combined full statement or current worldwide openness. Current verification is supplied separately from the historical 11October acceptance and check summaries.\n\n- K. Matsumoto, On automorphisms of C*-algebras associated with subshifts, J. Operator Theory 44 (2000), 91–112, Lemma 5.14 and Proposition 6.4: https://jot.theta.ro/jot/archive/2000-044-001/2000-044-001-005.pdf .\n- T. Crisp and D. Gow, Contractible subgraphs and Morita equivalence of graph C*-algebras, arXiv:math/0404542v1 (29April2004), Theorem 3.1 and canonical path map: https://arxiv.org/abs/math/0404542v1 . The current source inspection uses the preprint; final DOI10.1090/S0002-9939-06-08216-5 is bibliographic metadata, without assuming final-body identity.\n'
new['PROOF.md']=proof.encode()
new['PROOF.md']+=('''
### Broader prior-theorem consequence identified in the current audit

The full target is also an explicit consequence of Gabe–Szabó's general equivariant uniqueness theorem: arXiv:2205.04933v1 (10 May 2022), Definition 1.15 p.13, Proposition 3.14 p.29 and Theorem 5.8 pp.45–46 (https://arxiv.org/abs/2205.04933v1). For an outer finite abelian edge-phase action, each automorphism is equivariantly homotopic to the identity by interpolating its edge phases. Equivariant uniqueness gives asymptotically implementing, asymptotically whole-action-fixed unitaries; finite averaging and polar decomposition give exactly fixed unitaries. The normalized all-group vertex representation above removes the inner kernel, giving an outer quotient with no graph-period restriction. The genuine-cocycle averaging argument restores the original action. This complete assembly was written and checked in the current audit; it is not attributed as a printed Cuntz–Krieger theorem in that source. Final publication metadata is Acta Math.232(2024),1–77, DOI10.4310/ACTA.2024.v232.n1.a1; inspected theorem locators refer to the actual preprint, not an unavailable final body.

Christensen–Neagu–Szabó, arXiv:2504.12730v1 (17 April 2025), Definition3.1/Remark3.2 pp.11–12 and Theorem3.7 p.15 (https://arxiv.org/abs/2504.12730v1), supplies a prior duality framework for exactly the weaker strong approximate innerness used here. Genuine-cocycle and ambient-full-corner transfer can also be composed from that framework; these are not claimed as newly discovered invariance mechanisms. The current paper is an attributed exposition and complete verification of prior-theorem consequences. No first solution, new mechanism, earliest consequence date, or present worldwide openness is certified.
''').encode()
audit=old['INDEPENDENT_AUDIT.md'].decode()
before='The final pinching step is essential and correct; arbitrary exterior equivalence alone would not justify fixed-point membership.'
after='The final pinching step correctly supplies fixed-point membership in this argument. A genuine finite abelian cocycle perturbation also admits an averaging/polar alternative, so pinching is not a necessary form of the argument. Exact fixed-algebra membership must still be proved.'
if audit.count(before)!=1:raise RuntimeError('Exact audit qualification anchor differs')
audit=audit.replace(before,after)
audit=audit.replace('Date: 11 October 2026.','Date of historical audit: 11 October 2026. Current editorial qualification: 17 October 2026 local date.\n\nEditorial provenance: the original submitted report remains verbatim in the verification package. This current edition qualifies the former absolute pinching-necessity sentence. Its historical first-person source and execution statements are retained as historical claims, not as newly authenticated events. The older frozen proof, audit and supplement named below are unavailable in the submitted nine-file packet; current independent mathematical review does not certify those missing bytes or the old execution history.',1)
new['INDEPENDENT_AUDIT.md']=audit.encode()
new['README.md']=('''# Strong approximate innerness of finite abelian diagonal quasi-free actions

Problem30003587; OWR-15585-006. Original submitted edition:11October2026. Current qualification:17October2026 local date.

For an essential finite0–1 matrix M with simple purely infinite O_M, every finite abelian diagonal quasi-free action is strongly approximately inner. For each group element the implementing sequence is fixed by the entire action. No group law or approximate-representability conclusion for these sequences is asserted.

The proof reduces the full original question to Barlak–Szabó's published outer aperiodic theorem. Current independent AI reviews include a source-only reconstruction and fresh adversarial checks of that reconstruction and of a distinct full-corner/cocycle argument. The proof remains dependent on the expressly cited published operator-algebra and graph inputs. AI tools were used extensively. There is no external human peer review or formal proof-assistant certification.

The former assertion that pinching is necessary was too strong. The current proof and current editorial audit now give or identify a genuine finite abelian cocycle averaging/polar alternative. The original submitted files remain preserved separately. This qualification does not weaken the full theorem or repair a gap in its sufficient pinching argument.

Matsumoto2000 precedes the diagonal-coboundary/periodic-orbit mechanism. Crisp–Gow's29April2004 preprint Theorem3.1 subsumes the return-corner construction. The full target is also a composed consequence of Gabe–Szabó's10May2022 general equivariant uniqueness theorem (arXiv:2205.04933v1 Theorem5.8, Proposition3.14 and Definition1.15), normalized inner-kernel reduction and genuine-cocycle averaging. The short current note uses that route without any graph-period restriction. Christensen–Neagu–Szabó's2025 duality gives prior infrastructure for the weaker strong approximate innerness and its transfer mechanisms. This is an attributed exposition and complete verification of prior-theorem consequences. No first solution, firstness, new-mechanism, earliest consequence date, current worldwide openness or community-acceptance claim is made. No inspected old source is asserted to print the entire combined CK statement. Priority and publication readiness are separate from the historical audit and are documented in the current verification package.

Reading order:

1. PROOF.md gives the full theorem, its sufficient proof and the current qualification.
2. INDEPENDENT_AUDIT.md is the historically dated AI audit with an explicitly marked current editorial qualification. Its historical first-person and execution claims are not new events.
3. SOURCE_VERIFICATION.md and SOURCE_METADATA.json preserve the11October source-scope records. Fresh source versions and current priority checks are documented separately in the verification package.
4. ACCEPTANCE.json separates the historical acceptance data from the current qualification; EDITORIAL_CHANGE_MAP.json separates the historical change map from the new byte changes.
5. CHECK_RESULTS.json remains the historical aggregate summary. Its old check program and old raw inputs are not supplied in that historical packet and were not replayed as new evidence. Current authored diagnostic code, explicit limits, actual run receipts and durable normal/-O/-OO checks are in the verification package.
6. MANIFEST.json binds the eight other current files. Its own conventional hash is anchored outside this directory.

The current preprint and supporting package are maintained under publication/. All third-party source PDFs, extracts, page images and raw provider outputs are excluded from public authored membership. Hashes establish byte identity, not mathematical truth. The original historical frozen inputs named by the older acceptance cannot be independently authenticated without their bytes.
''').encode()
markdown=['PROOF.md','INDEPENDENT_AUDIT.md','README.md']
deltas=[]
for name in markdown:
    ol=old[name].splitlines(keepends=True);nl=new[name].splitlines(keepends=True)
    oo=[0];no=[0]
    for line in ol:oo.append(oo[-1]+len(line))
    for line in nl:no.append(no[-1]+len(line))
    matcher=difflib.SequenceMatcher(None,ol,nl,autojunk=False)
    for tag,ii,jj,kk,ll in matcher.get_opcodes():
        if tag=='equal':continue
        i,j,k,l=oo[ii],oo[jj],no[kk],no[ll]
        deltas.append({'path':name,'operation':tag,'original_byte_range':[i,j],'current_byte_range':[k,l],'original_fragment':bind(old[name][i:j]),'current_fragment':bind(new[name][k:l])})
emap={'schema':'current-qualified-edition-change-map-v2','at_utc':now,'problem_id':'30003587','scope':'Current source qualification and historical/current provenance separation. Historical nested records retain their old meaning and are not active current hash claims.','historical_20261011_editorial_map':json.loads(old['EDITORIAL_CHANGE_MAP.json']),'current_original_markdown':{n:bind(old[n])for n in markdown},'current_outputs':{n:bind(new[n])for n in markdown},'current_byte_changes':deltas,'limits':['Older original frozen proof/audit/supplement bytes are unavailable; the current review cannot authenticate old-to-submitted preservation.','New changes are against the captured submitted Git blobs, not unavailable historical inputs.','Acceptance/manifest wrappers and the full nine-file inventory are separately bound in CURRENT_EDITION_CORRECTION.json in the current verification package.']}
new['EDITORIAL_CHANGE_MAP.json']=js(emap)
accept={'schema':'current-qualified-ai-audit-binding-v2','problem_id':'30003587','at_utc':now,'current_status':'scope-qualified current deduction reviewed; full publication-package gate separate','accepted_theorem':json.loads(old['ACCEPTANCE.json'])['accepted_theorem'],'historical_20261011_acceptance':json.loads(old['ACCEPTANCE.json']),'current_qualification':{'main_theorem_unchanged':True,'sufficient_original_proof_unchanged_except_overclaim_and_added_alternative_explanation':True,'absolute_pinching_necessity_withdrawn':True,'honest_finite_abelian_cocycle_alternative_explained':True,'prior_mechanisms_credited':['Matsumoto2000 Lemma5.14/Proposition6.4','Crisp–Gow2004v1 Theorem3.1','Gabe–Szabó2022v1 Theorem5.8/Proposition3.14/Definition1.15 with the explicit current full-target composition','Christensen–Neagu–Szabó2025v1 Definition3.1/Remark3.2/Theorem3.7 prior framework'],'old_missing_inputs_or_runs_authenticated':False},'current_public_artifacts':{n:bind(new[n])for n in ['PROOF.md','INDEPENDENT_AUDIT.md','EDITORIAL_CHANGE_MAP.json','README.md']},'limits':['Extensive AI use; unrefereed, no external human review or formal certification.','Finite diagnostics do not certify operator-algebra limits.','No firstness, new mechanism or current worldwide openness claimed.','Current mathematical and priority gates are separate from final package review/publication approval.']}
new['ACCEPTANCE.json']=js(accept)
manifest=json.loads(old['MANIFEST.json']);manifest['created_date']='2026-10-17';manifest['original_submitted_created_date']='2026-10-11';manifest['revision_scope']='Explicit current documentary qualification with historical records nested; full theorem unchanged'
manifest['files']={n:bind(new[n])for n in sorted(new)if n!='MANIFEST.json'}
new['MANIFEST.json']=js(manifest)
reasons={'PROOF.md':'Qualify absolute pinching necessity with the valid honest-cocycle alternative and credit authenticated prior mechanisms.','INDEPENDENT_AUDIT.md':'Qualify the same necessity wording and explicitly distinguish historical first-person/old-input claims from current review.','README.md':'Explain current result/qualification, prior credit and historical-vs-current evidence boundaries.','EDITORIAL_CHANGE_MAP.json':'Preserve the original map nested as historical, add exact submitted-to-current markdown change spans.','ACCEPTANCE.json':'Preserve historical acceptance nested and bind the current documentary qualification without certifying missing old inputs.','MANIFEST.json':'Rebind all eight nonself current files after the qualification.'}
changes=[]
for name in sorted(old):
    if new[name]!=old[name]:changes.append({'path':name,'original_sha256':dig(old[name]),'current_sha256':dig(new[name]),'reason':reasons[name]})
if len(changes)!=6:raise RuntimeError('Expected exactly six current documentary changes')
for name,b in new.items():
    tmp=C/(name+'.qualified-tmp');tmp.write_bytes(b);tmp.replace(C/name)
receipt={'schema':'math-pr1280-current-edition-correction-v1','pr':1280,'problem_id':30003587,'original_head':'f5085a4c954f814cde1bc3be0727ff30373aea95','submitted_snapshot_sha256':dig((A/'SUBMITTED_SNAPSHOT.json').read_bytes()),'original_files':{n:bind(b)for n,b in sorted(old.items())},'current_files':{n:bind(b)for n,b in sorted(new.items())},'changes':changes,'at_utc':now,'scope':'Six controlled documentary/provenance changes; nine original Git-authenticated submitted files preserved verbatim. No main theorem weakening or gap repair. Honest-cocycle alternative is supported by a separate new structural proof and independent adversary. All prior source/raw artifacts remain private.'}
(A/'CURRENT_EDITION_CORRECTION.json').write_bytes(js(receipt))
print(json.dumps({'at_utc':now,'changed_files':[r['path']for r in changes],'correction_sha256':dig((A/'CURRENT_EDITION_CORRECTION.json').read_bytes()),'current_files':receipt['current_files']},indent=2))
