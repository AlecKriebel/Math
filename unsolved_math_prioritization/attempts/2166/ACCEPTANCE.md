# Acceptance of the prior EP538 matching-order claim

## Exact accepted problem

For a natural cutoff N and integer r>=2, maximize S(A)=sum_{a in A}1/a
over subsets A of the positive integers at most N. For every integer m,
the number of ordered pairs (p,a), with p prime, a in A and m=pa, must be
at most r. There is no restriction to products below N, and no squarefree
or coprimality premise on arbitrary admissible A. Denote this maximum E_r(N).

The prior result credited to STARFLEET Math gives, for each fixed r>=2,
E_r(N)=Theta_r(log N/log log N). The following precise finite assertions
are accepted:

1. For r>=2, N>=2 and every admissible A,

       log(log(N+1)) S(A) <= 2r (1+log(N^2)).

2. For every natural N, there exists A_N contained in {1,...,N}, with
   the original global cap two, such that

       log(N+1) <= 4+8192(ell(N)+1) S(A_N).

Here L(0)=0, L(N)=floor(log_2 N) for N>=1, and ell(N)=floor(log_2 L(N))
when L(N)>=1, with ell(N)=0 otherwise. Logs without subscripts are natural.
The empty set covers N=0; all stated denominators and endpoint conventions
are checked in the written audit.

For every r>=2 and N>=ceil(exp(8)), these imply the deliberately nonsharp
comparison

    (1/65536) log N/log log N <= E_r(N) <= 6r log N/log log N.

The r-dependence is not a matching growing-r theorem. No sharp leading
constant, exact finite maximum or novel-priority claim follows.

## Basis and scope of review

AUDIT.md reconstructs the complete conventional proof. It proves the
weighted incidence upper estimate, favorable finite-field child count,
exact outside danger probability, one common safe palette, cap two via
odd-characteristic polarization, weighted rainbow transfer, every repeated
color pattern, squarefree and nonsquarefree products, the k=1 boundary,
exact Omega-layer union, harmonic truncation, the coefficient 8192 and
fixed-r asymptotic deduction. No load-bearing gap or required mathematical
correction was found at that scope.

FOCUSED_AUDIT.md independently reconstructs the safe-kernel lower bound,
including child parametrization, danger probability, common labeling,
weighted transfer, original all-m cap, layer union, unit contribution,
prime-harmonic bound and exact coefficient. It passes at that focused scope;
it does not claim an independent second audit of the upper bound.

Historical independently authored exact checks passed in normal, -O and
-OO modes with byte-identical outputs. They are supporting evidence only;
universal acceptance rests on the written proofs. The publication stage
checks edition bytes, scope and addition-only structure, without rerunning
mathematical checkers or executing third-party code.

## Source fidelity and formal boundaries

The original source is P. Erdős, *Problems and Results on Combinatorial
Number Theory* (1973), section 4, printed p.124, equation (4.5). The primary
audit authenticated the retained 22-page PDF and visually inspected the
target page and its context; it did not audit every unrelated survey topic.
It read the complete STARFLEET #538 prose and inspected the retained final
statements and selected load-bearing archive modules as inert text.
SOURCES.json records exact byte identities, match and inspection metadata.

Both READMEs cite an absent experiment_1_formal_statement location. The
actual 1,923-byte Problem538.lean is under experiment_24_safe_kernel_arithmetic,
SHA-256 2095828c87994722fc02195edfd08c5a89e9768f96d2a9e7b02a86e4ca5177c3.
The final Proof.lean copy and FinalMatchingOrder.lean are byte-identical,
1,656 bytes, SHA-256
3edd0e3113677c0f3490df253ed93b3f09b0f8b7956bd6aead86a31a5e13f35e.
The website's schematic signature is not treated as the literal archive
theorem type: the inspected theorem states the two finite inequalities.

The project asks for mathlib using a movable stable label, while its retained
manifest pins fabf563a7c95a166b8d7b6efca11c8b4dc9d911f and its toolchain
specifies Lean 4.31.0. No dependency refresh was attempted. The publisher
reports formal success; no local Lean build, formal-kernel replay or
transitive axiom computation independently reproduces that report here.
Static scans and retained local import closure cannot substitute for it.

Acceptance is independent internal AI mathematical review, not external
human peer review, journal acceptance or local proof-assistant certification.
This AI-assisted work is unrefereed. No current tracker-status or exhaustive
community-resolution assertion is made.

## Edition treatment

Both full general derivations and all theorem constants are preserved.
Only optional primary finite examples, numerical computational witnesses,
finite test ranges, historical-check wording and the metadata filename are
edited. Source bodies, PDFs, code, raw certificates, datasets and private
coordination are excluded. Original sealed packets remain immutable inputs.

Sources: [STARFLEET Math](https://www.starfleetmath.com/);
[verification archive](https://www.starfleetmath.com/downloads/verify/erdos-538/erdos-538-solution.zip);
[Erdős original](https://www.renyi.hu/~p_erdos/1973-21.pdf).
