# Exact content review: earlier Yang–Baxter edition 21971507

2026-10-10T21:27:21.499462+00:00. Source/content proposal checkpoint: 80% complete; independent cross-review and publication remain root-owned. No remote metadata mutation.

Record: **An exceptional four-dimensional unitary Hecke Yang–Baxter operator**, DOI **10.5281/zenodo.21971507**, manuscript/package version **1.1.3**. Published 2026-08-17; native submitted date 2026-08-16. The deposited 12-page manuscript is dated 16 August 2026. Full exact extracted text was read, including definitions, every main construction/proof, limitations, declarations and references; first-page visual inspection confirmed its title, author, mathematical parameters and printed keywords. The single PDF is 131,746 bytes, MD5 **3f65c5978bb5b4719224e6463e8a5abb**, SHA-256 **f119f7a33285f37017ed4c76a964ae6d6d17415e03c7503e9bc079f7a96a93bb**. Downloads, text and checksum evidence are bound in `OLDER_YANG_BAXTER_SOURCE_CATALOG.json`.

Proposal: `patches/21971507.json` changes **keywords only**, preserving all five existing keywords and adding twelve manuscript-supported specialist terms (17 total). Its SHA-256 is **5523c65426a5692c6394d2981e49394e64e69afaa5ee47c7eb90ba15ad1f2a1f**. English is already recorded as `eng`, so there is no language change. Title, original description, creator/ORCID, submitted/publication dates, version 1.1.3, license, resource type, access, files, identifiers and complete two-record version history remain untouched.

## Checkable keyword evidence

| Terms | Exact content evidence |
| --- | --- |
| Yang–Baxter operator; Yang-Baxter equation; unitary R-matrices | Abstract and §1, pp. 1–2, define the unitary operator and ordinary braid/Yang–Baxter identity; Theorem 1.1 constructs the 16×16 operator at q=exp(iπ/3). |
| Hecke algebra; braid group representation | §1 Theorem 1.1 and §5, pp. 2, 5–7: specialized Hecke algebra representation with braid/far-commutativity and quadratic relations. |
| unitary localization; fusion category; C(sl3,6); Jones-Wenzl representations | Abstract, Theorem 1.1, §5 Proposition 5.1 and the paragraph preceding Corollary 5.3 identify the faithful quotient tower H_n(3,6) with the C(sl3,6) Jones–Wenzl representation sequence. |
| H_n(3,6); Markov trace; partial trace | §5 pp. 5–7 proves the η=1/2 Markov trace identity from scalar partial traces, identifies the annihilator with the representation kernel and proves compatible faithful embeddings. The matrix part of Theorem 1.1 on p. 5 proves both unnormalized partial traces equal twice the identity. |
| Pauli-Clifford expansion | §2 equation (2), p. 3 gives five real Pauli–Clifford words. §3 constructs the anticommuting involution circle; §4 Proposition 4.1, pp. 4–5 derives the finite 18-word cubic certificate and four allowed signed points. |
| Rowell-Wang localization conjecture | §5 Corollary 5.3, p. 7 verifies the conjecture for the simple C(sl3,6) tensor generator; it does not establish the general conjecture. |
| generalized Yang-Baxter equation | §7 Proposition 7.1, pp. 9–10 derives a (3,2)-generalized operator after a within-site qubit swap and gives exact all-strand chain conjugacy/far commutativity. |
| minimal local dimension | Corollary 1.2 and §6, pp. 2, 8–9 exclude dimensions 1–3 and supply dimension 4. The dimension-three step explicitly depends on Lechner's classification and Markov-character results. |
| exact symbolic verification | §8, p. 11 documents three exact routes: hardened SymPy, separately written sparse exact arithmetic, and matrix-free Pauli words; negative tests and frozen outputs accompany the source package. |

## Scope, assumptions and provenance preserved

The proof localizes the entire quotient tower using faithfulness of normalized matrix trace, rather than relying on a two-site numerical test. It cites GHR to identify the quotient tower with the desired fusion-category representation. Dimension-two minimality uses the published GHR obstruction; dimension-three minimality uses Lechner Lemma 3.1/Theorem 3.4 and exact three-strand obstructions. The metadata does not remove these dependencies or suggest a new full classification.

§6 provides amplification to dimensions 4m and explicitly leaves dimensions 6, 10, 14, … open. §7 distinguishes the operator's (3,2) tensor placement from the known GHR (3,1) operator, while observing that equal bare spectra permit unitary similarity after forgetting tensor structure. This edition does not identify an intertwiner with the known quaternionic (3,1) model. No quaternionic factorization, Turaev enhancement, HOMFLYPT polynomial, finite-image, branched-cover or polynomial-time keyword from the later edition was imported.

§8 discloses AI-assisted numerical discovery and that discovery code/random seeds were not retained. It disclaims reproducibility, exhaustiveness and uniqueness of that search; finite checkers do not replace the tower proof, classification step or priority assessment. §9's literature search is explicitly limited to 16 August 2026 and does not prove absolute priority. The manuscript's generative-AI declaration and sole-author responsibility remain in the unchanged PDF; its original preprint metadata and description are untouched. No claim of uniqueness, priority or completeness is introduced by the keyword proposal.

## Preservation route and baseline

`receipts/21971507/before.json` records current legacy/native metadata, original full native file object, record/version/concept DOI and OAI, and complete native registry [21971507, 22013710]. `original_legacy.json` preserves the additional owned-list record; `original_native.json` preserves the full current native public record. The baseline reports **legacy_compatible=false** because native metadata retain the exact submitted date 2026-08-16 that the legacy projection does not preserve. Use the existing reviewed **preserving native metadata route**, with exact final DOI/OAI, concept/version-history, raw files and rich-field equality. Do not apply the legacy wrapper.

`OLDER_YANG_BAXTER_PROPOSAL_QA.json` binds the patch checksum and records retained keywords, English, unchanged title/version/DOI and required route. The only remaining content gap is independent cross-review of this proposal; root alone approves and applies it.
