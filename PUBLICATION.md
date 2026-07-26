# Publication record

The public repository `AlecKriebel/Math` was created at **21 July 2026,
13:11:39 UTC** (**21 July 2026, 06:11:39 PDT**).

That second-level timestamp is encoded in the two original archival notes,
their rendered PDFs, and their web pages. It is the repository creation time
returned by the GitHub API. The initial commit is
[`c2e0a79d28b2f532d4a7442028889770a477cf17`](https://github.com/AlecKriebel/Math/commit/c2e0a79d28b2f532d4a7442028889770a477cf17).

The first commit was made one second earlier and contained release-time
placeholders. The immediately following publication-fix commit replaces them
with the repository's immutable creation time. This history is intentionally
preserved rather than rewritten.

Exploration 03, now titled “An explicit 44-variable vanishing witness from a
22-variable cubic Keller map,” was first released at
**21 July 2026, 14:42:57 UTC** (**21 July 2026, 07:42:57 PDT**). This is the
author and committer timestamp of the release commit.

A priority correction was posted at **21 July 2026, 15:20:23 UTC**. It records
that an equivalent six-variable symmetric transport was already public in
Eliott Cassidy's repository and that William Thompson had priority for the
rank-compression idea. The original release timestamp and Git history remain
unchanged.

Exploration 03 was the **canonical consolidated paper** for Explorations 01-03
at that stage of the notebook. Exploration 01 is archival because its
monodromy theorem was already available in stronger form; its uniform rational
collision survives as Appendix A. Exploration 02 is archival because its
27/54-variable construction was superseded by, and incorporated into, the
22/44-variable paper. Discovery 07 now incorporates the relevant 22/44
construction into the broader inverse-series consequence theorem. The
original files and timestamps remain public for provenance.

Discovery 04, “Full wreath-product monodromy for the square of an explicit
Keller map,” first entered the public repository in commit
[`786cd8f4ca320cdc187ecccc068121b5518907f0`](https://github.com/AlecKriebel/Math/commit/786cd8f4ca320cdc187ecccc068121b5518907f0)
at **21 July 2026, 18:44:48 UTC** (**21 July 2026, 11:44:48 PDT**). Its
strengthened website edition was prepared at **22 July 2026, 02:24:28 UTC**
(**21 July 2026, 19:24:28 PDT**). That
revision adds an exact function-field/subresultant certificate and replaces
the informal all-iterate growth argument with a local-field Puiseux induction;
it does not enlarge the theorem statement.

Discovery 05, “An explicit counterexample to the Special Image Conjecture in
dimension 21,” first entered a public branch at **22 July 2026, 02:59:33 UTC**
(**21 July 2026, 19:59:33 PDT**). It is a review draft rather than a website
publication. Its scope is deliberately narrow: the prior 22-variable cubic
model already implies SIC(22); Discovery 05 removes one homogenizing variable
and supplies a scalar-parameter lemma for the resulting nonhomogeneous linear
block.

Discovery 06, “A 14-variable polynomial map with everywhere unipotent
Jacobian and a three-point fiber,” entered its review branch in commit
[`82f74ce80de73d220a6fc5a5910aee251bfd11b3`](https://github.com/AlecKriebel/Math/commit/82f74ce80de73d220a6fc5a5910aee251bfd11b3)
at **22 July 2026, 14:26:12 UTC** (**22 July 2026, 07:26:12 PDT**). The same
commit separately publishes the third-iterate manuscript and bounded-memory
fourth-iterate certificate for Discovery 04.

Discovery 07, “A 14-variable unipotent Keller map and every-order image and
vanishing obstructions,” was prepared on **22 July 2026** as the repository's
canonical consequence paper. It consolidates Discoveries 03, 05, and 06
around two formal-inverse transfer identities, while preserving all precursor
files, PDFs, hashes, and timestamps. Discovery 04 remains the other current
paper because its iterated-monodromy theorem is mathematically independent.

## Ramsey \(R(5,5)\) endpoint note

The paused Ramsey-number research program was published as a research
checkpoint and seven-page technical note on **24 July 2026**. The narrow
candidate contribution is a minimum-miss transversal-capacity profile,
its graph-indexed aggregate inequality, and an equality-rigidity argument
excluding the regular-degree-18 endpoint
\((e(A),e(H))=(85,128)\), conditional on published catalog statements.

This publication does **not** determine \(R(5,5)\) or change the published
range \(43\le R(5,5)\le46\). It is listed once on the homepage as paused
research rather than promoted as an additional headline discovery.

The corrected history-independent verifier release
[`ramsey55-endpoint-capacity-v1.0.1`](https://github.com/AlecKriebel/Math/releases/tag/ramsey55-endpoint-capacity-v1.0.1)
was published at **24 July 2026, 22:28:24 UTC**. Its normalized archive has
SHA-256
`de541d6c7ed8be496784397ea0ee3f1b12c2b93cdbc42ba908160095c1d79cc4`.
Version v1.0 remains mathematically valid as a fresh archive, but v1.0.1
supersedes it for repeat-run and source-checkout reproducibility.

## Eternal domination and Lovász theta

The exact proof package for “A ten-vertex graph with
\(\gamma^\infty(G)<\vartheta(G)\)” first entered `main` in commit
[`64fbcd1ab5d6c4d86272985c202699009e1217ce`](https://github.com/AlecKriebel/Math/commit/64fbcd1ab5d6c4d86272985c202699009e1217ce)
at **26 July 2026, 05:46:55 UTC** (**25 July 2026, 22:46:55 PDT**).
The public paper page entered `main` in commit
[`2696384cd82d524c770f6cf30000e1448eb340f5`](https://github.com/AlecKriebel/Math/commit/2696384cd82d524c770f6cf30000e1448eb340f5)
at **26 July 2026, 05:51:56 UTC** (**25 July 2026, 22:51:56 PDT**).
GitHub Pages reported that exact commit built at
**26 July 2026, 05:52:40 UTC**, after which both the
[paper page](https://aleckriebel.github.io/Math/papers/eternal-domination-lovasz-theta/)
and [PDF](https://aleckriebel.github.io/Math/papers/eternal-domination-lovasz-theta/paper.pdf)
were retrieved successfully.

For the graph with graph6 record `IEhbtj{ro`, the note proves exactly
\[
\gamma^\infty(G)=3
<\frac{7593}{2500}
\leq\vartheta(G).
\]
The rational Lovász-theta certificate and the one-guard eternal-domination
fixed point are verified using Python's standard library, without an SDP
solver. The conclusion that order ten is minimum additionally uses the
published exhaustive order-at-most-nine computation of MacGillivray,
Mynhardt, and Virgile.

The graph and its eternal domination value are due to those authors. The
candidate contribution is the exact Lovász-theta certificate and the
resulting negative answer to the publicly recorded lower-bound question. A
focused search found no prior public resolution as of 25 July 2026, but this
does not establish absolute priority. No researcher was contacted, and the
note remains unreviewed.

## Authorship and status

**Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol.**

Alec Kriebel is a complete amateur and cannot independently verify the
mathematical claims. These papers are experiments in the limits of AI-assisted
mathematics. They require independent expert checking and should not be treated
as established results.
