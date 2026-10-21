# Convex-body SOS-density convergence: result and scope

For every fixed compact convex body K in R^n with nonempty interior and every fixed real polynomial f, the normalized Lebesgue-measure hierarchy

    f^(r) = inf { integral_K f q dx : q is a global sum of squares,
                 degree(q)<=2r, integral_K q dx=1 }

satisfies

    0 <= f^(r)-min_K f <= C_{K,f}/r^2,     r>=1.

PROOF.md gives a complete explicit construction and constant. The witness is a single global square. The construction combines a quadratic Taylor upper estimator, homothetic growth of its sublevel volumes, and a fixed even power of a polynomial endpoint kernel. A dyadic shell estimate compares each tail directly with the same core mass that normalizes the density, avoiding a logarithmic loss.

MOMENT_FORMULATION.md gives an exact generalized-eigenvalue formulation at the nonsimple apex of a square pyramid. Its entries and feasible kernel witnesses use rational moments; no numerical SDP is treated as a certificate.

## Scope and source credit

The quadratic upper-estimator reduction is already present in Slot and Laurent's work, and polynomial concentration kernels are classical. The proof here is self-contained; no novelty or priority claim is made. The independent audit describes its bounded literature check and its limits.

The inspected Slot–Laurent paper's Theorem 11 gives O(log^2(r)/r^2) for general convex bodies with Lebesgue measure. Its concluding questions ask whether the logarithm can be removed. The final 2026 Laurent–Slot overview still lists that general rate in Table 1. These statements identify the source-matched improvement; they do not certify that the theorem was previously unknown. [Slot–Laurent paper](https://arxiv.org/abs/1905.08142), [2026 overview](https://ir.cwi.nl/pub/36052/36052.pdf).

The original Oberwolfach contribution has an incomplete displayed integral constraint. This result explicitly uses unit mass, consistent with the probability-density hierarchy in the full papers. It does not purport to solve an unnormalized formula. [Original report](https://ems.press/journals/owr/articles/16633).

## Limits

- The measure is Lebesgue. No claim is made for arbitrary unspecified reference measures.
- This is an upper O(r^-2) rate. It is not a two-sided Theta statement for each objective or for each body; constant objectives have zero error.
- The result is for the ordinary multivariate SOS-density hierarchy. It does not generally prove the same rate for densities restricted to s(f(x)), since the construction instead uses a quadratic upper proxy.
- The proof is an existence and rate argument; it does not assert an efficient way to find the minimizing point used to define the witness.
- Independent mathematical review is not a machine-checked formal proof, peer review, or a novelty certification.

The original problem identifier is OWR-16633-006 (corpus ID 30003990).
