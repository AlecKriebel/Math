# Independent verification of the prior implication

Scope: finite adversarial priority verification for PR932 / 30003471. This is an exposition and verification of prior results, not a new theorem claim or an additional positive author proof-search turn. Original author accounting remains 1/5; audit positive proof turns: 0.

## 1. Claim and the exact imported foundations

Let P and Q be full-dimensional bounded convex polytopes in R^d, d>=2, with a fixed face-lattice isomorphism. Label corresponding actual facets, with outward unit normals n_i and m_i. If every corresponding ridge has interior angle theta_P(i,j)<=theta_Q(i,j), then there is one orthogonal map T with m_i=T n_i for every i. In particular the complete labelled normal Gram matrices agree. The three-dimensional target follows by applying this statement to the reverse ordered pair if every theta_P were strictly larger.

The foundational imported input is the Izmestiev matrix theorem, as stated in Winter, IMRN 2024(9), 7721-7747, Theorem 3.3. For a full-dimensional polytope K with vertices p_i and 0 in its interior, there is a symmetric matrix M, positively normalized, with: positive off-diagonal entries exactly at edges; zero off-diagonal entries at nonedges; MP=0 for the n-by-d vertex-coordinate matrix P; kernel dimension d; exactly one positive eigenvalue; M1=alpha, where alpha is the strictly positive Wachspress vector of 0 and 1^T M1=1. The row-sum identity follows from the polar-volume Hessian and Euler homogeneity (Winter Proposition 3.5 / Corollary 3.6).

The second imported foundation is the published generalized Wachspress coordinate construction: alpha_i(x)>=0, sum alpha_i(x)=1, sum alpha_i(x)p_i=x, continuity on K, strict positivity in its interior, and support on the vertices of the minimal face containing a boundary point. Winter Remark 3.7(i) states the boundary property explicitly without a simplicity hypothesis. Definition 4.2 uses these source coordinates even when the target points are an arbitrary graph embedding. No target realization is required.

These are genuine prior mathematical inputs. The matrix theorem traces to Izmestiev, *The Colin de Verdiere number and graphs of polytopes*, Israel J. Math. 178 (2010), 427-444, Theorem 2.4 in arXiv:0704.0349v3. Izmestiev uses the negative Hessian, so its one-negative-eigenvalue convention is Winter's one-positive convention after sign reversal. Its signature and kernel result imports the second Minkowski inequality and Bol's equality condition. This audit does not reprove those foundational inequalities.

## 2. Independent check of the material content of Winter Theorem 3.2

This section also makes the affine equality case explicit. The full relevant published body and the version-pinned author manuscript have both been read.

Translate K so that the point with Wachspress vector alpha is 0. Put A=alpha alpha^T-M. Then A is positive semidefinite. Indeed any v can be written v=c1+w, where c=alpha^T v and alpha^T w=0. Since 1^T M1=1 and 1^T Mw=0,

    v^T A v = -w^T M w >= 0.

If w^T Mw were positive, the M-form would be positive definite on the two-dimensional span of 1 and w, contradicting its single positive eigenvalue. Thus the displayed inequality holds, including zero or negative directions. Also

    ker A = span(1, columns of P).

For Av=0, Mw=0 with the same decomposition; conversely every such w and 1 lie in ker A. Here ker M=col(P), by the kernel-dimension and full-rank hypotheses. This gives the claimed kernel without assuming that the target graph embedding realizes a polytope.

For any target points z_i, define

    V_alpha(z) = sum_i alpha_i |z_i|^2 - |sum_i alpha_i z_i|^2
               = (1/2) sum_ij alpha_i alpha_j |z_i-z_j|^2,
    E_M(z) = sum_{ij an edge} M_ij |z_i-z_j|^2.

Expansion of squares gives

    E_M(z)-V_alpha(z) = tr(Z^T A Z) >= 0.

For the source, E_M(p)=V_alpha(p) because MP=0 and alpha^T P=0. If all target edges shorten weakly, strict positivity of the edge coefficients therefore gives

    V_alpha(z) <= E_M(z) <= E_M(p)=V_alpha(p).

Equality in the complete comparison forces every edge length to be unchanged and every column of Z to lie in ker A. Hence z_i=B p_i+b for one affine map. Conversely that affine condition with all edge lengths unchanged gives equality. This proves precisely the needed inequality and equality characterization in Theorem 3.2. It agrees with the published proof's centering at the positive eigenvector and its spectral decomposition, whose trace and equality steps were checked separately.

## 3. The zero-image specialization and genuine orthogonality

Suppose now |z_i|=|p_i|, all target edges shorten weakly, and phi(x)=sum alpha_i(x)z_i=0 at some x in int(K). Write S=sum alpha_i(x)|p_i|^2=sum alpha_i(x)|z_i|^2. The contraction theorem gives

    S = V_alpha(z) <= V_alpha(p) = S-|x|^2.

Thus x=0, and all inequalities are equalities. We obtain z_i=B p_i+b and equal lengths on every edge. It remains to justify orthogonality; affine equality alone is insufficient.

Consider the quadratic polynomial R(u)=|Bu+b|^2-|u|^2. It vanishes at every vertex. Along each edge its quadratic coefficient is the difference of the squared edge lengths, hence zero. Since its endpoint values are also zero, R vanishes on the entire edge. Induct on face dimension. On any face of dimension at least two, R vanishes on each facet by the induction hypothesis. A nonzero polynomial of degree at most two cannot vanish on three distinct facet hyperplanes: each hyperplane's affine linear equation divides the polynomial, whereas three such distinct factors have total degree three. Every bounded full-dimensional face of dimension at least two has at least three distinct facets. Hence R vanishes identically on each face, and finally on the full-dimensional K. Therefore R is the zero polynomial on R^d. Its coefficients imply

    B^T B=I, B^T b=0, |b|^2=0.

