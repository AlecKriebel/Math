# Independent audit: slowly growing image inradius

Problem 2305005 / AMR-022-5005; queue rank 1034. Audit date: 2026-10-08.

## Decision

**Accept the five approaches as qualified partial work. Retain `unsolved`, 5/5, for the literal-limit problem. No correction patch is required.**

The packet proves its elementary geometric and analytic claims. Its negative answer to an upper-envelope-only formulation is conditional on the domain theorem attributed to Fernández in the inspected problem collection. It does not prove that the resulting map's actual image has inradius tending to infinity. The report explicitly preserves this gap, so the partial-work disposition is accurate.

This acceptance does not claim a new complete solution, worldwide current openness, novelty, independent verification of Fernández's original proof, peer review, or resolution by an onto-map theorem. Source recovery, duplicate screening, computation, packaging, and this audit count as zero additional mathematical approaches.

## 1. Frozen input and trust boundary

The author input was preserved byte for byte. The separately supplied pins were checked before executing the pinned verifier:

- Author archive: `SLOW_INRADIUS_2305005_AUTHOR_PACKET.zip`, 20,951 bytes; SHA-256 `8c85e9a8e91e9a0124b62644a7663d7c69b487bb579678ef5772a57e0f1671a1`.
- Author manifest: `MANIFEST.json`, 1,082 bytes; SHA-256 `916ef2162da505bef37aab22de595ccc2c91497908a3b8f28f9c29a81588356a`.
- Author freeze receipt: `AUTHOR_FREEZE_RECEIPT.json`, 3,516 bytes; SHA-256 `7e17750906cdf0c3f2c2a6fef621c98cdf3ac756b307e6b7856cc89f8036a15b`.
- Executed author verifier: `verify.py`, 10,889 bytes; SHA-256 `487fcef8ed8739fc083835904b3093cd99920c388a3a07e6e48a712a5f7ed870`.
- Reviewed author report: `REPORT.md`, 17,949 bytes; SHA-256 `8dad8162b583d12b5dfd89bffa86a3f3fe2dbf58165a5b01b7e4bcb5dff6cf05`.

The archive contains exactly eight unique regular-file members: CLAIMS.json, FIXTURES.json, MANIFEST.json, README.md, REPORT.md, SOURCES.json, controls.py, and verify.py. Each archived member agrees exactly with the corresponding frozen loose file. The manifest lists the seven other members. No source document, source image, dataset body, or private coordination material occurs in this allowlist.

An external pin is a trust input, not something a verifier can authenticate by trusting a replacement manifest supplied alongside altered data. The audit therefore independently checked the archive, manifest, receipt, fixed inventory, and verifier bootstrap hash. Mutations with intentionally recomputed test pins probe semantic checks; they do not replace the actual trusted pin.

## 2. Scope and source inspection

The mathematical variable r is a radius in the value plane. For a nonconstant holomorphic f on the unit disk, put Omega=f(Delta). Its relevant radius function is the largest radius of an open disk contained in Omega whose center has modulus r, with value zero when no positive disk is available. Multiplicity and single-sheeted covering are irrelevant. For proper Omega this equals the maximum of distance to its complement on the circle of radius r. Distance is continuous and 1-Lipschitz; compactness yields the maximum. Comparing points on a common ray shows that d_Omega is 1-Lipschitz. Entire-plane image gives infinite radius at every r. Constant functions cause no difficulty: their radius function is zero and their coefficient sequence is bounded.

The coefficient conclusion is boundedness for each individual function, including its one finite constant coefficient. It is not a family-uniform bound. There is no given injectivity or normalization. The report correctly avoids substituting source-disk radii approaching one, an inverse-branch radius, or a varying-degree polynomial family.

