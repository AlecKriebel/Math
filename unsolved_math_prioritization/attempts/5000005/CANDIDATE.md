# A common germ label for parallel short trajectories

**Status: reconstructed complete candidate; independent review pending.**
This is an AI-generated, unrefereed reconstruction of the interrupted candidate for target 5000005 / AMR-049-0005, using its previously consumed approach. It is not the missing original file and does not inherit that file's hash. No historical-priority claim is made.

## 1. Target, convention, and dependencies

Put \(N=n-2\) and \(\delta=N\pi/n\). Place a regular polygon \(P\) with one vertex \(O\), its clockwise-following list of vertices \(P_0=O,P_1,\ldots,P_{n-1}\), and side \(OP_{n-1}\) horizontal to the right. The interior angles at \(O\) are \(0\leq\alpha\leq\delta\). A short trajectory stops at its first subsequent vertex; there is no upper bound on its length. Boundary sides are included.

The target is Fuchs's Conjecture 2.6, printed p.511 of [Fuchs 2021](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf): if the trajectory at angle \(\alpha\) has type \(A_k\), then the parallel trajectory at
\[
\alpha'=\ell\pi/n+\varepsilon\alpha\in[0,\delta],\qquad \varepsilon\in\{1,-1\},
\tag{1}
\]
has type \(A_{\varepsilon k-\ell}\), with indices in \(\mathbb Z/N\). When \(n\) is even, \(\ell\) is even. We prove this rule, including existence of a first-vertex endpoint in the asserted direction. This differs from the length-ratio Conjecture 2.7 treated in PR152 / target5000006.

Use the complete Definition 2.1, including its immediately preceding segment-parity selector. Write \(\pi-\beta\) for the final interior angle in Fuchs's Figure8. If the trajectory has \(q\) segments, its type is equivalently
\[
\begin{array}{ll}
q\text{ odd}:&s=n(\alpha+\beta)/(2\pi)\in\mathbb Z,
\quad k\equiv n-1-s\pmod N,\\
q\text{ even}:&s=n(\beta-\alpha)/(2\pi)\in\mathbb Z,
\quad k\equiv s-1\pmod N.
\end{array}
\tag{2}
\]
Here \(0\leq\alpha\leq\delta\) and \(2\pi/n\leq\beta\leq\pi\). The inequalities in the definition choose the representatives of (2). One must not drop the parity selector when both numerical angle relations happen to be integral. Direct polygon chords use the odd-segment formula.

