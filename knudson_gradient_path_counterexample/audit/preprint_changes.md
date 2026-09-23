# Preprint-readiness revision 1.0.1

The user requested successive fresh adversarial reviews, fixes propagated to
all current materials, and a final clean pass. Journal submission is outside
this revision's scope. Historical audit files retain their original wording,
hashes and version numbers; they are records of earlier states.

## Accepted corrections

1. **Citation schema error (packaging, substantive):** version 1.0.0 used
   `type: article` at the CFF root, which only permits `software` or `dataset`.
   The CFF now describes the verification package as software and sets the
   paper as its `preferred-citation` of type article. Validation uses the
   [official CFF 1.2.0 schema](https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json).
2. **Standalone preprint discoverability:** the PDF now links directly to the
   companion page with scripts and audit materials; its title and author are
   also embedded in PDF metadata. The bibliography mentioned in the priority
   qualification is directly linked.
3. **Expository precision:** define a critical simplex explicitly and describe
   the first descent and each matched upward step of an edge-to-vertex path.
   Clarify that filtration indices order the simplices while the field is
   constructed from persistence pairs. The theorem and computations are
   unchanged.
4. **Global revision:** update the current paper, citation, readme, site,
   verification report, Zenodo metadata/instructions and archive version to
   1.0.1. Regenerate the PDF, archive manifests and public copies together.

## Review status

[Fresh round 1](preprint_round1.md) passed the mathematics, source
interpretation and reproducibility of the 1.0.0 snapshot, and recorded the
CFF correction. [Fresh round 2](preprint_round2.md), conducted by a new agent
on the revised 1.0.1 snapshot, found **zero actionable mathematical,
bibliographic, PDF, metadata, or package defects**. Its independent proof route
explicitly decomposes the persistence module using a filtered triangular
basis; the finite intervals identify the same three persistence pairs.

The requested review/fix/fresh-review loop is complete. No unresolved
preprint blocker was identified. The original limitations concerning
historical priority and lack of external human peer review remain explicit;
this verdict is not a claim that those uncertainties have been eliminated.

The reviewed manuscript, PDF, verifier scripts, citation and Zenodo metadata
remain frozen after the clean round. Only review records, documentation of
the completed process, archive manifests and deployment evidence are appended.
Final clean-extraction and live-file checks accompany publication.
