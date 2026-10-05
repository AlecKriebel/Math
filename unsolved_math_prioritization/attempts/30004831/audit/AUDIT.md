# Independent adversarial audit: 30004831

## Verdict

**PASS.** The original unrestricted question is false. Accept the credited existing-resolution classification `already_solved`, with **0/5 new research attempts**. Mathematical credit belongs to Ruipeng Zhu's Example 4.11. The packet provides a correct, convention-consistent order-two reconstruction, rather than a novel counterexample.

The reviewed input is the eleven-file author freeze with archive SHA-256 `42c545640e66d6ee85dec4d0035ca9b834f733d40baa6f8ec731060586a8aa40` and author-manifest SHA-256 `ce591fbb475041f39c5b6df4e4bafb535f534f1a6c7abd2dc8e439c2314ddf52`. Its bytes are retained unchanged under `author/`. Historical claims there that an audit is pending are preserved as part of that freeze; this report records the completed audit.

This is an independent AI-assisted mathematical audit, not journal peer review, formal verification, an exhaustive priority certificate, or a claim of community acceptance.

## Exact target and source attribution

The dataset identifiers and statement hash match exactly. The official original is Bichon's Question 1, printed page 2413 of Oberwolfach Report 44/2021, PDF page 17. I independently retrieved the complete report and inspected that page in text and rendered form. Smoothness, cosemisimplicity and finiteness appear in a following list of positive special cases; they are not assumptions of the question. [Official report](https://publications.mfo.de/handle/mfo/3899).

