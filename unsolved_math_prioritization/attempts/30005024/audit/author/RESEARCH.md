# Finite-mean coding for finitely dependent processes

Problem 30005024 / OWR-9790359-005. Research date: 2026-10-05.

## Disposition and exact target

**Unresolved after five substantive approaches.** No example with an intrinsic infinite-mean coding obstruction has been proved, and no universal finite-mean construction has been proved. The results below are scoped auxiliary results, including elementary reconstructions of known facts. No novelty, formal-verification, human-peer-review, or publication-acceptance claim is made.

The target asks for a translation-invariant finitely dependent process on a lattice that has no finitary IID representation with integrable spatial coding radius. The quantifier is over **every** permitted IID source and every coding of the specified law. One inefficient representation is insufficient.

The primary setting in Spinka's Oberwolfach contribution is Z^d, initially with countable state spaces, explicitly allowing more general spaces for the coding definition. The finite-dependence question has no source-entropy or finite-source-alphabet restriction. We work with the standard countable-output interpretation, allowing standard-Borel IID input; no claim is made about arbitrary nonstandard measurable spaces. The known general finitary theorem used here has countable output. Translation invariance suffices; reflection or full graph-automorphism equivariance is an additional property, not imposed by our target.

Use the lattice 1-norm. The process is k-dependent if the sigma-fields on any two sets at distance greater than k are independent. Pairwise independence alone does not suffice. For a coding F, its radius R is the least nonnegative integer for which the output at 0 is determined by input in the radius-R ball, using a consistent almost-sure determination convention. Finitary means R<infinity almost surely; finite mean means E[R]<infinity. A deterministic radius bound is stronger. In d dimensions, coding volume is comparable to (R+1)^d, so finite expected volume is not the same target when d>1.

For any standard-Borel IID source, coordinatewise sampling from Uniform[0,1] reduces it to a uniform IID source without enlarging the spatial radius. This does not automatically preserve a finite-bit stopping convention. Spatial radius counts sites, not bits or local entropy.

## Verified source position

The original question appears in Yinon Spinka's contribution, report pp.447–449, with the question on p.448: [official report](https://publications.mfo.de/bitstream/handle/mfo/3933/OWR_2022_08.pdf?isAllowed=y&sequence=4). The workshop took place in February 2022; the report volume is 2022 and the publisher lists publication in March 2023. The catalog's 2023 title and 2022 problem year therefore require this distinction. Its extracted original statement also includes unrelated following material; that material is not part of the target.

The report's bibliography entry [9] points to a subcritical-Ising paper, whereas the finite-dependence theorem and 1/r bound are verified directly in [Spinka, Finitely dependent processes are finitary](https://arxiv.org/abs/1901.00123), Theorem 1.1 and the introduction/Remark 3. This is a bibliographic mismatch, not a mathematical contradiction. That theorem gives a finitary coding for countable-valued finitely dependent invariant processes on transitive amenable graphs. For 1-dependent processes on Z its construction has P(R>r)<=8/r. This upper bound proves all moments of order less than1 are finite, but decides neither the first moment of that coding nor the existence of a better one.

