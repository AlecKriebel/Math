# Source and scope review — Zenodo 23328912

Disposition: **SCOPE_COMPLETE — mathematical review pending**. This is not a mathematical PASS, a fresh execution result, external peer review, or a publication authorization. No submitted mathematical checker was run for this scope assignment.

## Edition and immutable source identity

The exact frozen queue entry is row 64, inventory index 80, work `Z-23328911`, record `23328912`: *A two-cube cubulation of the AIM free-by-cyclic example*, Alec Kriebel, version 1.0. Use the edition DOI **10.5281/zenodo.23328912**; the concept DOI is 10.5281/zenodo.23328911. The manuscript and metadata date are October 12, 2026; the record creation timestamp is October 13, 2026, 00:50:56.980394 UTC. These distinguish the stated edition date from a verified repository timestamp and do not establish historical priority.

Fresh API metadata and all three public files were acquired with normal HTTPS verification. API size/MD5, frozen queue size/MD5 and the independently computed SHA256 agree. `sources/receipt.json` pins every public file and every extracted archive member. `queue_identity.json` retains the exact input entry, and `final_integrity.json` rechecks originals after scope work.

| Public asset | Bytes | SHA256 |
|---|---:|---|
| aim_5_2_two_cube_cubulation.pdf | 77,863 | 3dfdfca7c0b9d41c54ed03dc9500afd8d8013fef2ebd589b2806712f84781841 |
| aim_5_2_source.zip | 11,430 | a244ddbbbb0f7ca6d9ca073d21589bef1e9c0a98a404daaca195ee9fc87f6935 |
| aim_5_2_verification.zip | 56,309 | 8ff6e88f6d4a539680667b22931e080365dfd905dd64f795f408e23cc7bb8f01 |

Main TeX SHA256: `6c339c55aef95458e633ba2dc3136b26e4abacf55acca08e170b992783785390`. Source ZIP has four regular files; verification ZIP has 24. Both were safely extracted into separate roots, avoiding same-name collisions. Every member was scanned by content for PDF/ZIP/tar signatures and compared byte-for-byte with its archive member. There is exactly one six-page reader PDF, no embedded reader PDF and no nested archive. No unrelated archived paper was included in the reader set.

## Coverage and independence

Read all six PDF pages, inspected all six rendered pages, read the complete 412-line current TeX and 232-line `packet/ATTEMPT_1.md` construction, both current READMEs, `PUBLICATION_ADDENDUM.md`, `packet/VERIFICATION_ADDENDUM.md`, all three mathematical programs and the entire current `verify_bundle.py` runner. The proof note's ancillary convex-hull visualization and its limitations were included in this reading; it is not needed for the finite construction in current Sections 2–4.

The current READMEs/addenda, the construction note's opening/closing status text, the bibliography-pointer access summaries, code comments and output literals contain historical review/acceptance/pending labels. Those were incidentally exposed while reading required current support and are **not adopted as evidence**. The dedicated `AUDIT.md`, `AUDIT_RESULT.json`, `BUNDLE_REPORT.md`, historical source-gate/research-log bodies and stored execution/result JSON bodies were not read. Hashing them for byte identity is not reading their findings. No sibling report or conclusion was consulted. The runner's static baseline expectations were read as code, never treated as observations.

Read the exact primary interfaces identified below, including their hypotheses and nearby proofs/definitions. This does not claim a full rereview of all 311 pages of the seven reference PDFs. Original-source acquisition receipts distinguish the 2024 archived AIM page from currently unreachable live endpoints.

## Exact target and claim map

