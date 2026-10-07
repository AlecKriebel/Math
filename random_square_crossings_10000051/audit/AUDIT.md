# Independent mathematical audit: problem 10000051

## Verdict

**ACCEPT AS RIGOROUS PARTIAL WORK AFTER THE THREE SMALL REPAIRS BELOW. NOT A SOLUTION.**

The finite geometric and probabilistic results survive independent checking. Neither the universal fixed-direction lower bound at fair coloring nor convergence to one half as the largest tile shrinks is proved. No assertion about all countable tilings follows merely from the finite results.

The audit binds to original manifest SHA-256 `d7e9b428572aa3864071d8e9bba50732afa6606586a4f1aa5250ada59ea24736` and original candidate SHA-256 `9db9ae5f8cfc0d05239e117c813a05ad6806c322f30b57637b8ed408fc906afd`. All eleven manifest entries match their recorded sizes and hashes; there are no unmanifested files in that public packet. The original packet was not changed. `CORRECTION.patch` is an actual, application-tested unified diff. `CANDIDATE_CORRECTED.md` is the corresponding complete corrected mathematical text.

## Required repairs

1. **Probability-measure quantifier, Proposition 7.2.** The original almost-sure alternative refers to the “chosen product coloring,” but the proof later uses fair marginals without specifying this in the hypothesis. State the almost-sure alternative under independent fair colors and explicitly assign independent fair colors to extra tiles. The conclusion is then P_(T,1/2)(H_fin) >= c. An arbitrary-p reading is unjustified: an all-white one-square tiling satisfies the geometric approximation and the crossing alternative while its black crossing probability is zero. This is a scope clarification of the intended fair-color transfer; it does not supply either missing approximation hypothesis.

2. **Strength of the Boolean control, Section 4.** AND has P_b=b^N, so it does not keep the high-density probability bounded below as N increases. It refutes simple multiplicative comparisons, but does not by itself demonstrate the stronger obstruction relevant here. Replace it with the event that at least ceil(alpha N) bits are black, where 1/2 < alpha < b. The patch proves by Chebyshev that its fair probability tends to zero and its probability at b tends to one. This remains a Boolean logical control, not a square-tiling construction.

3. **Fail-open verification under optimization.** Both supplied scripts put their validations in Python assertions. With `python3 -O`, an intentionally wrong influence in the stored results is accepted and the rational verifier still prints PASS; ordinary execution rejects it. The patch makes both scripts stop immediately under `-O` or `PYTHONOPTIMIZE=1`. Normal-mode result bytes remain unchanged. The additional independent audit script uses explicit exceptions, not assertions, and passes identically in normal and optimized modes. It rejects a one-byte frozen-file mutation in both modes.

None of these changes alters 65/128, 63/128, unit extremal length, Peled's parameter, the dyadic estimate, or the unresolved status.

## Primary-source and model audit

