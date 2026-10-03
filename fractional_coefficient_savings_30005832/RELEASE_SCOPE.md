# Final scope and release clarification

## Accepted quantitative result

For `m=2^d`, `d>=1`, the frozen theorem constructs an exactly specified cardinality-adder CNF with `N=5m-2d-4` variables, `37m-23d-35` clauses and width at most five. In the source's normalized Boolean literal-weakening convention,

- rational Nullstellensatz coefficient mass is at most `72d-102+106/m`;
- every arbitrary-real refutation has at least `m/2+1` terms;
- consequently every integer-coefficient refutation has mass at least `m/2+1`.

The resulting `Omega(N/log N)` advantage is unbounded. Independent adversarial review found no mathematical repair requirement. The first strict separation certified by these particular displayed bounds is at `d=11`; small-parameter looseness does not affect the general asymptotic result.

## Original qualitative question

The official OWR question asks for natural examples with great fractional-coefficient savings. It imposes no superpolynomial lower-bound requirement. A standard cardinality-circuit encoding with an unbounded, nearly linear factor is a defensible affirmative example under the ordinary reading of those words.

The conservative campaign classification remains `unsolved, 5/5` because subjective naturalness and historical closure have not been certified. This classification does **not** mean that a proof gap remains in the quantitative theorem, or that the example failed a superpolynomial condition in the original source. No such condition was stated there. Historical priority and whether this example closes the intended question remain qualified.

The adder encoding is established prior mathematics. The packet credits Potechin–Zhang's earlier finite separation and Eén–Sörensson's encoding work. Neither the author nor the audit asserts that the exact asymptotic bound is historically new. The independent review is AI adversarial review, not human journal peer review.

## Separate audit-side encoding robustness

Section 8 of the independent report proves a useful additional observation. If each local gate is replaced by any exact CNF over the same gate variables, every old forbidden full-tuple indicator is a weakening of a replacement clause. The old fractional certificate therefore still applies, and the valid cardinality witnesses establishing the lower bound remain unchanged.

In particular, the conventional seven-clause half-adder and fourteen-clause full-adder encodings have maximum width four. Replacing gates this way gives the same variables, mass upper bound and support/integer lower bound, with `22m-13d-20` clauses. Their exact truth tables were checked independently.

This is a separately justified audit consequence. It does not change the frozen theorem's original `37m-23d-35` clause count or its width-five construction. It also does not justify replacing the entire input by an unnormalized arithmetic axiom or changing the coefficient measure.

## Integrity and what changed for release

No mathematical or executable file in the frozen author packet or independent audit was altered. This top-level scope note and README supply the final interpretation and supersede frozen statements that review is pending. The release manifest inventories all content files by SHA-256, and the original author and audit manifests are retained.

There is no bit-complexity saving claim, no superpolynomial support lower bound, no general encoding-independence theorem, no categorical first-resolution claim, and no new paper or DOI release. Source PDFs and extracted source corpora are excluded.
