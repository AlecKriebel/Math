# A small-cavity obstruction to the additive boundary eigenvalue bound

## Status and exact claim

This is an authored counterexample argument for the stated class of all bounded smooth Euclidean domains, with no connected-boundary assumption. It uses established existence theorems credited below and has been accepted by an independent internal AI mathematical audit. The AI-assisted proof and audit are unrefereed; no external human peer review, journal acceptance, formal machine proof, historical novelty or priority is claimed.

For every fixed integer m >= 2, there are bounded, connected, smooth domains Ω_q in R^(m+1), whose boundaries have exactly two connected components, and indices k_q, for which

λ_{k_q}(∂Ω_q) |∂Ω_q|^(2/m) / (I(Ω_q)^(1+2/m) + k_q^(2/m)) → infinity.

Here I(Ω)=|∂Ω|/|Ω|^(m/(m+1)), and eigenvalues are listed with multiplicity as 0=λ_1<=λ_2<=..., including one zero per connected component. Consequently the requested constants A_m,B_m do not exist, in any dimension m >= 2. The spectrum is the intrinsic Laplace–Beltrami spectrum of the induced boundary metric.

## Established inputs

1. Colbois–Dryden–El Soufi, Theorem 1.4: the scale-invariant quantity λ_2(M)|M|^(2/m) is unbounded among smooth compact connected hypersurfaces embedded in R^(m+1). For m=2 topology may vary; for m>=3 one may fix the abstract manifold to be S^m. Their indexing calls the first positive eigenvalue λ_1; our indexing calls it λ_2. Their Section 5 gives the derivation from large-eigenvalue metrics, the Nash–Kuiper theorem, and smoothing.
2. Nash–Kuiper, in its C^0 approximation form: a smooth strictly short embedding of a compact Riemannian m-manifold into R^(m+1) can be approximated uniformly by C^1 isometric embeddings. A precise statement is also given in De Lellis–Székelyhidi, Theorem 1.2.
3. Standard smooth approximation of C^1 embeddings of compact manifolds, and the Jordan–Brouwer separation theorem for smooth compact connected embedded hypersurfaces.

The necessary quantitative spectral-continuity step is proved next, rather than assumed to preserve a merely C^1 spectrum without explanation.

## Lemma 1: metric comparison

Let g and h be metrics on a fixed compact smooth m-manifold and suppose, as quadratic forms,

c^(-1) g <= h <= c g, where c>=1.

Then c^(-m/2) dV_g <= dV_h <= c^(m/2) dV_g. Also, for every nonzero function u in H^1,

c^(-(m+1)) R_g(u) <= R_h(u) <= c^(m+1) R_g(u).

Indeed, the inverse metrics compare by the same two factors c^(-1),c. Thus the Dirichlet energies compare by c^(±(1+m/2)), whereas the squared L^2 norms compare by c^(±m/2). Division gives the displayed Rayleigh comparison. The min–max principle on the same function space gives the same bounds for every numbered eigenvalue, zeros included. In particular, uniform convergence of positive-definite metrics implies convergence of volume and of every fixed eigenvalue.

## Lemma 2: prescribed area and gap in a prescribed small ball

Fix m>=2. For any S>0, L>0, and r>0, there is a smooth compact connected hypersurface H embedded in B(0,r)⊂R^(m+1) such that

|H|=S and λ_2(H)>L.

Proof. By established input 1, choose a connected smooth manifold M admitting a smooth hypersurface embedding and a smooth metric g_0 with

λ_2(g_0)|M,g_0|^(2/m) > 2 L S^(2/m).

Rescale g_0 to a metric g with |M,g|=S. Then λ_2(g)>2L. Take any smooth embedding e of M in R^(m+1). By multiplying e by a sufficiently small positive constant, arrange both that its image lies in B(0,r/8) and that e^*g_Eucl<g. The latter follows from compactness and positive definiteness of g.

