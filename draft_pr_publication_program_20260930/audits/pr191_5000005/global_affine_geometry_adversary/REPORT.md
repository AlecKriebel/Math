# PR191 independent global affine-geometry audit

Final report UTC: 2026-10-15T04:29:19.548947+00:00
Original head: a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe
Audit family: global translation-surface geometry and all-direction transport.

## Decision

**Original authenticated target: do not certify solved.** Its bare A0 endpoint-angle characterization is incompatible with its requested rule. **Geometric result: the rule is proved for the explicitly defined parity-selected label K_PS**, with the candidate's common-label argument and the self-contained all-direction reduction supplied in GEOMETRIC_REDUCTION.md. This is a corrected-scope theorem, not clearance of the original problem record or a novelty claim.

Audit completion: 100% for this family's assigned mathematical examination and artifacts. Best estimate toward certifying the *original authenticated target as stated*: 0%, because the definitional incompatibility must first be corrected. Best estimate for a reviewable proof of the explicit K_PS theorem: 95%, with fresh whole-package adversarial review still required. These percentages measure different goals and are not success probabilities.

## Independence and evidence boundary

Read the assigned Fuchs primary PDF and viewed the critical rendered pages before any author candidate, author code, or review. INITIAL_ASSESSMENT.md was sealed 2026-10-15T04:17:24Z at SHA-256 ce4d28101ee5aadf24c066df485486d7f9290eeb18a87bd83b0ef60fcc6f87bb, mode 0444. No sibling/prior review was read before that seal. The initial assessment identified cone-germ transport, canonical pairing, cusp exhaustiveness, and synchronization of two cones as distinct gaps. Only afterward was the original submitted CANDIDATE.md read. No original author code was needed or read.

The initial tentative idea of a canonical *translation* pairing was superseded by the candidate's actual *reflection* pairing in its all-forward/backward common labels. This correction is recorded in the research log. The candidate is credited for that mechanism. The explicit cylinder shear on the exact even doubles and finite-length descent were derived in this audit, with the already-read odd-cylinder formula in Finster acknowledged. Root independently checked the analytic replacement and cone synchronization afterward; fresh whole-package review remains separate and no human peer review is claimed.

## Exact obstruction in the authenticated target

After the source-first seal, inspected ROOT_EXACT_UPSTREAM_TARGET_01.json, authenticated to upstream revision 37e53eabe540fb458758e198be61634bd02ee008. The imported statement characterizes A0 by beta-alpha=2pi/n, without the segment-parity qualifier used by the candidate.

There is an exact interior-diagonal incompatibility, independently derived here. In a regular heptagon, source clockwise chords OX5 and OX3 have respectively

    (alpha,beta)=(pi/7,3pi/7), (3pi/7,5pi/7).

Both have one segment, no intermediate vertex, and beta-alpha=2pi/7. Their slopes differ by exactly 2pi/7, so they are parallel even under the source's direct sum/difference criterion, with ell=2 and epsilon=+1. The bare characterization assigns A0 to both. The requested rule would assign the second A_(-2)=A3 modulo 5. A0 and A3 are distinct. The source diagonal calibration and K_PS instead assign these chords A4 and A2, which obey the requested rule correctly. Thus this witness refutes the combined imported shorthand/rule, not Fuchs's geometric conjecture with its diagonal type calibration.

EXACT_SCOPE_COUNTEREXAMPLE.json records the exact integer angle units and modular values. Replacing the target's labels by K_PS is a scope repair and must be explicit.

## Verified global chain

| Component | Finding | Exact evidence/gap |
| --- | --- | --- |
| Exact surface | Pass | Odd double: one cone angle 2(n-2)pi, genus (n-1)/2. Even double: two cones angle (n-2)pi, genus (n-2)/2, for both n mod4 families. Ordinary vertex points retained when necessary. |
| Even quotient distinction | Pass | n=0 mod4 double is unramified over one-vertex opposite-edge quotient; n=2 mod4 double branches over its two vertices. The proof uses direct double gluing, avoiding an unsupported quotient transfer. |
| Hyperelliptic involution | Pass, genus>=2 | Half-turn exchange has n regular fixed side midpoints and, for odd n, one fixed vertex. Riemann-Hurwitz gives sphere quotient. Affine conjugates have derivative -I and remain holomorphic with sphere quotient. Uniqueness proof via degree-two maps and a (2,2) curve rules out ambiguity. |
| Common shift | Pass | Odd one-cone angular lift shifts all labels together. Even synchronized coordinates yield G(phi)=F(phi)-e*pi+2pi*q on both cones, using centrality. This supplies the same residue for both direction signs and both cones. A derivative alone would not suffice. |
| Canonical pairing | Pass | All model germs are first-vertex polygon chords; endpoint labels satisfy a+b=-h mod n-2. Supporting vertices supply no interior germ; boundary descriptions denote one surface germ. |
| Exhaustive all-direction reduction | Pass after analytic repair | One full twist per explicit two-strip cylinder gives lambda=2cot(pi/n). Rotations reduce direction to an odd half-sector or even full sector; an actual shear strictly decreases nonmodel saddle-connection length. Finiteness below any length bound forces a canonical terminal direction. |
| Finiteness | Pass | Proper unpunctured nonpositively curved metric cover, finitely many endpoint lifts per bounded ball, and uniqueness of lifted geodesics; regular marked points remain endpoints. No cyclotomic holonomy-discreteness assumption. |
| Source orientation and sides | Pass for K_PS | Temporary vertical model maps to source angle -pi/n. Lower side requires representative k=n-2==0; upper side uses k=0. Actual angles remain unwrapped. |
| n=3,4,6 | Pass for K_PS | Triangle trivial label plus lattice existence; square primitive coordinate parity; n=6 covered directly by genus-two double geometry and the same shear. |
| Original label identification | Fail as imported | Bare A0 shorthand conflicts with exact diagonals. K_PS equivalence to a parity-free raw disjunction is not established and is not assumed. |

