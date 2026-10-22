# Independent audit of Rubel planar equilibrium resolution

## Verdict

**Accepted as an exact prior resolution, with no mathematical correction required.** The reviewed argument is valid for Problem 7.78, identified by 2307078 / AMR-022-7078. The requested zero-free sum cannot exist. More strongly, every admissible sum has infinitely many distinct zeros away from its poles.

This is a literature-status correction and an expanded elementary reconstruction of an established special case. It is not a new solution to an open problem. Clunie, Eremenko and Rossi explicitly state the exact special case on printed p. 310 of their 1993 paper, before Theorem 2.1. Hayman and Lingham Update 7.78, printed p. 186, already acknowledges the planar resolution. See the [primary paper](https://www.math.purdue.edu/~eremenko/dvi/cer.pdf) and [Hayman and Lingham v2](https://arxiv.org/abs/1809.07200v2).

The examined argument has 6,243 bytes and SHA-256 `7549bac5b1897865a8653c1822e447b63099e4d30e67a6c765e79e45600e761e`. The audit was performed on 11 October 2026. `PROOF.md` supplies a complete authored proof; `SOURCE_PINS.json` records the public source identities and inspection locations.

## Exact hypothesis match

The original statement is on Hayman and Lingham printed p. 185, continuing to p. 186, corresponding to physical PDF pages 186-187. It asks about an infinite sequence of distinct complex numbers, convergence of the sum of reciprocal moduli, and nonvanishing of the sum of reciprocal differences. The audited theorem retains each of these assumptions. The exclusion of zero among the charge locations is already forced by the finite reciprocal-modulus sum.

The original phrase about all complex values has to be interpreted off the charge locations. The series has a genuine pole of residue one at each location. The proof does not treat undefined values at poles as a trivial negative answer; it proves genuine equilibrium points elsewhere.

The primary paper states the more general absolute convergence assumption with coefficients on printed p. 309. Taking every coefficient equal to one gives exactly the condition above. Its printed p. 310 separately identifies the case of distinct locations and unit coefficients. Reliance on this paragraph avoids silently importing stronger multiplicity or charge hypotheses from other results in the paper.

## Mathematical audit

1. **Discreteness and the series.** A summable sequence of positive reciprocal moduli tends to zero, hence the locations leave every compact disk. On a disk of radius R, the tail denominators give the uniform bound 2/|z_n|. The series converges locally uniformly off the locations. Removing one summand near a location leaves a holomorphic function, so there is no pole cancellation.

2. **Product convergence and zeros.** The power-series branch of log(1-z/z_n) is defined on each sufficiently distant tail and bounded by 2R/|z_n| on the disk of radius R. Its normally convergent sum exponentiates to a nonvanishing tail product. The finite head determines all zeros and their multiplicities. Since the locations are distinct, all zeros are simple. The value at zero is one, so the product is not identically zero; infinitely many distinct zeros make it transcendental entire.

3. **Logarithmic derivative.** Differentiation of the locally normally convergent analytic tail is justified on smaller compact disks. The derivative is the locally uniformly convergent reciprocal-difference series, with the finite head restored. This proves F'/F=S off the zeros without assuming that F itself has a global analytic logarithm.

4. **Product growth.** The majorant sum L(r)=sum log(1+r/|z_n|) is finite. A finite-head/summable-tail argument yields L(r)/r tending to zero. This is stronger and more explicit than merely citing that F has order at most one: order one alone would not suffice.

5. **Derivative growth.** Cauchy's formula on unit circles gives M_(F')(r) at most M_F(r+1). The required sublinear upper bound for its logarithm follows. F' cannot vanish identically because F is not constant. No unproved derivative-type preservation theorem is needed.

6. **Finite-zero lemma.** All finitely many zeros of a nonzero entire G have finite multiplicity. Dividing by the polynomial with those multiplicities leaves an entire zero-free H. A lower bound for the polynomial on large circles, followed by the maximum modulus principle, preserves the sublinear logarithmic upper bound. The zero-free H has an entire logarithm by integration of H'/H on the plane. This is an elementary construction, not an appeal to Hadamard factorization.

7. **One-sided harmonic estimate.** A sublinear upper bound on Re h is sufficient; a bound for |h| is neither asserted nor needed. For u=A-Re h, positivity bounds the modulus of the first Fourier coefficient by its mean. The coefficient is minus R h'(a)/2, giving |h'(a)| at most 2(A-Re h(a))/R. The shifted disk is contained in the origin-centered disk of radius R+|a|. Letting R tend to infinity proves h'(a)=0 at each fixed center. The argument applies to an empty zero set as well, by taking the dividing polynomial equal to one.

8. **Infinitely many distinct derivative zeros.** If the nonzero entire F' had finitely many distinct zeros, the lemma would make it a polynomial. A polynomial antiderivative would then make F a polynomial, contradicting the established infinite zero set. This is a statement about distinct zeros, not merely a count involving multiplicities.

9. **Separation from poles.** At each charge location, F' is nonzero because the zero of F is simple. Every zero obtained for F' therefore lies in the domain where S=F'/F and is a genuine zero of S. No cancellation with denominator zeros is possible.

10. **Physical interpretation.** The convergent potential is the normalized sum of log|1-z/z_n|. Under the standard identification of vectors with complex numbers, its gradient is the complex conjugate of S. Both conventions have the same zero set. The candidate already notes normalization and conjugation; these are valid clarifications, not proof defects.

## Boundary and failure checks

- Replacing the infinite sequence by a single charge would allow a zero-free field. Infinitude is used in the contradiction with polynomiality.
- Weakening the finite-zero lemma from sublinear logarithmic growth to a linear upper bound would be false: exp(z) is a nonconstant zero-free entire function with log M(r)=r. The proof explicitly establishes the stronger bound it needs.
- Repeated locations would introduce multiple zeros of the product and common zeros with its derivative. The final separation argument would then require additional reasoning. Distinctness is present in the original question and retained throughout.
- A conditionally convergent or regularized reciprocal-difference series is not substituted for the absolutely normally convergent series in the question.
- The function with an entire logarithm is H after its finite zeros have been divided out, not F or G before this operation.
- The normalized potential is defined by its own convergent series. The proof does not subtract two divergent total potentials.
- The acceptance concerns the planar unit-charge problem only. It does not classify the current status of arbitrary positive charges or higher-dimensional analogues.

## Source and integrity checks

The two source PDFs were read and independently rendered. The primary paper's first two physical pages establish its bibliographic identity, convergence hypothesis, normalized potential, and exact unit-charge conclusion. Hayman and Lingham physical pages 186-187 establish the original hypotheses and the recorded resolution. Visual inspection was used to avoid depending on OCR for the formulae and page locations.

Both PDFs were independently retrieved from the public URLs in `SOURCE_PINS.json` and compared by byte count and SHA-256 with the reference versions. All five input identity checks, all four authored-artifact checks, and all 20 sealed-artifact checks passed. The existing integrity validator was rerun under normal Python, `-O`, and `-OO`; in every mode it accepted the unchanged inputs and rejected both a same-size one-byte mutation and a truncated copy. These are aggregate file-integrity results, not automated verification of the theorem.

The full proof is mathematical prose. There was no execution of source-author code and no formal verification claim.

## Disposition

The reviewed argument needs no mathematical patch. Its exact-target negative answer and stronger infinite-zero conclusion are accepted. Any downstream status description should explicitly say that the problem was already resolved by Clunie, Eremenko and Rossi in 1993 and recorded as resolved in Hayman and Lingham's 2018 update. A label implying a novel resolution would be inaccurate.
