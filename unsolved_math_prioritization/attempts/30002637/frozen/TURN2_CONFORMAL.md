# Author turn 2/5: conformal, potential-eigenfunction, and scalar-curvature route

**Target.** Prove that every compact smooth non-Einstein gradient shrinking Ricci soliton has a positive second-variation direction for Perelman's ν entropy after diffeomorphisms and scaling are removed, without a Kähler or dimension restriction.

**Outcome of this turn.** No proof of the target is obtained. This turn gives an exact conformal quadratic form, an exact Rayleigh formula for the centered soliton potential times the metric, and an explicit nonzero tensor in the correct quotient whose sign is a scalar exponential-moment inequality. The unresolved issue is an actual sign inequality; neither the existence of the potential eigenfunction nor its eigenvalue establishes it. The scalar-curvature test has the same unresolved sign problem. No Ricci or potential-Hessian gauge direction is counted as instability.

All formulas below are calculations from the cited shrinker and ν-Hessian identities. This attempt does not resolve the target or assert a new general instability theorem.

## 1. Notation, prior input, and elementary shrinker identities

Write

\[
\operatorname{Ric}+\nabla^2 f=\lambda g,\qquad \lambda=(2\tau)^{-1}>0,
\]

and use the probability measure

\[
d\rho=Z^{-1}e^{-f}\,dV,\qquad \mathbb E[a]=\int_M a\,d\rho.
\]

The normalization does not change the sign of a quadratic form. Put

\[
A=-\Delta_f,\quad F=f-\mathbb E[f],\quad S=|\nabla f|^2,
\quad r=\mathbb E[R],\quad m_j=\mathbb E[F^j].
\]

The standard soliton identities give

\[
AF=2\lambda F,\qquad R+S=n\lambda+2\lambda F,
\qquad \Delta f=n\lambda-R=S-2\lambda F.                 \tag{1.1}
\]

In particular,

\[
\mathbb E[S]=2\lambda m_2,\qquad r=\lambda(n-2m_2),
\qquad \mathbb E[|\operatorname{Ric}|^2]=\lambda r.         \tag{1.2}
\]

The last identity is the weighted integral of
\(\Delta_fR=2\lambda R-2|\operatorname{Ric}|^2\).
It implies \(r>0\): Ricci curvature cannot vanish identically on a compact positive shrinker, since the unweighted integral of the trace equation is \(\int R=n\lambda\operatorname{Vol}(M)\).
Thus

\[
0<m_2<n/2                                                   \tag{1.3}
\]

for a non-Einstein soliton. The strict lower bound follows because a constant potential is Einstein.

For an eigenfunction \(Au=\mu u\), \(\mu>0\), weighted Bochner integration gives

\[
\mathbb E[|\nabla^2u|^2]=\mu(\mu-\lambda)\mathbb E[u^2].     \tag{1.4}
\]

Consequently every positive scalar eigenvalue satisfies \(\mu>\lambda\). Equality would make \(\nabla^2u=0\), and hence \(u\) constant on the compact manifold. In the non-Einstein case (1.1) also gives \(\mu_1\leq2\lambda\).

On mean-zero functions define the strictly positive operator

\[
B=A-\lambda.
\]

The stability theorem used is the Cao–Zhu quotient decomposition. With

\[
L_f=\tfrac12\Delta_f+\operatorname{Rm},\qquad
V=\ker\operatorname{div}_f\cap\operatorname{Ric}^{\perp},
\]

the ν operator is

\[
N_fh=L_fh+\operatorname{div}_f^{\dagger}\operatorname{div}_fh
 +\tfrac12\nabla^2v_h
 -\operatorname{Ric}\,\frac{\mathbb E[\langle\operatorname{Ric},h\rangle]}{r},
\]

where

\[
(\Delta_f+\lambda)v_h=\operatorname{div}_f\operatorname{div}_fh,
\qquad\mathbb E[v_h]=0.                                     \tag{1.5}
\]

We write

\[
Q(h)=\mathbb E[\langle N_fh,h\rangle].
\]

The actual ν-Hessian has the same sign. Cao–Zhu proves that \(N_f\) vanishes on diffeomorphism directions and on the Ricci line, and equals \(L_f\) on \(V\). Therefore a positive \(Q(ug)\), if established, really would yield a positive quotient direction by orthogonal projection onto \(V\).

