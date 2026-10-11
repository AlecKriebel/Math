# Random-transposition entropic curvature: audited partial results

Problem **30002753 / OWR-13359-003**, rank 726. **Unsolved; five of five approaches used.** This guide and `audit_release/AUDIT.md` control interpretation of the preserved author packet. Its earlier “audit pending” and “no publication” fields are historical, pre-audit observations, not the present publication state.

## Controlling numerical qualification

The saved exploratory n=3 optimizer value **0.8816783052209357** does not reproduce to absolute tolerance 10^-9: independent evaluation of the saved density and potential gives approximately **0.8816783124866347**, a difference of about **7.27 × 10^-9**. The n=4 discrepancy is about 9.46 × 10^-12. The original output is preserved, rather than silently corrected. Optimizer values are exploratory only; no precision-certified bound, global optimum, or 10^-9 n=3 reproducibility is claimed. Six-decimal summaries should be used.

The **separate exact rational witness** with density (1,1,16,16,1,1) and potential (5,-5,8,-8,5,-5) proves **κ_3 < 9/10**. Its rigorously enclosed quotient lies between **0.881815 and 0.881816**. It does not depend on the optimizer digits and is not claimed to be optimal.

## Retained mathematics and unresolved target

The model is logarithmic-mean entropy-geodesic curvature for the continuous-time random-transposition chain on S_n, with rate 2/[n(n-1)] per distinct transposition and **total jump rate one**. Ordinary Ollivier/W_1 curvature is a different quantity.

- Positive one-card tests prove κ_n ≤ R_n(t), where R_n(t) = [n + (t+n-2-(n-1)/t)/log t]/[n(n-1)] for t>0, t≠1, with removable value R_n(1)=2/(n-1).
- Taking t=√n proves **limsup nκ_n ≤ 1**. This improves an upper-test constant without identifying the asymptotic order.
- **κ_2=2** and the distinct rational **κ_3<9/10** certificate are retained.
- Equitable quotient tests give **κ_X ≤ κ_Y**. A quotient lower bound cannot be pulled back in the reverse direction.
- The inspected local S_3 example has B_off/A→0 while **B/A→+∞**. A vanishing off-diagonal ratio does not prove sharpness for the full Hessian.

The established lower scale is n^-2 and the upper scale remains n^-1. A matching all-n order, an exact optimum for n≥3, and one-card optimality remain unresolved. No novelty, priority, or current global-openness claim is made. The full proofs and precise gaps are in `safe_release/PROOF.md` and the audit. The established entropy-Hessian criterion and published lower-bound decomposition are credited theorem dependencies.

## Verification and source limits

The author checker passes **113 arithmetic assertions over 872 states**. Independently written controls pass **187 exact assertions**, including **nine mathematical negative controls**. Supplemental symbolic work passes **19 checks**. Four binding negative controls verify sensitivity to changed or truncated bytes. These are finite or symbolic controls supporting the written proofs, not a universal optimizer certificate or a formal proof-assistant verification.

The primary OWR source and relevant Erbar–Maas–Tetali and Fathi–Maas statements were inspected. The exact UnsolvedMath website statement was inaccessible; the catalog-to-primary correspondence is qualified. The audit independently checked eight public-source PDF hashes, but did not independently reread every later paper. Literature and repository searches were bounded, and the raw AI-solution/progress corpora were not inspected. No absence-of-prior-work conclusion follows.

Both original directories and safe archives are included **byte-for-byte**. The archive members are only the same authored proof/audit/code/results and public verification metadata. No scholarly PDFs, source extracts, images, raw problem records, dataset contents, or private coordination files are included. Only this problem's queue Status and Turns are changed; Findings, Chat, DOI, every other row, and the existing embedded header are preserved.

## Portable replay

Use Python 3 with SymPy installed (audit version 1.14.0). From any working directory, run:

    python3 -B /path/to/30002753/verify_publication.py --expected-manifest PUBLICATION_MANIFEST_SHA256 --queue /path/to/QUEUE.md

Supply the external publication-manifest SHA-256 recorded in the draft PR description. Do not obtain the expected value from an untrusted modified packet. The optional queue argument verifies the exact published queue hash; full one-row byte comparison was also performed against the immutable base blob. The verifier checks the full inventory, both frozen manifests and archives, replays all five verification scripts, checks saved result agreement, and probes assertion failures. It rejects Python optimization (`-O` or `PYTHONOPTIMIZE`) before any checker runs. The optional NumPy/SciPy optimizer is not rerun and is not required.

Checks run from an unrelated directory and from a relocated copy. Mutation tests must reject changed proof/audit/guide bytes, missing or extra files, links, unexpected directories, archive corruption, self-consistent inner-manifest rewrites, outer-manifest rewrites, and optimized execution. Remote publication is subsequently checked against exact Git blob bytes; an absence of CI checks is not a CI pass.

Publication scope is a draft PR only. No merge, release, DOI creation, or outside outreach is part of this packet. The bounded five-route investigation is complete; a subjective 10% discovery-completion estimate reflects retained partial results rather than a fraction of a proof or a success probability.
