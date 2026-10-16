# Independent adversarial topology audit of PR 894

Recorded UTC: 2026-10-16T07:08:00.207284+00:00
Completion estimate: 100% of this independent topology audit. Original author effort remains 1/5.

**Verdict: PASS for the Levi/topology/homology mechanism. No fatal gap, hidden extra hypothesis, counterexample, or required mathematical repair was found in the pinned proof.** The proof's global topology implications are valid. This is an independent audit of the argument, not a claim of historical priority, external acceptance, or formal machine verification.

## Frozen object and independence

- Problem: 30005737 / OWR-14298013-001, “Post-Lie Structures with Semisimple Target.” The full finite-dimensional complex target excludes a post-Lie structure when the source is perfect and nonsemisimple and the target is semisimple. The brackets are on one vector space.
- Draft head: `401f86e018e8cc5075e37a29bae9350eb9f89c36`; original claimed-solved effort: 1/5. This audit is validation, without another substantive author approach.
- External manifest: 4,654 bytes; SHA256 `1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c`. All 18 listed source files passed byte length, SHA256, and Git blob SHA1 authentication. See `AUTHENTICATION.stdout.json` and `AUTHENTICATION_RUN.json`.
- Native canonical pair: 3,524 bytes; SHA256 `b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298`. The complete native pair, catalog entry, and root native receipt were read before the proof. The pair contains the complete problem/background and an empty report object; the receipt records `report_present: false`.
- Audited proof: `authored/PROOF.md`, 10,996 bytes, SHA256 `2ac96492f1791f7fa2d5e988a7a44f60040395f6f2994649441755559c01f7f1`.

The target and an independent mechanism were saved at 07:02:15 UTC before reading the authored proof or prior audits. The post-proof assessment was saved at 07:03:43 UTC before reading either old audit verdict. Only afterward were the two complete old audits read. Their agreement is recorded separately and does not supply the premises of this verdict. Remote PR eligibility was supplied by the parent audit; this subaudit authenticated its frozen bytes and did not query or mutate Git refs, the index, branches, or remote publication state.

