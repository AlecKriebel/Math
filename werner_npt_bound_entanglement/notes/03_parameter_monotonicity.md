# Monotonicity toward the identity

The endpoint is decisive for the entire interval closer to zero, provided
two-block positivity holds at every copy number.

**Lemma.** Fix \(d\) and \(\beta<0\).  Suppose
\(X_{\beta,d}^{\otimes k}\) is two-block-positive for every \(k\ge1\).
Then, for every \(\alpha\in[\beta,0]\) and every \(n\ge1\),
\(X_{\alpha,d}^{\otimes n}\) is two-block-positive.

**Proof.** Put \(t=\alpha/\beta\in[0,1]\).  Directly from the definition,
\[
X_{\alpha,d}=tX_{\beta,d}+(1-t)I.
\]
Consequently,
\[
X_{\alpha,d}^{\otimes n}
=\sum_{S\subseteq[n]}
t^{|S|}(1-t)^{n-|S|}
\left(\bigotimes_{i\in S}X_{\beta,d}^{(i)}\right)
\otimes
\left(\bigotimes_{i\notin S}I^{(i)}\right).
\tag{1}
\]
All scalar coefficients are nonnegative.

It remains to check a summand.  Reorder copies so that \(S\) comes first and
write the coefficient matrix \(C\) of a Schmidt-rank-at-most-two vector in
blocks
\[
C=(C_{u,v})_{u,v\in[d]^{n-|S|}},
\]
where \(u\) is the spectator row index and \(v\) the spectator column index.
Every \(C_{u,v}\) is a submatrix of \(C\), so
\(\operatorname{rank}C_{u,v}\le\operatorname{rank}C\le2\).  Orthogonality of
the spectator basis gives
\[
\left\langle\psi_C\left|
X_{\beta,d}^{\otimes |S|}\otimes I
\right|\psi_C\right\rangle
=\sum_{u,v}
\left\langle\psi_{C_{u,v}}\left|
X_{\beta,d}^{\otimes |S|}
\right|\psi_{C_{u,v}}\right\rangle\ge0.
\]
For \(S=\varnothing\), the summand is simply \(\|C\|_F^2\).
Thus every term in (1) has nonnegative expectation. \(\square\)

In particular, an all-copy proof at \(\alpha=-\tfrac12\) for a fixed
dimension would automatically prove all-copy undistillability throughout
\([-\tfrac12,-\tfrac1d)\) in that dimension.
