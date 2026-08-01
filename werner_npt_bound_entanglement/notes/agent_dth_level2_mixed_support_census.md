# Exact mixed-support census for the degree-three DTH lift

## Result

At one physical qutrit site, partial transpose on the anchored bivector
changes the local seven-replica space into

\[
\mathcal V_{2,5}=\bar{\mathbb C}^{3\,\otimes2}
\otimes\mathbb C^{3\,\otimes5}.
\]

The prolonged support map is the evaluation

\[
E:\mathcal V_{2,5}\longrightarrow
\mathcal V_{1,4}=\bar{\mathbb C}^3\otimes\mathbb C^{3\,\otimes4},
\]

\[
E(\bar e_a\otimes\bar e_b\otimes r\otimes e_z)
=\delta_{a,z}\,\bar e_b\otimes r.
\tag{1}
\]

This note gives the complete exact highest-weight census of (1).  The
companion verifier is
`verification/verify_dth_level2_mixed_support_census.py`.

## 1. Mixed source and target decompositions

Label irreducible rational (U(3)) types by their (SU(3)) Dynkin labels
\((p,q)\).  Exact rational raising-operator elimination gives the source
multiplicities

\[
\begin{array}{c|rrrrrrrrrr}
(p,q)&(5,2)&(6,0)&(3,3)&(4,1)&(1,4)&(2,2)&(3,0)&(0,3)&(1,1)&(0,0)\\ \hline
m_{2,5}&1&1&4&10&5&24&20&15&36&11.
\end{array}
\tag{2}
\]

The carrier dimensions are respectively

\[
81,28,64,35,35,27,10,10,8,1.
\]

They satisfy the two independent dimension audits

\[
\sum_{p,q}d_{p,q}m_{2,5}(p,q)=2187=3^7,
\qquad
\sum_{p,q}m_{2,5}(p,q)^2=2761.
\tag{3}
\]

The target multiplicities are

\[
\begin{array}{c|rrrrrr}
(p,q)&(4,1)&(2,2)&(3,0)&(0,3)&(1,1)&(0,0)\\ \hline
m_{1,4}&1&3&4&2&8&3.
\end{array}
\tag{4}
\]

Here

\[
\sum_{p,q}d_{p,q}m_{1,4}(p,q)=243=3^5,
\qquad
\sum_{p,q}m_{1,4}(p,q)^2=103.
\tag{5}
\]

Thus the local crossed commutant has dimension (2761), while the support
output commutant is the same (103)-dimensional mixed algebra that appears
in the five-replica crossing.

## 2. Exact support ranks

Applying (1) to exact rational highest-weight bases gives

\[
\operatorname{rank}E_{p,q}=m_{1,4}(p,q)
\tag{6}
\]

for every target type.  On the four source-only types

\[
(5,2),\ (6,0),\ (3,3),\ (1,4)
\]

the rank is zero.  Hence every target multiplicity map is surjective.  In
particular, the exact kernel multiplicities on the six common types are

\[
9,21,16,13,28,8,
\tag{7}
\]

in the order used in (4), in addition to all multiplicities of the four
source-only types.

This accounts for

\[
\operatorname{rank}E=243,
\qquad
\dim\ker E=2187-243=1944.
\tag{8}
\]

## 3. Uniform normalization and the exact kernel projector

The raw word formula (1) has the particularly useful identity

\[
\boxed{EE^\dagger=3I_{243}.}
\tag{9}
\]

Indeed, every target word has exactly three mutually orthogonal preimages,
obtained by choosing the contracted qutrit value.  Consequently

\[
P_{\operatorname{ran}E^\dagger}=\frac13E^\dagger E,
\qquad
\boxed{P_{\ker E}=I-\frac13E^\dagger E.}
\tag{10}
\]

For the three physical qutrit sites, the global prolonged support map is the
tensor product

\[
\mathcal C_{S,3}=E^{\otimes3}
\]

after the fixed replica reordering.  Therefore

\[
\mathcal C_{S,3}\mathcal C_{S,3}^\dagger=27I,
\qquad
P_{\ker\mathcal C_{S,3}}
=I-\left(\frac13E^\dagger E\right)^{\otimes3}.
\tag{11}
\]

For a positive crossed moment (R=T^{\Gamma_A}\), the support equation is
equivalent to any of

\[
\mathcal C_{S,3}R\mathcal C_{S,3}^\dagger=0,
\quad
\mathcal C_{S,3}R=0,
\quad
R=P_{\ker\mathcal C_{S,3}}R P_{\ker\mathcal C_{S,3}}.
\tag{12}
\]

Equation (11) is a lossless source-union representation of the mixed support
face.  It does not prove feasibility or positivity of the complete
constrained lift; it removes the need for a singular-value cutoff or a
framewise support estimate when that lift is assembled.

## 4. Residual bivector-pair symmetry

After partial transpose on the anchored bivector, interchange of the two
unanchored bivectors remains an ordinary linear involution.  In the ordering
used in (1), its local source permutation is

\[
(0,1,2,3,4,5,6)\longmapsto(0,1,4,5,2,3,6),
\tag{13}
\]

and on the support target it is

\[
(0,1,2,3,4)\longmapsto(0,3,4,1,2).
\tag{14}
\]

Exact restriction to the rational highest-weight bases gives the source
traces

\[
\begin{array}{c|rrrrrrrrrr}
(p,q)&(5,2)&(6,0)&(3,3)&(4,1)&(1,4)&(2,2)&(3,0)&(0,3)&(1,1)&(0,0)\\ \hline
\operatorname{Tr}\tau_{2,5}&1&1&0&2&1&0&0&3&0&-1,
\end{array}
\tag{15}
\]

and the target traces

\[
\begin{array}{c|rrrrrr}
(p,q)&(4,1)&(2,2)&(3,0)&(0,3)&(1,1)&(0,0)\\ \hline
\operatorname{Tr}\tau_{1,4}&1&-1&0&2&0&-1.
\end{array}
\tag{16}
\]

The evaluation map intertwines these involutions.  Over the union of all
three-site highest-weight multiplicity blocks, the exact dimensions of the
global (+1) source, its support range, and its support kernel are therefore

\[
\boxed{1,024,363,\qquad4,631,\qquad1,019,732.}
\tag{17}
\]

For example, the first number is

\[
\frac{127^3+7^3}{2},
\]

because the sum of source multiplicities is (127) and the sum of their
swap traces is (7).  The range count is

\[
\frac{21^3+1^3}{2}.
\]

These are source-union counts, not the dimension of the crossed image of the
post-Omega holomorphic cone.  The partial-transpose crossing still links the
two cones and can impose a much smaller effective affine slice.

## 5. Verification scope

The verifier uses only exact rational sparse elimination.  It independently
constructs every source and target highest-weight vector from the two
raising equations, evaluates (1), checks all highest-weight ranks, and
checks (9) on all (3^5) raw target words.

This is an exact local representation theorem.  For the actual fixed-marginal
extension problem, the tensor-product face (11) need not be imposed as a
separate constraint.  The theorem in
`notes/agent_dth_prolonged_face_automatic.md` shows that, once the fixed
five-replica marginal is already on its support face, positivity after
\(\Gamma_A\) forces the prolonged support face automatically.  Operationally,
the next global task is therefore to combine the crossed
\(2761\)-coordinate bridge with the fixed marginal and the grouped PPT
cones.  Equations (9)--(17) remain independent normalization and block-census
audits of that crossing.
