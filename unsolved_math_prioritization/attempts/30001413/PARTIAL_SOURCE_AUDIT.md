# Hinged-plate positivity: credited weakenings and the remaining domain question

**30001413 / OWR-4209-002. Conservative status: unsolved, 2/5 approaches.** The original C^{2,1} hypothesis is not optimal: a published theorem permits convex C^{1,1} domains. Smooth nonconvex domains also have a positivity interval in sigma near 1, by an earlier published theorem. The optimal geometric/regularity characterization, with the original parameter quantifiers retained, is not established here. Separate review is pending; no novelty claim.

## 1. Exact original problem

The full source is Enea Parini's contribution, joint with Athanasios Stylianou, in [Oberwolfach Report 8/2010](https://ems.press/content/serial-article-files/46265), printed pp.335–336. It concerns the energy

    I_sigma(u)=1/2 integral_Omega (Delta u)^2
                 -(1-sigma) integral_Omega det(D^2 u)
                 -integral_Omega f*u

on H=H^2(Omega) intersect H^1_0(Omega), for a bounded planar domain, f in L^2(Omega), and **-1<sigma<1**. The report distinguishes this mathematical interval from the narrower physical interval -1<sigma<1/2. The formal boundary problem is

    Delta^2 u=f,
    u=0,
    Delta u-(1-sigma)*kappa*partial_n u=0 on the boundary,

with outward normal derivative and signed curvature nonnegative on convex boundary pieces. Its Theorem 1 gives positivity, with a distance-to-boundary lower bound, under convexity and C^{2,1} regularity. The final paragraph asks whether and how the domain assumptions can be improved, singling out the higher regularity as apparently technical.

The object is the variational H^2 solution of this curvature-dependent problem. Replacing it by an iterated Dirichlet Laplacian on a rough nonconvex domain is not legitimate. The original report already cites examples with concave corners where positivity fails.

## 2. What the primary literature already establishes