So b=0 and B is orthogonal when the target dimension is d. This supplies the compressed final step of published Lemma 4.3 and independently validates the exact specialization used by the two-page note. No all-pair distance conclusion has been assumed prematurely.

## 4. The polar and degree bridge, with arbitrary labelled correspondence

Translate P,Q so that 0 is interior and write their facet support numbers h_i,k_i>0. Let

    K=P-polar,       p_i=n_i/h_i,
    L=Q-polar,       w_i=m_i/k_i,
    z_i=m_i/h_i.

Then |p_i|=|z_i|. Since theta=pi-arccos(normal dot product), the assumed angle direction gives n_i.n_j<=m_i.m_j on adjacent facets, so

    |p_i-p_j|^2-|z_i-z_j|^2
       = 2(m_i.m_j-n_i.n_j)/(h_i h_j) >= 0.

The edges of K are exactly those labelled facet adjacencies. This uses face-lattice duality and holds at nonsimple vertices as well.

Let alpha_i(x) be the source Wachspress coordinates on K. Define for 0<=t<=1

    phi_t(x) = sum_i alpha_i(x) lambda_i(t) w_i,
    lambda_i(t)=(1-t)+t k_i/h_i >0.

The target points at t=1 need not form any realization of K. The coordinate map is still defined and continuous, by the same fixed source coordinate functions.

At t=0, phi_0 maps each source face into its corresponding target face. Build a face-preserving boundary homeomorphism H:boundary K -> boundary L using barycentric subdivisions of all proper faces and the fixed lattice isomorphism. On any source face, H and phi_0 land in the same convex target face. Their straight-line interpolation therefore stays in boundary L and avoids 0. Radial projection shows that phi_0 on the boundary has degree +1 or -1, according to orientation. Nonzero degree is enough; no orientation-preserving correspondence is assumed.

For any proper source face, choose a target supporting hyperplane containing its corresponding target face. Normalize it to y.w_i=1 for every vertex in that face; 0 is strictly inside L, so this normalization is possible. Boundary face support gives, for x in that source face,

    y.phi_t(x) = sum_i alpha_i(x) lambda_i(t)
              >= min_i min(1,k_i/h_i) > 0.

Thus the whole relevant boundary face image is in one fixed strict halfspace throughout the homotopy. The y may vary from face to face, which causes no problem: pointwise nonvanishing and continuity give a global homotopy in R^d minus {0}. The boundary's radial degree is constant and nonzero.

If phi_1 had no zero inside K, its normalization would extend the boundary map continuously over the ball K and would force boundary degree zero. This contradiction gives phi_1(x)=0 for some interior point; it cannot be a boundary point because of the strict halfspace estimate. Section 3 then yields z_i=T p_i for one orthogonal T. Multiplication by h_i proves m_i=T n_i for all i, hence all labelled normal Gram entries agree.

## 5. Nonsimplicity and precise boundary limits

Nothing above needs source or target simpliciality/simplicity, a differentiable combinatorial map, equal supports h_i=k_i, or a convex realization by z_i. The source coordinates' published continuity and face support are sufficient. Face support can also be checked directly from positivity and linear precision: for a supporting affine function ell>=0 on K, ell(x)=sum alpha_i(x)ell(p_i); at ell(x)=0 all weights on vertices off that face vanish. In three dimensions this already forces unique boundary limits at an edge and at a vertex, including a nonsimple vertex, because the remaining vertex set is respectively the edge's two endpoints or the single vertex. At a relative facet interior only one source support slack vanishes; the polar-face volume weights have a common simple pole, whose positive leading coefficients vary continuously tangentially. Their normalized limits are the planar Wachspress coordinates of the facet. This agrees with published Remark 3.7 and introduces no hidden simplicity condition. The full arbitrary-dimensional continuity theorem is retained as a published coordinate input, not replaced by these three-dimensional checks.

The argument is for genuine full-dimensional bounded polytopes with their actual facets and positive interior support numbers. It gives no uniform estimate as a body degenerates, no theorem for zero supports or unbounded/lower-dimensional bodies, and no conclusion about congruence of P and Q themselves. Equal normal Gram matrices allow different facet support numbers.

## 6. Result and provenance

The exact stronger conclusion is already Theorem 1 of Martin Winter, *Stoker's theorem from polytopal tensegrities*, author-hosted two-page note. The note has a September 4, 2026 document date. Independently acquired author-repository API records commit 766c313bc2187a5eafd5757dca43ffefc6a9ced6, both author and committer dated 2026-09-04T20:55:42Z, as adding this PDF. The raw file at that historical commit is byte-identical to the live note. This is primary historical repository evidence, not an independent push-time or web-archive certificate; the commit is unsigned. Both dates precede the original candidate's October 8 date and its immutable Git head timestamp, 2026-10-08T00:48:11Z.

The foundational IMRN paper's publisher body was actually accessed through its public publisher CDN, not just inferred from the author PDF or bibliographic metadata. Its published record states online publication December 21, 2023; volume 2024, issue 9, May 2024, pages 7721-7747. The relevant Theorem 3.2, Theorem 3.3, Remark 3.7, and Lemma 4.3 were checked in that body and in arXiv:2302.14194v2. This does not mean the 2023 publication explicitly stated this dihedral comparison theorem: the explicit short derivation checked here is the September 2026 note.

No Wang-Xie-Yu or Dirac theorem, no claimed date of a broader historical resolution, and no unpublished energies manuscript is needed for this priority finding. The note's broad historical remark about a theorem since 2023 is not adopted here.
