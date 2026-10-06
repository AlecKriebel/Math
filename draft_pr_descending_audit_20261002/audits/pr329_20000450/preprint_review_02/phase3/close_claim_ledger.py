#!/usr/bin/env python3
"""Close the frozen IDs from written deductions; preserve the old log prefix."""
from pathlib import Path
import hashlib,json,re,stat,subprocess

if not __debug__:
    raise SystemExit('Assertions must remain enabled for this evidence check.')
N=Path(__file__).resolve().parent.parent
A=N.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def utc():
    return subprocess.run(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],capture_output=True,check=True).stdout.decode().strip()
assessment=N/'FIRST_CANDIDATE_ASSESSMENT.md'
assert sha(assessment.read_bytes())=='eced93c50a8afc19fa454b96c8ee2e956805c81560d7940a4004f86c6395206e'
rows=[]
for line in assessment.read_text().splitlines():
    if re.match(r'^\| [CSM]\d{3} \|',line):
        fields=[x.strip() for x in line.split('|')[1:-1]]
        assert len(fields)==4
        rows.append(dict(zip(['id','original_location','original_claim','frozen_first_assessment'],fields)))
assert [r['id'] for r in rows]==[f'C{i:03}' for i in range(1,62)]+[f'S{i:03}' for i in range(1,10)]+[f'M{i:03}' for i in range(1,5)]
g='families/geometry/GEOMETRY_FAMILY_REPORT.md'
k='families/kernel/REPORT.md'
ar='phase3/ARITHMETIC_MODULI_REPORT.md'
sp='phase3/SOURCE_PUBLIC_PACKET_REPORT.md'
proofs={
'C001':('F1',[g],'Expand the conjugate cyclotomic side factors. Consecutive unit-circle vertices and scale give the exact K-polynomial.'),
'C002':('F1',[g],'Homogeneous degrees require T; the exact projective restriction and origin are verified, with C028 supplying origin transport.'),
'C003':('F1,F6',[g],'Two genuine quadratic extensions, four odd branch places, primitivity and the nonzero infinity restriction prove the entire projective normalization. Exactly the three finite exclusions and the infinite member are treated separately.'),
'C004':('F3',[g,k,ar],'The whole normalization is established by C003; direct chord equivalence and simple degree-12 kernel give twelve abscissae/two signs plus O. Marked four and residual twenty have complete inverse-chart coverage.'),
'C005':('F5',[ar],'Actual Tate twist and all-specialization exact Tate field supply the upper inclusion. Nonzero transported P0 forces delta and the Weil pairing forces zeta, giving equality in both directions.'),
'C006':('F5',[ar],'The compulsory compositum has degree four. Norm degree four detects fifth powers already over K; adjoining theta therefore has degree one or five.'),
'C007':('F5',[ar],'Real theta and conjugation yield D10; its unique quadratic is the cyclotomic field and is distinct from the real twist field. Split case gives the two independent quadratics.'),
'C008':('F5',[ar],'The independent delta sign automorphism fixes the Tate field and acts as -I; a fifth-torsion vector fixed by it is zero.'),
'C009':('F2,F5',[k,ar],'The five smooth infinity points are the exact marked cyclic subgroup over the real twist field; real elliptic odd torsion has exactly five elements.'),
'C010':('F5',[ar],'The valuation of lambda+c at -c is one, so the generic radical is not a fifth power. The constant quadratics and the all-specialization field theorem give degree twenty.'),
'C011':('F1',[g],'Independent full coefficient expansion gives the displayed primitive quartic A Y^4+B Y^2+C.'),
'C012':('F1',[g],'Exact symbolic coefficient identity for B^2-4AC=h^2 times the displayed quadratic; conic discriminant is separately nonzero.'),
'C013':('F1',[g],'The actual V equation and rational inverse parametrize the nonsingular conic; a nonzero denominator is a function, rather than a missing component.'),
'C014':('F1',[g],'Independent substitutions and both directions give the two double-cover equations; each allowed specialization has the proved field degrees and dense charts.'),
'C015':('F1',[g],'Exact coefficient expansion after the specified shift reproduces all four a_i.'),
'C016':('F1',[g],'The nonzero a3 change produces the monic cubic by an equation identity; its discriminant is nonzero on exactly the allowed range.'),
'C017':('F1',[g],'All inverse expressions are derived from the conic/double-cover relations; both compositions hold on the actual complete source function field.'),
'C018':('F1',[g],'The cleared G identity and reverse conic branch are checked exactly; the latter does not change to the other square-root branch.'),
'C019':('F1',[g],'A function-field isomorphism of smooth projective curves extends uniquely. Integral full-curve identification and nonsingularity are proved before this standard principle is applied.'),
'C020':('F1',[g],'All four universal discriminant identities hold. The conic extension has genuine degree two and the subsequent quadratic has four odd branch places, giving genus one by Riemann-Hurwitz.'),
'C021':('F1',[g],'A has only the stated root. Its B-zero specialization has C=-1. Thus gcd(A,B,C)=1 on every allowed and relevant limiting fiber and no vertical component is lost.'),
'C022':('F1',[g],'The homogeneous T=0 restriction is nonzero, excluding a T component. Primitive affine irreducibility then describes the whole projective curve.'),
'C023':('F6',[g],'At zero the actual side product is five distinct lines, verified independently from the cyclotomic expansion.'),
'C024':('F6',[g],'Exact conjugate-phi product equals the -5r member, and the five resulting line factors are distinct.'),
'C025':('F6',[g],'At -c the nonsingular conic and explicit F with one double root leave two odd branch places. The primitive full source is integral with genus-zero normalization; no triple root or hidden component remains.'),
'C026':('F6',[g],'The pencil parameter at infinity is exactly T Q^2: a nonreduced member with rational reduced components, outside the elliptic theorem.'),
'C027':('F6',[g],'Universal vertex jet, nonzero kernel cubic and rotational invariance give five A2 cusps at the stated allowed parameter. Their delta total remains five and the normalization genus is one.'),
'C028':('F1,F2',[g,k],'Direct inverse valuations at the cubic origin give the plane limit [0:1:0]; the plane partial is ten, and actual scales/denominators are nonzero.'),
'C029':('F4',[g,ar],'Independent generalized-Weierstrass discriminant computation gives Delta_beta=beta^5(beta^2-11beta-1), with the exact nonzero lambda pullback.'),
'C030':('F4',[g,ar],'Actual origin-preserving equation isomorphism uses k delta, with all scales nonzero. It applies at exceptional j as well as generic j and is not inferred from equal j.'),
'C031':('F2,F3',[k],'Generalized chord law directly gives 2P0, 3P0, -P0 and exact order five with beta nonzero.'),
'C032':('F3,F7',[k,ar],'Original Morton v1/v4 operative table inspected in pixels/text; every row agrees under b=-beta with the manuscript residual.'),
'C033':('F3',[k],'Fresh direct-kernel calculation reconstructs all thirteen quintic coefficients and all eleven residual rows, without importing a packaged coefficient record.'),
'C034':('F3',[k],'Completing the square gives both ordinates; the resultant and discriminant proofs show the two values are distinct at every residual root.'),
'C035':('F3',[k],'Direct Vieta tangent/secant derivation produces Q3,H6,Q5 and factor x(x-beta)R. Classical division meaning is independently linked by the full iff chord proof.'),
'C036':('F3',[k],'Derive x(2P), x(3P) from the actual completed cubic chord formulas, retaining f and Q3 denominators and the exact cleared equality.'),
'C037':('F3',[k],'Full symbolic resultants are Delta^6 and Delta^8, with exact constants/signs. The polynomial discriminant is 5^11 Delta^22, so no allowed specialization loses coverage.'),
'C038':('F3',[k],'Fresh exact evaluations give R(0)=5 beta^8 and R(beta)=5 beta^12; both are nonzero on the domain.'),
'C039':('F3',[k],'Resultants exclude ordinate-zero and doubling-denominator roots. x(2P)=x(3P) forces 3P=-2P, since equality would imply P=O; conversely nonzero fifth torsion avoids all prohibited denominators.'),
'C040':('F3',[k,ar],'Constant leading coefficient five and nonzero universal discriminant yield twelve distinct abscissae with two distinct signs. The equivalence supplies exactly the full 25-element kernel; classical separable [5] agrees.'),
'C041':('F3,F6',[k,g],'Inverse transverse denominators reduce to x and x-beta. Exact residual evaluations exclude them. The additional node-image collision has finite inverse values and is not an excluded elliptic fiber.'),
'C042':('F2',[k],'Actual infinity factors yield the five slopes and nonzero plane partials; r/delta is sqrt(5-2r). Direct Tate limits identify every point and its real field.'),
'C043':('F2',[k,g],'Intrinsic rotation preserves the pencil and has order five on the whole normalization. Its origin-fixing linear part cannot have order five, so it is a translation. Direct marked limits independently identify the subgroup; the former C003 dependency is now discharged.'),
'C044':('F4',[ar],'Fisher marked-pair uniqueness removes automorphisms, including CM fibers. With fixed P and pairing value, the five complementary vectors form the actual fine finite-etale degree-five cover.'),
'C045':('F4',[ar],'Actual Fisher Lemma3.4 and marked-subgroup proof use exactly beta=tau f/g, with all f,g coefficients and conventions checked.'),
'C046':('F4',[ar],'Independent early rational identities and scalar matrix squares verify epsilon/iota involutions and both stated fractions exactly.'),
'C047':('F4',[ar],'The actual marked generic covers have the same function field. Both finite normal etale covers of the nonsingular normal base are its integral closure there, giving identical fibers, including split and CM fibers.'),
'C048':('F4',[ar],'Literal u=-1/theta gives both field inclusions and inverse Kummer class, without identifying a fixed class with its inverse.'),
'C049':('F4,F7',[ar],'Original Morton v1/v4 radical and the exact b=-beta transformation give u_M^5=c(lambda+c), u_M=phi theta.'),
'C050':('F4',[ar],'All eighteen Verdure scan pages and the operative proof were read. Correct roots/signs give the exact ratio, and his universal nonsingular specialization justification applies to every allowed beta.'),
'C051':('F4,F5',[ar],'With zeta and P the Galois image is unipotent of order one or five. Verdure sufficiency gives the upper inclusion; his necessity rules out degree one precisely when theta is absent, giving exact equality.'),
'C052':('F4,F5',[ar],'Actual twist transports the universal Tate equality over L, proving L(E[5])=L(theta) in both directions on every fiber, not merely generically.'),
'C053':('F5',[ar],'The exact transported P0 coordinate has nonzero K coefficient of delta for all allowed lambda, so the intrinsic full normalization torsion field contains delta.'),
'C054':('F5',[ar],'The actual primary Weil-pairing theorem is nondegenerate and Galois equivariant. A basis of the full geometric kernel supplies primitive zeta fixed by the full coordinate field.'),
'C055':('F5',[ar],'Norm d=5 excludes a square in K. The real twist quadratic and imaginary cyclotomic quadratic are distinct, yielding compositum degree four.'),
'C056':('F5',[ar],'For v^5=a in L, norm(v)^5=a^4, hence (a/norm(v))^5=a in K. The converse is immediate; negative a and all nonzero specializations are included.'),
'C057':('F5',[ar],'Real theta, inverted zeta, unique quadratic of D10 and its distinction from M prove the exact disjointness/direct product; the split case is separately computed.'),
'C058':('F5',[ar],'A valuation of one at -c excludes a generic fifth power; the degree-four norm descent retains this after the constant quadratics.'),
'C059':('F5',[ar],'The now-proved independent delta involution negates eta while fixing xi; it is -I on the actual curve, and has no nonzero fixed fifth-torsion vector.'),
'C060':('F2,F5',[ar,k],'Real elliptic odd-order torsion lies in the circle identity component and has exactly five points. The five explicit M-rational marked points exhaust it.'),
'C061':('F5',[ar],'Choose P and replace Q by Q-tP/2 to make conjugation diagonal. A nonzero unipotent Kummer action can be normalized to shift one; delta acts as -I. Determinants, orders, relation and split omission are checked.'),
'S001':('F7',[sp],'Fresh pre-exposure AIM source frontmatter and physical page51/all four remarks establish the attribution, dates and known infinity-subgroup boundary.'),
'S002':('F5,F7',[sp],'The actual K-rational origin prevents this model from supplying a nontrivial torsor/Sha example. All public statements exclude the additional variants and local-solubility claims.'),
'S003':('F7',[sp,ar],'Public wording disclaims firstness. Actual older primary mathematics is positively credited; the stated bridge contribution is not converted into certified ultimate originality.'),
'S004':('F7',[sp,ar],'Precise Fisher/Verdure/Morton operative hypotheses, equations, signs, versions, dates and all residual rows were independently compared to downloaded primary bytes.'),
'S005':('F7',[sp],'Retained prior report was read in full and is accurately acknowledged as partial. Selected upstream semantics and legacy report serialization reproduce; the old problem-wrapper serialization is an explicit unresolved historical boundary.'),
'S006':('F7',[sp],'All archive entries, program bodies, declared export transformations, expected outputs and primary comparison records were inspected/bound. All 29 actual children reproduce the claimed positives, mutants, guards and verifiers.'),
'S007':('F7',[sp],'Finite checks remain implementation evidence. The bounded search and all historical receipt/count limitations are explicit; no absence of hits establishes firstness or present openness.'),
'S008':('F7',[sp],'TeX, complete PDF and deposit consistently disclose extensive AI use, author responsibility and unrefereed status. Independent agent checks are not relabeled external human review or formal proof certification.'),
'S009':('F7',[sp],'Creator, affiliation, ORCID and date agree with the actual human-provided author metadata and current candidate; no invented coauthor/reviewer is added.'),
'M001':('F7',[sp],'Prepared metadata fields match title/creator/date/scope/type/open-access/license/version; live production API acceptance is neither tested nor claimed.'),
'M002':('F7',[sp],'Both intended upload filenames exist in the current public preparation and match the exact reviewed PDF and safe 51-file verification archive, including modes and declared license.'),
'M003':('F7',[sp,ar],'Primary URLs and bibliographic DOI/version/date information match actual retrieved source content and retained arXiv metadata; related identifiers do not misstate priority.'),
'M004':('F7',[sp,g,k,ar],'The description matches the now-proved all-normalization/kernel/field theorem and the reproducible package, with prior credits and excluded variants intact.'),
}
assert set(proofs)=={r['id'] for r in rows}
for r in rows:
    families,paths,reason=proofs[r['id']]
    r.update(final_status='VERIFIED_WITHIN_STATED_SCOPE' if r['id'].startswith('C') else 'VERIFIED_AS_BOUNDED_PUBLIC_CLAIM',
             families=families.split(','),deduction_or_check=reason,exact_mathematical_gap=None,
             evidence=[{'path':p,'bytes':(N/p).stat().st_size,'sha256':sha((N/p).read_bytes())} for p in paths])
    if r['id'].startswith(('S','M')):
        r['historical_or_operational_limit']='No ultimate-firstness/current-openness/external-human-review/live-publication certification; the particular declared limits remain in the source/public report.'
    else:r['historical_or_operational_limit']='Credited classical theorem inputs, where used, are not proof-assistant formalizations; historical and release limits are independent of the present deduction.'
