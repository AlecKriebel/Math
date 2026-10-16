# Complete-primary-source comparison: Goh 1992 and Problem 6.72

Review checkpoint: 2026-10-15 03:14:53 UTC. Assigned source audit: 100% complete, with authored outputs integrity-sealed. This is a bounded source comparison, not final package acceptance or a claim of historical firstness.

**Verdict:** No prior negative answer to either exact Problem 6.72 target was found or derived from the complete Goh 1992 paper. The source is now fully inspected. Its coefficient constructions and geometric proof steps have been compared, rather than excluding it merely because its named functionals differ. Goh supplies important applicable restrictions on a *second* supporting functional, but no contradiction to the candidate's single full-class maximization problem. The finite exact checks below all pass. Analytic inputs inherited from the classical literature remain explicit dependencies.

## Inputs and independence

The primary paper is Say Song Goh, *On the Two-Functional Conjecture for Univalent Functions*, Complex Variables 20 (1992), 197-206, DOI 10.1080/17476939208814600. PDF SHA-256: `94af0c114ce2ced1cb7f2337568c4ce0b8e0615c1ec32542f226d9bf177a0503`, 511209 bytes, eleven PDF pages including a publisher wrapper. All ten article pages, all intermediate displays/proofs, Brown examples, remarks, final reduction, acknowledgments and references were read; all ten rendered pages were visually inspected. The full source mechanism and hypotheses were recorded in `source_first.md` before the candidate proof, target, or prior reviews were consulted. Earlier source-review conclusions were not used.

The comparison then read the original archived `PROOF.md`, the current publication TeX as a historical input, and the original Hayman-Lingham Problem 6.72 text plus its page image. `compared_inputs.json` binds their hashes. The compared publication TeX was SHA-256 `c46d521e893a46466cf26b50c54294d1923e93dad4076e4b5dfa16c52d42830a`; future attribution edits do not invalidate the historical comparison but must not be misrepresented as this exact input.

Problem 6.72 asks whether the analytic arc omitted by a support point must have monotone argument, and whether the radius-tangent angle must be monotone. The candidate is stronger than an arbitrary formal slit: every full-class global maximizer of Re L for

    L=a2+i epsilon(a4-3a3), epsilon=10^-24,

has an actual omitted arc with nonmonotone continuous polar argument, signed outward radial angle, and ordinary unsigned angle. These are the exact comparison targets. Goh's introductory increasing-*modulus* property is not monotone argument or angle.

## Reconstruction and verification of the source mechanism

Goh's Theorem 1 uses the generalized Schiffer equation (2), with the coefficient polynomials P_j. For two independent equations it imports the Schaeffer-Spencer algebraic continuation mechanism and reduces to proving each continued branch has b1=1. Exact coefficient comparison gives b1^(n-1)=b1^(m-1)=1. The b2 elimination gives

    alpha(1-b1)=2a2(1-b1),
    alpha=((m-3)(lambda_(n-1)/lambda_n)
           -(n-3)(mu_(m-1)/mu_m))/(n-m).

The visually verified threshold is **|alpha|<=2 sqrt(2) or |alpha|>=4**. OCR is defective here. The strict support lower bound |a2|>sqrt(2) and the coefficient upper bound |a2|<=2 close these cases. The exact checker verifies the subtraction and denominator-free elimination polynomial identities, retaining n!=m and b1!=0 before division.

Theorem 2 handles a genuine degree-three equation together with a degree at least four, because the putative b1!=1 case would force L(f^2)=lambda2+2lambda3 a2=0. Theorem 3 handles equal degree after a real top-coefficient ratio has been established: normalizing and subtracting the *already valid* equations gives degree ell, so b1^(ell-1)=1, and the coprimality condition forces b1=1. Theorem 4 handles ell=3 by the beta=d2+2a2 d3 split. For beta=0, the actual finite tip forces a double root of an even quartic, which integrates to a rational map. The checker verifies its even-quartic factor identity and the differentiated rational integral identity. The remaining rational-support classification is cited, not reproved.

In particular, the same-degree results cover **all n=m=4 cases**, although the printed final corollary emphasizes n=m=5: for n=4, ell=2 or 3 and gcd(3,ell-1)=1. Same-degree n=3 and 5 are likewise covered. The explicit source remarks also extend applicable results to one global support equation and a second *full generalized Schiffer critical equation*. A freely chosen local trajectory is not such a second equation.

