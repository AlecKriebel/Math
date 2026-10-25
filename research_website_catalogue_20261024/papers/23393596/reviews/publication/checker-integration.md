# Remaining shared checker integration: deep derived pure braids

This editor did not edit or run shared scripts. At preflight, `verification/final-content-check.py` did not register `23393596`. Add the exact source path to `TEX_PATHS`:

```python
'23393596': 'published-source/deep-derived-pure-braids-source-verification-v1.0/note.tex',
```

Use the exact abstract normalization also implemented in the owned `check-bindings.py`:

```python
def normalized_braid_abstract(body):
    for old, new in [('$', ''), (r'\geq', '≥'), (r'\not\subset', '⊄'), (r'\F', 'F'), ('--', '–')]:
        body = body.replace(old, new)
    return ' '.join(body.split())
```

Wire it into abstract token comparison and require full normalized text equality, one paragraph, five sentences and 81 words. Preserve every original abstract sentence, including its 104-crossing phrase. The current TeX SHA-256 is `0f469c9c6c70475bdefac2ea261e7a8cbf2fe5c9e6714447a2a25cd2db0da897`.

Required rendered checks:

- Exact title, author/ORCID, DOI, printed/metadata version 1.0 and 15 October 2026 date; separate creation timestamp `2026-10-15T11:19:16.531335+00:00`. Labels are “Manuscript dated” and “Version 1.0”. No priority or public-availability inference.
- Exactly one distinct four-page reader and one verification ZIP, with the duplicate embedded note.pdf identified as identical. Both original assets linked and served byte-identically; all receipt/source/promotion hashes agree. The ZIP is the standard supplement, not an additional asset.
- Every m≥3 and every finite integer k≥1; ordinary derived P_m; standard oriented closure; integral smooth 1-solvability in Otto Definition 2.3. Witnesses may depend on k; no intersection witness. String-link concordance-class containment, not an operation on closed links.
- Corollary P_m^(n+2)⊄F_n^m for every m≥3 and integer n≥1 only. Preserve the m=1,2 and n=0 boundaries; no rational/topological/surface-braid/lower-central/power-subgroup extension.
- Exact third-derived nested commutator and 104-letter Artin word with ordinary signature −2. No minimum crossing claim or arbitrary-depth explicit word construction. The universal theorem is independent of this finite example.
- Raw signature versus homogenization, nonhomomorphism on P₃ itself, essential positive-power amplification and split-strand transfer.
- Classical signature/quasimorphism/amenability/pointwise-obstruction credit; Harvey's joint work with Park and Ray, exact Question 3, 2017 workshop versus 2018 publication. The finite-example-only Erle printed-index qualification and crossing-based reconstruction must remain bounded as written.
- Root clearance SHA-256 `36b0ccc972b713e507c5ea5a60f86f332fc0668fb9805e8e523d755c6643a871`; all three exact original review objects/hashes; unchanged scope-pending status resolved separately by later root clearance.
- Extensive AI assistance, unrefereed status, passive professional collaboration based on actual contributions, null follow-up, no firstness/current-open claim and no private replay counts or dated audit story in public HTML.

The owned editorial checks are pre-render bindings only. Root must inspect actual generated public text, scholarly/canonical metadata, local PDF/ZIP bytes and links, index/sitemap integration, desktop/mobile/browser behavior and live HTTP before native tracker updates. No public-page approval or publication action follows solely from these files.