Notice the essential gauge cancellation:

\[
g=\lambda^{-1}(\operatorname{Ric}+\nabla^2 f),\qquad N_fg=0.  \tag{1.6}
\]

Neither \(\operatorname{Ric}\), \(g\), nor \(\nabla^2f\) is an unstable ν direction.

## 2. Exact conformal quadratic form

For any smooth real scalar function \(u\), set \(h=ug\). Direct calculation gives

\[
\operatorname{div}_f(ug)=du-u\,df=:a_u,
\]

and

\[
q_u:=\operatorname{div}_f\operatorname{div}_f(ug)
 =\Delta_fu-\langle\nabla f,\nabla u\rangle-u\Delta_ff
 =-Au-\langle\nabla F,\nabla u\rangle+2\lambda Fu.           \tag{2.1}
\]

The function \(q_u\) has weighted mean zero, and (1.5) is exactly

\[
v_{ug}=-B^{-1}q_u.
\]

The individual Hessian terms are

\[
\mathbb E[\langle L_f(ug),ug\rangle]
=-\frac n2\mathbb E[|du|^2]+\mathbb E[Ru^2],
\]

\[
\mathbb E[\langle\operatorname{div}_f^\dagger
       \operatorname{div}_f(ug),ug\rangle]
=\mathbb E[|du-u\,df|^2],
\]

and, by two weighted integrations by parts,

\[
\mathbb E[\langle\nabla^2v_{ug},ug\rangle]
=\mathbb E[v_{ug}q_u]
=-\langle q_u,B^{-1}q_u\rangle_{L^2(\rho)}.
\]

For the first two terms, integrate the cross term in \(|du-u\,df|^2\):

\[
\mathbb E[-2u\langle du,df\rangle]
=\mathbb E[u^2\Delta_ff],
\]

so their sum is

\[
-\frac{n-2}{2}\mathbb E[|du|^2]
+\mathbb E[(R+S+\Delta_ff)u^2]
=-\frac{n-2}{2}\mathbb E[|du|^2]+n\lambda\mathbb E[u^2].
\]

Thus the exact formula is

\[
\boxed{
Q(ug)=n\lambda\mathbb E[u^2]
-\frac{n-2}{2}\mathbb E[|du|^2]
-\frac12\langle q_u,B^{-1}q_u\rangle
-\frac{\mathbb E[Ru]^2}{r}.
}                                                            \tag{2.2}
\]

The resolvent term is nonpositive. Omitting it would turn an upper bound into a supposed lower bound and can generate a false instability proof.

### Two checks on the formula

For \(u=1\), \(q_1=2\lambda F\) and \(B^{-1}F=\lambda^{-1}F\), so

\[
Q(g)=n\lambda-2\lambda m_2-r=0,
\]

as required by scaling invariance. More generally,

\[
\langle F,q_u\rangle
=\mathbb E[u\Delta F]=n\lambda\mathbb E[u]-\mathbb E[Ru],
\]

which verifies directly that the polarization of (2.2) with the constant function vanishes. Hence

\[
Q((u+c)g)=Q(ug).                                             \tag{2.3}
\]

Second, when the shrinker is Einstein, \(F=0\), \(R=n\lambda\), and a mean-zero eigenfunction \(Au=\mu u\) has \(q_u=-\mu u\). Formula (2.2) becomes

\[
\frac{Q(ug)}{\mathbb E[u^2]}
=n\lambda-\frac{n-2}{2}\mu-\frac{\mu^2}{2(\mu-\lambda)}
=\frac{(2\lambda-\mu)((n-1)\mu-n\lambda)}{2(\mu-\lambda)}.
                                                               \tag{2.4}
\]

This recovers the familiar conformal instability interval
\(n\lambda/(n-1)<\mu<2\lambda\) and the neutral value \(\mu=2\lambda\). The forced eigenvalue of a non-Einstein potential is exactly this neutral endpoint, not a strictly unstable Einstein eigenvalue.

## 3. Exact Rayleigh formula for \(Fg\)

This is the most direct test of whether the existence of a nonconstant soliton potential forces conformal instability.

Put

