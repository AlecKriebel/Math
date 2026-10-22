# Kirby Problem 3 46 finite orbit restrictions and the remaining gap

## Outcome

The intended connected-manifold problem is not solved here. No counterexample on a connected non-lens space was obtained. Four approaches were examined. The useful mathematical output is a homology-relation obstruction for any finite orbit set, together with precise reasons that approximation, changing the ECH homology class, and finite covers do not remove the outstanding hypothesis.

The homology-relation result below is an authored deduction from established embedded contact homology (ECH) facts. It is not claimed to be new. Closely related rank arguments already appear in Cristofaro-Gardiner and Pomerleano's 2014 exposition [P]. This report does not establish progress beyond the known literature on the full conjecture.

## Exact scope and source check

K3 Problem 3.46, printed page 164, asks whether a contact form on a closed three-manifold outside the lens-space class must have infinitely many simple Reeb orbits [K]. We work in the smooth category, with the coorientation and orientation induced by the globally defined contact form. Simple orbits are geometrically distinct embedded periodic trajectories; iterates are not new simple orbits.

Two conventions matter:

- The lens-space convention includes S^3 and excludes S^1 x S^2. This is explicit in [T], footnote 1.
- K3's displayed question does not explicitly say connected. The intended connected formulation is supported by the connected hypotheses in [I], Theorem 1.1, and [S], Question 8.1. If disconnected manifolds are literally admitted, two disjoint irrational ellipsoids give four simple orbits on S^3 disjoint-union S^3, which is not a lens space. This is a wording caveat, not a resolution of the intended question.

The verified literature distinguishes these cases:

1. Every contact form on a closed connected three-manifold has at least two simple orbits [O], Theorem 1.1.
2. Exactly two force a lens space, without an initial nondegeneracy assumption [T], Corollary 1.3.
3. Nondegenerate contact forms have two or infinitely many orbits, without a restriction on c1 [B]. Nondegenerate here includes every iterate of every simple orbit.
4. With torsion c1, the same dichotomy holds without nondegeneracy [I], Theorem 1.1.

Thus a counterexample to the intended problem would have nontorsion c1, finitely many simple orbits numbering at least three, and at least one degenerate periodic orbit, possibly an iterate. The inspected K3 remarks, [I] Section 1.4, and [S] Question 8.1 retain the simultaneous-removal problem. Searches on 6 October 2026 found no verified unrestricted result. This is a bounded literature assessment, not a claim that no unindexed or later result exists.

## Approach 1 retaining orbit counts under approximation

A nondegenerate approximation on a non-lens space has infinitely many simple orbits by [B]. This alone does not transfer infinitude to its limit. It supplies neither uniform period bounds for enough distinct trajectories nor a condition preventing different approximating trajectories from converging to covers of the same orbit.

The failure of this inference is concrete, even for smooth convergence through nondegenerate forms. On S^3 in C^2 write z_j = r_j exp(i theta_j) and set

    lambda_(a,b) = (a r_1^2 d theta_1 + b r_2^2 d theta_2)/2,
    a > 0, b > 0, a/b irrational.

These expressions extend smoothly across the coordinate axes. The form is contact, for example by pulling the standard Liouville form back from the boundary of the ellipsoid with semiaxis squares a and b. Its Reeb vector field is

    R = (2/a) partial_(theta_1) + (2/b) partial_(theta_2).

Indeed lambda_(a,b)(R)=r_1^2+r_2^2=1 and contraction of d lambda_(a,b) with R vanishes on TS^3. A trajectory with both coordinates nonzero closes only if a/b is rational. Hence exactly the two coordinate circles are simple periodic orbits. Their transverse return rotations, and all iterates, are nonresonant because a/b is irrational.

Irie's residual-density theorem [D], Theorem 1.1, supplies conformal contact forms arbitrarily C-infinity close to this form with dense periodic trajectories. Intersect that residual set with the residual set of nondegenerate forms, recalled in [T], Section 1.1. The space of positive smooth conformal factors is a Baire space, so the intersection is dense. Choose a sequence in this intersection tending to 1. Every resulting form has infinitely many simple orbits: a finite union of embedded circles is closed and has empty interior, so cannot be dense in S^3. The limit has exactly two.

This example is on the excluded lens-space topology. It disproves the proposed general passage of orbit counts to a limit, not the target conjecture. Additional non-lens-space geometry would have to enter any successful approximation argument.

## Approach 2 changing the ECH homology class

