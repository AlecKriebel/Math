# Five-turn result: morphic unbordered-factor conjecture unresolved

Problem30001554 / OWR-4425-009. Recommended disposition after independent review: **unsolved, 5/5**.

The original Conjecture27 asks whether |w|>=3tau_theta(w) forces the maximal theta-unbordered-factor length to equal the least alternating theta-period, for every nonempty word and morphic involution. Theta may have fixed points; borders are nonempty and proper, and overlaps are allowed. [Original report, p.2222](https://ems.press/content/serial-article-files/46296).

## Proven scoped results

1. A self-contained signed Fine–Wilf/extension/gluing argument reduces each fixed-tau question to finite windows. First appearances of new involution orbits occur within the first tau positions, giving a complete canonical finite alphabet reduction
2. The conjecture holds for **all finite alphabets, morphic involutions and word lengths whenever tau<=8**. Complete uncapped enumeration at tau8 has487,930 terminal canonical words; incremental Python and literal C++ agree on every per-depth count and the full stream digest
3. Equality is unconditional for tau<=3. The exact optimal saturation lengths for fixed tau4,5,6,7,8 are respectively9,11,15,17,21, with finite lower witnesses
4. An exact all-parameter classification of binary parity-adjusted three-run words with even middle length reproves the source's family and gives symmetric gap examples with n=3tau−4. They stay below the source threshold
5. For every morphic involution, n>=2pi_alt−1 implies tau=pi_alt, with an explicit primitive least-rotation witness. Consequently, any gap word has only strictly nonoverlapping theta-borders. A hypothetical least-tau original counterexample can be chosen with tau>=9, n=3tau, and pi_alt>=ceil((3tau+2)/2)

Turn1 additionally gives an orbit-period reduction using the credited ordinary Holub–Nowotka theorem. The later first-orbit bound and signed gluing proofs are independent of that external theorem. The signed Fine–Wilf statement is already in the original report and is reproved here; source overlap and novelty limits are explicit.

## Sharp remaining gap

No proof that the finite-window inclusion holds for every tau is known in this packet, and no genuine original-conjecture counterexample was found. The recurrence counting periodic completions counts a subset; it does not show all bounded-unbordered words belong to it. The all-length bounded-tau theorem is not an unrestricted theorem, and it is not merely a bounded-length scan.

All five author turns are frozen. Independent full source/proof review is pending. No novelty or priority claim is made. The contemporaneous Bischoff2010 thesis could not be retrieved (HTTP502), and its contents were not audited. Raw PDFs and imported records are not redistributed. Python controls use the standard library; the optional independent stream replay uses a C++17 compiler and sha256sum.
