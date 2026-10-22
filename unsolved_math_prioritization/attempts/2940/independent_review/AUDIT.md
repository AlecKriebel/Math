# Independent adversarial audit: KP-4.64

Audit date: 2026-10-03 UTC. Catalogue label: 2940. Rank label: 536.

## Verdict

**PASS for the stated unsolved obstruction-and-reduction packet.** No blocking mathematical error was found in the frozen packet. Five distinct substantive approaches are documented. None supplies an irreducible example, a general impossibility theorem, or a solution to KP-4.64. The appropriate disposition remains **unsolved, 5/5**.

This is an independent mathematical audit against identified primary sources and a deterministic arithmetic replay. It is not human peer review, a formal proof certificate, a novelty certificate, or an exhaustive literature search. Acceptance is confined to the assertions and hypotheses actually stated in the packet.

## 1. Frozen input and integrity

The author manifest SHA-256 is

`f3189bfe42f9ff83f655e547ac6cf6aaa12b7b84561717c928572c126d9128cb`.

The proof SHA-256 is

`8b05b4c8fe2bb2d7ad2db0ffbef45588a0f14a9e2ecd4fa200d7a96c3e78e2b0`.

All seven author-manifest entries have their specified bytes and SHA-256 hashes. The original verifier was run independently; its output agrees byte-for-byte with the frozen verification output and reports 24,475 assertions. A separate standard-library implementation, `independent_controls.py`, reads neither the author verifier nor its recorded output. It passes the same 24,475 controls with the same per-family counts. The author packet was not modified.

The audit manifest binds this report, both arithmetic outputs, the independent checker, the integrity report, source identities, and the audit disposition. Source PDFs, source extracts, screenshots, and external working material are not included in this audit deliverable.

## 2. Exact target and semantic boundaries

The full question and accompanying remark at printed/PDF p. 242 of the 2026 preliminary K3 problem list were inspected. They ask for the irreducible, closed, smooth four-manifold separation described by the packet and credit M. Stoffregen and I. Dai. The remark identifies connected-sum examples and reports no known irreducible examples. This agrees with the packet's dated, qualified source statement. It does not prove the present-day nonexistence of a later solution. [K3]

The packet consistently requires nonzero ordinary S¹-equivariant BF for at least one spinᶜ structure and zero ordinary integer-valued SW invariants for every spinᶜ structure and allowed insertion. It does not quietly replace these with family, relative, real, diffeomorphism, or Pin⁻(2) invariants. Its convention on smooth connected-sum irreducibility is explicit; the rejected examples split into factors with positive second Betti number, so the homotopy-sphere convention cannot rescue them.

The b₁=0, b⁺>1, and index restrictions belong to particular deductions. They are not advertised as restrictions on the original question. No chamber-dependent b⁺=1 argument, or universal claim for b₁>0, is smuggled into the conclusion.

The public rank and catalogue ID were treated as metadata. The mathematical target was independently matched to KP-4.64. Repository-history and catalogue-access assertions were not independently repeated in this mathematical audit.

## 3. Parity and integral-torsion checks

For every spinᶜ structure, the complex index is an integer and

    expected dimension = 2 index_C(D) - (1 - b₁ + b⁺).

When b₁=0 and b⁺ is even, the dimension is odd. The ordinary insertion algebra has only the degree-two generator U once the free part of H₁ is zero. Thus no ordinary monomial has the required degree; negative dimensions also contribute zero. This proves all the stated ordinary numerical SW invariants vanish, not merely the invariant of a selected spin structure.

Vanishing rational H₁ is enough: torsion in integral H₁ does not create free degree-one insertions in this convention. The rational cohomology ring does not imply spin, and the packet correctly retains spin as an independent hypothesis. It also avoids assuming that spinᶜ structures are determined by Chern classes in the possibly torsion-bearing rational-cohomology case. Multiple spin structures do not cause a gap because FKM's theorem applies to each one.

The orientation on the rational ring is important. It fixes the K3 sign convention and hence b⁺=6, b⁻=38 and signature −32, rather than their orientation-reversed counterparts. Changes in homology-orientation sign do not change vanishing or nonvanishing.

## 4. Connected sums and Hurewicz kernels

The BF-I construction/comparison chain was read through the finite-dimensional approximation, monopole-map boundedness, Propositions 3.3–3.4 and Lemma 3.5. In the packet's b₁=0, b⁺>1 range, the Picard torus is a point and the ordinary class is identified with stable cohomotopy of CP^(r−1). The comparison kernel table and its stated range agree with the source. Negative expected dimension gives zero by dimension/connectivity; at dimensions zero and four the comparison is injective. The congruences for dimensions one and two follow correctly from r even. Published stable-stem and attaching-map results remain external theorem inputs. [B1]

BF-II's setup and full three-homotopy gluing argument were inspected, including the common boundary identifications, neck estimates, Lemmas 3.2–3.5, and the final composition. Its applications support η² and η³ detection for two and three standard K3 factors. The fourth-factor conclusion uses the equivariant criterion in Proposition 4.5, not the false claim η⁴≠0. The fifth-factor vanishing is correctly scoped. The Kähler-support argument in §4.3, the dimension-zero comparison, and the proof of Corollary 1.4 jointly justify the claim that the standard K3 has no additional BF-supported spinᶜ structures. Merely knowing its SW support would not by itself have sufficed. [B2]

Every connected sum rejected in the packet has an explicit nontrivial smooth splitting. Neither invariant nonvanishing nor identification of an intersection form proves irreducibility. The packet does not claim otherwise.

