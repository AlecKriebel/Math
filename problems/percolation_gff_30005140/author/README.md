# Gaussian-free-field maxima on percolation clusters

Problem 30005140 / OWR-10252936-003. Research cutoff: 2026-10-05 (UTC).

**Outcome: scoped partials; the all-supercritical-p question is unresolved in this investigation.** No proof, disproof, novelty claim, or editorial-readiness claim is made. The known near-one theorem is credited to Florian Schweiger and Ofer Zeitouni. A bounded current-literature search found no later resolution. An independent audit has not yet occurred.

The strongest authored results here are finite-network Gaussian identities, a quantitative covariance-to-maximum transfer lemma, a conditional first-order upper bound under an exponential variance-defect moment, and counterexamples to two proposed logical shortcuts. These do not supply the missing percolation estimates.

## Exact model and target

Fix p in (1/2, 1], independently retain each unoriented nearest-neighbor edge of Z^2 with probability p, and let C_infinity be the almost surely unique infinite open cluster. The parameter is fixed as N grows; a sequence p_N approaching 1/2 is outside this question. Put V_N={0,...,N-1}^2 and S_N=V_N intersect C_infinity.

For each environment, the finite-volume field is zero on C_infinity outside V_N. On S_N its density is proportional to

    exp[-(1/2) sum_{ {x,y} in E(C_infinity) } (phi_x-phi_y)^2].

Each unoriented edge appears once. Thus covariance is the inverse of the grounded combinatorial Laplacian, with diagonal equal to the open degree including edges exiting V_N. There is no extra degree normalization and no single-site pin at the origin. Closed edges impose no boundary penalty. This is a family of finite-box zero-boundary fields, not an unpinned stationary infinite-volume 2D field. No conditioning that the origin belongs to C_infinity is needed.

Every component of S_N connects by open edges to C_infinity outside the box. Its grounded Laplacian is consequently positive definite. Small boxes with S_N empty may be assigned maximum -infinity; almost surely S_N is nonempty for all sufficiently large N.

Write g_p=1/(2*pi*a_p), where a_p is the deterministic homogenized coefficient in Schweiger-Zeitouni's convention (a_1=1). Then

    b_N(p) = sqrt(g_p) [2 log N - (3/4) log log N]
           = sqrt(2/(pi*a_p)) [log N - (3/8) log log N].

The target is almost-sure **quenched** convergence of max_{S_N} phi-b_N(p) to a nondegenerate law for every fixed p>1/2. The near-one theorem gives the same limiting probability law for almost every environment. Its normalized form is a randomly shifted Gumbel: E exp[-B_p exp(-2t)] for the field divided by sqrt(g_p), with a positive random mixing variable B_p. In the unnormalized coordinates the exponential slope is 2/sqrt(g_p). “Deterministic law” does not mean a constant limiting random variable. Annealed convergence is weaker.

The source is the 2022 workshop report, printed pp. 1535-1536. The catalog's parenthetical 2023 is not a different workshop. The detailed model and centering above are recovered from the cited 2022 preprint, Theorems 1.2 and 1.9; the article appeared in CPAM in 2024. See LITERATURE.md and source_identity.json.

## Five approaches and stopping result

1. Direct homogenization / continuity of the maximum: the requisite macroscopic theory exists, but maximum is not continuous in the available weak topologies. Proposition 1 provides an explicit Gaussian counterexample to that shortcut.
2. Fill closed bonds with small positive conductance: Proposition 2 proves fixed-box convergence and a coupling bound. Uniform control in N and restriction from the whole regularized lattice to S_N remain missing.
3. Electrical geometry of rare defects: Proposition 3 proves the exact pendant-tree decomposition and a conditional percolation pipe tail obstruction. It neither computes the true defect rate nor decides its relation to a_p.
4. Delete or control exceptional sites: Proposition 4 gives a conditional first-order upper bound and explains the loss at the log-log centering. Neither its all-p defect-moment hypothesis nor the O(1)-scale extremal estimate is proved.
5. Average over environments: Proposition 5 proves the one valid implication and gives a centered-Gaussian counterexample to the converse. No almost-sure quenched upgrade is obtained.

See PROOFS.md for complete arguments and exact gaps. No additional approach was pursued after these five.

## Reproduce the checks

Run from this directory, using Python 3 and its standard library:

    python verify.py
    python verify_manifest.py

The first command recomputes deterministic exact-arithmetic tests and compares the complete result with results.json. It does not read PDFs, source extracts, the catalog, or network resources. Computation checks the auxiliary identities, not the open conjecture. The manifest checks byte identities only, not mathematical validity.

## Contents and provenance boundary

This package contains authored exposition, executable checks, results, and public verification metadata. It excludes source PDFs, source extracts, images, raw source corpora, repository response bodies, private paths, and coordination material. Source byte hashes identify privately inspected inputs; they do not imply permission to redistribute those inputs. No third party was contacted and no remote write was made in this investigation.
