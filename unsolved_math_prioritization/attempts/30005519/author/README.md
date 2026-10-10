# Real subspaces in elementary-symmetric zero sets

Problem **30005519**, catalog rank **799**, code **OWR-13750332-001**.

## Outcome

The exact real, all-ambient-dimensions, even-degree target has a complete affirmative proof in Alper Ferudun's **30 September 2026 unrefereed preprint**, Theorem 1.3 and Corollary 1.4. Its relevant argument was inspected directly in the deposited PDF, including every step in Section 3. This packet gives a credited mathematical reconstruction, with an alternative elementary justification of the coefficient lemma, and reproducible exact controls. It makes no novelty, priority, editorial acceptance, or peer-review claim.

For every positive integer n and even integer r >= 2,

    max{dim_R L : L is a real linear subspace of R^n and e_r|L = 0}
      = min(n, r-1).

The stronger classification in that preprint also checks: for even r >= 4 and n >= r-1, every (r-1)-dimensional such subspace is a coordinate subspace. The main dimension bound holds for real affine subspaces too, by taking their direction spaces. The original target concerns vector subspaces.

The original conjecture is Conflitti (2006), Conjecture 8, p. 224, recalled in Oberwolfach Report 21/2023, p. 1131. The numeric record's cleaned statement asks only this algebraic question. The preceding star-transform question in the report and the preprint is a different target and is not claimed checked here.

## Contents and replay

- `PROOF.md`: self-contained credited reconstruction and hypothesis controls
- `SOURCE_VERIFICATION.json`: source identities, exact corpus hash checks, inspection scope and public publication status
- `PRIOR_ATTEMPT_CHECK.json`: bounded searches of the user's actual repository, distinguishing research artifacts from catalog triage
- `RESEARCH_LOG.md`: one substantive reconstruction/checking approach; early stop after verified prior resolution
- `verify.py` and `RESULTS.json`: exact finite and symbolic controls, not the general proof
- `QUEUE_RECOMMENDATION.json`: proposed disposition, not a remote write
- `AUTHOR_MANIFEST.json` and `verify_manifest.py`: exact frozen payload verification

Run from this directory with Python 3.10+ and SymPy 1.14.0:

    python verify.py
    python -O verify.py
    python verify_manifest.py

Both mathematical runs must reproduce `RESULTS.json` exactly. No source PDFs, source extracts, screenshots, source archives, raw corpora or private coordination files are included. No repository write was performed by this investigation.

## Main source

Alper Ferudun, *Star Transforms Without Type 2 Singular Directions and Conflitti's Conjecture on Elementary Symmetric Polynomials*, version 1.0, 30 September 2026, unrefereed preprint. https://doi.org/10.5281/zenodo.23062557 . Relevant locations: Theorem 1.3, Corollary 1.4, Theorem 1.5; Section 3, pp. 6-8. The deposited PDF is the reading copy actually checked.
