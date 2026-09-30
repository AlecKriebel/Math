# Research log

## 2026-09-30 12:05–12:08 UTC — Source and prior-attempt gate

Recovered the full pinned record and source-code keyed null report. Read repository instructions and current queue, historical target state/path and related groups; 150 all-state PRs show no prior problem-specific attempt. The original OWR model explicitly has partially directed walks, initial East step, nearest-neighbour nonconsecutive vertex contacts and a horizontal preferred-direction force.

Brak et al. 2009 treats exactly that model and reports second-order transition with 3/2 free-energy scaling, crediting Owczarek–Prellberg 2007 uniform asymptotics. These papers are being checked for exact theorem coverage. No original proof approach has begun. This is a potential known-result correction, not a new solution. Completion estimate toward source identification: 65%; discovery progress 0%. Actual runtime gpt-6-astra xhigh.

## 2026-09-30 12:23 UTC — Exact published coverage established

Read the complete relevant model definitions, singularity analysis and force discussion in the published 2007 and 2009 papers. The fully flexible preferred-direction transition is explicitly second order; the 2009 paper gives the force-side 3/2 free-energy asymptotic. The endpoint convention of the 2007 segment model matches by an exact weight-preserving reversal, and its free-energy sign is explicitly converted. The distinction from the unproved transverse-force discussion is retained.

The known asymptotic supplies the answer; no original proof-search approach was used. Elementary convex secant arguments explain the thermodynamic consequence without assuming termwise differentiation of a speculative finite-size expansion. All 13,347 bounded controls pass. Recommended status: already_solved, 0/5, pending independent source review. Source-identification completion estimate: 95%; no discovery claim.

## 2026-09-30 12:42 UTC — Separate source review passed

The independent reviewer confirmed exact published coverage, with no mandatory correction. All 13,347 submitted controls reproduce byte-identically and 7,495 independently implemented controls pass. The frozen source note is unchanged. The eight-file review bundle is included with its replay dependency. Recommended status: already_solved, 0/5. Source-identification completion: 100%; no new discovery or independent reconstruction of the published asymptotic machinery is claimed.
