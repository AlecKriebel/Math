# Exact original target

Numeric ID **30005044**, code **OWR-9790363-003**, queue rank 281.

The official source is Natalia Cardona–Tobón and Marcel Ortgiese's contribution, “The inhomogeneous contact process on Galton-Watson trees,” OWR 12/2022, printed pp. 618–620. The question is on p. 619; the report DOI is https://doi.org/10.4171/owr/2022/12. The volume has also been catalogued with a 2023 publication date; 2022 is its report identifier and workshop year.

The source model has:

- a rooted supercritical Galton–Watson tree;
- only the root initially infected;
- finite iid vertex fitnesses taking values in $[1,\infty)$;
- infection rate $\lambda F_uF_v$ across adjacent vertices;
- recovery rate 1;
- a finite offspring mean in the preceding theorems, which the explosion question explicitly asks to remove.

The target asks whether explosion **can occur** with infinite offspring mean. A single admissible offspring/fitness law with positive explosion probability answers that existential question. It is not a request to prove explosion for every infinite-mean law, and the candidate makes no such universal claim.

The source explains nonexplosion by finiteness of the infected set at every time. Accordingly the candidate proves infinitely many simultaneously infected vertices at a deterministic finite time, a stronger conclusion than infinitely many cumulative infections by that time.

The model permits the constant iid fitness $F=1$. If unbounded fitness support is additionally desired, independent finite fitnesses such as $1+\mathrm{Exp}(1)$ may instead be used by monotonicity. The unbounded-support condition on both variables earlier on p. 619 belongs to a different survival theorem, not to the general model definition.

## Extraction and neighboring-question boundaries

The primary page separates the moment-condition gap, the fitness lower-bound question, and the infinite-mean explosion question. This attempt addresses only the explosion question. The exact body of the upstream catalog extraction was not reproduced in this audit; no claim about that extraction is used.

Rank 280 / ID 30005042 is a different contribution by Mailler and Marckert, pp. 592–593, about a coupled discrete-generation weak-moment question. Sharing the report PDF does not identify their models.

The report's p. 618 summary reverses signs in two exponential-moment conditions. The introductory conditions on arXiv v4 p. 2 have the correct directions; v4 Remark 2.5 and publisher Remark 2 on p. 5 contain a separate survival/extinction prose inconsistency. These unrelated conditions and remarks are not assumptions or premises of the explosion proof. The original fitness model and constant-fitness specialization are bound directly to arXiv v1 pp. 4–5.

The potentially explosive process is explicitly defined here by finite root-originating infection paths, equivalently coupled increasing finite-ball restrictions. This chosen graphical extension is supported by BKV Definition 3.1/equation (19), p. 17. No unique continuation after explosion is attributed to the OWR report or the finite-mean author theorem.

## Current priority assessment, 2026-10-12 UTC

The whole exact existential target is assessed `already_solved`, category (b): an elementary consequence of ADGO's 2013 general weighted-GW explosion theorem through the fully written, independently checked recovery-free coupling in [PRIORITY_AUDIT.md](PRIORITY_AUDIT.md). This is a positive old-theory implication, not a claim that an older paper expressly printed this exact contact-process theorem. The BKV 2023/2026 growing-degree-ray proof plus timing/recovery addendum separately gives qualitative explosion; original-author arXiv:2406.12689v1 pp. 15–16 / v2 p. 16 anticipated the regime and route.

The accepted numerical probability theorem and all its quantifiers remain preserved in PROOF.md. Originality and significance of the bound are unestablished. No mathematical residual of the historical existential question is marked `partial`; future new refinements are separate targets. No current-openness, first-solution, new-mechanism, paper, merge, publication or DOI clearance is granted. Submitted `claimed_solved`, rank 281 and budget 1/5 remain historical facts. Root retains final user/live disposition authority; this correction makes no live mutation.