1. **Input and marking (page 1).** The free group is `F(a,b,c)` and the automorphism is `a↦a`, `b↦ab`, `c↦bcb`, with the last `b` positive. The semidirect-product convention is `tut⁻¹=φ(u)`. The inverse automorphism is written explicitly. This is one specified group, not a claim for all polynomially growing free-by-cyclic groups, a power of this automorphism, or a finite-index subgroup.
2. **Main theorem (pages 1–4).** A finite locally CAT(0), three-dimensional unit cube complex `Z` has cell counts `(1,7,8,2)` and fundamental group equal to the displayed group. Its universal cover supports a free, proper and cocompact action of the full group by cubical isometries. The manuscript proves local curvature first, then the exact group identification, then the global cover/action conclusion.
3. **Quotient convention (pages 1 and 3).** Characteristic cubes may have isometrically identified boundary faces and need not embed in `Z`. The counts apply before subdivision. This is a general cube complex; the CAT(0) universal cover is strict cubical under Leary C.4. Leary C.11 gives a strict quotient after the second cubical subdivision, with different counts. Two three-cells is not a statement that the whole quotient consists of only two closed cubes with embedded boundaries.
4. **Base and endpoint maps (pages 2–3).** `K` has one vertex, three edges, two squares `xyXY` and `bxBY`; its group is `<x,y,b | [x,y]=1, bxb⁻¹=y>`. `λ` interchanges `x,y` and reverses `b`. The four-vertex/six-edge/two-square domain `Q` has `π₁(Q,A)=<dp>≅Z`, mapping to `bx` and `b⁻¹y`. Full injective signed-link maps, not global injectivity of `Q→K`, are the local-isometry requirement. The repeated `A` in the second square is two separate corners.
5. **Finite quotient links (pages 3–4).** `Z=K∪_{j,λj}(Q×[0,1])`. The unique link comprises the base link and eight cones with distinct signed vertical apices. It is asserted to be an actual flag simplicial complex, with f-vector `(14,32,16)` and no four-clique. Incidence multiplicities and repeated corners matter; a simple graph's clique count alone would not establish the claim.
6. **Exact group (page 4).** Six product-square relations eliminate three vertical generators and produce `<x,y,b,z | xy=yx, bxb⁻¹=y, z⁻¹(bx)z=b⁻¹y>`. Reversible changes `t=x`, `a=xy⁻¹`, `c=(zx)⁻¹` identify it with the precise target. Checking the relators in the target is only a forward homomorphism; the written reversible Tietze argument carries the isomorphism claim.
7. **Global action (page 4).** Completeness, local finiteness and finite unit shapes support properness of the universal-cover metric; deck transformations are free and properly discontinuous, compact sets meet finitely many translates, and the finite quotient gives cocompactness. These are written geometric deductions, not finite verifier outputs. Proper and cocompact mean more than a free action.
8. **Prior-method existence route (page 5).** The manuscript separately derives an unspecified finite model using the element `g=bx` in a Bass–Serre tree. A finite pointwise axis-segment stabilizer gives WPD; hyperbolic embedding yields Morse/quasiconvexity; finite cubical completion gives `Q₀` with subgroup image exactly `<bx>`. Postcomposition by `λ` gives compatible local isometries on the same domain. Its double mapping cylinder has dimension at most three and the same entire group. This route supplies no `(1,7,8,2)` counts and does not itself establish discovery priority.
9. **Computational scope/disclosure (pages 5–6).** The supplied standard-library programs address finite attaching/link data and free-word/semidirect-product identities. They do not formalize the global curvature theorem or deck-action proof. The paper explicitly states extensive AI assistance, unrefereed status, no external human review and no proof-assistant certification.

## Original question and attribution

The freshly retrieved 28-August-2024 Wayback capture displays AIM Problem 5.2, attributed to Rylee Lyman, with the exact `a,ab,bcb` automorphism and asks for a geometric action on a CAT(0) cube complex. Its embedded problem ID is `0df1011a6fa8a3c46e2c977b7e12c66f`, revision `6-d5a22eda9ed96ccdc8327e2e9395bb3e`. The nearby remark concerns an existing geometric action on a CAT(0) **space**; that is not already the cubical assertion. Current live HTTP/HTTPS AIM requests timed out in this session. No TLS checks were bypassed. The archival evidence is explicit, not presented as a fresh live-page response.

