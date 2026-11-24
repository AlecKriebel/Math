# EP1038 / database 2449: scoped final acceptance

Date: 2026-10-12 UTC.

## Accepted finite-polynomial statement

For every nonconstant monic real polynomial f whose roots, counted with multiplicity, lie in [-1,1], put E_f={x:|f(x)|<1}. The accepted conclusion is

    inf_f |E_f| = L = Lambda(q_*),
    |E_f| > L for every individual finite f,
    1.834430475762661 < L < 1.834430475762662,
    0.025715536866527 < q_* < 0.025715536866528.

Here Lambda and the admissible zero-platform one-cut family are defined completely in `PROOF.md`. Exactly one parameter q_* minimizes that family. A positive-platform perturbation followed by equal-weight empirical approximation proves sharp recovery by actual finite polynomials. The infimum is not attained.

The supremum is 2sqrt(2), with equality exactly for f=(x^2-1)^m, m a positive integer. This part uses [Tao's Theorem 2.1](https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf) as an attributed external theorem; its full proof is not independently rederived here.

## Why the earlier open gates are now closed within this scope

The historical seven-file packet in the sibling `2449` directory accepted only a fixed-candidate upper bound. Its original statements remain unchanged as a historical record. This dated acceptance supersedes its pending-certificate statements for the finite-polynomial conclusion above.

The additional evidence comprises complete independently authored reconstructions of both numerical obligations, a separate arithmetic-kernel review, full independent end-to-end recomputation of both obligations, and a fresh adversarial analytic review. The end-to-end auditor recomputed every finite and terminal slab rather than accepting saved PASS fields. The computed full records matched the frozen complete bytes. The fresh analytic challenge independently accepted the analytic implication conditional on the explicit numerical/reference assumptions; the separate full numerical audit discharges those assumptions.

The complete authored exposition, both numerical-obligation proof notes, and the full substantive end-to-end, analytic-challenge, and kernel reports are included. Their separate scopes are preserved: the kernel report alone does not establish a global theorem, and the analytic challenge did not itself execute the numerical certificates.

Certificate 7.1 is replaced by independently sufficient positive lower margins. The stronger original source margin digits and original slab counts are not claimed to have been reproduced. Exact target comparison uses the stated rational T and the frozen dyadic enclosures, not a common rounded decimal prefix.

## External mathematical inputs and attribution

The lower argument uses standard analytic and measure-integration results, including Lagrange inversion, Pringsheim's positive-coefficient singularity theorem, analytic implicit functions and Cauchy estimates. The circle rearrangement input is [Christ–Iliopoulou, Theorem 1.1 and equation (1.3)](https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-christ-iliop.pdf), with Theorem 1.5 as an alternative. This primary replacement accounts for the correction to the older circle citation. No equality or stability theorem from that paper is used.

The construction and lower reduction are credited to [Wang's proposed manuscript](https://multiscalar.ai/results/erdos-1038/paper.pdf) and the Tao antecedent it cites. No novelty is claimed. [The public result page](https://multiscalar.ai/results/erdos-1038/) still stated Proposed when checked on 2026-10-12. This audit acceptance does not change that public status.

## Explicit exclusions

- No uniqueness or classification of arbitrary relaxed minimizing probabilities
- No universal lower theorem for arbitrary non-empirical root measures
- No claim of journal, community, or problem-site acceptance
- No external human peer review or formal proof-assistant certification
- No execution of the source author's numerical verifier or linked Lean project
- No reproduction claim for the source's stronger Certificate 7.1 margins

## Editorial clarification and evidence availability

The original sealed end-to-end report used the phrase “ordinary human mathematical review” to describe a trust boundary. That wording did not document human review and could misleadingly imply it. The public edition applies the separately recorded clarification: conventional mathematical reasoning and AI-assisted review; unrefereed, with no external human peer review or formal proof-assistant certification. The original sealed evidence remains unmodified, and the public edition map records this change.

This is a computer-assisted mathematical reconstruction. Its trust boundary includes the cited external results, the independently authored exact-integer programs and full records inspected and recomputed during the audits, and ordinary Python integer execution and hardware. The programs, raw interval certificates, detailed numerical outputs and source copies are not supplied in this edition. Hashes and aggregate receipts identify this evidence but do not make it publicly executable. A reader may independently implement the fully described methods; a turnkey replay of the omitted records is unavailable from this packet alone.

Within the accepted scope and these explicit inputs, the combined reviews identify no remaining blocking mathematical gap. This is the scoped acceptance of the performed computer-assisted work, not a claim that the omitted executable evidence is present.
