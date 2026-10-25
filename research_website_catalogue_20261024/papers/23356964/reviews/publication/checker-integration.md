# Root integration note — 23356964

This is an instruction record for later authorized root/shared-render ownership. No shared file was edited and no renderer or shared checker was executed by this editor.

The existing renderer's ordinary one-reader/one-supplement schema is used: `generic-wreath-hyperfiniteness-note.pdf`, `generic-wreath-hyperfiniteness-verification.zip`, `additional_assets=[]`. Both original assets are bound to the unmodified receipt. No distinct embedded reader should be advertised: `note.pdf` is byte-identical to the public reader. `publication.json` and `promotion.json` are source-bound preparation artifacts; their state is `BINDINGS_READY_RENDERING_PENDING`.

At this checkpoint `verification/final-content-check.py` has no `23356964` source mapping or abstract branch. Before running it for this paper, the later shared owner should add this source-relative `TEX_PATHS` entry:

```python
'23356964': 'published-source/generic-wreath-hyperfiniteness-verification/note.tex',
```

Normalize the entire actual TeX abstract, not a hand-picked excerpt:

```python
def normalized_wreath_abstract(body):
    for old, new in [('$', ''), (r'G_\delta', 'Gδ'),
                     (r'\Z\wr\Z', 'ℤ ≀ ℤ'), ('--', '–')]:
        body = body.replace(old, new)
    return ' '.join(body.split())
```

Dispatch this normalizer before generic abstract tokenization. The exact paragraph has 93 whitespace-separated words and six sentences and equals the frozen scope candidate and owned `ABSTRACT.txt`. The complete raw body and source hashes are in `ABSTRACT.tex` and `abstract-check.json`.

Scientific checks of the actual generated HTML must preserve the countable discrete **restricted** group; a dense Gδ **subset of the full Polish action space**; hyperfiniteness on the **entire phase space**; and the separate Borel theorem's actual equivariant `p:X→Ẑ`, `p(gx)=p(x)+χ(g)` hypothesis. That theorem allows stabilizers and nonsurjective maps. Generic continuous heights being onto is a consequence of compactness in that setting. No theorem for every Borel action, comeager conjugacy class, Gδ description of the whole property set, or uniform choice across actions is approved.

Check finite Borel asymptotic dimension without asserting finite slab components or a uniform dimension over widths. The divisibility/decreasing-distance argument supplies CJMST's exact metric compatibility. The whole possibly uncountable preimage of the embedded integers needs its height cutoff. The proof is not an arbitrary increasing-union theorem.

Preserve the printed/metadata version `1.0.0`, manuscript date `2026-10-13`, and separate record-created timestamp `2026-10-14T04:32:49.677542+00:00`. Treat the original scope object as custom `SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING`, with its original null mathematical verdict and false publication authorization. Do not demand or fabricate an original scope `PASS`; bind the later root clearance separately.

The original root authority is `verification/root-clearance-23356964-20261025.json`, SHA256 `e845d4a8a6c1db3c442a3d67889bbb5cfe027b5b87897243dc1782935818ca6b`. Exact original report/verdict bytes are embedded by reference and object in `promotion.json`. Reviewer verdicts approve their mathematical scope only. Root must inspect the actual rendered public copy before approving publication.

The final rendered-content gate must also check full abstract visibility, citation metadata, title/ORCID/DOI/date labels, canonical URL, index/sitemap, standard ZIP link, byte-identical PDF links and embed, simple readable desktop/mobile presentation, classical attribution, extensive-AI/unrefereed disclosure, passive contribution-based collaboration and absent follow-up. Keep custody hashes, member/replay counts and dated internal audit narratives off the public page. Then complete root's live HTTP/browser and native Sheet gates; redirects and any release remain later authorized work.
