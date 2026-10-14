# Final literal-source adversarial report for PR190 / 5000007

Completed: 2026-10-14 05:27:18 UTC
Relevant original head: 0c3346c8ebcb3b967a1d8bf9a283f027b44b738c.
Audit assignment completion: 100%. Novelty/publication readiness: not assessed.

## Verdict and target boundary

**The current PROOF_V2 establishes its explicitly stated parity-aware theorem. No mathematical gap was found in that theorem after independent source-first assessment, exact corner/gluing checks, and boundary attacks. The bare numerical angle formulation is false.** The two facts must remain separate in any queue status, abstract, or publication.

Fuchs's printed Conjecture3.2 is expressed using the symbol A0, with graph distance measured in the dodecahedral one-skeleton. Its full Section2 context supports the candidate's parity-selected reading: the paragraph before Definition2.1 chooses the angle sum or difference by the number N of straight pieces, and Figure9 calls pentagon sides A0 but its proper diagonals A1/A2. However, the p.506 standalone A0 difference shortcut contradicts that calibration in exceptional directions. This is a real source inconsistency, not a license to claim an isolated angle-only statement has been proved.

I certify the mathematical corrected theorem and the literal counterexample classification, not an affirmative resolution of every interchangeable rendering of the question. The exact imported dataset sentence was not retrieved by this adversary; its characterization as angle-only appears in original author notes and remains a target-identity item for the coordinator. If that is the campaign's literal target, its resolution is negative, by the face diagonals, while the positive theorem is a separately stated correction. The older CANDIDATE_PROOF conclusion needs this explicit scope caveat; current V2 supplies it.

## Independently sealed source result

Before reading the candidate, I found and sealed the direct-diagonal obstruction. Normalize the initial pentagon above its horizontal unit edge. Its proper vertex rays have angles alpha=pi/5 and alpha=2pi/5. With Figure8's supplementary terminal convention, beta is respectively 3pi/5 and 4pi/5. Both obey beta-alpha=2pi/5, and both are legal one-face geodesics with endpoint graph distance2. They have one straight piece, zero transverse edge crossings, and source Figure9 labels A2 and A1 (up to reflection), rather than A0.

More strongly, the claimed finite correction is exhaustive. For odd N, the source angle-sum rule combined with beta-alpha=2pi/5 forces alpha to be a multiple of pi/5. The permitted sector contains exactly four such rays: two sides and two proper diagonals. Each hits its first vertex in the initial face. For even N the bare difference rule is exactly the corrected interior class. Thus there are precisely two added literal-angle paths for each fixed initial face and vertex. No large-length search or generic-angle restriction is hidden here.

## Checked proof chain

Use r=exp(2pi i/5), p_j=sum_(t<j)r^t and q_j=sum_(t<j)r^(-t). P is counterclockwise; Q is clockwise. Independent exact arithmetic gives:

- h(z)=1-z sends p_j to q_(1-j mod5), so h(p0)=q1.
- P side j glues by translation to Q side -j; the side vectors coincide. On each glued side h sends parameter t to 1-t, fixing exactly its midpoint.
- A corrected interior A0 path has N even. Its terminal boundary direction is theta=alpha-beta=-2pi/5, and the unique clockwise Q corner with that outgoing direction is q1.

Consequently h composed with reversal of the projected connection has the same specified starting corner germ as the original. This is stronger than merely sharing an unbased vector at the common singularity. Straight continuation until the first vertex proves equality of the two parameterized connections. Their midpoint is regular, fixed by h, and lies on an edge midpoint; h has no polygon-interior fixed point.

The translation cover respects polygon interiors, open edges, and vertices. Hence the original no-interior-vertex condition prevents the projected path from meeting the double-pentagon singularity early, and an edge midpoint projects/lifts to a physical edge midpoint. The solid's half-turn about the center/edge-midpoint axis has intrinsic derivative -I there. It reverses the geodesic germ and, by continuation, exchanges its endpoint vertices.

The distance exclusion then follows without computation. A distance2 pair has a unique common neighbor, since two common neighbors would give a 4-cycle. Any involution exchanging the pair fixes that neighbor. A physical rotational half-turn fixes no dodecahedral vertex, whose rotational stabilizer has order3. Contradiction. This also recovers the already-known exclusion of equal endpoints for this midpoint class.

