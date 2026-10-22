# Source identity and actual access scope

`SOURCE_DOWNLOADS.json` binds full-source hashes computed in memory and one-based retained PDF selections. No broad physical source world was copied. Selected PDFs preserve the original page contents; their new-container hashes are in the closed manifest.

| Retained file | Source | Actual read scope |
|---|---|---|
| frank2004_selected.pdf/.txt | [OWR10/2004](https://ems.press/content/serial-article-files/45879), full-source identity:2906417bytes,SHA061421de9750f944d51a8e99f8b85b5f902d997cba873aca38c59bdd582a0d11 | Printed529–531 fully; Frank references through532. Visual529,531. Retained PDF51–54; unrelated next contribution not a dependency. |
| bjs2011_selected.pdf/.txt | [Bownik–Jasper–Speegle2011](https://pages.uoregon.edu/mbownik/papers/44.pdf),180830bytes,SHAfd9fae02b6ed4575fb59db9276d54e7f33b4b4fdee814af05cd29145d1f5c2a8 | Entire10-page paper read; p3255 visually checked. Criterion/proper-subclass evidence, not a classical explicit negative proof. |
| bl2007_selected.pdf/.txt | [Bownik–Lemvig2007](https://pages.uoregon.edu/mbownik/papers/29.pdf),171761bytes,SHA5a2bd018a172d178d3161d000705581548f54e7df3c7a64091a739abffd49cc4 | Printed263–266 intro, definitions, local commutant, propositions and historical correction; not a fresh audit of its full canonical-dual construction. |
| symmetric1998_selected.pdf/.txt | [Frank–Paulsen–Tiballi, arXivmath/9812052](https://arxiv.org/pdf/math/9812052),208844bytes,SHA5c01e3e5e64688900fa1e239013e010365f8348f4484a5d801df006d16127e13 | Intropp1–2 retained/read. Full-web-text term search recovered only introductory wavelet context and bibliography, no explicit wavelet-preservation negative. No full-proof audit claimed. |
| ferudun2026.pdf/.txt | [Ferudun2026 actual paper](https://eulersolve.org/papers/owr-720-011/paper.pdf?v=4c94d59915ef),178311bytes,SHA4c94d59915ef1b90ab1d731e643a8cd6524c616d502fc96e4ed6cb2b12466558 | Intro, Theorems1.1–1.2/Cor1.4,§§2–4 proof of full indexed target; p7 visually checked and retained asPNG. Other stronger conclusions not certified. |
| ferudun_metadata.json | [Publisher metadata](https://eulersolve.org/papers/owr-720-011/metadata.json?v=a9d844677cba) | Full metadata; authored dates/version/title/DOI matched. |
| datacite_record.json | [DataCite DOI registry](https://api.datacite.org/dois/10.5281/zenodo.23438995) | Full metadata; independent DOI identity/state/registration dates verified. |

Successful visual inspection of Frank529,531 and BJS3255 occurred before their PNG renders were removed to relieve an actual disk-full condition. Their selected primary PDFs remain available for re-rendering. No modification of original page contents occurred. Ferudun p7 PNG remains.

Access limits: direct1990 Daubechies author-host PDF retrieval timed out via both tools and command-line GET. Direct2002 Daubechies–BinHan PDF was partially exposed by web metadata/first pages, but attempts to retrieve p271 or full bytes timed out. Alternative author-host spellings also timed out. No fresh visual/complete primary inspection of those historical pages is claimed. The2007 paper and2026primary preprint corroborate older dual history; the PR's precise1990 Lemarié attribution and2002equation1.6 remain credited but not newly authenticated here. Han2003 AMS PDF returned403, so its detailed Question4 wording is not independently certified from the publisher text. Frank2004 primary itself suffices for the audited target and inverse convention.

Direct Zenodo API/DOI landing returned403; DataCite public API and author-hosted publication/PDF succeeded. The current PDF's public hash is pinned, but a historical archived-file checksum at17October was not independently recovered. No access restriction was bypassed.

No third-party author was contacted. All27PRblobs are identity-bound; complete manuscript/audit read scope is listed individually in `PINNED_MEMBER_HASHES.json`.
