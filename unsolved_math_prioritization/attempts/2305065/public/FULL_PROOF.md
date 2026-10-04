# Problem 2305065: an existing affirmative solution

**Status:** `already_solved`. **Verification budget:** 1/5.

This is a verification of prior mathematics, not a new solution. David A. Stegenga and Kenneth Stephenson proved a stronger result in 1985. The 2018 source also credits an earlier construction to A. A. Gol'dberg (1984). The latter article's proof is not independently verified here and is not needed for the conclusion below. This record was prepared with AI assistance; an independent audit is a separate requirement.

## 1. Exact question and notation

Let D = {z in C: |z| < 1}, T = {z: |z| = 1}, and let A(D) be the functions continuous on the closed disc and holomorphic in D. Equip A(D) with the uniform norm. The question is whether a **nonconstant** f in A(D) can satisfy

    f(exp(i theta)) in f(D) for Lebesgue-almost every theta in [0, 2 pi).

Set E(f) = {zeta in T: f(zeta) not in f(D)}. Let m be normalized angular Lebesgue measure on T. The exact success condition is f nonconstant and m(E(f)) = 0. There is no injectivity, finite-degree, smooth-boundary, or inner-function hypothesis.

## 2. Published theorem and complete implication

Stegenga–Stephenson [SS], Theorem 3.1, printed p. 231, states that, for each fixed Hausdorff gauge h, the functions in A(D) with zero h-Hausdorff measure exceptional set form a dense G-delta set. Their E_f, defined on printed p. 227, also includes boundary points where a nontangential limit fails to exist. For a disc-algebra function that extra set is empty, by continuity. Thus it is exactly E(f) here. Printed p. 228 explicitly connects the result with Problem 5.65.

Choose h(t) = t. Zero associated Hausdorff measure on T implies m(E(f)) = 0. For completeness, if a disc B(a,r), r < 1/2, meets T, choose zeta in that intersection. Its intersection with T lies in B(zeta,2r). The latter cuts an arc of angular length 4 arcsin(r), which is at most 2 pi r. Thus any disc cover with sum of radii tending to zero forces angular outer measure zero. The particular radius-versus-diameter normalization makes no difference.

Density supplies such an f in the open norm ball

    ||f - chi|| < 1/2, where chi(z) = z.

No constant c is in this ball: by the triangle inequality,

    2 = |1 - (-1)| <= |1-c| + |-1-c| <= 2 ||chi-c||,

so ||chi-c|| >= 1. Consequently the selected f is nonconstant. Continuity gives its boundary values at every point; m(E(f)) = 0 gives the required assertion for almost every theta. This answers the complete question affirmatively. QED.

## 3. A supplementary proof with an explicit published dependency

This section supplies an alternative, elementary Baire-category deduction of the Lebesgue-measure case. It avoids the depth-function formalism and records exactly the one non-elementary construction being imported. It is not a claim to a new theorem or a source-free proof.

### Published geometric input

A consequence of [SS], Lemma 3.2 and its proof on printed pp. 231–233, is:

> Given epsilon > 0 and eta > 0, there exists g in A(D) with g(D) = D, ||g-chi|| < epsilon, and m({zeta in T: |g(zeta)| = 1}) < eta.

Indeed choose an integer n with 4 pi/n < epsilon and then a sufficiently small positive zeta with n zeta < eta. The lemma gives the norm bound 4 pi/n and n closed boundary-contact arcs of normalized measure less than zeta each. Surjectivity is property (a). The at-most-two-to-one assertion is unnecessary here. This is an established external lemma, not an unproved new claim in this packet.

### Uniform persistence of interior coverage

Let f in A(D) be nonconstant, and let K be a compact subset of T such that f(zeta) lies in f(D) for every zeta in K. We prove there is delta > 0 such that every h in A(D) with ||h-f|| < delta satisfies h(zeta) in h(D) for all zeta in K.

For each zeta in K, choose a in D with f(a) = f(zeta). Zeros of f-f(zeta) are isolated, so choose a small circle C centered at a, together with its closed interior contained in D, on which f-f(zeta) never vanishes. Write

    b = min_{z in C} |f(z)-f(zeta)| > 0.

Continuity supplies a relative neighborhood V of zeta in T such that |f(xi)-f(zeta)| < b/4 for xi in V. If ||h-f|| < b/8, then on C and for xi in V,

    |(h(z)-h(xi)) - (f(z)-f(zeta))|
      <= |h(z)-f(z)| + |h(xi)-f(xi)| + |f(xi)-f(zeta)|
      < b/8 + b/8 + b/4 = b/2 < b.

Rouche's theorem shows h-h(xi) has as many zeros inside C as f-f(zeta), hence at least one. Thus h(xi) belongs to h(D). A finite collection of the V covers K. The minimum of the corresponding positive b/8 values is a uniform delta. This proves the assertion.

### An open dense family

