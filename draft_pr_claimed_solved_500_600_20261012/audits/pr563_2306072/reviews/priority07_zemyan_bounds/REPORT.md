# Zemyan 2005/2007 differential and angle family: bounded priority audit

## Verdict

**Source-scoped exclusion of an earlier verified negative answer in these two articles.** Complete article text, proofs, examples, remarks and references were read. The key equations and angle definitions were checked visually against the supplied PDFs. Neither article constructs or proves the existence of an actual support point whose polar argument or ordinary unsigned radial angle is nonmonotone. Neither supplies the candidate's fourth-degree perturbation mechanism, its quantitative actual-tip estimate, or its all-global-maximizers argument.

This is not a historical-first certificate, a complete literature search, or publication clearance. A quoted assertion about an earlier cited construction is not an audit of that construction. The full Zemyan 2003 construction, other cited papers, and any later work require their own source comparisons. The strongest verified result here is the exclusion of an earlier negative global target from the **contents of the two identified complete articles**, plus checkable derivations distinguishing their angle variables and necessary restrictions from the candidate.

The papers are Stephen M. Zemyan, *A New Approach to Support Point Theory for the Class S*, Computational Methods and Function Theory 5 (2005), 1-17, DOI 10.1007/BF03321083, and *On the behavior of the omitted arc of a support point of the class S*, Complex Variables and Elliptic Equations 52 (2007), 175-181, DOI 10.1080/17476930601065169. The exact supplied-file hashes, physical pagination and full input hashes are in `SOURCE_IDENTITY.json`; reading coverage is in `SOURCE_COVERAGE.json`.

## Target and chronology of this comparison

Hayman-Lingham's original Problem 6.72, printed p.143 / physical PDF page144, asks whether the analytic arc omitted by an actual support point has monotonic argument and whether the angle between radius and tangent vectors is monotonic. The source states that the second property implies the first and records positive results for point-evaluation support points. The 2018 update reports no progress reported to its authors. That is a statement about that edition, not evidence of the problem's status in 2026.

The frozen original `PROOF.md` and current `publication/support_slit.tex` assert that every global maximizer on normalized S of

\[
\Re\{a_2+i\varepsilon(a_4-3a_3)\},\qquad \varepsilon=10^{-24},
\]

has nonmonotone polar argument, signed outward radial angle and ordinary unsigned radial angle. The independent source inventory was saved in `INDEPENDENT_DERIVATION.md` **before** these candidate files were read. No older audit/family report was read or used. The candidate files were read only after the source assertions and positive examples had been recorded.

The candidate establishes an actual maximizing f by compactness and nonconstancy, not by solving a trajectory and declaring it extremal. Its second major step identifies a constructed trajectory segment with the actual slit using a tail at infinity, local uniqueness and a quantitative bound on the actual tip. These steps distinguish it from the two source papers' bounds conditional on already-known support membership.

## Angle variables and invariance

Let w be oriented outward, with r=|w| strictly increasing. Use continuous argument lifts

\[
\theta=\arg w,\quad \phi=\arg w_r,\quad
\beta=\phi-\theta,\quad \alpha=|\beta|.
\]

On a support slit the acute tangent-line/radial-line angle is alpha; in the regular interior |beta|<pi/4. The ordinary angle between outward tangent and radius vectors agrees with alpha. Reversing the tangent gives its supplement, which preserves nonmonotonicity. Positive orientation changes multiply derivatives by positive factors; changing a continuous lift by 2pi changes no monotonicity verdict. Inward parameterizations reverse the signs but preserve a sign reversal.

The exact identities

\[
w=r e^{i\theta},\quad \frac{w_r}{w}=\frac1r+i\theta_r,
\quad \beta=\arctan(r\theta_r),\quad
\theta_r=\frac{\tan\beta}{r},\quad \phi_r=\theta_r+\beta_r
\]

show that a wiggle (a sign change of theta_r) is a **sign change of beta**, whereas a waver is a sign change of phi_r. A waver is neither a sign change of beta nor a sign change of beta_r. The papers define G by wiggles and V by wavers, not by unsigned radial-angle extrema.

For an explicit check of logical insufficiency, prescribe beta(r)=atan(delta/(1+r^2)), delta=1/1000. Then beta and alpha are strictly decreasing and positive, theta_r=delta/[r(1+r^2)] is positive, but

