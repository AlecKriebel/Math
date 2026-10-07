# Output-sensitive sparse factorization over finite fields

The current manuscript adds complete sparse-input factorization with arbitrary binary multiplicities, in bit complexity polynomial in term count, binary degree, explicit field encoding and the total degree of all distinct densely returned factors. Its proof maintains a sparse numerator and a dense denominator through pth-root descent, bounding denominator growth by the original radical degree per level.

The requested dense factorization and prescribed-degree irreducible/extension construction are established as inherited consequences of the audited OpenAI prime-field theorem through Berlekamp, Shoup and Rai. The new contribution is the repeated compressed representation and degree invariant. Padé, logarithmic derivatives, known-root residue methods, Cartier identities and p-residue descent remain attributed to their original sources; no first-priority assertion is made.

Current workflow status: the revised manuscript and feasible reductions are being packaged for fresh complete reviews. Production Zenodo publication and DOI tracking have not yet occurred. Follow PUBLICATION_DECISION.md and the dated RESEARCH_LOG_CONTINUATION.md for current decisions. RESEARCH_LOG.md, reviews/FINAL_STATUS.md and artifacts/finite_fields_research_record_v3.zip preserve the historical dense-only record; its three reviews and withheld-publication decision do not certify the newer theorem.

The exact model and limits are in CURRENT_THEOREM.md and DEPENDENCY_LEDGER.md. SPARSE_CANDIDATE_DERIVATION.md gives the detailed sparse proof. manuscript/main.tex is a standalone source, and manuscript/paper.pdf is the exported paper. publication/README.md gives static package, reproduction, rights and disclosure information. Full source/priority audits and independent prototypes are under agent_notes/. Research-only downloaded third-party PDFs, caches, pinned source trees and credentials are excluded from intended uploads.

From a finalized extracted package, run:

    python3 code/reproduce.py --fileset PUBLICATION_FILESET.json --receipt receipts/clean_reproduction.json --compile-pdf

For a quick sparse-only check from code/:

    python3 -m unittest test_sparse_cartier -v

Python arithmetic checks use only the standard library. Export builds use Tectonic 0.16.9 and Poppler for verification; the native desktop LaTeX compiler is also used. The bounded prime oracle is toy-only, and no implementation of the enormous uniform prime-field branch or practical-efficiency promise is supplied. No relevant Lean build/full-follow-on formalization is claimed.

Author Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. No affiliation or coauthor is asserted. AI tools were used extensively; no conventional human peer review/refereeing has taken place. Newly authored prose/data are CC BY4.0, Python MIT. No outside individual was contacted. The persistent publication objective is incomplete until production publication and exact tracker read-back are confirmed.
