# Classical and mechanism priority audit

PR 894 · PID 30005737 · candidate head `401f86e018e8cc5075e37a29bae9350eb9f89c36` · 16 October 2026 UTC. This audit follows separately authorized mathematical review. It does not redo mathematical acceptance. The original mathematical effort remains 1/5, unchanged. The separate 5% figure was the parent’s initial export validation checkpoint; it is not a discovery-completion percentage or a conversion of the effort count.

## Decision

**No inspected primary theorem resolves the full target under matching assumptions. This is bounded evidence, with a material classical-source access limitation, and does not certify firstness or present openness.** No verified prior full resolution is flagged.

The strongest mechanism overlap is classical: Baues's 2008 determinant-relative-invariant argument for étale affine actions. The paper should acknowledge this comparison before any public priority assessment. The exact general application to a complex semisimple group was not found in the inspected bodies.

The closest exact-target partial results are in Burde–Dekimpe–Monadjem's 2023/2024 paper: Theorem 3.10 (target sl3(C)), Proposition 3.11 (simple Levi factor and irreducible abelian radical, arbitrary semisimple target), and Proposition 3.12 (target sl2(C)⊕sl2(C)). Its introduction leaves the unrestricted case conjectural. That is a statement about that dated body. [8 March 2024 author version](https://homepage.univie.ac.at/dietrich.burde/papers/burde_78_perfect.pdf).