The clean proof covers arbitrary genus, arbitrary short direction and length, all outgoing germs simultaneously, first-vertex stopping, diagonal/edge directions, both epsilon signs, admissible actual ell, and even-modulus cases without dividing by two. No finite enumeration is used to establish universality.

## Primary dependencies and repair status

[Fuchs 2021](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf), printed pp.501-505 and510-512, supplies definitions, angle pictures, diagonal calibration and the requested signed rule; source pages were rendered and viewed. Primary body SHA-256 is pinned in DEPENDENCY_PINS.json.

[Finster, arXiv:1005.4588v3](https://arxiv.org/pdf/1005.4588v3), sections3.1-3.2, states the odd/even groups and explicitly says the even opposite-edge quotient has the same Veech group as the double, tracing that equality to Hubert-Schmidt LemmaJ and group calculation to Veech5.8. Its odd cylinder formulas agree with the direct derivation here. [Boulanger-Lanneau-Massart2024](https://www.numdam.org/item/10.5802/ahl.211.pdf), section1.4, attributes the general saddle-direction/cusp statement to Veech; its one-cusp polygon discussion concerns the odd family. These bodies support the candidate's theorem statements but do not reproduce all loadbearing original proofs.

The Veech1989 original body was not recovered by this auditor; DOI and EuDML access attempts failed or returned metadata. Therefore, if the candidate retains its classical reduction unchanged, the proof-body provenance gap remains explicit. The independent cylinder/descent proof removes that dependency entirely and should replace the import rather than turning the gap into an unsupported assertion. It does not claim a new classification theorem or current firstness.

## Required repairs before any promotion

1. Correct the authenticated statement and explicitly name its type convention. The bare A0 characterization cannot coexist with the requested rule. A proof of K_PS must not be reported as a solution of that unchanged record.
2. Adopt the direct all-n double-surface cylinder/descent argument, or supply and check the actual primary proof chain for all imported cusp assertions. Cite the exact double surface, not merely the smaller even quotient.
3. Retain the synchronized-cone centrality proof, explicit actual-angle interpretation, source-side representative k=N, and genus-one marked-point exceptions. Do not replace these by type-invariance or a common-derivative slogan.
4. Submit the clean final scope, proof, and exact incompatibility witness to fresh adversarial verification. Root's intermediate check and this report are AI audit evidence, not human peer review or publication clearance.

Strongest verified result: a checkable analytic proof of the universal K_PS signed-angle theorem, plus an exact incompatibility witness against the imported bare A0 shorthand. Exact remaining gap for the original solved claim: coherent agreed target definition, followed by review of the appropriately restated result. No remaining central all-direction difficulty is hidden in a new unsupported lemma: the shear and finite descent are explicitly proved.

## Reproduction and containment

GEOMETRY_CHECK_RESULTS.json records PASS for n=3..128: 1,398,012 exact canonical chord identities and 16,506 exact corner physical-angle alignments; numerical corroboration covers 4,095 cylinder moduli, 12,285 cross-sections, 882 strict-descent samples, 63 even boundary equalities. These finite and floating-point checks are corroboration only; they are neither exhaustive proof nor interval-validated numerics. Run with the assigned Python3.14 stdlib invocation in execution.jsonl. Subprocess reads and checks have actual argv, UTC, exit and output-hash records in execution.jsonl; authoring invocations and artifact hashes are recorded separately. The one pre-fix failed launcher is recorded manually in the research log. The historical missing /usr/bin/rg launch and the draft cover-description correction are preserved rather than erased.

All work is confined to this audit family folder. No Git/index/ref/branch changes, environment installs, original/root edits, remote writes, outreach, editor changes or browser-tab changes were performed. Primary bodies, rendered source pages, raw tool outputs and retrieval headers are excluded from PUBLIC_SAFE_ALLOWLIST.json. Final manifests seal every file under this folder as 0444; the seal itself is listed separately to avoid self-hashing.
