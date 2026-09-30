# Exact two-atom Upsilon criterion and a Mellin-line limitation

Status: original general problem unresolved, 2/5. Separate review pending. The theorem below classifies every positive two-atom dilation measure on its full Lévy domain. It also answers negatively the particular Mellin-line converse mentioned in the original report. It does not classify arbitrary dilation measures. No novelty claim.

## 1. Source, domain and prior work

Jan Rosiński's contribution to *Mini-Workshop: Lévy Processes and Related Topics in Modelling*, Oberwolfach Report 7/2007, printed pp.439–440, defines

U_gamma(rho)(A) = integral rho(A/t) gamma(dt)

for a sigma-finite Borel dilation measure gamma on (0,infinity), with rho having no mass at zero. The question asks for general injectivity criteria on the Lévy domain. It also states that, for finite gamma, an interval of zeros of M_gamma(1+iu) implies noninjectivity, and asks whether the converse holds. Source: https://ems.press/content/serial-article-files/46095?nt=1 .

A Lévy measure on R^d is a positive Borel measure with rho({0})=0 and integral w(x)rho(dx)<infinity, where w(x)=min(1,||x||^2). We write D_c rho(A)=rho(A/c). For gamma=a delta_s+b delta_t, a,b>0 and 0<s<t, the transform is D_s(a I+b D_c), c=t/s>1. Fixed positive dilation is an invertible map of the class of Lévy measures. The full domain is exactly that class: each positive output term controls its input, and conversely w(c x)<=max(1,c^2)w(x). Thus it suffices to study gamma=a delta_1+b delta_c.

Prior theory is credited to Barndorff-Nielsen, Rosiński and Thorbjørnsen, *General Upsilon-transformations*, ALEA 4 (2008),131–165, https://alea.math.cnrs.fr/articles/v4/04-07.pdf . Theorem 3.4 gives the general full-domain criterion for finite gamma with finite second moment, and Section 6 treats multiplicative cancellation, dimension reduction and known noninjective examples. The Aarhus report https://data.math.au.dk/publications/thiele/2008/imf-thiele-2008-02.pdf is a version of the same paper, not a second independent result. Broader Mellin cancellation work is discussed in Section 5 below; no priority assertion is made for this restricted calculation.

## 2. Complete two-atom classification in every dimension

**Theorem.** For a,b>0, c>1 and any integer d>=1, a I+b D_c is injective on all Lévy measures on R^d if and only if

a/b <= 1 or a/b >= c^2.

Equivalently, it fails to be injective precisely when b<a<b c^2. Both endpoint cases are injective.

**Necessity of the open inequalities for a nonzero kernel.** Suppose two Lévy measures have equal images. Their difference nu is a signed locally finite measure on R^d minus {0}, with finite weighted total variation integral w d|nu|. This formulation avoids undefined subtraction of two infinite values on arbitrary sets meeting zero. On every relatively compact Borel set away from zero, equality gives

a nu(A)+b nu(A/c)=0.

Take the half-open annulus E={x:1<=||x||<c} and identify every annulus c^n E with E by scaling. Its signed finite measure nu_n(B)=nu(c^n B) satisfies a nu_n+b nu_{n-1}=0 for every integer n. Therefore nu_n=(-q)^n nu_0, where q=b/a>0. Total variation is preserved by these Borel bijections, so |nu|(c^n E)=q^n m, where m=|nu_0|(E).

If m=0, the countable annulus partition shows nu=0. Otherwise, for n>=0 the weight w is one on c^n E, and finiteness forces sum_{n>=0}q^n<infinity, hence q<1. For n<0, w(x)=||x||^2>=c^(2n) on c^n E. Thus finiteness also forces sum_{n<0}(c^2 q)^n<infinity, hence c^2 q>1. Together these are 1/c^2<q<1, or b<a<b c^2. At q=1 or c^2 q=1 the respective series has constant positive terms, so neither endpoint admits a nonzero kernel. This proves injectivity outside the open interval without density, moment, or angular assumptions.

**Sufficiency and explicit collision.** Suppose 1/c^2<q<1. Fix a unit vector e. Define the signed locally finite measure

