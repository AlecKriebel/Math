# Final result: complexity versus cohomology remains unresolved after five turns

**Proposed disposition: unsolved,5/5, pending independent full review.** The packet does not prove the implication for every repetitive aperiodic low-complexity tiling and does not construct an admissible infinite-rank counterexample.

## Exact original question

A. Julien's Problem2.5.1 in the2016 quasicrystal collection asks whether p(n)=O(n^d) forces finite total rational Čech cohomology rank for the translational hull of an aperiodic repetitive d-dimensional tiling. Here aperiodic means no nonzero translational period. Integral finite generation, singular cohomology, rotational hulls, partially periodic examples and inverse limits with no finite local generating description are different scopes.

The full source was read and page8 visually checked: https://arxiv.org/abs/1604.06280 . The published page is587. The available Julien0804.0145 version1 has different theorem numbering; its one-dimensional Rauzy proof was read directly. Later Koivusalo–Walton2020/2021 corrections to the almost-canonical setup are recorded, while the canonical subclass is kept separate. No unverified unrestricted cut-and-project equivalence is used.

## Five complete scoped outcomes

1. **TURN_1.md:** A sharp Cartesian-product theorem. Products of minimal aperiodic one-dimensional systems with finite liminf n-cube complexity/n^d have finite rational cohomology, with total rank at most3^d times that coefficient. Products of Sturmian systems attain the bound. The argument explicitly uses cofinal Rauzy ranks and persistent classes.
2. **TURN_2.md:** A genuine repetitive fully aperiodic O(n²) sheared Thue–Morse/Sturmian tiling has finite limiting cohomology but unbounded approximant Betti numbers. Exact complexity recurrences give Euler characteristics2n+6 and−2n on two cofinal scale sequences. This blocks a raw approximant-counting strategy rather than the source conclusion.
3. **TURN_3.md:** An exact stable-image rank criterion and cochain-image computation. A recognizable collared model reconstructs the classical rational Thue–Morse rank2; the sheared example has limiting Betti numbers(1,4,4). Exact cropping maps certify the death of two transient degree2 dimensions between later scales.
4. **TURN_4.md:** Finite-stage local covering extensions of product tilings retain finite rational cohomology. A proper recognizable substitution product admits minimal cyclic local covers of every finite degree q, with exact Betti numbers(1,4,q+3) and complexity O(n²) with a coefficient proportional to q. These are finite-rank source-admissible examples, not one infinite-rank example.
5. **TURN_5.md:** The inverse2-adic covering tower has countably infinite rational H², but is nonexpansive and has no continuous finite-alphabet generating code. Its direct full-state decoration fails FLC, and the canonical finite-level complexity constants diverge. This diagnoses a failed counterexample route; no general impossibility of another FLC realization is claimed.

The remaining gap is a persistent-rank bound for arbitrary source-admissible tilings, or a construction preserving infinitely many rational classes while also retaining a single finite local generating description and one O(n^d) constant. Neither has been obtained.

## Foundations and credit

The one-dimensional complexity/cohomology link and Rauzy inverse limits are credited to Julien. The Thue–Morse cohomology result is classical Anderson–Putnam territory; its specialized collared model is reconstructed here rather than used as an unexplained black box. The proofs use standard Čech continuity, finite graph homology, rational Künneth, elementary covering homotopy/transfer and finite-dimensional linear algebra. Every covering claim identifies its actual finite-level model; no finite-to-one factor is treated as a covering automatically.

The finite models, covering computations and subgroup constructions carry no historical novelty claim. The known failure of integral finite generation does not supply a negative answer over Q. Likewise a profinite inverse-limit suspension with infinite cohomology is not automatically a finite-local-complexity tiling.

## Reproduction

Python3.10+ standard library only:

    python REPLAY_ALL.py

This compares all five checkers' output bytes with their frozen receipts and verifies all author manifest bindings. The author controls total5,367 assertions, including exact rational chain maps and image ranks. Optional `--sources PATH` verifies the four frozen primary PDFs, which are not included in the public packet. Finite checks support the written all-scale arguments and do not replace admissibility or direct-limit proofs.

All five turn files and their historical snapshots are frozen. Author search stops at five; only additive source, review or packaging corrections should follow.
