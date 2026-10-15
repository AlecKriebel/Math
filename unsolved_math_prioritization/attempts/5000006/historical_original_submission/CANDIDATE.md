# Parallel short trajectories: a candidate proof of Fuchs's sine-ratio conjecture

**Status:** complete candidate, awaiting separate adversarial review. AI-generated and unrefereed; historical priority is unconfirmed. The proof uses the classical Veech-group and cusp theorems, with credit and access qualifications below.

## 1. Exact claim and source conventions

Let \(n\ge3\), and let a *short trajectory* in a regular Euclidean \(n\)-gon mean a billiard path from a vertex to the first subsequent vertex, reflecting in side interiors. Its Euclidean length is the sum of its segment lengths. Sides are included as limiting boundary trajectories, as in the source.

Fuchs's parallelism identifies unoriented directions under the polygon's dihedral symmetries: the sum or difference of the angles with a side is a multiple of \(2\pi/n\), modulo \(\pi\). The source's type \(A_k\) has \(k\in\mathbb Z/(n-2)\), represented by \(0,\ldots,n-3\). Set
\[
w_n(k)=\sin\frac{(k+1)\pi}{n}.
\]
Here and below this formula uses that canonical representative; it is not a periodic sine function of an arbitrary integer representative.

**Theorem.** If two parallel short trajectories have types \(A_k,A_\ell\), then
\[
\frac{L_k}{L_\ell}=\frac{w_n(k)}{w_n(\ell)}.
\tag{1}
\]
This is Conjecture 2.7 on printed p.512 of D. Fuchs, *Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra*, Arnold Mathematical Journal 7 (2021), 493–517. There is no small-length limit in the word “short.”

We use Definition 2.1 together with its immediately preceding reflection-parity convention, not the displayed angle equalities in isolation. Write \(\alpha\in[0,(n-2)\pi/n]\) for the initial interior angle and \(\pi-\beta\) for the terminal interior angle in Figure 8, so \(2\pi/n\le\beta\le\pi\). If the trajectory has \(N\) segments, its type is equivalently
\[
\begin{array}{ll}
N\text{ odd}:&
s=\dfrac{n(\alpha+\beta)}{2\pi}\in\mathbb Z,\qquad k\equiv n-1-s\pmod{n-2},\\[4pt]
N\text{ even}:&
s=\dfrac{n(\beta-\alpha)}{2\pi}\in\mathbb Z,\qquad k\equiv s-1\pmod{n-2}.
\end{array}
\tag{2}
\]
The inequality clauses in Definition 2.1 select the representative when these formulas wrap around. For example, in the sum case the conditions on \(\beta\) give
\[
\max\{0,(n-2k-2)\pi/n\}\le\alpha
\le\min\{(n-2)\pi/n,\,2(n-k-2)\pi/n\},
\]
which are exactly the two sum branches. In the difference case the two possibilities are \(s=k+1\) and \(s=k+3-n\), giving its two branches. At a polygon side the residues \(0\) and \(n-2\) agree. The sign must retain the stated parity when both a sum and a difference happen to be integral multiples; the source explicitly selects that sign before its definition.

We do not assume Conjectures 2.3, 2.4 or 2.6. Proposition 1.2's unlabelled length spectrum alone would not prove (1).

## 2. The double polygon and its angle circles

Let \(P\) be the polygon and \(Q=-P\) its half-turn. Label their vertices \(P_j,Q_j\), with indices modulo \(n\), clockwise and compatibly with this half-turn. Identify every side of \(P\) with its parallel side of \(Q\) by translation, reversing the endpoint order. Denote this translation surface by \(X_n\). For even \(n\) we still use **two** polygons; we do not replace this surface by the smaller opposite-side quotient.

The corner cycle beginning at \(P_0\) is
\[
P_0,\ Q_1,\ P_2,\ Q_3,\ldots .
\tag{3}
\]
Each corner contributes \(\delta=(n-2)\pi/n\). Thus, for odd \(n\), all vertices give one point with total angle \(2\pi(n-2)\), and the genus is \((n-1)/2\). For even \(n\), they give two points, each of angle \(2\pi r\), where \(r=(n-2)/2\), and the genus is \((n-2)/2\). The two classes are \(P_{\rm even},Q_{\rm odd}\) and \(P_{\rm odd},Q_{\rm even}\).