The code independent_double_pentagon_check.py imports no candidate module and checks the exact five-corner/five-side identities over Q[r]/(1+r+r^2+r^3+r^4). Its output reports success. It does not purport to test all trajectories; the proof uses the linear edge identity and geometric continuation. The author half-turn checker's source was read, but not executed here, because the graph argument is sufficient.

## Boundary and falsification record

| Attack | Result |
| --- | --- |
| Confuse N pieces with edge-crossing count | N-1 crossings, so corrected interior A0 has odd crossings. One-face diagonals have N=1 and zero crossings. |
| Apply p.506 difference shortcut to all directions | Falsified by the two face diagonals, independently before candidate access. |
| Exclude exceptional directions as genericity exceptions | Unnecessary and would change the target. The four exceptional rays are exhausted explicitly. |
| Ignore polygon sides | Source Figure9 includes them. A tangent starting ray follows that single edge to its first endpoint, distance1. |
| Allow an interior tangency to an edge | A straight geodesic tangent to an edge locally coincides with it and reaches a vertex; a non-edge first-hit path has transverse crossings. |
| Require embedded/simple paths | Unneeded: the physical argument uses a parameterized regular germ and continuation through regular points. |
| Continue past a vertex | Outside the short/saddle-connection convention and would invalidate the uniqueness argument. |
| Assume all pentagon connections are hyperelliptic-invariant | Not used; the specified terminal corner is essential. Proper face diagonals demonstrate the difference. |
| Import Fuchs's conjectural type/Veech-orbit equivalence | Not used. The local corner proof avoids this unsupported premise. |
| Deduce a universal claim only from finite trajectory samples | Not used. The computer artifact checks exact algebraic identities, and the rest is a proof. |

## Primary dependencies and prior-source limits

Fuchs primary final PDF was authenticated at SHA256 9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d. Relevant source pages and figures were inspected directly; the exact read/visual depth is in READ_DEPTH_LEDGER.md. The finite length120 and half-sector restrictions belong to his motivating experiment and do not limit Conjecture3.2.

Athreya--Aulicino--Hooper, arXiv1811.04131v2, supplies the polygon-respecting translation cover (Proposition4.4 and Theorem4.5) and the virtual-Weierstrass midpoint/half-turn mechanism (Section5). Its Theorem5.2 already gives absence of closed virtual-Weierstrass connections on the dodecahedron. Its Proposition5.3 all-connection claim is restricted to triangles/squares; no extension to pentagons is justified. Proposition9.1 also separates two unoriented affine connection classes; Section10.2.1 identifies the short class's midpoint mechanism and its absence of closed lifts. These were checked in primary body text, not inferred from titles.

This establishes substantial prior content behind the proof. The candidate's additional type/corner identification and the distance2 common-neighbor observation are the mathematical steps to examine in any later novelty audit. Neither historical originality nor current openness has been certified. The original LITERATURE_CHECK was read after my first mathematical seal, but its search completeness and later-source claims were not adopted as evidence.

The public 16-face certificate's source and geometry were not independently reconstructed by this adversary. I read the original author audit after sealing my assessment, and record its claims only as claims. No refutation or correctness judgment about that public certificate is part of this report. Its resolution is unnecessary for the elementary literal face-diagonal obstruction or the corrected theorem.

Primary URLs:
- https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf
- https://arxiv.org/html/1811.04131v2

## Independence, artifacts, and publication boundary

The source-only assessment and SHA receipt were set to actual 0444 modes before candidate access. The first mathematical assessment and exact independent checker/output were likewise sealed before any original review/sibling/root mathematical opinion. Original independent_review bodies remain entirely unread; root messages supplied assignment details, source locations/hashes, and disk limits only.

No Git/index/ref/branch/checkout command, candidate edit, external outreach, remote mutation, publication, or environment install occurred. The only download was the Fuchs primary PDF; its duplicate was deleted after byte equality with the shared source was checked. Only this adversary's dedicated folder was written. Source bodies, layout extraction, and rendered source pages stay private and are excluded from the authored-safe allowlist. The allowlist and final SHA manifest identify precisely the self-authored artifacts that may be incorporated into the coordinator's audit. No release or publication is initiated by this designation.