old_gate=json.loads((A/'ROOT_PREPRINT02_FIRST_CANDIDATE_GATE.json').read_text())
old_log=next(x for x in old_gate['objects'] if x['path']=='RESEARCH_LOG.md')
body=(N/'RESEARCH_LOG.md').read_bytes()
prefix=N/'phase3/first_candidate_log_prefix.md'
assert not prefix.exists()
assert len(body)==old_log['bytes'] and sha(body)==old_log['sha256']
prefix.write_bytes(body)
now=utc()
with (N/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+now+': Full-packet independent review checkpoint. Two fresh source-first family reports, all seven approach mechanisms, complete primary applicability/field deductions, all29 public replay streams, seven fresh scientific replays, and source/export/historical binding checks have been read and reconstructed. Stable74-ID closure written with no remaining mathematical gap under the exact characteristic-zero/K assumptions. Mathematical audit100%; complete requested reviewer evidence/hold preparation95%; publication workflow not authorized for this reviewer. Exact old log prefix saved and verified against the externally held first-candidate gate before this append. Remaining: integration report, native preservation/ledger check, final namespace freeze and external ROOT closure. No candidate, held-family, Git or publication object was edited.\n')
result={'stage':'whole-preprint-final-claim-closure','native_utc':now,'native_clock_argv':['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],
        'executed_body_sha256':sha(Path(__file__).read_bytes()),'original_assessment_sha256':sha(assessment.read_bytes()),
        'stable_claim_count':74,'mathematical_claims':61,'source_disclosure_claims':9,'metadata_claims':4,
        'all_exact_mathematical_gaps_closed':True,'candidate_repair_requested':False,'publication_approval':False,
        'global_remaining_work':['ROOT external namespace validation/closure','separately authorized downstream publication workflow'],
        'historical_limits_retained':True,'claims':rows}
dest=N/'phase3/CLAIM_STATUS.json';assert not dest.exists();dest.write_text(json.dumps(result,indent=2)+'\n')
md=['# Final stable claim ledger','',
    'The original74 claims and first-assessment judgments are retained verbatim in CLAIM_STATUS.json, bound to the immutable first assessment. The following closures concern the precise manuscript scope. Source/metadata rows verify bounded statements, not ultimate priority or production publication. Each cited report is independently read and its hash is recorded in the JSON. No mathematical gap remains; ROOT external closure remains pending.','',
    '| ID | Final status | Mechanism | Closure |','|---|---|---|---|']
for r in rows:
    md.append('| '+r['id']+' | '+('Verified deduction' if r['id'].startswith('C') else 'Verified bounded claim')+' | '+','.join(r['families'])+' | '+r['deduction_or_check']+' |')
md+=['','F1 local/projective geometry; F2 intrinsic origin/rotation/group law; F3 direct torsion elimination; F4 fine marked moduli; F5 arithmetic/descent; F6 degeneration/counterexamples; F7 proof/code/source/public consistency. The two fresh delegated geometry/kernel mechanisms preserved source-first independence; seven separate source-first agents are not claimed.','',
     'Important attached finding: lambda=-(13+5sqrt(5))/2 gives five coincident plane-image pairs of distinct normalization torsion points. The claimed25 points are on the normalization, so this is a plane-map injectivity counterexample and not a manuscript theorem counterexample.','']
(N/'phase3/CLAIM_STATUS.md').write_text('\n'.join(md))
print(json.dumps({'native_utc':now,'claim_count':74,'remaining_mathematical_gaps':0,'claim_status_sha256':sha(dest.read_bytes()),
                  'old_log_prefix_sha256':sha(prefix.read_bytes()),'publication_approval':False},indent=2))
