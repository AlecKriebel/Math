# Audit and established-theorem boundary: OWR-16635-009

## Status of this edition

This AI-assisted proof reconstruction and internal AI audit are unrefereed. Acceptance in this edition is the audit's mathematical judgment within its explicit imported-theorem boundary; it is not journal acceptance, external human peer review, or formal proof-assistant certification. The AVM source article is separately published in Forum of Mathematics, Sigma (2024). No novelty or new general-family claim is made.

This is a complete authored proof/audit edition, not a computational reproduction package. Finite checks support exact identities only; they do not establish imported vertex-algebra theorems. Source hashes authenticate retrieved bytes, not mathematical correctness. Source PDFs, extracted text, images, programs, and raw outputs are not distributed here.

This file and PROOF.md are complementary parts of the same accepted combined report. This file does not claim a second independent review. The exact accepted result is W_{-14/3}(sl7,(3,2,2)) ≅ L_{-4/3}(sl2) ≅ W_{-8/3}(sl4,(2,2)), for simple graded W-algebra quotients over C with standard Dynkin conformal vectors and common central charge −6.

## Audit of the written argument and its imports

### Main article proofs actually inspected

The complete written proof of AVM Theorem 8.8 was read, including its two parts, not just the concluding formula. It computes current levels, growth, and sine products and invokes Proposition 6.6. The latter's complete proof invokes Theorem 3.10 with the reduction mapping onto the simple W-algebra. The full proof of Theorem 3.10 and the proofs of Proposition 2.9, Theorem 3.5 and Lemma 3.6 were read. Their logical roles are as follows.

- Proposition 2.9 uses the coset Virasoro vector to show the affine map is conformal. A nontrivial coset with positive growth contradicts equality of growth. At central charge zero its proof treats the universal Virasoro radical and the maximal ideal of the source separately; merely knowing the coset central charge is zero would not suffice.
- Theorem 3.5 uses self-duality to rule out a surviving generating singular vector of the maximal ideal of the universal affine algebra. A non-split extension would force two copies of a highest-weight constituent in a cyclic image of a projective module, while Lemma 3.6 permits only one after quotienting by the Casimir. This is a representation-theoretic step, not a numerical calculation.
- Theorem 3.3 then supplies complete reducibility into admissible representations. Corollary 3.9 supplies positive asymptotic dimensions for the possible ordinary simple constituents. Since the vacuum constituent is present and \(V\) is a quotient of \(\widetilde V\), equality with the vacuum asymptotic dimension excludes every extra constituent. This proves Theorem 3.10.

The complete proofs of Proposition 4.2 and Lemma 5.5 were read for self-duality. The complete character-reduction calculation in Proposition 4.9 and the proof following Proposition 4.10 were read. The latter writes out the coprincipal case; the principal case used here is explicitly credited to Kac-Wakimoto [61], with the same sine-limit mechanism. Corollary 3.9's proof was read in full; the principal affine input Proposition 3.7 is itself a cited result [59], while Proposition 3.8 writes out the analogous coprincipal theta calculation. The full available proofs and formulas in Lemmas 8.4 and 8.6 were read, including the portions where the authors omit analogous calculations. Those omitted finite calculations have been supplied for our exact two cases above.

This inspection does not transform every imported lemma into an independently re-established theorem. In particular, the Casimir/projective-cover ingredients of Theorem 3.5 and the affine modular character formulas remain established imported results, even though the way AVM use them was read.

### Explicit external theorem boundary

AVM bibliography numbers are retained here to identify the dependencies unambiguously. The named original works below were identified from the authenticated bibliography; their full texts were not independently proof-audited in this packet.

| Import | Result needed here and location in AVM | Original source boundary |
|---|---|---|
| Admissibility and ordinary affine modules | Type A criterion (9); Theorem 3.3; ordinary weight description on p.15 | [61] Kac-Wakimoto, *On rationality of W-algebras* (2008); [8] Arakawa, *Rationality of admissible affine vertex algebras in the category O* (2016) |
| Associated orbit and reduction | Theorems 3.2 and 4.3; type A partition formula (45) | [10] Arakawa, *Associated varieties of modules over Kac-Moody algebras and C2-cofiniteness of W-algebras* (2015) |
| W-algebra construction and current embedding | Equations (20)-(21), (32), (34)-(35), conical grading and simple quotient | [57] Kac-Roan-Wakimoto, *Quantum reduction for affine superalgebras* (2003); [60] Kac-Wakimoto, *Quantum reduction and representation theory of superconformal algebras* (2004); standard PBW structure |
| Self-duality criterion | Proposition 4.2 invokes [14, Proposition 6.1 and Remark 6.2] | [14] Arakawa-van Ekeren, *Rationality and fusion rules of exceptional W-algebras*; the trace condition is checked in AVM using Lemma 5.5 |
| Affine and reduction asymptotics | Proposition 3.7, Corollary 3.9, Proposition 4.10(1); character quotient (27) | [59] Kac-Wakimoto, *Classification of modular invariant representations of affine algebras* (1989); [61] above; [54] Kac, *Infinite-dimensional Lie algebras*, third edition (1990), theta/denominator formulas |
| Conformality from growth | Proposition 2.9 and Lemma 2.7 | [67] Lepowsky-Li, *Introduction to vertex operator algebras and their representations*, Theorem 3.11.12; [43] Feigin-Fuchs and [58] Kac-Wakimoto for Virasoro structure and asymptotics |
| Descent to the simple affine quotient | Theorem 3.5 and Lemma 3.6 | [58] generating singular vector; [55] Kac-Kazhdan for highest-weight multiplicities; [16] Arakawa-Fiebig, *On the restricted Verma modules at the critical level*, Lemma 6.9; [72] Moody-Pianzola for primitive-vector multiplicities; [8] complete reducibility |

