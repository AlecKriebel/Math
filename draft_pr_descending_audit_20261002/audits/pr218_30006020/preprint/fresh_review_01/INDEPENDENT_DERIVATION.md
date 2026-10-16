# Independent reconstruction of the submitted theorem

This derivation was made from the frozen manuscript and the actual controlling primary statements/proofs, before reading the archived final priority recommendation. It checks the finite-vector interpretation identified in issue M1; it is not a claim to reprove the imported intersection-number theorems.

## Finite conditioning and the exact prior law

For fixed n the correct independent representation uses Z_1,...,Z_n with Z_j Poisson(a_j), a_j=zeta(2j)/(2j). Its conditioning event is S_n=sum_{j=1}^n j Z_j=n and has positive probability exp(-sum_{j=1}^n a_j)h_n. Therefore

P((C_1,...,C_n)=c)=1{sum j c_j=n}h_n^{-1} product a_j^{c_j}/c_j!.

An ordered composition with counts c has k!/product c_j! orderings; its probability product a_j/(h_n k!) gives exactly this count vector. DGZZ's theta_j=zeta(2j)/2 and cycle weighting give the identical law, as is visible in its definitions (1.7)–(1.8) and complete Lemma3.6 proof. This is old input, not a new model.

By contrast, independent Z_j for all j>=1 have sum_j P(Z_j>0)=infinity, because a_j>=1/(2j) and a_j<=zeta(2)/(2j). Independence and Borel–Cantelli imply infinitely many nonzero Z_j almost surely. Their infinite weighted sum is infinite almost surely. Conditioning that infinite vector on sum_j jZ_j=n is thus not an ordinary positive-probability conditioning. The manuscript should explicitly state the finite-vector representation. This affects one explanatory equivalence, not the primary composition definition or any succeeding formula.

Shifting a finite count vector by r_j selected components gives

E product (C_j)_{r_j}=h_{n-R}/h_n product a_j^{r_j}, R=sum j r_j<=n,

and zero if R>n. This also checks the positive-weight specialization of AT Lemma5/(126): take its exponential weights m_j/j!=a_j and p(n)=n!h_n. No interpretation of m_j as integers is needed for the displayed probability mass and exponent shift.

## Geometric comparison: the source dependence is sufficient

I checked DL1.4 and its exact stable-graph mixture definitions in Section3, Theorem3.2 and proof, Remark2.5's automorphism convention, Section4's actual conditioning proof, and (6.1)–(6.4)/the full Lemma6.4 proof. The one-vertex graph with k loops has 2^k k! automorphisms. A monomial indexed by positive j_i summing to n=3g-3 has positive coefficient A_{g,k} ctilde(j) product x_i^(2j_i-1)/(2j_i)!, with exactly the manuscript's A_{g,k}. Summing all heights produces zeta(2j_i). Integrating the simplex leaves product (2j_i-1)!/(2n-1)!. Dividing by the graph factor leaves a common genus factor times

D_{g,k} ctilde(j) product a_{j_i}/k!, D=A/2^k.

Conditional on the monomial, the normalized areas have Dirichlet parameters (2j_i). This is a positive mixture, so uniform coefficient bounds give uniform measure bounds rather than cancellation estimates.

At k<=floor(.6 log(2n)), g-k~g and the number of marks is logarithmic. DL(6.1) applies uniformly to c_{g-k,k}(j_i-1), and gives sup|ctilde-1|=o(1). Cancelling consecutive factorials independently gives

D_{g,k+1}/D_{g,k}=12(g-k)(3g-3-k)/((6g-5-2k)(6g-6-2k)).

For k=O(log g), this is 1+O((k+1)/g), and its product through the cutoff is 1+O(log(g)^2/g). If alpha=D_{g,k}ctilde/D_{g,1} differs from1 by at most e_g=o(1), the two conditioned latent laws have RN derivative alpha/E_model alpha. It lies between (1-e_g)/(1+e_g) and (1+e_g)/(1-e_g). Thus the RN error is at most 2e_g/(1-e_g). Integrating the common Dirichlet kernel and forgetting labels preserve the bound. This explicitly justifies the strong comparison for all nonnegative integrable f, including moving-window count powers.

