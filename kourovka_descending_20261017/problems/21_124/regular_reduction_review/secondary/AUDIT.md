# Independent narrow audit of the regular-module reduction

Reviewed frozen input: `nonabelian_holonomy/FINITE_REGULAR_REDUCTION.md`,
SHA256 `6372e5f77ba26f8d6c59a49c47fa1991ffa521359c65039cdf69d6c699f8a250`.

**Outcome: PASS within the scope below.** No complete Kourovka solution,
universal finite-quotient rank bound, or originality finding follows. I did not
read other approach-family proofs. This is independent verification of the
affine/rotational-to-regular-module part, not of the multiset matching argument.

Use the group presentation

\[
[a,t]=[b,t]=1,\qquad
s_i(a^{p_i}t)s_i^{-1}=b^{q_i}t,
\]

with pairs \((p_i,q_i)=(3,2),(20,14),(119,84)\). The two vertex groups are
the displayed copies \(\langle a,t\rangle\) and \(\langle b,t\rangle\)
of \(\mathbb Z^2\).

## 1. Original rotations and cocycles can be discarded existentially

Write the original affine image of a generator \(x\) as
\(z\mapsto R_xz+v_x\). Choose a common positive power
\(M\) killing the finite linear parts of \(a,b,t\). Let their \(M\)-th
powers be translations by \(A_0,B_0,T_0\), respectively. Vertex injectivity
implies \(A_0\ne0\): otherwise the image of \(a\) has finite order.

Taking the \(M\)-th power of each original conjugation relation and using
the two commuting vertex relations gives

\[
s_i a^{p_iM}t^M s_i^{-1}=b^{q_iM}t^M.
\]

Conjugating a translation by an affine isometry with linear part \(S_i\)
acts on its vector by \(S_i\); its translational cocycle cancels. Consequently

\[
S_i(p_iA_0+T_0)=q_iB_0+T_0.
\]

Sending \(a,b,t\) to the translations \(A_0,B_0,T_0\), and \(s_i\) to
the pure linear maps \(S_i\), satisfies every defining relation. This is
a new homomorphism, not a claim that the original one is conjugate to such a
homomorphism. It need not retain original vertex injectivity at this stage;
the independent last coordinate below restores it. There is no assumption
that the original representation or its rotation matrices are rational.

## 2. One regular module is enough

Let \(Q=\langle S_1,S_2,S_3\rangle\), a finite group. Choose a real linear
functional \(\ell\) with \(\ell(A_0)\ne0\). Define

\[
F(v)(g)=\ell(g^{-1}v),\qquad g\in Q.
\]

For the left regular action \((L(h)f)(g)=f(h^{-1}g)\), the calculation is

\[
F(hv)(g)=\ell(g^{-1}hv)
       =F(v)(h^{-1}g)=(L(h)F(v))(g).
\]

Thus \(F\) is equivariant, and \(F(A_0)(1)=\ell(A_0)\ne0\).
Injectivity of \(F\) is not needed. This last point avoids a possible
incorrect demand that every finite-group module embed in a single regular
module. Only the one detected vector, and preservation of the linear equations,
are required here.

## 3. Rational descent keeps the horizontal coordinate

The resulting equations have an integer matrix \(D\), because the regular
action consists of permutation matrices. Gaussian elimination over
\(\mathbb Q\) gives a rational basis \(v_1,\ldots,v_r\) for \(\ker D\),
which is also an \(\mathbb R\)-basis for the real kernel. If all their
\(A\)-coordinates vanished, every real kernel vector would have \(A=0\),
contradicting the vector just constructed. At least one rational basis vector
therefore has \(A\ne0\). This is a nonvanishing linear-coordinate argument;
it requires neither rational approximation nor rational original rotations.

## 4. Nonzero B and the exact vertical line

For any orthogonal solution, \(B=0\) implies

\[
p_i\|A\|^2+2\langle A,T\rangle=0
\]

after taking squared norms and dividing by the nonzero \(p_i\).
The distinct values \(p_1=3,p_2=20\) force \(A=0\).
Similarly, \(A=0\) implies
\(q_i\|B\|^2+2\langle B,T\rangle=0\), and the distinct nonzero
values \(q_1=2,q_2=14\) force \(B=0\). Hence \(A=0\) if and only if
\(B=0\).

In the regular module, a kernel vector with \(A=0\) must therefore have
\(B=0\), and then \(L(h_i)T=T\) for every \(i\). Because the \(h_i\)
generate \(Q\), invariance under them implies invariance under every left
translation. A function invariant under every left translation on \(Q\)
is constant. The vertical-only kernel is exactly one dimensional, including
the boundary case \(Q=1\). Generation is essential: if an ambient finite
group strictly larger than the generated subgroup were used, that fixed-space
dimension would instead be the number of left orbits.

## 5. Restoring genuinely discrete injective vertices

Clear the denominators by an integer \(d>0\) and adjoin a trivial integer
coordinate. The translation vectors for \(a,b,t\) become

\[
(dA,0),\quad(dB,0),\quad(dT,1).
\]

Both first vectors are nonzero. Each is real-linearly independent of the
last vector, because the last coordinate distinguishes them. Consequently
each displayed vertex maps injectively as a discrete rank-two subgroup of
the integral lattice \(\mathbb Z^{|Q|+1}\). The added coordinate respects
all relations: both edge words have last coordinate one, and \(Q\) acts
trivially there. This verifies the claimed existential reconstruction even
when the original commuting translations were not real-linearly independent.

## Checks and limitations

`independent_checks.py` uses exact rational elimination and independently
constructed permutation groups. It checks the inverse/action convention on
a noncommuting \(S_3\) module, and fixed-space and vertical-kernel dimensions
over generated cyclic, dihedral, and symmetric examples, including the trivial
group. These checks support and test the unbounded arguments above; they are
not a search over all finite groups and cannot establish the outstanding
universal matrix-rank assertion.

No substantive objection remains to the scoped implications audited here.