One can choose Gamma in H_1(Y; Z) so that c1(xi) + 2 PD(Gamma) is torsion. The existence of such a Gamma and of an ECH U-sequence in that class are established in [O], proof of Corollary 2.2. This repairs the integer grading issue but does not repair control of the topological index J0.

Here is the exact obstruction. Let alpha and beta be orbit sets with common class Gamma. Fix trivializations over their orbits and a relative class Z in H_2(Y, alpha, beta). For A in H_2(Y; Z), the index identities [I], equations (2.2), (2.3), and (2.13), give

    c_tau(Z + kA) - c_tau(Z) = k <c1(xi), A>,
    I(Z + kA) - I(Z) = k <c1(xi) + 2 PD(Gamma), A>,
    J0(Z + kA) - J0(Z) = k <-c1(xi) + 2 PD(Gamma), A>.

The last equality follows directly from J0 = I - 2 c_tau - CZ_top(alpha) + CZ_top(beta); the last two terms depend only on the ends and cancel in the difference.

If c1(xi) + 2 PD(Gamma) is torsion, these specialize to

    I(Z + kA) = I(Z),
    J0(Z + kA) = J0(Z) - 2k <c1(xi), A>.

If c1(xi) is nontorsion, there is an integral A with nonzero pairing: the kernel of H^2(Y; Z) -> Hom(H_2(Y; Z), Z) is torsion. As k ranges over the integers, J0 is unbounded in both directions while the ends and the ECH index remain fixed. The formal d-lambda area also stays fixed, since the integral of the exact two-form d lambda over A vanishes.

This is a statement about relative homology classes. It does not assert that those classes are represented by holomorphic curves. In particular, it cannot refute an analytic bound on the actual U-curves. It proves that such a bound does not follow merely from the asymptotic orbit sets, their actions, and a fixed ECH index. A geometric estimate controlling the Chern contribution of actual curves remains missing. This agrees with the obstruction identified in [S], Question 8.1.

## Approach 3 finite covers

Passing to a finite cover cannot make a nontorsion first Chern class torsion. For a finite covering p: Y_tilde -> Y of degree d, transfer in rational cohomology satisfies

    transfer composed with p^* = d times identity.

Therefore p^*: H^2(Y; Q) -> H^2(Y_tilde; Q) is injective. Naturality gives c1(p^*xi)=p^*c1(xi), so its rational image stays nonzero. Equivalently, if p^*c1(xi) were torsion, transfer would make d c1(xi) torsion, contradicting the assumption. Thus the torsion-c1 dichotomy cannot be applied by that route. No assertion about infinite covers or a different contact structure is made.

## Approach 4 the period map on homology relations

### Proposition

Let lambda be any smooth contact form on a closed connected three-manifold Y. Suppose its simple Reeb orbits are precisely gamma_1 through gamma_m. Put a_i = integral_(gamma_i) lambda > 0 and define

    H: Z^m -> H_1(Y; Z),       H(n) = sum_i n_i [gamma_i],
    L = ker H,
    ell: L -> R,              ell(n) = sum_i n_i a_i.

Then ell(L) is nondiscrete, hence dense in R. In particular, if r is the dimension over Q of the span of the orbit homology classes in H_1(Y; Q), then

    m - r >= 2.

Moreover PD^(-1)c1(xi) lies in the rational span of these orbit classes. In particular, if c1(xi) is nontorsion then r >= 1. A hypothetical three-orbit counterexample must therefore have r=1.

### Proof

Choose Gamma with c1(xi)+2 PD(Gamma) torsion and a homogeneous U-sequence sigma_k in ECH(Y, xi, Gamma). Write c_k for its spectral numbers. The established input from [O], Corollary 2.2 and Lemma 3.1, is

    c_(k+1) > c_k,       and       c_k/k -> 0.

The strict inequality uses the assumption that there are only finitely many simple orbits. Spectrality can be retained in the fixed homology class: for each k there is n(k) in Z_(>=0)^m with

    H(n(k)) = Gamma,       c_k = sum_i n_i(k) a_i.

For completeness, the homology assertion in the degenerate case follows by approximating lambda in C-infinity by nondegenerate conformal forms and choosing spectral orbit sets. Their total actions are uniformly bounded for fixed k. Nearby nonvanishing vector fields on a compact manifold have a uniform positive lower bound on periods. Consequently there are uniformly finitely many orbit components and uniformly bounded covering multiplicities. Passing to subsequences gives limiting Reeb loops, each an iterate of one of the gamma_i. Nearby loops are freely homotopic, so their total integral homology remains Gamma. Actions converge as well. This is also stated explicitly in [P], Fact 2. No admissibility constraint on multiplicities is imposed on the limiting degenerate orbit set.