I checked DGZZ1.12 and its derivation from the generating function, and DGZZ5.2 including the full proof's (5.7) and low-k regime split (5.8). At t=11/10<8/7, E t^K=O(n^.05). Markov gives P(K>cutoff)=O(n^-eta), eta=.6log(1.1)-.05>1/220. The new rational control gives a stronger elementary lower witness eta>1437/200000>1/220; this uses the alternating logarithm series, not a floating-point sign. The low-k relative multivertex error is O(log(g)^25 g^-1 2^k), and .6log2<1. The cutoff also lies strictly below log(g)/log(9/4). The claimed polynomial exceptional probability follows in a stated valid range. The unrestricted later Corollary5.3 and DL's overstrong printed exponential logarithmic-cutoff tail are unnecessary.

For every fixed r, summing the t^-k Chernoff bound beyond L log n with L sufficiently large gives E K^r=O(log(n)^r). This is true in both the geometric law and the model; for the model use [z^n]H^t/h_n. If delta_g is either polynomially small bad probability,

E[K^r;bad] <= (E K^(2r))^(1/2)delta_g^(1/2)=o(1).

This discharges the unbounded-moment issue that TV alone would not settle. I found no circular dependence on the desired mesoscopic conclusion in these inputs.

## Coefficients and all unmarked rates

The exact zeta expansion gives H(z)=(1-z)^(-1/2)B(z), B(z)=product_{m>=2}(1-z/m^2)^(-1/2). DL Lemma6.7 proves the corresponding analytic extension; the telescoping product at1 gives B(1)=sqrt2. Analyticity on |z|<4 bounds Taylor coefficients by C_R R^-k for every 1<R<4. Convolution with the binomial coefficient sequence gives h_n~sqrt(2/pi)n^-1/2. The same argument with the positive analytic power B^t gives [z^n]H^t~2^(t/2)n^(t/2-1)/Gamma(t/2). There are consequently global positive two-sided bounds by constants times (n+1)^-1/2 and the ratio bound used in the paper. Uniformity h_{n-R}/h_n->1 for R=o(n) follows directly from the asymptotic because n-R~n.

Set q=ns_g. The hypotheses are precisely q->infinity and q=o(n); no stronger rate is smuggled in. On any fixed size window j/q in[a,b], sum a_j tends to half log(b/a), by harmonic sums and exponential decay of zeta(2j)-1. In a fixed factorial moment of selected window components, removed size R is at most rBq=o(n). The coefficient ratio tends uniformly to1, so every joint factorial moment is the independent Poisson limit. Higher fixed moments supply tightness/UI for each lower moment if needed in the moment-method justification. The finite-dimensional Poisson vector is moment determinate. Bounded expected counts on compact sets give point-measure tightness. This proves the unmarked process convergence.

I separately checked ABT's actual CR, ULC definitions and complete Theorem3.1 proof. Let A=zeta(2)/2. Then jE Z_j->1/2 and jP(Z_j=1)=1/2+O(1/j). For ell>=2, jP(Z_j=ell)<=A^ell/(ell!j^(ell-1))<=A^ell/(ell!j). Thus e(j)=C/j and factorially summable constants satisfy ULC. The old theorem gives TV comparison of every initial segment b_n=o(n), including all bounded q-scale windows. The manuscript's prior-probability credit is accurate.

## Gamma tails, total normalization and arbitrarily slow q

Conditional on the components, attach independent Y_i~Gamma(2j_i,rate1). For a compactly supported Lipschitz test f on[a,b], the expected difference between the unnormalized marked and unmarked integrals is bounded by the manuscript's single-component sum, whose expectation factor is a_j h_{n-j}/h_n.

