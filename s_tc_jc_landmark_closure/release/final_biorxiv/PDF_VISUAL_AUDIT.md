# PDF build and visual audit

Status: **VERIFIED — v1.1.2**

The canonical submission PDFs and both journal variants were rebuilt from the
v1.1.2 source with `SOURCE_DATE_EPOCH=1786838400`. Repeated builds were
byte-for-byte stable. Tectonic reported no undefined references, missing
citations, or overfull boxes. The lone canonical underfull bibliography line
is visually unobjectionable. Tectonic's bundled `lineno.sty` emitted a
source-comment UTF-8 warning while building the Systematic Biology variant;
the rendered output contains no replacement glyph or malformed text.

| Output | Pages | SHA-256 |
|---|---:|---|
| bioRxiv main | 31 | `80c55068b3a06e1c65ce92265c513f91a039df574ce13bb3f336aefb6e433a13` |
| bioRxiv supplement | 6 | `39b9088d45012ee3cc40b5e407b690b662eb68f2a6fe0232382c576913fa2c44` |
| Systematic Biology main | 41 | `77d4f36a0aef06e29e8899ba15321e8891c34f5b4d42743dab62775fdef3af94` |
| Systematic Biology supplement | 6 | `39b9088d45012ee3cc40b5e407b690b662eb68f2a6fe0232382c576913fa2c44` |
| Systematic Biology cover letter | 1 | `5d7902cd660d12e0cd2b0e5f07306d70ef2f91d20cc7e86688e120e77d42f1be` |
| JMB main | 31 | `a8d8bc5a3f14dfeaf7582898a8107c83ee449ed898e7e47768916e476982ef96` |
| JMB supplement (Online Resource 1) | 6 | `a3e0264a89b727bf84a327ed2d308cb092d3fba08ea3661c254b5553e27b672c` |
| JMB cover letter | 1 | `5f2bde4fc539568e4cf5de9999d39d577d2b72b33efc4f67ba04b92ff52afb62` |

The Systematic Biology supplement is the canonical six-page supplement. The
JMB-specific six-page supplement adds the journal, corresponding-author, and
Online Resource 1 identification required by that journal's instructions.

## Complete-page rendering

Every page of the 31-page canonical article and six-page supplement was
rendered independently by Poppler and Ghostscript at 100 dpi. Every page of
the 41-page Systematic Biology article, 31-page JMB article, JMB-specific
six-page supplement, and both cover letters was rendered by Poppler.
Page-level normalized hash manifests and complete contact sheets are in
`visual_audit/`.

| PDF | Renderer | SHA-256 of normalized page manifest |
|---|---|---|
| canonical main | Poppler | `a64ffb7f0c017a154a6ddf011e4489800c3df80991bfc72e80dd7dfeeb925106` |
| canonical main | Ghostscript | `10dab4e61f1284881f29559faa7237492557b3e77ff808694aeb98bec903e9eb` |
| supplement | Poppler | `9d4bbb70eccfed851cad24ce16edae277d8d303fb089208b6246fbf5c0f9796e` |
| supplement | Ghostscript | `7d6c93f6072a614637c499d203ed9dfda87f49f881932abf339f7c8e8dede6f9` |
| Systematic Biology main | Poppler | `1c7c92896d138c79192d43d77d9c3c7560af51972ab3de481be9283964014e54` |
| JMB main | Poppler | `88ce780eee3d4bac96a97089319beb6defff921616f11448b70de3c622f82109` |
| JMB supplement | Poppler | `90450fcf548219800ff44d53aed8a1a889585cd7bc7307dddf8712353e7f4811` |

Contact-sheet hashes:

- canonical main: `ff5c4e7c81fbbe8d13bc1fd1bc9cb519aaea517d446977ca86d2b54ad91f478d`
- supplement: `ffad5589366defd730e53dadc7904224d7a83ed6354d7f22196eee79b7e68e3d`
- Systematic Biology main: `f6da5c5a0d44e872fefda77ededb798585ecba16802488315a3ea56dc0b0ce5c`
- Systematic Biology cover: `134d42568e24a73c19a54508449bbd253ea705a3e33a0485c5b37cf89bd73cfc`
- JMB main: `d4553d836934ead61b07014ded068d6cbacc818898b7e160d09d182837755507`
- JMB supplement: `1390832cae0510d201b6a0767e57daf3b320a2697c7b511e82539e585fc4f6bc`
- JMB cover: `d4a3a60f7aa3fd4e6005fc4ce1ec5a16f4ede448f6151df20fc229d45a2f318f`

## Inspection findings

The complete contact sheets were inspected page by page, followed by
full-size checks of all dense tables, the theorem/certificate crosswalk,
declarations, bibliography pages, and every figure. The repaired core-atlas
labels and all three triangle-redirection panels remain separated. In the
Systematic Biology variant, continuous line numbers, running heads,
one-and-a-half spacing, paragraph indentation, and seven figure alt-text
blocks render correctly. The JMB variant's `Statements and Declarations`
grouping is complete, its article cites Online Resource 1, and the
supplement's full identifying title block is clean and legible. Both one-page
cover letters are unclipped and legible.

No overlap, clipping, missing glyph, malformed equation, unresolved reference,
illegible table, or broken hyperlink was found. Poppler reports every font in
all eight delivered PDFs as embedded and subsetted.