Nash–Kuiper gives a C^1 isometric embedding f:(M,g)→R^(m+1) uniformly close enough to e that f(M)⊂B(0,r/4). Approximate f in C^1 by smooth embeddings f_j. Embeddings remain embeddings under sufficiently small C^1 perturbations on compact M. For all sufficiently large j, f_j(M)⊂B(0,r/3), and the smooth induced metrics h_j=f_j^*g_Eucl converge uniformly to g. Lemma 1 gives S_j=|M,h_j|→S and λ_2(h_j)→λ_2(g)>2L.

Put a_j=(S/S_j)^(1/m) and H_j=a_j f_j(M). Then |H_j|=S, a_j→1, and

λ_2(H_j)=a_j^(-2)λ_2(h_j)→λ_2(g)>2L.

For large j, a_j<2, so H_j⊂B(0,2r/3)⊂B(0,r), and λ_2(H_j)>L. Choose such a j. Every final hypersurface is smooth, even though the intermediate isometric embedding is only C^1. ∎

## Construction of connected domains with two boundary components

Write ω_{m+1}=|B(0,1)| and ρ_m=|S^m|=(m+1)ω_{m+1}. For an integer q>=1 define

T_q=q(q+m-1).

Apply Lemma 2 with S=q, L=T_q, and r=1/2 to obtain H_q⊂B(0,1/2), with |H_q|=q and λ_2(H_q)>T_q. The hypersurface is connected. By Jordan–Brouwer separation it is the boundary of its bounded complementary component U_q. Moreover U_q⊂B(0,1/2): every point outside the closed half-radius ball can be joined to infinity without meeting H_q, so belongs to the unbounded component.

Define Ω_q=B(0,1)\overline{U_q}. It is a bounded smooth open domain with

∂Ω_q=S^m ⊔ H_q.

It is connected. To check this explicitly, let E_q be the unbounded component of R^(m+1)\H_q. This is connected and open, hence path-connected. Every point x∈E_q∩B(0,1) can be connected in E_q to a point outside B(0,1). If x is inside B(0,3/4), stop such a path when it first reaches the sphere of radius 3/4; the stopped path lies in B(0,3/4) and hence in Ω_q. If x is outside that sphere, it lies in the full annulus B(0,1)\overline{B(0,1/2)}, which is path-connected. Thus all points connect to that annulus inside Ω_q. Also E_q∩B(0,1)=Ω_q.

The volume and boundary area obey

v_m:=ω_{m+1}(1-2^(-(m+1))) <= |Ω_q| <= ω_{m+1},

|∂Ω_q|=ρ_m+q.

In particular,

I(Ω_q)^(1+2/m) <= v_m^(-(m+2)/(m+1)) (ρ_m+q)^(1+2/m).                 (1)

The orientation of the cavity component has no effect on its intrinsic spectrum.

## Exact index and spectral counting

The unit m-sphere has eigenvalues ℓ(ℓ+m-1), ℓ=0,1,2,..., of multiplicity

d_{m,ℓ}=binom(ℓ+m,m)-binom(ℓ+m-2,m),

where a binomial coefficient is zero when its nonnegative upper index is less than its lower index. For ℓ=0,1 the same formula is understood with the second term zero. This follows by subtracting the dimension of homogeneous polynomials of degree ℓ-2 from that of degree ℓ in m+1 variables, using harmonic decomposition.

There are exactly

N_q=sum_{ℓ=0}^{q-1}d_{m,ℓ}=binom(q+m-1,m)+binom(q+m-2,m)

sphere eigenvalues strictly below T_q. The inner component has exactly one eigenvalue below T_q, namely its zero eigenvalue, since it is connected and λ_2(H_q)>T_q. Spectra of disjoint unions are multiset unions. Therefore, setting

k_q=N_q+2,

we have the exact identity

λ_{k_q}(∂Ω_q)=T_q.                                                   (2)

Both zero eigenvalues have been counted. No Weyl-law limit uniform in varying metrics is being invoked.

