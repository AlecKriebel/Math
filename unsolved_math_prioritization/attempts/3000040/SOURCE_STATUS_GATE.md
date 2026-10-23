# Gonality and edge subdivisions: source/status gate

Checked 2026-10-21. Ordered row **1871**, ID **3000040**, key **AMR-029-0040**; predecessor row 1870 is ID 2401 / EP-949. The order was recovered using the row identifier, not a physical line number. No queue or remote publication was changed.

## Disposition

**PARTIAL / OPEN RESIDUAL; existing-result gate, not a new solution.** The broad question is not a single yes/no conjecture. Do not mark it solved merely because subdivision invariance is false. Conversely, do not investigate invariance, bounded ratio, or finite attainment as if they had no established answer.

The [Egres problem page](https://lemon.cs.elte.hu/egres/open/Gonality_and_edge_subdivisions) asks about uniform edge subdivision and already records counterexamples. Its last displayed revision is 2021-11-30. Its suggestion that boundedness of the ratio is unknown is stale.

## Verified primary results and remaining targets

Van Dobben de Bruyn, Smit and van der Wegen, [Discrete and metric divisorial gonality can be different](https://doi.org/10.1016/j.jcta.2022.105619), JCTA 189 (2022), 105619:

- Write sigma_m(G) for replacing every edge by m segments; adding k new vertices means m=k+1. Gonality here is divisorial gonality of connected loopless multigraphs.
- Theorem 1.3 identifies unit-metric gonality with the minimum over regular subdivisions; the minimum is attained, not merely an infimum.
- Theorem 1.4 gives simple bipartite examples with original gonality 6t and two-segment gonality 5t, hence unbounded additive drops.
- Proposition 5.3 gives dgon(G) <= 2 dgon(Gamma(G)) - 1. Thus the ratio is bounded; its sharp universal constant is left between 6/5 and 2.
- Section 6 also asks whether an odd-segment subdivision can lower gonality, and whether a drop can first occur beyond two segments.

The [arXiv v2 record](https://arxiv.org/abs/2106.12568v2) explicitly says Proposition 5.3 was added and open question 2 changed. The final journal PDF retains those distinctions. Both PDFs were retrieved; statements and relevant proof passages were inspected, not independently re-proved in full.

## Scope and cautions

The recovered triage confuses divisorial subdivision questions with stable gonality. Stable harmonic-morphism gonality and stable divisorial gonality must not be substituted for unit-metric gonality without an explicit theorem. Arbitrary unequal subdivisions are not the uniform subdivisions in this row.

Targeted searches for later odd-subdivision and sharp-ratio resolutions found no verified newer resolution. This is a bounded search outcome, not proof of current openness. The authors' current publication pages and the publisher identify the 2022 paper; the checked source still presents the residual questions as open.

No novel claim was attempted. No full independent audit of the tricycle construction or exhaustive computation was performed. Next work must specify one residual target and first strengthen its current-literature check.

Public metadata records hashes/sizes only. Downloaded third-party source documents, extracted text, and corpus records remain private and must not be published with this gate.
