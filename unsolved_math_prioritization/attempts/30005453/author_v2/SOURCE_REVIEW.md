# Source and scope review

Checked 5 October 2026 (UTC).

## Identification

Problem 30005453, OWR-12697708-006, points to Conjecture 1 in the contribution
“Graph-based interacting Pólya urns” by V. Kleptsyn, joint with C. Hirsch and
M. Holmes, in the 2023 MATRIX-MFO report, DOI 10.4171/OWR/2023/12.
The official report was downloaded and its relevant mathematical pages
inspected, including visual inspection of printed pages 654 and 655.
The supplied problem statement's SHA-256 matches its supplied descriptor.
That identifies the record; the descriptor's assessment is not proof evidence.

The problem website itself was not readable: web opening failed and the
ordinary HTTP request returned 403. The report and the cited author manuscript
provide the primary mathematical content instead. No bypass was attempted.

## Hypotheses and conventions

The report uses positive vertex rates bounded above and bounded degrees,
continuous Poisson time, edge reinforcement proportional to a power of the
current edge count, and the normalization N_e(t)/t. The deterministic ODE
has a 1/t factor, removed by logarithmic time. Neither the rates nor the
edge weights are normalized to sum to one on an infinite graph.

The nonnegative reinforcement-exponent convention and unit initial weights
are explicit in the cited Couzinié-Hirsch manuscript. The theorem in this
package covers 0 <= alpha < 1, not negative exponents. Strict positivity
of the equilibrium is explicit here because boundary fixed points otherwise
invalidate uniqueness. Arbitrary initially zero edges are not included.

The report's bounded-degree scope is retained. Local finiteness alone is
not substituted for it. The candidate proof separately establishes the
stochastic convergence statement rather than claiming that equilibrium
uniqueness or ODE stability automatically gives convergence of the random
infinite network.

## Published and earlier baseline

Couzinié-Hirsch, Theorem 2.2, proves homogenization with unit firing rates on
bounded-degree graphs for alpha<1/2, on regular graphs slightly beyond 1/2,
and on the integer line for alpha<1. Its existence proposition applies
throughout the sublinear range. The inspected arXiv v2 is dated 25 June 2021;
the publisher/author institutional pages identify the 2021 ECP publication,
DOI 10.1214/21-ECP404.

Couzinié's September 2018 master's thesis also studies inhomogeneous firing
rates, with a positive uniform lower bound in its initial setup. Its general
convergence theorem has alpha<1/2. It does not supply the full claim made in
the candidate theorem here. Bibliographic references to an earlier “Infinite
WARM graphs I” manuscript are not evidence of an available full resolution.

## Current-literature and prior-work limits

Targeted searches used the paper title, authors, WARM homogenization,
sublinear reinforcement, infinite graphs, and equilibrium terminology.
The author publication pages and primary-paper results were checked. No
retrieved primary source was found to establish the complete positive-equilibrium
theorem stated here.
This is a dated, bounded search result, not proof of novelty or universal
absence of another result.

Repository checks found no matching actual prior-attempt artifact using the
exact ID, problem number, title, reinforcement terms, PR searches, branch and
commit searches, code search, and the main problems subtree. The full recursive
repository-tree requests failed; the successful subtree was not truncated.
See PRIOR_ATTEMPT_CHECK.json for the exact scope. A queue or triage entry is
not treated as an earlier proof attempt.

## Remaining validation

The package claims a complete author-level candidate proof of an explicitly
corrected positive-equilibrium statement. The primary report does not explicitly
restrict uniqueness to positive equilibria; that reading is an interpretation,
not a verified source convention. The outstanding task is independent scrutiny
of the compensator-normalized martingale law, passage to complete trajectories,
and the space-time maximum principle. There is no assertion that a numerical
check has discharged any of those analytic steps.
