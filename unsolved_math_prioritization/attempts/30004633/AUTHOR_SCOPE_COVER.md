# Compact-domain porous-medium particle convergence: author continuation

Problem 30004633, OWR-4990379-003. Prepared 7 October 2026.

## Claim status

**Partial result only. The general irregular-solution problem is not solved.** This is an author-only continuation packet. Each theorem and obstruction needs its own independent review; the associated review reports are separate documents and are not inferred from the diagnostic checks.

The central candidate estimate, for the exact original compact-domain frozen-proximal scheme, is

\[
\sup_t\|X_N-X\|_{L^2(\rho_0)}^2+\int\|\dot X_N-\dot X\|_{L^2(\rho_0)}^2
\le C\bigl(\delta_N^2/\varepsilon+\varepsilon+\tau/\varepsilon\bigr).
\]

It is proved here for specified regular-pressure free-boundary classes, with 0<ε≤1 and τ≤ε. Convergence follows when ε→0, δ_N²/ε→0, and τ/ε→0. The velocity comparison is along the exact material labels; no identical rate is claimed for evaluating the discontinuous zero-extended physical velocity at particle positions.

## Included substantive approaches

- **Approach 2:** Positive-time Barenblatt profiles in arbitrary bounded Lipschitz physical domains, with a fixed positive clearance of their support from the wall. A signed quadratic pressure is flattened to a negative constant before the wall; the resulting vacuum residual is controlled by signed relative energy.
- **Approach 3:** General smooth, uniformly nondegenerate moving free boundaries. A normal-collar construction extends the pressure and proves the residual is bounded by the negative pressure in vacuum. The theorem is conditional on the exact pressure/interface regularity; it does not establish that regularity for arbitrary initial data.
- **Approach 4:** Reflecting-wall and orthant Barenblatt profiles, including physical-wall contact. A tangential-flow variation preserves the constrained proximal domain. This handles permanent symmetric reflecting contact, not a generic first impact with a wall.
- **Approach 5:** A compactness attempt and an exact stationary micro-bump obstruction. At ε=c h², globally minimizing proximal bumps have particle barycenters that remain fixed, and the stationary limit fails the porous-medium equation. Here δ_N²/ε stays positive, so this does not contradict the sufficient scaling in Approaches 2–4.

One prior whole-space approach plus these four substantive continuations accounts for **5/5 author approaches**. Source retrieval, diagnostic checks, audits, and packaging are not counted as approaches. The prior approach's artifact is not included or reconstructed in this packet, and no acceptance of it is implied.

## Unresolved scope

The packet does not prove convergence for arbitrary finite-energy weak solutions, degenerate or waiting-time interfaces, merging supports, singular free boundaries, generic wall impact, or a Dirac initial state at time zero. The compactness route still needs control of the projected transport covariance and nonlinear pressure identification under the intended small-error scaling.

## Contents and verification

The four manuscripts are preserved at their exact submitted review hashes. Source verification metadata identifies the exact OWR and arXiv versions, with public URLs, PDF byte counts and hashes. Raw scholarly PDFs, source text, corpus contents, private coordination records, and earlier artifacts are excluded.

Two supplementary scripts check algebraic identities and finite examples. Their recorded normal, optimized, and isolated-relocated runs passed; targeted mutations were detected. These diagnostics are neither a formal proof verifier nor a numerical PDE convergence study. No repository publication or queue edit is represented by this author packet.
