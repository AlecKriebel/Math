# Scope and interpretation

Problem 8800068 / AMR-087-0068. Date: 2026-10-20 UTC.

This is an authored mathematical research and verification package, not a claim that the historical question has been solved or that its literature status is known exhaustively. No claim of novelty is made.

## Chosen target

An unbounded sequence of dimensions n, monic q in Z[X] of degree n, full-rank ideals in Z[X]/(q), and ordered bases B of their coefficient lattices in the fixed coordinates (1,X,...,X^(n-1)), with ordinary Euclidean norm. Each basis is exactly (delta,eta)=(3/4,1/2)-LLL-reduced. The desired first-vector ratio satisfies liminf log_2(||b_1||/lambda_1)/n >= 1/2, matching the general LLL upper-bound exponential rate.

The quotient polynomial may vary and be reducible; ideals need not be principal. This chosen target is not silently attributed to the historical author, whose question does not specify these conventions. A constant-factor match to 2^((n-1)/2) is stronger than the chosen rate requirement.

An already-reduced input is stationary only for the specified exact routine leaving size-reduction ties |mu|=1/2 unchanged and swapping on strict Lovasz failure. There is no assertion about HNF starts, all input bases, the shortest returned basis vector, general algorithmic hardness, or a runtime lower bound. SVP approximation and determinant-normalized Hermite factors are distinct.

## Limits of partial results

Obstructions with additional hypotheses apply only to those hypotheses. In particular, power-of-two negacyclic ideals, full or partial shortest-vector orbit span, fixed coefficient-order triangular bases, reversed control bases, and selected coordinate-prefix constructions must not be conflated with arbitrary coefficient ideals.

Exact finite computations check the stated cases and candidates only. A failed search, absent hit, or software exception does not establish nonexistence. Floating-point operations are exploratory; reported candidate reducedness is checked by exact rational arithmetic. The written proofs, not the finite checks, establish universal statements.

## Content boundary

Included: authored mathematical arguments, audits, scripts, generated finite-check results, public scholarly citations, and source-verification hashes/sizes. Excluded: source PDFs or extracted source text, source datasets and catalog records, personal information, and coordination material. Historical-source quotations are short and attributed.
