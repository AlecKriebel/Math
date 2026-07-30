# Square-zero positivity as a restricted coherent-exterior inequality

## Status

This note gives an exact reduction, not a proof of the remaining
inequality.

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},\qquad
 {\mathsf A}_i=\frac{I-F_i}{2},\qquad
 {\mathsf S}_2=\sum_{i<j}{\mathsf A}_i{\mathsf A}_j.
\tag{1}
\]
For two orthogonal isometries \(U,W:\mathbb C^2\to{\cal H}\), define
\[
 V|a,b\rangle=u_a\otimes w_b,\qquad
 R(U,W)=V^\dagger{\mathsf S}_2V.
\tag{2}
\]
Then \(R(U,W)\) is a positive two-qubit operator.  Its homogeneous
concurrence obeying
\[
\boxed{\qquad {\cal C}(R(U,W))\leq\frac12\qquad}          \tag{3}
\]
for every orthogonal pair \(U,W\) is exactly equivalent to
\[
\boxed{
 Q_3(C)\geq\frac14\bigl(s_1(C)-s_2(C)\bigr)^2
 \quad
 (C^2=0,\ \operatorname{rank}C\leq2).
}                                                        \tag{4}
\]
Equivalently, (3)--(4) are the single partial-trace inequality
\[
\boxed{
 3N-2S+P+2s_1s_2\geq0
 \quad(C^2=0,\ \operatorname{rank}C\leq2),
}                                                        \tag{5}
\]
where
\[
 N=\|C\|_2^2,\qquad
 S=\sum_i\|\operatorname{Tr}_iC\|_2^2,\qquad
 P=\sum_{i<j}\|\operatorname{Tr}_{ij}C\|_2^2.
\tag{6}
\]
In scalar/traceless degree masses this is
\[
\boxed{
 \|\Pi_2C\|_2^2-\|\Pi_3C\|_2^2
 \leq\frac23\|\wedge^2C\|_2.
}                                                        \tag{7}
\]

Thus the remaining square-zero problem is the coherent two-skew
exterior inequality from the earlier pair-sector program, restricted
to the additional equation \(C^2=0\).  The unrestricted version of
(5) is false; its known counterexamples do not satisfy \(C^2=0\).

Inequality (3), hence (4), is stronger than bare square-zero
positivity.  It implies \(Q_3(C)\geq0\), but no converse from bare
positivity to (3) is proved here.  The distinction is important:
under determinant-one logical filters, positivity only supplies the
filter-dependent allowance \(\|C\|_2^2/4\), whereas concurrence
requires the uniform allowance \(1/2\).

At equality in (4), any nonzero rank-two matrix must have equal
singular values and the corresponding feature state must satisfy
\({\cal C}(R)=1/2\).  This isolates the exact equality-rigidity
question suggested by the numerical boundary.

The dependency-free exact checker is
`verification/verify_n3_squarezero_concurrence_exterior.py`.

## 1. Endpoint Gram and the positive feature

Let \(H(U,W)\) be the endpoint Gram on the four transitions
\[
 E_{ab}=|u_a\rangle\langle w_b|.
\tag{8}
\]
The logical partial transpose is
\[
 H^{\Gamma_2}
 =V^\dagger YV,\qquad
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right).
\tag{9}
\]
The commuting-swap identity
\[
\boxed{
 Y-\frac14I+\frac18F_1F_2F_3
 =\sum_{i<j}{\mathsf A}_i{\mathsf A}_j
}                                                        \tag{10}
\]
is checked on expansion (or on the eight simultaneous swap sectors).
Orthogonality of the two planes gives
\[
\begin{aligned}
 \langle u_a\otimes w_b,\,
 F_1F_2F_3(u_c\otimes w_d)\rangle
 &=
 \langle u_a,w_d\rangle\langle w_b,u_c\rangle\\
 &=0.
\end{aligned}                                           \tag{11}
\]
Compressing (10) therefore yields
\[
\boxed{
 H^{\Gamma_2}=\frac14I_4+R,\qquad
 H=\frac14I_4+R^{\Gamma_2}.
}                                                        \tag{12}
\]

