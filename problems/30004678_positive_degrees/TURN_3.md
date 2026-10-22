# Turn 3: generic masks produce an infinite antichain, and defeat finite-code exhaustion

The original finite-cardinality problem remains unresolved. This turn proves a concrete obstruction to using the generic finite-code family of Turn 2 as an exact finite fiber. Genericity and signed oracle codings are classical methods; no priority claim is made.

## 1. Binary masks: exact equivalence criterion

Let A be a 1-generic binary sequence and S,T computable binary masks. Put X_S(n)=A(n) XOR S(n). Then

    X_S ≤p X_T  iff  S XOR T is finite.

If the masks differ at only finitely many positions, hardcode the correct target bits at those positions and copy the input at every other position. The hardcoded finite data are allowed in the existence of a recursive reduction; no uniform procedure from indices of S,T is asserted.

Conversely suppose a total positive truth-table functional Φ maps X_T to X_S. The c.e. open mismatch set is avoided by A, so some prefix σ forces equality for every binary extension. If n beyond σ has S(n)≠T(n), vary only A(n) in the direction making X_T(n) increase. Every other source bit stays fixed, while X_S(n) decreases. This contradicts monotonicity of Φ on all oracles. Hence every disagreement lies below the forcing prefix.

In particular there is no positive reduction in either direction for masks differing infinitely often. Every X_S is truth-table equivalent to A by the computable XOR operation, so this is a classification of the signed-mask subfamily inside one truth-table fiber, not of its entire fiber.

Take S_k={n: the exponent of 2 dividing n+1 is k}, for k=0,1,... . These computable sets are pairwise disjoint and infinite. Thus the X_Sk form an infinite antichain of positive degrees in the truth-table degree of every 1-generic A. This already excludes all finite cardinalities for this class of degrees.

## 2. Any nontrivial finite alphabet

The preceding obstruction also applies to the q-symbol generic sequences used in Turn 2, even when q is not a power of two. Identify the alphabet with {0,...,q−1}, and use the injective chain code

    u(a)_j=1 iff j<a,  for 0≤j<q−1.

Let π interchange symbols 0 and 1 and fix the others. For a computable mask S, define Y_S block n to be u(π^S(n)(Z(n))). All these encodings are truth-table equivalent by finite-block decoding and computable symbol permutations.

The same exact criterion holds: Y_S≤pY_T iff S XOR T is finite. Finite disagreement again permits hardcoding finitely many target blocks. If infinitely many blocks disagree, genericity forces a supposed reduction on an entire cylinder. Choose a disagreement block beyond the prefix, and choose its symbol in {0,1}. Increasing the source chain code from u(0) to u(1) decreases the target from u(1) to u(0), while all other blocks remain fixed. The target's first bit supplies the contradiction.

Consequently every generic q-symbol encoding, for every q≥2, has infinitely many positive degrees in its truth-table fiber. The 3,19,219-element copies from Turn 2 are therefore provably proper substructures of an infinite fiber. Merely changing the injective finite code or the alphabet size cannot turn that generic construction into a finite-cardinality example.

## 3. Scope and controls

This is a genuine restriction on a broad construction method, not an impossibility theorem for other odd cardinalities. The source's finite examples necessarily use different non-generic information. No statement about all nonrecursive degrees or arbitrary degrees below a generic is made.

The checker verifies the reversal witnesses for every ordered pair of alphabet symbols relevant to the two-symbol swap through alphabet size 20, exercises computable periodic masks and hardcoded finite exceptions, and exhausts all Boolean functions on up to three bits to check that no monotone function realizes a forced reversed coordinate. Infinite antichain nonreducibility is proved by genericity, not by finite simulations.
