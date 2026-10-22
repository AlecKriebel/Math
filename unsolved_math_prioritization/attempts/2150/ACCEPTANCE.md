# EP-509 / problem 2150: acceptance report

**Accepted without a required mathematical correction.** This is an exact restricted-family result and a rigorous obstruction to a componentwise-additive route. It does not solve or refute the unrestricted conjecture.

## Accepted conclusions

1. For every nonempty compact planar set with m finite connected components, finite/countable closed-disk covering content equals the minimum sum of circumradii over component partitions. This minimum is attained by at most m disks.
2. A fixed polynomial's bounds 2+epsilon for all positive epsilon would imply an attained cover of cost at most 2. No such general bound is proved in the submission.
3. The fractional-power disk lemma and the arbitrary-subset regular-polygon lower bound are valid, including the relevant closed-boundary cases.
4. For p(z)=(z-a)^n-c, n>=2 and t=|c|, exact minimum total radius is (t+1)^(1/n) when t<=1, and min{(t+1)^(1/n), n[(t+1)^(1/n)-(t-1)^(1/n)]/2} when t>1. The degree-one value is 1.
5. The family maximum is M_n=[2/(1-(1-2/n)^n)]^(1/n)<2, attained at t_n=[1+(1-2/n)^n]/[1-(1-2/n)^n], for n>=2.
6. For p(z)=z^4-65537/65536, the sum of separate component-cover minima exceeds 9/4, although one common disk costs less than 6/5. The loss from requiring separate covers is unbounded with degree.

All component partitions were handled by a size-dependent lower bound. No assumption that an optimal covering has the polynomial's rotational symmetry was used. Countable covers were handled by open enlargement and compactness, without an epsilon loss in the final attained minimum.

## Audit evidence and limits

The full submitted proof was reviewed independently. A separately authored standard-library checker passed in normal, optimized, and doubly optimized Python. Each run verified the frozen 36-member submission plus four external dependencies; exact quartic arithmetic; seven rational crossover cases; an exact five-variable polynomial identity for the Möbius disk map; and 16,272 finite block-size arithmetic checks. Each run also rejected 15 corrupted scalar certificates and 13 integrity-control mutations. The all-degree, analytic, and topological conclusions rest on the written proof rather than these finite checks.

The Pommerenke source passages supporting the historical discussion were visually inspected. The cited 1959 construction was not independently recovered or proved. No novelty or priority claim is accepted, and the full Hayman book was not freshly audited.

Reviewed manuscript SHA-256: `4f26e97b47115cdc5037db91ab9f87ff6f3c9ae0b1ad4823b48319b576d26a6c`.

Frozen submission manifest SHA-256: `3000e53e198c84b3ecf3000f155fbbb85925df4ba22bc27799c50978f788992d`.

No remote changes or publication were performed by this audit. Source copies and private verification records are not publication-eligible. The general EP-509 target remains open in this submission.

## Publication-edition scope

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI mathematical audit, without external human peer review, journal acceptance,
or proof-assistant certification. The complete original written mathematics
above is preserved without correction. It is independently checkable as prose,
including the analytic quartic construction and its exact comparisons.

Supplementary checking programs, scalar certificates, raw computational data,
and copied scholarly PDFs, scans, OCR, and source text are not included. The
supplementary computational runs cannot be replayed from this edition alone;
their hashes and aggregate results are verification metadata, not substitutes
for proof. The analytic and topological conclusions rest on the complete
written arguments. Source-inspection descriptions refer to the original
attempt and independent audit, with no new source inspection for this edition.
The 1959 construction is credited through Pommerenke's report and remains
unverified here. No novelty, priority, improved general bound, or unrestricted
solution is claimed.