1. **Convex C^{1,1} domains.** Giulio Romani, [*Analysis & PDE* 10 (2017), 943–982](https://msp.org/apde/2017/10-4/apde-v10-n4-p06-s.pdf), Theorem 4.7, Proposition 4.9 and especially **Remark 4.10, p.956**, explicitly extends the original *linear* positivity result to bounded convex C^{1,1} domains. It is not necessary to infer a linear all-load theorem merely from the paper's semilinear abstract. The crucial determinant boundary identity is Theorem 4.7, p.954.
2. **Smooth domains with a small curvature coefficient.** Gazzola–Sweers, [*Arch. Rational Mech. Anal.* 188 (2008), 399–427](https://gazzola.faculty.polimi.it/hinged.pdf), Theorems 2.3 and 4.1, provide constants delta_c(Omega)<0<delta_1(Omega), with delta_c possibly minus infinity, for the boundary coefficient alpha in Delta u=alpha*partial_n u. A coefficient lying strictly between those two constants gives a positive variational solution for every nonzero nonnegative L^2 load. This includes sign-changing coefficients and gives the near-1 consequence in Section 5 below.
3. [Antunes–Gazzola (2013)](https://www.numdam.org/item/10.1051/cocv/2012014.pdf), Theorem 2.1 and Corollary 2.2, already record a C^2 convex-domain version and the boundary-coefficient positivity interval. This is corroboration, not an optimal-domain classification.

The full primary PDFs above were retrieved. The later [Romani 2025 version](https://arxiv.org/abs/2304.14945v3) treats positivity of semilinear ground states on certain nonconvex deformations of limaçons with a parameter threshold. That result is not a theorem about every nonnegative forcing in the original linear problem and is not substituted for one here. The 2018 stressed-plate result has an additional differential term and retains convexity; it does not by itself answer this domain question.

## 3. Direct specialization of the known C^{1,1} argument

This section supplies a proof-level linear specialization of Romani's published method, with its identity credited. It is not presented as a new theorem.

**Proposition.** Let Omega be bounded and convex with C^{1,1} boundary. For each -1<sigma<1 and f in L^2(Omega), the energy has a unique minimizer u in H. If f>=0, then u>=0 and -Delta u>=0. If additionally f is not identically zero, then u>0 in the interior.

### Existence, uniqueness and the actual weak boundary problem

For a symmetric Hessian with entries p=u_xx, q=u_yy, r=u_xy, twice the quadratic energy density is

    Q_sigma=p^2+q^2+2*sigma*p*q+2*(1-sigma)*r^2
      =(1+sigma)/2*(p+q)^2
        +(1-sigma)/2*(p-q)^2+2*(1-sigma)*r^2.

It is bounded below by (1-|sigma|)*(p^2+q^2+2r^2). On H, the Hessian norm controls the full H^2 norm: Poincare's inequality and

    norm(grad u)^2 = -integral u*Delta u

give the lower-order estimates. Thus the energy is strictly convex and coercive, and the L^2 load is continuous. The standard Hilbert-space variational argument gives the unique minimizer.

Romani's C^{1,1} identity is

    integral_Omega det(D^2 v)
      =1/2 integral_boundary kappa*(partial_n v)^2,       v in H.       (1)

Here kappa is an L^infinity boundary function defined almost everywhere, and the normal trace is well-defined. Polarizing (1) yields the weak equation

    integral Delta u*Delta phi
      -(1-sigma) integral_boundary kappa*u_n*phi_n
      =integral f*phi,                                    phi in H.  (2)

This is the original hinged problem in its variational sense. A pointwise trace of Delta u for an arbitrary H^2 function is not being assumed.

### Superharmonic comparison without truncating an H^2 function

Let w be the Dirichlet solution of -Delta w=|Delta u|. Standard L^2 Dirichlet regularity on C^{1,1} domains gives w in H. The weak second-order maximum principle applied to w-u and w+u gives

    w>=u,   w>=-u.

Both differences vanish on the boundary. Their outward normal traces are nonpositive almost everywhere. One way to see this trace sign is to use the C^{1,1} inward collar: for a nonnegative H^2 function v with zero trace, the nonnegative quotients v(s-t*n(s))/t converge in L^2 on the boundary to -v_n. Therefore

    w_n<=u_n,   w_n<=-u_n,
    w_n^2>=u_n^2.                                                   (3)

Also norm(Delta w)_2=norm(Delta u)_2. Since kappa>=0 almost everywhere, 1-sigma>0 and f>=0, equations (1) and (3) imply

    I_sigma(w)-I_sigma(u)
      =-(1-sigma)/2 integral_boundary kappa*(w_n^2-u_n^2)
        -integral f*(w-u) <= 0.

The unique-minimizer property forces w=u. Hence -Delta u=|Delta u|>=0 and u>=0. If f is nonzero, (2) prevents u from being zero; the strong second-order maximum principle applied to this nontrivial superharmonic Dirichlet function gives u>0 in the connected domain.

Only non-strict comparison inequalities are needed; there is no assumption that w is strictly larger than |u| in every case. Nor is |u| used as an H^2 test function, since it need not belong to H^2.

## 4. An explicit domain outside the original regularity class

Take the open stadium

    Omega_st={x in R^2: dist(x,[-1,1] times {0})<1}.

It is bounded, convex and has C^{1,1} boundary. Straight horizontal pieces join unit semicircles with matching tangents and Lipschitz tangent field. At the upper-right join, its graph is y=1 for x<=1 and y=sqrt(1-(x-1)^2) for x>=1, locally. The first derivatives agree at the join, but the one-sided second derivatives are 0 and -1. Thus it is not C^2, and in particular not C^{2,1}.

The proposition applies on this single domain for **every** -1<sigma<1 and **every** nonnegative L^2 load. This concretely demonstrates that the original regularity assumption is not necessary, while keeping the original energy, forcing class and parameter interval.

## 5. A separately quantified nonconvex consequence

Let Omega be any fixed bounded C^2 planar domain, without assuming convexity, and let K=norm(kappa)_infinity. Choose a finite eta>0 with

    -eta>delta_c(Omega),    eta<delta_1(Omega).

Such an eta exists, also when delta_c=-infinity. Set

    epsilon=min{1, eta/(1+K)}.

For **1-epsilon<sigma<1**, the coefficient alpha=(1-sigma)*kappa satisfies

    delta_c < -eta < alpha < eta < delta_1

pointwise, with the evident harmless replacement of the middle strict bounds by the stronger estimate |alpha|<eta. Gazzola–Sweers Theorem 2.3, or Theorem 4.1 with weight beta=1, gives positivity for every nonzero nonnegative f in L^2. Identity (1), valid in this smoother setting as well, identifies its weak solution with the unique minimizer of the actual plate energy.

For example, the annulus 1<|x|<2 is connected, smooth and nonconvex. Its signed curvatures are 1/2 on the outer circle and -1 on the inner circle. The conclusion applies to this domain for some epsilon>0. It is a genuine curvature-dependent hinged-plate statement: the inner coefficient is negative, and sigma is strictly below the Navier value 1.

This is a direct consequence of a credited published theorem. **The threshold is domain-dependent and is not computed here.** It does not prove positivity on the annulus for all -1<sigma<1, for a prescribed arbitrary sigma, or throughout the physical interval -1<sigma<1/2. In particular, it does not give a sigma-uniform replacement for convexity in the original theorem.

## 6. Exact remaining gap

The literal question of whether the C^{2,1} assumption can be weakened has a known affirmative answer. A claim that no weaker general result exists is outdated. Nevertheless, the broad optimal-domain request still contains distinctions not settled by this package:

- no necessary-and-sufficient geometric criterion is given for a prescribed arbitrary sigma;
- no general nonconvex domain class is proved positive uniformly for the entire interval -1<sigma<1;
- C^{1,1} is a sufficient regularity class, not a proved minimal one;
- arbitrary Lipschitz domains, especially reentrant corners, require the correct variational operator and cannot be handled merely by decoupling Navier equations;
- positivity of nonlinear least-energy states is not positivity of the linear inverse for every nonnegative load.

Accordingly the overall record is retained conservatively as **unsolved**, with two credited and carefully quantified improvements. No new-discovery or human-peer-review claim is made. The checker verifies local algebra, the geometric regularity distinction and the parameter inequalities only; it is not a numerical positivity test for an unknown Green function.
