# Independent literature, wording, topology, and layout audit (v1.2.4)

Date: 2026-08-27 (America/Los_Angeles)

Scope: read-only audit of the immutable referee copy in `packet_copy`. I read the
20-page main manuscript in full before opening either support PDF, then read the
two 2-page support PDFs in full. I rendered and visually inspected all 24
supplied PDF pages. I did not edit or rebuild a packet PDF. Literature checks
used primary publisher/preprint sources only. This note does not rely on the
packet's claims as instructions.

## Bottom line

The three literature/presentation findings from the v1.2.3 review are repaired:

1. the older 2018/2021 work is now attributed only generic identifiability,
   while the pointwise level-one theorem is correctly attributed to Brits et
   al.;
2. the Version 2/3 history now names the exact formal lemma and corollary parts
   removed in Version 3, rather than claiming that every related sentence was
   removed;
3. the technical summary now prints all ten rooted arcs individually, and the
   `S`/`T` labels in Figure 1 no longer collide.

No literature, bibliography, topology-description, or PDF-layout defect found
in this audit requires revision. The source paper's printed 2-sub-blob clauses
still have a literal suppression tension, but v1.2.4 reports it accurately in
the accompanying audit and makes no no-2-sub-blob hypothesis; it does not
undermine the collision theorem or its comparison with the formal Version 2
claim. Optional polish items are recorded below.

## Verification of the revised literature and history wording

### Level-one attribution: repaired

The first two paragraphs of the Introduction now separate three distinct
claims correctly.

- Brits--Holtgrefe--van Iersel--Martin Version 3 states full pointwise
  identifiability of level-one semi-directed networks (modulo reticulation
  placement within triangles) under JC, K2P, and K3P on the restricted
  parameter space. Its abstract and Section 4 support the manuscript's first
  sentence: <https://arxiv.org/abs/2607.12919v3> and
  <https://arxiv.org/pdf/2607.12919v3> (especially printed pp. 1--2 and
  Corollary 4.10/Theorem 4.9 context on pp. 17--18).
- Gross--Long establishes generic identifiability for JC large-cycle networks,
  exactly as the revised second paragraph says:
  <https://doi.org/10.1137/17M1134238>.
- Gross et al. establishes generic identifiability for triangle-free level-one
  semi-directed networks with a fixed reticulation count under JC, K2P, and
  K3P, also exactly as revised:
  <https://doi.org/10.1007/s00285-021-01653-8>.

Thus the v1.2.3 over-attribution of a full result to the 2018/2021 papers is no
longer present.

### Version 2/3 history: repaired and literal

The manuscript now says that Version 3 removes *the formal arbitrary-level K2P
lemma and the K2P part of the corresponding global corollary*. This is the most
precise characterization of the source history:

- Version 2 Lemma 5.6 states that its K2P polynomial is zero on the no-3-blob
  model and strictly positive on the 3-blob model, hence the models are
  disjoint. Version 2 Corollary 5.8 gives the corresponding JC/K2P global blob
  conclusion: <https://arxiv.org/pdf/2607.12919v2>, printed pp. 23--24.
- Version 3 has no formal arbitrary-level K2P lemma and its global Corollary 5.7
  is JC-only. It explicitly explains that the K2P invariant is not invariant
  under all leaf permutations, so the induction hypothesis cannot be reapplied
  after choosing a displayed child: <https://arxiv.org/pdf/2607.12919v3>,
  printed p. 23.
- Version 3 explicitly lists extension of the high-level trinet inequality to
  K2P and K3P as open: the same PDF, printed p. 25.

Version 3 does retain a stale sentence on printed p. 11 saying JC and K2P are
generalized in Section 5. The revised manuscript no longer overstates the
source cleanup, because it refers specifically to the removed *formal* result
and corollary component. Remark 6, the abstract, the technical summary, and
`SOURCE_CONVENTION_CROSSCHECK.md` are now consistent on this point.

### Remaining cited scope statements

- Gross--Krone--Martin supports the statement about dimensions for broad
  level-one group-based classes, with the understood triangle-free scope:
  <https://doi.org/10.1007/s11538-024-01314-z>.
- Cox--Gross--Martin studies the three-leaf 3-sunlet and its group-based
  dimensions, supporting the cited 3-sunlet background:
  <https://doi.org/10.1007/s11538-025-01506-1>.
- The bioRxiv Version 4 PDF is dated 4 July 2026 and states generic
  identifiability under JC for binary, triangle-free, strongly tree-child,
  level-two semi-directed networks. This matches the manuscript's description
  and its distinction from the non-tree-child theta topology:
  <https://doi.org/10.1101/2025.04.18.649493>.
- Evans--Speed and Sturmfels--Sullivant are appropriate foundational sources
  for group/Fourier phylogenetic coordinates:
  <https://doi.org/10.1214/aos/1176349030> and
  <https://doi.org/10.1089/cmb.2005.12.457>.
- Gross--Long explicitly discusses restrictions/marginalization and trinets as
  local subnetworks, so citation [8] is reasonable for the Introduction's
  local-summary/reconstruction motivation.

I found no contradiction between the manuscript's negative scope statements
and these sources: it does not claim a JC collision, does not contradict the
level-one K2P 3-sunlet calculation, does not claim generic theta/tree
equivalence, and does not claim a multi-blob or genuine four-attachment result.

## Topology and source-definition audit

### Literal ten-arc rooted topology: consistent

