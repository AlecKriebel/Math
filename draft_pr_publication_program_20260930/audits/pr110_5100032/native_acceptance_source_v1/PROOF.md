# Accepted mathematical proof of focal antipedal invariant k603

The authoritative proof is the self-contained, four-page research note in
`publication/focal_antipedal_sum.tex` and `publication/focal_antipedal_sum.pdf`,
published as **A telescoping proof of the focal antipedal sum invariant**,
Alec Kriebel, version 1.0 (6 October 2026),
https://doi.org/10.5281/zenodo.23191247.

For an outer ellipse with semiaxes a>b>0 and a fixed strictly nested confocal
ellipse with parameter 0<lambda<b², every regular closed nonretracing
billiard/Poncelet orbit has equal sums of ordinary positive focal antipedal
radial distances. This is the literal k603 ratio-one target in the source's
two-confocal-ellipses setting. The proof covers every admitted period and
winding, including odd primitive periods, stars, reversal, and repetition.
It asserts equality of the two sums, without separately asserting constancy
of either sum across the orbit family. Hyperbolic, focal, degenerate, and
retracing extensions are outside the theorem.

The key identity, after orienting every edge with the caustic on the left, is

    q_plus - q_minus = Gamma * (y_next - y_current),
    Gamma = c/(a*b*sqrt(lambda)) * (-a² + b²*lambda/(b²-lambda)),
    c² = a²-b².

Here each q is the ordinary positive norm of the intersection of the full
lines through the edge endpoints perpendicular to their focus radii. The
manuscript proves uniqueness, positive focal heights, the positive norm
formula, consistent orientation even for stars, the edge identity, and
telescoping under closure. It treats horizontal edges and the zero coefficient
without dividing by either displacement or coefficient.

The portable `publication/verify.py` and `publication/run_verification.py`
check exact rational edge identities and genuine faulty subprocess rejection
in normal and optimized Python. Those finite controls support the written
all-real proof; they do not independently certify every closed orbit.

The original observation is credited to Reznik, Garcia, and Koiller. Classical
antipedal geometry, the known focal-height product, symmetry and telescoping
are credited as background. The dated bounded priority audit found no earlier
full covering theorem in its inspected corpus; no exhaustive or absolute-first
claim is made. Source and version limits remain explicit in
`publication/source_audit_summary.md`.

All seventeen original submitted files, including the nonempty imported prior
report and original proof, are retained byte-for-byte in `historical_original/`.
Historical triage statements remain historical evidence. The original submitted
status is claimed_solved and effort is 2/5. No new central proof-search turn was
charged during this review/publication workflow. A dated import of those facts
does not fabricate two historical structured ledger events.

AI tools were used extensively in solving, drafting, reproducing and reviewing
the result. Independent AI-agent adversarial reviews are not conventional human
peer review. The preprint is unrefereed and has not received conventional human
peer review.
