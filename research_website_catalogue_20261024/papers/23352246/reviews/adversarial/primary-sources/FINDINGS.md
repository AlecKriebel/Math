# Primary-source import findings

All receipts and downloaded source bytes are in this folder. No historical source-audit verdicts were used.

## GLS 1988

Author-hosted book: https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf

Printed pp.162–163, Definitions 6.2.1–6.2.2: strong optimization accepts any feasible exact optimizer; a vertex is not required. The unbounded alternative supplies a recession vector with objective at least one. Facet encoding, rather than an explicit facet list, supplies the well-described-polyhedron interface.

Printed pp.179–180, Theorem 6.4.9 includes unbounded polyhedra. Printed pp.308–310 specify rational value-oracle encoding and exact submodular minimization. Printed pp.313–315 describe the explicit lattice-family encoding, closure and Problem 10.3.8 reduction. These match the manuscript's stated interfaces. Critical printed pages 162, 179, 314 and 315 were also inspected as images; OCR incorrectly reads some non-strict inequalities as strict.

## Schrijver 2000

Author manuscript: https://homepages.cwi.nl/~lex/files/minsubm6.pdf

Section 6, manuscript pp.6–7, requires the smallest ring member and the smallest member containing each ground-set element when one exists. The target paper explicitly computes precisely this information by implication closure, including forced and prohibited nodes. The source supports the ring reduction; rational bit accounting is separately furnished by the target's uniform bounds and the GLS route.

## Original Conforti problem

Original report: https://ems.press/content/serial-article-files/46195

Printed pp.2904–2905 use a specified bipartite graph, rational edge demands, unrestricted signs and any selected integer coordinates. Problem 1 asks hull membership with real query notation; the preceding paragraph links this with optimization. The paper explicitly restricts queries to rational finite binary inputs. Conjecture 2 is a separate subtree-hull assertion and is not settled by this note. No model mismatch was found.

## Cook–Gerards–Schrijver–Tardos 1986

Author copy: https://www.math.uwaterloo.ca/~bico/papers/sensitivity.pdf

Printed p.258, Remarks (1), gives all-coordinate mixed proximity bounded by n times the combined matrix's largest subdeterminant, conditional on existence of a mixed optimum. The target credits this result and supplies its own specialized attainment argument. This historical import is accurately characterized and is not a replacement for that argument.

No exhaustive novelty assessment was attempted. Other contextual references are not load-bearing premises of the proof audited here.
