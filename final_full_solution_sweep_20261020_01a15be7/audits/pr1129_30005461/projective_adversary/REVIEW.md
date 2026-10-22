# Fresh independent projective adversarial review: PR1129

Review date: 2026-10-21 UTC. Problem 30005461 / OWR-12697710-007.
Immutable head: `26fed29c1130e539ba018a37200f133870f0e036`; base: `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`.

**Verdict:** I found no substantive mathematical defect in the projective proof that, for every fixed real c<3, all sufficiently large odd powers of f_c=x^4y^2+x^2y^4+1-cx^2y^2 are SOS. The argument proves the complete coefficient-threshold limit c_k→3. This conclusion imports Scheiderer's published projective theorem and standard projective-space cohomology. It does not certify priority, an explicit SOS decomposition, or publication readiness.

This is a fresh AI adversarial review, not independent human peer review or formal proof-assistant verification. No original/historical verification program was executed. No provider, PR, spreadsheet, Git index or ref was modified. All child-created artifacts stay in this review folder. The parent's live duplicate check preceded this review; I did not independently query the ledger. The first, mixed-exponent clause and priority are separate review families, not findings to be inferred from this mathematical verdict.

## Exact target recovered from the primary original

The [EMS original report](https://ems.press/content/serial-article-files/47007?nt=1), Reznick's contribution at printed pp778–780, defines the threshold by

{c∈R : (x^4y^2+x^2y^4+1-cx^2y^2)^(2k+1) is SOS}=(-∞,c_k],

with c_k∈[0,3), and asks its limit. The same page separately conjectures the mixed odd-exponent implication. Its later positive-definite perturbation M+c(x²+y²+z²)³ is a different family. I read the complete contribution and visually inspected printed p780 / physical PDF p40. The actual head's PROOF.md and MATHEMATICAL_AUDIT.md were read in full, along with README and source records. No QUEUE status, historical acceptance flag, count of checks, or no-novelty disclaimer was treated as proof.

The full mathematical claim examined here is ∀c∈R with c<3, ∃m₀(c), ∀odd m≥m₀(c), f_c^m is a finite sum of squares in R[x,y]. The needed conclusion is not merely a subsequence, a multiplier certificate, a rational SOS, or a result for a positive-definite ternary perturbation.

## Imported theorem: actual primary version and role

The fresh [Scheiderer arXiv primary manuscript](https://arxiv.org/pdf/1104.1772v1) contains Sections2.4–2.5, the complete Theorem4.1 proof, and Corollary4.2. I read them, plus Remark4.8, and visually inspected pp9 and11. Its byte identity differs from the historical author PDF, whose host repeatedly timed out. The [publisher abstract](https://link.springer.com/article/10.1007/s00229-011-0484-3) independently confirms the same theorem and publication identity.

Corollary4.2 applies to a reduced projective real scheme X with no one-dimensional irreducible component and with Zariski-dense real points. For invertible L,M, M ample, and everywhere strictly positive sections f∈H⁰(X,L²), g∈H⁰(X,M²), it gives f g^N as a sum of squares of global sections of L⊗M^N for **every sufficiently large integer N**. Smoothness and normality are not hypotheses. Positivity is measured in a local square trivialization, not an arbitrary choice of sign for a line-bundle fiber.

The proof obtains an auxiliary totally-real reduced section h, uses a local-global criterion on an affine open, clears powers of g, and divides every square root by h before cancelling h². Its initial reduction applies the even-power statement to f and fg, covering both parities of N. Thus the corollary has no retained h², extra positive multiplier, or unmentioned parity restriction. Foundational results cited inside this published proof are imported, not reproved by this review. Remark4.8 explicitly prevents the invalid shortcut from affine strict positivity alone.

## Independent reconstruction and attempted failures

Write S=Proj R[A,B,C,D]/(G), G=ABC-D³, and H=O_S(1).

1. **Integrality and dimension, despite singularities.** Regard G as a polynomial in C over the UFD R[A,B,D]. Its two coefficients AB and -D³ have gcd1, so G is primitive. Over the fraction field it has degree1 and is irreducible. Gauss's lemma makes G irreducible in R[A,B,C,D], and an irreducible in this UFD is prime. Consequently S is integral, reduced, and a projective surface, with its sole irreducible component of dimension2. The curve-component exclusion is met. The gradient (BC,AC,AB,-3D²) vanishes on S precisely at the three coordinate vertices [1:0:0:0], [0:1:0:0], [0:0:1:0]. These singularities do not invoke a smooth-surface theorem.

2. **All real points, including every sign chart.** On D≠0, normalize D=1. The equation becomes ABC=1, with coordinate ring R[A^±1,B^±1] and real parametrization (a,b,(ab)^-1), a,b≠0. Any Laurent polynomial vanishing on all such real pairs becomes an ordinary polynomial vanishing on a nonempty Euclidean open after multiplication by a monomial; it is zero. Hence these real points are Zariski dense in this nonempty open chart. The chart is dense because S is integral. Thus S(R) is Zariski dense. No assumption A,B,C≥0 occurs: four sign chambers with ABC>0 are present after this normalization. Representatives with D<0 are equally allowed before normalization.

3. **Strict positivity as a section.** Let q_c=A²+B²+C²-cD²∈H⁰(S,H²). At any real nonzero representative, AM–GM on the three nonnegative squares gives

A²+B²+C² ≥ 3(A²B²C²)^(1/3) = 3D².

When D≠0 and c<3, q_c≥(3-c)D²>0. When D=0, q_c=A²+B²+C²>0, since the representative is nonzero. This explicitly covers boundary lines and the three singular vertices. On any coordinate chart T≠0, T generates H and q_c/T²>0, so this is precisely the source's square-line-bundle positivity. The restriction H of O_P³(1) is invertible and very ample even at singular points. All theorem hypotheses are now verified over the usual real numbers, including arbitrary fixed real parameter c.

4. **Parity and quantifiers.** Put X=S, L=M=H, f=g=q_c. For every sufficiently large integer N the theorem gives

q_c^(N+1)=Σ_j s_j², s_j∈H⁰(S,H^(N+1)).

Select **even N** and write m=N+1. Every sufficiently large odd m is obtained, not only selected odd exponents. Square-root degree is m; the squared section lies in H^(2m). Taking odd N instead would give an even power and miss the question. Even if one retained only a single sufficiently large odd m, all larger odd exponents follow by multiplication with the square (q_c^r)²; there is no issue of a sparse subsequence. Dependence of the cutoff on c is allowed and essential to the statement proved.

5. **Lifting sections: no projective-normality shortcut.** The exact cubic hypersurface sequence on P³_R is

0→O(t-3) --G→ O(t)→i_*O_S(t)→0.

[Stacks Lemma30.8.1](https://stacks.math.columbia.edu/tag/01XS) gives H¹(P³_R,O(t-3))=0 for every integer t; its proof computes the Cech complex and intermediate cohomology. Therefore restriction in degree t≥0 is surjective and its kernel consists exactly of G times homogeneous polynomials of degree t-3, with negative degree meaning zero. Apply this at t=m to lift every s_j to a real homogeneous polynomial H_j of degree m. Apply exactness at t=2m to the equality of sections. It yields the polynomial identity

q_c^m - Σ_j H_j² = G K

for a homogeneous real K of degree2m-3 (or K=0 if that degree is negative). The equality is in the coordinate ring, not merely at real points. Nothing here assumes smoothness, normality, or eventual surjectivity without a bound. The all-twist vanishing handles even the small negative twists t-3=-3,-2,-1. The ordinary projective embedding, not a weighted Proj, ensures O(1) is invertible.

6. **Exact substitution and basepoints.** Define a homomorphism of polynomial rings by

(A,B,C,D)↦(x²y,xy²,z³,xyz).

It sends G to x³y³z³-x³y³z³=0 and q_c to M_c=x⁴y²+x²y⁴+z⁶-cx²y²z². Substitution in the exact identity gives

M_c^m=Σ_j H_j(x²y,xy²,z³,xyz)².

Each root is homogeneous of degree3m. This step is polynomial evaluation, valid for every triple x,y,z. The associated rational map has basepoints [1:0:0] and [0:1:0], but no global projective morphism is asserted or needed. At these points all four substituted cubics vanish, as do M_c and every root because m>0. There are no denominators to cancel or exceptional points to omit. Setting z=1 gives the required affine SOS identity.

7. **Boundary values and threshold inference.** For c≤0, f_c is already SOS as (x²y)²+(xy²)²+1²+(sqrt(-c)xy)², consistent with the theorem. For every c<3 the argument above gives admissibility for all sufficiently large odd exponents. If c>3, f_c(1,1)=3-c<0, so an odd power cannot be SOS. Hence c_k≤3, while every fixed c<3 satisfies c≤c_k for every sufficiently large k. Given ε>0, take c=3-ε to obtain 3-ε≤c_k≤3 eventually. Thus c_k→3. At c=3, q_c vanishes at [1:1:1:1] and strict positivity fails. This proof supplies no affirmative endpoint claim; extending the theorem there would be invalid. No explicit exponent, uniform cutoff, or convergence rate is inferred.

Every attempted failure above was resolved by a universal argument. I found no unfilled mathematical step in this route under the imported theorem.

## Supplementary controls and their exact meaning

`check_projective.py` is independently authored. It checks exact monomial identities, the exponent-map rank and primitive relation, quotient monomial dimensions across small/large degrees, rational signed points and singular boundary cases, parity/degree bookkeeping, and every negative-exponent support pattern in the four-chart Cech complex over Q. This last check corroborates intermediate cohomology vanishing; the written/source proof supplies the universal theorem.

Deliberately wrong cubic relations, coefficient signs, parity and degree choices are rejected. Endpoint and above-threshold evaluations detect illicit extension to c≥3. These finite checks cannot produce an exponent or SOS certificate and are **not** the reason the universal theorem is accepted. No historical count was reused.

The packet is closed by `MANIFEST.json` with an externally supplied SHA256 in `SEAL.sha256`. `verify_offline.py` checks safe paths, closure, immutable bytes, exact claim/source bindings, and independently authored finite controls. It uses explicit guards, not Python assertions, and is tested under normal, -O and -OO modes. Its integrity checks do not turn hashes, byte identity, or an acceptance label into mathematical evidence. Fault-control results are in `VALIDATION_RUNS.json`.

## Disposition and limits

Recommend accepting the **mathematical correctness** of the projective coefficient-threshold argument. This family does not establish originality, absence of prior equivalent results, coverage of the optional real-delta appendix, a complete publication package, or a need to publish. Those remain with the root's separate audits. No material objection to the projective route remains from this fresh review.