The source's Lemma 1 derives a real leading-coefficient ratio by comparing algebraic branches at infinity. Lemma 2 divides actual positive omitted-arc quadratic differentials and shows a common maximizer of L and cL has c>0. This positivity and common-maximizer hypothesis must not be discarded. The printed Brown corollary on p.201 omits repeating the standing essential-difference hypothesis: literally taking M=L would contradict compactness. Its sound use retains the paper's standing hypothesis. This audit does not claim to refute Brown's theorem or Goh's two-functional results.

## Exact application to the candidate

The source coefficient definition gives, independently,

    P2(s)=s,
    P3(s)=s^2+2a2 s,
    P4(s)=s^3+3a2 s^2+(2a3+a2^2)s.

For lambda2=1, lambda3=-3i epsilon, lambda4=i epsilon, the exact cubic is

    P_L(s)=a s+b s^2+c s^3,
    a=1+i epsilon(2a3+a2^2-6a2),
    b=i epsilon(3a2-3), c=i epsilon.

Thus the candidate differential is precisely Q(w)=-P_L(1/w)/w^2. Under w=-v^-2 it becomes

    Q(w)dw^2=4(a-bv^2+cv^4)dv^2.

This establishes the exact source-to-candidate normalization and sign bridge. No claim of sufficiency for arbitrary Q trajectories is used.

### An independent necessary-condition exclusion of every Koebe rotation

Let k_u(z)=z/(1-uz)^2, |u|=1. Plug its actual coefficients a_j=j u^(j-1) into Goh's full equation (2). Let C3 and C2 be the z^3 and z^2 coefficients of the residual LHS-RHS. Exact Laurent calculation gives

    C3=i epsilon(u^6+1),
    C2=-3i epsilon(u^4+1)+4u^-1 C3.

Therefore even a critical Koebe rotation for this L would require u^6+1=u^4+1=0. The exact Bezout identity

    (1-u^2-u^4)(u^4+1)+(u^2+1)(u^6+1)=2

rules this out. The calculation uses conjugate(u)=u^-1 and epsilon!=0. It does not depend on epsilon being small. The checker constructs the entire Schiffer residual and extracts both coefficients, rather than merely asserting phase conditions.

This independent conclusion is consistent with the candidate and with Goh. It shows why a supposed automatic second support would be an error: no maximizer of this L can be a Koebe rotation, so the source's two-functional theorems instead exclude the hypothesized second independent support whenever their degree hypotheses apply.

### Which source conclusions apply, and which hypotheses are missing

| Potential additional functional M | Applicable Goh conclusion | Consequence for this candidate |
| --- | --- | --- |
| Genuine degree 2, simultaneously globally supporting | The introduction's trivial degree-2 case / coefficient equality | Would force Koebe, hence impossible. |
| Genuine degree 3, simultaneously supporting (or under the stated support/critical extension) | Theorem 2 and final remark p.205 | Would force Koebe, hence impossible. |
| Genuine degree 4, not a complex multiple | Lemma 1 requires real top ratio; Theorem 3 covers ell=2,3 | A common support is impossible. |
| Complex scalar multiple cL | Lemma 2 | Only c>0 is possible; this gives no independent second equation. |
| Higher degree m with gcd(3,m-1)=1 | Schaeffer-Spencer case recounted and used by Goh | A common support would force Koebe, hence impossible. |
| Higher degree m>4, s=mu_(m-1)/mu_m | Theorem 1 with alpha=(3(m-3)+s)/(m-4) | Common support excluded in the theorem's two modulus ranges. |
| Higher degree m=7 and alpha in the unhandled annulus | No applicable complete theorem established here | This remains a genuine source-method gap, consistent with Goh's concluding n=4,m=7 example. |

The original full-class maximization of Re L supplies no additional M at all. Maximizing a sum does not imply maximizing its summands. In particular M=a2 and M=i(a4-3a3) cannot simply be declared common supports. The latter has the same normalized degree-4 penultimate coefficient as L, but ell=2, so Goh's Theorem 3 would force the impossible Koebe conclusion. Near equality in a2 is also not exact equality or a second Schiffer equation.

