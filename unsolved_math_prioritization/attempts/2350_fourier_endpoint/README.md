# Fourth-order Fourier endpoint for Erdős 864

Problem 2350 / EP-864; queue row 1741. Edition: 12 October 2026 UTC.

**Original interval conjecture: UNSOLVED by this work.** This appendix is an audited analytic partial accompanying the [weighted, continuum and modular-carry packet](../2350/README.md). It gives no unrestricted leading-constant improvement beyond √2, no integer counterexample, and no novelty or priority claim. This AI-assisted mathematical manuscript is unrefereed; its independent internal AI audit is not external human peer review, journal acceptance, or proof-assistant certification.

## What is proved

For a strong Sidon sequence B⊆[L] with |B|∼c√L and macroscopic uniform profile, write F for its Fourier sum, G for the constant-density interval model and R=F−G. The [complete proof](FOURIER_ENDPOINT_PROOF.md) establishes

    ∫|R|⁴ = (2c²−(2/3)c⁴+o(1))L,
    T(B) = (c⁴/6+o(1))L + Re ∫R³ conjugate(R),

where T(B) counts ordered a+b+c=d, including repetitions. All mixed quartic terms are o(L). Near-maximal ordinary Sidon sequences have the required uniform profile. At c=1 the residual fourth moment is (4/3+o(1))L and its supremum is at least (2/√3+o(1))L^(1/4). Thus neither an L⁴-small-error transfer nor the conventional supremum/second/fourth-norm absolute-value estimate can establish the desired endpoint transfer.

If triple avoidance holds, the normalized signed residual phase tends to −c²/[4(3−c²)], in particular −1/8 at c=1. The additional hypothesis Re ∫R³ conjugate(R)≥−κ∫|R|⁴+o(L) implies c²≤12κ/(1+4κ), only for this uniform-profile class. The value κ=1/14 would give c≤√(2/3) there. That phase inequality is not established for genuine Sidon sets, and nonuniform profiles remain outside this conditional theorem.

The complete proof also retains the exact leading carry coefficients, the phase correction for radii in the single coset Z+1/2, and two explicit scalar-norm countermodels. One is a measurable Fourier function; the other is a real-coefficient polynomial supported on [L]. Both are signed countermodels. Neither has the required nonnegative or indicator coefficient structure, and neither is an integer counterexample.

## Complete audit and provenance

The [full substantive independent audit](AUDIT_FOURIER_ENDPOINT.md) reconstructs every mathematical argument and checks the source-rate distinction and countermodel perturbations. Its sole required clarification is now explicit: the half-integer extension is for Z+1/2, not arbitrary mixed subsets of (1/2)Z. The shift B↦B+1/2, signed phase factor e(−α), and constants are unchanged.

See [acceptance and limits](ACCEPTANCE.md), [every editorial change](EDITION_MAP.md), [original input identities](INPUT_PINS.json), [public sources](SOURCE_METADATA.json), and [aggregate verification](VERIFICATION.json). [MANIFEST.json](MANIFEST.json) gives the complete public member set and hashes every other member; its digest is externally pinned in the preparation seal and intended draft description.

Only authored mathematical prose, complete substantive audit, acceptance, and aggregate public source/verification metadata are distributed. No executable code, raw diagnostic output, dataset contents, copied source document/text/image, private source, personal data, or coordination file is included. Written universal arguments are retained in full; finite diagnostics supplement those arguments and are not asymptotic proofs or a formal certificate. The companion 14-file packet is unchanged.
