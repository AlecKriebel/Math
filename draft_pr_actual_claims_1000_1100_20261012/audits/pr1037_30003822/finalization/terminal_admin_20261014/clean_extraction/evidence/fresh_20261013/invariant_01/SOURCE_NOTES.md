# Fresh primary-source verification

These three bodies were independently fetched on 2026-10-13 after the input pins, and their relevant complete pages were text-read, rendered with Poppler, and visually inspected. All source PDFs, extracted text, page text, and images are confined to sources/rawprivate. No third-party body is an authored review deliverable. Fetch timestamps, URLs, bytes, and hashes are machine-readable in sources/SOURCE_FETCHES.json.

| Source | Exact body | Bytes | SHA-256 | Checked page locations |
|---|---|---:|---|---|
| Caracciolo, Sokal, Sportiello | https://arxiv.org/pdf/0706.1509v2 ; arXiv v2, dated 16 October 2007 on the title page | 536872 | e72bd5a00ac88dd7c94564c058456a2adfe9d11c004d447e3f8fa57823d30ae5 | Printed/PDF one-based 17 and 49 |
| Sportiello thesis | https://pcteserver.mi.infn.it/~caraccio/PhD/Sportiello.pdf ; public 271-page PDF, edition identified here by exact bytes rather than an inferred revision number | 2336644 | 08fd9eaad8f6a79e34d69eeae7f543c6cbbb523c0c8c326bc6179b17ca959e59 | Printed 195,196,197,207,208,211,212,213 = PDF one-based 203,204,205,215,216,219,220,221 |
| Teufl-Wagner problem | https://ems.press/content/serial-article-files/46745 ; Oberwolfach Report 23/2018 | 1261683 | 6512c6b53d12d362868ca481bc7445bb97fc465da1e37d2ffdf40127d600e97f | Printed 1457-1458 = PDF one-based 77-78 |

## What the sources establish for this review

The [2007 v2 paper](https://arxiv.org/pdf/0706.1509v2) announces at printed p. 17 a noncrossing partition basis and Catalan dimension but defers its proof to reference [39]. That reference is marked "in preparation" on p. 49. This body therefore does not itself provide the advertised completed basis proof. The submitted Section 3 supplies its own argument and does not inherit validity from that announcement.

The [thesis](https://pcteserver.mi.infn.it/~caraccio/PhD/Sportiello.pdf) contains the completed basis treatment in Chapter 10, Theorem 10.3 on p. 207 and Lemma 10.6 on p. 208, proved on pp. 211-213. Its equation (10.3), p. 196, defines normalized forest polynomials, including their quadratic zero-parameter limit; p. 197 specifies the polynomial convention. The selected coefficients in the triangular proof are parameter independent and equal to +1 or -1. Thus the normalized polynomial argument supports the zero-parameter basis context. Directly substituting zero into unnormalized scalar products would collapse those products and cannot justify the basis. The nonplanar transfer context is present on p. 195.

The [2018 report](https://ems.press/content/serial-article-files/46745) defines the full Bell-partition matrix on p. 1457 by interlayer subsets combined with arbitrary chosen input-block trees. It asks for the Catalan determinant factor on p. 1458. This matches the submitted scope. The source's noncrossing-free state space and one-count-per-subset conventions are essential.

## Limits of this source check

These source bodies establish the problem match and the lineage of the forest algebra and Catalan quotient. They are not a worldwide novelty search and do not establish current unresolved status or priority. No new-method claim or theorem-priority verdict is made. The invariant-family proof is self-contained and does not require an external Catalan-basis theorem or an unsupported parameter specialization.
