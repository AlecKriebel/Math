# Result: complete criterion as a classical consequence

**Recommended status: already_solved. Substantive author turns: 1/5.**

For every prescribed generic immersed parametrized circle gamma in a closed
connected oriented surface S_g, an allowed proper stable disk extension in some
compact 3-manifold with exactly that boundary exists if and only if

`corank(pi_1(S_g)/<<gamma>>) = g`.

The proof includes nonorientable candidate fillings, all genera, and a fixed
parametrized boundary. Razborov’s published algorithm computes the maximal
free-image rank of the explicit coefficient-free equation system, so the
criterion gives a terminating yes/no procedure for every finite combinatorial
input. This is a full prescribed-curve existence criterion, beyond merely
producing a counterexample to universal existence.

The complete proof is [CORANK_CANDIDATE.md](CORANK_CANDIDATE.md), unchanged at
SHA256 `e86a939d63d618cd7cafccf9b0ba1f847970aa319f990517d9e592b5f756d020`.
A separate reviewer returned [full PASS](corank_independent_review/FINAL_REVIEW.md)
for that exact version, with no mandatory correction.

## Credit and limits

- This is an application of established results, especially Carter’s
  handlebody reduction, maximal-rank surface epimorphism realization, and
  Razborov’s rank algorithm; no new-algorithm or historical-priority claim
- The literal universal affirmative reading was already false by Carter 1991
- This does not classify all virtual-string cobordism classes
- No practical implementation or favorable complexity bound for the general
  rank algorithm is provided
- Author finite controls pass 6,185 assertions; independent controls pass
  6,881 checks. These are encoding/edge-case controls, not a corank solver
- The audit is independent AI review, not human peer review
- Carter and Razborov primary texts were readable, but local facsimile access
  limitations are retained in the source manifests and full review

Earlier source-only notes, imported open-status metadata, and pending-review
headers are preserved as clearly labeled history. This file and the full
independent review state the current outcome.