Fix n(1). For every k, n(k)-n(1) belongs to L, so

    c_k - c_1 belongs to ell(L).

If ell(L) were the zero group, strict increase would be impossible. If it were a nonzero discrete subgroup of R, it would be delta Z for some delta>0. The c_k would then be a strictly increasing sequence in c_1+delta Z, forcing

    c_k >= c_1 + (k-1) delta.

This contradicts c_k/k -> 0. Thus ell(L) is nondiscrete. Any nondiscrete additive subgroup of R is dense: it contains arbitrarily small positive h, and multiples of such h approximate any prescribed real number.

Since H_1(Y; Z) is finitely generated, rank L=m-r. A free abelian group of rank zero or one has cyclic image under any homomorphism to R, and every cyclic subgroup of R is discrete. Hence rank L>=2.

Finally, Gamma is represented by n(1), so its rational class lies in the orbit span. The torsion equation gives

    PD^(-1)c1(xi) = -2 Gamma in H_1(Y; Q),

which proves the last assertions. QED.

### What the proposition does not do

The inequality m>=r+2 is compatible with any finite m>=3 when the orbit homology span has small rank. Nondiscreteness of ell(L) also allows such configurations. The argument gives a necessary condition and no existence theorem for a flow realizing the abstract data. It supplies neither the missing geometric control in Approach 2 nor a contradiction for all possible finite orbit sets.

This proof reuses the established spectral mechanism of [O]. The related rank-zero/rank-one exclusions in [P] are prior art. Novelty of the general formulation has not been established and is not claimed.

## Stopping point

Four mathematical approaches were completed; none proves or refutes the connected problem. The deliverable is a rigorously delimited necessary-condition proof and an audit of tempting reductions. The remaining task is to rule out finite orbit configurations for degenerate forms with nontorsion c1. An unrestricted conclusion would require a new argument beyond the deductions established here.

## Public references

- [K] R. Inanc Baykur, Robion C. Kirby, and Daniel Ruberman, K3 A New Problem List in Low-Dimensional Topology, Problem 3.46, printed p. 164. [Author preliminary PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
- [O] Daniel Cristofaro-Gardiner and Michael Hutchings, From one Reeb orbit to two, especially Corollary 2.2 and Lemma 3.1. [arXiv:1202.4839v4](https://arxiv.org/abs/1202.4839v4).
- [T] Daniel Cristofaro-Gardiner, Umberto Hryniewicz, Michael Hutchings, and Hui Liu, Contact three-manifolds with exactly two simple Reeb orbits, especially Corollary 1.3 and footnote 1. [arXiv:2102.04970](https://arxiv.org/abs/2102.04970); [published article](https://doi.org/10.2140/gt.2023.27.3801).
- [B] Vincent Colin, Pierre Dehornoy, and Ana Rechtman, On the existence of supporting broken book decompositions for contact forms in dimension 3. [arXiv:2001.01448v4](https://arxiv.org/abs/2001.01448v4).
- [I] Dan Cristofaro-Gardiner, Umberto Hryniewicz, Michael Hutchings, and Hui Liu, Proof of Hofer-Wysocki-Zehnder's two or infinity conjecture. [arXiv:2310.07636v2](https://arxiv.org/abs/2310.07636v2); [published article DOI](https://doi.org/10.1090/jams/1072). Mathematical statements and equation numbers here were checked in the arXiv version.
- [S] Dan Cristofaro-Gardiner, Low-dimensional topology and symplectic dynamics, Section 8.1, Question 8.1. [arXiv:2510.07680v1](https://arxiv.org/abs/2510.07680v1).
- [D] Kei Irie, Dense existence of periodic Reeb orbits and ECH spectral invariants, Theorem 1.1. [arXiv:1508.07542v2](https://arxiv.org/abs/1508.07542v2).
- [P] Dan Cristofaro-Gardiner and Dan Pomerleano, A guest post by Dans C-G and P, 24 November 2014, especially Fact 2 and the homology-kernel arguments. [Authors' exposition](https://floerhomology.wordpress.com/2014/11/24/a-guest-post-by-dans-c-g-and-p/).
