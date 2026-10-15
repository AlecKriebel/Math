# Independent literature and priority audit of PR 662

Immutable head: `e31701151c331a6eed9224fb37a75a374ea1043e`. Problem: 2306086 / Hayman–Lingham 6.86. Review date: 2026-10-15 UTC. This is an independent broad literature family, not a review of another family's findings.

## Exact conclusion

I have **not verified an earlier theorem that states or positively implies the exact controlling qualitative result**. The reviewed classical and later sources do not, by themselves, support closing this PR as an already solved problem. This conclusion is a bounded search outcome, **not a novelty guarantee**.

Preparation of a narrowly framed qualitative research note is supportable from this family's evidence. It should explicitly present the result as an application of classical distortion rigidity and compactness to the fixed-point question, claim no historical firstness, and leave the quantitative radius undetermined in this note. The note should not claim an explicit improved upper bound, sharp radius, general extremizers, or complete variability region. Unconditional statements about present openness or absence of earlier work are not supported.

Two original-source leads remain material: Jenkins 1960, specifically its derivative bounds identified by Jenkins's own 1962 survey, and the special cases of Aleksandrov–Popova 1973. The parent has assigned a separate source-access family to the remaining historical originals. My report retains these gaps rather than guessing their contents. The parent also supplied the primary Rodemich 1979 abstract; I independently read and rendered it, without reading that family's report.

## Target and interpretation

For the normalized real-coefficient schlicht class `S_R`, put

`A_f(z) = (1-|z|^2) f''(z)/f'(z) - 2 conjugate(z)`

and `M(z) = max_{f in S_R} |A_f(z)|`. The claim being assessed is `M(z)<4` for every fixed nonreal `z` in the disk, `M(x)=4` on the real diameter, and a uniform strict gap on each compact subset of the nonreal disk. It is not a formula for `M`.

The complete normalization page and target page of the 2018 draft were independently read and rendered: printed pp. 114 and 147 / PDF pp. 115 and 148. The question fixes `z_0` and asks for improvement under reality of coefficients. Its wording does not explicitly require a numerical or sharp formula. Therefore failure to determine that formula is not, by itself, a reason to reject the controlling qualitative theorem. At zero, the original displayed expression degenerates to zero; the auxiliary quantity `A_f(0)` must not be substituted for it.

The source's 2018 no-progress update is a dated account of reports received by its authors. It is not evidence that no solution existed then or that the problem remains open in October 2026. The publisher's 2019 edition was verified bibliographically; its subscription-only target page was not inspected in the original. A secondary transcription of that edition appeared in search results and was not promoted to primary verification.

## Historical sources and exact gaps

**Koepf 1986, DOI 10.1007/BF01162704.** I read all five pages of the author-hosted original and visually checked complete printed p. 578. The main class has `f(0)=1` and omits zero. Section 4 treats the usual normalized real class and classifies its extreme points using convex representations. The paper deals with extreme/support points and continuous linear functionals. The quotient `f''/f'` is nonlinear. Nothing in the inspected statements makes its maximizer a support point or licenses evaluation on the listed extreme functions. Such a transfer would require a separate proof; the supplied convex-hull critical-point obstruction shows why a naive relaxation fails. This source is relevant background, not a verified earlier solution of the target.

**Jenkins 1960, DOI 10.2307/1969877, and Jenkins 1962, DOI 10.1090/S0002-9904-1962-10670-3.** The 1960 article's Annals issue metadata was checked. Ordinary and `seq=1` PDF endpoints returned identical 3038-byte HTML, not the article. I did recover the original nine-page 1962 AMS survey, read it fully, and rendered printed p. 7. There Jenkins explicitly identifies derivative bounds among the results of his 1960 real-coefficient paper, alongside covering and point-value results. He does not give the derivative formulas or their exact normalization there. This is a concrete source gap: a summary that mentions only the range of `f(z)` cannot eliminate the derivative overlap possibility. Conversely, a general statement that derivative bounds exist cannot establish overlap with this particular centered quotient. No exact prior implication has been verified.

**Aleksandrov–Popova 1973, DOI 10.1007/BF00969900.** The Russian abstract and publisher bibliography were read. They identify differentiable functionals of a function and its first derivative at a fixed point, with variation and Loewner optimal-control methods and some explicitly solved cases. The full Russian PDF did not reach this family's host: ordinary retrieval timed out, and bounded requests to both public MathNet hosts failed to establish a connection. The English publisher page was a subscription preview. I do not infer the exact special cases, a bound for `f''/f'`, or absence of overlap from the abstract. The original theorem context remains unverified here.

**Tepper 1976, AMS abstract 731-30-27.** I recovered the original January issue and read/rendered complete printed A-104 / PDF p. 194. It announces Loewner distortion results for the same real normalized class, but the displayed example concerns `arg f(re^{i theta})`. Moreover the example as printed has a visible `<=` sign and fails for the admissible identity map at `r=1/2`, `theta=pi/2`: its two sides are exactly `1` and `1/3`. This precise defect is preserved in `TEPPER_PRINTED_BOUND_COUNTEREXAMPLE.json`. A likely misprint cannot be repaired by guessing. Neither this faulty displayed example nor the general announcement is used as a verified target theorem. This says nothing about unspecified other results or a corrected full treatment.

**Rodemich 1979, AMS abstract 763-30-11.** I independently read/rendered complete printed A-68 / PDF p. 152 of the dated archive copy of the AMS original. It announces, for the same real normalized class, an argument bound for `(1-z^2) f'(z)` in terms of `q=|z-conjugate(z)|/(1-|z|^2)`: the right side is `2 arctan q` when `q<=1` and `pi/2+log q` when `q>1`. This is a different functional, and the abstract supplies no proof. Differentiating the inequality is not a valid implication to a bound for the derivative of its left-hand analytic logarithm. A more substantial implication is a separate mathematical question being assessed by the parent's other family; I have not assumed its answer.

