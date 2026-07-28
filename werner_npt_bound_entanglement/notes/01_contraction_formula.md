# Exact contraction formula and the sharp one-copy bound

## 1. Coefficient matrices

Put \(H=(\mathbb C^d)^{\otimes n}\).  For \(C\in\operatorname{End}(H)\),
define
\[
|\psi_C\rangle=\sum_{x,y\in[d]^n}C_{x,y}|x\rangle_A|y\rangle_B .
\]
Then
\[
\langle\psi_C|\psi_D\rangle=\operatorname{Tr}(C^\dagger D),
\qquad
\operatorname{SR}(\psi_C)=\operatorname{rank}C.
\]
The second assertion follows because the Schmidt rank of a bipartite vector is
the rank of its coefficient matrix: a rank-\(r\) matrix factorization gives
\(r\) product summands, while any expression as \(r\) product summands gives
a matrix of rank at most \(r\).

For \(S\subseteq[n]\), define the ordinary partial trace
\[
(\operatorname{Tr}_S C)_{x_{\bar S},y_{\bar S}}
=\sum_{z_S\in[d]^S}C_{(z_S,x_{\bar S}),(z_S,y_{\bar S})}.
\]

## 2. Projection-contraction lemma

**Lemma.** If
\[
P_S=\bigotimes_{i\in S}P_d^{(i)}
\]
and the identity acts on the pairs outside \(S\), then
\[
\langle\psi_C|P_S|\psi_D\rangle
=d^{-|S|}
\operatorname{Tr}\!\left[
(\operatorname{Tr}_S C)^\dagger(\operatorname{Tr}_S D)
\right].
\]
In particular,
\[
\langle\psi_C|P_S|\psi_C\rangle
=d^{-|S|}\|\operatorname{Tr}_S C\|_F^2.
\]

**Proof.** For each \(i\in S\),
\[
P_d^{(i)}
=\frac1d\sum_{r_i,s_i=0}^{d-1}
|r_i,r_i\rangle\langle s_i,s_i|.
\]
Expanding the product forces the two output indices on every contracted pair
to agree, forces the two input indices there to agree, and leaves all
complementary indices unchanged.  Thus
\[
\begin{aligned}
\langle\psi_C|P_S|\psi_D\rangle
&=d^{-|S|}
\sum_{x_{\bar S},y_{\bar S}}
\sum_{r_S,s_S}
\overline{C_{(r_S,x_{\bar S}),(r_S,y_{\bar S})}}
D_{(s_S,x_{\bar S}),(s_S,y_{\bar S})}\\
&=d^{-|S|}
\sum_{x_{\bar S},y_{\bar S}}
\overline{(\operatorname{Tr}_S C)_{x_{\bar S},y_{\bar S}}}
(\operatorname{Tr}_S D)_{x_{\bar S},y_{\bar S}},
\end{aligned}
\]
which is the claimed Hilbert--Schmidt inner product. \(\square\)

## 3. Exact quadratic form

Expanding the tensor product and applying the lemma gives, for every
\(\alpha\),
\[
Q_{\alpha,d,n}(C)
:=\langle\psi_C|X_{\alpha,d}^{\otimes n}|\psi_C\rangle
=\sum_{S\subseteq[n]}\alpha^{|S|}
\|\operatorname{Tr}_S C\|_F^2.
\tag{1}
\]
At the endpoint \(\alpha=-\tfrac12\),
\[
Q_{d,n}(C)
=\sum_{S\subseteq[n]}(-\tfrac12)^{|S|}
\|\operatorname{Tr}_S C\|_F^2.
\tag{2}
\]
The formula contains no explicit \(d\); dimension enters only through the
domains of the partial traces.

Equivalently, if
\[
\mathcal K_d(Z)=Z-\tfrac12\operatorname{Tr}(Z)I_d
\]
as a self-adjoint superoperator on \(d\times d\) matrices, then
\[
Q_{d,n}(C)
=\langle C,\mathcal K_d^{\otimes n}(C)\rangle_{HS}.
\tag{3}
\]
Indeed, the adjoint of the trace map is \(z\mapsto zI_d\), so expansion of
\(\prod_i(I-\tfrac12\operatorname{Tr}_i^*\operatorname{Tr}_i)\) gives (2).

## 4. Sharp one-copy theorem

**Theorem.** For every \(d\ge2\), every matrix \(C\) of rank at most two, and
every \(\alpha\ge-\tfrac12\),
\[
Q_{\alpha,d,1}(C)
=\|C\|_F^2+\alpha|\operatorname{Tr}C|^2
\ge(1+2\alpha)\|C\|_F^2\ge0.
\tag{4}
\]
At \(\alpha=-\tfrac12\), a nonzero rank-at-most-two matrix has equality if
and only if it is a scalar multiple of an orthogonal rank-two projection.
More precisely, equality in
\[
|\operatorname{Tr}C|^2\le2\|C\|_F^2
\tag{5}
\]
for nonzero \(\operatorname{rank}C\le2\) holds exactly when
\(C=\lambda P\), where \(P\) is an orthogonal rank-two projection and
\(\lambda\ne0\).

**Proof.** Take a singular-value decomposition
\[
C=\sum_{j=1}^r s_j|u_j\rangle\langle v_j|,
\qquad r\le2.
\]
Then
\[
|\operatorname{Tr}C|
=\left|\sum_{j=1}^r s_j\langle v_j,u_j\rangle\right|
\le\sum_{j=1}^r s_j
\le\sqrt r\left(\sum_{j=1}^r s_j^2\right)^{1/2}
\le\sqrt2\,\|C\|_F.
\]
Substitution proves (4).  For equality in (5), all inequalities above must
be equalities: \(r=2\); \(s_1=s_2=s>0\); each
\(|\langle v_j,u_j\rangle|=1\), hence \(v_j\) and \(u_j\) are parallel; and
the two trace summands have the same phase.  Therefore
\(C=\lambda(|u_1\rangle\langle u_1|+
|u_2\rangle\langle u_2|)=\lambda P\).
The converse is immediate. \(\square\)

The equality statement concerns the endpoint.  For \(\alpha>-\tfrac12\),
the last inequality in (4) is strict for nonzero \(C\).