\[
w=F^2-m_2,\qquad\mathbb E[w]=0.
\]

From \(AF^2=4\lambda F^2-2S\), (2.1) gives

\[
q_F=-2\lambda F-S+2\lambda F^2
=-2\lambda F+\tfrac12Aw.                                   \tag{3.1}
\]

Weighted integration of \(\Delta_fF^3\) and \(\Delta_fF^4\) gives

\[
\mathbb E[FS]=\lambda m_3,\qquad
\mathbb E[F^2S]=\frac{2\lambda}{3}m_4.                       \tag{3.2}
\]

Hence

\[
\mathbb E[RF]=\lambda(2m_2-m_3),\quad
\langle F,w\rangle=m_3,\quad
\langle w,Aw\rangle=\frac{8\lambda}{3}m_4.                  \tag{3.3}
\]

Since \(AF=2\lambda F\), self-adjointness yields

\[
\langle q_F,B^{-1}q_F\rangle
=4\lambda m_2-4\lambda m_3
 +\frac14\langle Aw,B^{-1}Aw\rangle.                         \tag{3.4}
\]

The favorable first two terms of (2.2) are only \(2\lambda m_2\). The \(4\lambda m_2\) part of (3.4) cancels them exactly. Therefore

\[
\boxed{
Q(Fg)=2\lambda m_3
-\frac18\langle Aw,B^{-1}Aw\rangle
-\lambda\frac{(2m_2-m_3)^2}{n-2m_2}.
}                                                            \tag{3.5}
\]

Equivalently, using the spectral identity
\(A^2(A-\lambda)^{-1}=A+\lambda+\lambda^2(A-\lambda)^{-1}\),

\[
\boxed{
\frac{Q(Fg)}{\lambda}
=2m_3
-\frac18\left(\frac{11}{3}m_4-m_2^2
                 +\lambda\langle w,B^{-1}w\rangle\right)
-\frac{(2m_2-m_3)^2}{n-2m_2}.
}                                                            \tag{3.6}
\]

This identifies the precise missing sign. Positivity of this particular test is equivalent to

\[
16m_3>
\frac{11}{3}m_4-m_2^2+\lambda\langle w,B^{-1}w\rangle
+8\frac{(2m_2-m_3)^2}{n-2m_2}.                               \tag{3.7}
\]

No identity above establishes (3.7). All terms on the right form a strictly positive quantity for a nonconstant smooth \(F\). In particular, **if** \(m_3\leq0\), this test is strictly negative. This is a conditional conclusion, not an assertion that such a shrinker exists. Even \(m_3>0\) is insufficient: it must dominate the fourth moment, a genuinely nonlocal resolvent expression, and the Ricci-projection penalty.

One rigorous upper estimate follows by retaining the \(F\)-spectral component of \(w\):

\[
\lambda\langle w,B^{-1}w\rangle\geq\frac{m_3^2}{m_2}.
\]

Also \(m_4\geq m_2^2+m_3^2/m_2\), by projecting \(F^2\) onto \(\operatorname{span}\{1,F\}\). Consequently

\[
\frac{Q(Fg)}{\lambda}
\leq2m_3-\frac13m_2^2-\frac7{12}\frac{m_3^2}{m_2}
-\frac{(2m_2-m_3)^2}{n-2m_2}.                               \tag{3.8}
\]

This is an obstruction/upper bound, not the positive lower bound a proof needs. No available shrinker identity forces the right-hand side, or the exact expression, to be positive.

For an additional independent check, weighted Bochner applied to \(S\) gives

\[
\Delta_fS=2|\nabla^2f|^2-2\lambda S,
\qquad\mathbb E[F|\nabla^2f|^2]=0.
\]

The latter identity does not determine the sign in (3.5); replacing \(Fg\) by \(\nabla^2f\) would instead return to a gauge direction.

## 4. General scalar eigenfunctions: why the eigenvalue alone is insufficient

For \(Au=\mu u\), the product rule gives

\[
A(Fu)=(2\lambda+\mu)Fu-2\langle\nabla F,\nabla u\rangle,
\]

so

\[
q_u=-\mu u+\tfrac12(A+2\lambda-\mu)(Fu).                    \tag{4.1}
\]

