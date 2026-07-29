# Unrestricted three-copy unshifted-minor falsifier and boundary audit

**Status, 2026-07-28.**  This note does not prove or disprove unrestricted
three-copy positivity.  It records five exact structural results:

1. the live unshifted determinant is a four-replica compound expectation;
2. a natural Cauchy--Schwarz/Monge proof loses an exact factor \(64\) at a
   true equality point;
3. the corrected exterior defect is exactly the *crossed evaluation* of
   the already proved strong positive-rank-two defect kernel;
4. at the canonical genuinely nonnormal zero, the complete constrained
   Hessian is positive semidefinite and the first unresolved local term is
   quartic on a \(55\)-dimensional explicitly certified flat space;
5. that entire \(55\)-variable quartic is a rational weighted sum of
   squares.

The exact checkers are

- `verification/verify_n3_unshifted_sector_obstructions.py`;
- `discovery/analyze_n3_unshifted_boundary.py`.
- `verification/verify_n3_boundary_flat_quartic_sos.py`.

## 1. The live crossed minor

Put
\[
 N=\bigotimes_{i=1}^3(2I-F_i).
\]
For orthonormal two-frames \(U=(u_1,u_2)\) and \(V=(v_1,v_2)\), define
\[
\begin{aligned}
a_1&=\langle u_1\otimes v_1,N(u_1\otimes v_1)\rangle,\\
a_2&=\langle u_2\otimes v_2,N(u_2\otimes v_2)\rangle,\\
h&=\langle u_1\otimes v_2,N(u_2\otimes v_1)\rangle .
\end{aligned}
\]
The unshifted two-plane target is
\[
 \boxed{\qquad |h|^2\leq a_1a_2. \qquad}                 \tag{1}
\]
It is exactly the relevant \(2\times2\) principal minor of
\[
 \bigl[(U^\dagger\otimes V^\dagger)N(U\otimes V)\bigr]^{\Gamma_2}.
\]

There is a useful four-replica formula.  Label the replicas by
\[
 1=u_1,\quad 2=u_2,\quad 3=v_1,\quad 4=v_2
\]
and write
\[
 z=u_1\otimes u_2\otimes v_1\otimes v_2.
\]
Then
\[
\boxed{
a_1a_2-|h|^2
=\langle z,\,[N_{13}N_{24}
-N_{14}N_{23}F_{12}F_{34}]\,z\rangle .
}                                                        \tag{2}
\]
Indeed the first term factorizes as \(a_1a_2\).  Acting first with
\(F_{12}F_{34}\), the two disjoint matrix elements of the second term
are \(h\) and \(\overline h\).

At one physical site put
\[
\begin{aligned}
p&=(2I-F_{13})(2I-F_{24}),\\
r&=(2I-F_{14})(2I-F_{23})F_{12}F_{34}.
\end{aligned}
\]
Thus the operator in (2) is
\[
 p^{\otimes3}-r^{\otimes3}.                              \tag{3}
\]
Neither \(p-r\) nor \(p+r\) is positive as an operator; orthogonality
and the common four-corner origin of \(z\) are essential.

## 2. Exact obstruction to crossed-energy Monge

Ordinary Cauchy--Schwarz in the \(N\)-inner product gives
\[
 |h|^2
 \leq
 a_{12}a_{21},\qquad
 a_{rs}=\langle u_r\otimes v_s,N(u_r\otimes v_s)\rangle .
                                                               \tag{4}
\]
It is tempting to finish with
\[
 a_{12}a_{21}\stackrel?{\leq}a_{11}a_{22}.                \tag{5}
\]
This route is maximally false at the simplest equality code.  Take
\[
 u_1=v_1=|000\rangle,\qquad
 u_2=v_2=|111\rangle .
\]
For computational strings,
\[
 \langle x\otimes y,N(x\otimes y)\rangle
 =2^{d_H(x,y)}.
\]
Also the crossed matrix element factorizes locally.  Hence
\[
 a_{11}=a_{22}=1,\qquad
 a_{12}=a_{21}=8,\qquad h=(-1)^3=-1.                     \tag{6}
\]
The true target (1) is saturated:
\[
 |h|^2=a_{11}a_{22}=1,
\]
whereas (5) would require \(64\leq1\).  Thus no proof may replace the
crossed matrix element by its two ordinary Cauchy--Schwarz norms and
then compare only those norms.  Its coherent swap phase is indispensable.

