# EP377 / 2083: carry-depth barriers and fixed-shell limits

This prose-only edition is AI-assisted and unrefereed. “Accepted” means an
independent internal AI audit of the stated partial results. No external human
peer review, journal acceptance or formal proof-assistant certification is
claimed. No novelty or priority is claimed. The absolute-bound target remains
unresolved by this work.

Source inspection and finite computations described below are historical
activities of the original proof and independent audit, not new work performed
to prepare this edition. No new mathematical test or scholarly-source inspection
was performed during edition preparation. Executable code, raw datasets,
detailed receipts, full computational certificates and copied third-party
sources are excluded. This is not an executable reproduction package.

For B_n=binom(2n,n), let f(n) be the sum of 1/p over primes p<=n that do not
divide B_n. The target is an absolute upper bound independent of n.

## What is established

- Exact carry, digit and residue criteria for prime nondivisibility.
- No summable all-n shell-depth-only envelope, even after finite prime deletion.
- An unbounded common-depth relaxation for L(n)=o(log n), and equivalence to
  the full target up to a finite-prime constant for each fixed positive
  logarithmic depth floor(c log(2n)).
- For each fixed r, the all-n limit F_r(n)->2^(-r) log(1+1/r), derived from
  Sander's published estimate. No uniformity as r increases is asserted.
- liminf f(n)=c0 and limsup f(n)>=c0+8/15, with c0=sum_{k>=2} log(k)/2^k,
  using the published EGRS first-moment and two-base inputs.

The remaining deep-shell reciprocal mass is uncontrolled. Neither the moving
fixed-prime examples, the relaxed cutoff obstruction, nor a weighted
asymptotic proves or refutes the full bound. No arbitrary-finite-prime
simultaneous nondivisibility theorem or sharp limsup is claimed.

## Reading order

1. PROOF.md contains the full substantive authored proof.
2. AUDIT.md contains the complete independent mathematical audit, including
   limiting arguments, edge cases and historical finite verification scope.
3. ACCEPTANCE.md and ACCEPTANCE.json state the accepted scope and bind the
   exact editorial proof/audit bytes.
4. SOURCES.json records public citations, PDF hashes and sizes, and historical
   inspection/retrieval limits. VERIFICATION.json gives aggregate historical
   check results and receipt identities. MANIFEST.json binds the selection.

The proof and audit are preserved with editorial distribution framing,
historical-verification wording, public-file references and the explicit
vacuous empty-set clarification. There are no substantive math corrections.
The original proof and audit packages are unchanged. This edition contains
eight additions only; existing repository content is preserved.

## Published inputs and attribution

- Erdős, Graham, Ruzsa and Straus, On the prime factors of (2n choose n),
  Mathematics of Computation 29 (1975), 83–92:
  https://www.renyi.hu/~p_erdos/1975-27.pdf
- J. W. Sander, On primes not dividing binomial coefficients (1993):
  https://doi.org/10.1017/S0305004100075927
- J. W. Sander, Prime power divisors of binomial coefficients (1992):
  https://doi.org/10.1515/crll.1992.430.1

The preceding publications and standard Mertens/Fourier tools are explicitly
credited. Earlier analytic theorems used in Sander's proof are accepted
published inputs. No novelty, priority or exhaustive literature search is
claimed for this assembled argument.
