# Primary theory used in the pentagonal-quintic computation

The prior imported computation supplies a proposed line product and Kummer-conic reduction; all identities used here are independently verified. Its claims are credited, not treated as an independent audit.

For the modular cover we use Tom Fisher, *Some examples of 5 and 7 descent for elliptic curves over Q*, J. Eur. Math. Soc. 3 (2001), 169–201, DOI 10.1007/s100970100030. The full 33-page primary PDF was downloaded from the publisher, https://ems.press/content/serial-article-files/31488 (277,396 bytes), after author-host requests failed. Printed pp.172–173 and 194–195 were rendered and inspected. The relevant assertions are:

- Lemma 1.1: a point of order at least four determines a Tate normal form, and the pointed pair has no automorphisms
- Equation (2), p.172: the Tate family with marked point of order five
- Equation (4), p.173: its discriminant and cusp parameters
- Lemma 3.4 and its proof, p.194: the universal split-torsion X(5) parameter and the degree-five map to X_1(5), with the displayed fractional-linear changes

Our use of the cover over a field containing the fifth roots of unity is geometric base change of those universal maps, not an application of an arithmetic rank or Selmer theorem over a different field. The proof states the finite-level labeling and the absence of a residual automorphism explicitly. Polynomial identities for the map are also checked independently.

For division polynomials and torsion kernels, see Andrew Sutherland, MIT 18.783, Lecture 5 (September 26, 2023), https://math.mit.edu/classes/18.783/2023/LectureNotes5.pdf, especially the section on division polynomials. The elementary recurrence used here is applied after completing the square in a general Weierstrass model. The degree-twelve fifth-division polynomial is expanded and its known quadratic factor removed exactly; its degree-ten remainder is displayed, not left as an instruction to run a package.

These established tools are credited. The new work under review is the explicit identification of the fixed plane pencil with the twist of the Tate family, its coordinate maps, and the resulting specialized torsion computation. Historical novelty is not established.