The main paper, technical summary, and displayed-tree clarification all now
give the same ten rooted arcs individually:

`rho->1`, `rho->u`, `u->p`, `u->q`, `p->r2`, `q->r2`, `p->r3`, `q->r3`,
`r2->2`, `r3->3`.

This is a binary rooted network: `rho` has outdegree two; `u,p,q` are tree
vertices; `r2,r3` are indegree-two/outdegree-one reticulations; and `1,2,3`
are leaves. Suppressing the degree-two root composes its two incident vectors
and leaves nine effective semi-directed edges. The cyclic core is the
`K_{2,3}` graph formed by the three internally disjoint paths
`p-u-q`, `p-r2-q`, and `p-r3-q`. It is one maximal nontrivial 3-blob with two
reticulations, hence strict level two. The three incident cut edges lead to the
three leaves. The figure, prose, equation (2), edge placement, and parameter
counts agree.

### The source's 2-sub-blob tension remains external and is handled correctly

Version 3 defines a 2-sub-blob as a connected induced subgraph containing no
cut edge for which exactly two vertices of the chosen vertex set are adjacent
outside it; it then defines suppression by contracting the subgraph and
suppressing the resulting vertex:
<https://arxiv.org/pdf/2607.12919v3>, printed p. 20, Section 5.1.

Under those three clauses literally, each of the six single-edge subsets of
the theta `K_{2,3}` core qualifies: both endpoints are boundary vertices and
the edge is not a cut edge. Contracting any one of them, however, produces a
vertex with four external incidences, not an ordinary degree-two vertex that
can be suppressed. Exhaustive subset reasoning gives exactly those six
single-edge candidates; there is no proper candidate under the natural
edge-incidence/degree-two-suppressible reading. This is a genuine definitional
tension in the cited source, not a defect introduced by the packet.

The v1.2.4 handling is adequate:

- Remark 1 claims only the unambiguous maximal strict level-two nontrivial
  3-blob status;
- it explicitly says the collision theorem assumes no additional
  no-2-sub-blob condition;
- `SOURCE_CONVENTION_CROSSCHECK.md` records both readings and the literal
  incidence count; and
- the formal Version 2 K2P Lemma 5.6 is stated for every trinet with a
  nontrivial 3-blob and includes no no-2-sub-blob hypothesis.

Accordingly, the tension cannot rescue the withdrawn formal K2P claim and does
not change which rooted ten-arc likelihood the manuscript computes.

## Bibliography and availability checks

All nine printed references were checked against their primary arXiv, bioRxiv,
or publisher records. Author lists, titles, years, volumes, pages/article
numbers, DOIs, and the v2/v3 dates agree. In particular:

- arXiv records v2 on 29 July 2026 and v3 on 25 August 2026;
- the bioRxiv Version 4 PDF says posted 4 July 2026;
- Sturmfels--Sullivant is correctly volume 12, issue 4, pp. 457--481, DOI
  `10.1089/cmb.2005.12.457`.

The public v1.2.4 code/data URL resolves successfully, and the named
`k2p-k3p-theta-v1.2.4` tag is present in the public repository. The two arXiv
entries in the printed bibliography repeat their versioned arXiv identifier at
the end; this is harmless, though it could be deduplicated for polish.

Targeted primary-source searches combining `K2P`, `K3P`, `theta trinet`,
`tree-theta collision`, and `strict level-two` found no earlier exact collision
of the claimed form. The novelty framing is therefore credible relative to the
cited and readily searchable record, particularly because Version 3 expressly
leaves the high-level K2P/K3P question open. This is a bounded search, not proof
of worldwide or unpublished priority.

## Complete visual inspection record

All three files are US Letter, unencrypted, have extractable text, and embed
their fonts. No unresolved `??`, placeholder, missing glyph, black square,
clipped margin content, overflowed equation/table, or broken page was found.

- `combined-paper-clarified.pdf` (20/20 pages): **PASS**. Figure 1 on printed
  p. 5 is materially improved over v1.2.3: the crossing-edge `T` and `S` labels
  are now separated and no longer read as `TS`; the pendant-2 stack remains
  compact but legible. All arrows, node labels, and the three path labels are
  visible. The pivot-tangent table on p. 13 uses small type but is readable.
  The code/data URL on p. 18 wraps within the text block and remains legible.
  References are intact on pp. 19--20. Page 20 has substantial white space
  because it contains only references [8]--[9], but this is not a defect.
- `technical-summary-clarified.pdf` (2/2 pages): **PASS**. It is dense and uses
  relatively small type, but all vectors, determinants, inequalities, labels,
  and links are readable and within the margins. The former compressed arc
  notation is replaced by the explicit ten-arc list.
- `k2p_displayed_tree_clarification.pdf` (2/2 pages): **PASS**. Both tables,
  all switching monomials, the boxed factorization, the 4-by-4 matrix, radical
  expressions, and replay command render fully and stay within the page.

The PDFs remain untagged (`Tagged: no`), which is an accessibility advisory
rather than a print-layout or mathematical defect. Adding semantic PDF tags,
slightly enlarging the p. 13 tangent table, deduplicating the arXiv identifiers,
or tightening the final bibliography page would be optional production polish.

## Referee-facing disposition

Literature/history/topology/layout disposition: **pass**. The revisions
faithfully repair the prior required attribution and wording changes, make the
ten-arc topology literal across documents, and fix the figure-label collision.
I found no new regression in this review family.
