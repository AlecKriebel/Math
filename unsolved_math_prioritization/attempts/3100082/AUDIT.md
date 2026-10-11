# Audit of the dimension 26 temporal unimodality counterexample

## Verdict

**Accept the finite counterexample and the disproof of the universal parity-restricted discrete-time conjecture.** All three walk counts, both strict differences, the stated probability normalization, and the stronger rational ratio enclosures were independently reproduced. No correction to the mathematical argument is needed. The prior Anonymous witness must remain credited and described as unrefereed and AI-assisted.

This audit is an independently implemented mathematical and arithmetic check within an AI-assisted workflow. It is not external journal peer review, an authenticated unaffiliated endorsement, a historical-priority determination, or a proof-assistant formalization.

## Exact target checked

The author-hosted Cooper–Spencer PDF has nine physical pages in reverse printed order. Its printed p. 8, physical page 2, states Conjecture 3. Printed p. 2, physical page 8, defines the parity relation by the sum of the coordinates and defines the transition probability by the endpoint at the stated time. Both pages were extracted and visually inspected. The surrounding equal-direction averaging and the dimension-one binomial formula identify the simple symmetric nearest-neighbour model. These are occupation probabilities. Walks that visited the endpoint earlier are included.

The current author problem list's Probability item matches this question. The relevant database identifiers are 3100082 and AMR-030-0082. The record's historical open/unverified classification is not a separate mathematical hypothesis; the finite witness determines the answer to the stated universal question.

For the witness, the coordinate sum is 17. The times 65, 67, 69 are odd and at least the endpoint's lattice distance 17, hence all are reachable. The normalization is 52 per step and 2704 across two steps. No zero-parity interleaving, lazy-walk convention, continuous-time clock, or first-passage event is substituted.

## Exhaustiveness and finite bounds

The return-walk recurrence in PROOF.md partitions walks by the number of step pairs in the newly introduced coordinate. The endpoint recurrence then partitions by the number of negative steps in the displaced coordinate. Time positions and signs uniquely reconstruct the walk, proving both injectivity and surjectivity of each count. The initial zero-dimensional walk is empty exactly when its length is zero. All coefficients used for a left-hand index at most 26 have index at most 26. No numerical cutoff, asymptotic expansion, or estimate is involved.

The number of step strings, 52 to the power 69, need not be explicitly traversed: a proved partition into counted classes is exhaustive. The independent histogram implementation below groups even further, with exact multiplicities; this does not omit trajectories.

## Independent arithmetic constructions

The checker was authored for this audit. It neither imports nor executes other implementations or source-author software. Only Python standard-library integer arithmetic is used. Its checks use explicit exceptions rather than assert statements.

### Coordinate occupancy histograms

Fix the first-coordinate negative count a, put s = r-a, and let D = d-1. For every j >= 1 let c_j be the number of transverse coordinates with exactly j positive and j negative steps. Then sum(j*c_j) = s and k = sum(c_j) <= D. The number of ways to assign this histogram to labeled transverse coordinates is

D! / ((D-k)! product_j c_j!).

For one labeled allocation, the number of time-ordered step strings is

n! / ((m+a)! a! product_j (j!)^(2*c_j)).

Multiplying and summing over a and every such histogram counts every walk exactly once. The histogram is an integer partition of s of length at most D. The implementation enumerates positive parts in nonincreasing order: the first part ranges from min(s, previous_part) down to 1, and recursion decreases the remainder and the available number of parts. Induction on s proves completeness and uniqueness; the zero remainder has exactly the empty continuation. No part greater than s can occur.

As an additional implementation check, the sum of the labeled-histogram multiplicities equals the weak-composition count binomial(s+D-1,D-1), with the zero-dimensional boundary handled separately. Every multinomial division is checked for zero remainder. This method is computationally different from the dimension-by-dimension time-slot recurrence and rational generating-function convolution.

### Squared multinomial recurrence

Define B_D(s) as the sum of (s! / product_i a_i!)^2 over all D-part weak compositions of s, with B_0(0)=1 and B_0(s)=0 for s>0. Choosing one coordinate allocation j gives

