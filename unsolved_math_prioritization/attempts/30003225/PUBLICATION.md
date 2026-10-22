# A free-chain counterexample to a Nash-intersection conjecture

Prepared preprint package for problem 30003225 / OWR-14754-011 and PR1332.
Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.
Version 1.0.0, 22 October 2026. Publication registration is pending.

The [five-page paper](publication/free-chain-nash-intersections.pdf),
[complete source and verification ZIP](publication/free-chain-nash-intersections-source-and-verification.zip),
[editable TeX](publication/source/main.tex), and
[source/priority audit](publication/source/SOURCE_AUDIT.md) contain the current
proof, its precise interpretation and its bounded literature investigation.
The audit includes the exact historical 20-query inventory and its actual
response-retention/read limits. The [upload kit](publication/free-chain-nash-intersections-upload-kit.zip)
contains the same two scientific attachments and the original reviewed metadata
and instructions. The [deposit manifest](publication/zenodo-deposit.json) and
[metadata](publication/zenodo-metadata.json) are the frozen preparation03 copies.

For centered complex formal arcs, after choosing regular coordinates flattening
the fixed prefix, the complete family of divisors obtained by n successive free
point blowups with the first k centers fixed, n >= 3 and 2 <= k < n, has intersection
of its closed reduced Nash supports

    {ord_t x >= ceil(n/k), ord_t y >= n}.

Every completion is represented by y=P(x)+x^n w, with all complex coefficients
of P=sum(a_j*x^j), k<=j<n, allowed. The proof exhausts the free-center family,
uses both blowup charts and dense transverse loci, and includes satellite
limits, identically zero coordinates and constant arcs. The conditional
exact-common-prefix reading gives the same reduced support. Every reference
prefix divisor D_j has exact-q and at-least-q contact closure

    {ord_t x >= q, ord_t y >= jq},  q,j positive integers.

Five blowups yield thresholds (3,5) and (2,5), for k=2 and k=3 respectively.
Neither equals (q,jq) for any positive integers q,j. Fixing the genuinely free
selected c3 still leaves c4,c5 variable. The mapped last-shared, literal
zero-based created-divisor, selected-point-fixed, one-based and conditional
exact-contact readings are all treated explicitly in the paper.

This is the specified-reference-multiple obstruction for Conjecture 1 in
Fernández de Bobadilla, Pe Pereira and Popescu-Pampu, arXiv1501.06898v3, p.31,
and Pe Pereira's joint workshop contribution, OWR 46/2016, pp.2678–2681,
Conjecture 1 on p.2679. Those primary formulations print an intersection; the
catalogue union is a transcription discrepancy. The bare equivalence symbol
is undefined and the source's global indexing is inconsistent. No unique
author-intended erratum or result about an unspecified replacement is asserted.
The publisher-typeset original remains unread/inaccessible; its
DOI 10.1016/j.aim.2017.09.035 identifies the source article, not this note.

The two intersections ARE maximal divisorial Nash sets of other primitive
toric divisors, weights (3,5) and (2,5). No arbitrary-divisor negative,
Conjecture 2, general Nash-problem solution, general satellite-family formula
or nonreduced-scheme equality is claimed. Ishii's established contact/toric
framework and the original paper's combinatorial/cylindrical results are
credited. The contribution is the explicit full-family calculation and its
reference-ray obstruction. The bounded source investigation found no
authenticated earlier exact negative in inspected material; worldwide
firstness, exhaustive novelty and continuous openness are unestablished.

The seven original research-reader files remain byte-for-byte historical
records. In particular their older 18/44-check and recovery-archive claims are
not newly replayed here: no corresponding executable is among the original
eight PR paths. Their older workshop page-range wording is superseded by the
correct 2678–2681 citation in the current paper and source audit. The new
[standard-library verifier](publication/source/verification/exact_checks.py),
[active mutation checks](publication/source/verification/run_mutations.py),
expected complete outputs and [reproduction instructions](publication/source/README.md)
are distinct, included and reproducible in normal, -O and -OO modes via
`python3 -I -S -B reproduce.py` from the expanded source directory. Finite
diagnostics supplement the universal written proofs; they do not certify
source intent, priority or arbitrary complex/infinite assertions. The builder
reconstructs all six products from the frozen PDF; genuine typesetting is a
separate verification recorded in the source build receipt.

AI tools were extensively involved in mathematical research, proof development
and reconstruction, exact/symbolic computation, literature investigation,
manuscript preparation and adversarial auditing. Alec Kriebel is the named
human author. This is an unrefereed preprint without formal independent human
peer review or journal acceptance; internal AI reviews are not those
certifications or proof-assistant certification. Authored prose is CC BY 4.0;
authored code is MIT licensed. No solution DOI is asserted in this prepared
package pointer.