## Later literature: boundaries that must be preserved

I recovered Prokhorov's 2019 journal original, DOI 10.18500/1816-9791-2019-19-3-258-279, and read complete Section 4, printed pp. 268–269, with p. 268 rendered. It concerns the value range of `f(z_0)` for `S_R` and its bounded subclasses, credits Fedorov with the full value-range solution and Jenkins with earlier partial results, and describes a controlled Loewner equation. It does not state the target quotient estimate. Its attribution about Fedorov remains secondary until Fedorov's original is inspected. It also prevents uncritical reliance on a broad encyclopedia summary that credits Jenkins with the full point-value range.

Koch–Schleissinger's original arXiv manuscript 1602.05058v3, published under DOI 10.1090/proc/13350, was read for its complete relevant definitions and Section 3, with pp. 5–6 rendered. Its functions are bounded disk self-maps with positive initial derivative, or hydrodynamically normalized half-plane self-maps; its extremal functionals are point values and inverse point values. These are not the target class and functional. Normalizing a disk self-map to derivative one leaves only the identity. No reduction preserving the needed class and quotient has been provided.

The 2025 Chuaqui–Efraimidis–Hernández original arXiv manuscript 2510.05395v1 was checked through its definitions, theorem statements and relevant full pages. Its pre-Schwarzian estimate on p. 8 lies within the proof for the convex subclass `C`, explicitly defined on p. 2 and maintained in the preceding proof. Its results for arbitrary real-coefficient functions concern Hardy membership and pathological derivative behavior, not the centered fixed-point disk. This recent source does not give a priority block for the target.

Other retrieved originals were screened at the stated, limited depth: Obradović–Tuneski 2018/2021 impose coefficient positivity or additional `U(lambda)` restrictions and study coefficient functionals; Saitoh's RIMS paper is dated 2008 in its header and gives sufficient conditions for starlikeness/convexity; Majchrzak–Szwankowski 1996 studies a polynomial expression in `a_2,a_3`. They do not supply a verified all-`S_R` quotient bound. Their unneeded proofs were not represented as fully audited. Recent Ma–Minda, harmonic, circularly symmetric and polygonal-domain leads impose different classes or functionals. Metadata-only and inaccessible leads remain explicitly identified in the source ledger.

## Publication framing and decision limits

The following claim is supportable: an affirmative answer to the **qualitative fixed-nonreal-point version** recorded in the 2018 source, proved using classical ingredients, together with exact real-axis sharpness and stated quantitative limitations. It is also reasonable to make the proof self-contained and credit the area theorem, the second-coefficient equality case, Koebe transformations and compactness rather than imply invention of those methods.

The following are not supported by this audit: a first-ever solution claim; a guarantee that no earlier equivalent exists; an assertion of current open status based solely on the 2018 update; elimination of Jenkins 1960 on the strength of a secondary summary; or treating an unproved bridge from a differently normalized value region or argument inequality as an earlier solution. A short deduction from classical foundations alone does not settle the historical priority of this specific application in either direction.

I recommend retaining a clear no-firstness statement and a precise quantitative limitation in any proposed note, and combining this report with the parent's focused historical-source and exact-implication addenda before final promotion. This family has no demonstrated mathematical or priority reason to label the target already solved, and has no evidence that supports closing it on that ground. It does not grant an unconditional novelty certificate.

## Checkable record

`REPORT_BINDING.json` checks all 24 captured native files against the immutable-head SHA-256 inventory: zero mismatches. `SOURCE_RETRIEVALS.json` records actual successes, non-PDF responses and failures; `SOURCE_LEDGER.json` has 20 carefully scoped source records. `SEARCH_LEDGER.json` records 101 targeted web queries plus separate metadata searches. Many searches returned irrelevant results or ignored some terms; the count measures attempted coverage, not evidential weight. Complete copyrighted originals, extracts, raw responses and renders are confined to ignored `tmp/` and are not publication payloads.

No other new family reports were read. No external communication, Git/branch/index changes, remote mutation, PR disposition, paper preparation, publication or tracker update was performed by this family. Review completion: **100% of this bounded independent literature assignment**, with the original-source gaps above explicitly retained.