Zhu explicitly presents the negative construction in Example 4.11. Its attribution is independently corroborated by Bichon's February 2026 introduction. The publisher and Crossref list Zhu's article in volume 229, issue 12, article 108123 (December 2025). The actual mathematical bytes inspected here are arXiv v2, not the journal's final PDF. Bichon's 2026 version is reported as a preprint, not as accepted work. [Zhu v2](https://arxiv.org/abs/2501.02828v2), [publisher](https://www.sciencedirect.com/science/article/pii/S0022404925002622), [Bichon v1](https://arxiv.org/abs/2602.12731v1).

## Proof review

1. **Algebras and normal forms.** The skew-Laurent polynomial construction and the monic central quadratic relations justify a basis with every integer Laurent exponent and skew degree zero or one. In particular the algebras are nonzero, and no completion or quotient at a numerical value of the Laurent generator is being taken. Characteristic zero makes the sign relation and the averaging denominator valid.
2. **Hopf structures.** Both quadratic relations survive the displayed coproduct because the mixed terms cancel. The antipode is an anti-homomorphism, satisfies both convolution identities, and squares to the sign automorphism on the skew generator. Thus the antipodes are bijective and their fourth powers are identity.
3. **Bicomodule algebra.** The proposed right and left coactions preserve all relations. Left coassociativity uses the corrected left coproduct. Commutation of the two coactions holds on the generators, hence on the algebra.
4. **Galois property.** I checked the canonical-map formulas, including negative powers and multiplication order in both subtraction terms. Each map is triangular on the stated module bases with invertible diagonal coefficients. The displayed inverses are therefore genuine two-sided inverses on the full vector spaces, not only on a bounded computational sample. Coefficient comparison yields scalar coinvariants on each side. Nonzero vector spaces are faithfully flat over the field.
5. **Tensor equivalence.** The L-H-bi-Galois object yields the strong k-linear monoidal equivalence from right L-comodules to right H-comodules, by cotensoring on the L side. The theorem invoked is Schauenburg's bi-Galois characterization, in the explicitly inspected statement of Bichon 2022, Section 2.2, printed page 565. This is a standard external categorical input, not proved by the tests. [Bichon 2022](https://www.numdam.org/articles/10.5802/crmath.329/).
6. **Upper bound for H.** With D=C[x,(1-x^2)^(-1)], the presentation indeed becomes the rank-two crossed product D+Dg. This identification follows in both directions from g^2=1-x^2 and g^(-1)=(1-x^2)^(-1)g. D is a PID, and H is free on both sides over D. The averaging map m -> (1 tensor m + g tensor g^(-1)m)/2 splits induction followed by multiplication and is H-linear, including the twisted g^2 relation. Thus every H-module has projective dimension at most one; this argument is not confined to finitely generated modules.
7. **Lower bound for H.** The central element x^2 is regular and generates a proper ideal. A projective quotient H/Hx^2 would force a left-module splitting whose complementary summand is annihilated by x^2, contradicting regularity. Consequently the upper bound is attained. An independent nonsplit two-dimensional module extension in `DIMENSION_CONVENTIONS.md` supplies a second lower-bound witness for the trivial module itself.
8. **Infinite dimension for L.** The embedded dual-number algebra E=C[y]/(y^2) has L free as a left module. Restriction therefore preserves projectives. The infinite periodic E-resolution has nonzero Ext against the trivial module in every degree. A finite L-projective resolution of its trivial module would contradict this. No false claim that arbitrary subalgebras preserve projectivity is needed; freeness was established explicitly.
9. **Dimension identification.** The claimed equality of global dimension, projective dimension of the trivial module, and Hochschild dimension is valid for Hopf algebras. It does not mean that self-Ext of the trivial module alone detects the dimension. The additional elementary justification and a warning example are in `DIMENSION_CONVENTIONS.md`.
10. **Hypothesis exclusions.** Both algebras are infinite-dimensional affine noetherian PI algebras. The displayed nonsplit two-dimensional comodule extensions show they are not cosemisimple. L is not homologically smooth. The example therefore cannot contradict results assuming both algebras smooth, both dimensions finite, or cosemisimplicity. Bichon's Theorem 3.5 requires both global dimensions finite, not finite vector-space dimension.

## Source-display reconciliation

The two cautions in the author packet are accurate for the retrieved Zhu v2 page 22 and were independently checked visually:

- Its left coproduct orientation does not match its left coaction. Reversing that coproduct and the corresponding antipode gives the compatible version used in the proof. This is an explicit convention repair; the inconsistent literal pair is not endorsed.
- The inclusive normal-basis endpoint is incompatible with the quadratic relation at n=2. The degree range must be zero or one. The proof avoids inferring convolution invertibility merely from linear bijectivity and establishes the canonical maps directly.

At n=2, the corrected L is even Hopf-isomorphic to the displayed source version: send its source Laurent generator to h^(-1), and its source skew generator to h^(-1)y. Indeed Delta(h^(-1)y)=1 tensor h^(-1)y + h^(-1)y tensor h^(-1), and the algebra relations are preserved. Thus the order-two reconstruction retains the claimed Hopf-isomorphism class.

These display issues do not invalidate the negative answer: the corrected specialization is verified in full. No journal erratum is asserted, and no assertion is made about the uninspected journal PDF's exact displays.

## Reproducibility and adversarial controls

- The frozen 4,543 author assertions reproduced exactly, including its two source-display controls.
- An independently written implementation performs 2,902 assertions using sparse exact Laurent matrices and the opposite PBW ordering; it imports no author code.
- The independent tests include 313 deliberately false variants: wrong signs in both canonical inverses, reversed coproduct, wrong square relations, commutation in place of skew-commutation, and omitted averaging normalization. Every variant is detected.
- Seven controls on the author packet and seven on the audit packet reject changed or missing payloads, extra files, extra directories, symlink payloads, a rebound author manifest, and an incorrect external manifest pin.
- The audit's strict file-set and payload verification runs before both mathematical scripts. Finite computation corroborates, but does not replace, the unbounded mathematical argument or the categorical theorem.

## Provenance and attempt accounting

All three complete local datasets were independently reread and hashed. The exact statement and identifying fields match; no exact research-results record was found. The catalog review hash, omitted from the author's public summary, is recorded in `DATASET_RECHECK.json` as a nonblocking metadata addition. It is an extracted catalog field, not a newly inferred or independently recomputed review-policy hash.

The prior-attempt check was independently repeated through read-only repository queries: exact-ID code, commit, branch and PR searches, problem-number code search, monoidal PR search, and examination of the two unrelated Hopf PR hits. The pinned default-branch attempts directory had 62 entries and lacked this target; the exact directory returned 404. This is bounded evidence only, not an exhaustive search of every branch's files or every historical revision. There were no remote writes.

The stopping reason is verified scholarly prior resolution, not a prior user attempt and not the dataset's stale positive-only triage. Reconstructing and auditing known mathematics is verification work, so it does not consume a new research approach. Retain 0/5.

## Corrections and limitations

No mathematical correction to the frozen author proof is required. The audit adds the review-hash metadata and a more explicit dimension explanation. Keep the source-display warnings, attribution, and distinction between unrestricted and both-finite statements in any publication. Do not promote the finite checks to a machine proof or represent this packet as a new solution.

The live problem page was not independently text-verified, the final journal PDF was not retrieved, and Schauenburg 1996 was not freshly inspected in full. The target is instead pinned by the supplied complete datasets and the official original question; the categorical theorem is read in the primary 2022 article. These disclosed limitations do not leave a gap in the stated negative answer.
