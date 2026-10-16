# Source-first independent reconstruction

UTC: 2026-10-15T11:28:52.172Z
Best-guess audit completion: 20%.

## Independence boundary
Read only the exact whole_record.json target, Thorisson's original Some Open Probability Problems (text, Section 4), and Last–Thorisson 0906.2062 (text, Sections 2/3 and 6/7 relevant definitions). No authored proof, root memo, previous verdict, auditor output, code, other problem attempt, or later literature report has been read. PDF byte hashes are recorded; the typeset PDFs have not yet been visually inspected.

## Exact source hypothesis
The target is Problem 4.1, not the separate Markovian-kernel Problem 4.2. For a diffuse, locally finite random measure xi on a locally compact second countable Hausdorff Abelian group G, with a jointly measurable G action on the state carrying X and xi, does invariance of the rooted law under every measurable equivariant xi-preserving allocation imply mass-stationarity? The forward direction is the allocation special case of the Palm transport identity. An allocation is tau(omega,s)=s+pi(theta_s omega), with covariance pointwise for every omega,s,t. Preservation is pushforward of the spatial measure xi, not invariance of the rooted state law; noninjective measurable allocations are permitted.

Mass-stationarity is the FULL joint law (theta_V omega,U+V) =d (omega,U): U Haar-uniform on any relatively compact positive-Haar continuity set C, independent of omega, and V conditionally drawn from xi in C-U. Nonzero xi is required. A counterexample to the marginal state-law equality already disproves the full equality; merely verifying a marginal equality would not prove it.

## Independent falsification/reconstruction plan
First check whether stabilizers can make diffuse mass behave like indivisible quotient atoms. Candidate independent construction, BEFORE seeing the submitted proof: on G=R^2, take a deterministic measure consisting of horizontal lines, each carrying one-dimensional Lebesgue measure, with alternating line weights 1 and irrational c>0 on heights 2k and 2k+1. The state space is its vertical phase orbit R/2Z, with horizontal translations acting trivially, root law concentrated at phase 0. The spatial measure is diffuse and locally finite, although its quotient under horizontal translations is atomic.

Pointwise allocation covariance under every horizontal stabilizer forces the allocation restricted to each horizontal support line to be a horizontal translation onto a single horizontal line. Vertical period 2 forces the same behavior on translates. The xi pushforward balance may then force a weight-1 line to a weight-1 line, since irrationality rules out changing quotient mass type. If so the root phase remains 0 under all permitted allocations, while the mass-stationary sampling experiment can choose a weight-c line and produce a different phase with positive probability. This is a concrete potential negative answer for the universal LCA claim; it requires proving preservation at all quotient levels, including arbitrary noninjective allocations and off-support behavior. A compact product version may simplify the exact balance proof.

Falsification attempts: allow noninjective maps and multiple preimage lines; test whether merely a.e. covariance would permit exceptional root changes; test whether the source permits a free auxiliary X which could break the stabilizer (a counterexample may set X trivial); distinguish invariant measure from root law; inspect whether a.e. preservation on a root-law support is sufficient; check support and positivity for every sampled box; test c=1, rational c, support-full/dimension variants only as boundary diagnostics. A valid universal counterexample needs only one permitted group and one pair, not all groups.

## Success criteria and exact remaining checks
PASS requires a complete checkable counterexample meeting the precise original hypotheses and all allocation quantifiers, a measurable state/action and random-measure map, diffuseness/local finiteness, proof of rooted invariance for every allocation (including noninjective), and an explicit positive-probability event contradicting the full mass law. FAIL requires a concrete excluded assumption, admissible allocation that changes the law, or failure of the claimed mass-law counterevent. Repair is reserved for a proof gap that can be corrected within the same exact claim. No novelty or priority inference follows from mathematical validity.

## Source input pins

```json
{
  "private_native/whole_record.json": {
    "sha256": "a2f0c5917b4a427939601986a00056dacaa7dc3b4d6a83b37519d1f363aae6fd",
    "bytes": 2609
  },
  "private_sources/some-open-probability-problems.pdf": {
    "sha256": "efe6b6e78e36185a2b278ba0cf5593c2e92f43b479f80159d6f6b7ecc4f6efaf",
    "bytes": 107028
  },
  "private_sources/some-open-probability-problems.txt": {
    "sha256": "9dadc3fedfee0bb6ffd15f8601f6408d5bfe90deec6844298374b869b879805a",
    "bytes": 15658
  },
  "private_sources/0906.2062.pdf": {
    "sha256": "0a4c4813cef44e99c232d0687aa704554248675c621755be85568d0588999719",
    "bytes": 307591
  },
  "private_sources/0906.2062.txt": {
    "sha256": "641dcdf8895408c5fc5ceac017b254e40507baf9e11bafa2045f762663c522f9",
    "bytes": 69907
  }
}
```
