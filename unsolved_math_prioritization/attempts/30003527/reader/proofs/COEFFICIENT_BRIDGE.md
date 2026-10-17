# Isolated finite-type subcase: coefficient bridge and exact movability

Target: queue row 1767, problem 30003527 / OWR-15575-006. Shared substantive pass 1, 13 October 2026. This is a partial theorem, not a solution of the unrestricted invariant-enlargement question. The underlying mod-2 theorem was already stated by J. J. Sánchez-Gabites in his 2016 AIMS abstract, “Some Constraints on the Topology of Isolated Invariant Sets and How They Sit in Phase Space.” Author abstract: https://aimsconference.org/conferences/2016/Abstracts-AIMS2016Orlando.pdf . No novelty is claimed. The argument below spells out the coefficient reduction and the movability consequence, using inspected 2024 primary-source results.

## Claim

Let K be an isolated compact invariant set for a continuous full flow on R^3. If Čech H^0(K; F_2) and Čech H^1(K; F_2) are finite-dimensional, then K is movable in the exact unrestricted neighborhood-homotopy sense of the target. In particular, for this subclass the target is satisfied with B = K, for every open U containing K.

All cohomology below is unreduced. Empty sets have zero groups in nonnegative degrees. All finiteness statements concern ordinary finite generation over Z or finite dimension over F_2. Disconnected compacta and surfaces are allowed.

## Primary inputs

J. J. Sánchez-Gabites, “Using an invariant knot of a flow to find additional invariant structure,” arXiv:2403.18805v1, 27 March 2024, https://arxiv.org/abs/2403.18805 .

- Section 5.4, pp.16–17: every isolated invariant compactum of a continuous flow on an orientable 3-manifold has arbitrarily small tame 3-manifold isolating blocks.
- Proposition 5(iii), p.6: for a block N with entry surface N^i and stable entry trace n^+, there is an isomorphism Čech H^q(N,K;G) ≅ Čech H^q(N^i,n^+;G). Its proof uses flow deformations, continuity, and quotient cohomology, so applies to Z and F_2 coefficients alike. No coefficient-dependent argument is used there.
- Theorem 10, pp.10–15, and its consequence on p.17: finite generation of integral Čech H^0(K), H^1(K) gives arbitrarily small regular isolating blocks.
- Theorem 16, pp.17–19: if Q is a regular isolating block, then Q\K is homeomorphic to ∂Q × [0,∞), with ∂Q corresponding to parameter zero.

Only these results are imported; the proof below does not infer shape equivalence merely from a cohomology isomorphism. The spine theorem supplies the necessary geometric information.

## Lemma 1: surface coefficient bridge

Let L be a compact subset of a compact orientable surface P. If Čech H^0(L;F_2) and Čech H^1(L;F_2) are finite-dimensional, then Čech H^0(L;Z) and Čech H^1(L;Z) are finitely generated.

Proof. Embed each component of P with boundary in its double, and retain closed components as they are. This gives a finite disjoint union S of closed orientable surfaces containing L. The case P or L empty is immediate.

Čech H^0(L;F_2) is the vector space of locally constant F_2-valued functions. Its finite dimension forces L to have finitely many components: in a compact Hausdorff space components equal quasi-components, and arbitrarily many distinct components can be separated by a finite clopen partition with arbitrarily many parts. The characteristic functions of those parts would be linearly independent. Thus H^0(L;Z) ≅ Z^c for some finite c.

Alexander–Lefschetz duality on S, followed by the relative singular homology exact sequence, gives for either coefficient group G the exact segment

H_1(S;G) → Čech H^1(L;G) → H_0(S\L;G) → H_0(S;G).

Here the middle cohomology group identifies with H_1(S,S\L;G). This holds for arbitrary compact L, not just submanifolds. With G=F_2, the two groups Čech H^1(L;F_2) and H_0(S;F_2) are finite-dimensional, hence so is H_0(S\L;F_2). Thus the open surface S\L has finitely many path components. Consequently H_0(S\L;Z) is a finite-rank free abelian group. With G=Z the displayed sequence now expresses Čech H^1(L;Z) as an extension of a quotient of finitely generated H_1(S;Z) by a subgroup of finitely generated H_0(S\L;Z). It is finitely generated. This includes L=S and empty complementary components. ∎

## Lemma 2: isolated-set coefficient bridge

Let K and the flow be as in the claim. Choose a compact 3-manifold isolating block N. Its entry part P=N^i is a compact orientable surface, possibly disconnected or empty. Put L=n^+=N^i ∩ N^+, where N^+ consists of points whose entire forward orbit stays in N. Both N and P are finite-type spaces.

For G=F_2, the exact sequences of (N,K) give finite dimension of H^1(N,K;G) and H^2(N,K;G), using respectively the segments

H^0(N;G) → Čech H^0(K;G) → Čech H^1(N,K;G) → H^1(N;G),