## 3. The target sector operator is a crossed strong-PSD defect

Use the singular-value purification
\[
\begin{aligned}
|\mathsf A\rangle&=\sum_{r=1}^2\sqrt{s_r}|r\rangle_K|u_r\rangle,\\
|\mathsf B\rangle&=\sum_{r=1}^2\sqrt{s_r}|r\rangle_K|v_r\rangle,
\end{aligned}
\]
whose two \(K\)-marginals coincide.  On
\(z=\mathsf A\otimes\mathsf B\), let \(k\) be the auxiliary
antisymmetric bit and let \(r\) count antisymmetric physical replica
pairs.  The corrected sharp defect has coefficient table
\[
\begin{array}{c|rrrr}
 &r=0&r=1&r=2&r=3\\ \hline
k=0&0&1&4&13\\
k=1&1&0&-3&-12 .
\end{array}                                               \tag{7}
\]

This table has an exact conceptual identification.  For a single
purification \(W\), put \(H=\operatorname{Tr}_K|W\rangle\langle W|\).
The sector eigenvalue of \(8Q_3(H)\) is
\[
 (-1)^k3^r.
\]
The sector eigenvalue of
\[
 2\operatorname{Tr}H^2-(\operatorname{Tr}H)^2
\]
is \(2(-1)^k-1\).  Therefore the strong-PSD defect kernel is
\[
 G_{\rm psd}
 =F_K\prod_{i=1}^3(2I-F_i)-2F_K+I                       \tag{8}
\]
with coefficient
\[
 g(k,r)=(-1)^k(3^r-2)+1.                                 \tag{9}
\]
Its two rows are
\[
 (0,2,8,26),\qquad(2,0,-6,-24),
\]
exactly twice (7).  Consequently the unrestricted sharp problem is
precisely
\[
 \boxed{\qquad
 \langle\mathsf A\otimes\mathsf B,
 G_{\rm psd}(\mathsf A\otimes\mathsf B)\rangle\geq0
 \qquad}                                                  \tag{10}
\]
for two purifications with equal \(K\)-marginal.  The established
positive-rank-two theorem proves only the diagonal case
\(\mathsf B=\mathsf A\).

This isolates the genuinely missing principle: crossed positivity of
the strong-defect kernel under equality of one qubit marginal.

### A grouped-sector cone obstruction

Three natural ways to import the three-block projector defect
\[
 f(w)=\mathbf1_{\{w=2\}}-3\mathbf1_{\{w=3\}}
\]
give, after summing over the three physical choices, the following
coefficient rows:
\[
\begin{array}{c|cc}
 &k=0&k=1\\ \hline
(Ki)|j|l &(0,0,3,-9)&(0,2,-3,3)\\
K|(ij)|l &(0,0,2,0)&(0,3,-6,3)\\
\text{omit }i\text{ and use }K|j|l
 &(0,0,1,3)&(0,2,-1,-9).
\end{array}                                               \tag{11}
\]
No nonnegative combination of these rows, plus coordinatewise
nonnegative sector masses, equals (7).  At \((k,r)=(1,1)\), the target
coefficient is zero while the three generator coefficients are
\(2,3,2\).  All three multipliers would therefore have to vanish, after
which the negative target coefficients at \((1,2)\) and \((1,3)\)
cannot be generated.

Because the target is physical-permutation invariant, averaging any
putative certificate made from the individual unsymmetrized generators
would give such a symmetric certificate.  Thus a grouped proof needs
phase-sensitive or genuinely nonlinear squares; sector-diagonal grouped
defects alone do not suffice.

## 4. Exact constrained Hessian at the canonical nonnormal zero

In any local dimension \(d\geq2\), one can embed the canonical zero
\[
 C_0
 =|000\rangle\langle110|
  +|001\rangle\langle111|
 =|0\rangle\langle1|\otimes|0\rangle\langle1|\otimes P_2.
                                                               \tag{12}
\]
It is a rank-two partial isometry and \(Q_3(C_0)=0\).

Parameterize the manifold of rank-two partial isometries as
\[
 C(t)=U(t)V(t)^\dagger
\]
using independent polar Stiefel retractions of the two frames.  A
horizontal variation of either \(d^3\times2\) frame contributes
\(4d^3-8\) real coordinates, and the relative logical
\(\mathfrak u(2)\) rotation contributes four, for a total of
\[
 8d^3-12.
\]