For the stronger unimodular formulation, the closest early obstruction is Burde–Dekimpe, Theorem 3.3: semisimple target and **solvable unimodular** source. Its proof places both projected images in Borel subalgebras using solvability. It does not cover a nonzero Levi factor. [2012 author version](https://homepage.univie.ac.at/dietrich.burde/papers/burde_44_postlie_der.pdf), [2011 arXiv submission record](https://arxiv.org/abs/1108.5950).

## Authentication and scope

All 18 candidate source files (91,564 bytes) match the 4,654-byte external manifest, SHA-256 `1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c`. The complete native pair is 3,524 bytes, SHA-256 `b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298`. Both records were fully read; record 2 is empty. Every pin is in AUTHENTICATION.json.

INDEPENDENT_SCOPE.md was frozen before reading the authored proof, SOURCES, READINESS, or old priority/acceptance material. No old audit or acceptance conclusion was used for this decision.

The full target is finite-dimensional **complex** Lie algebras on a common vector space, with g perfect nonsemisimple and n semisimple: no post-Lie structure exists on (g,n). The stronger candidate replaces perfectness by unimodularity and assumes homomorphisms j1,j2:g→n with invertible difference, concluding g semisimple.

Their graph h={(j1(x),j2(x))} complements Δn in n⊕n: invertibility gives injectivity, trivial diagonal intersection, and the required dimensions. Integration gives an infinitesimally simply transitive left-right action on the simply connected complex group N. An open orbit at the identity is weaker than transitivity everywhere. The candidate supplies the latter bridge by determinant covariance.

The graph formulation is an existing post-Lie tool, not a new correspondence. It appears as Proposition 2.16, p.7 in the inspected arXiv body of [Burde–Dekimpe–Vercammen](https://arxiv.org/abs/1109.0251), and as Proposition 2.6 in the 2024 perfect-paper body.

The general target conjecture occurs at printed p.2689 of OWR 46/2023, after its sl3(C) proposition; workshop 15–20 October 2023. Native metadata saying “(2024)” must not replace that report identity. [Official report](https://ems.press/content/serial-article-files/48175).

## Distinct classical routes

| Route | Primary passages inspected | Overlap and exact gap |
| --- | --- | --- |
| Étale affine actions | Baues 2008, §5.4.1 equation (5.3), Theorem 5.19 pp.44–45, Corollary 5.20 | **Close mechanism predecessor.** A determinant transforms by inverse adjoint determinant times a volume character. Trivial character forces constancy from an open orbit; all orbits become open. The stated theorem acts on affine space. |
| Reductive complements | Koszul 1978, unnumbered theorem p.547 and entire proof pp.547–551 | **Conditional theorem.** Both complementary subalgebras must be reductive in the ambient algebra. In Δn⊕h, that property of h is unknown; unimodularity does not supply it. |
| Onishchik decompositions | BDM 2022, Lemma 2.6 p.4 and Theorem 2.7 pp.4–5; attempts to retrieve the 1969 original | **Modern derivation checked; original body unavailable.** The checked result uses two semisimple summands. h is not known semisimple. No claim is made that every relevant theorem in the 1969 body was excluded. |
| Semisimple-source rigidity | BDM 2022, Theorem 3.3 p.6 | **Input direction mismatch.** Its source must already be semisimple. |
| Rota–Baxter structures | Burde–Gubarev 2018/2019 body and author annotation dated 2023, §§2–4 | **Tools and special cases.** No arbitrary unimodular-source theorem found; see correction below. |
| Global skew braces | Damele–Loi v1 (2025), v3 (2026), Theorem 1.1, post-Lie identities, Definition 2.10, proof of (R2) | **Global integrability and source roles matter.** Circle bracket is source g; semisimple circle group therefore means semisimple-source rigidity. |
| NIL-affine completeness | Deré–Origlia 2024, Theorems A/B, 2.9, 4.10 | **Target-class mismatch.** Completeness criteria concern nilpotent/2-step nilpotent targets. |
| Topological braces | Damele–Loi 2026, main theorem and Proposition 3.9 | **Target-class mismatch.** The affine-action theorem assumes solvable underlying target group. |
| Group topology | Etingof 2024, polar decomposition, Theorem 49.1 and Corollary 49.6 | **Classical tools.** They give compact-form homotopy type after integration, not transitivity from infinitesimal data. |

Baues's proof is materially the same style as the candidate's essential determinant step: relative-invariant covariance, character triviality, constancy on an open orbit, then constancy globally. The candidate uses a holomorphic function on a semisimple group instead of a polynomial on affine space. Its final compact-form homology obstruction also uses classical Lie theory. This is an attribution recommendation, not a firstness claim. [Baues primary body](https://arxiv.org/pdf/0809.0824v1).

Embedding N in matrices does not provide the étale affine representation required by that theorem: the ambient matrix-space dimension differs, and N is not the whole vector space. Local coordinates do not give a global affine action. Importing the candidate's transitivity argument to fill this gap would not demonstrate a previously published theorem-level corollary.

Koszul's proof was checked beyond its theorem statement. An initial step uses unimodularity, but subsequent cohomological and decomposition steps explicitly use reductivity. Removing that hypothesis would be an additional mathematical argument. [Original primary body, received 25 July 1977; published 1978](https://ir.library.osaka-u.ac.jp/repo/ouka/all/4821/ojm15_03_05.pdf).

The old solvable-source theorem cannot simply be applied to rad(g): restriction need not give an invertible difference onto a semisimple target of the same dimension. Likewise, an algebraic or closed-image factorization theorem requires its actual global hypotheses; local complement data alone are insufficient.

## Version and correction traps

The author's Rota–Baxter PDF dated 15 May 2023 explicitly warns before Proposition 3.6, p.9, that it is incorrect and that its proofs of Propositions 3.7–3.8 are invalid, pointing to replacement proofs. The inspected older arXiv body lacks that warning. Do not treat the unrestricted-sum proposition as a prior resolution. [Annotated author body](https://homepage.univie.ac.at/dietrich.burde/papers/burde_59_rota.pdf).

Burde–Moens 2022 explicitly gives nonsemisimple disemisimple examples and characterizes their nilradicals via prehomogeneous modules. The correct later rigidity theorem uses a **direct** vector-space sum of semisimple subalgebras. None permits assuming the unknown complement is semisimple. [2022 primary body](https://homepage.univie.ac.at/dietrich.burde/papers/burde_74_prehom.pdf).

Brace Theorem 1.1(R2) changes from group isomorphism in v1 to local isomorphism in v3, dated 25 February 2026. The paper explicitly distinguishes existence of an infinitesimal post-Lie product from integrability into a global brace. This prevents using global existence tables as a full answer here. [Version history](https://arxiv.org/abs/2507.06214).

Some served arXiv v1 PDFs contain later internal Date lines (2011 watermark/2021 internal date; 2015 watermark/2018 date). The ledgers record both; render dates are not silently treated as new manuscript versions. The perfect-paper arXiv record lists only v1 submitted 15 November 2023; its separately inspected author body is dated 8 March 2024.

## Coverage and limitations

SEARCH_LEDGER.json records 54 fresh queries, the returned URLs, and timestamp precision across factorization, diagonal complements, unimodularity, left-right actions, étale representations, post-Lie/Rota–Baxter work, and 2025/2026 developments. Primary version pages and the current author-publications list were checked. A URL appearing there does not establish that its body was inspected; BODY_LEDGER.json gives that distinction.

Five supplied official bodies were reused after independent size/SHA verification. Fourteen additional PDF bodies were successfully fetched and extracted. Only the listed portions are claimed inspected; Koszul's short proof was read throughout. Original Onishchik 1969 requests timed out or redirected, and IOP returned an HTML bot challenge. A failed find on a redirected home page is **not** absence of text from the PDF. Lancaster's supplements paper timed out and is not claimed inspected. No access challenge was bypassed.

Intermittent ENOSPC caused failed source-read launches, raw-response writes, report writing, and a ledger write. Failures/retries and response pins were preserved where available. Only this audit's own raw or redundant copied captures were removed. No foreign cleanup, Git mutation, publication, remote PR write, contact with people, or messaging of other agents/chats occurred.

Recommended public wording: “We give a proof of the perfect-source/complex-semisimple-target conjecture formulated in OWR 46/2023 via a stronger unimodular-source obstruction, using classical determinant-relative-invariant and Lie-group topology methods. Our bounded search did not locate a prior general resolution.” Add the early solvable-source theorem, Baues mechanism, BDM partial results, and global-integrability distinction. Avoid “first proof,” “new mechanism,” “still open today,” and “exhaustive priority clearance.”

Further direct inspection of Onishchik's 1969 body and older general homogeneous-action completeness results would improve priority confidence. This is recorded as a research limitation without preparing outreach. Oldest full resolution: **not established by this audit**. The missing Onishchik body is a bounded-coverage limitation, not a concrete possible prior full theorem identified by this audit.

