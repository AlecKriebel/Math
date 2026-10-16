# Source audit for random projective plane transversals

Checked 30 September 2026. The pinned full UnsolvedMath dataset at revision `37e53eabe540fb458758e198be61634bd02ee008` supplied the statement and source links. The public source records are preserved in `source_records.json` with attribution to [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), CC BY 4.0.

## Exact source

Noga Alon, “On designs and partial designs,” in [Oberwolfach Report 42/2025](https://ems.press/content/serial-article-files/52246?nt=1), pp. 2249–2251, Conjecture 5 on p. 2250. EMS lists publication on 16 February 2026; the workshop was 14–19 September 2025. The full relevant contribution was read.

The same conjecture is Conjecture 3.2, p. 4, in Alon's [Blocking partial designs and block-compatible sequences](https://web.math.princeton.edu/~nalon/PDFS/remark191.pdf), and Conjecture 4.7 in [Problems and results in Extremal combinatorics V](https://web.math.princeton.edu/~nalon/PDFS/sum280.pdf). These author-hosted versions still describe the target as open. Both the divergence statement and the proposed logarithmic rate are part of the research target.

The nearby solved partial-design theorem independently deletes each point-line incidence. Here one random set of points simultaneously determines every line section. Independence of the line sections must not be assumed.

## Related and prior attempts

ID 30006391 / OWR-14299518-004 is an exact duplicate of this target, rather than an independent problem. ID 30006389 contains the distinct partial-design and block-compatible counting questions already answered by Alon's source; it is not a solution of this random-point conjecture.

Before proof work, the main-branch queue listed 30006390 as queued with 0/5 turns. The pinned research-results dictionary has no matching report. All-state PR searches, full PR title/body checks, branch-reference checks, and attempt-path commit checks found no prior attempt for 30006390 or its duplicate 30006391. No matching attempt folder appeared in the main-branch tree. The related-target file had no entry identifying this duplicate pair. Shared historical records have not been changed.

The source gate passes for investigating an unresolved target. A bounded literature search does not establish exhaustive current open status or novelty.

## Container references checked

[Balogh–Samotij, An efficient container lemma](https://www.math.tau.ac.il/~samotij/papers/efficient-containers-revised.pdf), Theorems 1.1, 1.6, 2.1 and the epsilon-net application in Section 7, was checked for a direct application. Its numerical hypotheses fail for the full-line hypergraph here; the precise substitution is in `BASELINE.md`. [Balogh–Solymosi, On the number of points in general position in the plane](https://arxiv.org/pdf/1704.05089), the epsilon-net statements and construction context, concern a different constructed geometric system. Neither cited result supplies the missing random-projective-plane lower bound.
