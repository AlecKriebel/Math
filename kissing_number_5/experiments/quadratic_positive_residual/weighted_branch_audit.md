# Weighted-isotropy branch: exact identities and the remaining gap

## Scope warning

Proving the quadratic-positive-locus statement would show only that a
hypothetical 41-point kissing code admits weights
\[
p_i\geq0,\qquad \sum_i p_i=1,\qquad
\sum_i p_ix_i=0,\qquad
\sum_i p_ix_ix_i^{\mathsf T}=\frac15I.
\tag{1}
\]
It would **not** prove that the weights are positive or uniform.  Therefore
it would not imply that the unweighted code is centered or a unit-norm
tight frame.  The unweighted centered/tight full-matrix identity cannot be
used on this branch.

There is currently no exact contradiction or extension theorem for (1).
Thus QPL is a certified branch reduction, not a complete route to
\(\tau(5)\leq40\).

## 1. Exact weighted Gram identities

Let \(X\) have rows \(x_i^{\mathsf T}\), let
\(G=XX^{\mathsf T}\), and put \(P=\operatorname{diag}(p)\).
Equation (1) gives
\[
Gp=0,\qquad GPG=\frac15G.
\tag{2}
\]
Conversely, for a rank-five Gram matrix, (2), unit diagonal, and
\(\sum p_i=1\) recover (1).

The symmetric matrix
\[
H=5P^{1/2}GP^{1/2}
\tag{3}
\]
is an orthogonal projection of rank five:
\[
H^2=H,\qquad H\succeq0,\qquad
H_{ii}=5p_i,\qquad H\sqrt p=0.
\tag{4}
\]
For positive weights the kissing constraint is
\[
H_{ij}\leq\frac52\sqrt{p_ip_j}\qquad(i\ne j).
\tag{5}
\]
Zero-weight points disappear from \(H\), which is precisely why the
projection identity alone cannot control arbitrary extra points.

Adjoining the constant coordinate gives a second useful projection.  Put
\[
S=P^{1/2}(J+5G)P^{1/2}.
\]
With \(r=\sqrt p\), this is
\[
S=rr^{\mathsf T}+H,\qquad S^2=S,\qquad \operatorname{rank}S=6.
\]
Its complementary weighted stress, pulled back through \(P^{1/2}\), is
\[
\Omega=P-pp^{\mathsf T}-5PGP\succeq0,\qquad \Omega{\bf1}=0.
\tag{5a}
\]
The entries are
\[
\Omega_{ii}=p_i(1-6p_i),\qquad
\Omega_{ij}=-p_ip_j(1+5G_{ij}).
\tag{5b}
\]
If every positive-support inner product is at least \(-1/5\), then
\(\Omega\) is an ordinary weighted graph Laplacian.  On full support its
nullity six forces exactly six connected components in the graph of pairs
with \(G_{ij}>-1/5\); all cross-component inner products equal \(-1/5\).
This is a structural alternative, not a contradiction—the regular
six-point simplex is its smallest model.

Define
\[
B=I+J-2G.
\]
Then \(B_{ii}=0\), \(0\leq B_{ij}\leq3\), and exact expansion of (2) gives
\[
Bp={\bf1}+p,
\tag{6}
\]
\[
\boxed{
BPB=PB+BP-P+\frac25I+\frac75J-\frac25B.
}
\tag{7}
\]
If \(p_i=1/41\), multiplying (7) by 41 recovers
\[
B^2=\frac{77}{5}I+\frac{287}{5}J-\frac{72}{5}B.
\]
For nonuniform \(p\), (7), not the unweighted equation, is the valid
common-source identity.

## 2. Universal exact weight bounds

Fix \(i\), and regard \(T=\langle x_i,X\rangle\) under the probability
weights \(p\).  Then
\[
\mathbb E T=0,\qquad \mathbb E T^2=\frac15,
\]
and the atom \(x_i\) contributes \(p_i\) at \(T=1\).  The conditional
variance of the remaining atoms is nonnegative:
\[
\frac{1/5-p_i}{1-p_i}
-\left(\frac{-p_i}{1-p_i}\right)^2\geq0.
\]
Hence
\[
\boxed{p_i\leq\frac16.}
\tag{8}
\]
This improves the elementary projection-diagonal bound \(p_i\leq1/5\),
but permits support as small as six.  It is sharp: the regular simplex in
\(S^4\), with six weights \(1/6\) and all off-diagonal inner products
\(-1/5\), is an exact weighted kissing code.

There is also an exact weighted depth statement.  For every \(u\in S^4\),
put \(T=\langle u,X\rangle\) and
\[
\alpha_-=\sum_{\langle u,x_i\rangle<-1/50}p_i.
\]
The polynomial
\[
\phi(t)=(t+1/50)(1-t)
\]
is nonnegative on \([-1/50,1]\), at least \(-49/25\) on \([-1,-1/50]\),
and has expectation
\[
\mathbb E\phi(T)=\frac1{50}-\frac15=-\frac9{50}.
\]
Therefore
\[
\boxed{\alpha_-\geq\frac9{98}.}
\tag{9}
\]
Applying the same argument to \(-u\) gives weighted mass at least \(9/98\)
above \(+1/50\).