Dividing a functional by its complex top coefficient is valid as algebra within already established Schiffer equations, not as a replacement real-part objective. Here dividing by i epsilon gives a4-3a3-i epsilon^-1 a2. At the actual Koebe map Re L=2 while the normalized objective has real part -5; both objectives are zero at the identity. The order of these two members of S reverses. The checker verifies this exactly. Positive real scaling alone preserves the objective's order.

## Attempted priority collision through every actual source construction

The source's finite-tip beta=0 construction uses the *actual* omitted arc, but its conclusion is rational Koebe. Such a slit is a straight ray and has constant polar argument and zero outward radial angle. It cannot be either target negative. The beta!=0 branch also forces Koebe. The polynomial/coprimality constructions classify common supports and produce no new non-Koebe slit geometry.

Brown's cited degree-three examples are actual coefficient maximization problems with no extremal Koebe rotation for certain parameters; combined with Goh they show absence of an essentially different common maximizer. **Non-Koebe does not imply nonmonotone polar argument or radial angle.** Goh gives no conformal-map formula, actual tip bound, reversal sign calculation, or geometric conclusion for these examples. To check a direct route rather than dismissing degree mismatch, the simplest small imaginary degree-three perturbation a2+i tau a3 has the formal Koebe-limit pullback P=1+i tau(4-v^2), inverse first-order d=-2t+t^3/6, and q=d'-d/t=t^2/3. This has no leading-order sign reversal. The checker verifies these identities. This is only a local diagnostic: it neither proves global monotonicity for Brown's whole family nor refutes a source theorem. A route transferring the desired actual-slit reversal to an unproved Brown-family geometry assertion is blocked until new evidence supplies that missing assertion.

By contrast, the candidate's source-compatible cubic gives P0=-2-3v^2+v^4 and q=t^2-2t^4/5, with exact q(1)=3/5 and q(7/4)=-441/640. Its finite error controls and actual-tip separation are the additional mechanism needed for the target negative. Goh contains neither these identities nor an alternative actual target-negative construction.

The final section p.206 only passes from unequal-degree common supports to equal-degree common supports via L+M. It preserves the existing simultaneous-maximization assumption; it cannot manufacture it from one functional. Its preceding converse observation is likewise a conditional reduction. It asserts no angle or argument monotonicity and provides no hidden slit family. Complete-source inspection therefore found no verified collision with either exact target.

## Checks, limits, and integration recommendation

Run `python3 check_goh_candidate.py`. The script is pure standard-library exact rational/Gaussian-rational arithmetic, prints full JSON on stdout, reads no PDF or manuscript, and uses no absolute paths. Its 40 checks pass. Running it from an otherwise empty working directory produces byte-identical JSON (`portable_replay.json` equals `exact_checks.json`). The checked material includes source coefficient identities, the two-equation elimination, the quartic tip/integral algebra, the complete candidate Koebe residual diagnostic, the complex-normalization order reversal, low-degree case coverage, pullback signs, perturbation polynomials, exact endpoint signs, rational remainder absorptions, orientation bound, Rouché margin, and actual-tip radius separation.

These computations do not independently prove the source's imported Schiffer variation theorem, two-equation algebraic continuation, rational-support classification, Kirwan-Pell bound, Brown classification, or all of the candidate's global analytic continuation/trajectory identification. Source theorem proofs were followed and their finite algebra reproduced; external dependencies are not falsely promoted to independently formalized theorems. No local diagnostic has been used as a source-theorem refutation. No unique maximizer, closed extremal map, or complete slit classification is established here.

For integration, remove Goh 1992 from the manuscript's list of uninspected material and cite it as a checked two-functional classification. Suggested factual content: "Goh's coefficient two-functional theorems force Koebe under a simultaneous-support hypothesis, including all equal-degree-four pairs; they do not supply an actual omitted slit with either failure considered here." The parent should decide wording and package-level changes.

The human's 14 October instruction explicitly permits continuation without the unavailable Duren commentary and Hibschweiler 1995 source, accepts that priority cannot be fully cleared, and does not treat their disclosed absence as a publication blocker. This review honors that policy: it does not request those sources, revive a publication hold based only on their absence, certify historical firstness, or overlook a verified collision. None was found in this fully inspected source. Final package acceptance is outside this review.
