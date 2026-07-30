# A sharp three-replica linear-relaxation obstruction for the pair sector

## Status

This note gives an exact obstruction to the most direct
three-replica proof of the unresolved qutrit pair-sector inequality
\[
 \left\|\Pi _2C\right\|_2^2\leq\frac23\|C\|_2^2
 \qquad(\operatorname{rank}C\leq2).                       \tag{1}
\]
It is **not** a physical rank-two counterexample to (1).

On three replicas, every diagonal cube \(c^{\otimes3}\) of a
Schmidt-rank-at-most-two vector has three evident linear properties:

1. it is invariant under simultaneous replica permutations;
2. its three row replicas have no alternating component;
3. its three column replicas have no alternating component.

The theorem below constructs a vector satisfying all three properties
on which the averaged lift of
\[
 W=\frac23I-\Pi _2                                      \tag{2}
\]
has the exact negative Rayleigh quotient
\[
 \boxed{-\frac{35}{117}}.                                \tag{3}
\]
Consequently, positivity on the subspace cut out only by simultaneous
\(S_3\) symmetry and the two linear \(\bigwedge^3=0\) constraints is
false.  A successful three-replica proof must retain nonlinear
diagonal-cube (Veronese/Pluecker polarization) relations.

The dependency-free exact checker is
`verification/verify_n3_pair_three_replica_linear_nogo.py`.

## 1. The three-replica relaxation

Write the row and column Hilbert spaces of one coefficient matrix as
\[
 {\cal H}_R=R_1\otimes R_2\otimes R_3,\qquad
 {\cal H}_C=C_1\otimes C_2\otimes C_3,
\]
where every local factor is \(\mathbb C^3\).  On three replicas, let
\({\mathsf A}_R\) and \({\mathsf A}_C\) be the alternating
projectors for the replica action on \({\cal H}_R^{\otimes3}\) and
\({\cal H}_C^{\otimes3}\), respectively.  Let
\[
 \overline W=\frac13(W^{(1)}+W^{(2)}+W^{(3)}).             \tag{4}
\]

If \(c\in{\cal H}_R\otimes{\cal H}_C\) has Schmidt rank at most two,
then
\[
\begin{aligned}
 U_g^RU_g^C\,c^{\otimes3}&=c^{\otimes3}
                 &&(g\in S_3),\\
 {\mathsf A}_R c^{\otimes3}&=0,\\
 {\mathsf A}_C c^{\otimes3}&=0.                           \tag{5}
\end{aligned}
\]
The first identity is diagonal-cube symmetry.  The other two follow
because the row and column Schmidt supports both have dimension at
most two.

One might therefore try to prove that \(\overline W\) is positive on
the linear subspace defined by (5).  The next theorem disproves that
statement exactly.

## 2. Exact negative vector

Fix the traceless matrix unit
\[
 E_{01}=|0\rangle\langle1|
\]
at physical sites \(1\) and \(2\) in every replica.  Only physical
site \(3\) remains nontrivial.  Its three row qutrits have basis
\(|r_1r_2r_3\rangle_R\), and similarly on the column side.  Define
the unnormalized vectors
\[
\begin{aligned}
 \zeta
 &=\sum_{r\in\{0,1,2\}^3}|r\rangle_R|r\rangle_C,\\
 \chi
 &=
 \left(\sum_{\pi\in S_3}\operatorname{sgn}(\pi)
       |\pi(0)\pi(1)\pi(2)\rangle_R\right)
 \otimes
 \left(\sum_{\sigma\in S_3}\operatorname{sgn}(\sigma)
       |\sigma(0)\sigma(1)\sigma(2)\rangle_C\right),\\
 \eta&=\zeta-\frac16\chi.                                \tag{6}
\end{aligned}
\]
Tensoring (6) with the fixed \(E_{01}^{\otimes3}\) factors at sites
\(1\) and \(2\) is understood.

### Theorem 2.1

The vector \(\eta\) has all three properties in (5), but
\[
 \boxed{\qquad
 \frac{\langle\eta,\overline W\eta\rangle}
      {\|\eta\|^2}
 =-\frac{35}{117}.
 \qquad}                                                  \tag{7}
\]

### Proof

Both \(\zeta\) and \(\chi\) are invariant under simultaneous row and
column replica permutations.  The latter vector is invariant because
the two signs multiply to \(+1\).  Thus \(\eta\) has the first
property in (5).

Direct antisymmetrization gives
\[
 {\mathsf A}_R\zeta
 ={\mathsf A}_C\zeta=\frac16\chi,\qquad
 {\mathsf A}_R\chi={\mathsf A}_C\chi=\chi.                \tag{8}
\]
It follows immediately from (6) that
\[
 {\mathsf A}_R\eta={\mathsf A}_C\eta=0.                  \tag{9}
\]
The elementary inner products are
\[
 \|\zeta\|^2=27,\qquad
 \|\chi\|^2=36,\qquad
 \langle\zeta,\chi\rangle=6,
\]
and hence
\[
 \boxed{\|\eta\|^2=26.}                                  \tag{10}
\]

