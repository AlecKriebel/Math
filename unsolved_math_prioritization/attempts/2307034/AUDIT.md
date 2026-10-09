# Independent audit of Hall coefficient sign partial results

## Verdict

**ACCEPT AS PARTIAL RESULTS.** Every stated theorem and both proposed-bound counterexamples in the frozen report are correct. The rational-exponent bound is also correct. No mathematical correction is required to these results. The report does not solve the full arbitrary-complex-parameter problem for arbitrary positive real exponents, and must retain that limitation.

The original audit verdict applies to the exact 13,273-byte original proof report with SHA-256:

`fa99237c49ed63a529c8b5f30ebdb6e62cf516b648e2a5a3aa8b9983cdbed71e`

Audit date: 2026-10-09 UTC. Target: 2307034 / AMR-022-7034 / Hall Problem 7.34. Scope: the first coefficient-recurrence approach. This is an editorial edition of that independent audit; [ACCEPTANCE.json](ACCEPTANCE.json) separately identifies the original reviewed report and the present proof and audit editions. The original proof hash does not identify the edited proof.

There is one minor correction to explanatory wording in Section 8: a small positive parameter always creates a positive real pole of the logarithmic derivative, but creates a branch singularity of the function only when the merged exponent is nonintegral. This does not affect the stated obstruction to a nonnegative-coefficient denominator multiple or any accepted theorem.

## Acceptance boundaries

The following claims pass independently:

1. For all real parameters, some nonconstant coefficient is nonpositive by index `ceil(B)+n`.
2. The same bound holds when every nonreal parameter has nonpositive real part, while arbitrary positive real parameters remain allowed.
3. The same bound holds for all admissible complex configurations with one or two parameters.
4. For the exponent tuple `(3/5,3/5)`, the least universal bound is exactly 4, including the full complex-parameter class.
5. If all exponents have a common positive integer denominator q, the uniform bound `qB+1` holds for arbitrary admissible complex parameters.
6. The bound `1+sum ceil(beta_j)` fails, as certified by the two-negative-real-parameter example.
7. The bound `ceil(B)+n` fails in the full complex class, as certified by the four-parameter example with its first nonpositive coefficient at index 14, whereas the proposed bound is 13.

The audit does not certify a sharp general bound, a bound for arbitrary irrational exponents in the unrestricted complex class, or exhaustive novelty/current literature status. In particular, the complex counterexample disproves the proposed value 13 for its exponent tuple; it does not establish 14 as the optimal universal bound for that tuple. Its established universal range remains 14 through 85.

## Source and target fidelity