For \(d=2,3,4,5\), exact computational-basis construction gives
\[
\begin{aligned}
\operatorname{rank}\operatorname{Hess}_{C_0}Q_3
 &=8d^3-4d^2-4d-19,\\
\operatorname{nullity}\operatorname{Hess}_{C_0}Q_3
 &=4d^2+4d+7,
\end{aligned}
                                                               \tag{13}
\]
and the Hessian is positive semidefinite in each of those four
dimensions.  Its
nonzero graph splits into positive rank-one blocks with the following
complete profile:

\[
\begin{array}{c|c|c}
\text{block size}&\text{positive pivot}&\text{multiplicity}\\\hline
4&1/4&4\\
4&1/8&2\\
2&1&4(d-2)\\
2&1/2&4(d-1)^2+5\\
2&1/4&8d-12\\
1&1&8d(d-1)(d-2)\\
1&1/2&16d(d-2)\\
1&1/4&8(d-2)\\
1&2&2.
\end{array}                                                \tag{14}
\]
Zero-multiplicity rows are omitted when \(d=2\).  Summing the table gives
the rank and nullity in (13).  For \(d=3\), these specialize to \(204\)
coordinates, \(149\) positive directions, and \(55\) flat directions.

The observed block classification has a dimension-independent
equality-pattern explanation: the matrix-unit pairing in (15) depends
only on whether each tangent label equals \(0\), equals \(1\), or lies
outside the base support.  Formula (14) is therefore a natural uniform
conjecture, but a written all-\(d\) enumeration proof has not yet been
completed.  The verifier accepts the local dimension through the
environment variable `N3_LOCAL_DIMENSION`; dimensions \(2,3,4,5\) were
each checked with exact arithmetic.  Only the \(d=3\) specialization is
used as a proved theorem below.

The verifier constructs every entry directly from
\[
\mathcal B_3(E_{ab},E_{cd})
=\sum_{S\subseteq[3]}(-1/2)^{|S|}
\langle\operatorname{Tr}_S E_{ab},
\operatorname{Tr}_S E_{cd}\rangle                         \tag{15}
\]
using dyadic rational arithmetic, and checks the rank-one identity for
every block.

For the first genuinely higher-dimensional case \(d=3\), there is no
hidden cubic escape.  Exact polarization of all
\(\binom{55+3-1}{3}=29260\) cubic coefficients gives
\[
 \boxed{\qquad
 D^3Q_3(C_0)[x,x,x]=0
 \quad\text{for every Hessian-flat tangent }x.
 \qquad}                                                   \tag{16}
\]
Thus the first possible local sign change is the quartic form on this
explicit \(55\)-dimensional kernel.  In the certificate's sparse kernel
basis, 49 coordinate directions have zero quartic coefficient and six
have coefficient \(1\).  This coordinate statement is not a proof that
the full quartic is nonnegative: mixed quartic terms remain the exact
local frontier.

The conclusion is rigorous but local.  Exact checks through local
dimension five show that adding new local levels creates no negative
quadratic direction at this boundary; at \(d=3\) the result also rules
out every cubic bifurcation.  Thus this analysis
does **not** prove a dimension-three compression, but it excludes the
simplest way in which a higher local dimension could create a
counterexample: a negative quadratic or pure-kernel cubic direction.
The raw pure-kernel quartic is settled below.  A general curved branch
may nevertheless use positive-Hessian coordinates of order two; their
mixed cubic coupling changes the effective quartic and must be
eliminated separately.

### 4.1 Exact sum of squares for the flat-kernel quartic

Let \(q_4(x)\) be the degree-four Taylor coefficient of the polar
Stiefel chart restricted to the \(55\)-dimensional Hessian kernel above.
Then
\[
 \boxed{\qquad q_4(x)\geq0\quad\text{for every }x\in\mathbb R^{55}.
 \qquad}                                                   \tag{17}
\]
This is certified exactly, without a floating-point inference.

The monomial parity support of \(q_4\) has a \(14\)-dimensional
coordinate-sign symmetry group.  Averaging a Gram representation over
that group splits the degree-two monomials into \(192\) character
blocks.  Exact zero-diagonal elimination leaves \(969\) monomials.  A
relative-interior numerical Gram point was used only to discover the
minimal faces.  Their orthogonal range projectors reconstruct exactly
over \(\mathbb Q\), with block sizes at most \(24\) and total face rank
\(618\).

