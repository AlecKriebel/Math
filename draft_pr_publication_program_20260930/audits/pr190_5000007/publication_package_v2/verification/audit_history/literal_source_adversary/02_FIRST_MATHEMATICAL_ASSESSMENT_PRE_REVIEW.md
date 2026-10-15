# First independent mathematical assessment -- PRE-REVIEW SEAL

UTC: 2026-10-14 05:24:19 UTC
Audit completion estimate: 75%.

Read barrier: this was written after reading PROOF_V2.md in full, CANDIDATE_PROOF.md in full, SIMPLIFICATION_NOTE.md in full, and the author half-turn checker's source. No original independent_review content, sibling report, or root mathematical opinion has been read. A root message supplied only primary-source paths/hashes and disk constraints, not mathematical opinions. File-name inventory exposed review names but not review contents.

## Initial verdict

The current PROOF_V2 theorem is a plausible correct proof of the explicitly defined parity-aware A0 exclusion, and I have found no gap in its central geometric mechanism. It is not a proof of the bare beta-alpha angle criterion, which is false. PROOF_V2 itself clearly admits this distinction; the earlier CANDIDATE_PROOF conclusion is less guarded when it says it resolves the source conjecture affirmatively, and must be read subject to its scope convention. The source contains an actual inconsistent shortcut, so a status such as unqualified solved needs the exact target sentence attached.

The literal-angle failure is not a speculative attack: the one-face diagonal counterexamples were found and sealed independently before candidate access. The candidate's assertion that there are exactly two added literal-angle paths for a fixed initial face/vertex is correct under the vertex-to-first-vertex convention. Here is a short exhaustive proof: N odd gives alpha+beta in (2pi/5)Z; beta-alpha=2pi/5 implies alpha in (pi/5)Z; the initial sector is [0,3pi/5], giving four rays; each already meets an initial pentagon vertex without reflection. Two are sides (distance 1) and two are proper diagonals (distance 2). N even is the specified corrected type. No unbounded trajectory enumeration is needed.

## Independently checked proof mechanism

1. Define p_j=sum_(t=0)^(j-1) r^t, q_j=sum_(t=0)^(j-1) r^(-t), r^5=1 and 1+r+r^2+r^3+r^4=0. P is counterclockwise and Q clockwise. Exact independent arithmetic establishes h(p_j)=1-p_j=q_(1-j mod5). Glue P edge j to Q edge -j by the translation taking q_-j to p_j; parallel side vectors are both r^j. On the glued edge h acts as t->1-t. All five edge midpoints are fixed and no open polygon interior can be fixed.
2. For an even number N of face occurrences, the terminal polygon is a translate of Q, whose outgoing ray at q_j has vector r^(-j). The Figure8 supplement, with clockwise terminal ordering, gives theta=alpha-beta mod2pi. Therefore corrected A0 fixes theta=-2pi/5, hence j=1, and terminal corner q1=h(p0). There is no need to invoke Fuchs's conjectured type-orbit equivalence.
3. h composed with parameter reversal sends the terminal Q corner q1 to the starting P corner p0, with the same interior direction since Dh=-I. This is equality of a specified corner germ at the singular point, not just equality of an unbased holonomy vector. Local straight-line continuation through regular points is unique until a vertex is reached. Hence sigma(t)=h(sigma(L-t)). The midpoint is regular by first-vertex admissibility and lies over an edge midpoint.
4. The covering maps are locally translations on open faces and open edges. Since all double-pentagon vertices are singular, and polygon decomposition vertices are exactly the source surface singular set, an interior point of the original short geodesic cannot project to a double-pentagon singularity. Thus the projected path really is a saddle connection. Its edge midpoint lifts to a physical edge midpoint of D.
5. The physical half-turn about the center/edge-midpoint axis reverses the intrinsic germ at that regular point. It is a local rotation by pi: in an intrinsic plane chart its derivative is -I. Unique geodesic continuation proves it exchanges the endpoint vertices even when the parameterized path self-intersects.
6. Distance-2 vertices have exactly one common neighbor because the dodecahedral graph has no 4-cycle. A half-turn exchanging such vertices would fix that neighbor, impossible because a rotational vertex stabilizer is cyclic of order3. This proof is independent of the author computational histogram and also excludes same-vertex endpoints.

The independent code in independent_double_pentagon_check.py uses only exact rational arithmetic in Q[r]/(1+r+r^2+r^3+r^4), imports no candidate code, and checks the full five-edge gluing/h action, terminal-corner uniqueness, and the four exceptional rays. It passed. The sampled edge parameters in its self-tests corroborate a linear identity, whose proof is given by the explicit formula h(t)=1-t; the samples are not promoted into a universal proof.

## Primary dependency authentication

Read AAH arXiv1811.04131v2 body Sections4.1--4.3 and5 in HTML. Proposition4.4 gives a translation cover from a surface decomposed into regular n-gons to the n/double-n polygon surface, respecting the polygon decompositions; Theorem4.5 specializes regularity to Platonic unfoldings. This supports exactly the map used above, without using any affine orbit enumeration or an unsupported lift of a Veech generator. Section5 defines virtual-Weierstrass saddle connections, the regular edge midpoint condition, and the half-turn mechanism. Theorem5.2 gives absence of closed virtual-Weierstrass connections for odd vertex valence, including the dodecahedron. Proposition5.3's every-connection assertion is only for triangles/squares and does NOT apply to pentagons. The candidate explicitly respects that boundary. The source mechanism is prior, and a novelty claim would need a separate audit of the added type/corner identification and the distance-2 graph argument.

## Remaining exact scope limits

- Literal-source and corrected-target statements must remain separate in every promotion. The face-diagonal exception is central to target truth, not a harmless textual edit. No claim of proving all unqualified beta-alpha=2pi/5 paths is tenable.
- Boundary paths: a nonzero first-hit path tangent to an initial edge is exactly that single edge; it has graph distance1. A non-edge geodesic cannot merely touch or run along an edge without coinciding with it locally, so its crossings are transverse and N-1 parity is well defined.
- Genericity: no irrationality, angular separation, bounded length, embeddedness, or no-return assumption is needed after the corner argument. The first-vertex condition is essential. Paths artificially continued through vertices are outside the claim and break the uniqueness/midpoint reasoning.
- The public 16-face witness and the author's reconstruction have not yet been independently checked by this adversary. Their details are unnecessary for the source-level face-diagonal counterexample or the corrected theorem proof.
- No formal historical-priority or current literature audit is claimed. No theorem is being called novel.

Artifact identities at seal:
- original PROOF_V2.md: SHA256 f96288e95c946731091989cea3eb087829c94cf966898dae792122567da3f16b
- original CANDIDATE_PROOF.md: SHA256 e12f714910e410332c0e028fa410f7157dbf17913a571bb462109e4d8b93a8c1
- original SIMPLIFICATION_NOTE.md: SHA256 71df3921d5b5f74217eecf276f44e543cc92551c4cd018b58f44582732913b11
- original check_half_turn.py: SHA256 3cbb9b90004f0f7e56acfbd8d03ae1ff3fc3d7aed089b49320c79ad226e69e43
- Fuchs shared PDF: SHA256 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d; identical temporary local copy deleted to conserve disk.
