# PR #1150: adversarial review of the universal norm obstruction

**Verdict: PASS. No mathematical correction required within this family's scope.** The proof excludes every scalar in the original rational function field, accounts for all three kernel summands, and does not depend on an unwarranted perfect-residue-field assumption or a finite sample. This is a mathematical assessment, not a priority verdict or a whole publication-package review.

## Scope and independence

I read the single authorized candidate `inputs/COUNTEREXAMPLE.md`, 12,061 bytes, SHA256 `b1533a032e031d82a0d124cdb410e86e5ee59af477dd711d2157a5d72f36e2ca`. I did not read the previous audit, source audit, acceptance text, root review, sibling reports, or original PR discussion. The parent brief identified attack surfaces but gave no other review's result. I wrote `INDEPENDENT_CORE.md` before opening external theorem bodies. I sent the parent provisional/final mathematical findings; no parent response or sibling result was received before this report. Initial and final logs record UTC and completion estimates.

The assigned central claim is that, with the candidate's fields and class, every hypothetical three-summand decomposition produces an impossible norm condition. The candidate also contains hypotheses, differential identities, and a degree-one boundary statement; I checked their use as described below. I have not independently checked the original problem's printed statement or priority history, which belong to other review families.

## The full kernel reduction is valid

Let `a=s^{-1}`, `K=F(theta)`, `theta²+theta=a`, `f=1+beta² z`, and `M=L F(B)`. Work with the natural symbol identification `H_2²(E) ≅ Br(E)[2]`. Its displayed rule is `[u,v) ↔ u dlog(v)`; scalar extension commutes with this rule.

The entire relative Brauer kernel of a separable quadratic field extension is cyclic, with arbitrary scalar slot `c` in `F*`. This is not an assumption that arbitrary Brauer classes are single symbols. One can see the cyclic step directly: a normalized two-cocycle for the order-two Galois group is determined by its value `c` on the pair of nonidentity elements. The cocycle condition makes `c` invariant. A normalized coboundary changes it by `v sigma(v)`. The corresponding crossed product has basis `K ⊕ K j`, relations `j²=c` and `j d=sigma(d)j`; setting `i=theta` gives precisely `[a,c)`.

The general relative-Brauer/crossed-product theorem applies over arbitrary fields; characteristic two and imperfectness are allowed. I verified Milne's complete relevant construction and proof, not a local-field specialization. Details of the inspected version and pages are in `SOURCE_READ_RECEIPT.json`.

Consequently, if `xi=x+y+w` with the three stated summand memberships, `y=[a,c)` for some `c ∈ F*`. On restricting to `M`, `x` vanishes because `L ⊂ M`, and `w` vanishes because `F(B) ⊂ M`. The verified differential calculation gives `xi_M=[a,f)`. Thus `[a,f/c)_M=0`. Scalar extension to `D=k'((s))` preserves this zero class. There is no missing third summand and no claim that membership in only two kernels suffices.

For completeness, the cyclic norm criterion also has a short proof here. If `c=N(v)`, the crossed product acts on the two-dimensional base-field vector space `K`, with `K` acting by multiplication and `j` acting by `v sigma`; this identifies it with the full endomorphism algebra. Conversely, in a split crossed product the embedded quadratic field makes its two-dimensional module a one-dimensional `K`-space. Its `sigma`-semilinear operator `j` is `v sigma` in a `K`-basis, hence `c=j²=N(v)`. Irreducibility of the Artin–Schreier polynomial ensures the needed quadratic algebra is a field. The official Voight theorem independently confirms exactly this criterion in characteristic two.

## An explicit norm computation removes the ramification concern

The candidate's extension `T=D(theta)` is genuine: a negative `s`-valuation of `x²+x` is even, whereas `s^{-1}` has valuation `-1`. Put `pi=theta^{-1}`. Multiplying the defining relation by `s pi²` gives

`pi²+s pi+s=0`, `sigma(pi)=pi+s`, and `N(pi)=s`.

The polynomial is Eisenstein. Thus the candidate's total ramification, unchanged residue field and absence of defect are correct: the ramification degree is already two, consuming the full field degree. Its valuation normalization `v_D(N(h))=v_T(h)` is consistent with residue degree one.

There is also a direct proof that avoids relying on any general defect statement. Every element of `T` is uniquely `A+B pi`, with `A,B ∈ D`. Multiplying by its conjugate gives the exact identity

`N(A+B pi)=A²+sAB+sB²`.

For finite `u=v_s(A)` and `v=v_s(B)`, the first and third terms have valuations `2u` and `1+2v`. They have opposite parity and cannot tie. The middle term has valuation `1+u+v`, strictly larger than their minimum: if `u≤v` it is at least `2u+1`; if `u≥v+1` it is at least `2v+2`. Therefore

`v_s(N(A+B pi))=min(2u,1+2v)`.

The cases `A=0` or `B=0` follow immediately from the same norm formula. A norm of valuation zero must have `v_s(A)=0` and `v_s(B)≥0`. Its residue is then the square of the residue of `A`. This is valid over the actual imperfect residue field; there is no finite-field replacement, surjectivity assertion for residue norms, or assumption that the norm of a nonunit cannot be a unit without proof.