nu = sum_{n in Z} (-q)^n delta_{c^n e},

and let rho_plus and rho_minus be its positive and negative parts. The points are distinct; the even exponents carry rho_plus and the odd exponents carry rho_minus. Both are nonzero and distinct. Their total weighted mass is bounded by

sum_{n>=0}q^n + sum_{n<0}(c^2 q)^n < infinity.

Hence they are Lévy measures in the full domain. At the output atom c^n e the signed coefficient is

a(-q)^n+b(-q)^(n-1)=0.

The positive output measures are locally finite away from zero, and equality at every atom proves equality on all Borel sets by countable additivity, including sets of infinite mass. Thus U_gamma(rho_plus)=U_gamma(rho_minus). QED.

## 3. The imaginary Mellin line does not characterize the full Lévy domain

Take a=2,b=1,c=2. Then M_gamma(1+iu)=2+exp(iu log 2) has modulus at least one, so its zero set is empty. Nevertheless Section 2 provides different Lévy measures with the same transform:

rho_plus = sum_{n even} 2^(-n) delta_{2^n e},
rho_minus = sum_{n odd} 2^(-n) delta_{2^n e}.

This is a counterexample to the converse asked on printed p.440 of the original report. The density and total-mass conditions of the input cannot be dropped or silently changed: these measures have infinite total mass near zero, although their required quadratic small-jump integrals are finite. The dilation measure gamma itself is finite and has finite second moment.

There is no conflict with the source's sufficient interval-of-zeros condition. A sufficient condition for failure need not be necessary. Here the nontrivial cancellation occurs at nonzero real Mellin exponent: a+b c^z=0 has roots with real part log(a/b)/log(c) in (0,2), not on the imaginary axis. This observation is a diagnostic for this family, not an asserted general complex-strip criterion.

The negative-converse conclusion is also already implied by a published general construction: Jacobsen, Mikosch, Rosiński and Samorodnitsky, *Inverse problems for regular variation of linear filters, a cancellation property for sigma-finite measures and identification of stable laws*, Annals of Applied Probability 19 (2009),210–242, Theorem 2.1, https://arxiv.org/pdf/0712.0576v2 . In their notation use the dilation measure gamma, alpha=1 and theta=pi/log(2). Its tilted Mellin integral is 2+2 exp(i pi)=0. Their equations (2.5)–(2.6) provide the distinct positive densities x^(-2) and (1+cos(pi log(x)/log(2)))x^(-2) with the same transform. Both are Lévy measures. The required neighboring Mellin moments are finite for our two-atom kernel. We credit this prior implication; our discrete collision is an elementary certificate, not a new discovery claim. The cited theorem classifies cancellation against a prescribed power-law reference measure and does not assert full-domain injectivity for arbitrary inputs.

## 4. Finite-input cancellation is strictly weaker

For the same two-atom transform, injectivity holds on finite positive measures with no mass at zero for every a,b,c as above. Indeed the finite signed difference obeys the same recurrence. If m>0, its total variation dominates m sum_{n in Z}q^n, which diverges for every q>0. Thus m=0 and the difference vanishes. Restricting a general Fourier cancellation argument to finite input measures therefore cannot settle injectivity on the full Lévy domain.

## 5. Exact remaining gap and verification

The original demand for general criteria for arbitrary sigma-finite gamma is not resolved. No conclusion is supplied for arbitrary continuous kernels or arbitrary kernels with three or more atoms. The annular recurrence closes because there are exactly two dilation terms with a fixed ratio; this mechanism does not justify a general spectral characterization. Broader cancellation results for prescribed power-law outputs have different quantifiers from full-domain injectivity.

The checker verifies exact rational recurrence identities, positive/negative output equality on interior atoms of truncations, boundary residuals, and geometric weighted-tail formulas for many parameter choices. A finite truncation is not falsely called a kernel: its two boundary atoms are explicitly retained. Infinite summability and the all-dimensional annulus proof are proved above, not inferred from numerical tests. Review and independent checks are required before repository publication.
