# Research log for 30003813

## Source gate — 2026-10-03 08:20-08:25 UTC

**Author attempts used:** 0/5. **Estimated completion:** 10%.

Verified the source definition at printed OWR p. 1410, including the absence
of an explicit cyclic-order-statistic restriction. Checked the current queue
and accessible repository prior-attempt records. The original direct problem
page failed to load; the hash-verified authorized fallback and official report
agree on the exact mathematical target.

The AJR 2020 paper proves volume and integrality for this signed family, but
its stated h-star theorem is for a different consecutive-sum family. That
distinction prevents an incorrect prior-resolution claim. Stanley's
order-polytope/P-partition theory is the relevant classical framework.

## Substantive author attempt 1 — 2026-10-03 08:25-08:34 UTC

**Author attempts used:** 1/5. **Estimated completion of the literal
mathematical target:** 100% candidate; independent verification pending.

### Mechanism

Reflect the even coordinates, x_i -> 1-x_i. Every adjacent-sum inequality
becomes a directed comparison on the path. Its transitive closure is an
acyclic poset. The resulting polytope is its order polytope.

Fix any natural labeling, sort every integer order-preserving map first by
value and then by its label, and partition into linear-extension words.
Strict increases are required exactly at label descents. Subtracting those
strict steps gives the binomial lattice count and hence the descent
numerator of the Ehrhart series.

The final formula is explicit on the ordinary permutations with descent set
D = {odd i with sign +} union {even i with sign -}. For any alpha with that
same descent set, each sigma contributes
z^(des(alpha composed with inverse(sigma))).

### Complete artifact and boundaries

`PROOF.md` supplies the all-dimensions derivation, full dimensionality,
integrality, the dilation-dependent reflection, disjoint boundary handling,
and invariance under the choice of natural labeling. It includes dimension
one, both signs in dimension two, alternating signs, and a mixed-sign
nonpalindromic example.

There is no unresolved proof step in the author candidate. The external
review must still test the proof and scope. The formula is an application of
classical theory, with no novelty claim. It does not produce an additional
cyclic-order-specific statistic.

### Falsification checks

`verify.py` compares two different natural labelings and the descent formula
against integer dynamic programming in the original adjacent-sum
coordinates. The exact run covers every sign pattern through dimension 8.
It also checks every grid point through dimension 5, dilation 4, and an
intentional incorrect-label negative control.

The first checker run exposed an indexing error in the test harness:
dimension one's stored count list ended at m=3 while the grid loop went to
m=4. The harness was corrected to call the count function directly there.
This did not modify the formula or proof. The corrected run passed:

- 255 sign patterns
- 46,233 permutation words
- 2,558 Ehrhart evaluations
- 79,657 reflection checks
- 12,195 boundary tie-sorting checks

The negative control confirms that raw original vertex labels can give
2z instead of 1+z. Natural labeling is essential, not cosmetic.

## Freeze checkpoint — 2026-10-03 08:40 UTC

**Author attempts used:** 1/5. **Estimated completion:** 100% candidate;
fresh independent audit and publication decision pending.

Complete local proof and executable checks prepared for an uninvolved
reviewer. No additional author turns are claimed for source review,
formatting, test replay, or packaging. No remote publication occurred.

## Reviewed release — 2026-10-03 08:50 UTC

Independent audit PASS. The literal combinatorial interpretation is claimed
solved after 1/5 author attempts, as a classical corollary without novelty or
historical-closure claims. The audit required no mathematical repair. Its
optional constant-1 wording clarification is applied in this release, with
all other editorial changes recorded in RELEASE_CHANGES.md.
