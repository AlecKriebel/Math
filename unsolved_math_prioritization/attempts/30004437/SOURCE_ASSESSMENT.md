# 30004437: a credited negative answer to real-zero amalgamation

## Disposition and exact target

Recommended disposition, subject to separate review: **already_solved, 0/5 original proof turns**. This is a source-status correction and verification of published mathematics, not a new discovery or a classification of all amalgamable pairs.

The original is Markus Schweighofer's contribution, “Spectrahedral relaxations of hyperbolicity cones,” OWR 12/2020, printed pp.652–654. The **first conjecture on p.653** quantifies over arbitrary finite tuples
`x=(x1,...,x_l)`, `y=(y1,...,y_m)`, `z=(z1,...,z_n)` of distinct commuting variables. The field is R. “Real zero” means p(0) is nonzero and every polynomial t↦p(ta), for real a, has only real complex roots; degree drops and nonzero constants are allowed. Degree is total degree. For compatible real-zero p(x,y),q(x,z) of degree at most d, the conjecture asks for an exact common real-zero extension of degree at most d.

**Published counterexamples answer this in the negative.** Sawall–Schweighofer, Indagationes Mathematicae 35 (2024), 37–59, already give compatible cubic examples with six common variables and no real-zero extension of any degree. Their complete author manuscript, arXiv:2305.07403v2, §6 Example 6.1, is accessible here; the final journal-layout PDF was not compared. Kummer–Sawall, Algebraic Combinatorics 8 (2025), 1–15, DOI [10.5802/alco.399](https://doi.org/10.5802/alco.399), §§2–3, strengthen this to **two common variables and one private variable on each side**. The complete final publisher PDF, including its proof, was inspected. This packet checks the latter explicit example.

Thus the imported August 2026 “open” assessment is materially wrong: failure of the necessary compatibility condition to be sufficient is already a counterexample to the universal conjecture. It is not merely an unrelated partial result. The omitted tuple definition also matters: the distinct scalar-block case l=m=n=1 is a known positive case, not this source's unrestricted question.

## Two meanings of “weak” must not be identified

The second conjecture on OWR p.653, also called WRZAC, asks for one exact restriction and only agreement of the **cubic parts** on the other restriction, allowing arbitrary output degree. The later Sawall–Schweighofer Conjecture 7.6 uses the same adjective for **two common variables and both restrictions exact**, again without a degree bound. The 2025 counterexample refutes the latter and the assigned degree-preserving conjecture. This packet does **not** infer a verdict on the separate OWR cubic-part version merely from the reused name. Nor does it resolve the generalized Lax conjecture.

## Explicit published cubic pair

Use homogeneous variables `(u,a,b,s)` and define

B(u,a,b) = 2ab²+2a²b+2ub²+8uab+2ua²+2u²b+2u²a,

P1(u,a,b,y) = B(u,a,b)+4y(ab+ub+ua),

P2(u,a,b,z) = B(u,a,b)+4z(ab+ub+ua)+a²z.

These are precisely the diagonal specializations in Kummer–Sawall §3.1. In the original source notation take

p(a,b,y)=P1(1,1+a,1+b,y),
q(a,b,z)=P2(1,1+a,1+b,z).

Both have total degree three, constant term 20, and identical restrictions at y=0 and z=0. In particular, d=3 is allowed. There is no zero polynomial, vanishing-origin, field, or degree ambiguity. The exact coefficient dictionaries are in `EXACT_CERTIFICATE.json`.

### Why they are real zero

Let h1 be the sum of all squarefree cubic monomials in seven variables labelled `(0,0',1,1',2,2',3)`, except the triples `{0,0',3}`, `{1,1',3}`, `{2,2',3}`. Let h2 omit just `{0,0',4}`, `{2,2',4}` in the corresponding ground set with 4 in place of 3. These are the known stable basis polynomials of F7^(-4) and F7^(-5). Diagonalizing each primed coordinate to its unprimed partner gives P1,P2. Stability is preserved by this substitution.

The stability inputs are credited, not inferred from real-root samples. Wagner–Wei's criterion and F7^(-4) sum-of-squares Rayleigh identity are in arXiv:0709.1269v1, Theorem 3 and pp.4–6. Our exact expansion verifies the p.5 identity with its depicted labels and the relabelling to h1. The criterion uses the established half-plane property of matroids on at most six elements for the deletions/contractions. For h2, Choe–Oxley–Sokal–Wagner's Example 10.12 exhibits the dual as the nice transversal presentation `{123,156,2467,3457}`. All its nonzero four-column permanents are exactly two, verified here. Their permanent theorem (10.2), Corollary 10.3, and preservation under duality prove stability. Its two complementary forbidden triples meet at one point, identifying h2 up to relabelling.

Homogeneous stability gives hyperbolicity in the nonnegative direction `(1,1,1,0)`, where both cubics equal 20. Dehomogenizing after the shared-coordinate shear gives p and q real zero, as in Kummer–Sawall Lemma 2.11 and §3. There is no assumption that a general real-zero polynomial is stable.

## Why an extension of any degree is impossible

This is an explanatory reconstruction of Kummer–Sawall Theorems 3.3 and 3.5, not a new theorem. For a homogeneous stable polynomial, its support J is M-convex; the function

r(S)=max over alpha in J of sum_{i in S} alpha_i

is its associated polymatroid rank. Let r1,r2 come from P1,P2 on `{0,1,2,3}` and `{0,1,2,4}`. Here 0 denotes u, 3 denotes y and 4 denotes z. The complete two rank tables are in the certificate.

The following six quantities would all be nonnegative for an amalgamating polymatroid r, by submodularity or monotonicity:

1. r(03)+r(04)-r(034)-r(0)
2. r(23)+r(24)-r(234)-r(2)
3. r(034)+r(234)-r(0234)-r(34)
4. r(0234)-r(02)
5. r(13)+r(34)-r(134)-r(3)
6. r(134)-r(14)

All unknown mixed ranks cancel in their sum. The remaining known ranks are
r(03)=r(04)=r(23)=r(24)=r(13)=2,
r(0)=r(2)=2, r(02)=r(14)=3, r(3)=1.
The sum is **-1**, a contradiction. Scaling both input ranks by any positive integer gives -m instead. This is a compact certificate for the published rank obstruction.

For clarity, the passage from an arbitrary-degree polynomial extension to a rank amalgam must not be omitted. Suppose R(a,b,y,z) is real zero with the exact two restrictions. Let D=deg R≥3 and homogenize to H(u,a,b,y,z). It is hyperbolic in e0, and its restrictions are `u^(D-3) Pk(u,u+a,u+b,private)`.

Use the closed hyperbolicity cone containing e0, with convention that the roots of t↦H(te0+v) are **nonpositive**. The cones of each input shear contain each coordinate ray and also v=e0-e1-e2. This follows by pulling back the nonnegative orthant under the shear from Pk; the point v maps to e0, and the e0 direction maps to e0+e1+e2. These particular vectors all have u≥0. Consequently adding the factor u^(D-3) on the restrictions does not exclude any of these vectors. The corresponding membership tests use only the restriction on the relevant coordinate subspace, so all five coordinate rays and v lie in H's cone.

Now undo the shear: `T(u,a,b,y,z)=H(u,a-u,b-u,y,z)`. Its pulled-back cone contains the entire nonnegative orthant. The vector e0+e1+e2 is an interior hyperbolicity direction for T, since it maps to e0 for H; adding the remaining nonnegative coordinate directions keeps it interior. Every strictly positive vector is interior (subtract a sufficiently small positive multiple of e0+e1+e2 and use cone addition). Thus T is homogeneous stable by the standard hyperbolicity/stability equivalence. Its restrictions are `u^(D-3)P1` and `u^(D-3)P2`.

Drop monomials of T whose u exponent is below D-3 and divide the rest by u^(D-3), calling the resulting cubic T0. Its support equals the support of the stable nonzero derivative `partial_u^(D-3) T`: termwise differentiation changes coefficients by positive nonzero factorials and maps surviving exponent vectors injectively. Therefore its support is M-convex even though T0 itself need not be asserted stable. Its two restrictions are exactly P1,P2. M-convex exchange implies that rank restriction agrees with the rank of each nonzero coordinate restriction (Kummer–Sawall Lemma 2.17/Corollary 2.18). Hence it supplies the impossible amalgam above.

### Source convention cautions

The final Kummer–Sawall Definition 2.12 displays “nonnegative” roots with `te+v`, whereas the subsequent positive-ray statements require nonpositive roots; already the polynomial x at e=1 diagnoses the sign. We state the consistent cone convention explicitly above. Also, multiplication by u^(D-3) may intersect a whole cone with u≥0; our explanation uses membership of the required vectors, not an unjustified equality of full cones. These clarifications do not change the published no-amalgam conclusion or the credited status.

## Limits, controls, and attribution

The answer is to the universal existence conjecture; no characterization of every compatible pair, degree-one-overlap classification, or new priority is claimed. The established positive cases (no shared variables, one variable in each of three blocks, degree≤2) remain intact. The 2025 example is cubic with two shared variables, so it lies outside those cases.

`verify.py` is independently written standard-library validation code. It checks coefficient expansions, all basis-exchange axioms for the two seven-element matroids, the indicated published Rayleigh identity, the nice-transversal multiplicities, the collapsed rank axioms, the exact contradiction, compatibility and origin values. Its finite checks complement the analytic support/cone argument; they do not replace it. No downloaded program is executed, no root sampling is treated as proof, and no source PDFs are proposed for republication.

Credit belongs to Sawall–Schweighofer for the earlier counterexample, Kummer–Sawall for the two-variable strengthening, and their cited stable-polynomial and matroid inputs. This campaign supplies a source correction and reproducibility audit only.