## 5. Gluing along −2 spheres

The survey's positive-curvature gluing hypotheses and the derivation of Theorems 8.3–8.6 were checked. RP³ is a valid positively curved rational-homology-sphere boundary. The orientation-reversing boundary identification switches the two spin structures and forces inducing Chern evaluations 0 and 2. Therefore the product formula is not an unrestricted transplantation of the S³-neck argument. If BF-supported classes on both summands evaluate zero, one factor necessarily vanishes. The reflection/positive-semidefinite-span argument also retains the required hypothesis on both factors. Standard K3 meets it. [B]

The resulting topological calculation was independently reconstructed: removing each −2 disk bundle subtracts Euler characteristic two and removes one negative direction. Gluing along the full closed RP³ boundary gives χ=44 and signature −30. Rational Mayer–Vietoris, using connected complements and the injective H₀ map, gives b₁=0, hence (b⁺,b⁻)=(6,36). No unproved simple-connectedness or integral-homology claim is needed. Thus SW vanishes by parity, while every ordinary BF class vanishes by the gluing obstruction. The route is genuinely excluded regardless of any proposed irreducibility proof.

## 6. FKM nonvanishing and normalization

The relevant FKM proof chain was read in full: δ's transversality construction and choice independence, Lemmas 2–7; its zero class and bijectivity, Definitions 8–9 and Lemmas 10–12; the two-Hopf calculation, Lemma 13; the higher-n zero model, Lemma 14; and Proposition 16's free-involution/Stiefel–Whitney argument leading to Theorems 19–20. Crucially δ is defined on the S¹ stable-homotopy set, δ(0)=0, and the n=2 restricted class has δ=1. Nontriviality of a Pin(2) object alone is not the argument. The unit-sphere finite-approximation convention is compatible with BF-I's disk/sphere and based one-point-compactification descriptions. [FKM; B1]

Printed p. 172 was visually inspected. The denominator 2 and the isolated W₀ fiber label are genuinely printed, not extraction artifacts. The packet appropriately uses the standard complex index denominator 8 and the preceding definition of E. For the spin case, quaternionic index two is complex index four, with target real dimension six; the resulting expected dimension is one. The higher-n conclusion uses both δ=0 and δ's bijectivity, and is expressly limited to spin structures. [FKM]

Accordingly, the sufficient criterion is sound. An irreducible closed smooth spin manifold with the specified oriented rational ring would have ordinary BF nonzero and all ordinary SW invariants zero. The packet supplies no such irreducible realization. Retaining this as a conditional reduction is essential.

## 7. Free finite quotient obstruction

The quotient calculation was reconstructed without using the checker. A free orientation-preserving finite action of order q on the simply connected connected sum gives a smooth oriented quotient Y with finite fundamental group and therefore b₁(Y)=0. Finite oriented covering multiplicativity gives

    χ(Y) = (22m+2)/q,
    σ(Y) = −16m/q,
    1+b⁺(Y) = (3m+1)/q.

Thus q divides both 16m and 3m+1. Their gcd equals gcd(16,3m+1), since m is coprime to 3m+1. This proves the claimed necessary condition. For even m the gcd is one; for m=3 the only nontrivial arithmetic possibility is q=2. Its (χ,σ,b⁺,b⁻)=(34,−24,4,28) is correct.

Euler/signature arithmetic is not an existence theorem for a group action. It also gives neither quotient irreducibility nor a BF descent theorem. The packet explicitly leaves all three issues open. Branched or orientation-reversing actions are outside this proposition and cannot be silently substituted.

## 8. Search, verification limits, and disposition

A fresh targeted search recovered the modern primary question and the FKM/Bauer sources. Recent family-invariant, exotic-diffeomorphism, and Pin⁻(2) results were screened as potential semantic false positives. Their advertised conclusions do not establish the required ordinary single-manifold separation. No later full solution was located; the search is not exhaustive.

All thirteen finite-control families pass, with counts matching the frozen output. These controls check exact arithmetic and consistency of published formulas. They do not compute an invariant from a monopole map, construct a manifold, test irreducibility, prove the external analytic/homotopical theorems, or establish an unbounded assertion by enumeration.

**Required corrections: none for the stated unsolved scope.** The strongest realization statement remains conditional. The exact unresolved task is still an irreducible closed smooth example with the ordinary invariant separation, or a general obstruction. The frozen packet can be retained with this independent audit appended; it must not be promoted as a solution.

## Primary references

- [K3] Baykur–Kirby–Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, preliminary author version, Problem 4.64, p. 242: https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf
- [B1] Bauer–Furuta, *A stable cohomotopy refinement of Seiberg–Witten invariants. I*, inspected author preprint v1: https://arxiv.org/abs/math/0204340v1
- [B2] Bauer, *A stable cohomotopy refinement of Seiberg–Witten invariants. II*, inspected author preprint v1: https://arxiv.org/abs/math/0204267v1
- [B] Bauer, *Refined Seiberg–Witten invariants*, inspected author manuscript v1: https://arxiv.org/abs/math/0312523v1
- [FKM] Furuta–Kametani–Minami, *Stable-homotopy Seiberg–Witten invariants for rational cohomology K3#K3's*, J. Math. Sci. Univ. Tokyo 8 (2001), 157–176, final journal PDF: https://www.ms.u-tokyo.ac.jp/journal/pdf/jms080109.pdf

The BF-I/II typeset publisher PDFs were not separately inspected. The source-version limits of the author packet are preserved.
