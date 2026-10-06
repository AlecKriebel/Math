# Bounded follow-up: the published zero-caustic limit

2026-10-06 UTC. This lead was supplied by ROOT **after** the initial independent report was pinned; it does not change that report's independence. Primary preprint: Dragović–Radnović, *Periodic trajectories of ellipsoidal billiards in the 3-dimensional Minkowski space*, [arXiv:1909.08154v1](https://arxiv.org/abs/1909.08154v1), submitted 2019-09-18; parent supplied the 2020 publication DOI [10.1007/978-3-030-57000-2_8](https://doi.org/10.1007/978-3-030-57000-2_8) (publisher fulltext not separately read). Read introduction, §2, §3 including (3.1)–(3.4), Lemma3.3/Proposition3.5, and §4's lightlike polynomial proposition and Remark4.4. Private preprint PDF/text retained locally.

**Result:** the source's printed quadratures do recover the exact scalar closure condition through a valid singular limit, once real surface topology/counts are matched. The limit is not a fixed-reflection-count limit of a Cayley matrix. This strengthens the priority-negative conclusion: there is prior exact-problem resolution evidence with an explicitly reconstructible analytic condition, although the mean formula and normalized arc/winding statement are not printed.

The introduction names GKT Problem5.2 and Tabachnikov Problem7 as solved. Remark4.4 specifies a lightlike trajectory with ellipsoidal caustic approaching the surface caustic. Its theorem proof records polar/belt reflection counts and the $x_2=0$ crossing interpretation. These source claims need the calculation below to avoid treating a bare announcement as a checked equivalence.

## Recovering the finite scalar equation

Set $a_1=a>a_2=b>0$, $a_3=c>0$. First take the source's lightlike limit $\gamma_2\to+\infty$; divide its $P$ by the common positive factor $\gamma_2$. Write $\gamma=\gamma_1\in(0,b)$, so

\[
P_\gamma(x)=(a-x)(b-x)(c+x)(\gamma-x).
\]

The source's real coordinate intervals are \([-c,0]\), \([0,\gamma]\), \([b,a]\). Define

\[
A_k(\gamma)=\int_{-c}^0\frac{x^k\,dx}{\sqrt{P_\gamma(x)}},\quad
B_k(\gamma)=\int_0^\gamma\frac{x^k\,dx}{\sqrt{P_\gamma(x)}},\quad
C_k(\gamma)=\int_b^a\frac{x^k\,dx}{\sqrt{P_\gamma(x)}}.
\]

Its (3.2), with the first integral written in increasing orientation, is

\[
-m_1 A_k+n_1 B_k-n_2 C_k=0,\qquad k=0,1.
\]

Here $m_1,n_1$ count polar/belt reflections; its ambient period is $m_1+n_1$. All radicals in these integrals are positive. As $\gamma\downarrow0$, changing $x=\gamma s$ gives

\[
B_0=\frac{2\sqrt\gamma}{\sqrt{abc}}(1+O(\gamma)),\qquad
B_1=\frac{4\gamma^{3/2}}{3\sqrt{abc}}(1+O(\gamma)),\qquad
\frac{B_1}{B_0}=\frac23\gamma+O(\gamma^2).
\]

$A_0,C_0$ have finite limits: at $x=0^-$, the limiting singularity is $O(|x|^{-1/2})$; the other endpoint square-root singularities are integrable. Eliminate $n_1 B_0=m_1A_0+n_2C_0$ using the $k=0$ equation. If $m_1,n_2$ remain fixed, this gives

\[
n_1B_1=(m_1A_0+n_2C_0)\frac{B_1}{B_0}\longrightarrow0.
\]

In contrast $n_1$ itself grows like $\gamma^{-1/2}$. Thus a finite, fixed ambient $n=m_1+n_1$ limit is not appropriate.

Now $P_0=-x(a-x)(b-x)(c+x)$, and substitutions $x=-v$ and $x=-u$ give

\[
-A_1(0)=I_v,\qquad C_1(0)=I_u=\frac L2.
\]

The finite $k=1$ condition therefore becomes

\[
\boxed{m_1 I_v=n_2 I_u.}
\]

This also agrees directly with the limiting k=1 differential in (3.1): the middle coordinate collapses to zero, leaving the separated null differential in the other two coordinates. It is a third-kind displacement relation; no unsupported ordinary Jacobian torsion step is needed.

## Mapping the topological counts and limits of this inference

In the glancing surface limit, polar reflection points can approach only the tropics: a polar cap has positive-definite tangent metric and therefore no nonzero tangent null vector. They become the switches between the two null families. Hence $m_1=N$, the number of full tropic-to-tropic arcs, which must be even. The source proof interprets $n_2$ as crossings of $x_2=0$. A positive equator-angle winding crosses that plane twice, so $n_2=2r$. Its phrase about tracing the coordinate segment should be read with its crossing convention: a full oscillation comprises two monotone traversals, so identifying $n_2$ with all monotone traversals would introduce a factor-of-two error.

Thus $NI_v=rL$. With the already classical $I_u+I_v=\pi$, this is

\[
N\left(\frac\pi L-\frac12\right)=r,
\qquad M=\frac{N}{N+2r},\qquad N\text{ even}.
\]

The identical path displacement governs the GKT north-tropic equator return; for its $n$ steps, $n\rho=r$, without the arc-endpoint parity requirement. The GKT invariant coordinate and the separated limiting null flow make the scalar relation sufficient for closure on that circle, as well as necessary. Sufficiency here does **not** assert that every closed limiting chain is a limit of closed finite billiards with fixed $m_1,n_2$: integer belt counts and finite billiard periods cannot be held fixed, and such approximating closed orbits were not proved or assumed.

The source's full singular-flow convergence proof and a limiting finite algebraic Cayley criterion with prescribed null-chain counts are not displayed in the inspected text. These remain distinct from the scalar quadrature recovery. Nevertheless, the article explicitly addressed this exact source question before this candidate, and its published equations yield the candidate's analytic condition through the checked elimination above. Claiming a newly solved original problem or a new period identity would now be particularly difficult to defend. At most a separately justified contribution could be clearer exposition, explicit mean formula/count conventions, or treatment of the rotationally symmetric limit; none is established here as a new mathematical result.