\[
\phi_r=\frac{\delta(1-r^4+\delta^2)}{
r(1+r^2)((1+r^2)^2+\delta^2)}
\]

changes sign. This is an analytic radial prescription illustrating the logical distinction, **not** an actual support-point counterexample. Thus the introductions' citation of an existing tangent waver cannot alone settle either target question. The exact derivative identity and rational signs are checked in `checks.py`.

## Complete positive-example and existence inventory

| Location | Exact source scope | Target implication |
|---|---|---|
| 2005 pp.1-2; 2007 pp.175-176 | Actual support points have increasing modulus, small radial angle and an asymptotic half-line; polar monotonicity is described as an open question in those papers. | These restrictions allow a bounded reversal; they are not constructions. |
| 2005 Example 1, p.12 | Koebe k=z/(1-z)^2 omits a radial half-line; G=V=empty. | Polar argument and radial angle are constant. |
| 2005 Example 2, pp.12-13 | Pearce p_xy=[z-(x+y)z^2/2]/(1-yz)^2, |x|=|y|=1, x!=y, is a support point under 0<|arg(-x/y)|<=pi/4 and omits a nonradial half-line. | No wiggle or waver. Polar argument is monotone and unsigned radial angle decreases to zero. |
| 2005 Remark 3.2, p.11 | A slight variation of a Pearce function is discussed heuristically; if two simple Z_r zeros persist for all radii sufficiently near1, the stated bound excludes wiggles. | A conditional no-wiggle statement, not a negative example or a verified support construction. |
| 2005 p.2; 2007 p.176 | Zemyan 2003 is cited for a support point with an interior tangent waver; N wavers is a conjecture. | No theorem about that example's polar argument or radial angle is given here. |
| 2007 p.176 | Full-class-S analytic slit maps with infinitely many wiggles/wavers are mentioned. They are explicitly contrasted with the class of support points. | No maximizing functional, support certificate or explicit formula is supplied; they cannot be promoted to target counterexamples. |

For a half-line w=u+s v with Re(v conjugate(w))>0,

\[
\theta_s=\frac{\Im(v\overline u)}{|w|^2},\qquad
\phi_s=0,\qquad
\tan\beta=\frac{\Im(v\overline u)}{\Re(v\overline u)+s|v|^2}.
\]

The numerator has constant sign and the denominator increases. This verifies the complete target exclusion for the Koebe/Pearce examples, including unsigned radial angle. A zero numerator gives the radial case.

The two nonlinear curves in the conjugate Pearce specialization satisfy cos(theta)=2r cos(arg x)/(1+r^2), **in the parameter disk**. They are portions of a Schwarzian level set, not curved omitted arcs. Confusing them with the geometric slit would produce a false positive. The formula contains four level-set arcs, while the omitted slit is straight.

## Differential bounds: exact claims and limits

The 2005 paper uses