The official report confirms that the semisimple-target conjecture follows the perfect nonsemisimple-source/sl3 proposition. Adjacent nilpotent-target conjectures are separate. [OWR 46/2023, p.2689](https://ems.press/content/serial-article-files/48175).

## Strongest verified result and exact gap

The topology result independently verified here is:

> If a connected simply connected complex group G acts transitively on a connected simply connected complex semisimple group N, the dimensions agree, and its stabilizer has zero Lie algebra, then G is diffeomorphic to N. The solvable radical of Lie(G) must consequently vanish.

The candidate proves the required transitivity and zero stabilizer Lie algebra from a pair of homomorphisms `j1,j2: g -> n` with invertible difference and unimodular g. Its determinant identity also survived direct recalculation in this audit. Combining those deductions with the topology result proves its stated stronger unimodular-source theorem. The standard algebraic passage from post-Lie structures to this transverse pair is explicitly derived in the candidate and has no apparent sign or bracket reversal. Full independent coverage of the algebra/analytic family belongs to the parent audit's separate review.

**Exact remaining mathematical gap in this family: none.** Priority and novelty are unassessed: no broad priority search was performed. A topology pass does not by itself certify a new historical contribution.

## Theorem assumptions versus deductions

| Item | Status and use |
| --- | --- |
| Finite dimensionality, complex field, equal dimensions | Hypotheses of the candidate theorem; permit complex integration and the compact-form degree comparison. |
| Semisimple target n | Hypothesis; gives target unimodularity and a compact real form of dimension dim_C(n). |
| Unimodular source g | Hypothesis of the stronger theorem; derived from perfectness for the original problem. |
| Two homomorphisms with invertible difference | Hypothesis of the stronger theorem; derived from the post-Lie identities for the original problem. |
| Simply connected G and N | Auxiliary choices guaranteed by classical integration, not extra restrictions on groups supplied by the problem. |
| Integrated homomorphisms and global left-right action | Deductions by integration and the explicit action formula. |
| Global transitivity | Deduction from determinant invariance and holomorphic continuation; never assumed from a local orbit. |
| Closed discrete stabilizer and covering | Deductions after transitivity; no closed-image assumption on either homomorphism. |
| Global product R x S for G | Deduction by constructing a simply connected semidirect product and invoking uniqueness of integration. |
| R contractible | Deduction by codimension-one solvable induction; no assertion about a general solvable exponential map. |
| Compact-form polar topology and top fundamental class | Imported classical Lie theory and elementary topology. Orientability and the relevant dimensions are justified below. |
| Radical zero | Deduction by contradictory ordinary singular homology groups in degree dim_C(n). |

## Detailed adversarial checks

**1. Integration and nonclosed images.** Both algebra maps integrate from the same simply connected G to the chosen simply connected N. Neither map must be injective, algebraic, proper, or have closed image. The formula `A_h(p)=J1(h)pJ2(h)^(-1)` is a global action because composition reverses the right inverses in exactly the required order. It can be used even if the image subgroup in `N x N` is nonclosed. No quotient by that image occurs anywhere in the proof.

Left trivialization gives `B_p=Ad_(p^-1)j1-j2`; at the identity its determinant is nonzero. The inverse function theorem therefore supplies an open neighborhood in the identity orbit. This is an actual open subset of N, not an abstract immersed-orbit topology.

**2. Local-to-global action bridge.** Direct expansion confirms
`B_(A_h(p))=Ad_(J2(h)) B_p Ad_(h^-1)`.
The determinant characters of G and N have zero differential under the trace hypotheses. Connectedness makes their values identically one. Thus `det B_p` is invariant on the initial open orbit. It is a single-valued global holomorphic function because the adjoint action and the left trivialization are global. The identity theorem makes it the same nonzero constant on all connected N. Every orbit is then open; a partition into two or more open orbits would disconnect N. This is a valid deduction of transitivity, not a completeness theorem imported without hypotheses.

**3. Stabilizer and covering.** H is the inverse image of a point under the continuous orbit map, hence closed. Its Lie algebra is `ker B_e=0`, so the closed subgroup theorem makes it discrete. Transitivity identifies N with `G/H` with the usual quotient manifold structure. To see the covering directly, choose an identity neighborhood W so that `W^(-1)W` meets H only in the identity. Distinct right translates `Wh` are disjoint, and quotient images of left translates of W are evenly covered. No normality of H is required. Since the base N is simply connected and the total space G connected, this covering has one sheet. H is trivial. The orbit map is a biholomorphism, although a diffeomorphism suffices. It need not be a group homomorphism, and no Lie algebra isomorphism `g = n` is inferred from its existence.

**4. Global Levi decomposition.** The candidate does not assume that an arbitrarily chosen analytic Levi subgroup is closed, or that a radical in a general global form is simply connected. Start with the Lie algebra Levi decomposition `g=s semidirect r`. Choose simply connected integrations S and R independently. The derivation action integrates to an action on R: integrate first on its Lie algebra automorphism group, then use uniqueness of integration on simply connected R for the automorphisms. The resulting semidirect product has manifold `R x S`, is simply connected, and has Lie algebra g. Uniqueness identifies it with G. Both factors are consequently embedded and closed in this construction. This fully resolves the global Levi issue needed here.

**5. Solvable contractibility.** For nonzero solvable r, its derived algebra is proper. A nonzero functional killing the derived algebra has a codimension-one ideal kernel r'. A vector outside the kernel spans a one-dimensional subalgebra, so the algebra is a semidirect product of that line and r'. Integrating on simply connected groups makes the underlying manifold `C x R'`; induction starts at a point. Thus R is diffeomorphic to `C^q`, `q=dim_C(r)`. Every step concerns freshly chosen simply connected groups. This avoids the false claim that all connected solvable complex groups are contractible: `C*` is a counterexample. It also avoids the false claim that the exponential of every simply connected solvable group is a diffeomorphism.

**6. Compact-form dimensions, orientations, and ordinary homology.** A compact real form k of a complex semisimple algebra n satisfies `k tensor_R C = n`; therefore `dim_R(k)=dim_C(n)=d`, whereas the real dimension of N itself is `2d`. The compact group K_N in polar decomposition is connected, compact, and a manifold without boundary. Left translation of an ordered basis at the identity supplies a global real frame, hence an orientation. Its top fundamental class gives `H_d(K_N;Z)=Z`. Polar contraction preserves ordinary singular homology, so `H_d(N;Z)=Z`.

For the source, the contractible R factor can be removed by a product contraction. Polar contraction of S then gives a compact connected group K_S of real dimension `s=dim_C(s)`. If r is nonzero, `s<d` and `H_d(K_S;Z)=0`. This contradicts the diffeomorphism. There is no use of compactly supported homology or of degree `2d`; either would change the argument. Arbitrary torsion in lower homology has no bearing on the top-degree mismatch.

**7. Multiple simple factors and zero cases.** A semisimple algebra is a finite sum of simple ideals; its simply connected integration and compact form are corresponding finite products. Dimensions add. The product orientation has one integral top fundamental class, so the target top homology remains Z. This is not a simplicity-only argument. For s=0, K_S is a point and all positive-degree homology vanishes. For d=0, equal dimensions force g=n=0 and the stronger theorem is immediate; the original requirement of a nonsemisimple source cannot hold. If r=0, there is no contradiction, exactly as required.

The target cannot be weakened merely to reductive for this argument. An additive complex central factor contributes dimension but no positive-degree ordinary homology; innerness of all target derivations also fails. This identifies the exact role of target semisimplicity without importing any stronger assumption on its simple factors.

## Classical source verification

The source checks are bounded to precise inputs. [Etingof's MIT notes](https://ocw.mit.edu/courses/18-755-lie-groups-and-lie-algebras-ii-spring-2024/mit18_755_s24_lec_full.pdf) were checked at Proposition 4.12/Corollary 4.16 (p.31), Theorems 9.12–9.13/Corollary 9.14 (p.55), Theorem 48.9 (p.264), Theorem 49.1 (p.265), and Corollary 49.6 (p.266). Compact forms and polar lifting were checked at Theorem 43.4/Corollary 43.5 (pp.231–232), Theorem 43.7/Corollary 43.8 and following covering discussion (p.233). These locations have the required complex and simply connected scope. The fetched PDF exactly matches the candidate's source pin: 4,247,073 bytes, SHA256 `ffb09776bafa3fa50dfc2bc83ee36b89058f98b7f80ff6fa90e2e34962cc9046`.

[Hatcher, Algebraic Topology](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf), Proposition 1.32 (p.61), gives the covering sheet index; Theorem 3.26(a,c) (p.236) gives the top fundamental class and vanishing above manifold dimension. Fresh PDF: 8,121,741 bytes, SHA256 `bebb3032bf9021b956da3bd070eb6c67dc662cf849be9cdf6679f677560e5618`. Raw PDFs were hashed in memory and were not saved to this deliverable.

## Actually executed computations and limits

`AUTHENTICATION_RUN.json`, `BOUNDARY_CHECKS_RUN.json`, and `PRIMARY_RETRIEVAL_RUN.json` preserve real UTC process start/end timestamps, return codes, script hashes, and raw stdout/stderr hashes. All three returned 0 with empty stderr. A later administrative packaging command failed before Python started because the shell could not create its here-document temporary file; its exact stderr, return code, and timestamp limitation are preserved in PACKAGING_FAILURE.json and PACKAGING_FAILURE.stderr.txt. No failed run was suppressed.

`boundary_checks.py` verifies both homomorphisms on all basis pairs for the nonunimodular source `b_plus direct_sum C F -> sl2`. It computes trace-ad values `(2,0,0)` and invertible difference. A coefficientwise formal polynomial check gives `det B_p=-d^2(ad-bc)`, hence `-d^2` on SL2. All 116 integer determinant-one matrices with entries between -3 and 3 give the same formula, including matrices with d=0. Thus dropping unimodularity actually permits degeneracy beyond the identity orbit. At the group level the triangular product has the open cell `d!=0`, so this is a concrete test of the exact excluded failure.

The same script checks integer cellular-chain bookkeeping for `(S^3)^k`, 0 through 5 factors: top rank one in degree 3k and no chains above 3k. This is an explicit dimension/product diagnostic, not verification of all semisimple homology or a replacement for the fundamental-class theorem. Neither finite computation proves integration, covering theory, contractibility, polar decomposition, or the full obstruction.

## Issues, repairs, and disposition

- Fatal mathematical issues: none found.
- Required repairs to the pinned proof: none.
- Nonblocking improvements: a citation to Hatcher's exact top-homology theorem would make the elementary topology source location explicit; the current proof already states the input correctly.
- Unsupported assumptions introduced by this audit: none beyond the stated finite-dimensional complex Lie-theory setting and the named classical inputs.
- Remaining scope: full parent synthesis and priority/novelty review. Those limits do not weaken the proved topology implication.

No person was contacted or messaged. No Git mutation, push, release, external comment, or foreign cleanup occurred. All audit files were written within the dedicated audit folder. `SAFE_MANIFEST.json` enumerates public-safe payloads by relative path, size, and SHA256, excluding itself and `private_tmp`.

Final mechanical integrity check: PAYLOAD_INTEGRITY_RUN.json records return code 0 at 07:09:25 UTC. It reauthenticated all 18 unchanged source blobs, checked process output/script hashes, and verified public-payload exclusions and the preserved administrative failure.