In aq/2<=j<=2bq, both the ratio and the summed harmonic weights are bounded. The individual Lipschitz displacement has expectation at most const sqrt(j)/q, giving O(q^-1/2). Below aq/2 only the marked term can enter support; its upper-tail bound is exp(-aq)2^(2j)<=exp(-a(1-log2)q). The weighted sum loses only log(q+2), not log n. Above2bq, the lower-tail bound is exp(bq)(3/2)^(-2j)<=exp(-cj), c=2log(3/2)-1/2>0. The new rational sign witness log(3/2)>1/3 yields c>1/6. Up to n/2 the coefficient ratio is bounded, and beyond n/2 the extra sqrt n is dominated by exp(-cn/2). Therefore every error tends to zero even for q=logloglog n eventually, or for n/q diverging arbitrarily slowly. There is no union over all O(log n) components imposing an extra rate.

Lipschitz Laplace tests determine the vague point-process law. Given every composition, total T has Gamma(2n,rate1) distribution; hence T/(2n)->1 in probability under the mixture. Joint convergence with this asymptotically constant scalar requires no independence. Positive dilation acts continuously in the vague topology at scalar1, so multiplying locations by2n/T gives exactly normalized areas divided bys_g. No microscopic or macroscopic endpoint follows from this argument.

## Marked moments and geometric transfer

For a marked compact window put p_j=P(Gamma(2j)/(2q) in[a,b]) and w_j=a_jp_j. The same three ranges give sum w_j=O(1). The exact rth marked factorial moment is the sum over j_1+...+j_r<=n of h_{n-sum j_i}/h_n product w_{j_i}, with ordered selected components. Repeated sizes are already handled by falling factorials.

On removed mass<=n/2, the ratio is bounded and the sum is O((sum w_j)^r). Otherwise one selected j_i>=n/(2r). Because q/n->0, that selected Gamma mark must make an exponentially unlikely downward deviation to enter the window. Its probability is <=exp(-c_r n) for large n. The global ratio contributes at most C sqrt n, and all unrestricted size-weight sums contribute at most O(log(n)^r); the remainder vanishes. This bounds every fixed factorial and ordinary moment of marked counts. Finite unions follow by enclosing them in one compact interval if necessary.

On 1/2<=T/(2n)<=2, a normalized count on[a,b] is at most the unnormalized count on[a/2,2b]. The exceptional total-probability is exponentially small, while K<=n. The rth-moment loss is at most n^r exp(-cn). Thus every normalized count has a uniformly bounded higher moment, providing UI for all fixed powers and mixed powers. Weak process convergence gives window count convergence because the limiting PPP has no deterministic endpoint atoms. Hence all claimed fixed joint moments converge in the model.

For the geometric law, the good-event RN comparison multiplies each bounded model moment by1+o(1). The exceptional rth-count moments are bounded by E[K^r;bad]=o(1) in both laws. This transfers the full conclusion without an invalid TV-to-expectation inference.

Finally, at fixed genus the law from the exact mixture has simplex densities whenever K>=2; K=1 is an atom only at normalized area1. Each fixed compact rescaled window shrinks away from1 for sufficiently large g. Therefore its endpoints are continuity sets for the fixed-genus N->infinity law. Counts are bounded by3g-3 at that fixed genus, so fixed moments pass through the first limit. This uses no diagonal N(g) approximation. OWR's footnote and DGZZ's principal-stratum lattice-count passage support the uniform/weighted and principal/full-holomorphic conventions.

## Priority and normalization boundary

The credited geometric consequence is consistent with the original question and with the checked prior probability/geometric inputs. Liu's actual thesis Remark1.5.9 and the direct rendered slides distinguish all-multiplicity and primitive microscopic formulas; they only present fixed microscopic windows. Neither that quantifier nor a limiting intensity tail licenses a moving-window conclusion. The OWR source explicitly poses the intermediate question after its microscopic announcement. The note discloses the announced unavailable manuscript, does not claim a new microscopic law or universal first priority, and keeps the literal4g-4/6g-6 discrepancy visible. I found no positive same-target prior theorem in the source passages inspected for this manuscript review. This is a bounded assessment, not proof that unavailable work lacks overlap.
