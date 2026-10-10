# Independent mathematical audit: the variable-base parity counterexample

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the variable-base counterexample, with no external human peer review, journal acceptance, or formal proof-assistant certification claimed. The complete substantive mathematical proof and audit are retained. No mathematical correction was required. The fixed-base-2 irrational-ratio question remains unresolved by this work. The exact quartic family and positive-multiplier mechanism are prior work of Dubickas (2006); no novelty of the application is claimed. Executable programs, raw datasets, detailed execution receipts, full computational certificates, and copied source documents are omitted. This is not an executable reproduction package. Edition preparation performed byte-integrity and publication-structure checks, with no new mathematical test execution or scholarly-source retrieval or inspection.

## Verdict

**ACCEPTED, with exactly the stated variable-base scope. No mathematical correction is required.**

Let P(X)=X^4-X^3-X^2-X-1, let gamma be its positive root, and put

    c = 1/((gamma-1)P'(gamma)),
    alpha = 2c gamma^20,
    beta = gamma alpha.

These are admissible positive parameters with 1<gamma<2 and irrational alpha/beta. Every term in the two interleaved floor sequences is even, including both exponent-zero terms. Consequently every positive odd integer is absent from their finite subset sums. This disproves universal completeness for the variable-base extension. It does not resolve the fixed-base-2 question or classify every gamma in (1,2).

The original accepted proof, before the editorial changes documented in this edition, has SHA-256

    610ab47424d8d49c2d6aada416084fc2e3f55fc95e3a757f9e980c1e8fe6f0a8

and 8,897 bytes. Its candidate inventory has SHA-256

    cd452acb50ad0ea8c1e59acb079131605c2cc74e98c2a942944bb4a2bd9e6319.

Historically, all 35 candidate inventory members were independently checked by byte count and hash. No unlisted file was present at authentication. The original audit applies to those exact bytes. This prose-only edition retains its complete substantive mathematical reasoning; ACCEPTANCE.md and ACCEPTANCE.json bind the edition proof and audit separately.

## 1. Original formulation and admissibility

The original question was read from the complete Graham 1971 PDF, printed page 36, question 12, and independently from the complete Erdős–Graham 1980 PDF, printed page 58. Their displayed sequence starts with floor(alpha), floor(beta), then doubles each multiplier; the follow-on question substitutes a real gamma in (1,2). The hypotheses on the multipliers are positivity and an irrational ratio. Neither question adds multiplicative independence, disjointness of the two streams, or a restriction excluding beta=gamma alpha. These source questions are invitations to investigate, rather than separately asserted theorems. The result here refutes the universal affirmative answer to their variable-base extension. [Graham 1971](https://mathweb.ucsd.edu/~ronspubs/71_08_integer_sums.pdf), [Erdős–Graham 1980](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf).

The sumset definition in Graham, printed page 24, uses a separate zero-or-one coefficient for each sequence position and finite support. The book gives the same definition on printed page 53 and defines completeness on printed page 54. Thus sufficiently large integers, rather than all positive integers starting at one, are the required target, and equal values at different positions remain available separately. [Graham 1971](https://mathweb.ucsd.edu/~ronspubs/71_08_integer_sums.pdf), [Erdős–Graham 1980](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf).

The present obstruction is insensitive to multiplicities: a finite sum of even integers is even even if repetitions are retained or additional repetitions are permitted. Coincident terms therefore cannot repair this counterexample. Irrational gamma makes alpha/beta=1/gamma irrational. In contrast, a one-step shift at gamma=2 gives ratio 1/2 and is inadmissible under the fixed-base question. No condition may be silently imported from the fixed-base case to exclude the present admissible example.

## 2. Root and coefficient audit

Every rational endpoint evaluation in the proof was independently recomputed. They imply

    48/25 < gamma < 193/100,
    77/100 < u < 39/50,

where -u is the unique negative root. There is one positive root by Descartes' rule together with the sign change. The derivative decomposition

    d(P(-t))/dt = 4t^3 + 3(t-1/3)^2 + 2/3

is exact and positive for t>=0. It gives exactly one negative root and proves that root is simple. The positive root is simple because Descartes' bound counts multiplicity. The remaining roots are a distinct nonreal conjugate pair: extra real roots have already been excluded, and a repeated nonreal root would force its conjugate to repeat as well, exceeding degree four.

Writing z=x+iy with y>0, Vieta gives

    x=(1-gamma+u)/2,
    |z|^2=1/(gamma u).

The asserted rational enclosures check exactly:

    -2/25 < x < -7/100,
    5000/7527 < |z|^2 < 2500/3696 < 25/36,
    y^2 > 5000/7527-4/625 > 16/25.

In particular every root other than gamma has modulus less than 5/6, and y>4/5. The rational-root theorem excludes rational gamma since P is monic and gamma lies strictly between 1 and 2. The product formula P'(gamma)=(gamma+u)|gamma-z|^2 is positive, so c is positive.

For a root r define c_r=1/((r-1)P'(r)). The product formula for P' gives

    |(-u-1)P'(-u)|=(1+u)(gamma+u)|-u-z|^2 > 32/25,

and

    |(z-1)P'(z)|
      =|z-1||z-gamma||z+u||z-conjugate(z)| > 32/25.

The first two factors in the second inequality exceed 1 because x<0 and gamma>1; the remaining two exceed y and 2y. The conjugate case is identical. Thus each nonleading |c_r|<1 is justified with strict margins. No numerical root solver or floating-point inequality is needed.

Irreducibility is not needed for the proof's sum over all four roots. Nevertheless, it also holds: modulo 2 the quartic has no linear factor and is not divisible by the only irreducible quadratic X^2+X+1; the remainder is X+1 modulo 2. This independently confirms that all four roots are algebraic conjugates and that P is the relevant minimal polynomial for the cited Pisot results.

## 3. Trace sign, residue, and all-future induction

For m=0,1,2,3, evaluating the partial-fraction identity at X=1 gives

    sum_r r^m/(P'(r)(1-r)) = 1/P(1) = -1/3.

Changing the denominator from 1-r to r-1 reverses the sign. Therefore S_m=sum_r c_r r^m equals +1/3 initially, exactly as claimed. This sign is essential.

Every root obeys the same homogeneous quartic recurrence, so S_m does too. If S_m=k_m+1/3, the sum of the preceding four residues is 4/3, producing precisely the +1 in

    k_(m+4)=k_(m+3)+k_(m+2)+k_(m+1)+k_m+1.

With four initial zeros, k_m is a nonnegative integer for every m>=0. This is an induction for all indices, not an extrapolation from a finite list.

As a separate algebraic certificate, the auditor computed

    c = (80gamma^3+48gamma^2-341gamma+50)/1689.

It follows from the exact polynomial identity

    (80X^3+48X^2-341X+50)(X-1)P'(X)-1689
      = (320X^3-48X^2-1348X+1639)P(X).

The power traces for exponents 0 through 6 are 4,1,3,7,15,26,51. Applying the displayed cubic representative to each of the first four shifted traces gives 563/1689=1/3. This provides a second exact route to the four initial trace values, independent of the partial-fraction computation.

## 4. Uniform shift and floor endpoints

Complex-conjugate terms combine to a real number, so

    E_m=sum_(r != gamma) c_r r^m

is real. The audited coefficient and root bounds give

    |E_m| < 3(5/6)^m.

The integer comparison 18*5^20<6^20 proves that this is less than 1/6 for every m>=20. Since c gamma^m=k_m+1/3-E_m,

    1/6 < c gamma^m-k_m < 1/2,
    2k_m+1/3 < 2c gamma^m < 2k_m+1.

Both floor endpoints are safely strict; in particular the upper endpoint cannot be attained. Therefore floor(2c gamma^m)=2k_m for every m>=20. Alpha uses m=20+n and beta uses m=21+n for every n>=0. The exponent-zero prefix is covered, and there is no unproved passage from eventual parity to parity at all original positions.

The shift is substantive. The independent verifier confirms floor(2c gamma^3)=1, so a version that omitted a justified shift would fail. No assertion that 20 is the optimal shift is needed or made.

## 5. Independent computations and failure controls

The original auditor authored an independent verifier before inspecting the candidate verifier. It did not import or execute candidate code, third-party programs, or a numerical algebra package. Only Python standard-library rational and integer arithmetic was used. Programs, detailed receipts, and full computational certificates are omitted here. The following describes historical independent verification, not a new execution or executable reproduction from this edition.

Its independent computational route is:

1. Derive the inverse of (X-1)P'(X) in Q[X]/(P) by polynomial Euclid.
2. Compute traces as traces of multiplication maps in this four-dimensional algebra.
3. Check the trace residue against the integer recurrence for m=0 through 1023.
4. Isolate gamma by 640 rational bisections.
5. Reduce 2cX^m modulo P and enclose the resulting cubic by rational interval Horner evaluation. This differs from the candidate's direct power-and-denominator enclosure.
6. Isolate 512 consecutive floors, m=20 through 531, and check all claimed rational inequalities.

Historically, all 1,573 checks passed. Normal, -O, and -OO runs yielded byte-identical JSON. The verification uses explicit exceptions, not removable assert statements. Failure controls reject zero trace residue, a doubled multiplier, and the inadequate shift-3 bound; the unshifted m=3 floor is independently isolated as the odd integer 1. The reported decimal orientation values and first seven floors also agree with independently derived enclosures.

These finite computations test implementation and transcription. The all-future proof remains the root bounds, trace induction, and strict error estimate above. No finite sample is treated as a proof of universal parity.

## 6. Attribution and novelty boundary

Dubickas's 2006 Archivum Mathematicum paper, Theorem 4 and its proof, supplies the positive multiplier 1/((gamma-1)P'(gamma)) and the limiting residue 1/|P(1)| for the relevant Pisot case. The printed pages are 154 and 156; the PDF includes a library cover. The explicit coefficient and partial-fraction mechanism are prior published mathematics. [Dubickas, limit points paper](https://dml.cz/handle/10338.dmlcz/107991).

Dubickas's 2006 Glasgow Mathematical Journal paper gives the all-even floor mechanism in Theorem 1(iv). Its printed page 332 explicitly includes the family X^(d-1)-X^(d-2)-...-X-1 for d>=5, containing the exact present quartic at d=5. The printed-page-334 proof invokes the positive Pisot multiplier and a sufficiently large exponent shift. Its bibliography identifies the Archivum paper as reference 10. The final candidate properly acknowledges both the mechanism and this exact family. [Dubickas, parity paper](https://doi.org/10.1017/S0017089506003090).

The contribution accepted here is a correct, explicit, quantitatively checked application to the original variable-base question, with a self-contained proof and a specified shift. This audit makes no priority claim for the consequence, does not certify that the application has never appeared elsewhere, and does not treat a tracker label as authoritative evidence of novelty. The theorem is valid regardless of that historical question.

## 7. Publication boundary and residual status

This prose-only edition contains authored proof, mathematical review, acceptance reports, public citations, and source/verification metadata. Executable programs, raw datasets, detailed execution receipts, full computational certificates, source PDFs, source text, screenshots, and private coordination material are excluded. Historical source-inspection claims describe the original candidate and audit; edition preparation performed no new scholarly-source retrieval or inspection.

The residual status is precise:

- Universal completeness for all admissible alpha,beta and all gamma in (1,2): false by this counterexample.
- Completeness at gamma=2 under irrational alpha/beta: unresolved by this work.
- A classification of gamma in (1,2): not supplied.
- Novelty of the application to the named problem: not established.

No proof correction remains outstanding. The exact-family attribution clarification was incorporated before the candidate was sealed and before final acceptance.