Nilpotent Jordan classification, trace-form normalization, and the dimension formula \(\dim\mathfrak{sl}_n^f=\sum_i(\lambda_i')^2-1\) are standard finite-dimensional linear algebra; all their numerical applications here are shown and checked. The reconstruction does **not** require the row/column-removal theorem, the full Conjecture 8.11, rationality of the W-algebras, the unproved general reduction-simplicity conjecture, or Allegra's thesis. It also does not require Theorem 4.5: using the nonzero reduction as a surjective cover is sufficient for Theorem 3.10. The even-good-grading theorem would give simplicity of the reduction in these type A cases, but is unnecessary for the claim about the simple quotients.

Thus there is no unresolved **specialization-specific** gap. A demand for a fully self-contained proof down to the original character formulas, projective-cover theory and W-algebra construction would exceed the achieved inspection boundary; this packet explicitly does not certify that stronger task.

## Corrections and limits that must accompany reuse

1. Use subscripts for the simple W-algebras. The corresponding universal algebras are not isomorphic: their associated Slodowy slices have dimensions 18 and 7. This follows from the usual associated-variety identification for universal W-algebras, which AVM recall on p.22, and the computed centralizer dimensions. It is not legitimate to change the target to \(\mathcal W^k\).
2. Retain the orbit-closure overbar in Theorem 8.8. Losing it would make the hypothesis false for both examples.
3. At \(m=0\), the table expression \(\mathbb C\times\mathfrak{sl}_m\times\mathfrak{sl}_2\) must be replaced by the actual triple centralizer \(\mathfrak{sl}_2\). The paper's necessity argument through a central level cannot be reused verbatim there. Only the affirmative level is needed, and the direct proof above handles it. No \(\mathfrak{sl}_0\) is invoked.
4. Do not infer the example from the literally printed bound in Conjecture 8.11. The proof uses Theorem 8.8(2) and independently checked hypotheses.
5. The published paper and local preprint have the same relevant theorem numbering, but the second part of the published proof is on p.48, while the local arXiv version has it on p.47. The Allegra paragraph is p.48 in both.
6. The thesis catalog reports a defense date of 11 February 2020 and no attached files; AVM's bibliography labels the thesis 2019. These are different kinds of dates. Neither is silently substituted for the other, and no thesis theorem or proof was read.
7. The exact checker verifies arithmetic and packet integrity only. Successful computation does not independently establish any imported VOA theorem.

## Public source authentication and inspection scope

The workshop PDF was retrieved in full: 756,610 bytes, SHA-256 `b33ed36eaa470877bc6cfb5b45b1019564f568925ea9d94e8dc7ee355879976e`. The local AVM arXiv:2102.13462v3 PDF (21 February 2023, 92 pages) was retrieved in full: 821,728 bytes, SHA-256 `2349653f92ebfa2499ad28e82aaba943ddca51b9da95b2231fb052692cc64cfc`. Retrieval of the complete files does not imply inspection of every page.

The published AVM PDF was accessed as web-readable text for the relevant metadata, Theorem 8.8 and complete proof (pp.46–48), Theorem 3.10 and complete proof (pp.19–20), Proposition 4.2 and conventions (p.22), and the Allegra attribution (p.48). No locally retained published PDF, local hash, whole-PDF comparison with arXiv, or published-page visual inspection is claimed. The arXiv pages listed in SOURCES.json were visually inspected. Allegra's thesis was not retrieved and its proof was not inspected; it is not needed for this proof route.

SOURCES.json preserves the precise source versions, public URLs, retrieval and inspection scope, and public file hashes. VERIFICATION.json separates historical finite checks from publication-edition integrity checks. The seven files other than MANIFEST.json are authenticated by that manifest; its digest is independently pinned in the publication description.
