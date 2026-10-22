# Checkable prior implication: the complete strengthening is already known

This is an audit reconstruction of a prior argument, not a new contribution or a positive author proof-search turn. It applies to full-dimensional bounded convex Euclidean polytopes in every dimension d >= 2, and therefore to the selected three-dimensional target. The fixed face correspondence is preserved throughout.

## Primary antecedents and attribution

Martin Winter's **Stoker's theorem from polytopal tensegrities**, Theorem 1, states exactly the weak-angle implication below, with the stronger conclusion that all corresponding unit normals differ by one orthogonal transformation. The author-hosted two-page note is dated September 4, 2026. Both complete pages were read as text and pixels. Its bytes match the file in the author's public Git commit `766c313bc2187a5eafd5757dca43ffefc6a9ced6`, whose API record has committer date `2026-09-04T20:55:42Z`:

- [Author note](https://martinwintermath.github.io/pdf/publications/Stokers_conjecture.pdf)
- [Commit-pinned note](https://raw.githubusercontent.com/martinwintermath/martinwintermath.github.io/766c313bc2187a5eafd5757dca43ffefc6a9ced6/pdf/publications/Stokers_conjecture.pdf)
- SHA256 `520aed6feadfdda0906f61a3d780830142d36fbbd93bca80678533ee321610e1`, 289110 bytes.

A distinct two-page version dated September 3, 2026 is attached to Adiprasito's September 4 post. It has the same theorem and radial-homotopy proof; its SHA256 is `84d396275a7635ff1fc577221d0789109ec12c096a6368250aeb451161756899`.

The substantive metric input is Winter, **Rigidity, Tensegrity, and Reconstruction of Polytopes Under Metric Constraints**, IMRN 2024(9), 7721-7747, [DOI 10.1093/imrn/rnad298](https://doi.org/10.1093/imrn/rnad298), Theorem 3.2, Remark 3.7 and Lemma 4.3. The journal typeset copy obtained from Warwick's institutional repository was read at these statements and the complete Theorem 3.2 proof (PDF pages 5-10, 12-13); the theorem and dependency pages were inspected as pixels. The arXiv version is `2302.14194v2`, revised January 8, 2024. The journal registrar gives online publication December 21, 2023 and print publication May 7, 2024. Publication metadata is evidence of the bibliographic record, not an independent proof endorsement.

The note credits Akopyan for noticing the finite consequence of Winter's earlier work. Its historical assertions about other Stoker proofs are not needed here. The reduction below uses the published metric theorem and checks the whole additional bridge directly.

## Imported metric theorem, with the exact hypotheses used

Let R be any full-dimensional convex polytope with labelled vertices r_i and edge graph E. Its continuous Wachspress coordinates a_i(x) on R have

    a_i(x) >= 0,  sum_i a_i(x) = 1,  sum_i a_i(x) r_i = x.

At an interior point every coefficient is positive; on a proper face F, coefficients vanish for vertices outside F. Neither simplicity nor simpliciality is required. Given an arbitrary assignment of target vectors z_i in the same Euclidean dimension, define

    Var_a(r) = (1/2) sum_ij a_i a_j |r_i-r_j|^2,
    Var_a(z) = (1/2) sum_ij a_i a_j |z_i-z_j|^2.

Winter's Theorem 3.2 says that `|z_i-z_j| <= |r_i-r_j|` on every edge implies `Var_a(z) <= Var_a(r)` for a = a(x), x interior. Equality implies `z_i = A r_i + b` for one affine map, with equality on all graph-edge lengths. The target assignment need not realize any polytope and its nonedge distances need not be bounded.

I checked the published proof: a normalized Izmestiev matrix has positive off-diagonal entries precisely on edges, kernel the coordinate columns, a single positive eigenvalue, and row sums the Wachspress coefficients. After translation by its positive Perron eigenvector, the spectral decomposition makes the remaining trace term nonpositive. Edge positivity proves the edge equality condition, and the kernel condition proves affine equality. Izmestiev's `0704.0349v3`, Theorem 2.4 and Appendix A.3, supplies these properties for arbitrary convex polytopes, including nonsimple ones; the volume Hessian is C2 across combinatorial changes. The second Minkowski inequality and Bol's equality condition remain standard imported convex-geometric foundations.

## Complete finite bridge

Suppose P and Q have corresponding facets with outward unit normals n_i and m_i, and every adjacent pair satisfies `theta_P(i,j) <= theta_Q(i,j)`. Translate an interior point of each to zero and write

    P = {x: n_i . x <= h_i},   Q = {y: m_i . y <= k_i},
    h_i > 0, k_i > 0.

Put R = P polar and S = Q polar. Their labelled vertices are

    r_i = n_i/h_i,    s_i = m_i/k_i.

Polar duality reverses the fixed face-lattice isomorphism; in particular the edges of R are exactly the adjacent-facet pairs of P. Define **z_i = m_i/h_i**. The denominator is h_i, not k_i; the z_i need not be the vertices of a realization of R. This is why the general-assignment form of the published metric theorem is essential.

The equal-radius and edge-contraction requirements hold exactly. Indeed `|r_i|=|z_i|=1/h_i`, and

    theta = pi - arccos(normal inner product)

is increasing in that inner product. Thus `n_i.n_j <= m_i.m_j` at every edge of R, and

    |r_i-r_j|^2 - |z_i-z_j|^2
      = 2(m_i.m_j - n_i.n_j)/(h_i h_j) >= 0.           (1)

It remains to find the interior zero that a naive appeal to polar normalization omits. For 0 <= t <= 1 define positive radial factors and Wachspress maps

    c_i(t) = (1-t)/k_i + t/h_i,
    Phi_t(x) = sum_i a_i(x) c_i(t) m_i,   x in R.       (2)

For a proper face F of R, let F' be its corresponding face of S. Choose a supporting linear functional L for F' with value b > 0 there; positivity follows because zero is interior to S. For every vertex r_i of F, `L(s_i)=b` and hence `L(m_i)=k_i b > 0`. Face support of the a_i gives

    L(Phi_t(x)) = sum_{r_i in F} a_i(x)c_i(t)k_i b > 0
    for every x in F and every t.                      (3)

Consequently no Phi_t vanishes on the boundary. At t=0 it sends each face F into F'. Take any face-preserving boundary homeomorphism B from R to S, obtained by barycentric subdivision of their face lattices. On F the straight interpolation between Phi_0(x) and B(x) stays in the convex face F' and avoids zero. Their radial normalizations are therefore homotopic. The normalized B has degree +1 or -1, so the boundary map Phi_0 has nonzero degree. Equation (3) preserves this degree through t=1.

If Phi_1 had no interior zero, its radial normalization on all of R would extend its nonzero-degree boundary map over a ball, which is impossible. Thus `Phi_1(x)=0` for some x in the interior of R. No boundary zero is possible by (3).

Now set a = a(x). The elementary variance identity and equal radii give

    Var_a(z) = sum_i a_i |z_i|^2
             = sum_i a_i |r_i|^2
             = |x|^2 + Var_a(r).                       (4)

The published metric theorem gives the reverse inequality, so x=0 and equality holds in that theorem. We get `z_i=A r_i+b` and equality on every edge. Taking the a(0)-weighted sum shows b=0.

For completeness, the final isometry inference is checked explicitly rather than inferred from equal variances term by term. Let T=A^T A-I, a symmetric matrix. Equal vertex radii imply `r_i^T T r_i=0`. Equal edge lengths and expansion of the corresponding quadratic form imply `r_i^T T r_j=0` for every edge ij. The vectors r_i together with the neighbors of a fixed vertex r_i span the ambient space: their differences generate the full-dimensional tangent cone at r_i. Therefore T r_i=0. This holds at every vertex, and the vertices span the ambient space because zero is interior to R. Thus T=0 and A is orthogonal.

Multiplying `z_i=A r_i` by h_i gives **m_i=A n_i for every facet**. Hence **n_i.n_j=m_i.m_j for every pair**, including nonadjacent facets. This is exactly the selected candidate's strengthening. Reversing P,Q excludes strict domination at all edges and proves OWR Problem 4 and the corresponding dimension-three instance of Akopyan-Karasev Conjecture 5.1. The same reasoning proves its all-dimensional formulation.

## Boundary checks and limitations

- A nonsimple vertex gives a nonsimplicial face of R. Equation (3) uses every vertex of that face simultaneously and requires no triangulation preserving a target metric. It applies, for example, to the four normals at a square-pyramid apex.
- The face correspondence is the fixed geometric labelling; it is never replaced by an arbitrary matching of angle multisets.
- Nearly flat positive-volume examples remain included. No uniform bound over all polytopes is needed; h_i,k_i are positive for each fixed pair. Flat, unbounded, or lower-dimensional objects are outside the statement.
- Equal-angle rigidity, infinitesimal rigidity, and an unsupported order-convexity assertion play no role. No path of angle-monotone polytopes is assumed.
- Orthogonal equality of the normals does not assert congruence of P,Q. Their support numbers may differ.
- This derivation verifies the prior implication with named standard published inputs; it is not formal verification of all convex geometry or a fresh audit of every line of the selected smooth-Dirac proof.
