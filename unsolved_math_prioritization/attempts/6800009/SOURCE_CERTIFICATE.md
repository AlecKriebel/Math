# Even conjugate multiplicity does not force bi-invariance

## Conclusion and attribution

**The literal question has a negative answer.** A left-invariant metric on the fixed product group SU(2) × SU(2) can be globally isometric to a product of round three-spheres while failing right invariance for that group law. Consequently every geodesic segment has even fixed-endpoint Morse index.

This is a **credited consequence of known constructions**, not a claim of a new counterexample. Fusi, Lafuente and Stanfield, *Homogeneous Generalized Ricci flows II*, arXiv:2608.25619v1, Theorem E and Proposition 7.3, construct the relevant metric on K × K and explicitly identify its underlying Riemannian metric with a bi-invariant product. Their paper studies additional torsion and flow questions; no such extra structure is needed here. [Primary source](https://arxiv.org/html/2608.25619v1#S7).

There is older relevant prior art: Barbaro, *Bismut Hermitian Einstein metrics and the stability of the pluriclosed flow*, arXiv:2307.10207v2, Example 4.1, constructs invariant metrics on SU(3) × T² whose lifts are isometric to a bi-invariant SU(3) × R² metric but are not bi-invariant for the product group law. This too implies a counterexample to the compact-connected version. The example appears in the 2023 preprint, with the checked v2 dated 30 September 2024. [Primary source](https://arxiv.org/html/2307.10207v2).

Neither checked source was found to explicitly discuss Morgan–Pansu Question 9. The implication to that question is spelled out below; the construction itself receives full prior credit. No earliest-priority claim is made.

## Exact mathematical target

Catalog identity: 6800009 / AMR-067-0009, *Bi-invariant metrics and multiplicity of conjugate points*. In Morgan and Pansu's 2018 collection, this is Section 8, Question 9, proposed by Claudio Gorodski, printed page 8.

The question concerns a Riemannian metric g on an arbitrary compact connected Lie group G, invariant under every left translation. Assuming every geodesic segment has even Morse index, it asks: **“Must the metric be bi-invariant?”** [Original source, p. 8](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf).

Bi-invariance here refers to the given multiplication on G. The source does not replace this conclusion with being isometric to some bi-invariant metric, and does not assume that G is simple. Both distinctions matter. The example below is globally isometric to a bi-invariant metric, and its group is semisimple but not simple. It settles the printed question and makes no claim about either strengthened restriction.

## An explicit instance of the known construction

Write K = SU(2) as the unit quaternions, and let q be its curvature-one round metric. Multiplication on either side by a unit quaternion is an orthogonal linear transformation of R⁴, so q is bi-invariant. Let

\[
 G=K\times K,\qquad h=2q\oplus q,\qquad
 F(a,b)=(a,ba^{-1}),\qquad g=F^*h.
\]

The map F is a global diffeomorphism, with inverse F⁻¹(u,v) = (u,vu). Thus g is a positive-definite smooth Riemannian metric, and F is a global isometry from (G,g) to (G,h). The group G is compact, connected, simply connected, and semisimple.

### Left invariance

For (x,y) in G, conjugate its usual left translation by F:

\[
 F\circ L_{(x,y)}\circ F^{-1}(u,v)=(xu,yvx^{-1}).
\]

On the first factor this is a left translation. On the second it is a left translation followed by a right translation. Both preserve the scaled bi-invariant metrics in h, so the displayed map is an h-isometry. It follows that L_(x,y) is a g-isometry for every (x,y), proving left invariance.

### Failure of right invariance

Identify the Lie algebra of K with the imaginary quaternions, with orthonormal basis i,j,k and [i,j] = 2k. At the identity,

\[
 dF(A,B)=(A,B-A),\qquad
 g_e((A,B),(C,D))=2\langle A,C\rangle+\langle B-A,D-C\rangle.
\]

Its matrix in the ordered basis ((i,0),(j,0),(k,0),(0,i),(0,j),(0,k)) is

\[
 M=\begin{pmatrix}3I_3&-I_3\\-I_3&I_3\end{pmatrix}.
\]

If g were bi-invariant, differentiating invariance under conjugation would give

\[
 g_e([X,Y],Z)+g_e(Y,[X,Z])=0
 \quad\text{for every }X,Y,Z\in\mathfrak g.
\]

Take X=(i,0), Y=(j,0), Z=(0,k). The two ideals commute, so [X,Z]=0, whereas [X,Y]=(2k,0). The left side is then −2. This contradiction proves that g is not bi-invariant.

### Identification with the cited metric

The source uses Q = minus the Killing form on the compact simple algebra and its orthogonal diagonal/anti-diagonal decomposition. In those coordinates its metric g_(1,3,1) has multiplicity-space matrix

\[
 P=\begin{pmatrix}1&1\\1&3\end{pmatrix}.
\]

Returning to the two direct-product factors gives

\[
 \frac12
 \begin{pmatrix}1&1\\1&-1\end{pmatrix}
 P
 \begin{pmatrix}1&1\\1&-1\end{pmatrix}
 =\begin{pmatrix}3&-1\\-1&1\end{pmatrix}.
\]

This is exactly the metric above with q replaced by Q. On SU(2), Q is a positive scalar multiple of q, so the two descriptions differ only by an overall homothety. Proposition 7.3's simply transitive action gives the same product-isometry mechanism. The metric here is therefore not presented as an independent new family.

## All geodesics and endpoint conventions

The index is the number of negative directions of the energy Hessian on H¹ vector fields vanishing at **both endpoints**. It is not the periodic/free-loop index, and “segment” is not restricted to minimizing segments. The following argument covers arbitrary duration and also conjugate endpoints.

By left invariance it suffices to start at the identity. For initial velocity (A,B), the image under F is the h-geodesic

\[
 \eta(t)=(\exp(tA),\exp(t(B-A))).
\]

Constant scaling of a metric preserves its Levi-Civita connection. In each round three-sphere factor the normal Jacobi equation, in a parallel frame, is f″ + c²f = 0, where c is the speed measured by q. There are two independent normal directions. The tangential equation is f″=0 and yields no nonzero field vanishing at two distinct parameter times. If c=0, every direction satisfies f″=0 and there are no conjugate times.

Consequently a moving factor contributes conjugate times t = mπ/c, m=1,2,..., each with multiplicity two. The product connection and Jacobi equation split by factors, so simultaneous conjugate times have the sum of the two multiplicities, hence multiplicity four. There are no other conjugate times. The isometry F preserves all these spaces of Jacobi fields.

For T>0 put N(r) = #{m in the positive integers : mπ < r}. With c₁=|A|_q and c₂=|B−A|_q, the fixed-endpoint Morse index is

\[
 \operatorname{ind}(\gamma|_{[0,T]})
 =2N(Tc_1)+2N(Tc_2).
\]

The inequality is strict: a conjugate time at the final endpoint contributes to nullity rather than to the negative index. More explicitly,

\[
 \operatorname{null}(\gamma|_{[0,T]})
 =2\mathbf1_{Tc_1\in\pi\mathbb N_{>0}}
 +2\mathbf1_{Tc_2\in\pi\mathbb N_{>0}}.
\]

These formulas also follow directly by expanding each normal component of the index form in the Dirichlet sine basis: its eigenvalue signs are those of (mπ/T)²−c², twice per moving factor. Tangential and stationary-factor components are positive. Thus no nonconjugate-endpoint qualification is needed. Constant geodesics have index and nullity zero. Translating the starting point handles every geodesic segment on G.

Both the index and endpoint nullity are always even. Together with the failure of right invariance, this proves the claimed negative answer.

## Scope and verification limits

- This certificate concerns ordinary Riemannian geodesics and their fixed-endpoint index. No torsion connection is substituted for the Levi-Civita connection.
- The product isometry supplies a direct proof; Bismut-flat terminology or classification is not needed for this explicit example.
- The metric is isometric to a bi-invariant metric. An isometry-invariant reformulation would be a different question.
- No counterexample on a compact simple group is claimed.
- Current UnsolvedMath site content could not be read: the exact page returned HTTP 403. The pinned catalog statement agrees with the original author-hosted source; current site status remains unverified.
- The cited 2026 result is a preprint. The mathematical counterexample is elementary and proved here, but fresh independent review of this packet remains a separate gate.
