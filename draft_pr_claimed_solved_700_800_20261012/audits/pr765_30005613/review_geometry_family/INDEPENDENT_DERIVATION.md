# Independent geometric/form derivation — initial position

Recorded 2026-10-16T04:42:23.601874+00:00. Input read before this checkpoint: root AGENTS.md, queue AGENTS.md, immutable author PROOF.md, selected_record.json. No inherited audit report/verdict, README assessment, or new-family work has been read. Initial audit completion estimate: 20%.

## Exact hypothesis

The candidate is existential in cube half-widths and positive interface apertures, for each d>=2. It seeks a connected open quasi-conical domain with complete Dirichlet eigenbasis, full essential spectrum [0,infinity), and no continuous spectral subspace. Source compatibility remains to be checked independently.

## Initial reconstruction (not a source-based endorsement)

Adjacent cubes meet at x_1=p. For delta smaller than both half-widths, the two open half-cubes of Q_delta(p) already lie inside the neighboring cubes. Only its middle (d-1)-dimensional face is added. The union is open because the entire connector cube is open; it joins the two components because it has open overlaps with both. Thus all finite-window L2 spaces coincide modulo null sets.

For a finite stage choose a containing bounded box B. Zero extensions of H_0^1 of every domain are closed subspaces of H_0^1(B), so compact Dirichlet resolvents follow from compact embedding on B without any slit-boundary regularity.

Let V_delta=H_0^1(D_delta), embedded by zero in H_0^1(B). The spaces decrease with delta. I expect intersection_delta V_delta=H_0^1(D_0). Here is a direct mechanism: for bounded u in the intersection, multiply by a smooth radial cutoff vanishing near p and equal to one away from p. Choose delta with the connector fully inside the zero neighborhood. Approximate u in H_0^1(D_delta) by smooth compactly supported functions and multiply by the cutoff; their resulting supports are compact in D_0. The cutoff energy tends to zero because a point has zero H1 capacity. For d>=3 the transition from radius r to 2r has energy O(r^(d-2)). For d=2 use inner radius r^2 and outer radius r, with logarithmic transition: energy 2*pi/log(1/r). The cutoff products converge to bounded u in H1. Truncate arbitrary u first, using Lipschitz Sobolev truncation, then pass to the limit. Previously opened windows are entirely unchanged by this local removal argument.

A bounded-energy weak limit of u_delta belongs to every fixed V_s, hence the intersection. Conversely each v in H_0^1(D_0) belongs to every V_delta, giving the Mosco recovery sequence v_delta=v. Variational uniqueness then gives strong convergence of the +1 Dirichlet resolvents. Their unit-ball images lie in a fixed bounded ball of H_0^1(B), hence are collectively compact. To obtain norm convergence directly, if f_j is a bounded sequence and delta_j->0, pass to f_j weakly converging to f and R_delta_j f_j strongly converging in L2 by compactness. Its variational limit is R_0 f. Compactness also gives R_0 f_j->R_0 f. This contradicts any persistent positive operator-norm discrepancy. This argument needs to be written carefully, but presently no missing central analytic claim is apparent.

The infinite-domain form exhaustion has a separate elementary proof: C_c^infinity(O) functions have support in one O_N by the finite-subcover property of an increasing open cover. Hence the union of H_0^1(O_N), zero extended, is dense in H_0^1(O). Variational solutions are energy-orthogonal projections and converge strongly. It does not require convergence in norm on the infinite domain.

For spectrum as a set, cutoff plane waves supported deep inside pairwise disjoint growing cubes lie in the actual Dirichlet operator domain, have residual O(r^-2+sqrt(lambda)/r), and are orthonormal/weakly null. Nonnegativity then gives spectrum=essential spectrum=[0,infinity). Infinite volume and connectedness rule out an L2 zero mode.

## Open checks at this checkpoint

1. Read exact primary source propositions and verify their versions/hypotheses, including d=2 and boundary behavior.
2. Check the original open question actually permits cube-size freedom.
3. Expand the intersection/Mosco proof to make support and bounded-truncation details explicit.
4. Independently cross-check the finite-rank completeness argument; no verdict yet.
5. Produce checkable diagnostic controls and exact provenance receipts; then final closure.
