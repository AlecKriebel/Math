# Independent audit of the Fourier-kernel step in Lau, arXiv:2604.15042v2

## Finding

The identity between the integral of the real part and the integral of the absolute value on PDF p.28 is false under the paper's actual smoothing hypotheses. The ensuing printed argument does not justify the many-coordinate normalization by its stated uniform-error bound alone.

This is a substantive missing argument, rather than a harmless change of notation. However, a concrete replacement argument is supplied in `SECOND_KERNEL_REPAIR.md`: it preserves the exact one-coordinate Euler factors and controls the interaction correction in an absolutely summable algebra of nonnegative translations. Conditional on the preceding exact Euler-product/truncation formula (6.6), it recovers both (6.9) and Lemma 6.2's divisor-probability bound, with the original K and 8^s constant. That authored replacement has now been independently checked within its stated scope. The companion `SECOND_DISTINCT_OMEGA_CHAIN.md` supplies and verifies the restricted small-prime moment, the distinct-prime logarithmic barrier, and its fixed-epsilon consequence. None of these is a certification of the manuscript as a whole.

No assertion here says that Theorem 1.1, Theorem 1.3, or an Erdős problem is false.

## Source and inspection

Cheuk Fung (Joshua) Lau, *On the Number of Prime Factors of Consecutive Integers*, arXiv:2604.15042v2, dated 24 June 2026.

- Versioned public PDF: https://arxiv.org/pdf/2604.15042v2
- Public version record: https://arxiv.org/abs/2604.15042v2
- PDF: 37 pages, 717637 bytes
- PDF SHA256: `90443d4ebbdfe9e05052e1a8115b8acd9d29d3ce7269d7e9c71cb09716c718d1`
- The relevant displays on PDF pp.28–29 were visually inspected, not inferred solely from text extraction. PDF page numbers agree with the printed page numbers.

Scope inspected: the smoothing construction on p.20; the exact local Euler factors and truncation on pp.21–24; the approximations on pp.24–26; Lemma 6.2 on pp.26–29; the later coordinate cancellation on pp.30–32; normalization dependencies on pp.33–35; and the reduction statements in §5. This audit does not assert that every estimate in these sections is valid.

## 1. The actual hypotheses force strict inequality

Put h(t)=eta-hat(t) and

A(t,u)=(1+it)(1+iu)/(2+i(t+u)).

The construction on p.20 fixes eta: R -> [0,1], smooth, compactly supported in [-1,1], with eta(0)=1, and chooses it so that h is even and nonnegative. The Fourier normalization is h(t)=(1/(2pi)) integral eta(v) exp(itv) dv. Thus

h(0)=(1/(2pi)) integral eta(v) dv > 0.

Continuity makes h strictly positive on a neighborhood of zero. Its Gevrey decay makes all integrals below absolutely convergent.

Exact algebra gives

Re A(t,u)=(2+t^2+u^2)/(4+(t+u)^2)>0,
Im A(t,u)=(1+tu)(t+u)/(4+(t+u)^2).

The valid constant on pp.27–28 is

c0=integral_R2 A(t,u)h(t)h(u) dt du
  =integral_R2 Re A(t,u)h(t)h(u) dt du
  =integral_0^infinity [d/dv(exp(-v)eta(v))]^2 dv >= 1.

The imaginary integral vanishes by simultaneous sign reversal; its integrand does not vanish pointwise.

Let D=integral_R2 |A(t,u)|h(t)h(u) dt du. Then D>c0. Indeed choose any sufficiently small a>0 with h(a)>0. Along the diagonal,

A(a,a)=(1+ia)/2,
|A(a,a)|-Re A(a,a)=(sqrt(1+a^2)-1)/2 > 0.

Continuity gives a two-dimensional neighborhood of (a,a) on which both h factors and |A|-Re A are strictly positive. Elsewhere |A|-Re A is nonnegative. Integrating therefore proves the strict inequality. This is stronger than a pointwise example at t=u=1, because no assumption about h(1) is needed.

The final equality in the unnumbered display following the imaginary-part cancellation on p.28 identifies c0 with D and is therefore false. The initial imaginary-part computation also omits a minus sign before an intermediate imaginary-part expression; its final formula is correct. That sign typo does not remove the principal problem.

## 2. Why the printed absolute-value argument is insufficient

On p.29, the numerator bound takes absolute values in all K coordinate pairs and then replaces the resulting integral by c0^K. The actual absolute-value integral is D_H^K, where H=(log x)^0.2 and D_H is D truncated to [-H,H]^2. Since D_H -> D>c0, the direct replacement loses an exponential-in-K factor.

For the normalization, the uniform pointwise approximation (6.7), or the p.29 version for F_1, supplies an error inside a complex integral. The direct bound for a relative pointwise error epsilon_x=O((log x)^(-0.69)) is of size

epsilon_x (D/c0)^K,
K=floor((log x)^0.001).

For any fixed rho>1 and b>0,

(log x)^(-b) rho^K -> infinity,

because its logarithm is K log rho - b log log x. Thus the available sup-norm error, used in this way, does not imply a relative o(1) error after integration. This is an insufficiency of the estimate, not evidence that the actual arithmetic error has that magnitude.