\[
f^{\#}=\frac{|f'|}{1+|f|^2},\quad Z=\frac1{r f^{\#}},
\quad S_f=\frac{f'''}{f'}-\frac32\left(\frac{f''}{f'}\right)^2.
\]

Its Proposition2.1 gives kappa^2=1+r^2 Z_r^2/4, tau=r Z Z_rtheta/(4 kappa^2) and r Z_rtheta=Z Im(z^2 S_f). Proposition2.3 then identifies angular curvature critical points with lambda_r union Lambda_0, where lambda_r={Z_r=0} and Lambda_0={Im(z^2 S_f)=0}. These are statements about the image of an inner parameter circle and its stereographic projection. The circle's parameter angle is not the polar argument of the omitted arc.

Theorem3.1 **states**

\[
2+2\#G\le\#(\lambda_r\cap C_\rho)\le
\#(\Lambda_0\cap C_\rho)
\]

for rho sufficiently near1; the middle inequality is stated for every S and every rho. The middle inequality has a direct Rolle argument: between successive zeros of Z_r, nonconstant kappa starts and ends at1 and attains a larger maximum, whose derivative vanishes through Z_rtheta. Degenerate infinite/cardinality cases must not be treated as a finite bound. Even granting the full displayed source theorem, it bounds wiggles above; it does not deduce a wiggle from multiple level-set intersections.

The generic exact calculations independently confirm

\[
S_k=-\frac6{(1-z^2)^2},\qquad
S_{p_{x,y}}=-\frac{3(x-y)^2}{2(1-xz)^2(1-yz)^2}.
\]

Polynomial cross multiplication verifies these with symbolic x,y. The spherical/Schwarzian identity is also checked exactly at two Gaussian-rational disk points for identity, Koebe, a Pearce specialization and a small univalent quadratic. These finite checks supplement the derivative calculation; they do not prove every global support assertion.

Lemma4.1, using cited support coefficient inequalities, bounds |S_f(0)|=6|a3-a2^2| away from0. Theorem4.1 consequently gives four Lambda_0 arcs at right angles **near0**. Remark4.1 explicitly leaves their global continuation and extra boundary-to-boundary arcs for further investigation. Even its conditional four-intersections-everywhere scenario would only imply at most one wiggle, which allows the target negative example. The paper never proves the missing global zero-count condition for all support maps.

Remark3.2 supplies no functional, maximizing map or estimate uniform as rho approaches1 for the proposed Pearce variations. Compact-open convergence controls derivatives at each fixed rho but does not prove the required boundary-uniform root persistence. Replacing that gap by an unsupported uniform statement would transfer the difficulty. This route remains blocked as a construction mechanism unless materially new boundary or extremality evidence is supplied.

## Proof caveats found by adversarial algebra

**2007 tangent at infinity.** The proof on pp.178-179 sets g(tau)=tau w(tau) but uses g''/g' for the imaginary part of w''/w'. The correct identity is

\[
\frac{w''}{w'}=\frac{\tau g''}{\tau g'-g}-\frac2\tau.
\]

For w=1/tau+i+tau, w'=-1/tau^2+1 is real near0, while g''/g'=2/(i+2tau) has nonzero imaginary part. At tau=1/2 the correct ratio is real and the printed ratio has imaginary part -1. This is an exact formula error, not an adverse actual-support example. Since g(0)=d_-1!=0, the denominator tau g'-g is nonzero near0 and the imaginary part of the corrected expression is real analytic there. Its first nonzero Taylor coefficient gives eventual sign stability, or it vanishes identically. The qualitative finiteness mechanism survives this repair; it creates no global monotonicity or existence theorem.

**2007 endpoint parameter.** The proof on p.177 assumes a regular Taylor parametrization and also the normalized natural-parameter equation Q(w)(dw/dt)^2=1. A simple zero Q(w0)=0 yields w-w0 proportional to t^(2/3), rather than a finite nonzero natural-parameter derivative. Regular geometric and natural parameters must be distinguished. In the p.179 tip expansion, m must index the first nonconstant coefficient: w0 is nonzero by the quarter theorem, so literally taking the first nonzero coefficient would give m=0 and the displayed coefficient would be undefined. The real-analytic compact-subarc uniqueness lemma also needs infinitely many distinct zero points and may be applied after restricting to a conjugation-symmetric neighborhood. These are routine repairs to the cited mechanism, not evidence of an actual new support example.

**Stronger 2005 waver claim.** Remark3.1(e)-(f), pp.8-9, asserts a waver after the last wiggle and #G<=#V, citing a then-submitted paper. Published 2007 Theorem3.1, pp.180-181, states only the intervening-waver result, #G<=#V+1; it omits the post-last-wiggle assertion. The 2005 proof of the sharper count bound uses the stronger assertion, so this audit does not certify that step merely by referring to the later paper.

The claimed post-wiggle behavior does not follow from elementary analytic geometry. The exact analytic arc

\[
w(s)=-s+i\delta\left(1-\frac1{5s}\right),\quad
s\ge\tfrac14,\quad\delta=\tfrac1{1000},
\]

has increasing modulus, radial-angle magnitude below pi/4, and an asymptotic half-line, but

\[
\theta_s=\frac{\delta(1-2/(5s))}
{s^2+\delta^2(1-1/(5s))^2},\qquad
\phi_s=\frac{2\delta/(5s^3)}{1+\delta^2/(25s^4)}>0.
\]

There is one polar wiggle and no tangent waver. Its modulus derivative is positive because s>=1/4 makes 1-1/(5s)>0; its radial-angle tangent has absolute value at most delta/s<=1/250. Both derivative formulas are exact polynomial-identity checks. **This arc has no verified support membership and is not an earlier target counterexample.** It only isolates the gap in inferring the stronger assertion from geometry. The source's count theorem might admit another support-specific proof; no falsification for actual sigma is claimed. The source-scoped exclusion does not depend on accepting or rejecting that stronger bound.

## Reconciliation with the actual candidate

Coefficient extraction gives the candidate's exact differential

\[
Q(w)=-a/w^3-b/w^4-c/w^5,\quad
a=1+i\varepsilon A,\ b=i\varepsilon B,\ c=i\varepsilon,
\quad A=2a3+a2^2-6a2,\ B=3a2-3.
\]

This is a degree-four coefficient functional. The two Zemyan papers work in the full support class and offer no lower-degree coefficient classification excluding it.

The original and publication use |A+2|<106eta and |B-3|<24eta, eta=10^-12, so |A|<3, |B|<4 and |a|>1-3eps. Every omitted point has |w|>=1/4 by the Koebe quarter theorem. For r=|w|>=1/4,

\[
\frac{|b|r+|c|}{r^2}\le32\varepsilon<1-3\varepsilon<|a|.
\]

Thus Q has **no zero anywhere on an actual candidate slit**, including its finite tip. Also |b|^2<4|ac| implies the quadratic numerator aw^2+bw+c has two distinct roots, both inside |w|<1/4. They are formal simple zeros in the image region, not omitted endpoints. The 2007 simple-zero/natural-parameter caveat therefore does not invalidate this candidate. It remains important that an actual slit may stop at a regular Q-point; local trajectory extension beyond the actual tip is not an omitted-arc proof.

The candidate's original tip/segment separation addresses precisely that issue: its actual tip has radius<3/10, while its certified segment has |W|>25/81, with rational gap7/810. The publication additionally proves the segment orientation through Re(t V'/V)>0. The source papers cannot substitute a necessary-condition trajectory for this membership proof.

With the inward parameter t, the candidate uses Z=t V'/V, theta_t=-2 Im(Z)/t, beta=arg(Z), and

\[
Z=1+i\varepsilon q(t)+R(t),\quad
q=t^2-\tfrac25t^4,\quad |R|<2000\varepsilon\eta.
\]

The rational values q(1)=3/5 and q(7/4)=-441/640 have margins much larger than2000eta. Therefore theta_t has both signs, beta has both signs, and alpha=|beta| has an interior zero between positive endpoints. This is a polar wiggle and unsigned radial-angle failure, rather than a tangent-waver inference. The exact rational margins and angle ratio are independently checked here. This audit does not reprove all analytic remainder estimates or every classical support theorem.

Oddness of V makes W a Laurent series in tau=t^2: its leading term is -a/tau. This fits the repaired eventual-stability mechanism of the 2007 paper. Finite G and V do not impose G=empty; eventual behavior at infinity permits the candidate's bounded reversal. Near-zero Lambda_0 structure is likewise compatible: |a3-a2^2|>1-61eta>1/2, so S_f(0)!=0 and its four local Schwarzian arcs are expected. No global Lambda_0 intersection count for an actual candidate maximizer has been computed or asserted.

## Checkable artifacts and remaining gap

`checks.py` uses only Python's standard library, exact fractions and Gaussian rationals. Its 36 checks include generic polynomial identities, exact differential extraction, the printed/corrected 2007 formula discrepancy, angle distinctions, candidate reversal margins, root/endpoint exclusion and geometric diagnostics. `CHECKS.json` records every check. Re-run `python3 checks.py`, then `python3 verify_manifest.py` in this directory.

The manifest seals only authored notes, receipts and reproducible checking tools. Supplied copyrighted PDFs, extracted article text and rendered page images remain in ignored locations and are not included as publication artifacts. No canonical file, Git index, branch or remote was modified; no external individual was contacted. Publication integration is left to the parent process.

Exact remaining gap: no article inspected here supplies an earlier verified global target or an equivalent complete construction, but the **actual 2003 support construction and other referenced/full-source families must be checked directly** for beta/alpha behavior before any global priority decision. The source's stronger 2005 post-last-wiggle assertion and claimed boundary-uniform Pearce-variation persistence are not promoted to independently verified constraints. They are also not needed to exclude an earlier negative construction from these two complete articles.