At the natural stress threshold \(-1/5\), a base-point-dependent statement
is available.  For a positive-weight point \(x_i\), set
\[
\alpha_i=\sum_{j:G_{ij}<-1/5}p_j.
\]
On \([-1/5,1/2]\), the polynomial
\[
h(t)=(t+1/5)(1/2-t)
\]
is nonnegative, while on \([-1,-1/5]\) it is at least \(-6/5\).  The
weighted row moments give
\[
\sum_{j\ne i}p_jh(G_{ij})=\frac{6p_i-1}{10}.
\]
Consequently
\[
\boxed{\alpha_i\geq\frac{1-6p_i}{12}.}
\tag{9a}
\]
If \(p_i<1/6\), every positive-weight vertex therefore has a neighbor with
inner product below \(-1/5\).  Equality \(p_i=1/6\) in the variance bound
forces every other positive-weight point to have inner product exactly
\(-1/5\) with \(x_i\).

For a 41-point kissing code, the exact enlarged-cap theorem separately
forces at least two points below \(-1/50\) in every direction.  Combining
this count with (8)--(9) does not contradict feasibility: one or several
weights of size at most \(1/6\) can carry mass \(9/98\).

This failure has an exact code-axis relaxation countermodel.  Give all 41
vertices weight \(1/41\), and join vertex \(i\) to
\(i\pm1,i\pm2\pmod {41}\).  Every vertex has four deep neighbors and deep
weight mass
\[
\frac4{41}>\frac9{98},
\]
while every individual weight is below \(1/6\).
`verify_local_depth_weight_countermodel.py` checks this exactly.  It is not
a Gram matrix, but it proves that the current local count, mass, symmetry,
and individual-weight inequalities cannot by themselves close the branch.
The same graph also satisfies (9a): for \(p_i=1/41\), its required
\(-1/5\)-deep mass is \(35/492\), while its four neighbors carry
\(4/41=48/492\).

## 3. Exact counterexamples to uniform-weight assumptions

The \(D_5\) kissing code admits many nonuniform exact weighted two-designs.
Give every one of the four sign choices on support edge \(\{i,j\}\) the
same weight \(w_{ij}\).  Centering and vanishing off-diagonal covariance
are automatic, while isotropy is exactly
\[
\sum_{j\ne i}w_{ij}=\frac1{10}\qquad(1\leq i\leq5).
\tag{10}
\]

Starting from \(w_{ij}=1/40\), add \(\delta=1/200\) on edges
\(\{1,2\},\{3,4\}\) and subtract it on
\(\{1,3\},\{2,4\}\).  Equation (10) is unchanged, all 40 point weights are
positive, and the weights take the three distinct values
\[
\frac3{100},\qquad\frac1{40},\qquad\frac1{50}.
\]
Thus even an exact 40-point kissing code with full-support design weights
does not force uniformity.

Taking \(\delta=1/40\) instead sets eight point weights to zero and gives
an exact weighted two-design supported on only 32 of the \(D_5\) roots.
An even sparser exact weighting stored in the verifier uses only 12 roots:
eight have weight \(1/10\), four have weight \(1/20\), and the other 28
points of the 40-point code have weight zero.  Consequently, claims that
(1) forces full support, support near 41, or uniform weights are false.

`verify_weighted_branch_identities.py` checks these examples and (6)--(7)
with exact `Fraction` arithmetic.

Independently, Carathéodory's theorem applied to the 19-dimensional feature
map \((x,xx^{\mathsf T}-I/5)\) says that whenever (1) is feasible, some
feasible weighting has support at most 20.  Hence a proof may always
stratify the weighted branch as a 6-to-20 point weighted design support plus
at least 21 zero-weight points.  The exact 40-point \(D_5\) example with
support 12 shows that this support/extension formulation is not artificial.

## 4. Numerical attack using unrestricted near-minimizers

`analyze_near_minimizers.py` recursively collected 132 distinct 41-point
coordinate arrays from independent construction folders, including the
best current unrestricted input with maximum inner product
`0.514994652512166`.

All 132 admit floating-point nonnegative weighted two-designs.  More
strongly, all 102 arrays with maximum inner product below `0.55` admit
full-support weights with a common lower floor between
`0.0204426384` and `0.0243902439`.  The best input has maximum common
weight floor `0.0217560797`, close to the uniform value \(1/41\).

These calculations are numerical evidence only, and many searches inherit
centering/tight-frame bias.  They nevertheless show that the persistent
near-minimizers lie robustly in the weighted-isotropy branch, not near the
quadratic-separation branch.  Any complete strategy must attack (2) or
(7), including nonuniform and zero-weight cases.

## 5. Precise unresolved theorem

Rule out \(N=41\) matrices and weights satisfying
\[
\begin{gathered}
G\succeq0,\quad \operatorname{rank}G=5,\quad G_{ii}=1,\quad
G_{ij}\leq1/2,\\
p\geq0,\quad {\bf1}^{\mathsf T}p=1,\quad
Gp=0,\quad GPG=G/5.
\end{gathered}
\tag{11}
\]
Equivalently, rule out the weighted projection formulation (3)--(5),
while retaining the unit Gram realization of zero-weight points.

No current artifact proves (11) infeasible.