Ordinary billiard unfolding produces translates alternately of \(P\) and \(Q\). Passing each copy to \(X_n\) makes a short trajectory a saddle connection, preserving its length and excluding intermediate marked vertices. The first copy is \(P\); the terminal copy is \(P\) for odd \(N\), \(Q\) for even \(N\). Forgetting the individual reflected labels does not change the physical corner angle. This is the usual double-polygon quotient of the unfolding.

The map
\[
\iota:P\longleftrightarrow Q,\qquad z\longmapsto-z
\tag{4}
\]
is an affine involution with derivative \(-I\). It has exactly the \(n\) glued edge midpoints as regular fixed points; it also fixes the unique vertex point when \(n\) is odd, and exchanges the two vertex points when \(n\) is even. For \(n\ge5\) these counts are \(2g+2\). Riemann–Hurwitz shows that the quotient is a sphere, so \(\iota\) is the hyperelliptic involution.

Every orientation-preserving affine automorphism \(f\) of \(X_n\) commutes with \(\iota\). Indeed, \(f\iota f^{-1}\) has derivative \(-I\), hence is holomorphic in the translation complex structure, and is topologically conjugate to \(\iota\). It is therefore a hyperelliptic involution. The uniqueness of that involution on a compact Riemann surface of genus at least two gives equality. The same argument works for an orientation-reversing affine map: the conjugate still has complex-linear derivative \(-I\).

At a vertex point of angle \(2\pi r\), the circle of outgoing germs has an angular coordinate modulo \(2\pi r\). An orientation-preserving real-linear derivative \(A\) induces an increasing angular lift \(F\) with
\[
F(\theta+\pi)=F(\theta)+\pi,\qquad
F(\theta+2\pi)=F(\theta)+2\pi.
\tag{5}
\]
One can check (5) directly from \(A(-v)=-A(v)\), continuity and positive orientation. The lift on the cone can have an additional integral sheet offset; that offset cancels in differences at the same point.

## 3. An affine-invariant type index

Let \(\gamma\) be an oriented saddle connection, with outgoing start germ \(u\) and backwards-pointing end germ \(v\).

If its endpoints coincide, their Euclidean directions differ by \(\pi\), so there is a unique residue \(m\pmod r\) such that the positive angular difference from \(u\) to \(v\) is
\[
\pi+2\pi m\pmod{2\pi r}.
\tag{6}
\]
This includes every connection for odd \(n\).

For even \(n\), let \(e=0\) when the endpoints coincide and \(e=1\) when they are different. In the second case bring \(v\) to the start point by \(\iota\). Its direction now agrees with that of \(u\); define \(m\pmod r\) by
\[
\angle(u,\iota v)=2\pi m\pmod{2\pi r}.
\tag{7}
\]
Equations (5) and the commutation with \(\iota\) prove that \(m\), and also \(e\), are preserved by every orientation-preserving affine automorphism.

**Type identification.** The source type of \(\gamma\) is
\[
\begin{cases}
k\equiv2m+1\pmod{n-2},&n\text{ odd},\\
k\equiv2m+1-e\pmod{n-2},&n\text{ even}.
\end{cases}
\tag{8}
\]

Here is a corner-by-corner verification, including the endpoint identification in the even case. Normalize the starting corner to \(P_0\), with lower boundary angle zero. For odd \(n\), the index \(t\) of the terminal corner in (3) is even for \(P\), odd for \(Q\), and its lower-boundary cone angle is \(t\delta\). For even \(n\), use \(P_0\) as the start of its own cone cycle and \(Q_0=\iota P_0\) as the start of the other. In the latter case apply \(\iota\) to identify that cone with the starting one; again the lower-boundary cone angle is \(t\delta\). Terminal \(P\) then has \(t=2a+e\), and terminal \(Q\) has \(t=2a+1-e\).

