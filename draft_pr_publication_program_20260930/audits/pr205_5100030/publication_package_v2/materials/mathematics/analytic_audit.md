# PR205 adversarial analytic audit

The submitted written proof is mathematically sound for the stated proper-confocal, odd least-period setting. I found no missing central lemma, sign error, invalid division, winding restriction, or repetition counterexample. The original computational harness needs repair before publication: bare asserts disappear under optimized Python, and the candidate checker's running maximum can mask a NaN formula value even in ordinary Python. These findings concern verification reliability; they do not refute the proof.

This family is an adversarial audit after submitted-proof exposure. Root explicitly corrected the initial independence premise because the full inherited history included the candidate proof. I recorded that correction before opening the local proof. I then read the exact 9,132-byte candidate at submitted HEAD e8d7e925d19698edcb75822e40ca5ac820eb4388 (SHA256 09bfb91289e683809e71a668e020c1d37f8f99f717e3658d1cc80268fe55f147). I do not claim an independent discovery or a pre-proof derivation. The preliminary elementary focal-tangent calculation is recorded as an audit calculation, not as evidence of independence.

## Precise target and primary inputs

For a>b>0, fix a proper nested confocal elliptic caustic alpha>beta>0, with c^2=a^2-b^2=alpha^2-beta^2. The quantities are ordinary nonnegative Euclidean perpendicular distances from F+=(c,0) and F-=(-c,0) to the complete original side lines. They are not vertex, contact-point, outer-polygon, antipedal, or segment distances. The theorem concerns odd physical least period N, including all admissible coprime winding classes, and separately permits repeated odd index lists with the correct scaling.