Let X be the set of nonconstant functions in A(D). The constants form a closed subspace, so X is open. It is dense: a constant c is approximated by c + epsilon z. The disc algebra is a Banach space, since a uniform limit on the closed disc is continuous and is holomorphic in its interior. Therefore its open subspace X is a Baire space.

For each integer N >= 1, define

    U_N = {f in X: m(E(f)) < 1/N}.

We first show U_N is open in X. For nonconstant f, f(D) is open, so E(f) is closed in T and hence compact. If f in U_N, regularity of angular measure gives a relative open O containing E(f) with m(O) < 1/N. Apply the persistence assertion to K = T minus O. Every sufficiently small perturbation h of f covers h(K) from the interior, so E(h) is contained in O and m(E(h)) < 1/N. Also take the perturbation small enough to keep h in X. Thus U_N is open.

We next prove U_N is dense in X. Fix f in X and a desired norm tolerance tau > 0. Uniform continuity of f on the closed disc gives epsilon > 0 such that |f(z)-f(w)| < tau whenever |z-w| < epsilon. Apply the geometric input with this epsilon and eta = 1/N, and put F = f composed with g. Then F is in A(D), ||F-f|| < tau, and F(D) = f(g(D)) = f(D). In particular F is nonconstant.

If zeta in T has |g(zeta)| < 1, then

    F(zeta) = f(g(zeta)) in f(D) = F(D).

Hence E(F) is a subset of {zeta: |g(zeta)| = 1}, and m(E(F)) < 1/N. This proves density.

The Baire theorem now gives a dense intersection of all U_N in X. Any member has m(E(f)) < 1/N for every N, hence measure zero, and is nonconstant by definition. This independently completes the implication from the published geometric input to the exact problem. QED.

## 4. Checks that prevent incorrect shortcuts

- **Constants:** For a constant c, c belongs to c(D), so E(c) is empty. Nevertheless c + epsilon z has E = T for every epsilon != 0. Accordingly the measure-small sets are not open at constants. Section 3 works in X throughout. This addresses a suppressed nonconstant hypothesis in the source's openness presentation; it does not undermine existence or the corrected dense-set argument.
- **Surjectivity:** A map g(z) = r z, 0 < r < 1, has no unit-circle boundary contacts but has E(g) = T. Therefore small contact set alone is insufficient. The equality g(D) = D in the geometric input is essential to the composition step.
- **Almost every versus every:** No nonconstant f in A(D) can have E(f) empty. A point on T where |f| attains its positive maximum cannot share that value with any point of D, by the maximum modulus principle. A measure-zero exceptional set can be nonempty.
- **Univalence:** A univalent f in A(D) cannot satisfy the target. If f(zeta) were in f(D), continuity of the inverse on f(D), applied to f(r zeta) as r tends to 1, would force r zeta to approach a point in D, a contradiction.
- **Gauge quantifiers:** The published theorem fixes a gauge before choosing the residual set. Nothing here asserts a single function works simultaneously for every conceivable gauge.
- **No empirical proof:** The controls exercise strict inequalities and deliberately false simplifications. They do not construct g or f, evaluate an infinite exceptional set, or mechanically verify Rouche's theorem, uniformization, harmonic measure, or Baire's theorem.

## 5. Source and proof scope

[SS] D. A. Stegenga and K. Stephenson, *Generic covering properties for spaces of analytic functions*, Pacific Journal of Mathematics 119(1) (1985), 227–243. Primary publisher PDF: https://msp.org/pjm/1985/119-1/pjm-v119-n1-p12-s.pdf . Relevant proof: Sections 2–3, especially Theorem 3.1 and Lemma 3.2, pp. 229–234. The published construction uses a simply connected branched surface over D, thin attached neighborhoods of slits, harmonic-measure control, and rotational symmetry. The proof was read, and printed pp. 227, 231–234 were visually checked. The present record imports that geometric lemma and provides all remaining analytic deductions above. It does not independently reprove its uniformization and harmonic-measure dependencies.

[HL] W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)* (2018), Problem and Update 5.65, printed p. 109; bibliography [318], printed p. 222. https://arxiv.org/abs/1809.07200 . Update 5.65 already reports the affirmative answer. Its description of the Stegenga–Stephenson work as unpublished is superseded by [SS].

[G] A. A. Gol'dberg, *Analytic functions mapping a disk on a disk*, Izv. Vyssh. Uchebn. Zaved. Mat. (1984), no. 6, 24–25; English translation titled *On analytic functions mapping a disk onto a disk*, Soviet Math. (Iz. VUZ) 28:6 (1984), 29–30. Bibliography independently corroborated at https://www.mathnet.ru/rus/person18068 . Only metadata and [HL]'s attribution were checked; [G]'s proof is not a dependency.

**Remaining gap for the exact mathematical target:** none, as an application of the published theorem. **Remaining gap for a wholly source-free reconstruction:** the established geometric input is cited rather than fully rederived. **Novelty:** none claimed. The catalogue's prior open-triage assessment was wrong; this is a source-status correction.