At a terminal \(P\) corner the backward germ has interior offset \(\pi-\beta\). At a terminal \(Q\) corner reflection reverses the offset, giving
\(\delta-(\pi-\beta)=\beta-2\pi/n\).
Consequently, modulo the full cone angle,
\[
(1-e)\pi+2\pi m=
\begin{cases}
t\delta+\pi-(\alpha+\beta),&\text{terminal }P,\\
t\delta+(\beta-\alpha)-2\pi/n,&\text{terminal }Q.
\end{cases}
\tag{9}
\]
For odd \(n\) take \(e=0\) throughout.

For even \(n\), substituting \(t=2a+e\) in the first line gives
\[
mn=a(n-2)+e(n-1)-s.
\]
Since \(n\equiv2\pmod{n-2}\) and \(s\equiv1-k\), this gives \(2m\equiv e-1+k\). Substituting \(t=2a+1-e\) in the second line gives
\[
mn=a(n-2)+s+e-2,
\]
and \(s\equiv k+1\) gives the same conclusion. Changing the lift in (9) alters the integer equalities only by a multiple that vanishes in these congruences. For odd \(n\), the identical calculation with \(t=2a\) or \(2a+1\) and \(e=0\) gives \(2m\equiv k-1\pmod{n-2}\). This proves (8).

It follows that orientation-preserving affine maps preserve \(k\). Under orientation reversal, (6) changes \(m\) to \(-m-1\), while (7) changes \(m\) to \(-m\). The same changes follow on reversing the orientation of a connection, using \(\iota^2=1\) in the different-endpoint case. Thus these operations change \(k\) to \(-k\pmod{n-2}\).

Crucially,
\[
w_n(-k)=w_n(k).
\tag{10}
\]
For \(k\ne0\) this is the identity
\(\sin((n-1-k)\pi/n)=\sin((k+1)\pi/n)\); for \(k=0\) it is immediate. Hence the type **weight** is preserved under affine orientation changes and under all polygon dihedral isometries.

## 4. Reduction to single diagonals

We invoke the following classical Veech facts for the double regular polygon, for odd \(n\ge5\) and even \(n\ge8\):

1. It is a lattice translation surface.
2. Every saddle-connection direction is a parabolic direction.
3. For odd \(n\), its Veech group has one cusp, represented by a polygon symmetry direction. For even \(n\), it has two cusps, represented by the two adjacent symmetry directions, separated by \(\pi/n\).

Therefore an orientation-preserving affine automorphism sends any given saddle-connection direction to one of those model directions. This is a direction statement: the **same** automorphism acts on every connection in that direction.

These are the Veech-group calculation and cusp theorem, not conjectures from Fuchs. The group calculation is explicitly reproduced, with attribution to Veech's Theorem 5.8, in Finster, §§3.1–3.2 and Remark 3.5; her even-surface discussion explicitly identifies the Veech group of the two-polygon cover. Her p.20 describes the two cusp representatives. The saddle-connection/cusp correspondence is also stated in Boulanger–Lanneau–Massart, §1.4. Exact access qualifications are in the source audit.

In a model direction, every saddle connection is a side or diagonal lying in one polygon. To see this without a length-spectrum assertion, reflect a polygon in its symmetry axis perpendicular to the direction. A vertex not on the axis has a distinct reflected vertex. The line through those two vertices cuts the convex polygon in exactly their chord; an inward ray therefore reaches that reflected vertex before it can reach any side interior. At a vertex on the axis the parallel line is supporting and there is no interior ray. Boundary rays are sides. Applying this to every corner of \(P\) and \(Q\) exhausts the saddle connections.

The direct chord from \(P_0\) to \(P_j\), \(1\le j\le n-1\), has length
\[
2R\sin(j\pi/n),
\tag{11}
\]
where \(R\) is the circumradius. In the source's angles,
\[
\alpha=(n-1-j)\pi/n,\qquad
\beta=(n+1-j)\pi/n.
\]
It has one segment, so (2) gives \(k\equiv j-1\pmod{n-2}\). This also covers \(j=n-1\), the second side of type \(A_0\). Thus every model connection satisfies
\[
L=2R\,w_n(k).
\tag{12}
\]
Rotating its initial vertex to \(P_0\), or exchanging \(P,Q\), preserves the weight by the preceding section.

