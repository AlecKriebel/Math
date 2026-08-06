# Gate-0 audit of the Phase-IV bounded-defect interface

## Finding

The Phase-IV verifier correctly checked several finite graph and
Poisson-corrector identities, but its structural `unpaired service` interface
did not by itself certify all of the following simultaneously:

- retention of the actual reaction target at each fast phase;
- population feasibility of a chosen target-following path;
- containment of that path in the declared stopped component;
- the possibility of long internal fast motion before absorption.

Accordingly, the Phase-V proof does **not** use the Phase-IV local theorem as
a black box.

## Replacement certificate

For every ordered pair of complexes, Phase V fixes an actual directed
reaction path.  If the current augmented state is \((r+y_k,y_k)\), the
reaction \(y_k\to y_{k+1}\) is literally enabled and leads to
\((r+y_{k+1},y_{k+1})\).  Consequently:

1. the finite phase space is the finite path itself;
2. every terminal and path phase is explicit;
3. population and lattice feasibility are exact;
4. closedness of the communicating class keeps every lifted path state in
   the class;
5. every designated conditional probability is the positive constant
   \(\kappa_{e_k}/\bar\kappa_{y_k}\) times the positive source probability;
6. a deviation stops immediately rather than being hidden in an SCC;
7. the source-probability estimate is uniform through the state-independent
   constant \(C_0\);
8. no absorption approximation \(P_N=P_0+O(N^{-1})\) is required;
9. no Poisson corrector is required;
10. physical duration has the explicit Gamma domination stated in
    `defect_promotion.md`.

The exact residual identity and finite recursion have two independent
implementations: direct recursion and exhaustive enumeration of all terminal
branches for each calibration episode.

The prior bounded-defect theorem remains useful intuition and its verified
finite algebra is preserved, but no unverified interface from that phase is
load bearing in the final theorem.