Thus the drift correction couples \(u\) to the entire scalar spectral expansion of \(Fu\).
If \(u\) is a normalized eigenfunction and \(\{\phi_k\}_{k\geq1}\) is a weighted orthonormal mean-zero scalar eigenbasis, \(A\phi_k=\mu_k\phi_k\), then

\[
Q(ug)=n\lambda-\frac{n-2}{2}\mu
-\frac12\sum_{k\geq1}
\frac{\left[-\mu\langle u,\phi_k\rangle
+\frac12(\mu_k+2\lambda-\mu)\langle Fu,\phi_k\rangle\right]^2}
     {\mu_k-\lambda}
-\frac{\mathbb E[Ru]^2}{r}.                                 \tag{4.2}
\]

The Einstein calculation (2.4) is recovered only when \(F=0\). Merely proving that \(-\Delta_f\) has an eigenvalue below \(2\lambda\), even if possible, would not by itself justify importing the Einstein sign computation into a non-Einstein shrinker. One needs quantitative control of the multiplication coefficients \(\langle Fu,\phi_k\rangle\) and the Ricci overlap, or another argument that incorporates them.

## 5. An explicit, nonzero tensor already in the correct quotient

There is one especially simple way to avoid both the gauge-projection PDE and the resolvent:

\[
\operatorname{div}_f(e^Fg)=d(e^F)-e^Fdf=0.
\]

Let

\[
M(t)=\mathbb E[e^{tF}],\qquad M'(t)=\mathbb E[Fe^{tF}].
\]

The unweighted integral of the trace equation gives

\[
\mathbb E[Re^F]=n\lambda M(1).
\]

Together with (1.2), this shows that

\[
\boxed{
 h_{\exp}=e^Fg-\frac{nM(1)}{r}\operatorname{Ric}\ \in V.
}                                                            \tag{5.1}
\]

This is a genuine quotient tensor. For a non-Einstein shrinker it is nonzero: if \(e^Fg\) were a constant multiple of \(\operatorname{Ric}\), the Ricci tensor would be a scalar function times the metric, and the contracted Bianchi identity in dimension \(n>2\) would force that scalar, and then \(F\), to be constant. The low-dimensional compact shrinkers are Einstein; the target's non-Einstein case does not occur there.

Because \(q_{e^F}=0\), (2.2) yields

\[
Q(h_{\exp})=n\lambda M(2)
-\frac{n-2}{2}\mathbb E[e^{2F}S]
-\frac{n^2\lambda^2 M(1)^2}{r}.
\]

