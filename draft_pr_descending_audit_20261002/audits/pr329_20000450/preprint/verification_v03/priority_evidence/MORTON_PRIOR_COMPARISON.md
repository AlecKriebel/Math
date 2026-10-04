# Stronger prior explicit 5-torsion formulae: exact comparison

Patrick Morton, *Product formulas for the 5-division points on the Tate normal form and the Rogers–Ramanujan continued fraction*, already supplies the relevant degree-ten table and radical formulas in arXiv1612.06268v1 (19December2016), with an expanded v4 (11June2018), subsequently J.NumberTheory200(2019),380–396, DOI10.1016/j.jnt.2018.12.013. This is old explicit universal coordinate and Kummer machinery directly relevant to the candidate, materially stronger attribution than merely saying that division polynomials can in principle be computed. It is not evidence that Morton printed the exact AIM pentagonal normalization or its λ-to-Tate coordinate bridge. [Primary v1](https://arxiv.org/pdf/1612.06268v1), [primary v4](https://arxiv.org/pdf/1612.06268v4), [published article](https://doi.org/10.1016/j.jnt.2018.12.013).

## Exact operative primary scope

The full19-pagev4 text and full10-pagev1 text were independently read. Original pixels on v4 physical/printed5,6,7,18 and v1 physical/printed3,4,5 were inspected. Section2 v4p5/v1p3 prints the degree-ten polynomial D₅ whose roots are the x-coordinates outside the marked cyclic subgroup. V4p6/v1p4 prints the quintic factor, the Kummer parameter u⁵=(2b+11+5√5)/(−2b−11+5√5), and equation(2.1) expressing b as a rational function of u⁵. Theorem2.1 atv4p7/v1p5 gives product formulae for both coordinates of all points outside the marked subgroup. V4p18 additionally recovers the generic x-coordinate field as Q(ζ₅,b,u). This last generic recovery statement must not be conflated with a separately checked every-specialization claim. The prior specialization input is now independently established in Verdure's original Theorem5 and its proof; see VERDURE_PRIOR_COMPARISON.md.

The19-page institution-deposited manuscript was also retrieved independently. It has different PDFbytes but its entire extracted text, normalized only by whitespace, matchesv4. That computed text comparison is not byte equality, original publication-PDF identity, or independent proof checking. Repository PDF metadata records a2018creation/2019modification; arXiv's currently servedv4 PDF has a2022build date. Its displayed version and arXiv history date remain11June2018. The actual v1 primary establishes the relevant table and parameter formula already on19December2016; this does not assert that every expandedv4 section was already present in2016. The journal PDF itself has not been retrieved as such.

## Exact convention and parameter bridge

Morton's normal form is

\[
E_5(b):Y^2+(1+b)XY+bY=X^3+bX^2.
\]

The candidate's Dβ is exactly this curve under **b=−β**, with no further point-coordinate change. If φ=(1+√5)/2 and c=φ⁵, then Morton's ε=(−1+√5)/2=φ⁻¹ and ε̄=(−1−√5)/2=−φ. For the candidate's

\[
\beta=\frac{(11-5\sqrt5)\lambda}{2(\lambda+5\sqrt5)},
\]

the actual old Kummer parameter becomes

\[
u^5=\frac{2b+11+5\sqrt5}{-2b-11+5\sqrt5}
=\phi^5(\lambda+\phi^5).
\]

Thus one may take **u=φθ**, where θ⁵=λ+φ⁵. Over a field containing K=Q(√5), adjoining u and θ gives the same extension. Substitution in Morton's equation(2.1), b=(ε⁵u⁵+ε̄⁵)/(u⁵+1), recovers b=−β exactly. The candidate's Fisher-coordinate Kummer value is −1/(λ+c); multiplying its inverse by −c is precisely Morton's u⁵. The difference is a fifth power factor and inversion/sign conventions, not a different radical mechanism.

Every one of the11coefficients of Morton's D₅(x;b) atv4p5/v1p3 equals the candidate's Rβ(x) in TURN_1equation(20) after b=−β. This exact equality is verified independently by the portable standard-library checker `verify_prior_parameter_comparison.py`, along with the Tate coefficient and Kummer/Fisher/Verdure transformations:25exactsymbolic comparisons over Q(√5). The expanded actual native replay ended2026-10-04T10:02:40.348669+00:00, exit0/empty stderr. The earlier21-comparison run and its genuine receipts remain private and unchanged. The initial comparison implementation required unavailable SymPy and genuinely failed with ModuleNotFoundError; that complete failure and unchanged failure-program body are preserved privately. No installation occurred; the successful checker now uses rational-polynomial arithmetic and the standard library.

## Priority implication and exact limitation

The complete universal remainder polynomial, explicit remaining-torsion coordinate formulae, and radical parameter on the Tate family have prior published treatments. They must receive classical prior credit and must not be advertised as novel universal torsion formulae or a newly found radical solver. The candidate's nontrivial comparison task is its explicit bridge from the source-specific singular plane pencil and chosen origin to that Tate twist, followed by the correctly stated field/specialization/rational-torsion conclusions. Whether that exact pentagonal bridge or the resulting complete pentagonal answer was previously printed remains a separate historical question, not resolved by this equality.

Morton himself credits Hugues Verdure, *Lagrange resolvents and torsion of elliptic curves*, IJPAM33(1)(2006),75–92, for an earlier Kummer element and formulae in terms of a root of the division polynomial (v1p3 andv4pp3,18–19). The full18-page original scan has now been visually read and confirms the prior full-torsion criterion including specialization. This later correction to the initial provisional note is recorded in the separate stage3 log; both early independence freezes are untouched. No first-discovery/application or2026continuing-openness claim follows from the bounded corpus.
