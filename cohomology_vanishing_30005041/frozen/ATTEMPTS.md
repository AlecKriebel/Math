# Five substantive proof attempts

**Verdict: original problem UNSOLVED.** These five routes include proved special cases, exact obstructions to tempting arguments, and an explicit remaining mathematical gap. They are not five claims of resolution.

Throughout, use real functions, a standard sigma-finite measure space, and

`pi_p(g)f = epsilon_g J_g^(1/p) (f o T_g^(-1))`,

where `J_g=d((T_g)_*mu)/dmu`. Write `delta_p f(g)=pi_p(g)f-f`. For discrete groups, no continuity issue arises in identifying algebraic and continuous cocycles. The original question includes more general groups.

## Attempt 1. Transport by the Mazur map

### Proposed mechanism

The equivariant map `M_{p,q}(f)=sgn(f)|f|^(p/q)` transports the linear actions. Could it transport a nonzero cohomology class from an intermediate exponent to a forbidden endpoint?

### Exact failure on cocycles

Take one point with unit measure, `G=Z`, trivial representation, and `b(n)=n`. With p=1,q=2, the image has `M(b(1))=1`, but `M(b(4))=2`, whereas any cocycle with value1 at the generator has value4 at4. Thus applying M to cocycle values does not even preserve the cocycle equation. The nonlinear equivariance relation is not a cochain map.

### A rigorous all-positive-exponent special case

**Proposition1.** Let G be countable discrete and `0<p<q<infinity`. Assume the only measurable pi_q-invariant function is0. If formal first cohomology vanishes at q, it vanishes at p.

**Proof.** Let `b=delta_p f` be an Lp-valued cocycle for measurable f. For `alpha=p/q in(0,1)`, the real signed power satisfies

`|sgn(x)|x|^alpha-sgn(y)|y|^alpha| <= 2^(1-alpha)|x-y|^alpha`.

For equal signs this follows from concavity; for opposite signs it follows from `u^alpha+v^alpha <= 2^(1-alpha)(u+v)^alpha`. Equivariance therefore gives `delta_q(M f)(g) in Lq` for every g. By vanishing of formal cohomology there is h in Lq with `delta_q(M f)=delta_q h`. Hence `M f-h` is measurable invariant and must be0. Therefore `M f in Lq`, so f in Lp and b is an Lp coboundary. QED.

This also shows that the invariant-vector hypothesis is independent of the chosen positive exponent: the appropriate Mazur maps biject the measurable invariant spaces.

### Why the full route stops

A genuine cocycle need not be a formal coboundary. On the same one-point trivial Z-action, all formal coboundaries are zero, while `b(n)=n` represents a nonzero ordinary class at every p. Proposition1 and the published broader formal theorem cannot suppress this obstruction.

## Attempt 2. Same-space endpoint interpolation and a density obstruction

### Finite invariant measure gives a rigorous interval argument

**Proposition2.** Suppose the measure class admits an equivalent finite invariant measure. Then the fixed-family vanishing set intersected with `[1,infinity)` is an interval.

**Proof.** Changing to an equivalent measure conjugates each pi_p by the usual density multiplier and does not change its cohomology. Normalize the invariant measure to a probability. Then all pi_p have the same formula, including the sign cocycle, and `L^b -> L^a` is a continuous equivariant inclusion for a<b.

Let `1<=a<b<c`, and assume ordinary H1 vanishes at a and c. Any Lb cocycle is an La cocycle, so it is `delta f` for some f in La. It is consequently a formal coboundary at b. Ordinary vanishing at c implies formal vanishing there; Marrakchi–de la Salle Theorem5.4 implies formal vanishing at b. Thus the original cocycle is a coboundary in Lb. QED.

This is a consequence of the cited known theorem, not an asserted new resolution. No ergodicity is needed for this deduction. The proof's formal-theorem step is kept in its published range b>=1.

### Can a density multiplier restore the same proof in general?

**Proposition3.** Fix `0<p<q<infinity`, `t=1/p-1/q`, and `r=1/t`. A strictly positive finite-a.e. multiplication map `Tf=a f` is a bounded intertwiner `Lq(mu)->Lp(mu)` for the same Lamperti family if and only if

`w=a^r` is integrable, strictly positive a.e., and the measure `w mu` is G-invariant.

Its operator norm is `||a||_r=(integral w)^(1/r)`.

