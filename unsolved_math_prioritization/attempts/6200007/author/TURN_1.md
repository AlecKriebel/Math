# Attempt 1: remove elementary and countability obstructions

Problem 6200007 / AMR-061-0007, rank 548. Author work, 2026-10-04.

## Target and convention

The question asks whether a minimal convergence action of a group G on a compact
metrizable space Z is induced by a uniform quasi-action on a hyperbolic space
having boundary equivariantly homeomorphic to Z. Here minimal means that every
orbit is dense. The primary source calls this “topologically transitive” but
explicitly gives the stronger, every-orbit-dense definition. We use that explicit
definition. Proper discontinuity on triples means that every compact subset K
of the distinct-triple space has only finitely many g with gK intersecting K.
No finite-generation or faithfulness hypothesis is added.

## Proposition 1.1: the finite cases have exact isometric realizations

For a nonempty finite Z, take a metric tree consisting of one ray for each point
of Z, all initial endpoints identified. Permute rays using the given action,
preserving their distance coordinates. This is an exact isometric action, and
its end boundary, with its natural G-action, is Z. A geodesic ray eventually
lies in exactly one arm, so the boundary identification is a homeomorphism.
For an empty Z take a one-point metric space. It has empty Gromov boundary.
The trees are 0-hyperbolic. Thus even an infinite kernel in the one- or two-point
cases causes no problem: the question does not require a proper interior action.

## Proposition 1.2: in the remaining case Z is perfect and G is countable

If p were isolated, its orbit would be open and invariant. Its complement would
be a closed invariant set. Minimality would force that complement to be empty.
Thus every point of Z would be isolated. Compactness would then make Z finite,
a contradiction. Hence an infinite Z is perfect.

Fix a compatible metric d on Z and a triple t of distinct points. The compact
sets

K_n = {(x,y,z): min(d(x,y),d(y,z),d(z,x)) >= 1/n}

exhaust the distinct-triple space. For each n, C_n = K_n union {t} is compact.
If gt belongs to K_n, then gC_n intersects C_n, so there are only finitely many
such g. Every g occurs for some n. Consequently G is countable. The stabilizer
of t, and therefore the kernel of the action on Z, is finite, by applying proper
discontinuity to {t}. Finally G must be infinite, since every orbit of a finite
group is finite and closed and could not be dense in an infinite Hausdorff space.

## What this attempt does and does not establish

This eliminates elementary spaces, uncountability, isolated points, and infinite
kernels as potential obstructions in the infinite case. It neither supplies a
compatible hyperbolic geometry nor makes the triple quotient compact.
The general problem remains unresolved.

Checkpoint: approximately 5% toward the universal target, a subjective research
estimate rather than a probability. The elementary subcase is complete.