Writing every block as
\[
 G_\chi=B_\chi X_\chi B_\chi^T
\]
with the reconstructed rational range basis \(B_\chi\), exact
coefficient matching gives \(3348\) rational equations in \(1894\)
entries of the symmetric reduced matrices \(X_\chi\).  Sparse rational
elimination has rank \(1361\).  Choosing rational values for the \(533\)
free entries and solving the pivots exactly produces a certificate in
which every \(X_\chi\) is positive definite.  Exact \(LDL^T\)
factorization verifies every pivot is positive, and direct expansion
matches all \(3348\) coefficients of \(q_4\).

The complete \(126\)-kilobyte certificate is
`verification/certificates/n3_boundary_flat_quartic_sos.json`.
The independent verifier
`verification/verify_n3_boundary_flat_quartic_sos.py` uses only the
Python standard library.  The certificate vendors the already-expanded
exact quartic; the verifier reconstructs all character blocks, checks
their exact positive \(LDL^T\) pivots, and checks every coefficient.

This settles the **raw restriction** of the quartic to the Hessian
kernel, but not yet the Lyapunov--Schmidt effective quartic.  If \(k\)
is a kernel coordinate and \(p\) a positive-Hessian coordinate, mixed
cubic terms of type \(p\,k^2\) allow the minimizing branch
\(p=O(k^2)\) and subtract a nonnegative Hessian-inverse square from
\(q_4(k)\).  That exact Schur-complement correction remains to be
computed.  The raw SOS also has a nontrivial common zero variety.  No
local-minimum or global \(Q_3\) conclusion follows from (17) alone.

### 4.2 Exact Lyapunov--Schmidt quartic and its zero set

Choose one coordinate \(p_j\) from each of the \(149\) positive
rank-one Hessian blocks, so that on the resulting complement
\[
 q_2(p)=\sum_{j=1}^{149}h_jp_j^2,\qquad h_j>0.
\]
Let
\[
 \ell_j(k)=Dq_3(k)[p_j]
\]
be the mixed-cubic quadratic form on the \(55\)-dimensional kernel.
For a curved branch \(z=tk+t^2p+O(t^3)\), its order-four coefficient is
\[
 q_{4,\mathrm{raw}}(k)+\sum_j\{h_jp_j^2+\ell_j(k)p_j\}.
\]
Eliminating \(p\) exactly gives
\[
 \boxed{\quad
 q_{4,\mathrm{eff}}(k)
 =q_{4,\mathrm{raw}}(k)
  -\sum_{j=1}^{149}\frac{\ell_j(k)^2}{4h_j}.
 \quad}                                                    \tag{18}
\]

The effective quartic is also nonnegative:
\[
 \boxed{\qquad q_{4,\mathrm{eff}}(k)\geq0
 \quad\text{for every }k\in\mathbb R^{55}.\qquad}           \tag{19}
\]
Its \(30\)-dimensional coordinate-sign symmetry leaves \(505\)
quadratic monomials in \(158\) character blocks of size at most \(24\).
The reconstructed rational minimal face has total rank \(300\).
Coefficient matching on that face is a system of \(1759\) equations in
\(670\) reduced Gram variables, of exact rank \(555\).  An exact
rational solution with \(115\) free parameters makes every nonzero
reduced Gram block positive definite; the smallest numerical
eigenvalue of those exact matrices is \(1/2\).

The certificate is
`verification/certificates/n3_boundary_effective_quartic_sos.json`.
The standard-library verifier
`verification/verify_n3_boundary_effective_quartic_sos.py` no longer
trusts a discovery expansion.  Its independent companion
`verification/derive_n3_boundary_effective_quartic.py` starts from the
definition of \(Q_3\) and the polar Stiefel chart, reconstructs the
complete \(204\)-coordinate Hessian, its \(55+149\) splitting, all
\(2446\) raw quartic terms, all \(149\) forms \(\ell_j\) (with \(544\)
terms in total), and the \(1448\)-term effective quartic.  The verifier
then checks (18), all positive exact \(LDL^T\) pivots, and all \(1759\)
Gram coefficients.  The complete check uses only the Python standard
library.

