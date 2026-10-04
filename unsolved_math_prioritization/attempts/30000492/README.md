# Settled quadratic polynomials: audited partial results

Problem 30000492 / OWR-1274-008, queue rank 656. Final research disposition: **unsolved, 5/5 approaches completed**.

The intended odd-characteristic settledness conjecture and a justified general refined transition law remain unresolved. The independent AI audit passes the stated partial results without required corrections. It does not certify novelty, human peer review or proof-assistant verification.

## Results and boundaries

- A finite critical-orbit stability criterion certifies individual factors.
- An exact eventual-stability threshold is proved for the fixed-critical-point special family over odd prime powers.
- Monotone stable mass and a conditional uniform-depth absorption inequality are proved. The uniform-depth hypothesis remains unproved in general.
- The characteristic-two result for x^2+x+1 over F2 is a separate scope correction, not a solution of the intended odd-characteristic problem.
- The Markov-history obstruction is credited published prior work. The exact witness illustrates it, without claiming novelty.
- Finite mass lower bounds do not resolve the limiting unstable mass.

Read [the author proof](packet/PROOF.md), [limitations](packet/LIMITATIONS.md), and [the full independent audit](audit/AUDIT.md). The original author and audit files and both archives are preserved byte-for-byte. Historical pending-audit and no-remote-write fields describe their frozen creation stages; this entrypoint records the completed independent audit and current draft submission. They are not silently rewritten.

## Reproduce without a network

The recorded byte-exact runtime is Python 3.12.14 with SymPy 1.14.0. Install the pinned dependency in a suitable environment, then run from any working directory:

    python -B /path/to/30000492/verify_packet.py

The wrapper verifies exact inventories, hashes, archive membership and author/audit binding, then runs all four frozen programs in a clean temporary copy. It compares saved results, distinguishing byte-exact reproduction from runtime-version-only differences. It rejects optimized Python because the frozen programs use assertions. No original files are modified and no source downloads are needed. To check only the package integrity, add --integrity-only.

The independent full-iterate check shares SymPy with the author; the separate certificate checker is pure Python and imports neither SymPy nor author code. Finite checks supplement the written partial proofs and do not prove general settledness.

## Repository scope

Only this problem's Status and Turns queue cells change. All other queue bytes, including the pre-existing embedded malformed header, are preserved. This draft contains authored mathematics, code, the full safe independent audit, and public verification metadata. No source PDFs, extracted source text, catalogue corpus, private coordination files or credentials are included. No merge, GitHub release, DOI action or outreach is part of this submission.

Research-goal estimate retained from the author: 10%, subjective and not a probability of solution. The five-approach research budget is complete; the general theorem remains open in this packet.