Integrating \(\operatorname{div}_f(e^{2F}\nabla F)\) gives
\(\mathbb E[e^{2F}S]=\lambda M'(2)\). Therefore

\[
\boxed{
\frac{Q(h_{\exp})}{\lambda}
=nM(2)-\frac{n-2}{2}M'(2)
-\frac{n^2M(1)^2}{n-2m_2}.
}                                                            \tag{5.2}
\]

This is a concrete sufficient criterion for the full target on any particular shrinker:

\[
nM(2)>\frac{n-2}{2}M'(2)+\frac{n^2M(1)^2}{n-2m_2}.           \tag{5.3}
\]

But there is no proof here that every non-Einstein compact shrinker satisfies it. Its sign is transparently competing if rewritten as

\[
\frac{Q(h_{\exp})}{\lambda}
=n\bigl(M(2)-M(1)^2\bigr)
-\frac{n-2}{2}M'(2)
-\frac{2nm_2}{n-2m_2}M(1)^2.                                \tag{5.4}
\]

The first term is positive variance; the other two are negative. In particular, Cauchy–Schwarz \(M(2)>M(1)^2\) and nonconstancy of \(F\) alone do not prove positivity. Treating that strict variance inequality as sufficient would discard both genuine penalties.

## 6. Scalar curvature as a conformal test

Non-Einstein compact shrinkers have nonconstant \(R\): if \(R\) were constant, the unweighted trace integral would give \(R=n\lambda\), then \(\Delta f=0\), then \(f\) constant.
Thus \(u=R-r\) is a nonzero mean-zero scalar test. Set

\[
K=|\operatorname{Ric}|^2,\qquad
J=\operatorname{Ric}(\nabla f,\nabla f),\qquad
\sigma_R^2=\mathbb E[(R-r)^2].
\]

The identities \(\Delta_fR=2\lambda R-2K\) and \(dR=2\operatorname{Ric}(df,\cdot)\) give the exact forcing

\[
q_{R-r}=2\lambda R-2K-2J+2\lambda F(R-r).                   \tag{6.1}
\]

Thus

\[
\boxed{
Q((R-r)g)=n\lambda\sigma_R^2
-\frac{n-2}{2}\mathbb E[|dR|^2]
-\frac12\langle q_{R-r},B^{-1}q_{R-r}\rangle
-\frac{\sigma_R^4}{r}.
}                                                            \tag{6.2}
\]

Here \(\sigma_R^4\) means \((\sigma_R^2)^2\). Alternatively,

\[
\mathbb E[|dR|^2]
=2\operatorname{Cov}_{\rho}(R,K)-2\lambda\sigma_R^2,
\]

so the first two terms in (6.2) equal

\[
2(n-1)\lambda\sigma_R^2-(n-2)\operatorname{Cov}_{\rho}(R,K).
\]

The scalar evolution equation therefore does not close this sign either. Nonzero curvature variance produces the favorable term, but it also brings a gradient/covariance cost, a resolvent cost, and the scaling-projection cost. No general bound established in this turn makes the favorable term dominate them.

## 7. Precise endpoint and usable next input

The conformal route remains unresolved at these specific points:

1. For the canonical potential test \(Fg\), the missing claim is the strict moment/resolvent inequality (3.7). The favorable quadratic potential term cancels exactly, so a claim based only on \(AF=2\lambda F\) is invalid.
2. For the explicit quotient tensor \(h_{\exp}\), the missing claim is the strict exponential-moment inequality (5.3). It is a concrete sufficient condition with no gauge ambiguity, but it is not known here to hold universally.
3. For an arbitrary low scalar eigenfunction, formula (4.2) has additional multiplication and projection terms absent from the Einstein formula. A scalar spectral gap alone does not settle their sign.
4. For the scalar-curvature test, equation (6.2) needs quantitative control of three nonpositive terms, not merely \(R\) nonconstant.

Failure of any one of these tests would not prove ν-stability: positive directions could lie outside this conformal family. Conversely, positivity of any one exact expression would be a legitimate instability certificate in the full quotient. No example or formal moment distribution is claimed to realize a compact soliton unless it actually does.

### Verification record

- Derived every sign using weighted adjoints, in the Cao–Zhu convention \(L_f=\frac12\Delta_f+\operatorname{Rm}\).
- Checked the constant conformal direction gives zero, including its polarization with every \(u\).
- Checked the Einstein scalar-eigenfunction specialization gives (2.4), with the correct neutral and gauge endpoints.
- Expanded the potential resolvent both spectrally, (3.4)–(3.5), and by \(A^2/(A-\lambda)\), (3.6).
- A local SymPy check returned zero for the difference in (2.4), zero for the difference between the two potential formulas, and zero for the constant scaling check.
- Independently computed the exponential test from \(\operatorname{div}_f(e^Fg)=0\), then projected onto Ricci-perpendicular tensors using \(\mathbb E[|\operatorname{Ric}|^2]=\lambda r\).

### Prior-source attribution

- H.-D. Cao and M. Zhu, *Linear Stability of Compact Shrinking Ricci Solitons*, arXiv:2304.01453v4 (2024), especially the ν-Hessian formula and Theorems 1.1–1.2: https://arxiv.org/abs/2304.01453 . The quotient theorem is prior credit, not a contribution of this turn.
- S. J. Hall and T. Murphy, *On the Linear Stability of Kähler–Ricci Solitons*, arXiv:1008.1023 (2011): https://arxiv.org/abs/1008.1023 . The paper notes the potential eigenvalue and asks about intermediate weighted scalar eigenvalues. Its Kähler/Hodge instability result is not used as a proof of the unrestricted target.
- Original target: K. Kröncke, Oberwolfach Reports 11 (2014), pp. 2017–2019, DOI https://doi.org/10.4171/OWR/2014/36 . Cao–Zhu 2024 still states the compact stability-implies-Einstein conjecture. This note does not change its unresolved status.
