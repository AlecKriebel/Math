# EP413 / problem 2104: corrected prior prime-factor barriers

## Accepted result and remaining problem

For one absolute C>0, infinitely many positive integers n satisfy

    omega(n-k) <= Omega(n-k) <= C log k,  2<=k<n.

Here omega counts distinct prime factors, Omega counts with multiplicity,
omega(1)=Omega(1)=0, and log is natural. This is the backwards result of
Cheuk Fung (Joshua) Lau, *On the Number of Prime Factors of Consecutive
Integers*, [arXiv:2604.15042v2](https://arxiv.org/abs/2604.15042v2),
24 June 2026, accepted here through complete authored proof corrections.
The accepted multiplicity proof uses fixed A=100 and s=ceil(4 log k).

Put N=n-1 and epsilon=1/(C log 2). Then every positive integer m<N obeys

    m + epsilon*omega(m) <= m + epsilon*Omega(m) <= N.

The same one epsilon works for infinitely many N. The closest endpoint uses
k=2; the theorem never asserts its logarithmic bound at k=1. No numerical C
or epsilon is certified. The coefficient-one problem remains unresolved: a
fixed finite terminal window still needs simultaneous control at infinitely
many witnesses. No novelty, priority, or whole-problem resolution is claimed.

## Reading guide

1. AUDIT.md records the exact original statement, source inspection, printed
   errors, corrected theorem, endpoints, and remaining coefficient-one gap.
2. KERNEL_REPAIR.md supplies exact-Euler-product factorization, the
   nonnegative-translation algebra, and valid integrated normalization.
3. DISTINCT_OMEGA_RECONSTRUCTION.md supplies the CRT/Fourier antecedent,
   fixed-schedule distinct-prime moments, and complete existence argument.
4. MULTIPLICITY_REPAIR.md extends that chain at A=100, using signed CRT main
   terms, absolute error sums, a uniform prime-power budget, and tiny-prime
   excess tails. Together these three modules give the complete proof.
5. SECOND_AUDIT.md, SECOND_KERNEL_REPAIR.md and SECOND_DISTINCT_OMEGA_CHAIN.md
   give the complete separate earlier distinct-only audit and derivation.
   Their appended scope notes point to SECOND_MULTIPLICITY_AUDIT.md, the
   complete separate acceptance and derivation of the full Omega extension.
6. ACCEPTANCE.md and ACCEPTANCE.json state the final bounded disposition.
   SOURCES.json records public citations and historical source verification;
   VERIFICATION.json separates written proofs, supplementary historical
   checks, and publication preparation. MANIFEST.json binds this edition.

## Publication and review boundaries

The printed p.28 absolute-value identity, p.16 uniform growing-moment estimate,
broad parameter claims, and p.35 signed inequalities are not endorsed. The
authored replacements establish the needed narrow schedule without them.
Standard prime number/Mertens estimates, CRT, Fourier inversion and ordinary
analytic/combinatorial facts remain explicit mathematical inputs.

Acceptance is independent internal AI review. This AI-assisted work is
unrefereed; no external human peer review, journal acceptance, or formal
proof-assistant certification is claimed. The historical distinct-only scope
is preserved and explicitly supplemented rather than silently rewritten.

This edition contains authored prose and public verification metadata only.
It excludes copied source bodies/PDFs/images, code, raw computational
certificates or datasets, numeric computational witnesses, private sources,
and private coordination material. Analytic numerical constants and their
written derivations are part of the proof, not computational certificates.
It is not an executable reproduction package. Preparation adds no new source
inspection or mathematical experiment. The original sealed research packets
are unchanged. The proposed repository patch adds only this attempt directory;
QUEUE.md and every unrelated repository path remain unchanged.