Even conjugation symmetry does not fix an arbitrary sup-norm error. On a symmetric box let B=product_k A(t_k,t'_k), and take r=epsilon_x conjugate(B)/|B|. Then |r|=epsilon_x and r(-t,-t')=conjugate(r(t,t')); nevertheless integral rB product h equals epsilon_x D_H^K. Thus a structured property beyond symmetry and a uniform bound is genuinely needed.

The exponentially small truncation error exp(-c(log x)^0.1) is different: it does beat exp(O(K log log x)). It is not the obstruction identified here.

For fixed admissible k and s, the factor (D/c0)^K cannot be absorbed into a uniform constant times 8^s. Rescaling eta or the whole sieve weight changes numerator and denominator together and does not change D/c0. Simply renaming D as c0 would assign the wrong value to the signed leading integral.

Reducing K dramatically is not a local repair of the manuscript. The argument on p.7 uses log log x <=1000 log k when k>K and R_k=w. Replacing K by, for example, O(log log x) no longer supports that estimate near the transition.

## 3. Later uses and cancellation already present

- Lemma 6.2, pp.27–29: the false identity directly enters the absolute-value numerator bound and the justification of normalization (6.9).
- Lemma 6.3, p.30: (6.9) normalizes the small-prime moment. On p.31 the paper correctly notices that all divisor factors depend on one coordinate and integrates untouched coordinates. This is useful exact-main-term cancellation. However, the preceding frequency-dependent Euler-product remainder has been treated as though it could already be extracted from the complex integral; the displayed sup bound alone does not justify that operation.
- Lemma 6.4, p.33: explicitly uses (6.9) to convert an unnormalized arithmetic error into a probability error.
- Lemma 6.5, pp.34–35: requires comparison of the total mass with its arithmetic main term. Its proof is not separately certified by this kernel audit. Repairing the normalization does not automatically certify every signed inequality appearing there.
- Proposition 5.5 supplies the random-variable inputs for Lemma 5.3, Proposition 5.2, Proposition 5.1, and the announced main theorem. Theorem 1.3 is stated to follow by the analogous negative-shift argument. Therefore the source's downstream claims cannot be accepted solely by ignoring the normalization issue.

No later section in the inspected v2 supplies the translation-algebra estimate in the accompanying replacement argument. Section 7 concerns a different conditional problem and does not repair §6.

## 4. A replacement that keeps the necessary cancellation

The attached authored argument proceeds as follows.

1. The exact Laplace/Fourier identity identifies a coordinate with paired divisor factors as the L2 inner product of two right-translated finite differences of f=(exp(-u)eta(u))'. Right translations are contractions, so every extra paired divisor factor costs at most 4 in squared norm. The exact leading tensor integral is therefore at most 4^j c0^K/d, without D^K.
2. Write the exact Euler product as a product of single-coordinate factors g_k, times a coupling correction H_d. Approximate each g_k separately by C_k A, with uniform relative error O((log x)^(-0.7)). The total cost is (1+O((log x)^(-0.7)))^K=1+o(1), because each coordinate can be integrated separately before multiplying.
3. Expand H_d in absolutely summable nonnegative-translation monomials. For d=1, its distance from 1 in the coefficient norm is O(K^2/w)=o(1). With j divisor primes, its norm is at most exp(O(K^2/w+jK/w)) <=(1+o(1))2^j. No claim that jK/w=o(1) is needed.
4. Every monomial is controlled by the same translation contraction, uniformly in the translation lengths. This yields the required 8^j c0^K/d bound for the main numerator and (1+o(1))c0^K for the denominator. The previous truncation error is negligible at these scales.

The accompanying derivation spells out the exact local-factor factorization, the coefficient norm, the single-coordinate zeta comparison, the uniform shifted integrals, and the final error comparison. It is a mathematical replacement for the missing step, not a claim that the printed identity becomes true.

## 5. Acceptance boundary

Established by this audit:

- The printed L1 identity is false for every fixed eta satisfying the stated hypotheses.
- D>c0 follows from those hypotheses without a numerical approximation.
- The printed many-coordinate sup-norm error argument is insufficient.
- The exact main term has a valid finite-difference contraction argument.
- A detailed structured replacement for normalization and Lemma 6.2 has been independently checked.
- The prerequisite exact CRT/Fourier formula is separately verified in `SECOND_DISTINCT_OMEGA_CHAIN.md`, §2.
- The needed small-prime factorial moment is proved for the fixed A=10, r=ceil(4 log k) range in that companion, §4.
- The corrected distinct-omega logarithmic barrier and one fixed positive-epsilon barrier follow by the fully supplied moment, union-bound, endpoint, and infinite-witness arguments.

Not established by this audit:

- Validity of all arbitrary-A ranges of Lemma 6.3, Lemmas 6.4–6.5, or the manuscript's prime-power moment estimates.
- The full multiplicity-counting Omega versions of the main theorems.
- The coefficient-1 version of Erdős problem #413.
- Absence of a later public correction: this audit is pinned to the supplied v2 PDF rather than a new literature-status search.

## Final bounded disposition

Accept the corrected distinct-omega logarithmic result and its fixed-positive-epsilon consequence as a reconstructed consequence of the prior sieve argument. Keep the original coefficient-1 barrier unresolved. Keep the stronger Omega claim outside this acceptance. The p.28 printed identity remains false; acceptance rests on the supplied replacement, not on reinterpreting that identity.

## Publication-edition scope clarification

This is the complete earlier distinct-only review, retained at its original
mathematical scope. The separate SECOND_MULTIPLICITY_AUDIT.md extends that
acceptance to the full corrected backwards omega<=Omega logarithmic theorem,
using fixed A=100 and s=ceil(4 log k). Its all-endpoints fixed-positive-epsilon
consequence is also accepted. Earlier statements that the full Omega theorem
is outside this document's acceptance describe this document alone; they are
not the final disposition of this edition. Coefficient one remains unresolved.

All mathematical acceptance here is independent internal AI review of the
specified authored arguments. This AI-assisted work is unrefereed; no external
human peer review, journal acceptance, or formal proof-assistant certification
is claimed. No novelty claim is made.