For a positive two-qubit operator \(R\), define homogeneous
concurrence by
\[
 {\cal C}(R)
 =
 \inf_{R=\sum_\mu|z_\mu\rangle\langle z_\mu|}
 \sum_\mu
 \left|z_\mu^{\mathsf T}
  (\epsilon\otimes\epsilon)z_\mu\right|,
 \qquad
 \epsilon=
 \begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\tag{13}
\]
For a pure column \(z=\operatorname{vec}M\), the smallest eigenvalue
of its partial transpose is \(-|\det M|\), while
\[
 |z^{\mathsf T}(\epsilon\otimes\epsilon)z|
 =2|\det M|.
\tag{14}
\]
Summing (14) over a decomposition and taking the infimum gives
\[
\boxed{
 R^{\Gamma_2}\succeq-\frac12{\cal C}(R)I_4.
}                                                        \tag{15}
\]
Consequently (3) implies \(H\succeq0\) directly from (12).  The next
section records the stronger exact equivalence with (4).

## 2. Determinant-one filters

We use the exact two-qubit filter formula
\[
\boxed{
 {\cal C}(R)
 =
 \sup_{A,B\in SL(2,\mathbb C)}
 \left\{
 -\operatorname{Tr}\!\left[
 F_{\rm L}(A\otimes B)R(A\otimes B)^\dagger
 \right]
 \right\}_+ ,
}                                                        \tag{16}
\]
where \(F_{\rm L}\) swaps the two logical qubits.  A self-contained
proof follows by applying (14) after determinant-one filters for the
upper bound and putting a positive two-qubit operator into its
balanced Bell-diagonal form for the reverse bound.  This is the same
filter lemma used in the coherent pair-sector reduction.

Fix \(A,B\in SL(2,\mathbb C)\), and put
\[
 X=UA^\dagger,\qquad Y_0=WB^\dagger,\qquad C=XY_0^\dagger.
\tag{17}
\]
The ranges of \(X\) and \(Y_0\) are orthogonal, hence \(C^2=0\).
Moreover
\[
 \det(X^\dagger X)=\det(Y_0^\dagger Y_0)=1
\tag{18}
\]
and therefore
\[
 s_1(C)s_2(C)=1.
\tag{19}
\]

Partial transposition of the three physical replica pairs in
\({\mathsf S}_2\), followed by the coefficient-matrix contraction,
gives the exact identity
\[
\boxed{
 \operatorname{Tr}\!\left[
 F_{\rm L}(A\otimes B)R(A\otimes B)^\dagger
 \right]
 =
 {\cal J}(C),
}                                                        \tag{20}
\]
where
\[
 {\cal J}(C)
 =\frac34N-\frac12S+\frac14P.
\tag{21}
\]
Indeed,
\[
 {\mathsf A}_i^{\Gamma}
 =\frac12(I-3P_i),
\tag{22}
\]
and summing the three pair expansions gives exactly the coefficients
in (21).

Equations (16), (19), and (20) prove
\[
 {\cal C}(R)\leq\frac12
 \quad\Longleftrightarrow\quad
 {\cal J}(C)+\frac12s_1(C)s_2(C)\geq0
\tag{23}
\]
for all rank-two square-zero \(C\).  For the reverse parametrization,
write a nonzero rank-two square-zero matrix in its thin singular-value
decomposition
\[
 C=U\operatorname{diag}(s_1,s_2)W^\dagger .
\tag{24}
\]
The equation \(C^2=0\) implies
\(\operatorname{ran}C\perp\operatorname{ran}C^\dagger\), so
\(U^\dagger W=0\).  Dividing (24) by \(\sqrt{s_1s_2}\) produces a
determinant-one logical filter of the form (17).  Rank one follows by
continuity.  Multiplying (23) by four gives (5).