B_(D+1)(s) = sum_(j=0)^s binomial(s,j)^2 B_D(s-j).

Grouping the first-coordinate allocation in the walk multinomial count gives

W_(m+2r)(d,m) = binomial(m+2r,r) sum_(a=0)^r binomial(r,a) binomial(m+r,m+a) B_(d-1)(r-a).

To check the latter factorization, each summand for an underlying transverse allocation is exactly (m+2r)! divided by the product of (m+a)! a! and all squared transverse factorials. Thus no probabilistic independence assumption on the coordinate occupation counts is being made. This produces an integer-only computation with factors and scaling different from the time-slot recurrence.

### Time slot recurrence and low dimensional control

A separate implementation evaluates equations (1) and (2) of PROOF.md. All three methods agree on all three large counts. A direct lattice dynamic program, which distributes each state's count to every signed coordinate neighbour without symmetry reduction, checks all three counting functions for d=1,2,3, times 0 through 8, and nonnegative axis endpoints 0 through 9. This gives 810 exact comparisons and includes unreachable distances and wrong parities. Each direct layer also has total mass (2d)^n.

Computing the recurrence arrays with bound 30 instead of 26 preserves each target value. This is an implementation check of the mathematically proved truncation property, not the reason truncation is valid.

## Results and discriminating controls

The exact counts and differences are stated in PROOF.md. Both positive differences are strictly greater than zero. Integer cross multiplication also verifies the narrower ratio intervals with denominator 10^12. No floating-point value is used.

Normal Python, Python -O, and Python -OO all pass with the same mathematical output. In every mode the following deliberately invalid alternatives are rejected:

- Incrementing any one of the three certificate counts by one
- Replacing the two-step normalization 2704 by 52
- Relabeling the times as the unsupported even times 64, 66, 68
- Substituting dimension 25 or endpoint 16 in the certificate
- Reversing the sign of the first positive difference
- Actually testing the alleged valley with multiplier 52: the first required inequality fails
- Omitting the necessary return coefficient of index 26: the resulting W69 is strictly too small
- Substituting first-passage counts: in dimension one, the length-3 occupation count at endpoint 1 is 3, whereas the first-passage count at time 3 is 1

The first eight cases exercise exact certificate identity and metadata validation. The final three exercise substantive model/arithmetic distinctions. A run passes only if all expected failures occur, so the negative controls are not unobserved test files. These checks also survive optimized modes.

The strict decrease followed by strict increase defeats every standard rise-then-fall unimodality convention relevant here, including flat plateaus and monotone limiting cases. No later-tail calculation is needed, and no claim about the total number of modes is inferred.

## Source version and credit

The inspected Anonymous manuscript is version 1.0.0-candidate dated 19 September 2026. The first page identifies the author and unrefereed status and states the same finite witness as Theorem 1. Its Section 2 gives the exact counting formulas; Appendix A prints the three matching counts and signed differences. Page 6 explicitly describes AI assistance and distinguishes internal checks from external peer review. These locations were read; title, counting, status, and certificate pages were also visually inspected. The current Evidence Press page and GitHub release retain candidate status.

The GitHub release identifies commit 95678898ede180f04d6b416e605faa73aed58196 for the candidate tag. Source PDF byte counts and SHA256 hashes are in SOURCE_PINS.json. Public source URLs are given there and in PROOF.md. The prior source's finite witness is credited. Its statements about d >= 64, continuous time, Bessel functions, and any priority search are outside this audit and are neither prerequisites nor certified conclusions.

## Publication boundary

PROOF.md is self-contained through its finite recurrences, three essential integers, and two differences. AUDIT.md and ACCEPTANCE.md provide authored verification commentary; SOURCE_PINS.json contains public provenance metadata. The report is self-contained without distributing implementation files. No raw exhaustive count table or third-party source text is needed for the proof.

The public report contains authored mathematical exposition and verification metadata. It does not redistribute source documents, extracted source text, page images, software, or exhaustive count tables.
