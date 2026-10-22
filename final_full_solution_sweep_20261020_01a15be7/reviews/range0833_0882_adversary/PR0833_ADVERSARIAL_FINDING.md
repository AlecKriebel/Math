# PR833: adversarial verification of the rejection

Frozen head: `0e6e23213494ecb4a7208f920d25d7b49502a5cb`. Problem 30003711 / OWR-15987-022. Review dated 2026-10-21 UTC.

The correct disposition is **full solution not verified; preserve the ordinary section-genus upper bound at most eight**. The precise remaining obligation is a checkable lower bound at least eight for the nine-flex cover over the smooth cubic coefficient space. This finding does not prove a smaller genus or falsity of the final journal theorem.

## Claim, category, and exact dependency

The frozen author PROOF.md concerns X = CP^9 minus the cubic discriminant and Y = {(F,p): p is one of F's nine flexes}. Its ordinary unnormalized genus counts open domains carrying one continuous section; the domains may be disconnected. Normalization subtracts one. Connected domains trivializing the whole nine-sheet cover are a different, stronger original formulation explicitly left open in that packet.

The author's own work constructs an eight-domain upper bound. Its equality claim imports Chen–Wan arXiv:2306.17303v2, Theorems 1.2/4.1. The lower-dependency sections of both historical audit manuscripts explicitly import this input rather than supply a separate lower proof. The later source addenda likewise disclose that they inspected v2 and did not obtain the final journal body. No independent matching lower proof is hidden in these acceptance labels.

I was supplied the proposed objection before this review. This is an adversarial verification of that objection, not a claim of blind rediscovery or a new independent approach family. I checked the actual v2 text: Proposition 4.2 names the principal K-cover PU(3) -> PU(3)/K and constant F3 degree-seven cohomology. The source then pulls the flex cover back along the Fermat orbit to obtain this cover. Thus the objection uses the same map and coefficient category as the inspected detector; it does not substitute the projective moduli quotient for X.

## Direct verification of the entire-map vanishing

Let omega be a primitive cube root, A the three-coordinate cycle, and B=diag(1,omega,omega^2). Both have determinant one. The exact monomial action of omega^t A^a B^b is

    e_j -> omega^(t+b*j) e_(j+a),  a,b,t,j in F3.

Consequently the actual inverse image H of K=<[A],[B]> in SU(3) is the 27-element group

    (a,b,t)(d,e,s)=(a+d,b+e,t+s+bd).

Its scalar kernel is its center and commutator subgroup, so H_ab=K=C3^2. Since SU(3) is simply connected, M=PU(3)/K=SU(3)/H has fundamental group H. The universal H-cover, followed by H -> K, classifies the actual K-cover PU(3) -> M: quotienting SU(3) by the scalar kernel gives PU(3). Hence the characteristic map c:M -> BK factors through BH and induces an isomorphism

    c*:H^1(BK;F3) -> H^1(M;F3).

This finite-lift argument remains valid although the source also factors through a topological U(1) central extension in U(3). Both factorizations classify the same K-bundle; replacing H by a split group would classify the wrong lift.

Let u(a,b)=a and v(a,b)=b, and f(a,b,t)=t-ab. For the usual trivial-coefficient inhomogeneous coboundary,

    delta f(g,h)=f(h)-f(gh)+f(g)=a(g)b(h).

Thus inflation sends uv to zero and c*(uv)=0. Independently coded monomial-matrix and cochain checks cover all 729 ordered pairs, with no failures. Negating f, replacing it by zero, and replacing the extension by the split law each fails on 324 pairs. These are targeted finite controls of the actual algebra, not a machine proof of topology.

The constant-coefficient ring is H*(BK;F3)=Lambda(u,v) tensor F3[x,x'], with x,x' in degree two. Each degree-seven class is uP_3(x,x')+vQ_3(x,x'). Multiplication by either degree-one generator is zero or a multiple of uv. Its image therefore pairs trivially with every class in H^1(M;F3).

The manifold M is connected, closed, oriented, and real eight-dimensional. Finite right translations of SU(3) preserve orientation because SU(3) is connected. Poincare duality over F3 makes H^7(M) x H^1(M) -> F3 a perfect pairing. Surjectivity on H^1 now forces

    c*:H^7(BK;F3) -> H^7(M;F3) = 0.

The pairing is on compact M, not on noncompact X. The conclusion concerns the entire constant-F3 degree-seven map, rather than only the particular polynomial printed in the source. It therefore survives correction of the primed/unprimed Leary transcription. No claim about twisted coefficients is being smuggled into this conclusion.

## Repair boundaries and disposition

| Route | Evidence and status | Exact remaining gap |
|---|---|---|
| Eight-domain geometry | Author construction and separate prior topology/group audits support upper <=8; retained as useful partial work. | Does not supply lower >=8. |
| Inspected v2 detector | Direct extension/cup/duality argument above annihilates its entire stated map. | Cannot certify its claimed lower bound by that detector. |
| Normalization, alternate constant-F3 degree-seven polynomial, printed ring typo | Same base/map and whole-map vanishing. | These changes do not repair nonvanishing. |
| Final 2025 journal version | Distinct publication and later revisions; body not inspected. Verified retrieval evidence contains gate HTML rather than the final proof. | A checkable final replacement proof may exist; its truth is not adjudicated here. |
| Twisted coefficients, other test space, geometric lower bound | Potential materially different mechanisms, but no concrete proof was supplied or recovered in the bounded evidence. | Unsupported nonvanishing merely transfers the central difficulty; blocked pending new evidence. |

The official arXiv version history freshly read during this review still identifies v2 dated 21 July 2023 and the separate 2025 journal DOI. It does not authenticate the final proof body. The two fresh sealed topology/source reviews, 21 and 62 payloads, were reauthenticated byte for byte; no sealed program was executed in place. The 28 original files and all three original archives/21 members match the frozen Git head and manifests.

The historical PR row is claimed_solved. The current main row is queued, but that does not erase the historical claim or constitute a withdrawal of that claim at the frozen head. The existing closed/unmerged state and closure comment 6185756578 match this exact lower-bound gap. No additional closure, comment, DOI, manuscript, or ledger row is needed for this bounded disposition.

The root's authenticated 197-record/eight-page account capture was independently rescanned for exact IDs, aliases, PR reference and flex/genus terms. It has 197 unique record IDs and no matching own publication; the fresh 178-row GWS read has no matching ledger row. This rescan was not a separate reauthentication of the account and is not worldwide priority evidence. A new full priority certificate would be premature while correctness remains unverified.

Primary references: [Chen–Wan v2](https://arxiv.org/pdf/2306.17303v2), [official history](https://arxiv.org/abs/2306.17303), [distinct journal DOI](https://doi.org/10.1090/proc/17184). This is extensive AI-assisted verification, not conventional human peer review or formal proof-assistant certification.