The inspected collection's Problem 5.5 uses actual image geometry. Its Update 5.5 reports a criterion for all maps with values in a prescribed domain. The imported statement concerns capacity-zero complement and bounded contained disk radii. It does not specify onto counterexamples. The current PDF's bounded-coefficient equation number is 5.10. The audit inspected both extracted text and the supplied image of printed page 86, and cross-checked the public HTML. The original Fernández theorem and proof were not obtained. Publisher metadata alone supplies no stronger theorem. [Collection](https://arxiv.org/pdf/1809.07200v2), [HTML](https://arxiv.org/html/1809.07200v2), [Fernández bibliography](https://annals.math.princeton.edu/1984/120-3/p04), [DOI](https://doi.org/10.2307/1971085).

The latest inspected PR 807 head is `1da2801e3f6da057b5b65cd00b0141df053c96d9`. Its declared target is 2305007: shrinking inradius and coefficient decay. It does not supply the missing onto unbounded-coefficient assertion for a slowly widening domain. It is related context, not a duplicate resolution of this packet. [PR 807](https://github.com/AlecKriebel/Math/pull/807).

## 3. Route 1: independent reconstruction of the geometry

Assume H is finite, nondecreasing, at least 16, and divergent. Define

    h(r) = (1/4) inf over s>=0 of [H(s)+|r-s|].

Each candidate as a function of r is 1-Lipschitz before division by four; the infimum has the same Lipschitz bound. Positivity and the candidate s=r give 4<=h(r)<=H(r)/4. Because H is nondecreasing, candidates s>r cannot improve on s=r. For r2>r1, candidates s<=r1 are no smaller than their value at r1, while the new candidates r1<s<=r2 are at least H(r1), which is at least 4h(r1). Thus h is nondecreasing, even if H has jumps or the infimum is not attained.

Splitting the infimum at s=r/2 gives

    h(r) >= (1/4) min(16+r/2, H(r/2)).

Both terms tend to infinity, so h diverges. No smoothness, strict increase, or attainment of the infimum is needed.

Set E={m+in : m,n are integers and |n|>=h(|m|)} and D=C\E. This is a nonempty closed locally finite subset of the square lattice, and its complement is path connected: a finite line segment meets only finitely many omitted points, each avoidable by a small arc. Every compact subset of E is finite and has logarithmic capacity zero. Equivalently, E is a countable polar set. These facts apply to the actual infinite E, rather than being inferred from finite tests.

For the lower bound, use the center r on the real axis. An omitted point with |m-r|>=h(r)/2 is already sufficiently far away horizontally. Otherwise,

    ||m|-r| <= |m-r| < h(r)/2,
    |n| >= h(|m|) > h(r)-h(r)/8 = 7h(r)/8.

Consequently every omitted point is at distance at least h(r)/2 from r. The open disk of that radius is contained in D.

For the upper bound, write w=x+iy, |w|=r, and choose an integer m within 1/2 of x. Select an integer n on either sign when y=0, and otherwise on the sign of y, with magnitude at least ceil(h(|m|)) and with |n-y|<=h(|m|)+1. Such an n is supplied either by rounding |y| or by that ceiling. Since |x|<=r,

    h(|m|) <= h(|x|)+1/8 <= h(r)+1/8.

Using coordinate distance as an upper bound on Euclidean distance gives

    dist(w,E) <= h(r)+13/8 < h(r)+2.

Therefore the advertised estimates are valid:

    h(r)/2 <= d_D(r) <= h(r)+2 <= 3H(r)/8 < H(r).

In particular d_D(r) tends to infinity. The slack constants handle integer rounding, including small r. Eventual envelopes are accommodated by modifying an initial interval; an arbitrary finite positive function tending to infinity has an eventual nondecreasing divergent minorant given by its tail infimum.

The qualified historical theorem now yields a map f into D with an unbounded coefficient sequence, because D contains arbitrarily large disks and has polar complement. Inclusion gives d_f<=d_D<=H. This is a correct refutation of the upper-envelope-only criterion, conditional on that theorem.

It remains only an inclusion. The image f(Delta) can be smaller than D. The bounded-inradius coefficient implication forces d_f to be unbounded; an omitted point bounds d_f on each bounded r-interval, giving limsup at infinity equal to infinity. A 1-Lipschitz function can have arbitrarily high widely separated peaks while returning to zero. Thus neither unboundedness nor regularity supplies the required limit. This is the decisive unclosed gap.

## 4. Route 2: Bloch and Cauchy bounds

If no disk in f(Delta) has radius greater than R, apply Bloch's theorem to f after a disk automorphism taking zero to z. Its derivative modulus at zero is (1-|z|^2)|f'(z)|. Any smaller fixed positive universal Bloch constant beta therefore gives

    (1-|z|^2)|f'(z)| <= R/beta.

Cauchy's estimate for the coefficient of z^(n-1) in f' gives

    n|a_n|t^(n-1) <= R/[beta(1-t^2)].

At t=1-1/(2n), Bernoulli gives t^(n-1)>=1/2, and direct arithmetic gives n(1-t^2)=1-1/(4n)>=3/4. The stated bound |a_n|<=8R/(3beta) follows, for all n>=1. The constant coefficient is separately finite. Injectivity is not used.

For a global nondecreasing envelope H, a disk in the source of radius s-t centered on |z|=t stays inside |zeta|<s. The Bloch image disk center has modulus at most M_f(s). Its radius is therefore at most H(M_f(s)), giving the report's variable-envelope estimate. At t=1-1/n and s=1-1/(2n), n(s-t)=1/2 and (1-1/n)^(n-1)>=e^(-1), giving the factor 2e/beta. This argument does not bound H(M_f(s)) as s approaches one. It does not prove the target implication.

## 5. Route 3: onto approximation and the exact category gap

The punctured domain is hyperbolic, so a universal covering map pi:Delta->D exists and is onto. Every g in Hol(Delta,D) lifts to a disk map h with g=pi composed with h. This covers constant maps as well.

The Schur algorithm removes h(0)=gamma by a disk automorphism, divides by z, and iterates. Replacing a sufficiently late tail by a unimodular constant and reversing the steps produces a nonconstant finite Blaschke product. The first prescribed finite jet is preserved. Taylor coefficients of disk maps have modulus at most one, so agreement through degree N-1 implies an error at most 2r^N/(1-r) on |z|<=r. Early termination gives a finite Blaschke product already. A disk-valued constant does not force a constant unimodular approximant: taking at least one reverse step produces a nonconstant approximant. Thus the construction genuinely supplies onto finite-Blaschke approximants.

Composition with pi preserves local uniform convergence, and each pi composed with a nonconstant finite Blaschke product is onto D. Hence onto maps are dense in Hol(Delta,D). This part of the route is valid.

For each integer m, the set of maps whose every coefficient has modulus at most m is closed, since each coefficient is a continuous functional in the local uniform topology. A single unbounded-coefficient map lies outside their union. It does not imply that each closed set has empty interior. Two dense sets need not intersect unless stronger hypotheses are available, and here the unbounded-coefficient set has not even been proved dense.

The proposed sufficient Baire strengthening is coherent. For this countably punctured D, Hol(Delta,D) is a G-delta subspace of the complete space Hol(Delta,C): on each closed subdisk, a map must stay a positive distance from each omitted point. It is therefore Baire. For a compact exhaustion K_j of D, the conditions K_j subset g(Delta) are open by finite local Rouché stability and dense by the established onto approximation. The conditions that some coefficient exceed a prescribed A are open; their density is the missing claim. If this density were proved for every A, Baire would indeed impose both properties simultaneously. The report does not assert that the missing density follows from the historical theorem.

The polynomial-partial-sum example in the unrestricted holomorphic function space is used correctly as a warning about coefficient bounds under local uniform limits, not as an approximation theorem inside D. The universal covering map and arbitrary onto approximants cannot simply be substituted for the historical counterexample.

## 6. Route 4: logarithm squared

The Cayley map sends the unit disk onto the right half-plane, and the principal logarithm sends it onto the strip |Im zeta|<a with a=pi/2. For w=u+iv, a square root has squared imaginary part (|w|-u)/2. Thus squaring the strip gives exactly the region

    u > v^2/(4a^2)-a^2.

No missing branch or slit invalidates this onto statement. For real r>=a^2, the squared distance to the boundary point t^2-a^2+2ait is

    (t^2-(r-a^2))^2+4a^2r.

Its minimum is 4a^2r. This supplies d_f(r)>=2a sqrt(r). At another center u+iv on the same radius circle, the nearer boundary point on its vertical line is at distance at most 2a sqrt(u+a^2), and u<=r gives the reported upper bound. Therefore d_f(r) is asymptotic to pi sqrt(r).

The series L(z)=2 sum over odd j>=1 of z^j/j gives zero odd coefficients after squaring. At n=2m, partial fractions in the finite convolution give

    a_(2m) = (4/m) sum from j=1 to m of 1/(2j-1).

The sum is O(log m), so these coefficients tend to zero. This is a correct large-inradius example with bounded, indeed decaying, coefficients. It is not a counterexample to the target conclusion. The complement has positive capacity, so the example does not conflict with the quantifiers or hypothesis of the imported polar-domain theorem.

## 7. Route 5: lacunary failure

The series sum 4^k z^(8^k) converges uniformly on compact subdisks, and its coefficient sequence is unbounded. On |z|=2^(-1/8^k), the kth term has modulus 4^k/2. Earlier terms sum to less than 4^k/3. For j>=1, 8^j>=8j, hence the later terms sum to at most

    4^k sum (1/64)^j = 4^k/63.

The remaining strict margin is greater than 4^k(19/126). For any w with modulus below this margin, Rouché compares the full function minus w with the kth monomial and forces a zero in the source disk. Increasing k covers every finite w. The entire-plane image claim is therefore proved, not guessed from large coefficients or numerical samples. Its inradius is infinite at every value radius and it cannot obey a finite envelope. The report correctly limits this obstruction to the tested construction rather than all lacunary strategies.

## 8. Computational and integrity results

All following results concern exact finite calculations or byte integrity. None computes an infinite analytic theorem.

1. Replayed the author's 6,806 finite checks in normal, -O, and -OO modes, with identical output: 64 coefficient identities; 3,084 lattice upper checks; 2,119 lattice lower checks; 771 height checks; 384 parabola identities; 256 lacunary inequalities; 128 Bloch scalar checks.
2. Replayed all 21 author corruption cases in each mode: 63 rejections. Repeated author read-only relocation as a genuine UID-1000 process; both attempted creation and attempted append were denied, all three modes passed, and the file inventory and hashes stayed unchanged.
3. Independently wrote 37 additional negative cases, each run in normal, -O, and -OO modes: 111 rejections. These include boolean and float identifiers/counts, booleans in integer slots, finite floats, NaN, negative infinity, overflow-form JSON, duplicate keys, invalid rational directions, zero denominators, altered claim flags, invalid external pins, unsafe path spellings, root and manifest symlinks, extra nested payload, and mismatched optional source inputs.
4. Independently recomputed 20,510 further exact checks: 256 coefficient convolutions; 256 Bloch scalar bounds; 512 lacunary inequalities; 1,156 rational parabola identities; 3,005 properties of a piecewise-affine H and its exact infimal envelope; 4,808 lattice upper checks; and 10,517 lattice lower checks. The additional height fixture crosses slope changes above and below one, rather than merely reusing the author's height routine.
5. Independently repeated nonroot read-only relocation in the new harness, again denying both creation and append. All three verifier modes returned the baseline output; the relocated and original packets stayed unchanged.
6. Rehashed both complete authorized datasets, independently selected and canonicalized the designated records, and rehashed the inspected PDF. All whole-file and record pins matched. The author's optional source replay also passed in all three modes, with identical output. Public receipts contain only hashes, sizes, labels, and match results.

The new audit harness itself was run in normal, -O, and -OO modes with identical JSON results. Runtime validation uses explicit condition checks, not removable assertions. `CHECK_RESULTS.json` records the counts and labels; `audit_checks.py` reproduces the additional checks against the frozen author input.

Reproduce the audit harness with Python 3.12 or later as an ordinary nonroot POSIX user, supplying local paths to the unchanged author inputs:

    python -B audit_checks.py --author-root AUTHOR_PUBLIC_DIRECTORY --archive AUTHOR_ARCHIVE --receipt AUTHOR_FREEZE_RECEIPT

Repeat with `-O` and `-OO` after `-B`. The harness authenticates the fixed external author pins before executing the author verifier, works on disposable temporary copies, and does not require source documents or datasets. Full source binding replay is separately available through the author verifier's optional input arguments. Neither command publishes anything.

### Limits of the verifier

The verifier is not a general-purpose mathematical proof checker or a validator for arbitrary newly authored manifests. It guards selected mathematical identities and selected status flags, while the external manifest pin authenticates all other exact content. It does not establish Fernández's theorem, the category density strengthening, a surjective counterexample, or correctness of every sentence under arbitrary repinning. Optional source rehashing is optional and is explicitly distinguished in output. The generic inventory check lists regular files; the independent audit additionally fixed the eight-file allowlist and matched every archive member. These are scope limits, not failures of the frozen packet's advertised accepted result.

## 9. Accepted disposition and remaining task

Accepted status: **unresolved in this investigation; five mathematical approaches completed**. Recommended queue representation: **unsolved, 5/5**. This audit does not edit the queue or publish anything.

Accepted mathematical scope:

- A self-contained slowly widening polar-complement domain construction with the stated lower and upper bounds.
- A negative upper-envelope-only result conditional on the accurately qualified historical input.
- A bounded-inradius coefficient estimate, a valid but insufficient variable-envelope estimate, dense onto approximation, an explicit decaying-coefficient parabola example, and an exact entire-plane-image obstruction for the lacunary candidate.

Still required for a literal-limit negative solution: construct or authoritatively verify an unbounded-coefficient map whose actual image inradius tends to infinity and stays below an arbitrary prescribed slow divergent envelope. An appropriate onto strengthening would suffice. A positive literal-limit theorem or authoritative source resolving that exact formulation would also settle the target. None was supplied here.

No source text or source body is attached. Only the original eight-member packet, its frozen archive and receipt, and the separately hashed audit artifacts named in the audit manifest are eligible deliverables. The original author's pending-audit labels remain historical frozen content; this separate acceptance records completion of the independent review without rewriting them.
