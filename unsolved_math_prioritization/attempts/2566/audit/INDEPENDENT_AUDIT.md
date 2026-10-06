# Independent adversarial audit: rank 465 / problem 2566 / KOU-21.57

Audit date: 2026-10-03 UTC.

## Verdict

**PASS as an explicitly unresolved partial-progress package. HOLD for any promotion to a solution, a general reduction to simple groups, or a novelty claim.** No blocking mathematical defect was found in the retained reductions, positive cases, or exact controls. Two optional wording clarifications are recorded below. The unresolved steps are genuinely left unresolved in the release.

An independent AI review examined the five written mathematical attempts and computational controls. This is verification of existing deductions, not an additional proof-search attempt. The mathematical review is reproduced in full; workflow-only provenance has been omitted and file references are repository-relative.

## Statement and scope

The supplied image of printed Notebook page 185 was independently viewed. Entry 21.57 states the finite-group question for a nonempty class of odd-order groups closed under subgroups, homomorphic images, and extensions, with H relatively maximal and N normal. Its authors are W. Guo and D. O. Revin. There is no Hall or solvability assumption on G or N. The entry is unstarred in that image; neighboring 21.58 is starred.

The live October PDF URL was attempted during this audit but the web tool could not access it. Accordingly, the fresh statement check rests on the supplied primary-page image, not a claimed successful fresh PDF retrieval. This limitation does not alter the mathematical target. No exhaustive openness or historical-priority claim is made.

## 1. Complete-class reduction and Hall cases: PASS

Let π consist of primes p with C_p in X. Cauchy's theorem and subgroup closure imply every X-group is a π-group, and oddness excludes 2. Conversely, every finite π-group is solvable by Feit–Thompson. Its prime-order composition factors lie in X, so extension closure puts the whole group in X. The empty π case is explicitly harmless. No claim about arbitrary complete classes is being substituted for this odd-order argument.

Replacing G by HN preserves normality of N, the intersection A, and π-maximality of H: every forbidden larger π-subgroup in HN would also be one in the old G. The new quotient G/N is H/A, hence an odd π-group.

When N is solvable, so is HN: H is solvable by odd order and the quotient H/A is solvable. Hall embedding in that solvable group produces a π-Hall subgroup containing H; π-maximality makes it H. The equality [N:A]=[HN:H] then makes A π-Hall in N and therefore π-maximal. The same index argument is valid whenever H is already π-Hall in HN. No later argument silently upgrades a π-maximal subgroup to Hall in a nonsolvable group.

## 2. Solvable normal kernels and minimal counterexamples: PASS

For R normal in G, solvable, and contained in N, the use of Hall embedding is valid every time it appears. HR is solvable. The full preimage E of a π-subgroup of G/R is also solvable, because E/R has odd order. Thus a π-Hall subgroup L of E containing H exists. Its quotient image is all of E/R: its index is at once a divisor of the π′-index [E:L] and a π-number. Maximality then gives L=H, proving q(H) π-maximal.

For intersection maximality, q(A)=q(H)∩(N/R). If a larger quotient π-subgroup contains q(A), its solvable full preimage in N has a Hall subgroup containing A and mapping onto that larger subgroup, providing a strict enlargement of A. Conversely, a π-overgroup B of A whose image equals q(A) lies in AR. Since A∩R=H∩R is π-Hall in R, the index [AR:A]=[R:A∩R] is π′. The index [B:A] divides it and is π, so B=A. This proves the claimed equivalence, not only one direction. Neither A nor B has been assumed normal in N; the index and containment arguments require no such assumption.

For least |G|, R=Rad(N) is characteristic in N and normal in G, so a nontrivial R would give a smaller counterexample. After Rad(N)=1, T=Rad(G) has T∩N=1 and embeds into the π-group G/N. Thus T is π and HT is a π-subgroup, forcing T≤H. Passing to G/T preserves H/T maximality because its overgroups lift through a π-kernel. N maps isomorphically onto NT/T, and the intersection is AT/T; hence any failure survives. This proves Rad(G)=1.

Finally C_G(N) is normal, has intersection Z(N)=1 with N, and therefore embeds into the odd group G/N. It is solvable and must be trivial. The conjugation embedding G≤Aut(N), with N identified with Inn(N), is justified.

The indispensable limitation is correctly retained: radical-free N need not equal its socle, and the solvable-preimage argument does not permit quotienting away a nonsolvable normal layer.

## 3. Direct products, transport, and genuine almost-simple localization: PASS

For N=∏S_i, conjugation permutes the simple direct factors. If A_i is the ith projection of A, normality A◁H implies the product D=∏A_i is H-invariant. Therefore DH is a π-group. Maximality forces D≤H∩N=A, giving A=D. This step really eliminates diagonal intersections; it does not assume them absent.

Transport is valid with right-conjugation conventions. If h and h′ both send S_i to S_j, then hh′⁻¹ stabilizes S_i, so B_i^h=B_i^{h′} whenever B_i is normalized by H_i. For an additional h∈H, the chosen transporter followed by h is another permitted transporter to the new factor. The transported product is consequently H-invariant. Factors in other H-orbits remain the corresponding A_j. No normality of B_i in S_i is used.

After splitting, the embedded factor subgroup A_i lies in H_i. Its conjugation image is precisely its inner copy in S_i. Consequently A_i≤K_i∩S_i. The latter group is a π-subgroup normalized by K_i, so transport forces equality. To test π-maximality of K_i in L_i=S_iK_i, take an arbitrary π-overgroup U. The group U∩S_i is K_i-invariant, even though U need not be normalized by any larger group, and transport forces it to be A_i. Since both U and K_i surject onto L_i/S_i, their equal kernels imply equal orders and hence U=K_i.

