# Prepublication theorem-state snapshot

Assembled October 6, 2026, 22:32 America/Los_Angeles (October 7 UTC). This immutable package snapshot predates the final fresh review and production publication. Subsequent complete-package reviews, publication receipts, DOI/tracker status and research log are recorded separately in the [project repository](https://github.com/AlecKriebel/Math/tree/main/openai_followon_weighted_hafnian), outside the frozen upload archive. Pending steps below describe this assembly time.

Strongest unconditional result: exact polynomial-bit reduction from every binary nonnegative rational symmetric even-order hafnian to a finite simple graph count, with exact matching fibers. Integer gadget signature (W,1,0,0), size 4 bits(W)-2; global graph size O(L²); rational scale D^m has O(mL) bits. Empty hafnian one. Support feasibility decides zero exactly.

Approximation/sampling consequences: citing the audited OpenAI family-113 unweighted FPRAS, the reduction gives relative epsilon error with failure <=delta and polynomial bit time in full input, epsilon inverse, log delta inverse; a feasible positive input returns a positive estimate on every tape. Weighted sampler has TV <eta, worst-case bit time polynomial in input and eta inverse, and always-feasible output. Expanded order N=2s uses <=s² calls at relative eta/(4s), failure eta/(4s²), <=s²+1 witness calls and <=s ceil(log2(4s²/eta)) additional draw bits.

Validation basis: independent mathematical source audit found no substantive gap; independent exact gadget reconstruction, adversarial reconstruction and finite enumeration passed; sampling proof and exact finite-law integration passed. Actual upstream Lean semantics inspected, but kernel/axiom-closure rebuild unverified. No claim of follow-on formalization or practical base FPRAS implementation.

Priority: rational weighted/unweighted equivalence and logarithmic gadgets already public; no separate previously unresolved complexity statement is credited to this project. Publication framing is an attributed consequence/implementation note, with no first claim. Complete-package reviews and production publication/tracker still pending.
