# Exact seven-to-five DTH contraction

## Purpose

The exact five-replica pseudomoment obstruction makes the next convex-hull
question a symmetric-extension problem.  This note fixes the marginal map and
its normalization before any symmetry-reduced seven-replica calculation.

Put

\[
H=(\mathbb C^3)^{\otimes3},\qquad A=\wedge^2H.
\]

Use replica pairs \((1,2),(3,4),(5,6)\) for three copies of the bivector and
replica (7) for (z).  The degree-two and degree-three physical monomials
are

\[
h_2(w,z)=w_{12}\otimes w_{34}\otimes z_5,
\]

\[
h_3(w,z)=w_{12}\otimes w_{34}\otimes w_{56}\otimes z_7.
\]

Here (w=(u_0\otimes u_1-u_1\otimes u_0)/\sqrt2), so an orthonormal pair
gives \(\|w\|=1\).

## The marginal and its normalization

Let \(J_2\) and \(J_3\) denote the isometric inclusions of

\[
K_2=S_{(2,2)}H\otimes H,
\qquad
K_3=S_{(3,3)}H\otimes H
\]

into the five- and seven-replica tensor spaces.  After relabelling replica 7
as replica 5, define the full marginal

\[
\mathcal M_{\rm full}(T)=\operatorname{Tr}_{5,6}(J_3TJ_3^\dagger).
\]

For every physical monomial,

\[
\mathcal M_{\rm full}
 \bigl(|h_3(w,z)\rangle\langle h_3(w,z)|\bigr)
=
\|w\|^2|h_2(w,z)\rangle\langle h_2(w,z)|.
\]

Thus the normalized Grassmann convention introduces **no scalar factor**.
For unit (w), the marginal is exactly the degree-two moment.

Writing (P_2=J_2J_2^\dagger), the compressed map is

\[
\mathcal M(T)
=J_2^\dagger P_2\mathcal M_{\rm full}(T)P_2J_2.
\]

Its Hilbert--Schmidt adjoint is

\[
\boxed{
\mathcal M^*(Y)
=J_3^\dagger\bigl(J_2YJ_2^\dagger\otimes I_A\bigr)J_3.
}
\]

If (T\succeq0), \(\operatorname{Tr}T=\operatorname{Tr}R\), and
\(\mathcal M(T)=R\), then the uncompressed marginal is already exactly (R).
Indeed, its compression onto (K_2) has the full trace; positivity forces the
orthogonal diagonal block and then the off-diagonal blocks to vanish.  Hence
the compressed equality plus trace normalization loses nothing in the PSD
extension problem.

## Sparse permutation-diagram formula

At one physical qutrit site let (P_\pi) be the permutation operator for
\(\pi\in S_7\).  Delete the symbols 5 and 6 from the disjoint-cycle notation
of \(\pi\), shortcutting every cycle through the deleted symbols.  Let

* \(\pi\downarrow\in S_5\) be the induced permutation of the retained
  symbols \(1,2,3,4,7\), in that order;
* \(c(\pi)\) be the number of cycles of \(\pi\) lying wholly in
  \(\{5,6\}\).

Then

\[
\boxed{
\operatorname{Tr}_{5,6}P_\pi
=3^{c(\pi)}P_{\pi\downarrow}.
}
\tag{1}
\]

Proof: draw the permutation matrix as a wiring diagram.  Removing a traced
wire shortcuts its incoming and outgoing edges.  A component that contains a
retained wire becomes precisely one cycle of \(\pi\downarrow\); a component
containing only traced wires becomes a closed index loop and contributes
\(\sum_{j=0}^2 1=3\).  Components are independent, proving (1).

For a three-site diagram basis element this tensorizes:

\[
\boxed{
\operatorname{Tr}_{H_5\otimes H_6}
 \left(P_{\pi_1}\otimes P_{\pi_2}\otimes P_{\pi_3}\right)
=3^{c(\pi_1)+c(\pi_2)+c(\pi_3)}
 P_{\pi_1\downarrow}\otimes
 P_{\pi_2\downarrow}\otimes
 P_{\pi_3\downarrow}.
}
\tag{2}
\]

Consequently the exact seven-to-five contraction matrix in matched diagram
coordinates has entries

\[
D_{(\tau_1,\tau_2,\tau_3),(\pi_1,\pi_2,\pi_3)}
=
\begin{cases}
3^{\sum_i c(\pi_i)},&\pi_i\downarrow=\tau_i\ \text{for all }i,\\
0,&\text{otherwise}.
\end{cases}
\]

No dense physical tensor or numerical normalization is needed.  Projecting
the input and output by the exact degree-three and degree-two Grassmann
projectors gives the symmetry-reduced block map.

The adjoint statement is even simpler.  If \(\widehat\sigma\in S_7\) fixes
5 and 6 and acts as \(\sigma\in S_5\) on \(1,2,3,4,7\), then

\[
\bigl(\operatorname{Tr}_{5,6}\bigr)^*(P_\sigma)=P_{\widehat\sigma}.
\]

## Lift of the witness objective

Let \(O_0^{(j)}\) denote the minimal DTH witness acting on the (j)-th
bivector pair and the final (z) replica, with identities on the other
pairs.  In the degree-two and degree-three spaces put

\[
\widetilde O_0^{(2)}=\frac12(O_0^{(1)}+O_0^{(2)}),
\qquad
\widetilde O_0^{(3)}=\frac13(O_0^{(1)}+O_0^{(2)}+O_0^{(3)}).
\]

If (P_3) is the degree-three Grassmann projector, its range is invariant
under every permutation of the three bivector pairs.  Hence the three
compressed operators (P_3O_0^{(j)}P_3) are equal.  The adjoint marginal
therefore obeys the exact identity

\[
\boxed{
P_3\mathcal M^*(\widetilde O_0^{(2)})P_3
=P_3\widetilde O_0^{(3)}P_3.
}
\tag{3}
\]

Consequently any fixed extension (T) of the committed five-replica moment
(R) preserves its witness value exactly:

\[
\operatorname{Tr}(T\widetilde O_0^{(3)})
=\operatorname{Tr}(R\widetilde O_0^{(2)}).
\]

Thus extension feasibility would immediately produce a negative
degree-three pseudomoment, while positivity of the properly constrained
degree-three witness would rule out the extension.

## Verification

`verification/verify_dth_seven_to_five_contraction.py` checks, for all
\(\pi\in S_7\) and \(\sigma\in S_5\), the exact adjoint identity

\[
\langle P_\sigma,\operatorname{Tr}_{5,6}P_\pi\rangle_{\rm HS}
=
\langle P_{\widehat\sigma},P_\pi\rangle_{\rm HS},
\]

using \(\operatorname{Tr}P_\rho=3^{\#\mathrm{cycles}(\rho)}\).  It also
checks trace preservation and the three-site identity normalization
\(3^6=27^2=729\).  The verifier is dependency-free and uses exact integer
arithmetic.

## Scope

This is the exact linear marginal needed for the fixed-extension test.  It is
not a proof that the committed five-replica pseudomoment has or lacks a
degree-three extension, and it is not a physical DTH result by itself.
