# Euler equations for a smooth interior DTH critical point

## Status

Let

\[
 \mathcal F(z)=\sum_{j=1}^4s_j(D_z)^2
\]

on the unit sphere of three-qutrit tensors.  The DTH/Ky--Fan-four target is
\(\mathcal F(z)\le1/2\).  This note derives a basis-free exact system obeyed
by every critical point at which the top four squared singular values form
an isolated cluster.

If \(S=D_z^\dagger D_z\), \(P\) is its top-four spectral projector,
\(F=\operatorname{Tr}(PS)\), and \(M=PS\), then

\[
 \boxed{\operatorname{Tr}_{\widehat i}M
       ={F\over2}(I-\rho_i^z),\qquad i=1,2,3.}
 \tag{1}
\]

Consequently the normalized top and bottom output states

\[
 \tau={PS\over F},\qquad
 \sigma={S-PS\over1-F}
 \tag{2}
\]

have exactly the same one-site marginals:

\[
 \boxed{\tau_i=\sigma_i={I-\rho_i^z\over2}.}
 \tag{3}
\]

Moreover, \(\tau\) has rank at most four and paired spectrum

\[
 (a,a,b,b),\qquad a+b={1\over2}.
 \tag{4}
\]

Thus a smooth full-support violation must produce a very special pair of
orthogonally supported states with identical three qutrit marginals.  This
is a necessary critical-point theorem, not yet a contradiction.

## 1. Hodge covariance and the ambient gradient

For a local matrix \(G\in GL(3)\), the three-dimensional Hodge identity is

\[
 A_{Gx}=\det(G)G^{-\mathsf T}A_xG^{-1}.
 \tag{5}
\]

Applying it at one physical site and differentiating at \(G=I+\epsilon H\)
gives

\[
 \boxed{
 D_{H^{(i)}z}
 =\operatorname{Tr}(H)D_z-H^{\mathsf T(i)}D_z-D_zH^{(i)}.
 }
 \tag{6}
\]

Let \(y_1,\ldots,y_4\) be an orthonormal frame for \(P\).  Alternation of
the three-Hodge form gives \(D_zy=-D_yz\).  Define

\[
 G_P=\sum_{\alpha=1}^4D_{y_\alpha}^\dagger D_{y_\alpha}.
 \tag{7}
\]

At an isolated top cluster, ordinary spectral perturbation gives

\[
 d\mathcal F_z(\delta)
 =2\operatorname{Re}\langle G_Pz,\delta\rangle.
 \tag{8}
\]

Hence the complete unit-sphere Euler equation is

\[
 \boxed{G_Pz=Fz.}
 \tag{9}
\]

The coefficient is fixed by
\(\langle z,G_Pz\rangle=\operatorname{Tr}(PS)=F\).

Using the exact Fierz identity, (7) can also be written solely in terms of
the rank-four projector and its marginals:

\[
\boxed{
8G_P=4I-P-
\sum_i (P_i\otimes I_{\widehat i})
+\sum_i\left(I_i\otimes(P_{\widehat i})^{\mathsf T}\right).
}
\tag{10}
\]

Thus (9)--(10), together with \(P\) being the top spectral projector of
\(S_z\), are an explicit finite Euler system.

## 2. The marginal complement equation

Because \(D_z^{\mathsf T}=-D_z\),

\[
 D_zD_z^\dagger=\overline{S},
 \qquad D_zPD_z^\dagger=\overline{PS}=\overline M.
 \tag{11}
\]

Take \(H=H^\dagger\) in (6).  On one hand, (8)--(9) give

\[
 {1\over2}d\mathcal F_z(H^{(i)}z)
 =F\operatorname{Tr}(H\rho_i^z).
 \tag{12}
\]

On the other hand, substitute (6) in the spectral derivative.  The two
left/right terms agree by (11), and one obtains

\[
 {1\over2}d\mathcal F_z(H^{(i)}z)
 =F\operatorname{Tr}H
  -2\operatorname{Tr}\!\left(H\operatorname{Tr}_{\widehat i}M\right).
 \tag{13}
\]

Equality for every Hermitian \(H\) proves (1).

There is also an unconditional output-marginal identity.  Directly
contracting two epsilon tensors gives, for arbitrary (not necessarily
normalized) \(z\),

\[
 \boxed{
 \operatorname{Tr}_{\widehat i}(D_z^\dagger D_z)
 ={1\over2}\left(\|z\|^2I-\rho_i^z\right).
 }
 \tag{14}
\]

For unit \(z\), subtract (1) from (14) and divide the two pieces by their
traces \(F\) and \(1-F\).  This proves (3).

Finally, the skew singular values occur in pairs.  On an isolated
top-four cluster, \(M\) has nonzero eigenvalues

\[
 \lambda_1,\lambda_1,\lambda_2,\lambda_2,
\]

and division by \(F=2(\lambda_1+\lambda_2)\) gives (4).

## 3. Immediate scalar consequences

The common marginal in (3) has purity

\[
 \boxed{
 \operatorname{Tr}\tau_i^2
 =\operatorname{Tr}\sigma_i^2
 ={1+\operatorname{Tr}(\rho_i^z)^2\over4}.
 }
 \tag{15}
\]

Also

\[
 \operatorname{Tr}\tau^2=2(a^2+b^2),
 \qquad {1\over4}\le\operatorname{Tr}\tau^2\le{1\over2}.
 \tag{16}

A purification of \(\tau\) therefore needs only a four-dimensional
ancilla and has ancilla spectrum (4).  Any global critical-point exclusion
may now be stated as a four-party pure-state marginal theorem augmented by
the existence of the orthogonally supported companion \(\sigma\).

The dependency-free verifier

```text
python3 verification/verify_dth_full_rank_euler.py
```

checks (6), (9), (1), and (14) with exact rational arithmetic, using a
generic rational tensor for the unconditional identities and a generic
smooth factor equality point for the critical identities.