Let \(P_r\) be the normalized maximally entangled projector between
the row and column qutrits in replica \(r\) at physical site \(3\):
\[
 P_r=\frac13
 \sum_{a,b=0}^2|a\rangle_R|a\rangle_C
                  \langle b|_R\langle b|_C.              \tag{11}
\]
For each \(r\),
\[
\begin{aligned}
 \langle\zeta,P_r\zeta\rangle&=27,\\
 \langle\zeta,P_r\chi\rangle&=6,\\
 \langle\chi,P_r\chi\rangle&=4.                           \tag{12}
\end{aligned}
\]
Substitution of (6) gives
\[
 \langle\eta,P_r\eta\rangle
 =27-2+\frac19=\frac{226}{9},\qquad
 \frac{\langle\eta,P_r\eta\rangle}{\|\eta\|^2}
 =\frac{113}{117}.                                       \tag{13}
\]

The two fixed \(E_{01}\) factors are entirely traceless.  Therefore,
on the present subspace, the degree-two projection in replica \(r\)
is exactly \(P_r\) on the remaining third site:
\[
 \Pi_2^{(r)}=P_r.                                        \tag{14}
\]
Equations (2), (4), (10), and (13) now give
\[
\begin{aligned}
 \frac{\langle\eta,\overline W\eta\rangle}{\|\eta\|^2}
 &=
 \frac23-\frac13\sum_{r=1}^3\frac{113}{117}\\
 &=\frac23-\frac{113}{117}
 =-\frac{35}{117},
\end{aligned}
\]
proving (7). \(\square\)

## 3. Consequence for three-replica certificates

Let
\[
 {\cal K}=
 \left\{\xi:
 U_g^RU_g^C\xi=\xi\ (g\in S_3),\
 {\mathsf A}_R\xi={\mathsf A}_C\xi=0\right\}.             \tag{15}
\]
Theorem 2.1 proves
\[
 \overline W\big|_{\cal K}\not\succeq0.                  \tag{16}
\]
In particular, no proof can consist merely of showing that the
negative directions of \(\overline W\) lie in either global
three-replica alternating sector.  Equivalently, a Gram/SOS
certificate modulo only the two linear constraints
\({\mathsf A}_R=0={\mathsf A}_C\) is impossible.

This does not rule out a higher-degree SOS modulo the full
determinantal ideal.  The missing information is precisely that the
test vector is not an arbitrary member of \({\cal K}\), but the
diagonal cube \(c^{\otimes3}\) of one common coefficient vector.
Those Veronese relations are nonlinear and are not captured by (15).

### 3.1 No degree-six Hermitian SOS modulo the cubic rank ideal

The obstruction has a direct polynomial consequence.  For a
coefficient vector \(c\), put
\[
 f(c)=\|c\|^4\langle c,Wc\rangle
 =\langle c^{\otimes3},\overline Wc^{\otimes3}\rangle.
                                                               \tag{17}
\]
The cubic \(3\times3\) minors of the coefficient matrix are exactly
the linear functionals on \(\operatorname{Sym}^3\) carried by the
row-sign/column-sign sector.  Thus (9) says that every cubic minor
functional vanishes on \(\eta\).

Suppose there were a homogeneous degree-six certificate
\[
 f(c)=
 \sum_j|p_j(c)|^2+
 \sum_\alpha
 \operatorname{Re}\!\left(
 q_\alpha(c)\overline{\Delta_\alpha(c)}\right),            \tag{18}
\]
where the \(p_j,q_\alpha\) are homogeneous cubics and the
\(\Delta_\alpha\) are the \(3\times3\) minors.  Polarizing (18)
produces a positive-semidefinite Gram form on
\(\operatorname{Sym}^3\), plus cross terms containing one determinant
functional.  Evaluating that polarized form on \(\eta\) kills every
cross term by (9), while the Gram part is nonnegative.  This
contradicts (7).

Consequently,
\[
\boxed{\text{there is no degree-six Hermitian SOS certificate
modulo the cubic rank-two determinantal ideal.}}           \tag{19}
\]
Higher-degree multipliers can impose additional Veronese relations
and are not excluded by this argument.

The same no-go applies to the stronger even-parity proposal
\[
 W_{\rm even}=\frac23I-(\Pi_0+\Pi_2).                     \tag{20}
\]
Indeed, the two fixed \(E_{01}\) factors make the degree-zero
projection vanish identically on the constructed subspace.  Hence
\(W_{\rm even}\) and \(W\) have the same Rayleigh quotient (7) on
\(\eta\).

## 4. What remains open

The construction is not of the form \(c^{\otimes3}\), and it does not
give a rank-two matrix with negative pair-sector defect.  Thus it does
not disprove (1) or the equivalent marginal operator inequality
\[
 3I+2\sum_{i<j}\rho_{Kij}
 -3\sum_i\rho_{Ki}-|\Psi\rangle\langle\Psi|\succeq0.
\]

It does identify an exact requirement for any successful
three-replica attack: the certificate must couple replica irreducible
sectors through the common diagonal-cube amplitudes, rather than use
only symmetry and absence of \(\bigwedge^3\).
