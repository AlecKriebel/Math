# Function Theory 6.72: candidate negative resolution

This provisional, unrefereed note claims that every support point maximizing

L(f) = a2(f) + i·10^(-24)·(a4(f) − 3a3(f))

has an omitted slit with nonmonotone argument and nonmonotone radial angle. Both the signed radial angle and its ordinary nonnegative magnitude are covered.

The maximizer exists by compactness of the normalized schlicht class. The proof applies uniformly to every maximizer and uses the classical support-slit/Schiffer theorem. A quantitative endpoint estimate ensures that the sign-changing trajectory segment really is omitted by the extremal function. The note does not assume that arbitrary quadratic-differential trajectories are extremal.

- [Complete candidate proof](PROOF.md)
- [Research and approach log](ATTEMPT_LOG.md)
- [Source and scope checks](SOURCE_GATE.md)
- [Source manifest](SOURCE_MANIFEST.json)
- [Exact finite-control results](CHECKS.json)
- [Claim status and limitations](STATUS.json)

Run with Python 3.10 or later, using only the standard library:

    python verify.py
    python verify_manifest.py

The first command performs 56 exact algebraic and inequality checks, including positive and negative controls. The second checks the frozen file hashes. Neither is a formal verification of the analytic theorems or proof, nor a novelty certificate. No source PDFs or catalogue corpus files are included.

Target: [UnsolvedMath 2306072](https://www.unsolvedmath.com/problems/2306072), AMR-022-6072, Hayman–Lingham Problem 6.72, attributed to P. L. Duren. The catalogue URL was inaccessible at checking time; the actual mathematical target was verified against the primary 2018 collection.
