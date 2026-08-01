# Orthogonal equal-marginal purity filter for smooth DTH violations

## Theorem

Let \(z\) be a unit three-qutrit tensor at a differentiable critical point
of

\[
 \mathcal F(z)=\sum_{j=1}^4s_j(D_z)^2.
\]

If \(\mathcal F(z)>1/2\), then

\[
\boxed{
 P_{\rm loc}(z)>
 {23-\sqrt{193}\over6}
 =1.5179260017\ldots .
}
\tag{1}

This strengthens the scalar-plus-one-body projection threshold \(29/21\).
It uses not only the common one-site marginals of the top and bottom output
states, but also their orthogonal supports.

## Proof

Put

\[
 S=D_z^\dagger D_z,
 \qquad F=\mathcal F(z),
\]

and let \(P\) be the isolated top-four spectral projector.  The exact Euler
theorem gives orthogonally supported density operators

\[
 \tau={PS\over F},
 \qquad
 \sigma={S-PS\over1-F}
\]

with common one-site marginals

\[
 q_i=\tau_i=\sigma_i={I-\rho_i^z\over2}.
\tag{2}

Let \(Q\) be their common Hilbert--Schmidt projection onto the
scalar-plus-one-body operator space:

\[
 Q={I\over27}+{1\over9}\sum_i(q_i-I/3)\otimes I_{\widehat i}.
\tag{3}

Writing \(p=P_{\rm loc}(z)\), orthogonality of the local-degree sectors
gives

\[
 L:=\|Q\|_2^2={1+3p\over108}.
\tag{4}

Set

\[
 A=\operatorname{Tr}\tau^2,
 \qquad B=\operatorname{Tr}\sigma^2.
\]

The top state has rank at most four, so \(A\ge1/4\).  Decompose

\[
 \tau=Q+\tau_\perp,
 \qquad \sigma=Q+\sigma_\perp.
\]

Because \(Q\) is their common orthogonal projection,

\[
 \|\tau_\perp\|_2^2=A-L,
 \qquad
 \|\sigma_\perp\|_2^2=B-L.
\]

Their supports are orthogonal, hence \(\operatorname{Tr}(\tau\sigma)=0\)
and

\[
 \langle\tau_\perp,\sigma_\perp\rangle=-L.
\]

Cauchy--Schwarz now supplies the coupled bound

\[
\boxed{
 (A-L)(B-L)\ge L^2,
 \qquad
 B\ge {AL\over A-L}.
}
\tag{5}

This is strictly stronger here than applying the one-body projection to
\(\sigma\) alone.

The output purity identity and orthogonality give

\[
 {1+p\over32}
 =\operatorname{Tr}S^2
 =F^2A+(1-F)^2B.
\tag{6}

For \(1\le p\le3\), one has

\[
 2L\le {5\over27}<{1\over4}\le A.
\]

Therefore \(AL/(A-L)<A\).  The right side of (6), after substituting
(5), is increasing in \(F\ge1/2\).  At \(F=1/2\), it is

\[
 {1\over4}\left(A+{AL\over A-L}\right)
 ={A^2\over4(A-L)},
\]

which is increasing for \(A>2L\).  Its minimum is attained at \(A=1/4\):

\[
 \operatorname{Tr}S^2
 > {27\over16(26-3p)}
 \qquad(F>1/2).
\tag{7}

Combining (6)--(7) gives

\[
 {1+p\over32}>{27\over16(26-3p)}.
\]

After clearing the positive denominator \(26-3p\), this is

\[
 3p^2-23p+28<0.
\]

The second root exceeds three, while the first is

\[
 {23-\sqrt{193}\over6}.
\]

This proves (1). \(\square\)

The dependency-free verifier

```text
python3 verification/verify_dth_equal_marginal_orthogonality_filter.py
```

checks every rational coefficient and the quadratic threshold exactly.