**Proof of boundedness criterion.** Holder's inequality, with exponents r/p and q/p, proves sufficiency even if p<1. Conversely, restrict to increasing finite-measure sets on which a is bounded above and below. On each such set A test with `f=1_A a^(r/q)`. Because `p(1+r/q)=r`, the norm ratio is `(integral_A a^r)^(1/r)`. Boundedness and monotone convergence imply `a in Lr`, and give the asserted exact norm.

**Proof of intertwining criterion.** Cancelling the common sign cocycle in `T pi_q(g)=pi_p(g) T` gives

`a(x) J_g(x)^(1/q) = J_g(x)^(1/p) a(T_g^(-1)x)`,

or `a/(a o T_g^(-1))=J_g^t`. Raising to r gives

`w=J_g (w o T_g^(-1))`,

which is exactly invariance of the density measure w mu. The reverse implication follows by the same calculation. QED.

Consequently this *specific class of bounded injective multiplication intertwiners* exists exactly when the class admits a finite invariant measure. It does not exclude more complicated linear or nonlinear maps.

### Exact two-atom control

Let masses be1 and4 and let g swap the atoms. Then

`pi_1(g)=[[0,4],[1/4,0]]`, and `pi_2(g)=[[0,2],[1/2,0]]`.

The identity inclusion is not equivariant. Multiplication by `diag(1,1/2)` does intertwine L2 with L1; its squared density is `(1,1/4)`, giving invariant atom masses `(1,1)`. This matches Proposition3 exactly.

### Remaining gap

Absent an equivalent finite invariant measure, neither the raw inclusion nor an everywhere-positive bounded multiplier supplies the endpoint cochain map used above. The proposition diagnoses the obstruction; it does not show there are no other methods.

## Attempt 3. Search for holes in signed atomic cyclic actions

Here every hypothesis and every positive exponent can be handled explicitly.

**Theorem4.** Let G=Z act by a fixed signed permutation Lamperti family on a countable atomic sigma-finite space. Then its cohomology-vanishing set is all `(0,infinity)` precisely when:

1. Every permutation orbit is finite;
2. The product of the signs around each orbit is -1;
3. The orbit lengths are uniformly bounded.

In all other cases its vanishing set is empty. The zero space satisfies the conditions vacuously.

**Proof.** Every atom has positive finite mass m_i. The isometry `f_i -> m_i^(1/p) f_i` conjugates the action to the same signed permutation U on counting-measure lp, for every p. A Z-cocycle is uniquely specified by its value v at1. Thus

`H^1(Z,U)=lp/(U-I)lp`.

Signs can be removed along each orbit except one edge of a finite cycle; its remaining sign is the cycle sign.

**Positive finite cycle.** On that cycle U is conjugate to the ordinary cyclic shift. Summing coordinates annihilates `(I-U)x`, while it does not annihilate a coordinate vector. Hence H1 is nonzero, and extension by zero to the other orbits preserves this obstruction.

**Infinite orbit.** After removing signs U is the bilateral shift. Solving `(I-U)x=delta_0` forces x to be constant on each of the two tails, with those constants differing by1. At least one nonzero constant tail remains, so x is not in lp for any finite positive p. Again H1 is nonzero globally.

**Negative finite cycle of length n.** Now `U^n=-I`, so

`(I-U)^(-1)=(1/2)(I+U+...+U^(n-1))`.

For p>=1 its norm is at most n/2. For0<p<=1, the pth power of the output quasi-norm is at most `n/2^p` times the pth power of the input quasi-norm. If all lengths are at most N these estimates sum over the disjoint blocks and give a bounded global inverse.

**Unbounded negative-cycle lengths.** Choose distinct cycles with lengths `n_k>=2^k`, k>=1. In the gauged coordinates let u_k have the constant value `n_k^(-1/p)` on the kth selected cycle. Then `||u_k||_p^p=1`, while `(I-U)u_k` has exactly one nonzero coordinate, of absolute value `2 n_k^(-1/p)`. Define v blockwise by these differences and zero elsewhere. We have

`||v||_p^p=2^p sum_k (1/n_k)<infinity`.

Any global solution of `(I-U)x=v` must agree with u_k on every selected cycle, because that finite negative block is invertible. Thus its pth-power quasi-norm is at least `sum_k1=infinity`. So H1 is nonzero. QED.

### Consequence for the counterexample search

This entire class has no interval holes, even below p=1. Changing atomic weights cannot introduce any p-dependence because the normalization removes them. Searching larger finite signed permutations cannot reach the diffuse nonsingular obstruction in the original question.

## Attempt 4. Assemble a hole from infinitely many cohomologically trivial blocks

