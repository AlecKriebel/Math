# Turn 1: complete torus gauge coordinates and an exact small-volume optimum

The original large-lattice quarter-filling problem remains unresolved. This turn repairs the finite torus coordinates, derives a variational reformulation over projections, and proves the global optimum on the4 by4 torus. It also identifies why that small-volume saturation cannot extend unchanged to larger even square tori. These are scoped results, not a resolution by changing the source's size or optimization domain.

## 1. All gauge data on a periodic square grid

Use vertices(x,y) modulo L in each coordinate, with L>=4. Let u_(x,y) be the hopping phase from(x,y) to(x+1,y), and v_(x,y) that from(x,y) to(x,y+1). Reverse entries are conjugates. Define the plaquette product

    F_(x,y)=u_(x,y) v_(x+1,y) conjugate(u_(x,y+1)) conjugate(v_(x,y)).

The product of all F is1, because every edge occurs once in each orientation. Define H as the product of horizontal phases along row0 and V as the product of vertical phases along column0. All are invariant under vertex gauge transformations T→D*TD.

**Claim.** The compatible data(F,H,V), with product F=1 and otherwise arbitrary unit complex values, parametrize gauge classes completely.

To prove it, gauge all non-wrapping horizontal edges to1 and all non-wrapping vertical edges on column0 to1. These edges form a spanning tree, so the gauge exists by recursively fixing vertex phases, uniquely up to a constant. Write the remaining horizontal wrap edge in row y as h_y. Set v_(0,y)=1 for y<L−1 and v_(0,L−1)=V. Plaquette equations then force

    v_(x,y)=v_(0,y) product_(a=0)^(x−1) F_(a,y),
    h_0=H,
    h_(y+1)=h_y / product_(a=0)^(L−1) F_(a,y).              (1.1)

The final y closure is exactly product F=1. Conversely these formulas construct a hopping matrix with the prescribed data. Thus the data are both necessary and sufficient. This is a concrete spanning-tree version of the circuit-flux gauge lemma in Lieb–Loss1992, SectionII.

For zero plaquette flux, the spectrum with loop phases H=e^(ia),V=e^(ib) is

    2 cos((2 pi r+a)/L)+2 cos((2 pi s+b)/L), 0<=r,s<L.     (1.2)

This follows by using twisted plane waves in the gauge with phases only on the two wrapping seams. For L=4, H=V=1 gives largest eigenvalue4; H=−1,V=1 gives largest eigenvalue2+sqrt2. The local plaquette data agree but the spectra differ. Hence discarding the loop phases is not legitimate in finite volume.

## 2. An exact Grassmannian variational reformulation

Let q=N/4, N=L². For any Hermitian T, the sum E_q(T) of its q lowest eigenvalues equals

    min_{P=P*=P², rank(P)=q} Tr(PT).                       (2.1)

Indeed, in an eigenbasis of T, the diagonal weights of P lie in[0,1] and sum to q, so the weighted sum is at least the sum of the q lowest eigenvalues; the corresponding spectral projection attains it.

Both the edge-phase torus and the rank-q projection space are compact. We may minimize jointly and in either order. For fixed P the phases on distinct undirected edges are independent choices, and

    Tr(PT)=2 sum_edges Re(P_yx T_xy).

The edge term is minimized by T_xy=−P_xy/|P_xy| when P_xy is nonzero, with arbitrary phase at a zero entry. Consequently

    min_edge_phases E_q(T)
      =−2 max_{P=P*=P²,rank(P)=q} sum_edges |P_xy|.          (2.2)

All flux compatibility conditions are automatic because we optimize actual edge phases. Formula(2.2) does not by itself identify its maximizing projection; it is a nonconvex optimization on the rank-q Grassmannian. It is not the half-filled trace-norm problem.

## 3. A universal bound and its exact equality condition

For even L, the torus is bipartite. In the two color classes, write

    T=[0 B; B* 0].

Its eigenvalues are plus and minus the singular values s_1>=...>=s_(N/2)>=0 of B. Every vertex has degree4 and all edge magnitudes are1, so Tr(T²)=4N and sum_j s_j²=2N. Therefore

    E_q(T)=−sum_(j=1)^q s_j >= −sqrt(q sum_(j=1)^q s_j²)
           >=−sqrt(q*2N)=−N/sqrt2.                        (3.1)

Equality holds precisely when s_1=...=s_q=sqrt8 and all remaining singular values vanish. Equivalently T has eigenvalues−sqrt8 and+sqrt8 each with multiplicity q and0 with multiplicity N/2, or T³=8T together with Tr(T²)=4N and the bipartite symmetry.

This is a global bound over arbitrary edge phases and all torus holonomies. It does not assume uniform flux.

## 4. The4 by4 torus attains the global bound

On L=4 set u_(x,y)=1 and v_(x,y)=i^x. The plaquette products are all i, including wrapping plaquettes, since i^(−3)=i. Both reference loop holonomies are1.

Let A be the positive-direction horizontal hopping shift and C the positive-direction vertical hopping shift, so T=A+A*+C+C*. They satisfy A^4=C^4=I and AC=i CA (changing the orientation convention conjugates i without affecting the conclusion). In this representation, direct multiplication gives

    T³=8T,  Tr(T²)=64.                                    (4.1)

For a short explicit verification independent of symbolic commutation conventions, the supplied checker constructs the16 by16 matrix with Gaussian-integer entries and multiplies it exactly; it verifies every entry of(4.1). This is a finite algebraic certificate and can also be verified by expanding the four shifts. Hermiticity gives real eigenvalues; (4.1) makes them0 or±sqrt8. Bipartite symmetry and the trace identity give multiplicities8,4,4, respectively. Thus

    E_4(T)=−8 sqrt2.

By(3.1), this is the global optimum on this exact finite torus.

There is also a zero-plaquette-flux minimizer: choose H=V=−1 in(1.2). Each coordinate cosine is±sqrt2/2, twice each. The resulting eigenvalues are−2sqrt2 with multiplicity4,0 with multiplicity8 and+2sqrt2 with multiplicity4, again attaining−8sqrt2. Thus the local flux of a minimizer is not unique at this size. This tie does not refute the assertion that uniform pi/2 is an optimal choice.

## 5. The same bound cannot be saturated for even L>=8

Fix x and y separated by three horizontal positive steps. On an L by L torus with L>=8, y is not adjacent to x, and the only length3 walk from x to y is the straight three-edge path. Therefore

    (T³)_(x,y)=T_(x,x+e1) T_(x+e1,x+2e1) T_(x+2e1,y)

has modulus1, whereas T_(x,y)=0. Thus T³=8T is impossible. The global lower bound in(3.1) is strict on every such finite torus. Compactness ensures a strictly positive finite-volume gap, but no size-uniform lower gap is asserted in this turn. L=6 is not included in this argument, because positive and negative three-step paths have the same endpoint.

This obstruction shows why an exact4 by4 saturation certificate cannot be extrapolated to the source's large-square-lattice problem.

## 6. Checks and remaining gap

verify_turn1.py verifies the full plaquette-plus-holonomy reconstruction modulo several integer phase grids, its compatibility and gauge invariance, and all entries of the4 by4 Gaussian-integer polynomial identities. It also verifies distinct same-plaquette spectral moments under different twists and counts the unique three-step displacement paths on L=8,10,12. These controls certify the finite matrix assertions above; they do not establish uniform-flux optimality on arbitrary large tori or in the thermodynamic limit.

The next unresolved comparison is the global quarter-filled energy against arbitrary spatial flux patterns at large size, with holonomies retained. Neither the small exact optimum nor the known half-filled theorem supplies it.
