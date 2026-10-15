# Independent source-scope checkpoint

This checkpoint was sealed before reading any sibling family report, the root proposed disposition, or the proposed closure comment. Incoming head: `8163ee0dc7a0f944570925984cef2dc0fb291ad8`; target: `30001234`. This is validation of the original one-turn construction, not a second proof-search turn. The original ledger remains 1/5.

## Independently inspected primary evidence

Downloaded the official [Takagi 2013 PDF](https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf), DOI [10.2140/ant.2013.7.917](https://doi.org/10.2140/ant.2013.7.917), extracted its full text, and inspected actual full-page 240 dpi pixels of printed pp. 937, 939, 940. Also downloaded the official [OWR 2009 report](https://ems.press/content/serial-article-files/46224), DOI [10.4171/owr/2009/21](https://doi.org/10.4171/owr/2009/21), and inspected printed pp. 1137-1139 at 240 dpi. PDF bodies, full text and pixels remain private and ignored.

The 2009 LP uses rational nonnegative variables, nonstrict augmented inequalities, and existence of one optimizer with a singleton augmented-image fiber. Minimal binomial generation and monomial exclusion enter Question 8. The 2013 matrix includes term exponents and one sum row per polynomial. Remark 4.3 repeats that fiber condition for a normal complete-intersection ambient variety. Example 4.4 specifies affine six-space and the same three minors; it states failure of the condition and an LP optimum of 3. These are exact source facts, not a comparison with a modified graph LP.

## Coordinate bridge (independent calculation)

Use row order `(x1,x2,x3,y1,y2,y3)` and Takagi's paired term coordinates `q=(q11,q12,q21,q22,q31,q32)`. The printed third polynomial is `x1*y3-x3*y1`, the negative of the candidate's third polynomial. Reconstructing the term matrix gives

```
B = [1 0 0 0 1 0
     0 1 1 0 0 0
     0 0 0 1 0 1
     0 1 0 0 0 1
     1 0 0 1 0 0
     0 0 1 0 1 0
     1 1 0 0 0 0
     0 0 1 1 0 0
     0 0 0 0 1 1].
```

For the candidate blocked order `z=(mu1,mu2,mu3,nu1,nu2,nu3)`, set

```
q = (mu1,nu1,mu2,nu2,nu3,mu3) = P*z.
```

Then `B*P` is the candidate's complete 9-by-6 augmented matrix. This permutation includes both the paired/blocked conversion and the third-pair swap. It preserves nonnegativity, rationality, the objective, feasibility, all nine image coordinates, and singleton fibers bijectively.

At optimum, the three sum rows imply the objective is at most 3. Substituting

```
q(t) = (t,1-t,t,1-t,1-t,t),  t in Q intersect [0,1]
```

gives all nine image coordinates equal to 1 and objective 3. Conversely, optimum forces all three pair sums to 1. Writing `q=P*z`, the top x-coordinate rows give `mu1<=mu3`, `mu2<=mu1`, `mu3<=mu2`; hence all are `t`, with `nu_i=1-t`. Thus this is the full rational optimal face. For every `t`, choose `s=0` if `t!=0`, and `s=1` otherwise. Then `q(s)!=q(t)` and `B*q(s)=B*q(t)`. No optimizer has a singleton fiber.

## Scope challenges resolved before disposition review

* Ambient versus subscheme: in Example 4.4 the ambient `X` is affine six-space, so `c=0`. The additional equality in Remark 4.3 is the empty equality `0=0`; all three minors define `Z`. Reassigning them as ambient equations would change the LP and the problem.
* Normal/complete-intersection/local conditions: affine space is smooth, normal, a complete intersection with zero ambient equations, and log canonical at 0. The LP uses exponents and does not acquire new local constraints. The degree-two generators remain minimal after localization at the origin.
* Coefficients: the relevant Remark does not require algebraically independent coefficients. That condition belongs to Theorem 4.1. Here all coefficients are nonzero, and changing the third generator by a unit leaves the ideal unchanged while swapping its two term columns.
* Monomial exclusion: evaluation at `(1,1,1,1,1,1)` kills every minor but no nonzero monomial. Hence the ideal contains no monomial over any characteristic-zero field.
* Minimality: all six degree-two terms are distinct, so the three homogeneous generators are linearly independent in degree two. Their independent classes modulo the homogeneous maximal ideal times the ideal give a minimum generator count of three, globally and at the origin.
* Rational/nonstrict: both operative LPs are rational and closed. A strict-inequality substitute would remove the optimum and is not the printed LP. Equality of just exponent images is not substituted for equality of all nine augmented-image coordinates.

## Preliminary conclusion and limits

The 2013 primary example supplies a negative answer to the exact 2009 existential condition for precisely the candidate's ideal and generator system. The full-face parametrization is an independent elementary explanation of that already published obstruction. No new target resolution is established by this candidate. A finer unprinted formula is not automatically a novel research theorem, and the disposition still requires adversarial assessment after this seal.

Source-scope review completion estimate: 95%. Novel complete resolution estimate for this construction: 0%. No outside communication, Git/index mutation, or changes to original artifacts were made. No copyrighted prose is quoted in this checkpoint.
