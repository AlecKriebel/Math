# Independent audit of Kirby 2.8

Problem 2756, KP-2.8, rank 908. Audit date: 2026-10-06.

## Decision

**Accept the exact frozen author package as a rigorous partial result, with no required mathematical correction.** This is not acceptance of a solution for arbitrary bridge number. The accepted queue scope remains partial, 3/5 approaches. No novelty is certified.

The accepted author archive is `TANGLE_STABILIZER_2756_AUTHOR_SAFE_FREEZE.zip`, 13,913 bytes, SHA-256 `72f9afea11f77de85242d98b32b8769beafdf33599ea939a93ba923bf897f652`. Its separate external manifest has SHA-256 `2c07eb0303f15e18f7937bc7ec554d0b2384fae38395fa8475334478288a8606`. All seven members, all six internal-manifest entries, and the archive's exact allowlist were independently checked. This acceptance attaches to those bytes. The frozen author's pending-audit fields are historical and are not silently rewritten.

## Formulation and group conventions

A fresh rendering of printed page 90, PDF page 90, of the hash-verified K3 author PDF was visually inspected. The bar over the second tangle is present. The inherited statement loses that bar. The author report correctly recovers the reflected union, common endpoints, distinct trivial-tangle classes, ordinary planar braid group, and unrestricted bridge-number question. The attribution to J. Meier and N. Salter is correct. [K3, Problem 2.8](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

The proof consistently uses orientation-preserving maps, disk boundary fixed pointwise, and punctures permuted setwise. The additional capped point is fixed individually only at the intermediate mapping-class-group stage. The spherical group preserves each ball, and does not include side exchanges. No pure-braid theorem is silently substituted for the full braid group. Reflecting the second ball identifies the two extension subgroups in the common boundary mapping class group; it does not change either extension condition.

## Full preimage and the point at infinity

The key assertion is stronger than identifying the image of a stabilizer: every lift of a spherical extension class must stabilize the planar tangle. The proof establishes precisely this.

For a fixed boundary map f, any two extensions to the ball differ by a boundary-fixing ball homeomorphism. The Alexander trick makes their actions on the boundary-relative tangle isotopy class identical. If the spherical class of f extends over the tangle, choose such an extension with boundary f_0. An isotopy from f_0 to f preserves the finite endpoint set and therefore has constant endpoint permutation. Composing with f_0 inverse produces a path k_t fixing each endpoint individually.

The collar map (x,s) -> (k_(t rho(s))(x),s) is a homeomorphism: its inverse at each fixed s uses the inverse surface map. It matches the identity at the inner collar edge and fixes every radial tangle segment pointwise. Hence it adjusts the tangle-preserving extension to have boundary exactly f.

There is no omitted requirement that the auxiliary spherical isotopy fix the cap or infinity. Compare its final extension with a chosen planar extension of f. Their difference fixes the entire boundary, including infinity, and the Alexander-trick isotopy is relative to that boundary. The compact tangle's track under this isotopy is compact and avoids infinity, so it is a valid half-space tangle isotopy. Thus W_i = q^(-1)(H_i), the whole kernel lies in both stabilizers, K = q^(-1)(G), and q restricted to K is surjective.

This argument uses the standard tame/proper tangle category. It does not assert a result for wild arcs or change the relative-boundary isotopy convention.

## Kernel and splitting

For m = 2n >= 4, cap the boundary by a disk carrying a distinguished point p, then forget p. The first kernel is the central infinite cyclic boundary twist. The second is pi_1(S^2 minus P,p), a free group of rank m-1. The required negative Euler characteristic is 2-m < 0. These are the correct marked-point and capping versions of the standard sequences. [Farb–Margalit, Proposition 3.19 and Theorem 4.6](https://pagine.dm.unipi.it/~a019210/Farb%20Magalit_Primer%20on%20Teichmuller%20theory.pdf).

The resulting extension 1 -> Z -> ker(q) -> F_(m-1) -> 1 splits by choosing lifts of a free basis; centrality makes that kernel extension a direct product. Therefore the accepted sequence is

1 -> F_(2n-1) x Z -> K -> G -> 1.

Only the kernel extension has been split. There is no conclusion that K itself is a direct or semidirect product with G. As an additional check, the n=2 unknot sequence cannot split: a section would embed the nontrivial finite group C2 x C2 into the torsion-free planar braid group B4. This torsion-freeness is also recorded in Farb–Margalit Section 9.1. The original does not make this erroneous splitting claim. The infinite central factor also rules out confusing K with a finite spherical quotient.

## Finiteness and intersection arguments

Lemma 4 is correct. Finite generation lifts through a finitely generated kernel and descends to a quotient. A finitely presented total group has a finitely presented quotient when the normal kernel is generated by finitely many elements as a group: add those elements as finitely many relators. Conversely, finite presentations of the kernel and quotient give a finite presentation of the extension by adjoining lifted quotient relations and the finitely many conjugation relations in both directions. No splitting hypothesis is needed.

Since F_r x Z is finitely presented, finite generation and finite presentation are each equivalent for K and G. The proof supplies a reduction, not generators or relations for an unknown quotient.

The example in F(a,b) x Z is also correct. Both the horizontal copy of F(a,b) and the graph of chi(a)=1, chi(b)=0 are rank-two free subgroups. Their intersection is ker(chi) x {0}. The infinite cyclic covering graph has one independent b-loop at each integer after collapsing its a-line spanning tree. Thus its first homology has infinite rank and the intersection is not finitely generated. This refutes the abstract closure argument; it does not produce a wicket-intersection counterexample.

## Source scope and low bridge number

The five claimed source PDFs were independently hashed, byte-counted, checked for page count, and freshly text-extracted. Their identities and cited locations match the metadata. Source documents and their extracts are excluded from this audit package.

- HIKK uses spherical braids and a further quotient, rather than literally the planar subgroup. Its definition is side-preserving. Example 2.8 includes the trivial knot and gives C2 x C2. Example 2.9 gives finite presentability for any 3-bridge decomposition of a 2-bridge link or the trivial knot. Thus the n=2 index-four F3 x Z subgroup and the n=3 F5 x Z kernel and finite-presentability conclusions are supported. Question 2.10 does not settle arbitrary n. [HIKK, inspected v1](https://arxiv.org/abs/2004.03098v1).
- Brendle–Hatcher Proposition 3.6 supplies a finite presentation for one wicket group. It gives no general intersection-closure theorem. [Inspected v2](https://arxiv.org/abs/0805.4354v2).
- Iguchi–Koda Theorem 0.1 requires g >= 0, n > 0, and (g,n) outside {(0,1),(0,2),(1,1)} for the general distance-at-least-6 conclusion. For (0,n) decompositions in S3 with n >= 3, distance at least 5 suffices. K3's referenced 2020 Twisted book paper is not the correct paper for this theorem. The author's correction to the 2021 Distance paper is correct. No universal unknot finiteness statement follows without the distance hypothesis. [Inspected v2](https://arxiv.org/abs/2105.00631v2).
- The Koda–Tanaka v2 classification is for (1,1)-decompositions, not arbitrary (0,n) decompositions. The 2025-01-27 version and its stated to-appear status were rechecked. [Primary version](https://arxiv.org/abs/2403.15809v2).
- Koda–Takao's double-rectangle criterion is conditional and concerns Heegaard diagrams. Its theorem and corollary do not supply the missing universal bridge-group result. The 2024-04-21 version was rechecked. [Primary text](https://arxiv.org/html/2402.06849v2).

The live problem page was not independently recovered. The author's unsuccessful retrieval is not converted into a current live-site status. The publisher DOI endpoint for HIKK returned HTTP 429 during this audit; the primary manuscript was available, and bibliographic details agree with the author institution's publication record. The optional Koda–Takao abstract-version endpoint failed, while the requested version's full HTML remained available. These retrieval limits do not block the proof-source checks.

## Corpus and artifact verification

The complete catalog, problems, and research-results files match all three advertised byte counts and hashes. There is exactly one exact-ID match in each relevant list. The catalog stores the ID as a string and the full record stores it as an integer; exact comparison was normalized without substring matching. The full record and exact report match the author's private working copies, and the report is empty. The complete default JSON serialization of [record, report], with sorted keys, gives `78431b9e53a607d921c9d20eac15eccdfcc8780e8132abe2bcb030adcb33c8d6`. The statement hash also matches. The inherited material is dated literature triage, with no substantive inherited proof or computation. Only verification metadata is included here.

The author builder was independently copied into temporary relocated directories and run from an unrelated working directory, normally and with Python -O. Both clean builds reproduce the exact frozen ZIP and external manifest byte for byte. Eleven mutation classes in each mode fail closed: unexpected file, missing proof, false solution, wrong problem ID, wrong approach count, false acceptance, directory, symlink, coordination marker, malformed JSON, and empty proof. Total: 24 author-builder cases, all passed.

The separate supplied validator checks the fixed outer ZIP pin, external-manifest pin, all members, inner manifest, and partial scope. Its 19-case suite was run both normally and under -O. Cases include relocation, outer corruption, truncation, external-manifest mutation, individual alteration of all seven members, extra/missing/duplicate members, and path traversal. Inner validation was exercised separately so the outer hash could not mask a missing inner check. Both suites passed.

These are packaging tests, not computational verification of topology. The mathematical result was reviewed deductively. The author package supplies no mathematical checker and claims none. Historical GitHub query counts are bounded author retrieval history, not an independently exhaustive search or evidence of novelty. No repository state was changed by this audit.

## Exact limit of acceptance

No finite-generation theorem, finite-presentation theorem, explicit classification, or counterexample for all admitted n >= 4 unknot pairs is proved. No later-literature nonexistence claim is certified. The simultaneous-complex route still lacks the required connectivity, quotient finiteness, and stabilizer results. The unchanged author artifact is accepted only for its proved reduction, verified low-bridge consequences, counterexample to an invalid abstract method, and appropriately bounded report.

No required repair was found. No corrected derivative is needed. The audit's added explanations clarify the already valid proof and do not replace the accepted bytes.
