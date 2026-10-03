# Turn 5: quantitative lower gaps, frequencies, and the missing coarse invariant

Date: 2026-10-03. This final mathematical route asks whether the nested lamination can be detected by a quantitative statistic rather than only a poset. It obtains explicit all-n estimates and then tests their geometric scope. The original QI conjecture remains unresolved after five substantive turns.

Let T_n=|phi^n(e)| and let L_n be the length of its longest contiguous subword using only a,b,c. Write rho>1 for the real root of x^3-x-1 and tau=(1+sqrt(5))/2.

## Longest lower-only gaps

Give a,b,c weights 1,rho,rho^2. Then alpha multiplies the weighted length of every positive lower word by exactly rho: the third image uses 1+rho=rho^3.

Every top-generator image starts with a top letter; only phi(d)=ea appends a lower letter. Consequently a maximal lower run after substitution comes from the image of one old lower run, possibly with one a prepended. No two old lower runs merge across a top letter, since every top-letter image retains at least one top letter. If R_n is the maximum weighted lower-run length, then

    R_(n+1) ≤ rho R_n + 1,
    R_n ≤ (rho^n-1)/(rho-1).

On the other hand, for n≥2,

    phi^n(e)=phi^(n-1)(e) phi^(n-2)(e) alpha^(n-2)(a).

Thus R_n≥rho^(n-2). Since the smallest and largest lower-letter weights are 1 and rho^2,

    rho^(n-4) ≤ L_n ≤ (rho^n-1)/(rho-1),   n≥2.       (1)

In particular L_n=Theta(rho^n). This is a proved estimate for every n, not a regression from the finite data.

## Frequencies and total growth

The full abelianization matrix M is also the exact letter-count matrix, because all images are positive. Its dominant eigenvalue is tau, strictly larger in modulus than the other four eigenvalues. An associated positive right eigenvector is

    v=(1,1,tau-1,1,tau).

Substitution verifies Mv=tau v using tau^2=tau+1. The upper 2-by-2 block is primitive, and e has nonzero projection to its Perron eigenspace. Solving for the forced lower block, or using the spectral decomposition, shows that M^n e_e divided by its total coordinate sum converges to v/(2+2tau). Hence

    T_n=Theta(tau^n),
    (#d+#e in phi^n(e))/T_n → 1/2.

Despite positive asymptotic top-letter frequency, the lower-only gaps are unbounded. Combining (1) with the total-length estimate gives

    L_n=Theta(T_n^kappa),
    kappa=log(rho)/log(tau)≈0.5843571576574038.

This is an explicit quantitative hierarchy in this marked positive-substitution model. It refines the finite-language certificate but is not claimed as a previously unknown theorem.

## Trying to turn the statistic into a QI obstruction

The frequency 1/2 fails an immediate metric test. Give each lower edge length k and each top edge length 1. This changes the graph metric by bounded multiplicative factors and cannot change the mapping torus's quasi-isometry class. The limiting top-edge share of total length becomes 1/(k+1), not 1/2. Therefore that raw density cannot be the desired QI invariant.

The power-law exponent survives this particular bounded rescaling and passage to positive powers. That is only a necessary sanity check. It is defined using the chosen fiber, its invariant free factor, the forward monodromy and its iterated top-edge paths. We have not shown that an arbitrary QI carries these features to corresponding objects. Even though Turn 1 makes the height epimorphism unique up to sign as an abstract group homomorphism, that does not make its fibers recognizable by arbitrary QIs. Also, reversing height exchanges the positive and negative dynamics and cannot be ignored.

The same missing transport theorem appears in the canonical subgroup-system approach of the 2026 depth paper: group-theoretic canonicity is weaker than coarse canonicity. This turn supplies no theorem making the gap exponent or nested subgroup pattern quasi-isometry invariant.

## Final mathematical disposition

The exact pair is noncommensurable, with a direct attracting-core reconstruction of the credited depth gap. Additional checked partials are: natural cyclic-cover homology; an integral class-two obstruction to retraction; a degree-two all-period filter plus bounded periodic-class search; and the gap/frequency estimates above.

Neither atoroidality of phi nor non-quasi-isometry of Gamma and G has been established here. The original AIM conjecture is **unsolved in this work**. No literature priority, complete lamination-poset computation, or general QI-invariance theorem is claimed.

## Verification

verify_t5() tracks exact letter counts and longest lower runs using a concatenation-summary recursion to n=100. It independently cross-checks those summaries against explicit words through n=15. checks_turn5.json includes exact counts and approximate explanatory constants. The asymptotic and all-n assertions rest on the proofs above, not the finite numerical checks.
