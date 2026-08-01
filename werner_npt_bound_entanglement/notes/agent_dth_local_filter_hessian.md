# Summed one-site filter Hessian at a smooth DTH maximum

## Theorem

Let \(z\) be a unit tensor at a differentiable local maximum of

\[
 \mathcal F(z)=\sum_{j=1}^4s_j(D_z)^2.
\]

Let \(Y:\mathbb C^4\to\mathcal H\) be an isometry onto the isolated
top-four right singular space and define

\[
 P=YY^\dagger,
 \quad R=D_zY,
 \quad \Lambda=Y^\dagger D_z^\dagger D_zY,
 \quad M=Y\Lambda Y^\dagger=PS,
 \quad C=YR^\dagger=PD_z^\dagger.
\]

Put \(F=\operatorname{Tr}\Lambda=\mathcal F(z)\).  Then, for every
physical site \(i\),

\[
\boxed{
 \left\|\operatorname{Tr}_i C\right\|_2^2
 +\operatorname{Tr}\!\left[
   (\operatorname{Tr}_iP)(\operatorname{Tr}_iM)
  \right]
 \le2F.
}
\tag{1}

Here \(\operatorname{Tr}_i\) traces the indicated one-site qutrit and
leaves an operator on the complementary two-qutrit system.

This is an exact second-order necessary condition.  No lower bound strong
enough to contradict a high-purity critical point is claimed here.

## Proof

For a traceless Hermitian one-site matrix \(H\), transport both the tensor
and the trial singular subspace by the local filter \(e^{tH}\).  Expanding
the resulting Rayleigh trace through second order gives

\[
 U_2(H)-2F\operatorname{Tr}(\rho_i^zH^2)\le0,
\tag{2}

where

\[
\begin{aligned}
U_2(H)={}&
2\operatorname{Tr}(R^\dagger H^2R)
+4\operatorname{Tr}\left[(Y^\dagger HY)(R^\dagger HR)\right]\\
&+4\operatorname{Tr}\left[(Y^\dagger HY)^2\Lambda\right]
-2\operatorname{Tr}\left(\Lambda Y^\dagger H^2Y\right).
\end{aligned}
\tag{3}

Choose a Hilbert--Schmidt orthonormal basis
\(H_1,\ldots,H_8\) of traceless Hermitian \(3\times3\) matrices.  Its
completeness relations are

\[
 \sum_aH_a^2={8\over3}I,
 \qquad
 \sum_aH_aXH_a=\operatorname{Tr}(X)I-{1\over3}X.
\tag{4}

With identity factors restored on the complementary sites, (4) reads

\[
 \sum_aH_a^{(i)}XH_a^{(i)}
 =I_i\otimes\operatorname{Tr}_iX-{1\over3}X.
\tag{5}

The first and last terms of (3) sum to \(16F/3\) and \(-16F/3\), so they
cancel.  The two middle sums are

\[
\begin{aligned}
\sum_a\operatorname{Tr}
 [(Y^\dagger H_aY)(R^\dagger H_aR)]
 &=\|\operatorname{Tr}_iC\|_2^2-{F\over3},\\
\sum_a\operatorname{Tr}
 [(Y^\dagger H_aY)^2\Lambda]
 &=\operatorname{Tr}[(\operatorname{Tr}_iP)
                      (\operatorname{Tr}_iM)]-{F\over3}.
\end{aligned}
\tag{6}

Finally,

\[
 \sum_a2F\operatorname{Tr}(\rho_i^zH_a^2)={16F\over3}.
\]

Summing (2), substituting (6), and dividing by four proves (1).

The exact identities

\[
 CC^\dagger=M,
 \qquad C^\dagger C=D_zPD_z^\dagger=\overline M
\]

follow from skewness and may be useful for a future lower bound.  They are
not sufficient by themselves in the present argument.

The dependency-free verifier

```text
python3 verification/verify_dth_local_filter_hessian.py
```

checks the completeness contraction and all normalizations at a generic
smooth factor equality point.