The [versioned arXiv record](https://arxiv.org/abs/1809.07200v2) was freshly opened; it confirms Hayman and Lingham, the stated title, and revision on 21 September 2018. The preserved [versioned PDF](https://arxiv.org/pdf/1809.07200v2) was checked by text extraction and visual inspection at printed page 170, PDF page 171.

The main question permits positive real exponents and complex parameters, assumes real Taylor coefficients, and requests an exponent-only uniform bound guaranteeing a nonpositive coefficient. It does not impose distinctness or exclude zero parameters. The source's update reports no progress at the time of that manuscript; this says nothing definitive about later literature.

The ledger's identification of the explanatory integer/noninteger index error and the missing variable in the multiplier is confirmed by the rendered source. The submitted results use the coherent main question and do not manufacture a counterexample from those defects.

The preserved public PDF hash and byte count match the ledger:

- PDF: 1,706,228 bytes; SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.

This audit did not independently repeat the earlier broad literature/history screen. Its results establish the mathematics of this report, not the absence of earlier work or a current global open-status certificate.

## Positive polynomial factor lemma

The ODE and coefficient inequality in Section 2 are valid for arbitrary positive real exponents, sparse polynomials, and repeated polynomial factors.

Write a coefficient contribution of `Q=product P_l` using exponents `(e_1,...,e_s)` and nonnegative weight `w=product [z^(e_l)]P_l`. If `sum e_l=i`, the same choice contributes

`w * sum_l gamma_l e_l`

to the coefficient of degree `i-1` of R. Since each `e_l<=d_l`, its weight is between zero and `T w`, with `T=sum gamma_l d_l`. Summing gives `0<=r_(i-1)<=T q_i`, including the case `q_i=0`. Neither division by a possibly zero q_i nor strict positivity of every coefficient of Q is needed.

From `QF'=RF`, the degree `K-1` equation is exactly

`0=K c_K + sum_(i=1)^d ((K-i)q_i-r_(i-1)) c_(K-i)`.

For `K=ceil(T)+d`, every multiplier in the sum is nonnegative. Moreover, `K-d=ceil(T)>=1`, because the lemma is applied to at least one nonconstant polynomial with positive exponent. All coefficients used under the contradiction hypothesis therefore lie in the asserted positive prefix. The term `K c_K` is strictly positive, and no constant-term exception or off-by-one error occurs. The conclusion is that at least one coefficient is **nonpositive**; the lemma does not promise a negative coefficient.

The empty retained product is not an application of this lemma. It equals 1 and is disposed of directly in the cancellation argument. The original number of factors n is understood to be positive, as in the source's exponent tuple.

## Positive real parameter cancellation

For `t>0` and `beta>0`, the coefficients of `(1-tz)^(-beta)` are nonnegative, with constant coefficient 1. This follows from the rising-factorial binomial coefficients. A finite product H preserves those properties.

If `a_1,...,a_K>0`, the coefficient of degree k of `fH`, for `1<=k<=K`, is `a_k` plus nonnegative terms involving only `a_0,...,a_(k-1)`. Thus it remains strictly positive. No assumption about coefficients beyond K is being made. Cancellation is a local analytic identity at zero and does not require H to converge on the entire disk of f.

After cancellation and deletion of zero parameters, a real-parameter configuration has only factors `(1+t_j z)^(beta_j)` with `t_j>0`. The lemma applies with degrees 1. The retained exponent sum and retained factor count are at most B and n, respectively, so the resulting bound is at most `ceil(B)+n`. If all parameters were positive or zero, the remaining product is 1, which contradicts the positive-prefix hypothesis already at degree 1.

Repeated parameters cause no difficulty in this part: treating them separately is allowed by the lemma, and merging them would only improve the degree count.

## Reality, merging, and the half plane theorem

Because `f(0)=1`, its logarithmic derivative is analytic near zero. Real Taylor coefficients of f imply real Taylor coefficients of `f'/f`, hence reflection symmetry of its rational continuation.

Equal nonzero parameters must first be merged. For a distinct parameter lambda, the aggregated exponent `gamma(lambda)` is the sum of positive original exponents at lambda. In partial fractions, the corresponding term is

`gamma(lambda)/(z-1/lambda)`.

Its residue is positive and nonzero. Distinct parameters give distinct poles, so these terms cannot cancel, including when a merged exponent happens to be an integer. The latter case is a zero of f rather than a branch point, but it is still a pole of `f'/f`. Uniqueness of partial fractions then forces conjugate pole pairs with equal residues. Equivalently, lambda and its conjugate have equal **aggregated** exponents. There is no unjustified demand that the individual labeled exponents pair one by one.

A negative real merged parameter gives a degree-one polynomial with nonnegative coefficients. A nonreal conjugate pair gives

`1-2 Re(lambda) z+|lambda|^2 z^2`.

Its coefficients are nonnegative precisely in the asserted closed left half plane. When the real part is zero, the missing linear term is allowed by the sparse-polynomial version of the lemma. The weighted degree contribution of the pair is `2 gamma(lambda)`, exactly the sum of its original exponents after merging; its ordinary degree contribution is 2. Removing zero parameters and positive real parameters leaves `T<=B` and `d<=n`.

Normalized branch identities hold near zero by equality of logarithmic derivatives and of constant values. No global branch convention is needed. If no parameter remains, the same empty-product argument from the preceding section applies. The theorem therefore includes all advertised boundary, repetition, aggregation, and zero-parameter cases.

## Exhaustion for one and two parameters

For one parameter, `a_1=-beta_1 zeta_1` is real only when zeta_1 is real, since beta_1 is strictly positive.

For two parameters, the merged-pole alternatives are exhaustive:

- Both nonzero parameters are real, with zero entries allowed separately.
- A single distinct nonzero parameter remains after merging or deletion of zeros. Reflection forces that parameter to be real.
- There are two distinct nonreal parameters. They must be conjugates, and because each then has one original label, their original exponents must be equal.

In the last case, `a_1=-2 beta Re(zeta_1)`. A nonnegative real part gives `a_1<=0`, including equality on the imaginary axis. A negative real part is covered by the half plane theorem. Thus no admissible two-parameter configuration escapes the claimed bound.

## Independent finite arithmetic

The independent calculation directly expands each of the four individual linear factors using generalized binomial coefficients represented as pairs of rational numbers, then convolves the four series. This verifies the original complex-parameter specification rather than assuming the supplied quartic coefficients.

Independent multiplication of the four degree-one polynomials obtains

`P=(1,1/2,-559/20000,3483/80000,61263981/1600000000)`

in ascending coefficient order. Thus the stated parameters, quadratics, and quartic agree exactly. A second calculation uses the ODE recurrence. For `f=P^alpha`, the coefficient equation is

`k a_k=sum_(i=1)^4 (((alpha+1)i-k) p_i a_(k-i))`.

Putting `alpha=21/10` gives the submitted factor `31/10`; the sign and index shift are correct. All 14 fractions in the report agree exactly with the independent calculation. Imaginary parts in the direct four-factor calculation vanish exactly.

The complete independently reconstructed table is:

| k | Exact a_k |
|---|---|
| 1 | 21/20 |
| 2 | 46011/200000 |
| 3 | 63959/1000000 |
| 4 | 2604972279/20000000000 |
| 5 | 17176057899/400000000000 |
| 6 | 1716180224143/4000000000000000 |
| 7 | 18850467170403/5000000000000000 |
| 8 | 378974338478734383/200000000000000000000 |
| 9 | 267541186415691881/8000000000000000000000 |
| 10 | 416255521145722785681/400000000000000000000000000 |
| 11 | 45257562655633678288701/8000000000000000000000000000 |
| 12 | 1130659439881192077002447/160000000000000000000000000000000 |
| 13 | 25669021687283962042020147/3200000000000000000000000000000000 |
| 14 | -2888094401257003768564291271949/32000000000000000000000000000000000000 |

The first thirteen numerators and all denominators are positive; the fourteenth numerator is negative. Here `B=4*(21/10)=42/5`, so `ceil(B)+n=9+4=13`. The example therefore refutes exactly the claimed unrestricted bound. The right half plane pair makes clear why it lies outside the accepted half plane theorem.

The independent direct-factor calculation also yields, for `(beta_1,beta_2)=(3/5,3/5)` and `(zeta_1,zeta_2)=(-1,-2/5)`,

`a_1=21/25, a_2=3/625, a_3=301/15625, a_4=-6471/390625`.

Hence a universal bound of 3 fails. The proved two-parameter upper bound is 4, establishing exact sharpness for this exponent tuple over the entire admissible complex class.

No floating-point comparison is used in this audit's sign or fraction tests. The exact rational calculations and this independent reconstruction suffice for the certificates.

## Rational and integral exponent bounds

If q is a positive integer with all `q beta_j` positive integers, the local identity `f^q=product (1-zeta_j z)^(q beta_j)` makes `f^q` a polynomial of degree at most the integer `D=qB`. Zero parameters and cancellations may reduce that degree, which only strengthens the argument.

Assuming `a_1,...,a_(D+1)>0`, every contribution to the degree `D+1` coefficient of the ordinary integer power `f^q` is nonnegative: all its coefficient indices lie between 0 and D+1. The q contributions using `a_(D+1)` and q-1 constant terms already have positive sum `q a_(D+1)`. The polynomial coefficient must instead be zero. This establishes the uniform bound `D+1` without a root-location assumption.

When all exponents are integral, q=1 gives `B+1`; taking every parameter equal to -1 yields `(1+z)^B`, positive through degree B and zero at B+1. Thus the integer benchmark is sharp and illustrates why the source's conclusion cannot be silently strengthened to strict negativity.

## Compactness discussion and degree drop

The pointwise assertion about all nonnegative coefficients is correct. After merging equal nonzero parameters, any nonintegral merged exponent produces a genuine finite branch point, because every other distinct factor is analytic and nonzero there. A nonpolynomial member therefore has a finite radius of convergence. Pringsheim's theorem places a singularity at its positive radius R. Along the positive real interval approaching R, the positive exponent at that point forces the modulus of the product to tend to zero; all other factors remain bounded. This contradicts `f(t)>=1` from its nonnegative coefficients and constant coefficient 1.

Integer aggregated exponents can instead produce a polynomial, even when the original individual exponents were nonintegral. Zero parameters remove factors entirely. Consequently, compactness of normalized parameter tuples can produce a nonnegative-coefficient polynomial limit, and that pointwise assertion supplies no contradiction at such a limit. Strict positivity is not a closed condition, so positive prefixes in a sequence can converge to zero coefficients beyond the limiting degree.

The nonzero-parameter neighborhood observation is compatible with the usual positive-polynomial multiplier argument: a fixed real denominator of positive constant term, positive leading coefficient, and no nonnegative real root is strictly positive on the nonnegative real axis, and its homogenization has the endpoint positivity needed by that argument. A symmetrized denominator preserves reality even when individual labels are not conjugate-paired. Fixed nonzero parameters keep its degree and leading coefficient from dropping.

That observation does not prove uniformity at a zero-parameter limit. A nearby small positive real parameter epsilon creates a denominator zero at `1/epsilon`. A nonzero polynomial with nonnegative coefficients cannot vanish at a positive real number, so that denominator has no nonzero polynomial multiple with nonnegative coefficients. This is already a decisive obstruction to the stated naive multiplier-continuity step; it is not an obstruction to every possible proof of Hall's requested bound.

The report appropriately leaves degree-drop and merger uniformity unresolved. Neither the accepted partial theorem nor the rational-exponent result depends on this unfinished compactness discussion.

## Corrections and status handling

One explanatory sentence in the original proof requires the following refinement, without changing any theorem; this edition applies it:

- The original Section 8 describes every nearby small positive real parameter as introducing a distant positive real singularity.
- Precise replacement: “This introduces a distant positive real zero of the denominator, hence a pole of the logarithmic derivative; it is a branch singularity of f when the corresponding merged exponent is nonintegral.”

This is a minor terminology correction. Positive integral exponents give ordinary zeros of f and still give logarithmic-derivative poles, so the denominator-multiple obstruction remains valid in either case.

For maximum explicitness, Section 4 may repeat the already established empty-retained-product case before applying the lemma. This is optional exposition rather than a proof repair, because the preceding cancellation argument is explicitly incorporated.

The original reviewed proof and this publication edition are distinct objects. The edition incorporates the stated wording refinement and retains every mathematical result and limitation. Its status records the completed independent audit. The original documents remain unchanged.

Final classification: **accepted partial report with one minor explanatory wording correction; unrestricted arbitrary-positive-real-exponent complex problem remains unresolved by this approach.**