For q>=m,

k_q <= 2(q+m)^m+2 <= 2^(m+2) q^m,

and hence

k_q^(2/m) <= C_m q^2, where C_m=2^(2+4/m).                          (3)

## Contradiction to every proposed pair of constants

Suppose dimension-only positive constants A_m,B_m satisfy the proposed inequality. Equations (1)–(3) give, for q>=m,

q(q+m-1)(q+ρ_m)^(2/m)
  <= A_m v_m^(-(m+2)/(m+1))(q+ρ_m)^(1+2/m) + B_m C_m q^2.

Divide by q^2(q+ρ_m)^(2/m). Since q(q+m-1)>=q^2, this implies

1 <= A_m v_m^(-(m+2)/(m+1)) (q+ρ_m)/q^2
     + B_m C_m/(q+ρ_m)^(2/m).

The right side tends to zero as q→infinity, a contradiction. This proves the claim in every m>=2. Equivalently, even the quotient with the sum of the two unweighted target terms tends to infinity.

## Scope and consistency checks

- Ω_q itself is connected; its boundary has exactly two connected components, as permitted by the stated question. This argument makes no additional claim for connected boundaries.
- The construction works with smooth induced metrics, with no singular or C^1 final domain. The smoothing is performed separately for each q; no uniform smoothness bound is needed or assumed.
- For m>=3, H_q can be diffeomorphic to S^m. For m=2 its genus is allowed to vary. The question has no topology restriction.
- The known multiplicative estimate is not contradicted: its right-hand side contains the additional factor k_q^(2/m), so it is much larger in this regime.
- At each fixed q, ordinary Weyl asymptotics are also unaffected. The index k_q is allowed to vary together with the domain, which is exactly what a uniform-in-domain, uniform-in-k assertion must permit.
- The argument does not establish or use a Dirichlet, Neumann, Robin, Wentzell, or Steklov bound.

## References and source credit

[OWR] B. Colbois, “Upper bounds for the spectrum of Riemannian manifolds,” in Geometric Aspects of Spectral Theory, Oberwolfach Report 33/2012, printed pp. 2034–2036. The exact additive question is on p. 2036. https://doi.org/10.4171/owr/2012/33 ; public report: https://ems.press/content/serial-article-files/46403

[CDE] B. Colbois, E. B. Dryden, A. El Soufi, “Bounding the eigenvalues of the Laplace–Beltrami operator on compact submanifolds,” Bull. Lond. Math. Soc. 42 (2010), 96–108, Theorem 1.4 and Section 5. https://doi.org/10.1112/blms/bdp100 ; author preprint: https://arxiv.org/abs/0909.5346

[CEG] B. Colbois, A. El Soufi, A. Girouard, “Isoperimetric control of the spectrum of a compact hypersurface,” Theorem 1.1. https://doi.org/10.1515/crelle-2012-0008 ; author preprint: https://arxiv.org/abs/1007.0826

[NK] J. Nash, “C^1 isometric imbeddings,” Ann. of Math. 60 (1954), 383–396; N. H. Kuiper, “On C^1-isometric imbeddings,” I, II, Indag. Math. 17 (1955), 545–556, 683–689. The C^0-dense embedding form used here is stated precisely as Theorem 1.2 in C. De Lellis and L. Székelyhidi Jr., “John Nash’s nonlinear iteration”: https://www.math.ias.edu/delellis/sites/math.ias.edu.delellis/files/contr_vol_Nash_11.pdf

[H] M. W. Hirsch, Differential Topology, Graduate Texts in Mathematics 33, Springer, 1976, smooth approximation of C^1 embeddings (also explicitly used and cited at p. 14 of the CDE preprint).

The authored contribution of this note is the two-component cavity construction, exact sphere-mode bookkeeping, and asymptotic contradiction, conditional only on the named established inputs. This wording makes no historical novelty or priority claim: a bounded literature check cannot establish whether this combination has appeared before.