The primary [Benjamini manuscript](https://arxiv.org/abs/1510.05196), Conjecture 2.2 on PDF page 3, asks for a positive absolute lower bound with independent fair colors on an arbitrary prescribed square tiling. It permits infinitely many tiles and imposes the no-fourfold condition. It does not contain the asserted small-mesh limit in Conjecture 2.2 itself.

The [archived author slides](https://arquivo.pt/noFrame/replay/20201231041529id_/http://www.wisdom.weizmann.ac.il/~itai/conformaltalk1.pdf) do contain both targets. Their actual PDF pages 22 and 23, zero-based indices 21 and 22, are successive animation frames. The conjecture is faint on page 22 and fully visible on page 23. Direct visual inspection of the hash-matched PDF confirms that the largest-square limit is one half. The audit's web request for the archive failed; this does not invalidate the inspected local PDF or establish a fresh download. The slides' title page dates the talk October 2015; embedded PDF creation metadata dates September 2015, which is not a contradiction.

[Benjamini–Kalai, Conjecture 2.1](https://msp.org/memocs/2018/6-2/memocs-v6-n2-p01-p.pdf), independently confirms the arbitrary-tiling fair-color lower-bound scope. No distribution on tilings may be introduced into either target. Transposition-invariant random tilings give a separate annealed observation only. [Quenched Voronoi percolation](https://arxiv.org/abs/1501.04075) addresses a random tessellation and does not supply a bound for every deterministic square tiling.

Conventions in the candidate are adequate for its finite theorems:

- Tiles are closed, positive-size, axis-parallel squares, contained in the closed unit square, with pairwise disjoint interiors and exact coverage.
- Tile adjacency is nonempty geometric contact; no-fourfold finite tilings have no corner-only tile pairs, so side-contact adjacency agrees.
- Independent black/white states are assigned to whole tiles. “Open” in percolation terminology is a retained state, not the topological interior of a tile. Replacing closed tiles by disjoint open interiors would change connectivity.
- Boundary colors are free. The four artificial terminal colors in the Hex proof only encode which event is tested and do not force colors on boundary tiles.
- The finite model excludes zero-size tiles, overlapping interiors, gaps, and fourfold meetings. A packing with gaps is expressly used only where exact coverage is unnecessary.
- Axis alignment is explicit throughout the mathematical claims. No extension to arbitrary countable tilings with differing orientations or unspecified accumulation conventions is asserted.

The searched primary literature did not reveal a resolution of the exact targets. This is a bounded-search finding as of 2026-10-07, not proof that no resolution exists. Peled is verified as arXiv:2001.10855v1; this audit does not certify a peer-reviewed publication of that manuscript.

## Section-by-section mathematical findings

### 2. Finite Hex duality and the asymmetric example: PASS

A finite square tiling with no fourfold point has a contact graph that becomes a triangulated disk after adding the four side terminals. At interior T-junctions, all three tiles are mutually side-adjacent; the boundary fans and corner triangles supply the other triangular faces. Bichromatic interfaces have four outer endpoints and no interior branches. Planar pairing leaves either a black left-right bank or a white top-bottom bank. Two monochromatic paths between alternating terminal pairs cannot be disjoint in this disk, establishing exclusivity. Thus q_T(p)+v_T(1-p)=1. At p=1/2 the result is a sum identity, not equality of the summands.

The seven-square coordinates have exact coverage, no overlap and maximum incidence three. Independent union-find enumeration, not the packet's bit-frontier algorithm, verifies all 128 colorings. The coefficient counts are exactly:

- H: (0, 0, 1, 13, 24, 19, 7, 1)
- V: (0, 0, 2, 11, 22, 20, 7, 1)

The direct conditional formula is correct in both states of central tile D. Its ordinary power expansion is

q(p) = p^2 + 8p^3 - 18p^4 + 15p^5 - 6p^6 + p^7.

This yields H=65/128 and V=63/128. All eight square symmetries were checked: direction-preserving variants retain 65/128 and transposed variants give 63/128. The example only disproves exact equality for every fixed finite tiling. Its mesh is fixed.

A further independently constructed admissible 13-square control replaces tile A by a scaled copy of the seven-square pattern. All 8192 colorings give H=1063/2048 and V=985/2048. Its maximum mesh is still 1/2, so this control likewise says nothing against the source small-mesh limit.

**Necessary-hypothesis adversary.** In a 2-by-2 four-tile checkerboard, corner adjacency allows both a black horizontal and a white vertical crossing. With side adjacency, neither occurs. This demonstrates why the no-fourfold assumption cannot be omitted from this version of Hex duality or replaced by an unspecified convention.

### 3. Vertex extremal length: PASS

For the side-length metric, the projection of a connected crossing covers the full horizontal interval, so path length is at least one. The sum of squared side lengths is one. For every competing nonnegative metric, almost every horizontal line encounters a simple adjacent path and has total metric length at least the minimum crossing length. Integration gives the linear functional sum rho(t)s(t); Cauchy–Schwarz bounds it by sqrt(A(rho)). Both bounds are attained by rho=s. Vertical symmetry gives the other direction.

This is a direct quadratic variational proof. No unproved LP strong-duality theorem, interchange of infinite optimizations, or uniqueness assertion is used. The horizontal-line distribution also supplies an exact finite certificate: each tile is included with probability s(t). The proof handles arbitrary finite mesh and does not require the no-fourfold hypothesis. On a rectangle of width W and height H, the same derivation gives VEL_H=W/H and VEL_V=H/W; the independent 2-by-1 control returns 2 and 1/2. This checks the normalization.

Equality of the two VEL values cannot be converted into equality of crossing probabilities: the seven-square tiling already has VEL_H=VEL_V=1 with unequal probabilities. A geometry-sensitive theorem relating these invariants to Bernoulli crossings is still missing.

### 4. Influences and transfer in p: PASS after stronger logical control

Russo differentiation and variance tensorization have the stated normalization. The fair influence vector is (23,23,7,33,7,7,7)/64 and its sum is 107/64. These are verified by pairing configurations differing in a single coordinate, and the derivative of the exact polynomial agrees.

The differential inequality is a lower derivative bound. Integrating it cannot furnish a positive earlier probability from a later lower bound; the direction has not been reversed. The maximal likelihood ratio (2b)^N and its second moment [2(b^2+(1-b)^2)]^N are correct for b>=1/2. Their exponential dependence on N is indispensable to these arguments. The threshold-function correction isolates the lack of a general dimension-free implication even if the probability at b tends to one. No influence decay, noise sensitivity or conformal invariance for arbitrary fine tilings is established.

### 5-6. Peled dependency and quantitative consequences: PASS

[Peled's manuscript](https://arxiv.org/abs/2001.10855), Theorem 2.13, equation (7), applies to finite or countable regular packings, uses nonempty contact and finite retained-set chains, and measures ambient set-distance and diameter in the sup norm. A positive axis-parallel square has diameter its side length and satisfies the regularity condition with epsilon=1. Section 3, equation (8), explicitly gives exp(-26) for square packings. Section 8.6 warns that closure-based connectivity is a different question. The theorem is a credited external input, not independently reproved in this audit.

The candidate's reduction from that input is correct:

1. A finite crossing witness has a largest tile. Choosing any one in a tie suffices.
2. The dyadic class (2^(-k-1),2^(-k)] contains at most 4^(k+1) squares by disjoint area.
3. If D=2^(-k), k>=6, an endpoint tile on at least one boundary is at sup-norm set-distance at least (1-3D)/2>1/4 from the selected tile. The two signed lower bounds used in the proof are valid even if one is negative.
4. The entire witness belongs to the packing of tiles no larger than D. Peled therefore supplies exp(-2^(k-2)); using an upper bound for the actual supremum diameter weakens the estimate in the correct direction.
5. The resulting series has successive ratio 4 exp(-2^(k-2)). Replacing e by 2 gives exactly R_K=4^(K+1)/(2^(2^(K-2))-4). In particular R_6=4096/16383<1/3, and R_K tends to zero.
6. Conditioning all tiles larger than 1/64 to be black costs at most the factor (1-exp(-26))^4096. Small-tile colors remain independent with their original law. This proves the stated c_0 and the fine-mesh crossing-to-one limit using finite Hex duality.

The Bernoulli-inequality lower estimate on c_0 is valid. The bound on large tiles is deliberately loose but sufficient. The proof extends monotonically upward in black density only. Its parameter p_0=1-exp(-26) cannot be lowered to 1/2 by monotonicity or by the preceding derivative inequality. The square-packing result does not provide exponential decay at every rare-color density below 1/2.

### 7. Countable statements: PASS with fair-measure repair

The finite-chain event is measurable because it is a countable union over finite witnesses. The cutoffs s(t)>=1/m are finite by area and increase with m. Every finite witness eventually belongs to a cutoff. Thus the increasing-event exhaustion and convergence of probabilities are exact, even for packings that do not cover the square.

The rare-white-crossing bound transfers to these finite-chain events. The proof does not need a planar dual, full coverage, local finiteness or no-fourfold contact. It supplies only an upper bound on W_fin. The inequality P(H_fin)+P(W_fin)<=1 under the no-fourfold convention has the wrong direction to turn this into a lower bound on H_fin.

A cutoff is generally a packing with holes. A limiting path in arbitrary completions need not stabilize to a finite witness in the original collection. Nor is a connected closure automatically a finite-chain component or even path-connected. Accordingly, the candidate correctly leaves the infinite Hex alternative and stable finite-completion property unproved. With fair colors explicitly stated, Proposition 7.2's proof is sound: a finite witness persists in every sufficiently late completion, so the black crossing indicators converge almost surely, and bounded convergence applies. Extra-tile colors may be defined on one countable product extension; no independence between different n is needed.

## Independent computational coverage

`checks/independent_audit.py` is read-only on the frozen packet and uses exact integers and rational arithmetic. It verifies:

- all eleven original file hashes, byte counts and the complete public-file inventory;
- seven-square geometry, both reliability count vectors, the direct Boolean formula and influence vector;
- all eight reflected/transposed variants and the admissible 13-square refinement;
- the exact line occupation and shortest side-metric certificates;
- every integral square tiling of square boxes of side 1, 2, 3 and 4: respectively 1, 2, 6 and 40 tilings, 49 in total;
- VEL certificates for all 49, plus all colorings of the eight admissible tilings among them, 520 colorings in this census;
- rejection of zero-size, overlapping, gapped, out-of-box and fourfold geometries;
- both fourfold checkerboard convention adversaries, and the rectangular normalization control;
- exact dyadic constants for K=6 through 10 and endpoint separation.

Normal and optimized independent runs produce identical JSON. The original scripts reproduce their frozen results normally. The corrected scripts do likewise and fail closed under both optimization entry points. The unified diff was applied to a clean copy and the resulting files matched the intended corrected bytes. These finite checks support, but do not replace, the general written proofs.

## Exact remaining gaps and acceptance boundary

The accepted material consists of finite duality, the explicit asymmetric examples, deterministic unit VEL, finite-size interpolation identities, the high-density consequence of Peled, and carefully qualified countable finite-chain results. Five substantive approaches are recorded in the original ledger; this audit and its repairs are verification, not additional attempts.

Still absent are:

1. A uniform strictly positive horizontal crossing bound at independent fair coloring for every finite admissible tiling.
2. A proof that those fair crossing probabilities tend to one half for every admissible deterministic sequence with vanishing maximum side length.
3. A specified countable crossing convention and a universal argument that resolves the source target under that convention.

No novelty or priority is claimed for Peled-dependent consequences. No numerical sample is presented as proof. This source-free audit packet contains authored audit/correction material, exact checks, and public source metadata only; it contains no source PDFs, source text extracts, dataset contents or private coordination material.