H^1(N;G) → Čech H^1(K;G) → Čech H^2(N,K;G) → H^2(N;G).

By Proposition 5(iii), Čech H^q(P,L;G) is therefore finite-dimensional for q=1,2. In the exact sequence of (P,L), the segments

H^0(P;G) → Čech H^0(L;G) → Čech H^1(P,L;G),

H^1(P;G) → Čech H^1(L;G) → Čech H^2(P,L;G)

show that Čech H^0(L;F_2) and Čech H^1(L;F_2) are finite-dimensional. Lemma 1 upgrades these two groups to finite generation over Z.

Now run the relative sequences over Z. The segments

Čech H^0(L;Z) → Čech H^1(P,L;Z) → H^1(P;Z),

Čech H^1(L;Z) → Čech H^2(P,L;Z) → H^2(P;Z)

show finite generation of the relative groups in degrees 1 and 2. Proposition 5(iii) transfers this to (N,K). Finally,

H^0(N;Z) → Čech H^0(K;Z) → Čech H^1(N,K;Z),

H^1(N;Z) → Čech H^1(K;Z) → Čech H^2(N,K;Z)

give finite generation of the required integral groups. No hypothesis on H^2(K;F_2) was needed. The argument uses neither connectedness of K nor connectedness of L. ∎

To apply the connected-block hypothesis of Theorem 10, decompose a chosen compact manifold block N into its finitely many components N_a. Every trajectory that stays in N lies within one component, so K_a=K∩N_a is an isolated invariant compactum with block N_a; empty K_a can be discarded. Its cohomology is a direct summand of that of K, because the finitely many K_a form a clopen partition. Apply Theorem 10 to the nonempty K_a separately and take the finite disjoint union of the resulting regular blocks. This also gives arbitrarily small regular blocks inside any prescribed O, starting with N⊂O. The spine homeomorphisms and later homotopies combine componentwise.

## Lemma 3: a spine gives the exact required homotopies

Suppose Q is a compact tame manifold neighborhood of K and h:Q\K → ∂Q×[0,∞) is a homeomorphism carrying ∂Q to ∂Q×{0}. For r≥0 define

Q_r = K ∪ h^{-1}(∂Q×[r,∞)).

These compact sets form a neighborhood basis of K in Q. Indeed, Q\Q_r is a compact collar except for its inner frontier; compactness of Q and continuity of h on Q\K show that every compact subset disjoint from K has bounded h-coordinate. Each Q_r is a neighborhood because its complement's closure is contained in the compact h^{-1}(∂Q×[0,r]), disjoint from K.

Let O be any open neighborhood of K. Choose a regular isolating block Q ⊂ O using Lemma 2 and the primary inputs. Set V=int Q. This is an open neighborhood of K. Given any open W⊃K, choose r>0 with Q_r⊂W. Define for 0≤t≤1 and s≥0

f_t(s) = tr + (1 - tr/(r+1))s for 0≤s≤r+1,
f_t(s) = s for s≥r+1.

This is jointly continuous, f_0(s)=s, f_t(s)≥0, and f_1(s)≥r. On Q\K set F_t(h^{-1}(p,s))=h^{-1}(p,f_t(s)); on K set F_t(x)=x. Since F_t is identically the identity on Q_{r+1}, a whole neighborhood of K, this extension is jointly continuous at K. Its image stays in Q⊂O, and F_1(Q)⊂Q_r⊂W. Restricting F to V×[0,1] proves movability exactly as required. In fact these homotopies fix K pointwise, although the target does not require that. ∎

## Consequence and limitation

An inverse-limit solenoid with circle bonding degrees d_j≥2 has one-dimensional Čech H^0 over F_2 and Čech H^1 over F_2 of dimension at most one. It is nonmovable, as its integral winding-number inverse system has strictly decreasing images. Therefore it cannot be an isolated invariant set of a continuous full flow on R^3. This consequence is consistent with, and should be credited to, the stronger result already announced in the author's 2016 abstract; it is not a new counterexample or a new non-isolation theorem.

The argument says nothing by itself about a nonisolated invariant A with no finite-type isolated invariant enlargement inside U. A general compact neighborhood N of A need not be isolating; the identity flow already has Inv(N)=N meeting its boundary. The unrestricted target remains unresolved by this partial theorem.


## Source inspection metadata

The 2024 preprint PDF was retrieved from https://arxiv.org/pdf/2403.18805 on 13 October 2026. It identifies itself as arXiv:2403.18805v1. Size: 693,688 bytes. SHA-256: 8c5c4626f488e061368b4fe2476cd0937ee14aa528fbade3227285a9b2fe79c9. Proposition 5 and its proof, Definition 6, the handle-theorem argument, block-existence discussion, and spine-theorem argument were text-inspected; printed/PDF pages 6 and 17 were locally rendered and visually inspected. The source PDF and extracts remain private.
