# Independent mathematical audit: compact-domain Barenblatt theorem

## Verdict and exact scope

**ACCEPTED as a partial convergence theorem, with no mathematical correction required.** The proof establishes the claimed estimate for the original Gallouët–Mérigot–Natale frozen-proximal particle scheme, for each fixed dimension d≥1 and exponent m>1, on a fixed positive-time interval, when the Barenblatt support has positive clearance from the physical wall. It also proves the stated reconstructed-density and material-velocity conclusions.

This is not acceptance of a solution for arbitrary irregular weak solutions, Dirac initial data at time zero, support/wall contact, all time-step regimes, or Euler dynamics. It makes no assertion of literature priority. The unrecovered historical Approach 1 is not a proof premise or an audited artifact.

The complete file audited was `APPROACH_02_COMPACT_DOMAIN.md`, 14,564 bytes, SHA-256:

`0ae49bf12019ed74fcaf614caa3c2fc14807a8d05ab7286703ac2005799832c1`

An exact private audit snapshot is `FROZEN_APPROACH_02.md`. The author confirmed this freeze. The audit did not change the author file. All equation references below are to that frozen candidate unless explicitly marked GMN.

## Source and scheme identification

The [OWR report](https://ems.press/content/serial-article-files/46885), DOI [10.4171/OWR/2021/10](https://doi.org/10.4171/OWR/2021/10), printed pp. 519–522, describes the compact-domain Lagrangian regularization and frozen dynamics. Printed p. 522 asks about less regular solutions, including Barenblatt free boundaries. That page was checked in extracted text and in a locally rendered image.

The exact [GMN v2 PDF](https://arxiv.org/pdf/2105.12605v2) was inspected independently through the public primary source. Section 1.1 defines H=L²(ρ₀;Rᵈ); pp. 3–5 define the energy on all H, the particle subspace, minimization (1.17), and frozen gradient evolution (1.21). Section 4, printed p. 13, explicitly discusses particles outside M. Theorem 1.2 on printed p. 7 requires smooth velocity; §6 on printed pp. 25–26 excludes its nonsmooth numerical examples from those theorems. No convex-domain constraint is imposed on the scheme. The candidate changes the admissible reference solution, not the particle algorithm.

[Natale v2](https://arxiv.org/html/2304.05069v2), revised March 2025, uses a different interacting-cell energy; §1.4 distinguishes that energy from the density Moreau–Yosida energy used here. Its §4.2.1 also excludes its Barenblatt example from its theorem. It is not a substitute convergence theorem for this audit. [arXiv:2106.08084](https://arxiv.org/abs/2106.08084) is a different paper about domain decomposition for optimal transport.

Public web PDF screenshot attempts returned cache errors. This did not block text inspection of the GMN v2 PDF. Subsequently the exact-version downloaded GMN PDF was locally rendered at printed pp. 5 and 13 and visually inspected; the OWR PDF was likewise rendered at printed p. 522. The locally checked PDF hashes are recorded in the audit manifest. Those access details do not supply a missing mathematical premise.

## 1. Correct reference solution and pressure extension

Let c=(m−1)/m and α=1/(m−1). With β=1/(d(m−1)+2) and λ=dβ(m−1), one has λ+2β=1. The candidate's q₀ has

- ∇q₀=−βx/t and div(−∇q₀)=dβ/t;
- q₀,t=−λAt^(−λ−1)+β|x|²/(2t²);
- support radius R(t)²=2At^(1−λ)/β=2At^(2β)/β.

Consequently q₀,t−|∇q₀|²+(m−1)q₀ div(−∇q₀)=0 by cancellation of the constant and |x|² coefficients. Also ρ(t,X(t,a))=(t/t₀)^(−dβ)ρ₀(a), so X(t,a)=(t/t₀)^βa pushes forward ρ₀ to ρ(t). This directly proves continuity of the transported mass, without differentiating a possibly non-C¹ density across the interface. In the positive region, ρ∇q₀=∇ρᵐ. The same identity extends distributionally across the free boundary because ρᵐ is a positive power p=m/(m−1)>1 of q₀,+ and its gradient has zero trace there. Thus this is indeed the no-flux porous-medium solution on the stated domain.

Choose the radii and smooth cutoff once for the fixed reference solution and clearance; κ can, for example, be fixed to 1. Because R₁>R(T), q₀ has a uniformly negative upper bound on the cutoff annulus. A convex combination of q₀ and −κ remains uniformly negative there. On the inner ball q=q₀; outside the outer ball q=−κ. It follows that:

1. q₊=q₀,+ exactly, and u=−∇q has compact support strictly inside Ω.
2. The derivatives needed by the proof are bounded globally, including at particle locations outside M.
3. The residual R vanishes on the inner ball and outside the outer ball, while |R|≤C(−q) on the remaining annulus.

The sign of q in the vacuum is essential. No pressure trace for a reconstructed density on the physical wall has been imposed.

## 2. Proximal minimizers exist, without uniqueness or convexity of Ω

For X constant on a finite measurable partition with positive masses wᵢ, every finite-energy map Y produces submeasures Y#(ρ₀1_{Pᵢ}). Each is dominated by Y#ρ₀=r dx, so it has an Lᵐ density rᵢ, 0≤rᵢ≤r. The transport term splits into the stated cellwise costs, and r=Σrᵢ.

Conversely, normalize each atomless source restriction and each target rᵢdx by wᵢ. These are probability measures on standard Euclidean measurable spaces, and a measurable transport map exists from the absolutely continuous source to the target. Equivalently, one may use quadratic optimal transport between the two bounded, absolutely continuous measures. Combining these finitely many maps realizes precisely the candidate's objective, and the resulting map is in H because the target is bounded.

The uniform subdensities give a finite feasible point. Bounded objective implies an Lᵐ bound for Σrᵢ and hence every rᵢ. Since 1<m<∞, the finite product is reflexive. Nonnegativity and the mass constraints are weakly closed; the bounded cost functions belong to L^{m/(m−1)}(Ω); and the convex internal-energy functional is weakly lower semicontinuous. A minimizer exists and is realized by a map. Boundary-supported singular mass is excluded by finite energy, and ∂Ω has zero Lebesgue measure for a Lipschitz domain.

This argument needs neither an optimal Lagrangian map unique in H nor distinct particle locations. It works for every proximal choice used by the theorem.

## 3. The proximal first variation has the correct sign and is admissible

For v smooth with compact support in Ω, T_s=Id+sv is a global diffeomorphism for sufficiently small |s|. It preserves Ω because it fixes a neighborhood of the boundary; both signs are allowed. Thus T_s∘Y is a legitimate competitor for any minimizer Y, even if its density reaches the physical wall.

Writing J_s=det(I+sDv), the transformed internal energy is

F(T_s∘Y)=∫ r(y)ᵐ J_s(y)^(1−m)/(m−1) dy.

Its derivative at zero is −∫rᵐ div v. The derivative of the squared Hilbert cost is ε^(−1)〈Y−X_n,v(Y)〉. Both differentiations are justified by an Lᵐ majorant and uniform Jacobian control. Their sum vanishes. This proves exactly (3.2), including its sign. No integration by parts on Ω and no unproved boundary cancellation is being used.

## 4. The reference pressure integral identities hold for every m>1

Let P(t)=∫ρᵐ. The convex-dual function

F*(q)=(c q₊)^{m/(m−1)}

has derivative (F*)'(q)=(c q₊)^α=ρ, including at q=0. Hence P'=∫ρq_t by differentiation of a C¹ scalar function and dominated convergence. The reference scaling gives P(t)=P(t₀)(t/t₀)^(−λ), so

P'=−λP/t=−(m−1)∫ρᵐ div u.

Both identities in (4.5) are therefore valid; they do not rely on a smooth physical pressure q₊ across the interface.

## 5. Signed energy is coercive in precisely the needed quantities

For U(r)=rᵐ/(m−1), the convex conjugate over r≥0 is F*(q)=ρᵐ. Thus e=U(r)−qr+ρᵐ≥0 for every real q. On {q<0}, e=U(r)+(−q)r≥(−q)r. Therefore the residual integral is bounded by C_R E, for every reconstructed density, with no lower density bound.

The exact decomposition Z=A+E+∫(q(Y)−q(X)) and the global Lipschitz bound Q yield

|∫(q(Y)−q(X))|≤Q||Y−X||≤A/2+εQ².

Consequently W=Z+(Q²+1)ε≥A/2+E+ε≥0, and A+E≤2W. This verifies (5.4) and all subsequent uses of coercivity. In particular Z itself need not be positive; the proof correctly uses W.

## 6. Frozen energy dissipation and node resets

Because X,V belong to H_N and Π_N is orthogonal,

A'=ε^(−1)〈X−Y,V〉=ε^(−1)〈X−Π_NY,V〉=−||V||².

The internal energy F(Y) is fixed inside a time step. At its right endpoint the newly minimized energy is no greater than the old frozen competitor, so

∫_{t_n}^{t_{n+1}}||V||²≤f_n−f_{n+1}=Δ_n,

and ΣΔ_n≤f₀ because all f_n≥0. The term −∫q(t,X)+P(t) is continuous at a reset, so Z and W have nonpositive jumps. A finite time partition is understood, as in the original scheme; a last shorter step is harmless. Endpoint f values can be defined by the proximal infimum even when no next dynamical interval is needed.

## 7. Differential identity and the exact vacuum cancellation

Differentiating Z inside one step gives

Z'=−||V||²+〈u(X),V〉−∫q_t(X)+P'.

Adding D=||V−u(X)||² proves (6.1). Since u(X) is constant on each source cell, projection can be removed in its pairing with Π_NY. Splitting X−Y against u(X)−u(Y), and then splitting X−Y=(X_n−Y)+(X−X_n), gives (6.2)–(6.3) exactly. The first split is controlled by 2LA; the second is precisely the frozen-step error. The proximal identity applies to v=u(t,·) by the established interior support.

With g=|u|²−q_t, bounded ∇g gives

|∫g(X)−g(Y)|≤G||X−Y||≤A+εG²/2.

Finally the residual relation is g=(m−1)q div u−R. Therefore

−∫rᵐ div u+∫rg+P'
=−(m−1)∫[U(r)−qr+ρᵐ] div u−∫rR.

This is (6.5), with no error term missing. Although div u can have either sign, its bounded absolute value controls the energy term. The residual is controlled by E. In particular the proof never replaces q by q₊ in a global Lipschitz estimate.

## 8. Frozen-step error, summation, and Grönwall

For any t in its step,

|ε^(−1)〈X(t)−X_n,u(t,Y)〉|
≤(2ε)^(−1)∫_{t_n}^t[||V(s)||²+||u(t,Y)||²] ds
≤(Δ_n+τ||u||_∞²)/(2ε).

This is an ordinary Hilbert-space Young inequality and uses mass one. In particular it does not assume that u(t,Y)=u(s,Y) or that the proximal map is updated continuously. Integrating the bound over a step of length h_n≤τ gives h_nΔ_n/(2ε)+h_nτ||u||_∞²/(2ε). Summation bounds these by

τf₀/(2ε)+(T−t₀)τ||u||_∞²/(2ε).

Thus the forcing has the claimed O((τ/ε)(1+f₀)) size. Applying an integrating factor on each interval and including the nonpositive jumps yields

sup W+∫D≤C[W₀+ε+(τ/ε)(1+f₀)].

The unweighted ∫D is controlled because the integrating factor is bounded above and below on the fixed interval. There is no hidden factor equal to the number of steps.

## 9. Initialization and final estimates

The competitor Id gives f₀≤δ_N²/(2ε)+F(Id). At t₀ the identity U(ρ₀)−qρ₀+ρ₀ᵐ=0 eliminates the reference energy. Taylor expansion of q around each barycenter xᵢ gives

∫_{Pᵢ}[q(a)−q(xᵢ)]ρ₀(a) da
=∫_{Pᵢ}O(|a−xᵢ|²)ρ₀(a) da,

because ∫_{Pᵢ}(a−xᵢ)ρ₀=0. The global Hessian bound makes the implied constant independent of the partition and N. Hence W₀≤δ_N²/(2ε)+Cδ_N²+Cε. Substituting f₀ and W₀ gives exactly (7.3); ε≤1 and τ≤ε reduce it to C(δ_N²/ε+ε+τ/ε).

For B=X_N−X_exact, split V−dot X_exact into V−u(X_N) and u(X_N)−u(X_exact). Young's inequality and the global Lipschitz constant give

(||B||²)'≤D+(1+2L)||B||².

Its initial value is δ_N². Grönwall proves the flow part of (2.4). The squared velocity difference is bounded by 2D+2L²||B||², giving its time-integrated material-velocity part.

The common-label coupling gives W₂(r_n,ρ(t))≤||Y_n−X_N(t)||+||X_N(t)−X_exact(t)||. Its first squared term equals 2εA≤4εW; its second is already controlled. Also E≤2W. Thus uniform-in-time density and signed-relative-energy convergence follow under the three stated scale limits. They apply on the right-continuous reconstruction intervals; at the terminal endpoint either the left reconstruction or a fresh minimizer obeys the corresponding bound.

## 10. Diagnostics, limitations, and patch disposition

The author's diagnostic program was read and rerun: 669 finite/symbolic consistency checks passed; the four supplied sign/vacuum/scaling mutations each failed their intended check. These are useful smoke tests only. The continuum argument above, including compactness, admissibility, interface regularity, node summation, and all m>1, was checked mathematically rather than inferred from finite tests.

No proof patch is needed. Two harmless conventions may be made explicit in a later exposition: use an ordinary finite mesh including the last endpoint; and fix κ and the cutoff as functions of the fixed reference data before naming the constant C. Neither changes the theorem or repairs a failed inference. Any whole-space theorem, wall-contact theorem, or claim for arbitrary weak solutions requires a separate proof and separate audit.
