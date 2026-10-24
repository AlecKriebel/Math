# Source contract — Kourovka 21.126

Prepared October 24, 2026 UTC. Future-candidate source preparation only; no original solution effort begun.

Official main source: https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-3.pdf
Edition/update: 21st edition, official October 20 main update.
Locator: printed p.198, problem 21.126 (PDF page index 197).
Attribution: the question is credited parenthetically to N. Brady; the entry is signed I. Soroko.
SHA-256: f133b4547caae29822fb65455b2115c4af075aa168983996a2aac1c2b21bc118

The two requested existence classes are finitely presented subgroups H of a right-angled Artin group A(Γ) with intrinsic Dehn function:

1. super-exponential; or
2. sub-exponential but not polynomial.

The source context contrasts the general CAT(0) setting with the exponential and polynomial degrees known for RAAG subgroups. Preserve the two branches separately. A witness to either branch answers the literal disjunction; it need not answer the other branch. No normality, finite-index, quasiconvexity, type F3, or compact-special structure is imposed on H. Finitely presented means a finite presentation (type F2), not merely finitely generated or homological FP2. The Dehn function belongs to H, not to the ambient RAAG and not to the pair’s distortion function. If infinite defining graphs are allowed, finite generation of H puts its generators in a finite induced RAAG, so finite ambient graphs suffice.

For a finite presentation P=⟨S|R⟩ of H, let Area_P(w) be the least number of conjugates of relators or their inverses whose product is freely equal to a null word w. Then
\[
\delta_P(n)=\max\{\operatorname{Area}_P(w): |w|\le n,\ w=_H1\}.
\]
This is interpreted up to the usual coarse equivalence. One standard convention is
\[
f\preceq g\quad\Longleftrightarrow\quad
\exists C\ge1\ \forall n\ge1:\ f(n)\le Cg(Cn)+Cn,
\qquad f\simeq g\Longleftrightarrow f\preceq g\text{ and }g\preceq f.
\]
For the nondecreasing Dehn functions at issue, allowing separate constants, additive shifts, and additive constants gives the same convention. Brady–Soroko Definitions 2.1–2.2 distinguish this from the finer equivalence used for automorphism growth; do not interchange them. Brady–Tran Convention 2.1 and Definition 2.2 give the displayed convention and presentation independence.

The Notebook does not formally define its rate adjectives. For future research use the presentation-invariant strong interpretation: super-exponential excludes every bound δ≼exp(n); an explicit witness also satisfying exp(n)≼δ gives a strict coarse separation. A robust intermediate witness should have no polynomial upper bound and satisfy log(δ(n))/n→0. Merely δ≼exp with δ≉exp is a weaker coarse formulation for potentially irregular functions and should be distinguished if used. “Not polynomial” is treated as not polynomially bounded, rather than merely not an integer power or not exactly equal to a polynomial. This interpretation is consistent with the literature’s polynomial-isoperimetric-inequality convention, but is not an extra definition quoted from the Notebook.

All ordinary exponentials a^n, a>1, are coarsely equivalent; a larger base is not super-exponential. The scale exp(n²) is super-exponential, while exp(√n) and n^{log n} illustrate superpolynomial subexponential scales. These are comparison examples, not claimed RAAG subgroup realizations. Nonintegral powers n^α and n^d log n remain polynomially bounded. A lower bound alone cannot certify the subexponential branch; both an appropriate upper bound and a superpolynomial lower obstruction are needed.

Success requires a finite presentation of H, a verified injection into a RAAG (or into a group with a verified finite-index RAAG embedding, followed by intersection), and a proof of the required intrinsic Dehn growth. Large distortion or an abstract double with large Dehn function is insufficient without the embedding step. Finite-index passage preserves finite presentability and the Dehn equivalence class, so a verified virtual embedding suffices.
