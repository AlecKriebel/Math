# Request for independent full review

Target: 30001370 / OWR-4132-003. Candidate complete answer after three genuine
author turns. No final disposition or publication before independent audit.

Read SOURCE_SCOPE.md, FINAL_RESULT.md, TURN_1.md and TURN_3.md as the main
dependency chain. Audit TURN_2.md separately: it is not needed by turn 3,
but all its derivative-space qualifications and the preprint proof precision
must be checked. Replay all three check_turn_*.py files and compare their
complete outputs to TURN_*_CHECKS.json. Check all historical manifests and
FINAL_AUTHOR_MANIFEST.json with raw file bytes.

Highest-risk points:

- exact source D, relative L1 topology, 0<A≤0.4 and 6<B≤16;
- source Proposition 4 is only on D', whereas the new backward lift is
  asserted for all densities, without regularity or positivity assumptions;
- turn 1: monotonicity in the implicit feedback inversion, sections on zero
  target-density fibers, and the open-map boundary pullback;
- turn 3: pathwise differentiation on an arbitrary probability space, the
  rank-one norm estimate and the rational certificate for the whole range;
- the two coupled inputs have identical original branch labels, which cancel
  in the L2 difference; no branch independence is allowed or needed;
- each backward law is absolutely continuous by branchwise sublaw domination,
  and its parameter is exactly the law's own feedback;
- the global transport glues continuously at every cut, remains absolutely
  continuous, and can have flat intervals;
- the logarithmic distortion constant is uniform in the number of steps;
- estimate (17) is under unweighted Lebesgue measure using P_sequence(1),
  not under the original u measure; no square-integrability of u_n is assumed;
- total variation is obtained from H_*(H' dx)=dx, which remains valid with
  flat intervals; mere uniform closeness of H to the identity would not suffice.

The full source PDFs and renders are retained separately from this public
packet. SOURCE_MANIFEST.json binds the PDFs and exact bibliographic URLs.
Please return exact mandatory corrections, or a scoped complete PASS, with
independent artifacts. No additional author research is occurring during review.
