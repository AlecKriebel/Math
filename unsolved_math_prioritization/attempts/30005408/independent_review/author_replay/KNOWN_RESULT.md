# The local Hilbert–Burch parametrization conjecture is solved by Oszer

**30005408 / OWR-12697689-004. Recommended status: already_solved, 0/5 original proof attempts, pending independent source audit.**

## Exact target and credited resolution

The original OWR6/2023 contribution by Roser Homs, jointly with Anna-Lena Winz, works over a characteristic-zero field k in R=k[[x,y]]. Its Conjecture6 on printed p.347 asks whether the prescribed finite-dimensional perturbation matrices parametrize the local Groebner cell of every finite-colength monomial ideal. It is the same conjecture as Homs–Winz (2021), Conjecture5.14, and Homs–Winz (2023), Definition4.1 and Conjecture4.2.

Piotr Oszer, *Hilbert–Burch matrices and explicit torus-stable families of finite subschemes of A²*, **Corollary8.12**, proves the stated map is an isomorphism. Thus it is, in particular, a bijection as asked. The full author version is arXiv:2407.07993v4 (11 August2025); the journal article is Quarterly Journal of Mathematics **76**(4),1159–1187 (2025), DOI10.1093/qmath/haaf032. The publisher lists online publication on18 September2025. We read the full author version and checked the publisher's bibliographic listing; access to the publisher's complete PDF was unavailable in this audit.

This is a credited prior result. No new proof of Oszer's general isomorphism theorem, novelty claim or resolution of a different ambient Hilbert-cell problem is asserted.

## The exact matrix space

Write

    E=(x^t,x^(t−1)y^m_1,...,y^m_t),
    0=m_0<m_1<=...<=m_t,     d_i=m_i−m_(i−1).

Redundant intermediate monomial generators and zero differences d_i are permitted. The canonical (t+1) by t matrix H has diagonal y^d_i and subdiagonal −x. Put

    u_ij=m_j−m_(i−1)+i−j.

The admissible entries n_ij are polynomials in y with coefficients on precisely these exponent ranges:

    max(0,u_ij+1)<=e<d_i       when i<=j,
    max(0,u_ij)<=e<d_j         when i>j.                     (1)

An empty range forces a zero entry. This is the finite-dimensional space called T'(E) in the OWR conjecture and N_<d(E) in Homs–Winz Definition4.1. The target is

    V(E)={J subset k[[x,y]] : Lt_local(J)=E},

where smaller total degree leads, and equal-degree ties use lexicographic x>y. It is not the global lex or degree-lex cell in k[x,y]. The map takes the maximal minors and then the ideal they generate in the complete local ring R.

### Notation cautions checked against the surrounding definitions

- The OWR definition calls the space T(E) before the conjecture calls it T'(E). The cited Homs–Winz definition gives (1) unambiguously.
- The display immediately before Oszer Corollary8.12 uses ord in its upper bound and varies its subscript notation. Its ambient spread-out matrix, Definition3.1, already imposes the **degree** bounds in (1), and the corollary's proof identifies the space with that restricted finite-dimensional matrix space. Retaining only an order upper bound while allowing arbitrary higher coefficients would be a different, infinite-dimensional space and is not the result used here.
- Oszer Example2.4 has an adjacent reversed inequality for deg(x) and deg(y). Its actual displayed cocharacter and its defining monomial comparison give the intended negative-degree lex order. The matching calculation below uses those formulas, not the reversed inequality.

## Independent matching calculation

Oszer assigns a coefficient of y^e in position(i,j) the torus bidegree

    (i−j, m_j−m_(i−1)−e).

For an integer M sufficiently large, choose weights deg(x)=−(M−1), deg(y)=−M. The resulting coefficient weight is

    w_ije=M(e−u_ij)+(i−j).                                  (2)

Since |i−j|<=t, taking M>t shows that positive weight is equivalent to e>=u_ij for i>j and e>=u_ij+1 for i<=j. Combining with the ambient degree bounds gives exactly (1). No parameter of weight zero survives: equality would require e=u_ij and i=j, but then e=d_i contradicts e<d_i. Thus the attracting parameter space has only the origin as a fixed point, matching the hypothesis of Corollary8.11 used to prove Corollary8.12. For the finite monomial range needed for a length-d quotient, M can also be chosen larger than that range; then −M(a+b)+a orders monomials by negative total degree and lexicographic x-priority exactly.

### Why the punctual/local target is preserved

For negative y-weight Oszer's construction first removes extraneous support by adding y^(t m_t). Theorem8.10 writes the relevant resultant as

    y^(t m_t) [u + y W(parameters,y)],

with u invertible on the stated locus. On the strictly positive-weight parameter cell, this coefficient has weight zero, so it is its nonzero value at the origin (1 with the monic normalization). In k[[x,y]], u+yW is a unit. Since the resultant is in the ideal of the extreme minors, y^(t m_t) already belongs to the completed ideal. Therefore

    (I_t(H+N)+(y^(t m_t))) R = I_t(H+N) R.                  (3)

This explains why removing a distant polynomial component does not alter the local ideal in the conjecture. It does not assert that the uncompleted polynomial ideals have the same support or colength. The global construction and its isomorphism are supplied by Oszer; equations(1)–(3) verify their application to this exact local problem.

## Validation and limitations

The exact checker compares (1) and (2) over many non-strict staircases, checks the monomial-order signs on bounded ranges, and verifies truncated inverse identities for 1+yW. These controls validate the convention matching, not the full geometric isomorphism theorem. No dimension count up to a finite colength is used as a proof of bijectivity.

The original source's characteristic-zero scope is retained. The theorem already addresses every finite-colength monomial ideal, rather than only lex segments or complete intersections. Arbitrary term orders, higher embedding dimension and unrelated Hilbert loci are not claimed. The inherited native runtime was unchanged; its exact model identifier was not exposed. Separate source review is required before the repository draft.

### Primary sources

- OWR Conjecture6: https://doi.org/10.4171/owr/2023/6
- Homs–Winz (2021), Conjecture5.14: https://arxiv.org/abs/2004.04776
- Homs–Winz (2023), Definition4.1 and Conjecture4.2: https://arxiv.org/abs/2309.06871
- Oszer, Corollary8.12 and preceding support construction: https://arxiv.org/abs/2407.07993v4
- Published article: https://doi.org/10.1093/qmath/haaf032
