# Positive three-braid concordance: exact scoped results

Problem 30006060, OWR-14298592-014. Author investigation, 5/5 substantive approaches. The original smooth-concordance question remains **unsolved**. This packet does not claim a new solution, historical novelty, or independent acceptance.

Let K and J be the oriented closures of

- K: sigma1^3 sigma2^3 sigma1^6 sigma2^6;
- J: sigma1^3 sigma2^5 sigma1^3 sigma2^7.

Retained results:

1. Both have the same explicitly calculated Alexander polynomial, determinant 243, and genus 8. The difference passes the Fox–Milnor factorization test.
2. Their entire Levine–Tristram signature and nullity functions agree. This is proved by a tree-gauge argument and exact equality of adjacency characteristic polynomials, including singular parameters, rather than numerical sampling.
3. Their double branched-cover homology groups are different, proving non-isotopy. Nevertheless the difference linking form has a fully explicit metabolizer, so this linking-form obstruction vanishes.
4. Their tau, Rasmussen s, and Upsilon(1) agree at 8, 16, and -7. Neither knot is an L-space knot or quasi-alternating. The full Upsilon functions and full knot Floer complexes have not been computed.
5. A six-saddle movie gives a connected genus-three cobordism. Baker's theorem rules out a ribbon disk for K # -J and rules out homotopy-ribbon concordance in either direction. It does not rule out smooth concordance.

The remaining task is to obstruct a smooth annulus using a genuine stronger concordance invariant, or construct and verify an annulus. No topological locally flat concordance verdict is asserted either.

## Replay

Run `python3 verify.py > replay.json`, then compare `replay.json` with `results.json`. Python's standard library suffices. The program checks exact integer and rational identities; the mathematical proof and the geometric interpretation of the matrices are in `PROOF.md`.

Files contain authored proofs, code, calculated certificates, and public verification metadata only. Downloaded papers, source extracts, images, full source datasets, and private coordination material are excluded. `SOURCE_AUDIT.md` records current-source and prior-repository inspection limits. A frozen manifest accompanies the packet. Independent audit is still required.