Finally, a square-zero matrix has \(\operatorname{Tr}C=0\), and hence
\[
 Q_3(C)=N-\frac12S+\frac14P
       ={\cal J}(C)+\frac14N.
\tag{25}
\]
Using \(N=s_1^2+s_2^2\), equation (23) is exactly
\[
\begin{aligned}
 Q_3(C)
 &\geq
 \frac14(s_1^2+s_2^2)-\frac12s_1s_2\\
 &=\frac14(s_1-s_2)^2,
\end{aligned}
\]
which proves the claimed equivalence (3)--(5).

## 3. Degree and Pluecker form

Let \(w_k=\|\Pi_kC\|_2^2\), where \(\Pi_k\) selects exactly \(k\)
traceless local factors.  Direct scalar/traceless expansion gives
\[
 {\cal J}(C)=3w_0-\frac34w_2+\frac34w_3.
\tag{26}
\]
For square-zero \(C\), \(\operatorname{Tr}C=0\), so \(w_0=0\).
For rank at most two,
\[
 s_1s_2=\|\wedge^2C\|_2.
\tag{27}
\]
Substitution of (26)--(27) into (23) gives (7).

Equation (7) is the smallest exterior target isolated by this note:
prove a contrast of two common scalar/traceless layers using both
relations
\[
 \wedge^3C=0,\qquad C^2=0.
\tag{28}
\]
The first relation alone is insufficient, by the exact counterexamples
to the unrestricted coherent two-skew inequality.

## 4. Exact sharp frame and two no-go conclusions

Take
\[
 U=(|000\rangle,|001\rangle),\qquad
 W=(|110\rangle,|111\rangle).
\tag{29}
\]
Then
\[
 R=
 \begin{pmatrix}
 1/4&0&0&0\\
 0&3/4&-1/2&0\\
 0&-1/2&3/4&0\\
 0&0&0&1/4
 \end{pmatrix}.
\tag{30}
\]
It is invariant under the logical spin flip and has Takagi values
\[
 \frac54,\quad\frac14,\quad\frac14,\quad\frac14.
\tag{31}
\]
Thus
\[
 {\cal C}(R)=\frac12.
\tag{32}
\]
The matrix
\[
 C=|000\rangle\langle110|
  +|001\rangle\langle111|
\tag{33}
\]
has \(C^2=0\), equal singular values, and \(Q_3(C)=0\).
Hence every constant in (3)--(7) is sharp.

Two tempting shortcuts are ruled out by the same exact frame.

1.  The stronger Loewner bound \(R\preceq I/2\) is false:
    \(R\) has eigenvalue \(5/4\).  The concurrence bound, if true,
    must use cancellation of the three smaller Takagi values.
2.  The positive part
    \[
    A_W=I-\frac12\sum_i\rho_{Ki}^W
          +\frac14\sum_{i<j}\rho_{Kij}^W
    \tag{34}
    \]
    of the anchored code output cannot be universally positive
    definite.  The vector corresponding to (33) lies in
    \(K\otimes W^\perp\) and has zero \(A_W\)-expectation.  If
    \(A_W\succeq0\) is eventually proved, the appropriate rank-one
    Schur test for
    \(A_W-|\Psi_W\rangle\langle\Psi_W|/8\) must therefore use the
    Moore--Penrose inverse:
    \[
    |\Psi_W\rangle\in\operatorname{ran}A_W,\qquad
    \langle\Psi_W,A_W^+\Psi_W\rangle\leq8.
    \tag{35}
    \]

## 5. Remaining equality-rigidity problem

The quantitative route reduces the desired zero-rigidity statement
to:

> If \(U^\dagger W=0\) and
> \({\cal C}(R(U,W))=1/2\), then at least one of the six one-site
> plane marginals \(\rho_i^U,\rho_i^W\) is singular.

Every exact equality frame presently known has this property.  No
proof of the implication is supplied here.  Establishing (3) together
with its equality case would prove that the full-local-support
square-zero locus has no endpoint zero, which is the topological
rigidity mechanism currently sought.