Positive examples do not answer the existential obstruction problem. [Holroyd–Hutchcroft–Levy](https://arxiv.org/abs/1706.09526), Theorem 1, gives exponential-tail finitely dependent colorings with (k,q)=(1,5),(2,4),(3,3). Its critical (1,4),(2,3) cases remain conjectural obstructions in that paper. [Holroyd's symmetrization paper](https://arxiv.org/abs/2305.13980) constructs fully isometry-equivariant exponential-tail finitely dependent 4-colorings in every dimension, with no assertion that the dependence parameter is 1. [Timar's later paper](https://arxiv.org/abs/2402.17068) gives bounded-degree finitely dependent coloring constructions, not the universal integrability theorem or intrinsic counterexample needed here.

The searches also examined the current v2 of [Chazottes–Gallo–Takahashi](https://arxiv.org/abs/2602.14618). Its general concentration implication requires a second coding-volume moment; the first-moment implication has an additional structural hypothesis. It cannot be applied as a universal finite-mean-radius obstruction. A recent [quantum cycle-coloring lower bound](https://arxiv.org/abs/2608.11720) concerns exact probability-one finite-cycle algorithms and likewise supplies no such implication.

The literature search is bounded and dated, not proof of worldwide absence of a solution. No matching prior attempt was found by exact-ID, problem-number and phrase searches of this user's repository PRs, or in its main attempt-directory listing. Those checks do not exclude unindexed/deleted/differently named work. No prior actual attempt was identified, so this investigation records five new substantive approaches rather than skipping on the basis of catalog triage.

## Approach1: Integrability, tails, and representation dependence

The natural first route was to upgrade the known 1/r construction or turn its tail into a lower bound for every representation. Both fail without a new ingredient.

### Proposition1.1: the exact tail threshold

For an integer-valued nonnegative R,

E[R] = sum_{r>=0} P(R>r).

This follows by writing R=sum_{r>=0} 1{R>r} and applying monotone convergence. In particular, finiteness is equivalent to convergence of sum_{j>=0} 2^j P(R>2^j), by monotonicity on dyadic intervals. If E[R]<infinity then r P(R>r) tends to0: the tail sum over floor(r/2)<=s<r is at least floor(r/2)P(R>r) and tends to0. The converse is false, for example with a decreasing survival tail comparable to 1/(r log r).

An O(1/r) upper bound does not imply divergence. Both an exponential-tail variable and a variable with survival 1/(r+2) satisfy such an upper bound. For 0<a<1, an O(1/r) bound does imply E[R^a]<infinity, by the layer-cake integral, whose large-t integrand is O(t^{a-2}).

### Proposition1.2: an IID output with an essential infinite-mean representation

At each i in Z put an IID source symbol U_i=(N_i,(A_{i,j})_{j>=0}), where all bits are independent fair bits, independent of all selectors, and

P(N_i=n)=1/((n+1)(n+2)), n>=0.

Set X_i=A_{i+N_i,N_i}. Conditional on the entire selector field, distinct output sites use distinct bit coordinates: equality of (i+N_i,N_i) and (h+N_h,N_h) forces N_i=N_h and then i=h. Consequently X is an IID fair-bit process.

This specific coding has minimal spatial radius exactly N_i. The radius N_i suffices, and for any smaller radius the selected bit is an independent unseen bit. Changing it changes the output, even under almost-sure determination. Thus P(R>r)=1/(r+2) and E[R]=infinity. Yet the output law plainly has an identity coding with radius 0.

This example decisively rejects the inference from an inefficient given coding to an intrinsic obstruction. Its source entropy is infinite, which is permitted here; it does not establish an obstruction at finite source entropy either.

**Gap after approach1:** a law-invariant lower bound with a nonsummable tail, or a new construction with summable tails, is still needed.

## Approach2: Critical colorings and the wrong lower bounds

The two Holroyd–Liggett laws remain concrete candidates. Generic proper-coloring lower bounds do not settle them.

[Holroyd–Schramm–Wilson, Finitary Coloring](https://arxiv.org/abs/1412.2725), Theorem 1, has summable inverse-tower bounds in dimension 1 with at least 3 colors. These express an obstruction to a deterministic radius bound, not to finite mean. Theorem 2(ii), for 3 colors in d>=2, gives E[R^2]=infinity, not E[R]=infinity. In addition, Corollary 25 rules out stationary finitely dependent 3-colorings in these dimensions. Neither hypothesis matches the desired candidate.

### Proposition2.1: a source-atom bound is still summable

Suppose a proper coloring of Z is coded from an IID source having an atom a of mass p>0. On the event that all inputs in [-r,r+1] equal a, probability p^(2r+2), the two origin-centered input windows of radius r are identical after translation. If both sites0 and1 had radius at most r, their colors would therefore be equal. Hence

P(R>r) >= (1/2) p^(2r+2).

A rigorous almost-sure version uses the positive-probability cylinder and conditional determinacy at the two sites; impossible-coloring inputs have zero conditional mass. The bound is exponential and summable. It does not imply infinite mean, and supplies no estimate for an atomless source.

### Proposition 2.2: finite local transformations preserve integrability

If X=F(U) has integrable radius and Z_i is a deterministic radius-a local function of X, then

R_Z(0) <= a + max_{|j|<=a} R_X(j),

and E[R_Z(0)] <= a+(2a+1)E[R_X(0)] in dimension 1. No independence among the radii is needed. In dimension d replace 2a+1 by the ball size. Also, a radius-a transformation of a k-dependent field is (k+2a)-dependent, since separated enlarged input sets are independent. Finite independent products likewise preserve integrability, using a product IID source and a maximum bounded by the sum of radii.

Therefore such operations on the known good examples do not manufacture the desired obstruction. A reduction from a proposed candidate to a genuinely obstructed process would have to preserve the relevant law and all hypotheses.

**Gap after approach2:** no nonsummable, source-uniform radius lower bound is available for either critical one-dimensional law. Finite coloring constraints and failed bounded-radius coding cannot supply it alone.

## Approach3: Markov/Hankel obstructions and their exact stopping point

The known Holroyd–Liggett cylinder laws [Finitely dependent coloring](https://arxiv.org/abs/1403.2448), Section 3, use the building number B(w): B(empty)=1; B(w)=0 if w is improper; otherwise B(w) is the sum of B over words obtained by deleting one letter. Their critical laws are

p4(w)=B(w)/(2^n (n+1)!),
p3(w)=2 B(w)/(n+2)!,

for a word of length n. These source formulas are used as given; the finite verifier does not replace their published consistency/existence proof.

### Proposition3.1: explicit infinite-rank certificates

Let w_n be an alternating word on two fixed distinct colors, n>=1. Every interior deletion creates a repeated adjacent letter, while either endpoint deletion leaves an alternating word. Therefore B(w_n)=2^(n-1), by induction, and

p4(w_n)=1/(2(n+1)!),
p3(w_n)=2^n/(n+2)!.

For a positive integer s, take prefix u_i=(12)^i, i=1,...,s, and suffix v_j the alternating word starting with 1 of length j, j=0,...,s-1. Each concatenation is alternating. The corresponding Hankel minor has entries

H4(i,j)=1/[2(2i+j+1)!],
H3(i,j)=2^(2i+j)/(2i+j+2)!.

Writing V_s=product_{r=1}^{s-1} r!, their determinants are

det H4 = (-1)^[s(s-1)/2] 2^[s(s-1)/2] V_s /
          [2^s product_{i=1}^s (2i+s)!],

det H3 = (-1)^[s(s-1)/2] 2^[2s^2] V_s /
          [product_{i=1}^s (2i+s+1)!].

For H4, multiply row i by 2(2i+s)!: column j becomes the monic polynomial product_{t=j+2}^s(2i+t) of degree s-1-j in 2i. Reversing columns makes the degree order increasing, with unit triangular change of basis to monomials. The Vandermonde determinant at 2,4,...,2s is 2^[s(s-1)/2] V_s. This proves the first formula. For H3, remove row factors2^(2i) and column factors2^j, multiply row i by (2i+s+1)!, and repeat the same argument with product_{t=j+3}^{s+1}(2i+t). Restoring the powers of2 proves the second formula. Both are nonzero for every s.

For a hidden Markov process with m hidden states, every word probability admits the form alpha M_w 1, so p(uv)=alpha M_u M_v 1; every Hankel matrix factors through an m-dimensional space and has rank at most m. The nonzero minors above exclude every finite m. This is a reconstruction of a known exclusion for these laws; it is not a new resolution claim.

The continuation ratios 1/(n+2) and2/(n+3) also directly exclude finite-order Markov laws: lengths n and n+2 have the same fixed suffix but different conditional probabilities of alternating extension once n exceeds the proposed order.

### Why countably many states remain a genuine gap

Holroyd–Hutchcroft–Levy's Theorem 2 turns **bit-finitary** finite-mean coding into a function of a **countable-state** Markov chain. Infinite Hankel rank does not exclude countably many states. Moreover, unrestricted spatial finitariness of a continuous input is not automatically bit-finitariness of that particular coding. A measurable indicator of a positive-measure nowhere-dense closed subset of [0,1] already illustrates the finite-bit issue on one site. This is a caution about a representation, not an obstruction to coding its IID output law by other means.

For a countable IID input, coordinatewise inverse-transform generation reads finitely many bits almost surely for each input symbol, so a finite window can be generated from finitely many bits with no spatial enlargement. Thus the Markov implication is usable for that restricted source class, but still only gives a countable hidden chain.

**Gap after approach3:** one would need a countable-state hidden-Markov exclusion, together with an appropriate source/bit reduction for the full target, or another obstruction that works directly for all spatial codings. Neither is proved here.

## Approach4: information, variance, and conditioning barriers

### Proposition4.1: bounded information across a cut

For a stationary k-dependent finite-alphabet process on Z, finite left block A=X[-m,0], near-right block B=X[1,k], and far-right block C=X[k+1,n] satisfy I(A;C)=0. The chain rule gives

I(A;B,C)=I(A;B|C)<=H(B)<=k H(X0)<=k log|alphabet|.

The same holds for countable alphabets with H(X0)<infinity. Passing to increasing finite blocks gives the corresponding sigma-field bound. Thus an attempted obstruction based on divergent mutual information across a cut cannot work for finite-alphabet finitely dependent laws. This says nothing about more subtle information invariants or infinite-entropy output.

### Proposition4.2: exact tail triviality and additive concentration

The ordinary outside-finite-sets tail sigma-field of any finitely dependent process is trivial. A tail event is independent of the variables on every fixed finite set because it can be represented outside that set's k-neighborhood. A monotone-class argument then makes it independent of the entire sigma-field, including itself.

For a finite set V in Z^d, let Y_v=g_v(X_v) lie in an interval of length b_v. Partition V by its coordinates modulo k+1. There are M=(k+1)^d classes. In each class all variables are jointly independent, since each point is at distance greater than k from the union of the others. Holder's inequality followed by the elementary independent bounded-variable exponential estimate yields

log E exp[t sum_{v in V}(Y_v-EY_v)] <= (M t^2/8) sum_{v in V} b_v^2.

Indeed, Holder reduces the left exponential moment to the product, over classes c, of E exp[Mt sum_{v in c}(Y_v-EY_v)]^(1/M), and the independent Hoeffding estimate gives the displayed constant. This proves additive-observable concentration, not Gaussian concentration for every nonlinear local function.

In particular, bounded single-site covariances vanish outside radius k; their total absolute sum is finite. A susceptibility/divergent-covariance obstruction therefore cannot be copied from critical Ising directly. The general concentration literature has stronger assumptions and different moment targets, as recorded above.

### Proposition4.3: finite dependence does not give uniform conditional decoupling

Let U_i be IID Bernoulli(p), p=1/3, and X_i=U_i XOR U_{i+1}. This is 1-dependent and already has coding radius 1. Put n=2m and condition on E_n={X1=...=X[n-1]=1}. The compatible strings U1,...,Un are the two alternating strings, each with exactly m ones; hence U1 is conditionally fair. Under the additional condition X_n=0, its posterior probability of being1 is 1-p; under X_n=1 it is p. Since U0 remains independent Bernoulli(p),

P(X0=1 | E_n,X_n=0)=1-2p+2p^2=5/9,
P(X0=1 | E_n,X_n=1)=2p(1-p)=4/9.

These are positive-probability conditioning events at arbitrarily large n. The boundary influence remains 1/9 despite unconditional1-dependence. Thus a universal coupling proof cannot simply replace finite dependence by a uniform conditional-mixing estimate. The example is not a counterexample to finite-mean coding, as its radius 1 representation emphasizes.

**Gap after approach4:** the obvious tail, two-point, additive-concentration and cut-information invariants already behave well, while the conditional control needed by straightforward perfect-sampling constructions is not supplied by finite dependence.

## Approach5: a constructive subclass and the missing general extension

### Proposition5.1: finite-state primitive Markov laws have exponential-tail codings

Let P be a primitive transition matrix on a finite state set S. At each time t, independently sample a random map F_t:S->S, with the values F_t(x) independent across x and distributed by row P(x,.). There is L such that every entry of P^L is positive. Fix a terminal state a. We can choose supported maps f1,...,fL with composition constantly a: at each time choose, from every state that has a path of the remaining length to a, an edge leaving such a path; choices exist recursively. Values at states not in that set can be filled arbitrarily with a supported edge. All initial states are in the length-L predecessor set.

The probability delta that a consecutive random-map block equals this word is positive. Independent disjoint length-L blocks therefore yield

P(no such word in the preceding mL maps) <= (1-delta)^m.

Define Z_t by composing all updates from sufficiently far in the past. The last synchronizing occurrence makes the value independent of the earlier state, and such an occurrence exists almost surely. These definitions are consistent across t, translation-equivariant, stationary, and obey Z_t=F_t(Z[t-1]); F_t is independent of the past, so the transition law is P. Uniqueness of the stationary distribution identifies the desired law. A synchronizing block in the preceding mL maps certifies determination from that window, giving an exponential spatial-radius tail (up to an inessential endpoint shift). The analysis uses disjoint blocks only to bound the tail; the coding itself has no chosen global grid or random global phase.

If a finite-state stationary Markov chain is k-dependent, remove zero-stationary-mass states. Independence of Z0 and Z[k+1] gives P^(k+1)(x,y)=pi(y)>0 on the remaining states. Thus its matrix is primitive and the proposition applies. A finite-order finite-alphabet Markov process reduces to this case by taking block states; block states remain finitely dependent with a finite enlarged range. Finite local factors of these processes retain finite mean by Proposition 2.2.

This is a self-contained version of standard coupling-from-the-past reasoning, not a new general theorem. It excludes a substantial familiar subclass from the counterexample search.

**Gap after approach5:** a general finitely dependent law need not be finite-order Markov, as the critical-coloring continuation ratios prove. No finite synchronizing-state representation has been constructed for it. General finitary coding is known, but upgrading the multiscale completion probability to a summable spatial tail remains exactly the unresolved issue.

## Reproducible diagnostics and conclusion

Run `python verify.py`. It reproduces `results.json` using only the Python standard library. There are 9093 exact assertions: finite cylinder normalization/consistency and separated-block tests for the source formulas, alternating-word identities, nonzero Hankel minor formulas through size 8, selector-coordinate injectivity, telescoping tails, the conditional-XOR example, and a finite primitive-chain synchronizing word. The assertions neither formally verify the analytical arguments nor prove the original conjecture. Finite cylinder checks are diagnostics of formulas, not a replacement for the published infinite construction.

The exact remaining task is to construct a valid stationary k-dependent law and rule out every integrable-radius IID coding of that law, or prove an integrable-radius construction for every law in the original class. None of the five approaches meets either condition. The appropriate status is **unsolved, 5/5 substantive approaches**, with independently checkable scoped results retained.
