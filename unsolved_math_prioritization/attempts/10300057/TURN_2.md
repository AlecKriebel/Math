# Author turn 2: regular covers and controlled equivariant descent

**Partial theorem and route obstruction; original Question13.4 unresolved.** This turn removes the nonregular-cover bookkeeping and establishes a sufficient quantitative condition under which upstairs isotopies do descend. The quantitative hypothesis is not inferred from the source's endpoint plane-field convergence.

## 1. Reduction to a finite regular cover

Assume M and the chosen cover N are connected, and let p:N to M have degree d. Write H for its subgroup of pi_1(M), after choices of basepoints. The core K=intersection_(g in pi_1(M)) g H g^(-1) is normal of finite index at most d!, because it is the kernel of the action on the d cosets. Let q:Q to N be the corresponding further cover. Then p q:Q to M is a finite regular cover.

Every isotopy h_t:N to N starting at the identity lifts uniquely to an isotopy h_tilde_t:Q to Q starting at the identity: apply homotopy lifting to the maps h_t q. Its inverse is the corresponding lifted inverse isotopy, so every lifted map is a diffeomorphism in the smooth category (or a homeomorphism in the topological category). Naturality gives

h_tilde_1(q*G_N)=q*(h_1 G_N).

Pullback by the fixed finite covering preserves local plane-field convergence, and on compact manifolds preserves uniform convergence. Thus any example in the original question can also be witnessed in a regular finite cover. This validates the step that TURN_1 explicitly left to be checked; it does not make the lifted isotopies commute with the full new deck group.

## 2. A controlled descent theorem

Let M be a closed smooth manifold, p:N to M a finite regular smooth cover, and D its deck group. Give N a D-invariant metric. Let F,G be foliations with continuous tangent distributions, and let h_(n,t), 0<=t<=1, be smooth isotopies of N starting at the identity. Write V_(n,t) for their time-dependent generating vector fields. Define

W_(n,t) = (1/|D|) sum_(delta in D) delta_* V_(n,t).

Assume there is a fixed finite L such that

integral_0^1 ||V_(n,t)||_(C2) dt <= L

for all n, and assume

e_n = integral_0^1 ||V_(n,t)-W_(n,t)||_(C1) dt tends to zero.   (1)

If h_(n,1)(p*G) converges uniformly as plane fields to p*F, then there are isotopies kbar_(n,t) of M, starting at the identity, whose endpoints send G to foliations converging uniformly to F.

### Proof

Deck averaging gives D-invariant vector fields W. Their time integrals of C2 norms have the same uniform bound, up to a fixed norm-equivalence constant; using covariant derivatives for a D-invariant metric removes even that deck-dependent issue. Let k_(n,t) be their flows. Compactness gives global flows, and uniqueness of the ODE implies that every k_(n,t) commutes with D. These entire isotopies descend to M.

We check that their endpoint plane fields have the same limit. Standard ODE estimates here require a spatial second-derivative bound, which is why the theorem assumes the integrated C2 bound. For completeness, embed the compact N in Euclidean space and use a fixed bounded linear extension of C2 tangent fields, obtained from a finite atlas and partition of unity, to a common compact neighborhood. Integral curves starting on N remain on N. Norms of the extended fields and their differences are controlled by fixed constants.

For the two position flows h and k, the integral equation and Gronwall give

sup_t ||h_(n,t)-k_(n,t)||_(C0) <= C e_n.

The derivative flows satisfy J'=DV(h)J and K'=DW(k)K. Subtracting them introduces DV(h)-DV(k), bounded by the C2 norm of V times the position difference, and DV(k)-DW(k), bounded by ||V-W||_(C1). A second Gronwall estimate, using the integrated uniform bounds, gives

sup_t ||h_(n,t)-k_(n,t)||_(C1) <= C' e_n.             (2)

The same variational equations bound first derivatives and inverse first derivatives uniformly. Differentiating once more gives J_2'=DV(h)J_2+D2V(h)[J,J], which bounds the second derivatives uniformly under the integrated C2 assumption. All constants depend on N and L, not on n.

Let xi be the continuous plane distribution of p*G. A pushforward at y is Dh(h^(-1)y) xi(h^(-1)y). Equations (2), the uniform inverse bounds and the uniform continuity of xi imply that the two pushforward distributions approach each other uniformly. More explicitly, the difference is bounded by a constant times e_n plus the modulus of continuity of xi evaluated at another constant times e_n. The uniform second-derivative bound controls the change of Dh when its inverse argument is changed. Uniform invertibility ensures that passage from spanning vectors to a Grassmannian plane does not lose control.

Therefore k_(n,1)(xi) has the same limit p*TF as h_(n,1)(xi). Since k_n commutes with D, its pushforward is the lift of kbar_n(TG). Convergence then descends through the finite covering. This proves the theorem.

The argument is about continuous tangent distributions and smooth controlled isotopies, not stronger convergence of leaves, holonomy charts or transverse derivatives. It does not assert these regularity and boundedness hypotheses for an arbitrary source sequence.

## 3. Why straightforward averaging does not close the gap

Averaging plane-field defining forms can destroy integrability even when all forms are arbitrarily close to one fixed integrable form. In coordinates x,y,z on a bounded region with z>0, let eta>0 and consider

alpha_1=dz-eta z^2 dx,        alpha_2=dz+eta dy.

Both define nonsingular foliations. The first is a nonzero multiple of d(z/(1+eta xz)) where the denominator is nonzero; the second is d(z+eta y). They are arbitrarily close to dz for small eta. But their average satisfies

((alpha_1+alpha_2)/2) wedge d((alpha_1+alpha_2)/2)
 = -(eta^2 z/2) dx wedge dy wedge dz,

which is nonzero. On two disjoint covering charts interchanged freely by a deck transformation, this is literally the local deck-average calculation. It is a local obstruction to a proposed averaging method, not a hyperbolic taut-foliation counterexample to the original question.

Averaging generating vector fields avoids this integrability problem because its flow carries a foliation to a foliation. Nevertheless, the source hypothesis controls only endpoint distributions, not the defect in (1). An arbitrary time-dependent loop of diffeomorphisms beginning and ending at the identity can be inserted into an isotopy without changing its endpoint distribution. Such loops may have large non-equivariant generators and large derivatives. Thus bounds on a chosen isotopy path do not follow merely from convergence of its endpoint distributions. This observation does not rule out finding better paths; that is precisely the missing step.

## 4. Outcome

Every candidate may be studied in a regular finite cover. If an upstairs approximating sequence admits the explicit uniformly C2-controlled, asymptotically deck-invariant generators above, it necessarily descends. A counterexample must escape this sufficient regime for every appropriate choice of paths; alternatively, a general proof would need to produce suitable equivariant approximations without assuming (1).

Two substantive author turns complete. No construction of the required taut foliations on a hyperbolic manifold, and no unconditional orbit-closure descent theorem, has been obtained. Next turn should test a concrete residual torsion or holonomy mechanism rather than infer endpoint-to-generator control. Completion estimate20%.
