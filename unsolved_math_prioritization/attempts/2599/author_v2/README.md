# Kourovka 21.90 (UnsolvedMath 2599; ranked item 770)

**Disposition: partial results and an important convention boundary. Under the connected/nondegenerate interpretation, the existence question remains unresolved in this investigation.**

The primary problem statement does not explicitly impose the connected/nondegenerate convention; that research interpretation is an inference from the surrounding literature, not verified authorial intent.

The target asks for a Q-polynomial distance-regular graph of diameter three with both exact-distance-two and exact-distance-three graphs strongly regular. The October 2026 editor-maintained source, printed page 190, attributes it to A. A. Makhnev, with no solved or unverified-AI-solution marker.

Results:

- If disconnected strongly regular graphs with μ=0 are permitted, the six-cycle works. More generally every crown graph K(n,n) minus a perfect matching works. A full distance-count and Q-polynomial proof is included. The 2019 literature already explicitly recognizes this exception; it is not presented as a new solution.
- Independent adjacency-algebra calculations recover the necessary intersection array {t(c+1)+a,tc,a+1;1,c,t(c+1)} and Q-polynomial equation (c+1)(t²−a−1)=a(a+1).
- Complete exact arguments exclude primitive solutions with t≤3 or c=1. Five specific arrays are ruled out by rational triple-intersection certificates, including {19,12,5;1,4,15} and {17,8,6;1,2,12}.
- A fully rational necessary-parameter sieve through t=30 tests 959 parameter triples and retains 159. The five certificates remove five, leaving 154, before applying external published exclusions. These survivors are not constructed graphs and are not claimed to be open parameter sets.
- The directly matching 2019 paper, related 2019/2020 exclusions, and a relevant 2023 exclusion were located. Later searches did not verify a full construction or a full nonexistence theorem.

## Files and replay

`PROOFS.md` contains complete authored proofs and precise scope.
`RESEARCH_LOG.md` records five approaches and literature status.
`SOURCE_VERIFICATION.json` records public source URLs, inspection limits, and dataset hashes.
`LIMITATIONS.md` records the unresolved gap.

Run from this directory:

    python verify_math.py
    python verify_triples.py
    python verify_symbolic.py
    python verify_manifest.py

The first two use only the Python standard library. The optional symbolic identity check requires SymPy (tested with 1.14.0). Discovery used floating-point linear programming, but the shipped nonexistence certificates replay solely with exact rational arithmetic. Positive controls use explicit crown graphs; mutated certificate controls must fail.

No graph construction for the connected/nondegenerate problem, comprehensive novelty claim, or editorial status change is asserted. A fresh independent audit is required before any publication.