If \(D f=A\) and two connections have a common unoriented direction represented by a unit vector \(v\), both lengths are multiplied by \(\|Av\|\). Their type weights are preserved. Transporting them to the model direction and using (12) proves (1) for that direction.

Finally, Fuchs-parallel directions can be aligned by a polygon dihedral isometry, allowing reversal of the connection. For odd \(n\), angles modulo \(\pi\) also permit the half-step \(\pi/n\); the double polygon has the isometry rotating by \(\pi/n\) and exchanging its polygons. For even \(n\), only steps \(2\pi/n\) are needed. All these isometries preserve lengths and weights. This establishes exactly the source's broader parallelism, not only identical unfolded slopes.

## 5. The three elementary cases

For \(n=3\), unfold into the triangular lattice. The first vertex on a ray is its primitive lattice point. The direction symmetries preserve this lattice and primitivity, so parallel short trajectories have equal length. There is only type \(A_0\).

For \(n=4\), the same argument uses the square lattice. Types are \(A_1\) when both primitive coordinates are odd and \(A_0\) otherwise, as in Fuchs §2.3. Square symmetries preserve this parity condition, so a parallel family has one weight and one length.

For \(n=6\), use the triangular-lattice basis \((1,0),(-1/2,\sqrt3/2)\). The vertices of the developed hexagons are the integer points with \(p+q\not\equiv2\pmod3\). Let \(v=(p,q)\) be primitive in the full triangular lattice and put \(s=p+q\pmod3\). The first hexagon vertex on its positive ray is \(v\) if \(s=0,1\), and \(2v\) if \(s=2\). The source's explicit type rule in §2.3 gives:
\[
\begin{array}{c|c|c|c}
s&\text{endpoint}&\text{type}&w_6\\ \hline
0&v&A_1\text{ or }A_3&\sqrt3/2\\
1&v&A_0&1/2\\
2&2v&A_2&1
\end{array}
\]
The triangular-lattice dihedral symmetries preserve the norm and primitivity and send \(s\) to \(s\) or \(-s\); for example their generators \((p,q)\mapsto(q,p)\) and \((p,q)\mapsto(p-q,p)\) do so. Thus a parallel family with \(s=0\) has constant length and weight. In the other family, \(L/w_6=2\|v\|\) in either residue case. This proves (1) for the hexagon and completes the proof.

## 6. Scope and evidence

The argument resolves the labelled ratio asserted in Conjecture 2.7 if its angle-index identification and classical-theorem application survive independent review. It does not claim a proof of the neighbouring reachable-polygon or type-distribution conjectures, nor a new proof of Veech's theorems.

The exact verifier checks polygon vertex identifications, genera and involution fixed-point counts; the two parity-sensitive angle-index formulas; direct-chord labels; representative-sensitive reversal of the sine weight; and the primitive-lattice cases. Such finite controls support the proof but do not replace the geometric arguments or the imported theorems.

The search performed for this attempt found the source conjecture and relevant classical translation-surface results, but did not establish historical priority. All novelty and human-peer-review claims remain withheld.

## References

- D. Fuchs, [Billiard Trajectories in Regular Polygons and Geodesics on Regular Polyhedra](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf), Arnold Math. J. 7 (2021), 493–517; §§1.1, 2.2–2.3, Conjecture 2.7.
- W. A. Veech, [Teichmüller curves in moduli space, Eisenstein series and an application to triangular billiards](https://doi.org/10.1007/BF01388890), Invent. Math. 97 (1989), 553–583. The underlying group and cusp theorems are credited to this paper; its full text was not retrieved in this attempt.
- M. Finster, [A series of coverings of the regular n-gon](https://arxiv.org/abs/1005.4588), arXiv:1005.4588v3 (2011), §§3.1–3.2, Remarks 3.2 and 3.5, p.20. Full text retrieved and the relevant group formulas checked.
- J. Boulanger, E. Lanneau and D. Massart, [Algebraic intersection for a family of Veech surfaces](https://www.numdam.org/item/10.5802/ahl.211.pdf), Ann. H. Lebesgue 7 (2024), §1.4 and §2.3. The relevant family here is odd double polygons; it is not used as an even-polygon theorem.

