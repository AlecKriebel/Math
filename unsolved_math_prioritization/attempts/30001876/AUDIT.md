# Independent normalization challenge: GL3 restriction, problem 30001876

Review date: 11 October 2026. This review concerns exact local formulas and the explicitly scoped spectral reconstruction, not the validity of the entire Li–Young restriction theorem.

This AI-assisted manuscript is unrefereed. Acceptance refers to an internal AI mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification. This is not a computational reproduction package. No novelty or priority claim is made.

Editorial chronology: this is the complete independent mathematical challenge to the earlier reconstruction retained as PROOF.md. Its two convention-relative calculations refine the earlier hold without erasing that report’s original reasoning or implying that all original displays were consistent. Only authored prose and public metadata are distributed; source documents, source extracts and images, datasets, executable code, raw outputs and private coordination material are excluded.

## 1. Result and acceptance boundary

The audit's principal decision to **withhold blanket acceptance of the printed exact-normalization chain is confirmed**. The alleged incompatibility of (3.13), (3.18), (3.19), and (3.20) is real under their printed definitions. The literal upper-unipotent quotient in (2.8) also contributes an additional factor 2 when unfolded against the ordinary hyperbolic measure on the modular surface. Neither problem disappears merely by invoking an unspecified quotient convention.

However, the factor 2 issue must not be promoted into the assertion that the final printed gamma-period expression is necessarily off by a factor 2. A fresh Bessel/Mellin/Barnes calculation below gives a precise mechanism by which the local factor errors compensate. There is also a **previously untracked interchange of the two spectral parameters in the power function**. That interchange distinguishes two legitimate but different repair conventions:

- Preserve literal Li–Young (2.1)–(2.3): the local period factor is `8 J = P_plus / D`, conditional on the standard corrected Takhtadzhyan–Vinogradov Bessel formula used below.
- Use the Bump/Blomer power-function convention, obtained by interchanging the two exponents in Li–Young (2.3): the local period factor is `8 J = P_minus / D`. Here `P_minus / D` is exactly the expression printed as (3.19). Thus the final expression survives the factor corrections in this intended-convention reading.

The change of power function is material and cannot be silently applied while claiming to preserve all printed definitions. In particular, this review does **not** certify `8 J = P_minus / D` for the literal printed Jacquet definition. Conversely, it does not conclude that the paper's final restriction theorem is false. Its eigenvalue-aspect bound and the rest of its proof are outside this review.

The fixed-scale spectral decomposition, zero global constant component, odd-parity vanishing, Mellin inverse factor `1/pi`, and norm factors `1/pi` and `1/(4 pi^2)` are accepted in the audit's stated cuspidal setting, with its stated standard analytic imports. Those conclusions are independent of the gamma/sign ambiguity.

## 2. Source versions and actual inspection

### Main article

