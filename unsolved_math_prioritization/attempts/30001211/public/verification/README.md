# Exact controls and limits

Run `python check.py` from this directory, or `python verification/check.py`
from the packet root. Python 3.10+ and its standard library suffice. Output is
deterministic JSON; compare it byte-for-byte with `result.json`.

All field operations use pairs of rational numbers in Q(sqrt(2)). Ordering is
decided by rational squares and signs, without binary floating point. The
tested 3-IET is the first return of an irrational rotation to [0,1), with
lengths a=(sqrt(2)-1)/2, b=1/4, c=3/4-a. Minimality follows analytically from
the irrational rotation, not from these finite trajectories.

The controls check translation integrality and conjugate bounds; 102 initial
points through 200 iterates; the exact 1,2,1 inducing clock; inverse identities;
continuity-cylinder translations and two-sided endpoint sets up to depth 24;
nine finite reciprocal-potential inequalities, each through 512 terms; and the
first three stages of the rational covering construction. Negative controls
reject a corrupted middle translation, a corrupted inverse target, and a
constant sequence as an all-target collapsing sequence.

The exact analytic arguments are in RESULT.md. Samples do not establish a
universal IET theorem, any limit, literature completeness, or novelty. The
covering construction's proof supplies its unbounded continuation; only three
stages are computed. No approximation of an uncountable quantifier by a grid
is used in a proof.
