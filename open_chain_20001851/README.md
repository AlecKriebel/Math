# Equilateral open chains in three-space: five partial attempts

Problem **20001851 / AIM-GEOMETRY-0189**, rank 459.

**Outcome: unsolved, 5/5 substantive proof attempts.** The original question
asks whether every embedded open chain of unit rigid bars in R3 can be
straightened while preserving lengths and avoiding self-intersections. This
packet supplies neither a universal proof nor a locked equilateral chain.
The imported catalogue title describes an earlier sufficient certificate,
not a different solved problem.

## Results and their exact scope

1. [Linear scalar-axis characterization](ATTEMPT_1.md): for `n>=4`, the
   nonadjacent-interval certificate is equivalent to `n` strict linear
   inequalities in the axis. Failure has a convex-dependence witness involving
   at most four vectors. This is a certificate test, not a locking test.
2. [Direct ordered-core motion](ATTEMPT_2.md): terminal rotations within safe
   spherical caps followed by normalized edge interpolation give a
   self-contained rigid-bar straightening of every scalar-certified chain.
3. [Exact limits of that certificate](ATTEMPT_3.md): rational five- and six-bar
   equilateral chains fail every scalar-axis certificate but have simple
   orthogonal projections. The six-bar obstruction is stable in three
   dimensions. These chains are unlocked.
4. [Local clearance and rational reduction](ATTEMPT_4.md): an explicit
   same-component neighborhood shows any hypothetical locked unit chain has
   a rational-coordinate locked counterpart with the same number of bars.
   Fixed-count component computation is possible in principle, but none was
   carried out.
5. [Failure of greedy endpoint induction](ATTEMPT_5.md): an explicit
   eight-unit-bar construction prevents straightening the first joint while
   fixing the seven-bar tail. Its spherical barrier is not shown to survive
   unrestricted motion of that tail and therefore does not prove locking.

The primary-source and prior-attempt checks are in [SOURCE_GATE.md](SOURCE_GATE.md).
The attempt record is in [RESEARCH_LOG.md](RESEARCH_LOG.md). No first-discovery,
novelty, or resolution claim is made for these partial results.

## Reproduction

Run `python3 verify_certificates.py` from this directory. It uses only the
Python standard library and reproduces [checks.json](checks.json).

- 21,504 finite scalar-sequence consistency tests of the interval-order theorem
- 11 exact rational unit-length checks and two positive-dependence witnesses
- 16 exact nonadjacent-pair checks for the simple projections
- 40 rigorously outward-rounded interval inequalities certifying the
  eight-bar geometry at parameter `99/100`

The eight-bar length identities follow from the written algebraic construction;
the verifier's eight enclosures containing one are consistency checks, not
proofs of equality. No finite check proves the universal connectivity claim.

## Research status

The original source is [Streinu's Item 2 in the 2014 AIM list](https://aimath.org/pastworkshops/linkagesproblems.pdf),
clarified by [Working Group 2 in the workshop report](https://aimath.org/pastworkshops/linkagesrep.pdf).
The known simple-projection theorem and unit-chain bound for at most five bars
are discussed in [Biedl et al.](https://arxiv.org/abs/cs/9910009).

AI tools were used extensively for research, derivation, writing, and checking.
These are unrefereed partial research notes, not an externally peer-reviewed
resolution. Original PDFs, screenshots, and corpus copies are not included.
