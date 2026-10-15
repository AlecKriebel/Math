# Separate audit of ROOT's complete least-period classification candidate

**Verdict: conditional mathematical PASS; no substantive defect identified.** Under the stated canonical parametrization and standard Jacobi analytic facts, ROOT's argument proves that, for a noncircular outer ellipse and a strictly nested nondegenerate confocal elliptical caustic, either fixed-focus ordinary distance product is phase-independent **if and only if the least period is $2\pmod4$**. Every positive number of repetitions preserves constancy and nonconstancy exactly. This is a later, separate review; the original independent report is preserved unchanged.

Candidate SHA-256 at review: `f772d2067059fa1d8af2e59688147fb465e0f26327a68f07c67354a614e7c32a`.

## Claim, inputs, and scope

Assume $a>b>0$, $c^2=a^2-b^2>0$, a strict positive-minor-axis confocal caustic, modulus $0<k<1$, and

\[
P(u)=(-a\operatorname{sn}u,b\operatorname{cn}u),\qquad
\delta=2v=4K\tau/n,
\]

with $0<v<K$, $\gcd(\tau,n)=1$, $0<\tau<n/2$, and the canonical axes relations. The ordinary distances are exactly $g_+=a+c\operatorname{sn}u$ and $g_-=a-c\operatorname{sn}u$, both positive for real $u$. The elementary distance identity is independently derived in the earlier report.

The analytic input needed for this extension is the full-sn torus $\Lambda_0=4K\mathbb Z+2iK'\mathbb Z$: each $g_\pm$ has simple poles at $p=iK'$ and (p+2K); $g_-$ has zeros at $p+K\pm v$, and $g_+$ has zeros at $p-K\pm v$. The nonzero coefficient (c) prevents removal of the sn poles. In each case the two displayed zeros are distinct and nonpolar for $0<v<K$, and two simple poles force total zero degree two. Hence they exhaust the divisor and are simple. These facts were logically checked here against the supplied formulas, but the cited source identities themselves remain the separate source audit's responsibility.

## Independent odd-period argument using torsion

This proof read uses a torsion obstruction instead of the candidate's integer-parity congruence.

On the full-sn torus let $H=\langle\delta\rangle$, an order-(n) subgroup, and $T=2K$, a nonzero point of order two. For odd (n), Lagrange's theorem gives $T\notin H$. Thus the pole orbits (p+H) and (p+T+H) are disjoint.

For any initial zero offset $z=\pm K\pm v$,

\[
2z=T\pm\delta\pmod{\Lambda_0},
\]

because $-2K\equiv2K$. If the zero orbit met either pole orbit, then $z\in H$ or $z\in T+H$. Doubling either inclusion would imply $2z\in H$, since $2T=0$. But $T\pm\delta\notin H$. This is a contradiction. It applies to both foci and every primitive odd-period rotation, including even turning numbers.

Consequently each full product has (2n) uncancelled simple poles and is a nonconstant meromorphic function. The two initial zeros differ by one step, so the product has one zero orbit with double multiplicity; this does not affect the pole obstruction. There is no assumption that the two translated zero orbits remain distinct.

This settles the odd-period family universally **conditional on the stated analytic divisors**, rather than only at the exact three-period counterexample.

## Even periods and real nonconstancy

For $n=2m$, primitivity makes $\tau$ odd. The half-step is antipodal, and the two ordinary focal products are equal to the norm of $F=a^2-c^2\operatorname{sn}^2u$ on the smaller $2K$-period torus. The independent subgroup/coset lemma in the earlier report shows:

\[
\text{complete norm cancellation}\iff m\text{ is odd}.
\]

If (m) is odd, the complete divisor is zero and compact-torus holomorphy gives a constant. If (m) is even, the two zero cosets are disjoint from the pole coset. The norm has (m) uncancelled double poles on the smaller torus, hence is nonconstant.

No translated pole lies on the real phase line: its imaginary coordinate is an odd multiple of $K'>0$. If a meromorphic product were constant on all real phases, its difference from that constant would have zeros accumulating in a neighborhood with no poles. The identity theorem on the connected complex domain would force the meromorphic function to be constant, contradicting its exhibited poles. Thus the argument proves **real-family nonconstancy**, rather than only complex nonconstancy. Positivity also makes all real focal products finite and removes any ambiguity from taking lengths.

## Repetitions and exceptional boundaries

For an (r)-fold traversal the focal product is exactly (D_n(u)^r). Since (D_n(u)>0) on real phases and $r\ge1$, the map $x\mapsto x^r$ is injective there. Repetition therefore preserves constancy in both directions. Independently, its complex divisor is (r\operatorname{div}$D_n$), so nonzero pole divisors cannot disappear by repetition.

For a nominal return length $N\equiv2\pmod4$, a least period dividing (N) is either odd or $2\pmod4$; a least period divisible by four cannot divide such (N). The extension therefore correctly distinguishes admissible repeated even families from doubled odd families. The exact doubled-triangle counterexample in the original report supplies a concrete test of the latter failure.

Circles have $c=0$, making every distance to either coincident focus equal to (a); they are a separate constant case. The noncircular iff claim expressly excludes them. A primitive $n=2$ is impossible under $0<v<K$; hyperbolic or degenerate caustics are outside scope. Reversing orientation permutes the factors and changes no product.

## Exact computational falsification controls

The separate standard-library script `classification_checks.py` performs **12,808 exact assertions** over **580 primitive rotations** with $3\le n\le61$:

- 394 odd-period rotations;
- 95 rotations with $n\equiv0\pmod4$;
- 91 rotations with $n\equiv2\pmod4$.

For both focus signs it inventories poles and zeros on the full denominator-(4n) grid. It checks the predicted constancy class, total degree, the odd-period uncancelled (2n) simple poles and (n) double zeros, the even excluded (n) double poles on the full torus, and exact divisor scaling for repetitions $r=2,3,4$. Every assertion passes. These finite inventories condition on the analytic pole/zero locations; they do not establish them by sampling.

No extra numerical diagnostics were necessary: the preserved exact geometric controls already establish same-caustic nonconstancy for primitive periods three and four, plus admissible six-period examples. The earlier 560 reflected-ray diagnostics provide additional selected-family support for the even admissible part.

## Strongest result and remaining gap

The later candidate survives this independent proof read and exact falsification checks. The odd-period torsion obstruction, even-period coset obstruction, real identity-theorem step, and repetition argument have no identified logical gap under the explicit canonical/Jacobi inputs. It is mathematically stronger than the authenticated submission and should be identified as a separately derived extension with its own review record.

The remaining gap is source verification of the analytic inputs and priority review. This agent has not reclassified the extension as novel or independently source-certified. Original `REVIEW.md` SHA-256 remains `ca1ed7216584399c39d5f31e015c0c59bec0ee347dd259e320ce55afa53d25f4`.

Assigned classification addendum completion: **100%**. This percentage describes completed audit work, not a probability of theorem truth or a claim that all independent source/priority work is finished.