Finite-dimensional tests alone miss uniform primitive estimates. This was a plausible way to make an intermediate exponent fail, so it needs a separate analysis.

**Proposition5.** Let G be finitely generated discrete, fix a finite generating set S, fix `1<=p<infinity`, and let `E=(direct_sum E_i)_p` be a countable lp-sum of Banach representations by isometries. Suppose `H^1(G,E_i)=0` for every i. Define C_i as the norm of the inverse coboundary map

`E_i/E_i^G -> Z^1(G,E_i)`,

where the cocycle norm is `(sum_{s in S} ||b(s)||^p)^(1/p)`. Then `H^1(G,E)=0` if and only if `sup_i C_i<infinity`.

**Proof.** The cocycles form a closed subspace of `E_i^S`: the relations are closed linear conditions, and values on generators determine all values. Thus this is a Banach space. The quotient by invariant vectors is also Banach. Vanishing H1 makes the coboundary map a bounded bijection, so its inverse is bounded by the open mapping theorem.

If the constants are uniformly bounded, decompose a global cocycle into its coordinate cocycles b_i. The sum of their generator-norm pth powers is finite. Choose a primitive f_i with norm at most twice the uniform bound times that generator norm; if b_i=0, choose f_i=0. The f_i have summable pth-power norms, so form a global primitive.

Conversely, if global H1 vanishes, the same open mapping theorem supplies a global primitive estimate C. A cocycle supported in one component has a global primitive with quotient distance at most C times its generator norm. Projecting a primitive and an invariant vector to that component gives its quotient estimate with the same constant. Hence C_i<=C for every i. QED.

### Explicit failure of naive componentwise reasoning

Take the negative cycles of lengths `2^k` from Theorem4. Each block has zero H1 at every p. Their disjoint union has nonzero H1 at every p. The constant block vector gives a primitive-to-coboundary ratio `n^(1/p)/2`, diverging with n.

Thus one cannot conclude that the vanishing set of an infinite direct sum is merely the intersection of the component vanishing sets. Uniform estimates matter. However this construction still gives an empty vanishing set, so it does not create the required interval hole. Establishing p-dependent uniform estimates in a genuine diffuse nonsingular construction remains open here.

## Attempt 5. Isolate the genuinely nonformal obstruction

### An exact algebraic reduction

For a countable discrete G set `V_p=L^p(X,mu)`, `W_p=L^0(X,mu)` with the **p-dependent** Lamperti action, and `Q_p=W_p/V_p` as an algebraic G-module. Then

`H^1_sharp(G,V_p) = Q_p^G / image(W_p^G)`.

Indeed, an invariant coset `[f]` is exactly a measurable f with `delta_p f(g) in Lp` for every g. Sending `[f]` to the class of this cocycle is well-defined modulo Lp and maps onto the formal classes. Its kernel consists exactly of cosets representable by invariant measurable functions. This proves the displayed identification directly, without topological quotient assumptions.

The inclusion `V_p -> W_p` induces a map on H1, whose kernel is precisely this formal subspace. Consequently

`H^1(G,V_p)/H^1_sharp(G,V_p)`

injects into `H^1(G,W_p)`.

### Necessary condition for a hole

Suppose `1<=a<b<c`, ordinary H1 vanishes at a and c, but not at b. The known formal theorem applied from c to b forces `H^1_sharp(G,V_b)=0`. Hence every nonzero b-class has a nonzero measurable-cohomology image. A hole cannot be witnessed solely by a measurable primitive with a bad Lb tail. The upper endpoint already rules such formal classes out.

The lower endpoint a does not automatically kill that measurable image: the actions on W_a and W_b differ by their Radon–Nikodym powers. The Mazur map intertwines them only nonlinearly and fails to preserve cocycles (Attempt1). Bounded positive multiplier maps that could connect the Lp cohomologies require a finite invariant density (Attempt2).

### Why the global-action theorem cannot close the gap

The Maharam and additive skew-product constructions in Marrakchi–de la Salle enlarge the measure space and change the linear representation. They prove existence statements about *some* action at a new exponent. The present question fixes sigma before all exponents are considered. Applying that theorem does not produce a cocycle for `pi_{b,sigma}` or `pi_{c,sigma}` as required.

### Frozen outcome

No cocycle with the required two vanishing endpoints was constructed, and no transport argument eliminates all genuinely nonformal intermediate classes. The full interval question, including its p<1 part, remains unresolved in this work. The preceding propositions are scoped reductions and controls, not a full solution.
