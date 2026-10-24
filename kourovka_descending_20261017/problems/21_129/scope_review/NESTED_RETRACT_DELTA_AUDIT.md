# Fresh adversarial audit: nested central retracts and ordinary filling

**Verdict: pass.** The core retraction and quadratic ordinary Dehn-function deduction in `../geometry/NESTED_CENTRAL_RETRACTS.md` are valid for irreducible spherical rank n≥2, with quadratic filling restricted to n≥3. This is a bounded verification of a derived filter, not a new-source priority claim or a solution of21.129.

Exact source-note hash, source-scan hash, audit timestamp, and finite indexing sanity checks are preserved in `NESTED_RETRACT_AUDIT_MANIFEST.json`. The indexing argument is general; its validity does not depend on checking finitely many ranks.

## Winding normalization and the crucial indicator formula

For every ambient reflection hyperplane H, winding of its defining linear form is an integer homomorphism λ_H on P. Rescaling that form changes no winding. In particular a positively oriented meridian has value1, including in rank1: the Artin generator is a half twist in the orbit quotient, while its square is the pure meridian.

For a standard parabolic X, take a point a in the relative interior of its standard real chamber face and a sufficiently small generic normal vector b. Exactly the hyperplanes of its reflection subsystem contain that face. Along a+εexp(2πit)b, the defining form has a simple positively oriented circle about0 for those hyperplanes, and a small circle not enclosing0 for every other hyperplane. Thus its winding vector is exactly the claimed0/1 indicator, with no Coxeter-number factor. The local arrangement is the reflection arrangement of W_X in its normal space, and its full scalar turn represents the embedded pure full twist Δ_X². A basepoint path through the standard chamber realizes the standard parabolic embedding; changing it only conjugates the pure loop and cannot alter λ_H.

This argument also works for reducible X: the product decomposition of its local arrangement makes the full scalar turn the product of the components' full twists. No connected-prefix assumption is required.

For X=S the Hopf loop has winding1 at every hyperplane. The Hopf product splitting and the infinite cyclic pure center, [CP Proposition3.1](https://ems.press/content/serial-article-files/39000?nt=1), identify this fiber with the whole pure center. Primitivity is essential and valid: if this central loop were a proper power of a pure central generator, each integer winding coordinate1 would be divisible by that power. Therefore every difference λ_H−λ_H′ vanishes on all of Z(P), rather than only a finite-index central subgroup. The global pure full twist is Δ_S² even when the generator of Z(A) is Δ_S itself.

## Commutation and the integral splitting

Put X_j={s1,…,sj}, for1≤j≤n−1. For i≤j, Δ_Xi² belongs to A[X_j] and Δ_Xj² is central there, so all the chosen elements commute before passing to Q. This supplies the group homomorphism from the free abelian source; independence is then established by the retraction rather than assumed.

A simple reflection s_i lies in the standard parabolic W_Xj exactly when i≤j. Hence λ_Hi(z_Xj)=1_(i≤j), and the consecutive differences satisfy

\[
(\lambda_{H_i}-\lambda_{H_{i+1}})(z_{X_j})
=1_{i\le j}-1_{i+1\le j}=\delta_{ij}.
\]

There is no off-by-one at j=n−1: the second coordinate λ_Hn is outside that proper prefix and equals0 there. The pairing is exactly the identity matrix over the integers, so no denominator, nonprimitive sublattice, or rational-only splitting occurs. Thus r∘j=id, proving injectivity, the \(\mathbb Z^{n-1}\) subgroup, and a homomorphic retraction onto it.

The auxiliary parabolic-center intersection argument also holds: pure parabolic elements have zero winding outside the subsystem, whereas a nonzero pure global central power does not. For a central element of A lying in a proper parabolic, a positive power enters that pure intersection; spherical Artin torsion-freeness then makes the original element trivial. The core retraction proof does not depend on this auxiliary fact.

If the title's “maximal-rank” is intended as an optimality claim, an explicit supporting sentence is useful. Deconing supplies a finite(n−1)-dimensional K(Q,1), so cd(Q)≤n−1. The exhibited free abelian subgroup gives the reverse inequality. Since cohomological dimension is monotone on subgroups, no free abelian subgroup can have rank greater than n−1. This completes that wording using the already established arrangement model.

## Ordinary Dehn inequalities

Q is finitely presented: P has a finite presentation, and killing one generator of its cyclic center is a finite presentation for Q. The split P=Q×Z makes Q a homomorphic retract of P.

For a finitely presented retract R of a finitely presented group G, use finite generating sets and a retraction ρ. Replace each edge label of a G-filling by the bounded word for its ρ-image. Every G-relator becomes a fixed null word in R; finitely many such words admit a uniform area bound. Replacing each ambient cell by its chosen R-filling proves δ_R≼δ_G. This applies equally to the upper bound Q≤retractP and the lower bound Z²≤retractQ. No subgroup distortion or subquadratic-gap theorem is needed.

The [Charney1992 primary article](https://eudml.org/doc/164935) was retrieved as its actual GDZ scanned article, and complete printed pages671–672 were rendered and visually read. Printedp672 explicitly states biautomaticity for both the finite-type Artin group and its pure subgroup and records the quadratic isoperimetric consequence. Thus δ_P≼L² is a verified source input. A link to the scanned article, retrieval hash and provenance are in `sources/charney1992_biautomatic.json`; its PDF is a local research cache.

For n≥3, the retraction onto Z^(n−1), composed with coordinate projection and inclusion for Z², makes Z² a retract of Q. Since δ_Z²≃L², the lower bound L²≼δ_Q follows. Together with the upper bound, δ_Q≃L². By CP Corollary3.2, Q has finite index in A/Z(A), and ordinary Dehn functions are equivalent under finite-index passage. The claimed conclusion for that full central quotient follows.

## Boundaries and exact scope

- **n=1:** P is cyclic, Q=1, and A/Z(A)=1. The positive-rank retract and quadratic statements do not apply.
- **n=2:** irreducibility gives a dihedral reflection arrangement with m≥3 lines. Its projectivization is CP1 minus m points; Q is F_(m−1), hence nonabelian free. The constructed retract is Z¹. The full central quotient is virtually free, and both have linear Dehn function. The quadratic lower bound is correctly withheld.
- **n≥3:** the Z² retract exists and gives the quadratic lower bound.
- **Reducible ambient diagrams:** excluded by the theorem's irreducibility hypothesis, which is necessary. For example A1×A1 has a two-dimensional pure center and trivial pure central quotient, contradicting an unqualified rank-minus-one formula. Reducible *prefix* diagrams cause no issue.

All residual types have equal rank at least4 within each pair and therefore share this retract rank and ordinary quadratic filling type. This verifies the failed ordinary-filling filter; it does not compute higher filling functions, a Morse boundary, or quasi-isometry rigidity.