The [published source, Table 7 p.349 and §3.7](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf) matches this exact product of sums, code k601. Its historical question mark is not a current novelty certificate. The [Stachel preprint, Theorem 2 pp.11–12](https://arxiv.org/pdf/2105.03624) gives precisely the canonical parametrization and axes used here. This family checked that available full text; it did not independently verify the published theorem numbering. The candidate's standard special-function inputs match [DLMF §22.8](https://dlmf.nist.gov/22.8) and [§22.16](https://dlmf.nist.gov/22.16).

There is an unused source typo: Stachel's preprint p.10 prints an alternating sign for dn(u+2jK). The correct real period of dn is 2K. The candidate does not use this typo; its quarter-period identities are correct. This is a source caution, not a mathematical finding against the candidate.

## Universal analytic argument audited

Put k=c/alpha, m=k^2, k'=beta/alpha, and K=K(k). Thus 0<k<1 and k'>0. In the canonical parametrization, h=2*tau*K/N, gcd(tau,N)=1 and 0<tau<N/2. Consequently 0<h<K, so cn(h)>0. The axes a=alpha*dn(h)/cn(h), b=beta/cn(h) are positive and properly contain the caustic. Indeed a^2-alpha^2=alpha^2*(1-m)*sn(h)^2/cn(h)^2>0, b^2-beta^2=beta^2*sn(h)^2/cn(h)^2>0, and a^2-b^2=c^2. No analytic continuation or complex pole assumption is needed.

For y=x+a0, put S=sn(x)sn(y), Dxy=dn(x)dn(y), Cxy=cn(x)cn(y). The difference-addition laws give the linear system

    Dxy + m*S*Cxy = dn(a0)*(1-m*S^2),
    Cxy + S*Dxy   = cn(a0)*(1-m*S^2).

The determinant 1-m*S^2 is at least 1-m>0 for real arguments. Solving gives

    Dxy=dn(a0)-m*cn(a0)*S,
    Cxy=cn(a0)-dn(a0)*S.

I re-inverted the system rather than accepting the quoted identities. All signs are correct. Therefore the difference Dxy-m*Cxy is

    dn(a0)-m*cn(a0) + m*(dn(a0)-cn(a0))*S.

For the grid t_i=t+4Ki/N and a_r=4Kr/N, r=1,...,N-1, oddness implies sn(a_r) is nonzero: a real zero would require 2r=N*j, impossible for an interior r when N is odd. The zeta addition formula gives

    sum_i sn(t_i)sn(t_i+a_r) = N*Z(a_r)/(m*sn(a_r)).

The cancellation is legitimate because shifting by a_r permutes the grid modulo 4K and Z has real period 2K. No boundedness assertion or formal cancellation of divergent terms is being made; every term is finite on the real axis. Each nonzero-shift cyclic correlation of dn*dn-m*cn*cn is therefore constant. The diagonal is dn^2-m*cn^2=1-m. Every ordered pair (i,j) belongs to exactly one difference class r=j-i modulo N, including the diagonal, so expansion proves that

    (sum_i dn(t_i))^2 - m*(sum_i cn(t_i))^2

is constant. There is no missing factor of two: the grouping uses all ordered pairs.

## Geometric bridge audited

For the midpoint parameter v_i=u+(2i+1)h, the caustic tangent is

    -(sn(v_i)/alpha)X + (cn(v_i)/beta)Y = 1.

Substituting either canonical endpoint at v_i-h or v_i+h reduces exactly to the second difference identity above with shift h. Thus this is the physical chord line; the contact phase is checked and is not simply assumed.

The normal norm is dn(v_i)/beta. It is strictly positive and at least k'/beta=1/alpha. Evaluation at each focus yields

    q_plus  = beta*(1+k*sn(v_i))/dn(v_i),
    q_minus = beta*(1-k*sn(v_i))/dn(v_i).

Both numerators are at least 1-k>0. Hence removing the ordinary-distance absolute value at this step is justified by an explicit sign bound. The per-side identity q_plus*q_minus=beta^2 follows, but was not used as a substitute for the needed product of sums.

Coprimality of tau and N implies that the sample set with step 4*tau*K/N is exactly the uniform 4K/N grid. This includes all admissible stars. Reversal permutes the same complete side lines and cannot change either sum.

Define A(v)=sum 1/dn(v+4Ki/N) and B(v)=sum sn(v+4Ki/N)/dn(v+4Ki/N). With t=v+K, the correct quarter-period identities give A=D(t)/k' and B=-C(t)/k'. Therefore

    (sum q_plus)(sum q_minus)
       = beta^2*(A^2-m*B^2)
       = alpha^2*(D^2-m*C^2).

The negative sign in the B bridge is correct, even though it disappears in the final square. Setting v=0 pairs the odd function sn/dn under negation and gives the claimed positive finite constant

    beta^2 * [sum_i 1/dn(4Ki/N)]^2.

The proof handles every odd N algebraically, rather than extrapolating from samples.

## Boundary and falsification checks

An odd repeated indexing length reduces to an odd physical least period: its repetition count is odd, each distance sum is multiplied by that count, and the product scales by its square. No new primitive theorem follows from repeated lists.

The circular limit k=0 is excluded from the zeta division and is treated directly: the coincident foci lie at the center and every complete side has distance beta, giving N^2*beta^2. The beta=0 caustic degeneration, grazing limit, hyperbolic caustics and nonperiodic trajectories are outside the theorem. No uniform numerical error bound near beta=0 is inferred.

Evenness cannot silently be added. For k=0.7, N=4, the analogous dn/cn expression is approximately 11.75314274283428 at t=0 and 11.50713783569825 at t=K/3, a difference about 0.2460049071360314. The same canonical construction yields the corresponding proper even-period geometry.

## Reproduction and harness findings

EXECUTION_RECEIPT.json binds ten actual executions and raw stdout/stderr files. Both original ordinary runs reproduce their submitted counts: the candidate reports 10 named exact check groups and 126 numerical orbit cases; the old independent checker reports 3,609 exact assertions and 8,938 numerical diagnostics across 45 geometry families. These counts describe the source loops, not thousands of independent mathematical theorems.

Known-false exact-identity controls add 1 to one equality in each original checker without changing the original files. Ordinary mode fails with AssertionError. Optimized mode incorrectly reports PASS, because Python removes every bare assert. Merely reproducing an original PASS under -O is consequently not verification.

NAN_METRIC_CONTROL_RECEIPT.json separately records a nonfinite control: the candidate's tested focal formula is replaced by NaN in an owned derivative. It incorrectly reports PASS even in ordinary mode because max(previous_finite_error,NaN) retains the previous error. The original archive remains untouched.

The new audit_checker.py contains no assert statements. It uses explicit exceptions, strict real scalar/period checks and finite guards before every metric update. Actual ordinary and optimized executions both pass 11 exact algebra/ordered-pair checks, 100 analytic phase cases and 260 physical orbit instances, comprising 22,000 scalar diagnostics at 90 decimal digits. The sample uses k in {0.001,0.2,0.7,0.97,0.999999}, N in {3,5,7,9,15}, every admissible coprime winding for these N, and four positive/negative phases. Its worst normalized residual is about 5.04e-86. Physical tests compute the focus-to-chord distances from endpoint coordinates, check contact incidence, caustic tangency, outer incidence and specular reflection, and compare with the explicit invariant. They use normalized alpha=1; extension to other positive alpha is exact geometric homogeneity.

Both modes reject fourteen genuine controls: NaN/infinity/complex metrics, bool/even periods, zero/unit/NaN modulus, nonprimitive and impossible windings, a wrong difference sign, a wrong quarter-period sign, a signed-distance substitution, and a corrupted lemma coefficient. The finite sweep is noninterval diagnostic evidence and does not prove the universal theorem. Its value is in detecting implementation/sign/scope failures separately from the audited universal argument.

## Disposition and remaining gap

Mathematics: PASS, with no unresolved proof gap under the stated assumptions and credited canonical input. Source-to-target fit: PASS. Original harness: REPAIR REQUIRED or preserve as explicitly historical, superseded by a fail-closed implementation. The supplied replacement audit demonstrates the necessary behavior in both Python modes; Root must decide how to integrate a portable, repaired verification package.

This family does not establish current novelty, priority, independent discovery, human peer review, or publication readiness. A separate positive priority audit and the program's fresh whole-package adversarial reviews remain necessary.
