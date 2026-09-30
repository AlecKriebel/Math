# Independent review: single-root differents and upper ramification for x²+1 over Q₂

**Verdict: PASS for the stated partial theorem.** The original image/size question remains **unsolved, 1/5 attempts**. No mandatory correction was identified. The zero basepoint is an explicit interpretation; no historical novelty or human peer review is established.

The frozen `PARTIAL_RESULT.md` reviewed has SHA-256 `045ed9ab8b9a9105d0471740724fc5bd7d48246647e8cb246269d4493c6f6caa`. Its unchanged snapshot, verifier and receipt are included in `author_replay/`.

## Source and exact scope

The complete cached primary [AIM section12](http://aimpl.org/galarithdyn/12/) was read, including the surrounding section and both problems. Problem12.2 asks about the size of the arboreal representation for f(z)=z²+1 over Q₂. It does not specify a basepoint. Problem12.1 separately asks about wild ramification and a Sen-type analogue. The artifact correctly labels the zero-rooted tree as an interpretation and does not represent a basepoint as recovered source text. A direct web retrieval during this review returned a server error; the complete primary HTML snapshot and its hash were available and inspected.

I read the imported prior report. Its regularity argument, branch valuations, first two splitting-field degrees, level-sign quotient and qualitative infinite-index/wild-ramification assertions are prior material, correctly credited. They are not premises needed to repair a gap in the new single-root calculation, which is proved directly.

[Anderson–Hamblen–Poonen–Walton, *Local arboreal representations*](https://math.mit.edu/~poonen/papers/arboreal.pdf), IMRN2018,5974–5994, Theorem2.1, covers infinite index; Theorem7.3 covers infinite wild ramification for degree p and v(c)≥0. Our f=z²−c has c=−1 and v₂(c)=0. Section5.2 supplies precisely the lower/upper conventions and quotient compatibility used in the submitted proof. Theorem1.3(c) gives a broader applicable regime. These qualitative results are not claimed as new discoveries.

The [June2026 Barcau–Paşol preprint](https://arxiv.org/abs/2606.29310), Theorem1.1, concerns a fixed inverse branch for a monic polynomial with derivative in the maximal ideal. Here f′=2x satisfies that hypothesis. I checked the primary theorem statement and its surrounding scope; I do not certify the preprint's entire proof. The artifact appropriately credits the overlap, uses no theorem from it as a proof premise, and does not deduce APF or strictly APF behavior.

## Eisenstein and local integral basis

For every n, the shifted polynomial Q_n(x)=fⁿ(x+ε_n), with ε_n=0 for even n and 1 for odd n, is monic, has all nonleading coefficients divisible by two, and has constant coefficient congruent to two modulo four. The recurrence of the critical orbit modulo four proves the last assertion for both parities. Hence Q_n is Eisenstein over Z₂.

Every chosen branch field E_n=Q₂(α_n) therefore has degree and ramification index 2ⁿ, residue degree one, and uniformizer π_n=α_n−ε_n. The local monogenicity argument is valid: in the unique power-basis expansion, the valuations 2ⁿv₂(c_i)+i are distinct modulo 2ⁿ. There can be no cancellation at the minimum. Integrality of the sum forces every coefficient c_i to belong to Z₂, because 0≤i<2ⁿ. Thus the full integer ring, not merely an order, is Z₂[π_n]. No unjustified global monogenicity statement is used.

Characteristic zero ensures separability, and the positive critical orbit never returns to zero. This verifies the regular zero-rooted binary tree and the compatible nested fields used in the theorem.

## Different calculation and an independent derivation

The derivative formula for the different applies because the full integer ring is monogenic. [Sutherland's Lecture12, Proposition12.24](https://ocw.mit.edu/courses/18-785-number-theory-i-fall-2021/mit18_785f21_full_lec.pdf) states that formula; Proposition12.28 gives transitivity in a finite separable tower. Complete discrete valuation rings in characteristic zero satisfy the required hypotheses.

The submitted chain-rule calculation gives

\[
v_2((f^n)'(\alpha_n))
=n+\sum_{j=1}^{\lfloor n/2\rfloor}4^{-j}.
\]

At odd levels α_j is a unit; at even levels its valuation is 2^(−j). Multiplying by e(E_n/Q₂)=2ⁿ yields the displayed exact different exponent. The passage between the extended valuation v₂ and the uniformizer-normalized valuation of E_n is correct.

I independently recovered the formula from the **relative quadratic tower**, which supplies a different check of the parity and scaling. The branch equations give

\[
\pi_n^2=\pi_{n-1}\quad(n\text{ even}),
\]

\[
\pi_n^2+2\pi_n+2=\pi_{n-1}\quad(n\text{ odd}).
\]

For odd n>1 the second polynomial is Eisenstein over E_{n−1}, since π_{n−1} has valuation one there whereas two has valuation 2^(n−1). The case n=1 is the ordinary polynomial x²+2x+2. The even polynomial is also Eisenstein. Consequently

\[
d(E_n/E_{n-1})=
\begin{cases}
2^n,&n\text{ odd},\\
2^n+1,&n\text{ even}.
\end{cases}
\]

Indeed the two derivatives are respectively 2(π_n+1), with a unit second factor, and 2π_n. Different transitivity now gives

\[
d_n=2d_{n-1}+2^n+1_{2\mid n},\qquad d_0=0.
\]

Solving this recurrence recovers

\[
d_n=2^n\left(n+\frac{1-4^{-\lfloor n/2\rfloor}}3\right).
\]

The first values 2,9,26,69 agree. Since these single-root fields have residue degree one and the full integral basis has been proved, their local field-discriminant valuations also equal d_n. This statement is not being transferred to a splitting-field polynomial discriminant.

## Passage to finite splitting-field upper breaks

Although E_n/Q₂ need not be Galois, it is an intermediate field of the finite Galois splitting field L_n. Different transitivity is valid without a Galois assumption on E_n. With e_n=e(L_n/Q₂), nonnegativity of the relative different gives

\[
\frac{d(L_n/\mathbb Q_2)}{e_n}
\ge \frac{d(E_n/\mathbb Q_2)}{2^n}.
\]

The denominator here is the ramification index, equivalently the order of inertia, not automatically the full Galois-group order. An unramified residue-field contribution would make the latter larger, and the proof does not conflate them.

The lower-group definition in the artifact agrees with AHPW Section5.2. For a real parameter t it uses the condition v_L(σx−x)≥t+1, so on a noninteger interval it has the usual ceiling-index convention. Hilbert's formula is

\[
d=\sum_{i\ge0}(|G_i|-1).
\]

Separating the i=0 contribution and changing variables through Herbrand's function gives

\[
\frac de=1-\frac1e+
\int_0^\infty\left(1-\frac1{|G^u|}\right)du.
\]

The tame term is correctly retained, and step-function endpoints do not change the integral. The author's derivation through a uniformizer over the maximal unramified intermediate field is also valid: that totally ramified local extension is monogenic, its derivative product runs over inertia, and the different of the unramified extension is trivial.

The integrand is nonnegative, bounded above by one, and vanishes beyond the largest upper break b_n. Therefore

\[
b_n\ge n-1+\frac{1-4^{-\lfloor n/2\rfloor}}3+\frac1{e_n}>n-1.
\]

This proves unbounded **upper** breaks; it is not an inference from unbounded lower breaks alone.

## Infinite upper subgroups

Upper numbering is compatible with finite Galois quotients. Thus restriction from G_{n+1}^u to G_n^u is surjective, and the infinite group is their inverse limit. Given u≥0, the unbounded break estimate supplies a nontrivial finite quotient G_n^u. Surjectivity of the inverse system lifts a nonidentity element, so G_∞^u is nontrivial.

The intersection of all upper groups is trivial: its image in each finite G_n lies in that finite group's eventual trivial group. This agrees with AHPW Lemma5.4. If any G_∞^u were finite, its finitely many nonidentity elements would all disappear by some common larger parameter; that later group would be trivial, contradicting the preceding conclusion. Hence every upper group is infinite.

The argument establishes infinitude, not openness or finite index in G_∞. The explicit absence of an APF conclusion is necessary and correct. It also supplies no recursive description of the splitting groups, their exact sizes or breaks, or Hausdorff dimension.

## Reproduction and verdict limits

The submitted SymPy verifier reproduced its receipt byte for byte: **679 exact assertions** passed. The independent standard-library checker imports no author code. It verifies **1,598 exact assertions**, including a modular-polynomial calculation through degree1024, the different recurrence through level256, local power-basis valuation controls, and Hilbert/Herbrand identities with tame factors and nontrivial unramified degrees. Its finite order profiles are expressly normalization diagnostics, not claimed realizable field extensions.

From this directory:

```sh
python independent_checks.py > independent_results.replayed.json
cmp independent_results.replayed.json independent_results.json
```

For the author replay, with SymPy installed:

```sh
cd author_replay
python verify.py
```

Primary-source hashes and inspected scopes are in `source_verification.json`. Publish only the eight files listed in `review_summary.json`, excluding source PDFs and caches.

The theorem is correct for the explicitly chosen zero-rooted tree. The literal source remains under-specified about its root, and even this interpretation's full image/size question is not answered. Publish as **unresolved partial progress**, with the imported and published qualitative results credited and no novelty claim.
