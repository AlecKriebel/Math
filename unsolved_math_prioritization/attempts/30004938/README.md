# Totally nonnegative critical varieties: accepted partial results

Problem **30004938** / **OWR-8415362-003**, queue rank **945**.

**Current disposition: unsolved after five substantive author approaches.** The
universal stratified-polytopality target remains unresolved. The accepted bowtie
homeomorphism is an **unstratified** product of two triangles. Neither that result
nor the exact finite combinatorics establishes the source-defined stratification.

## Accepted scope

- The all-n connected-strand displacement bounds reduce rank 2 and corank 1 to
  known top-cell cases.
- The five-strand bowtie critical closure is homeomorphic to
  Delta(2,3) x Delta(2,3), with an exact inverse valid on the entire boundary.
- Two admissible degenerations obstruct extending the unchanged global cyclic
  side-length quotient to that lower cell. This is not a counterexample to
  polytopality.
- The angle-simplex energy is strictly concave for r >= 3. The proposed
  all-graph injectivity argument remains conditional on unproved gauge and
  kernel hypotheses.
- An independent exact periodic certificate confirms 37 proper tube classes
  and cyclohedron codimension counts **1, 37, 189, 304, 152**. The **49** labels
  are combinatorial predicted product-face types. Surjectivity of every
  individual open-face image onto its predicted product-face interior and the
  natural stratification identification remain unproved.

Read the [independent acceptance report](critical_variety_audit/REPORT.md),
[machine-readable acceptance boundary](critical_variety_audit/ACCEPTANCE.json),
and [exact periodic tube audit](critical_variety_audit/tubes/REPORT.md).

## Original history and correction

The five original manuscripts, original checks, and original manifest are
preserved byte for byte under `nonnegative_critical_varieties_30004938/`.
Their statements that review was pending are **historical author-stage status**,
not the current disposition. Likewise, the audit records that no publication or
queue change had been made **by the reviewer at the time of that audit**.
The current accepted scope is stated above and in the acceptance report.

The sole required correction replaces “Grassmann-necklace complements” with
“reduced Grassmann-necklace sets J_r = I_r minus {r}”. It changes terminology
only. The original is retained; the exact one-line
[patch](critical_variety_audit/patches/01_necklace_terminology.patch) and
[corrected standalone copy](critical_variety_audit/patches/02_bowtie_product_topology.corrected.md)
are both included. The verifier applies the patch to a temporary copy and checks
that exactly that manuscript changes and that the result equals the corrected
copy byte for byte.

## Reproduction

Requirements: Python 3, SymPy, and the standard `patch` command. From this folder:

    python verify.py

The verifier checks the full public allowlist, all historical author/audit pins,
the exact patch target, and every saved checker result. It then runs the five
original checks, independent algebra/strand checks, and exact periodic tube/face
certificate on temporary copies. No source document, source extraction, dataset,
network access, or private file is required. Original files are not overwritten.

These are reproducible computations accompanying the mathematical proofs, not a
formal proof verification system. The finite checks do not prove the all-n,
continuity, compactness, or strict-concavity arguments. This package makes no
novelty, human-review, full-stratification, or universal-resolution claim.

Public primary-source titles, URLs, PDF hashes/sizes, and inspection scope are
in [source verification metadata](critical_variety_audit/SOURCE_VERIFICATION.json).
Copied source PDFs, extracted source text, images, dataset contents, personal
data, and private coordination material are excluded.