Now take *any* nonzero `c ∈ k(s)`, including negative valuation and arbitrary rational denominators. It has a Laurent leading term `s^r c0` with `r ∈ Z`, `c0 ∈ k*`. If `f/c=N(h)`, multiplying by `N(pi^r)=s^r` gives the unit norm

`u=s^r f/c=f/(s^{-r}c)`.

Negative `r` is allowed because norms are defined on all of `T*`. Its residue is `f/c0`, so the previous calculation forces `f/c0 ∈ k'^{*2}`. The sign of the exponent used in the candidate's normalization is correct.

## The residue contradiction covers every rational scalar

Write `x=beta²`, `y=z²`, `tau=gamma²`. These are algebraically independent. Then

`S=k'²=F2(x,y,tau)`, `R=F2(x²,y,tau)`, and `k=R(z)`.

The extension `k/R` has degree two, so each `c0∈k` has a unique expression `u+v z` with `u,v∈R`. This includes all rational functions, not just polynomials. Explicitly, writing numerator `P0+P1 z` and denominator `Q0+Q1 z`, multiplication by the denominator again uses `z²=y` and has scalar denominator `Q0²+yQ1²`, which is nonzero because the original denominator is nonzero in a field. This gives the required two coefficients in `R` for arbitrary rational denominators.

Also `z∉S`: its square `y` has odd valuation at `y=0`, whereas a square in `S` has even valuation there. Thus `1,z` are linearly independent over `S`. If `f/c0=q∈S*`, then

`1+x z=q(u+v z)`

forces `q u=1` and `q v=x`. In particular `u≠0` and `x=v/u∈R`. But every element of `R=F2(x²,y,tau)` has even `x`-valuation, while `x` has valuation one. This is impossible. The cases `u=0`, `v=0`, and both nonzero are all covered by these coefficient equations.

This proves the desired exclusion for every `c∈F*`, hence the full three-summand nonmembership. Indeed it also proves that `xi_M` is nonzero (choose `c=1`), so the class itself cannot be zero.

## Supporting checks and limits

I independently checked the differential path used in the reduction. In `L`, `d(beta²)=0`, `dlog(f)=h dlog(z)`, and `h²=bz²/(1+bz²)`. Applying the logarithmic Artin–Schreier relation to `s^{-2}h dlog(z)` gives `xi_L=[s^{-2},f)`, and the scalar relation `s^{-2}+s^{-1}=wp(s^{-1})` gives `[s^{-1},f)`. Thus `xi` dies over `LK`, as claimed. No illegal square-root operation on differential coefficients is used.

The basic field hypotheses also survive the relevant attacks: the independent `b` slot gives the degree-four exponent-two extension; the odd `s`-pole gives a separable quadratic extension over both base and completion; the independent `t` slot stays nonsquare after adjoining `beta` by its `t`-valuation. The binary projective quasilinear quadric is integral with function field obtained by adjoining `sqrt(t)`, so the field used for the third summand is the displayed one. This family did not independently inspect the original problem's convention for such quadrics.

The degree-one (`n=0`) discussion is consistent: Artin–Schreier roots cannot first appear in a purely inseparable extension, and rational extensions have no new algebraic constants. A quasilinear-quadric function field has the stated purely inseparable-over-rational presentation; separable extensions preserve the required anisotropy by linear disjointness. This peripheral observation is not needed for the counterexample at `n=1`. It does not assert failure at every index or in exponent one.

`diagnose_norm.py` uses sparse exact formal polynomials over `F2`, with explicit exceptions active under `python -O`. It verifies the conjugate norm identity, multiplicativity, uniformizer norm, and two universal rationalization identities as polynomial identities. It also checks 961 Laurent valuation pairs (including negative valuations), 62 cases with a zero coefficient, and 16 unit cases with their square residues. Its three deliberately wrong normalization alternatives are computed sanity comparisons, not algorithm-mutation coverage. Normal and optimized runs have identical JSON output. The universal proofs above, not these finite counts, establish the result. No numerical or finite-field test is substituted for the rational-field exclusion.

Primary bodies actually inspected: Milne *Class Field Theory* v4.03, general-field Chapter IV relative Brauer theorem/construction; Voight's official 2021 Chapter 6, Theorem 6.4.11 including the short proof and defining conventions; and Chapman–Quéguiner-Mathieu arXiv2111.15251v3, symbol/Kato identification on page3. Critical theorem pages were rendered and viewed. Exact versions, bytes, hashes, read extents and remaining source-proof limits are recorded separately. The full original Kato theorem and every foundational Brauer theorem are accepted standard inputs rather than independently reproved historical results.

No old audit, sibling verdict, priority conclusion, or external contact supported this decision. No merge, PR change, publication, Git mutation, or external write was performed. Third-party bodies/extracts/renders have remained in the excluded local source directory. The only unresolved matters are outside this family's remit: original-target transcription, independent priority analysis, and final publication-package review.
