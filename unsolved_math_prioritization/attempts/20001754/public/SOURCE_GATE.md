# Source and scope gate

Checked 2026-10-03.

## Original target

- The requested problem page, https://www.unsolvedmath.com/problems/20001754, returned HTTP 403.
- The pinned fallback identified AIM-GEOMETRY-0092, de Laat's Problem 1.32. Its displayed title describes an earlier partial theorem rather than the full question.
- The primary page http://aimpl.org/discreteaf/1/ was successfully retrieved directly (HTTP 200) and independently confirmed the exact formula: the admissible lengths are |x|, |y|, |x-y|, with no |x+y| requirement. Its attribution is de Laat. The HTTPS endpoint failed.
- The [AIM workshop archive](https://www.aimath.org/pastworkshops/) dates the workshop to September 24–28, 2018.

The original target is the unrestricted optimum comparison and a function-conversion question; proving only the independently invariant subproblem is insufficient.

## Literature

The primary [Cohn–de Laat–Salmon paper](https://arxiv.org/abs/2206.15373) was read directly. Its current arXiv record lists only the 2022 v1. Relevant statements were checked in the full text: general sign-constrained duality, Schwartz comparison, the product bound, and the distinct lattice bound with both sums and differences. Targeted current searches did not identify a verified resolution of the exact AIM triangle formulation. This is a limited search, not an assertion that no such result exists.

## Genuine prior attempts

The pinned research attempt on this exact target already established the independent-subclass collapse and the sign-set sandwich, and discussed naive tensor/restriction failures. Those claims are treated as prior work and rechecked. The additional results in this package are identified separately in `RESEARCH_LOG.md`.

Read-only GitHub searches on AlecKriebel/Math for the exact problem ID, “lattice three-point”, and a Cohn/lattice pull-request query found no separate indexed matching attempt. GitHub code search is not an exhaustive repository-history search. The main-branch queue read confirmed rank 514 and its queued 0/5 state at source-check time. Adjacent rank 513 concerns Mellin/modular periods of magic functions and is mathematically different.

## Publication boundary

Only this directory's mathematical notes, original check script, check output, and frozen manifest are proposed for publication. No source downloads, complete third-party texts, cached corpus records, private context, or PDFs are included. No repository mutation was performed in this investigation. Publication awaits fresh independent review.
