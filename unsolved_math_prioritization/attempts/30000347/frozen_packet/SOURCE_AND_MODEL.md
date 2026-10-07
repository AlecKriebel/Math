# Source and model verification

Checked 7 October 2026.

## Historical source

The publisher PDF of Oberwolfach Report 50/2005 identifies the workshop as
6–12 November 2005. The report is also cited with a 2006 publication year.
Krause's contribution
is on printed pp. 2856–2858, PDF pages 24–26 counting the first page as 1.

Its problem uses a simple undirected graph, unit traversal lengths, optional
edge deletion costs, and all three pairs of three specified vertices. Distances
must increase by at least one; original shortest paths are to be hit. The
undirected triangle complexity is left open there. The same contribution
explicitly states directed triangle NP-hardness. Thus a secondary description
that also labels the directed version open is not supported by this source.

Fresh publisher retrieval and the earlier cached PDF have different byte hashes
and PDF-production metadata, but their complete Krause contributions match
exactly after collapsing extracted whitespace. The public source manifest
records this distinction; neither PDF is included in the authored packet.

Publisher source: https://ems.press/content/serial-article-files/46024?nt=1 .
DOI: https://doi.org/10.4171/OWR/2005/50 .

## Dissertation cross check

Krause's dissertation is dated 24 February 2006. Printed p. 2 defines BSP and
permits assuming positive deletion costs and initially connected, nonadjacent
terminal pairs. It explicitly treats ordinary multicut solutions as feasible
BSP solutions, so terminal disconnection is allowed. Section 4.3, printed
pp. 34–36, leaves the undirected triangle case unresolved. Theorem 9.3, printed
pp. 83–84, proves directed triangle hardness. The phrase triangle describes the
three demand pairs, not three adjacent graph terminals. Traversal lengths remain
unit lengths throughout the target model.

Institutional-library mirror:
https://webdoc.sub.gwdg.de/ebook/dissts/Braunschweig/Krause2006.pdf .
The university-hosted URL was returned by search, but a fresh browser read
encountered a security-check page; the mirror and locally cached PDF were
available for inspection:
https://leopard.tu-braunschweig.de/servlets/MCRFileNodeServlet/dbbs_derivate_00000049/Document.pdf .

## Match to the authored construction

Every constructed instance is finite, simple, undirected, and has unit traversal
lengths and unit positive deletion costs. The three terminals are new and are
never deleted. They are pairwise nonadjacent and have pairwise distance 3.
All edges are eligible for deletion, including those incident to terminals.
The conversion of a general blocker to a vertex cover explicitly accounts for
middle-edge deletions. The proof does not confuse deletion cost with length,
and does not require restricting deletion to a special edge set. Initial
connectivity also holds: the three terminals are connected through the nonempty
part-edge types, and every other vertex has a spoke to one of them.

The usual infinity convention suffices for the stated source problem. A separate
optional construction supplies intact four-edge routes and proves that a
finite-terminal-distance requirement would not defeat the hardness reduction.
No planar, bounded-degree, unique-geodesic, or global residual-connectivity
restriction is asserted.

## Literature and attribution limit

A bounded public search on 7 October 2026 used exact problem names, Krause's
name, triangle instances, shortest-path multiway cut, distance-increasing cuts,
and tripartite vertex cover combinations. It recovered the report and thesis
but did not locate an exact subsequent classification of this undirected
three-terminal unit-length problem. Related hits concerned general length-bounded
cuts, directed multiway cuts, or Force Path Cut and did not establish the exact
claim proved here. Search absence is not evidence of priority or of an exhaustive
open-problem status. The manuscript makes no priority claim.

The authored proof depends externally only on classical Vertex Cover
NP-completeness. The tripartite subdivision identity and its reduction to BSP
are both proved in full, so neither is delegated to an uninspected theorem.

Karp’s original article was inspected at its Main Theorem and Node Cover entry
on printed p. 94, PDF page 10 of the university-hosted scan:
https://cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf .
The scan is image-only; the relevant page was read visually after rendering.
