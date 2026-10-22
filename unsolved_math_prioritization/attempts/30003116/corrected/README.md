# Quantitative entropy of rational multiplicative orbits

Problem **30003116 / OWR-14603-015**, normal queue rank **993**.

## Disposition

**Intended sufficiently-large-denominator problem: unresolved after five distinct mathematical approaches.** This packet contains rigorous restricted results and explicit gaps. It does not claim a proof or counterexample to the asymptotic question, research novelty, formal verification, or human peer review. The work was AI-assisted and has not received independent review in this packet.

There is a genuine defect in an unqualified all-denominators reading: the admissible pair a=4,b=7 fixes 1/3, contradicting a positive logarithmic entropy bound at s=3. That finite exception is separated from the intended asymptotic problem rather than used to force a solved label.

## Target, conventions, and source discrepancy

The controlling source is Elon Lindenstrauss's Question 2 in *Around Furstenberg's ×2 ×3 theorem*, OWR 21/2016, printed pp.1127–1128, DOI [10.4171/OWR/2016/21](https://doi.org/10.4171/OWR/2016/21). It asks for constants depending only on multiplicatively independent integer bases so that the rational orbit, with each exponent bounded by a constant times log s, has logarithmic covering number at scale (log s)^(-N) bounded below by a positive multiple of log log s. The source writes 1/K rather than K, an equivalent positive-constant parameterization. Covering uses intervals of the stated length.

We work with a,b>1, unit numerator r modulo a positive denominator s, gcd(s,ab)=1, nonnegative exponents, positive constants, and sufficiently large s. These conventions make the mathematical question meaningful. The printed source does not explicitly add the large-s threshold. The finite issue above and s=1 are disclosed, not silently removed.

The printed Baker-case condition is |s|<r^(1-theta). It was checked in the page image. Replacing r by r+js preserves the orbit while eventually satisfying that condition for 0<theta<1. Consequently it cannot simply be adopted as a meaningful restricted residue condition without clarification. Approach 2 proves its own explicit small-residue condition; it does not claim to repair the author's intended wording.

## Five approaches and retained results

1. [Congruences and finite exceptions](01_congruence.md): exact grid-scale cardinality, fixed-point classification, and why a cardinality-only transfer is insufficient.
2. [Logarithmic-form small seeds](02_logarithmic_seed.md): the desired bound under a power-small forward-residue hypothesis; extension near bounded-denominator rational points. Baker–Wüstholz is an explicitly credited external input.
3. [Difference amplification](03_difference_amplification.md): uniformly in all admissible r,s, at logarithmic time,
   C(A,(log s)^(-4)) >= c sqrt(log log s).
   This is much weaker than the requested (log s)^c covering bound. A power-close pair would suffice for the target but is not obtained.
4. [Averaged collision energy](04_average_collision.md): for all sufficiently large prime p not dividing ab, all but at most (p-1)/sqrt(log p) numerators satisfy
   C(A,(log p)^(-6)) >= c (log p)^(3/2).
   The worst numerator and composite denominators remain gaps.
5. [Empirical entropy](05_empirical_entropy.md): exact approximate-invariance identities and a precise entropy-production gap; a single-generator symbolic example explains why fine entropy cannot automatically survive the change of scale. It is not a two-generator counterexample.

## Literature and duplicate-search scope

The [source and search record](source_scope.json) gives versioned PDF identities, inspection ranges, bounded search coverage, and exclusions. Bourgain–Lindenstrauss–Michel–Venkatesh's 2009 theorem already supplies logarithmic-time rational-orbit density at a triple-log scale. It is prior work, not a new result of this packet. Fan–Queffélec–Queffélec's 2024 paper supplies related semigroup gap/distribution results, without being used as a solution of this finite-orbit target. A 2024 Burton–Panangaden abstract concerns equivalent formulations of measure/periodic-equidistribution conjectures, not this covering estimate. No later resolution of the precise target was verified in the bounded search. Current global openness is not certified by absence of search hits.

Exact/source-code and semantic PR/branch searches, the observed main attempt-directory listing, main target-path commit history, and main queue/state/history records found no earlier target attempt. Related Furstenberg measure-classification and two-torus questions are substantively different. No exhaustive all-branch full-text history claim is made. The supplied research corpus contains unsupported measure-rigidity solution claims in a different problem; those claims are not used here.

## Reproduction and frozen scope

Run Python 3 using the externally supplied SHA-256 of MANIFEST.json:

    python -B verify_public.py --expected-manifest <SHA-256>

The verifier binds the exact flat packet inventory, rejects symlinks and extra paths, verifies each byte count and SHA-256, checks that executable validators contain no assert statements, and reproduces checks.json through check_math.py. The latter performs **86,778 exact finite checks**. These computations supplement the written proofs; they cannot certify universal asymptotic claims or Baker's theorem. Normal Python, -O, and -OO are supported because checks use explicit exceptions. Mathematical and actual mutated-packet negative controls are documented in the separate frozen verification receipt supplied with the packet.

MANIFEST.json is the sole self-hash exception and must be externally pinned. The separate receipt/archive are not recursive members of this manifest. No copied PDFs, extracted source text, page images, raw corpus records, dataset contents, repository queue, private coordination files, or private personal data are included. Public source titles/URLs, byte counts, hashes, match results, inspection metadata, authored mathematics, and authored validation code/results are included. There were no remote writes or publications for this investigation.