The official three-page workshop report was separately retrieved and read. Printed page 2 discusses `b↦aba, c↦bcb` and a three-dimensional candidate hoped to be cocompact. That different marking/formula is preserved rather than silently substituted for Problem 5.2. Do not claim priority over that candidate or unpublished work. The current note itself declines historical firstness and absolute novelty.

Primary bodies inspected:

| Primary source | Interface read | Hypotheses and use |
|---|---|---|
| Leary, arXiv:1009.1540v3 | Appendix C introduction; C.4 p31; C.9 and C.11 p33, nearby proofs | Arbitrary cube-complex vertex links must be **flag simplicial complexes**. CAT(0) cover is strict cubical; second subdivision handles the quotient convention. |
| Ben-Zvi–Kropholler–Lyman, arXiv:2011.05374v1 | Thm1.1 p2; local-isometry definition/Prop2.1 p3; Thm5.1 and proof pp8–9 | Based graph realizing the exact subgroup; finite NPC target; word quasiconvexity for the maximal-tree generating set yields finite completion. Full-link local isometry gives π₁ injection. |
| Minasyan–Osin, corrected arXiv:1310.6289v6 | Cor4.3 and proof p13 | Hyperbolic element of a simplicial-tree action with finite pointwise stabilizer of two axis vertices is WPD. No R-tree or finite-extension substitution. |
| Dahmani–Guirardel–Osin, arXiv:1111.7048v5 | Def2.8/Cor2.9 p8; Thm6.8 p89 and initial proof | Loxodromic WPD element has virtually cyclic hyperbolically embedded `E(g)`; Thm6.8 with one element has no pairwise-commensurability issue. |
| Sisto, arXiv:1310.7753v1 | Morse definition/Thm1 p1; nearby Thm2 p2 | Finitely generated ambient group and infinite-order element in hyperbolically embedded virtually cyclic subgroup. Gives Morse control in word metrics. |
| Hagen–Wise, arXiv:1605.07879v3 | Remark3.7 p17; Cor7.2 pp3,43 | Remark concerns compatible edge cubulations/convex subcomplexes and compact local-isometry graph of spaces; paper uses its own link argument. General fast polynomial-growth corollary supplies a **free** action, not automatic properness/cocompactness. |

For the completion interface, the paper uses the one-vertex `K`: its universal 1-skeleton is the Cayley graph for exactly `{x,y,b}`, and the maximal tree is trivial. The lifted two-edge `bx` circle is within one edge of `<bx>`. This is an explicitly stated metric match, not conversion from CAT(0)-metric quasiconvexity. Whether each manuscript application and finite incidence assertion is correct remains the independent mathematical reviewers' responsibility.

## Candidate, limits, follow-up and exact remaining work

`CONTENT_CANDIDATE.md` is conditional explanatory copy and `abstract_original.{tex,txt}` contains the entire original 97-whitespace-word abstract, source-bound by `abstract_receipt.json`. Preserve the title and exact group. Explain the small explicit finite model as the contribution, credit the prior qualitative tools, and preserve unrefereed/AI disclosure. Avoid first-answer, smallest/minimal, dimension-optimal, virtually special, all-free-by-cyclic, or strict-quotient cell-count claims. Do not turn an archived-source check or finite program PASS literal into a proof verdict.

**Follow-up: null.** Minimality/dimension/specialness questions are not automatically recommended merely because the manuscript does not settle them. This scope pass has not established a focused, sufficiently grounded paper-worthy next problem.

The strongest scope conclusion is exact source identity, complete current-reader coverage, a bounded primary-interface comparison and an exact claim/limitation map. Full independent analytic/adversarial proof evaluation, fresh finite controls and replay, root scientific clearance and all publication steps remain outside this scope result. No defect verdict or mathematical promotion is issued here.