Li–Young, *The L2 restriction norm of a GL3 Maass form*, Compositio Mathematica 148 (2012), 675–717, DOI [10.1112/S0010437X11007366](https://doi.org/10.1112/S0010437X11007366). The creator's retained publisher PDF has 890977 bytes and SHA-256 `4d9e561254394b453a0bea6bc7de585f6138c82c54949db836fdf6b8669fed7b`.

I read the definitions and Fourier/spectral conventions at printed 677–680; the normalization comparison at 683; Proposition 3.3 and its entire printed proof at 684; Proposition 3.4 and its entire printed proof at 685–686; Proposition 3.5, Corollary 3.6 and Theorem 4.1's spectral/Plancherel argument at 686–687. Rendered pages 683–684 were directly visually checked. Other passages were read from the full retained PDF's text extraction. I did not re-audit sections 5–10. Proposition 3.5's proof is omitted in the source; no omitted proof is counted as inspected.

### New primary normalization source

Blomer, *Applications of the Kuznetsov formula on GL(3)*, Inventiones Mathematicae 194 (2013), 673–729, DOI [10.1007/s00222-013-0454-3](https://link.springer.com/article/10.1007/s00222-013-0454-3). I inspected the publisher's section 2 HTML, including definitions (2.10)–(2.12), Mellin formula (2.15), and notes 3–5. I also retrieved [arXiv:1205.1781v2](https://arxiv.org/pdf/1205.1781v2), dated 21 January 2013, and read and visually inspected its pages 6–7. These contain the same relevant normalization definitions and notes. The retained arXiv PDF has 464121 bytes and SHA-256 `465f761889d19314b4902138f988b1acb2a4db14cab4b3329f7032b664518d29`.

Blomer's note 4 explicitly warns that the parameters in the Goldfeld p.154 power-function display are interchanged relative to the following formulas and Bump's convention. Note 5 records the change from 4 to 8 in Goldfeld (6.1.3), and the factor 2 between the Stade 1993 function and the corresponding completed function. These are directly relevant normalization warnings, not an official erratum to Li–Young.

The Bessel identity (2.12) is imported as the classical Takhtadzhyan–Vinogradov formula. I checked its complete displayed prefactor, both Bessel arguments, its measure, its raw Jacquet definition, and the coordinate and parameter mapping. I do not claim to have inspected the original Takhtadzhyan–Vinogradov proof or the original Stade 1990 proof. Blomer's following display defining the modified W-tilde changes `u^2` to `u` without the corresponding visible factor 1/2; it is therefore not used for a constant calculation. The present calculation uses (2.12) directly and independently derives its Mellin transform, agreeing with (2.15) after normalization.

### Additional corroboration, not the decisive convention anchor

Broughan, *Evaluating Jacquet's GL(n) Whittaker function*, Mathematics of Computation 78 (2009), 1061–1072, electronically published August 2008, DOI [10.1090/S0025-5718-08-02158-3](https://doi.org/10.1090/S0025-5718-08-02158-3). The author's [retained PDF](https://kevinbroughan.nz/papers/whittaker.pdf) is explicitly a 4 November 2005 preprint, not the 2009 final version: 266617 bytes, SHA-256 `dc688fcf35a57f4b50652773276393cde6c27f7631af1c2f54c4ed05ae7e7cc5`. I read its power/Jacquet definitions, Theorem 3.1, rank-three part of Theorem 3.2, dimension-three comparison, and Figure 1; pages 4, 7 and 9 were visually inspected. I also inspected corresponding published text via the [Waikato institutional copy](https://researchcommons.waikato.ac.nz/server/api/core/bitstreams/08f01ebd-d44e-4ec8-9f2d-bf4e0bd0ccbd/content), but did not obtain its PDF bytes. It is not represented as a pinned final PDF.

Broughan explicitly records the correction from 4 to 8 and identifies the completed gamma multiplier. Its rank-three display and Figure 1 have the Bump-convention Bessel expression. Its stated power/Q conventions do not provide a clean independent way to eliminate the interchange flagged by Blomer. I therefore use it only as corroboration and use Blomer's matched raw definition as the convention anchor. No GL(n)pack or other source-author code was downloaded or executed. Looking at printed equations/code output is not executing it.

Blomer–Buttcane–Raulf, *A Sato–Tate law for GL(3)*, CMH 89 (2014), 895–919, DOI [10.4171/CMH/337](https://doi.org/10.4171/CMH/337): I inspected the creator's retained page 905 and footnote 4 visually, and read the opening parameter discussion. Its 8-versus-4 correction is corroborative. The repeated `y2` in both displayed Bessel arguments is not propagated into this review.

Search/retrieval failures are retained as such. No claim is made to have obtained Goldfeld 2006, Stade 1990, or the final Broughan PDF when the attempted route returned an error. Complete retained PDFs were not read in their entirety.

## 3. The printed four-equation contradiction really is local and algebraic

Put

`A = i alpha = 1 - nu1 - 2 nu2`,
`B = i beta = -nu1 + nu2`,
`C = i gamma = 2 nu1 + nu2 - 1`, so `A+B+C=0`.

Let

`D = pi^(1/2-3nu1-3nu2) Gamma(3nu1/2) Gamma(3nu2/2) Gamma((3nu1+3nu2-1)/2)`.

This is symmetric in `nu1,nu2`. Replacing the parameters with (2.5)–(2.7) gives exactly the denominator printed in (3.19). Let

`P_minus(s,tau) = pi^(-3s) product_{q in {A,B,C}, epsilon=+1,-1} Gamma((s + epsilon i tau - q)/2)`.

For the common integration functional `I`, equation (3.18) is `G=4 I(W_J)`, while (3.13) is `W_J*=D W_J`. Equation (3.20), as visibly printed, is `I(W_J*)=P_minus/(4D)`. Consequently those three equations imply `G=P_minus/D^2`. Equation (3.19) instead says `G=P_minus/D`. No change to a later spectral measure or signed-index convention changes this linearity calculation. For generic parameters `D` is neither zero nor one.

At the special triple `A=B=C=0`, `D=1`. That special test would fail to expose the contradiction and must not be used as the only test of it. The incompatibility is a functional one for general spectral parameters.

Replacing `W_J*` by `W_J` in (3.20), or deleting its denominator, can repair one implication, but neither operation by itself establishes the correct factor 4/8 or the correct parameter orientation. The corrected calculation below is needed.

## 4. Why the U2 unfolding contributes 2

The printed group is the integer upper unipotent group with diagonal entries 1. Hence `-I` is not in `U2`. The paper independently confirms that convention in (2.18), where its usual Eisenstein series is one half of the sum over `U2\SL2(Z)`.

Let `Gamma_infinity = {+I,-I} U2`. Above every `Gamma_infinity` coset there are two `U2` cosets. On the restricted upper-block matrix,

`diag(-gamma,1) diag(r g_z,1) = diag(gamma,1) diag(r g_z,1) diag(-1,-1,1)`.

The same identity remains true after left multiplication by the positive diagonal `M` in the Fourier expansion. The rightmost matrix is orthogonal, so every spherical Whittaker seed is unchanged. This is not an identification of distinct U2 cosets: it is an equality of the two summands on this particular restriction. A modular fundamental domain under the ordinary effective action tiles the strip once with `Gamma_infinity` cosets, and twice with the printed `U2` cosets.

The ordinary measure is `dx dv/v^2`, and the continuous density for the paper's Eisenstein normalization is `d tau/(4 pi)`. If one instead uses half this measure to reflect the ineffective center, the spectral density for the unchanged Eisenstein functions must double. Keeping (2.18), (2.23), and the ordinary hyperbolic measure simultaneously rules out an invisible half-volume cancellation.

After the correct substitution `a=r/sqrt(v), b=v`, the Whittaker integral is

`J_tau(s) = integral_{a,b>0} W_J(diag(ab,a,1)) K_{i tau}(2 pi b) (a^2 b)^s da db/(a^2 b^2)`.

The remaining factors are 2 from `W_(1/2+it)=2 sqrt(y) K_it(2 pi y)e(x)`, and 2 from pairing `n` and `-n` for an even GL2 form. Thus, with the Fourier coefficients and measure literally printed,

`Lambda_j(s) = 8 conjugate(rho_j(1)) L_j(s) J_tj(s)`.

The same holds for the Eisenstein period with its stated Fourier coefficient. Eisenstein constant terms give zero when paired with each nonzero Whittaker character. Replacing `U2` by `Gamma_infinity` without doubling the restricted seed coefficients is not the same Fourier expansion.

## 5. A general calculation with every constant retained

Use Blomer's shifted parameters `eta1,eta2`, set `eta0=eta1+eta2`, and write

`lambda1=2 eta1+eta2`, `lambda2=-eta1+eta2`, `lambda3=-eta1-2 eta2`.

Let `delta=eta1-eta2=-lambda2` and `mu=3 eta0/2=(lambda1-lambda3)/2`. The completed form of Blomer (2.12) is

`W_lambda*(a,b) = 8 a b (a/b)^(delta/2)`
`  times integral_0^infinity K_mu(2 pi a sqrt(1+u^2))`
`       K_mu(2 pi b sqrt(1+u^(-2))) u^(3 delta/2) du/u`.

The completion multiplier of the raw Jacquet integral is

`D_eta = pi^(-3/2-3 eta0) product_{j=0,1,2} Gamma(1/2+3 eta_j/2)`.

No quotient multiplicity is present in this Archimedean identity. The number 8 belongs to the Bessel formula itself.

### 5.1 Double Mellin transform

Define

`M_lambda(x,y) = integral W_lambda*(a,b) a^(x-1) b^(y-1) da/a db/b`.

The elementary Bessel Mellin formula is

`integral_0^infinity K_mu(2 pi c t) t^(z-1) dt`
` = (1/4) (pi c)^(-z) Gamma((z+mu)/2) Gamma((z-mu)/2)`.

Its factor `1/4` follows from the usual `2^(z-2)` transform and the argument `2 pi c t`; see [DLMF 10.43.19](https://dlmf.nist.gov/10.43.E19).

Integrating `a` uses `z=x+delta/2=x-lambda2/2`, giving the gamma factors `(x+lambda1)/2` and `(x+lambda3)/2`. Integrating `b` uses `z=y-delta/2=y+lambda2/2`, giving `(y-lambda1)/2` and `(y-lambda3)/2`. The remaining u-integral is

`integral_0^infinity u^(y-lambda2) (1+u^2)^(-(x+y)/2) du/u`
` = (1/2) Gamma((y-lambda2)/2) Gamma((x+lambda2)/2) / Gamma((x+y)/2)`.

The total numerical constant is `8*(1/4)*(1/4)*(1/2)=1/4`. Therefore

`M_lambda(x,y) = pi^(-x-y)/4`
` times product_{k=1}^3 Gamma((x+lambda_k)/2) Gamma((y-lambda_k)/2)`
` divided by Gamma((x+y)/2)`.

This calculation agrees with Blomer (2.15) after removing his explicitly displayed auxiliary normalization. It does not use the potentially mistyped following W-tilde Bessel display.

### 5.2 The GL3 times GL2 integral

Set

`I_lambda(s,tau) = integral W_lambda*(a,b) K_(i tau)(2 pi b)`
`                       (a^2 b)^s da db/(a^2 b^2)`.

Mellin inversion of the last K factor gives

`I_lambda = pi^(-3s)/16 product_k Gamma(s+lambda_k/2)`
` times (1/(2 pi i)) integral Gamma((z+i tau)/2) Gamma((z-i tau)/2)`
`      product_k Gamma((s-z-lambda_k)/2) / Gamma((3s-z)/2) dz`.

The substitution `z=2w` contributes another factor 2, so the leading constant becomes `pi^(-3s)/8`.

For completeness the form of Barnes' second lemma used here is

`(1/(2 pi i)) integral Gamma(w+a) Gamma(w+b)`
`   product_{k=1}^3 Gamma(c_k-w) / Gamma(a+b+c1+c2+c3-w) dw`
` = product_{k=1}^3 Gamma(a+c_k) Gamma(b+c_k)`
`   / product_{1<=j<k<=3} Gamma(a+b+c_j+c_k)`.

Use `a=i tau/2`, `b=-i tau/2`, and `c_k=(s-lambda_k)/2`. Since `sum lambda_k=0`, the three denominator factors are exactly `Gamma(s+lambda_k/2)` and cancel the outside factors. We obtain

`I_lambda(s,tau) = pi^(-3s)/8`
`   times product_{k=1}^3 product_{epsilon=+1,-1}`
`           Gamma((s+epsilon i tau-lambda_k)/2)`.

For tempered parameters start with `Re(s)>0` and a line `0<Re(w)<Re(s)/2`; for general parameters start further to the right with a separating contour. The Bessel Mellin integrals and beta integral converge there, and exponential gamma decay justifies the Mellin/Barnes manipulations. The identity then continues meromorphically. No claim of pointwise convergence of a later global spectral family follows just from this local continuation.

Barnes' second lemma is a standard imported special-function identity; its full five-gamma, one-denominator version is stated here to make the constant and substitutions checkable. It can also be found in the primary exposition D. Dufresne, [*G distributions and the beta-gamma algebra*](https://fbe.unimelb.edu.au/__data/assets/pdf_file/0009/2591802/181.pdf), Theorem 4.3 and its proof (PDF page 12, inspected through the web extraction). That source is a 36-page author/institutional version; the entire paper and its earlier probabilistic imports were not audited. The identity is not inferred from a search snippet with a missing denominator.

### 5.3 Diagnostic checks, not substitutes for proof

At `lambda1=lambda2=lambda3=tau=0`, `s=2`, integrating `a` and `b` reduces the calculation to

`I/P = (1/4) integral_0^infinity u log(1+u^(-2))/(1+u^2)^2 du = 1/8`.

Indeed `t=u^2`, followed by `v=1/(1+t)`, makes the integral equal to `1/2`. Reviewer-authored numerical controls independently evaluate the Barnes contour for a nonsymmetric imaginary triple and its negative, at a nonreal s, so that an undetected sign reversal cannot hide behind a self-dual test. These controls check arithmetic and transcription only, not the imported Whittaker identity or the automorphic theorem.

## 6. Mapping this calculation to the actual Li–Young definitions

This is the crucial distinction that prevents premature lifting of the audit hold.

### 6.1 Literal printed power function

Li–Young (2.3) says

`I_nu(diag(ab,a,1)) = a^(nu1+2nu2) b^(2nu1+nu2)`.

Blomer (2.11) says

`I_eta(diag(ab,a,1)) = a^(1+2 eta1+eta2) b^(1+eta1+2 eta2)`.

The two functions coincide if and only if

`eta1=nu2-1/3`, `eta2=nu1-1/3`.

The unipotent coordinates match by `u1=u23, u2=u12, u3=u13`; both characters are `exp(-2 pi i(u23+u12))`. Their long Weyl matrices differ by a diagonal sign, which leaves the power function unchanged. This is explicitly noted by Blomer and follows directly from the orthogonal quotient. Therefore the raw Jacquet integrals, not merely their spectral labels, match under this substitution.

For this substitution,

`(lambda1,lambda2,lambda3)=(-A,-B,-C)`

and `D_eta=D`. Consequently the result of Section 5 gives

`8 J_tau(s) = P_plus(s,tau)/D`,

where

`P_plus = pi^(-3s) product_{q in {A,B,C}, epsilon=+1,-1}`
`                           Gamma((s+epsilon i tau+q)/2)`.

This is an explicit calculation relative to the literal printed power-function convention and the imported corrected Bessel identity. No a/b interchange was made: `a` remains the lower diagonal ratio, and the GL2 K function is at `b`.

### 6.2 Intended Bump convention

If instead one corrects the power function to

`I_nu^Bump = a^(2nu1+nu2) b^(nu1+2nu2)`,

then `eta1=nu1-1/3`, `eta2=nu2-1/3` and

`(lambda1,lambda2,lambda3)=(C,B,A)`.

Now `D_eta=D` as before, but Section 5 gives

`8 J_tau^Bump(s) = P_minus(s,tau)/D`.

Thus the printed gamma expression is a consistent final period factor in this corrected convention: the omitted stabilizer 2 and the local factor 4-versus-8 error compensate. A coherent repair uses 8 instead of 4 in the defining integral, uses `I(W*)=P_minus/8` without a D denominator, and restores the stabilizer factor in the unfolding. The earlier Stade comparison constant becomes 2 instead of 4 when matching the corrected completed function and the square-root substitution. More precisely, Li–Young (3.11) equals `2 W_J*(nu2,nu1)` under the Bump convention, but equals `2 W_J*(nu1,nu2)` if its literal power-function convention is retained. All of this must be stated together with the power-function convention.

The two triples `{A,B,C}` and `{-A,-B,-C}` are not generally permutations of each other. They agree in special self-dual cases, which is another reason that checking only `beta=0`, or only the zero triple, is inadequate. The nonsymmetric numerical control deliberately distinguishes them. This review does not silently relabel F as its contragredient or interchange the Fourier indices to remove this difference.

## 7. Independent checks of the spectral and analytic claims

### Constant component

The global constant coefficient is zero. In the fixed-r unfolding every Whittaker summand has a nonzero `u12` Fourier index, and integration over `0<=x<=1` kills it. The possible extra stabilizer 2 multiplies zero. Standard convergence of the cuspidal Fourier expansion and its rapid decrease justify this unfolding. This is not a claim that the restricted function has zero GL2 cusp constant term. A nonzero Eisenstein component is compatible with zero pairing against the global constant eigenfunction.

### Odd parity

The element `diag(-1,1,-1)` of SL3(Z), together with the right orthogonal action, sends `x` to `-x` on the restricted upper block. Thus `f_r(-x+iv)=f_r(x+iv)` for every r. This proves fixed-scale vanishing against odd GL2 forms directly. It avoids relying only on uniqueness of a transformed period. Pairing the signed Fourier indices gives the same conclusion. The sign-pair factor 2 in an even period is distinct from the stabilizer factor 2.

### Mellin inverse and norm constants

With `Lambda(s)=integral c(r) r^(2s-1) dr/r` and `x=log r`, the central-line transform uses Fourier frequency `2t`. Hence

`c(r)=(1/pi) integral_R Lambda(1/2+it) r^(-2it) dt`

in the appropriate inversion sense. Mellin Plancherel gives

`integral |c(r)|^2 dr/r = (1/pi) integral |Lambda(1/2+it)|^2 dt`.

Combining this with ordinary GL2 Parseval and its `1/(4pi)` continuous density gives the audit's coefficients `1/pi` and `1/(4pi^2)`. These identities concern the integral-defined Lambda and survive every local gamma normalization question.

### L2 versus pointwise

Finite restriction norm yields L2 inversion and almost-everywhere continuous-spectrum assertions; it alone does not imply an absolutely convergent inverse at every r. The audit correctly separates this from the stronger smooth cuspidal case. Its short-row-lattice argument supplies a genuine route to uniform decay at both scale ends: the determinant-one representative has lattice vectors of lengths at most `r^(1/3)/sqrt(v)` and `r^(-2/3)`. For `r>=1` their geometric mean is `r^(-1/6)v^(-1/4)`; for `r<=1` the first suffices. Quantitative reduction and standard cuspidal rapid decrease for derivatives then supply arbitrarily high power decay, enough to integrate against any fixed Eisenstein series of polynomial growth and to obtain Schwartz behavior in log r.

Those reduction and derivative-decay results remain imports. The audit does not claim that one unquantified sentence about rapid decay proves them. Its Fejer-regularized formula is a safe alternative for a continuous L2 coefficient. I also accept its restriction against interchanging the full j,t,tau family without an additional majorant. The spectral expansion is safely an L2 identity; pointwise local-uniform convergence uses the smooth spectral/Sobolev theorem stated in the source, not just formal Parseval.

## 8. Final recommendations

1. Retain acceptance of the scoped, integral-defined spectral reconstruction.
2. Retain the finding that the four displayed normalization assertions cannot all be literal.
3. Retain the literal U2 stabilizer factor, but add that it can cancel a separate local factor error in the intended convention.
4. Add the explicit power-function interchange warning and the two scenario calculations above before adopting a single gamma replacement.
5. Do not call the final period formula false solely because of the intermediate factor errors; do not call it certified under literal (2.3) solely because the constants cancel in the other convention.
6. Do not infer a new unsolved conjecture, a failure of the paper-wide restriction bound, or a claim of official erratum from this local review.

The resulting hold is now narrower and more informative: the constant can be calculated, and the remaining editorial choice is whether the defining power function or the parameter signs are corrected. A fully specified corrected theorem can be written in either convention, subject to the standard imported Bessel identity. A source-level statement that all original displays were already consistent cannot be accepted.