Thus S_i≤L_i≤Aut(S_i) is a genuine almost-simple configuration, with exactly the required maximality and intersection. This is not merely a projection of H to an uncontrolled quotient. A failure of maximality for A in the product entails failure for at least one projection, because otherwise every π-overgroup projects back into each A_i.

If Out(S_i) is π′, K_i has trivial outer image, giving K_i=A_i≤S_i and L_i=S_i. Arbitrary factor permutations are already accounted for in the transport proof. Hence pure odd factor permutation does not evade this positive result. The proof does not assert that arbitrary radical-free normal subgroups reduce to their simple factors.

## 4. Normalizer theorem and nilpotent boundary: PASS

The primary Guo–Revin–Vdovin text, Definition 2 and Lemma 2.10, distinguishes normal from subnormal realizations and states the needed π′-normalizer conclusion. Here A=H∩N has a normal realization, so it qualifies even for the stronger realization requirement. The credited general theorem is an accepted input, not independently reproved by the finite controls. Source: [arXiv:1808.10107v2](https://arxiv.org/abs/1808.10107v2).

For every π-overgroup B of A, N_B(A)/A embeds in N_N(A)/A and is also π. Therefore N_B(A)=A. The upper-central-series proof that a proper subgroup of a finite nilpotent group is strictly smaller than its normalizer is sound. Accordingly no proper nilpotent π-overgroup can exist. The subnormal-overgroup exclusion also follows: the first strictly larger term in a subnormal chain normalizes A.

The order-21 Frobenius complement is a valid warning that self-normalizing does not mean π-maximal, and is explicitly not presented as a realizable counterexample. Likewise, the PGL₂(7) example is genuinely an even-π control. With π odd and index [G:N]=2, every H maps trivially to G/N and lies in N, eliminating that mechanism.

The 2024 adjacent paper concerns odd relatively maximal nonpronormal subgroups in simple ambient groups. Such a group has only the normal subgroups 1 and itself; neither supplies the required failure. The distinction in the release is correct. Primary abstract and bibliographic record checked at [MathNet](https://www.mathnet.ru/eng/smj7876).

## 5. Fixed points and classification scope: PASS

Ω is nonempty by finite maximal extension of A. It is H-stable because N and A are H-stable. Each a∈A fixes every B∈Ω setwise because a∈B; it need not centralize B. Thus the action factors through P=H/A. An H-invariant B makes BH a π-subgroup, forcing B=A. Conversely A maximal makes Ω={A}. No Hall assumption enters.

For P a p-group, no global fixed point implies every orbit size is a positive power of p, so p divides |Ω|. It does **not** generally imply |P| divides |Ω|, and the release does not claim that stronger statement. For arbitrary nontrivial odd P, every non-singleton orbit has size at least its smallest prime divisor, hence a failure requires at least three members. An odd cardinality or a π′-cardinality alone gives no general fixed-point theorem. The C₁₅ action with orbit sizes 3 and 5 is a valid countercontrol to that inference.

The published classification has the precise hypotheses S minimal simple, |π∩π(S)|>1, and π(S) not contained in π. Tables 1, 3, 5, 7, 9 state maximality in the odd cases. For odd π the last hypothesis is automatic; the intersection-zero and intersection-one cases are trivial/nilpotent. Therefore the cited application is valid. Primary source: [Guo–Revin, Theorem 1.1 and the odd tables](https://link.springer.com/article/10.1007/s13373-017-0112-y).

The passage from minimal nonsolvable N to N/Rad(N) is valid because every proper subgroup of N is solvable: all proper normal subgroups lie in the radical, the quotient is nonabelian simple, and its proper subgroups have proper solvable preimages. The direct-product extension through Rad(N) then follows from the already verified lemmas. No broader quotient-preservation theorem for arbitrary submaximal groups is needed.

## 6. Exact independent controls: PASS

The author checker replayed successfully and its parsed JSON exactly matched `control_results.json` at the problem-directory root.

A separately written checker used canonical invertible 2×2 matrices over F₇ modulo scalar multiplication, rather than the release's projective-line permutations. It imported no release code. Its findings were:

- |PGL₂(7)|=336, |PSL₂(7)|=168; normality checked.
- H has order 16 and A=H∩N has order 8.
- For every one of the 320 elements outside H, adjoining it to H gives order 336.
- The entire subgroup interval [A,N] was enumerated, not just immediate one-element extensions of A. It consists of four groups, of orders 8, 24, 24, and 168.
- The two order-24 groups are the maximal {2,3}-overgroups and an order-8 generator of H interchanges them.
- An independent affine-permutation model of C₇⋊C₃ has order 21, with a complement of order 3 and normalizer of order 3.

The independent code and machine-readable results are in `independent_matrix_controls.py` and `independent_matrix_results.json` beside this audit. These certify only the named controls. They are not evidence for a universal theorem or for novelty.

## Clarifications and remaining HOLD boundaries

No correction is necessary to rescue a false retained theorem. Two terminology clarifications are recorded here and made explicit in `../PUBLICATION_NOTE.md`:

1. In turn 5, replace “empty-prime and single-prime cases” with “|π∩π(S)|≤1 cases.” This makes clear that π may contain extra primes absent from S. The existing local nilpotence argument already proves these cases.
2. Replace “fixed-point-free action” with “action having no global fixed point,” or explicitly write Ω^P=∅. The former phrase can elsewhere mean the stronger semiregular condition, which is not established or needed here.

The claims that must remain on HOLD are exactly the general invariant-overgroup assertion, any deletion of a nonsolvable normal layer using the solvable quotient lemma, and any construction of an odd counterexample from only an abstract odd permutation action, a self-normalizing subgroup, or nonpronormality. The release preserves these gaps accurately. Its unresolved status and absence of novelty claims are appropriate.