The double-polygon construction, affine type index, and classical cusp reduction were developed in the [PR152 candidate](https://github.com/AlecKriebel/Math/pull/152). We credit that work and give the additional common-label argument, including a direct rederivation of the type identity needed here. The imported classical theorem is stated precisely in Section5. Nothing here assumes Fuchs's other conjectures, including Conjecture2.7.

## 2. Coordinates on the vertex cones

Let \(Q=-P\), with its vertices \(Q_j=-P_j\), after taking the polygon center as the origin for this notation. Glue each side of \(P\) to its parallel side of \(Q\) by translation with reversed endpoint order. Keep two labelled polygons even when \(n\) is even. The resulting translation surface is \(X_n\).

The corner-successor cycle is
\[
P_0,Q_1,P_2,Q_3,\ldots .
\tag{3}
\]
For odd \(n\) it visits all \(2n\) corners, giving one cone of total angle \(2\pi N\). For even \(n\) it gives two cycles, each of \(n\) corners and total angle \(\pi N\). Their bases are \(P_0\) and \(Q_0\). The genera are respectively \((n-1)/2\) and \((n-2)/2\), by Euler characteristic.

Give each cone an increasing angular coordinate \(\phi\), with zero at the lower side of its base corner. Corner \(t\) has angular interval
\[
[t\delta,(t+1)\delta].
\tag{4}
\]
For odd \(n\), its polygon copy is \(P\) for even \(t\) and \(Q\) for odd \(t\), and its vertex index is \(t\bmod n\). Its physical tangent direction is \(\phi\bmod2\pi\).

For even \(n\), write \(c=0,1\) for the cone based at \(P_0,Q_0\). At corner \(t\), the vertex index is \(t\bmod n\) and the polygon copy is \(P\) when \(t+c\) is even. The physical tangent direction is
\[
\phi+c\pi\pmod{2\pi}.
\tag{5}
\]
For example, the lower physical side at vertex \(P_j\) or \(Q_j\) is \(-2j\pi/n\) or \(\pi-2j\pi/n\), which verifies these coordinate descriptions directly.

The affine involution \(\iota\) exchanges the two polygons by the half-turn. For even \(n\), it exchanges the two cones and preserves their synchronized coordinate \(\phi\). It has \(n\) regular fixed points, the glued edge midpoints, and additionally fixes the sole vertex point when \(n\) is odd. Thus, for \(n\geq5\), it has \(2g+2\) fixed points. Riemann–Hurwitz gives a sphere quotient, so \(\iota\) is the hyperelliptic involution.

Every affine automorphism \(f\) of \(X_n\) commutes with \(\iota\). Indeed, \(f\iota f^{-1}\) has derivative \(-I\), hence extends holomorphically across the cone points, and has a sphere quotient. Uniqueness of the hyperelliptic involution in genus at least two proves the assertion. This applies whether or not \(f\) preserves orientation.

Ordinary billiard unfolding alternates translates of \(P\) and \(Q\). It therefore maps short trajectories to saddle connections on \(X_n\); the terminal copy is \(P\) when the number of segments is odd and \(Q\) when it is even. Conversely, a saddle connection can be folded along the successive edges to give the billiard trajectory belonging to its initial polygon germ. Intermediate vertices are excluded in both descriptions.

## 3. The common label and the source type

Fix a real lift \(\theta\) of an oriented physical direction. For a germ with cone coordinate \(\phi\) in direction \(\theta\) **or** \(\theta+\pi\), define
\[
L_\theta(\phi)=\frac{\phi-\theta}{\pi}\pmod N.
\tag{6}
\]
The quotient is an integer by (5), or its odd counterpart. It is well-defined when the cone coordinate wraps: the period is \(2N\pi\) for odd \(n\) and \(N\pi\) for even \(n\).

For either fixed physical direction, (6) labels the \(N\) germs bijectively by \(\mathbb Z/N\). For odd \(n\), the labels are the \(N\) residues \(2j\), or \(1+2j\), and \(N\) is odd. For even \(n\), each cone contributes \(N/2\) labels of one parity; the other cone contributes the other parity. No division by two in an even cyclic group is being used.

For an oriented saddle connection in direction \(\theta\), let \(a\) label its outgoing initial germ and \(b\) its backwards-pointing terminal germ, using the **same** reference \(\theta\) in (6). Define its intrinsic index to be \(b-a\).

**Lemma 1 (source type).** For a billiard trajectory starting at \(P_0\) with slope \(\alpha\), its intrinsic index is its source label \(k\).

**Proof.** Take \(\theta=\alpha\). The initial coordinate is \(\phi=\alpha\), so \(a=0\). If the terminal corner is \(t\), the backward germ has coordinate
\[
\phi_v=\begin{cases}
t\delta+\pi-\beta,&\text{terminal copy }P,\\
t\delta+\beta-2\pi/n,&\text{terminal copy }Q.
\end{cases}
\tag{7}
\]
The second offset is \(\delta-(\pi-\beta)\): the terminal reflected copy reverses the physical corner offset. Let \(j=t\bmod n\) be the vertex index. In the first case, comparing the physical terminal direction with \(\alpha+\pi\) gives
\(s+j\equiv0\pmod n\); in the second it gives \(s-j-1\equiv0\pmod n\). This uses the physical lower side directions listed after (5), not an assumed conclusion about types.

From (7), in the first case,
\[
b=1+(tN-2s)/n,
\qquad b-(n-1-s)=N\big((t+s)/n-1\big)\equiv0\pmod N.
\]
In the second,
\[
b=(tN+2s-2)/n,
\qquad b-(s-1)=N(t-s+1)/n\equiv0\pmod N.
\]
The quotients on the right are integers by the physical-direction congruences. Equation(2) proves the claim. Changing a cone lift changes \(b\) by a multiple of \(N\). This proof works for both parities of \(n\), including side germs. ∎

**Lemma 2 (common affine shift).** If \(f\) is orientation-preserving affine and takes physical direction \(\theta\) to \(\theta'\), then it adds the same residue \(d\) to all labels (6), both outgoing and backward, in that direction. In particular, it preserves \(b-a\).

**Proof.** An orientation-preserving real-linear derivative has an increasing angular lift \(F\) satisfying
\[
F(x+\pi)=F(x)+\pi.
\tag{8}
\]
This follows from linear antipodality and degree one. For odd \(n\), the map on the sole cone differs from \(F\) by a constant multiple of \(2\pi\), so the assertion follows immediately from (8).

For even \(n\), suppose \(f\) takes cone0 to cone \(h\in\{0,1\}\). Its map in synchronized coordinates on cone0 is \(G(x)=F(x)-h\pi+2\pi q\), for an integer \(q\), modulo the full cone angle. Commutation with \(\iota\) makes the map on cone1 the **same** \(G\), modulo that angle. Choose \(\theta'=F(\theta)\). Every germ under consideration has \(\phi-\theta\) an integer multiple of \(\pi\), so (8) gives
\[
L_{\theta'}(G(\phi))=L_\theta(\phi)-h+2q\pmod N.
\]
The residue does not depend on the cone or the direction sign. ∎

## 4. Model chords pair the labels by a reflection

Take a direction parallel to polygon sides or diagonals. Equivalently, its real angle can be written \(\theta=h\pi/n\) with integer \(h\). Reflection in the polygon symmetry axis perpendicular to this direction pairs its vertices. At a vertex not fixed by that reflection, an inward ray goes straight along the chord to the reflected vertex. Convexity prevents a prior encounter with a side interior. At a fixed vertex the line in this direction is supporting, so there is no interior germ. Boundary germs give polygon sides.

Consequently every outgoing germ in this direction, across both polygons and all corners, ends after one polygon chord. Boundary rays may have two corner descriptions; they denote the same surface germ and satisfy the calculation below in either description.

**Lemma 3 (model matching).** The endpoint labels of every such chord obey
\[
a+b\equiv-h\pmod N.
\tag{9}
\]

**Proof.** Let its initial and final vertices be \(j,j'\) in the same polygon, its cone corner numbers be \(t,t'\), and let \(q\in\{1,\ldots,n-1\}\) represent \(j'-j\pmod n\). The initial and backward-final interior offsets are respectively
\((n-1-q)\pi/n\) and \((q-1)\pi/n\). Their sum is \(\delta\), hence
\[
\phi_u+\phi_v=(t+t'+1)\delta.
\]
The physical chord direction, taken modulo \(\pi\), gives
\(j+j'\equiv n-1-h\pmod n\). Since \(t\equiv j\) and \(t'\equiv j'\pmod n\), write \(t+t'+1=n-h+dn\). Then
\[
a+b=\frac{\phi_u+\phi_v-2\theta}{\pi}
=\frac{(n-h+dn)N-2h}{n}=(d+1)N-h.
\]
This proves (9). ∎

## 5. Classical reduction and endpoint reflection in every short direction

We use the following classical Veech results for odd \(n\geq5\) and even \(n\geq8\):

1. The double regular \(n\)-gon is a lattice translation surface
2. Every saddle-connection direction represents a parabolic cusp
3. There is one cusp orbit for odd \(n\), and two for even \(n\); representatives are polygon symmetry directions, with the two even representatives separated by \(\pi/n\)

Thus a single orientation-preserving affine automorphism takes any direction containing a saddle connection to a model direction of Section4. It acts on all germs in that direction, not separately on individual connections.

These are imported theorems, not conjectures of Fuchs. [Finster, arXiv:1005.4588v3](https://arxiv.org/abs/1005.4588v3), §§3.1–3.2, Remarks3.2/3.5 and p.20, reproduces the relevant group and cusp descriptions, crediting Veech's Theorem5.8. For even \(n\geq8\), §3.2 explicitly identifies the group of the **two-polygon** surface with the group under discussion; no unsupported transfer from the smaller opposite-side quotient is made. [Boulanger–Lanneau–Massart2024](https://www.numdam.org/articles/10.5802/ahl.211/), §1.4, gives the general saddle-connection/cusp correspondence and credits Veech. Its one-cusp polygon family is odd and is not applied to even polygons. The original [Veech1989](https://doi.org/10.1007/BF01388890) full text was not recovered here; the dependency is read in these complete later primary papers and remains explicitly credited.

**Lemma 4 (endpoint reflection).** For each physical direction \(\theta\) containing a short trajectory, all \(N\) outgoing germs end at vertices. Their matching with backward terminal germs has the form
\[
b=C_\theta-a\pmod N
\tag{10}
\]
for one residue \(C_\theta\).

**Proof.** Apply the single affine map supplied above. All model germs are finite chords by Section4. An inverse affine map preserves saddle connections and their first-vertex property, proving finiteness for every original germ. By Lemma2, both endpoint labels change by a common \(d\). Lemma3 therefore yields \((a+d)+(b+d)=-h\), or (10) with \(C_\theta=-h-2d\). ∎

## 6. The signed angle rule

First let \(\varepsilon=1\). Let \(\gamma\) start at \(P_0\) at angle \(\alpha\), with source type \(k\). Its initial label at reference \(\theta=\alpha\) is zero. By Lemma1 its backward label is \(k\), so Lemma4 has \(C_\alpha=k\).

There is an orientation-preserving isometry \(R_\ell\) of \(X_n\) rotating physical directions through \(-\ell\pi/n\). For odd \(n\), odd \(\ell\) exchanges the two polygons and even \(\ell\) preserves them. For even \(n\), our required even \(\ell\) is an ordinary polygon rotation. These operations respect the translation gluing.

Apply this isometry to the initial germ at \(P_0\) of angle \(\alpha'=\alpha+\ell\pi/n\). The resulting germ has physical direction \(\alpha\), and hence has a finite saddle connection by Lemma4. Pulling it back proves existence of the claimed short trajectory \(\gamma'\).

Suppose the rotated initial germ is at corner \(t\). Rotation preserves its interior offset \(\alpha'\), so its cone coordinate is \(t\delta+\alpha'\). Its label \(a\), relative to \(\alpha\), therefore satisfies
\[
a=(tN+\ell)/n,\qquad na=tN+\ell,
\qquad 2a\equiv\ell\pmod N.
\tag{11}
\]
The first expression is an integer because it is the germ label; equivalently, the physical-direction alignment verifies that integrality. The last step uses \(n=N+2\). **It does not divide by two modulo \(N\).**

The matching formula gives backward label \(b=k-a\). The intrinsic type of the rotated connection is consequently \(b-a=k-2a=k-\ell\). Lemma2 preserves that index under \(R_\ell\), and Lemma1 identifies it with the source type of \(\gamma'\). This proves (1) for \(\varepsilon=1\).

For \(\varepsilon=-1\), reflection in the angle bisector at \(O\) maps slope \(x\) to \(\delta-x\), and maps type \(k\) to \(-k\). To verify the latter directly from (2), the reflected angles are
\(\widetilde\alpha=\delta-\alpha\) and
\(\widetilde\beta=\pi+2\pi/n-\beta\), with segment parity unchanged. In the odd case \(\widetilde s=n-s\), yielding \(\widetilde k\equiv-k\); in the even case \(\widetilde s=2-s\), yielding the same result.

Now write
\[
\alpha'=\ell\pi/n-\alpha
=\delta-\big(\alpha+(N-\ell)\pi/n\big).
\]
The expression in parentheses belongs to \([0,\delta]\) whenever \(\alpha'\) does. Apply the positive rule with shift \(N-\ell\), then bisector reflection. The resulting type is
\(-[k-(N-\ell)]\equiv-k-\ell\pmod N\), as required. For even \(n\), \(N-\ell\) is even, so every applied rotation is permitted.

## 7. The elementary cases

For \(n=3\), there is only one type. Triangular-lattice unfolding shows that every allowed parallel angle has a first primitive vertex endpoint.

For \(n=4\), unfolding uses the square lattice. At the first endpoint the two coordinates are relatively prime; the type is \(A_1\) when both are odd, and \(A_0\) otherwise. The only nontrivial allowed angle change within the initial quadrant swaps the coordinates. It preserves this type, which is precisely (1) modulo two when \(\ell\) is even.

For \(n=6\), we retain the elementary case already proved by Fuchs on pp.511–512, with the following independent arithmetic replay to avoid relying on typographical labels in that prose. In the basis \((1,0),(-1/2,\sqrt3/2)\), let \(v=(p,q)\) be a primitive lattice direction. The first hexagon vertex is \(v\) if \(p+q\equiv0,1\pmod3\), and \(2v\) if \(p+q\equiv2\pmod3\). The type is
\[
K(v)=\begin{cases}
0,&p+q\equiv1\pmod3,\\
2,&p+q\equiv2\pmod3,\\
1,&(p,q)\equiv(1,2)\pmod3,\\
3,&(p,q)\equiv(2,1)\pmod3.
\end{cases}
\tag{12}
\]
These are Fuchs's explicit lattice classes on p.506. The missing residue pair \((0,0)\) is impossible for primitive \(v\).

Rotation by \(\pi/3\), namely \(R(p,q)=(p-q,p)\), satisfies
\(K(Rv)=K(v)-2\pmod4\). Bisector reflection \(B(p,q)=(q,p)\) satisfies \(K(Bv)=-K(v)\pmod4\). Both identities follow immediately by reducing their coordinate pairs modulo three; they also preserve primitivity. Iterating them gives (1) for all even \(\ell\), wherever the resulting angle lies in the initial sector. The first vertex is recomputed using (12), so no false assertion that the missing honeycomb residue is preserved is needed.

This completes the candidate proof for every \(n\geq3\).

## 8. Scope of the claim and checks

The new step beyond the previously reviewed ratio work is the common labelling of **all** outgoing and backward germs, followed by the endpoint-reflection identity and its common-shift transport. Type invariance alone would not prove this result.

The accompanying exact checker tests the coordinate and modular identities, model chords, angular alignment including even moduli, source type branches with segment parity, and the elementary cases. Finite tests do not prove the classical Veech theorems, the all-direction reduction, or the all-\(n\) result. Those depend on the geometric argument and imported results stated above. Separate adversarial review and novelty assessment remain necessary before any publication claim.