The equality geometry can also be classified exactly.  Positive
definiteness of every reduced Gram block shows that equality in (19) is
equivalent to \(300\) rational quadratic equations.  Of these, \(278\)
factor as products of rational linear forms; only \(36\) distinct
independent linear factors occur.  Their product graph has exactly
\(64\) maximal independent sets, with size profile
\[
 2\text{ of size }18,\qquad
 6\text{ of size }10,\qquad
 56\text{ of size }6.
\]
On those \(64\) branches the remaining \(22\) ambiently irreducible
quadrics factor recursively.  Exact rational branching visits \(486\)
distinct linear states.  Every terminal state is linear; there is no
nonlinear residual ideal.  After removing contained leaves,
\[
 \boxed{\quad
 \{k:q_{4,\mathrm{eff}}(k)=0\}
 =L_0\cup L_1\cup L_2\cup L_3,
 \quad
 (\dim L_0,\dim L_1,\dim L_2,\dim L_3)=(37,37,27,27).
 \quad}                                                    \tag{20}
\]
At deterministic rational generic points, the exact Jacobian ranks of
the \(300\) equations are respectively \(18,18,28,28\), so each listed
linear space is a genuine maximal component.  The complete RREF
equations are printed and checked by
`discovery/decompose_n3_boundary_effective_zero_ideal.py`.

The first component has an intrinsic explanation.  It is precisely the
tangent space at \(C_0\) to
\[
 C=|a\rangle\langle b|_{12}\otimes P_W,
 \qquad \operatorname{rank}P_W=2,
                                                               \tag{21}
\]
whose real dimension is \(16+16+4+1=37\).  Every such operator is an
exact zero because
\[
 Q_3(C)=Q_2(|a\rangle\langle b|)\,Q_1(P_W)=0.
\]
Thus \(L_0\) integrates into a known exact equality manifold.  The
other three components are not tangent to (21).  For three deterministic
rational samples in each of \(L_1,L_2,L_3\), the exact
order-\(t^2\) Hessian-minimizing Stiefel path has its first nonzero term
at order six, and that coefficient is positive.  This last observation
is exact sample evidence, not yet a uniform sixth-order theorem:
additional order-two kernel curvature and order-three positive
directions must still be eliminated.

## 5. Current implications

### An exact obstruction to separate Hermitian-quadrature positivity

The sufficient route that tries to prove \(Q_3(H)\geq0\) for every
Hermitian \(H\) of inertia at most \((2,2)\) is false.  On two qutrit
parties put
\[
 A=\operatorname{diag}(1,1,-2),\qquad B=-A,\qquad
 D=I_3\otimes A+B\otimes I_3.
\]
The only nonzero eigenvalues of \(D\) are \(3,3,-3,-3\), so
\(\|D\|_2^2=36\).  Since \(A\) is traceless while
\(L(I_3)=-I_3/2\),
\[
 (L\otimes L)(D)=-\frac12D,\qquad Q_2(D)=-18.
\]
If \(R=|0\rangle\langle0|\) on a third qutrit, then
\[
 H=\frac16D\otimes R
\]
has rank four, inertia \((2,2)\), unit Hilbert--Schmidt norm, and
\[
 \boxed{Q_3(H)=\frac1{36}Q_2(D)Q_1(R)=-\frac14.}
\]
Thus a proof for \(C=A+iB\) must use the nonlinear common rank-two
origin of its two Hermitian quadratures; their individual inertia
bounds are insufficient.

Exactly established here:

- the four-replica compound formula (2);
- the factor-\(64\) obstruction (6);
- the crossed strong-defect identification (8)--(10);
- the grouped sector-cone obstruction (11);
- the exact inertia-\((2,2)\) obstruction above;
- positive semidefiniteness and the complete rank profile of the qutrit
  constrained Hessian, together with exact dimension-\(2,4,5\)
  cross-checks of the conjectured general profile (13)--(14);
- in local dimension three, cubic vanishing on its whole kernel (16).
- the rational weighted-SOS theorem (17) for the complete
  \(55\)-variable flat-kernel quartic.
- the exact Lyapunov--Schmidt formula (18), its rational SOS theorem
  (19), and the complete four-linear-component equality decomposition
  (20).

Not established:

- the secondary sixth-order Lyapunov--Schmidt forms on
  \(L_1,L_2,L_3\);
- classification of which higher-order continuations, if any, leave
  the exact equality family (21);
- the crossed strong-defect theorem (10);
- unrestricted three-copy positivity;
- an exact negative witness.
