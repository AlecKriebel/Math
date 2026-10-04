# Independent adversarial audit: Function Theory 6.80

## Verdict

**PASS.** The frozen package gives a complete negative answer to the exact
question in Problem 6.80. Its classification as **already_solved**, attributed
to Peter Lappan (1981), is supported. The recorded **1/5** substantive turns
is consistent with one completed reconstruction followed by this verification.
There is no required mathematical correction and no justification for a novelty
claim. This is an independent AI audit, not external expert peer review.

Audited input: the eight files frozen by manifest SHA-256
`fd3c7f0b74cf7dbfcc314b08aa6b8e8b958b99b5076bffd84019b5aebdf9a5d1`.
The manifest's seven component hashes and byte counts, plus all eight hashes in
the private freeze record, agree. The input was not edited. No remote write,
external communication, release, or source-document redistribution was made.

## 1. Exact scope and original source

I independently inspected a fresh rendering of Hayman–Lingham,
[arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), PDF page 146,
printed page 145. Problem 6.80 asks whether the zero-based primitive of every
analytic univalent function on the open unit disc is normal. It does not impose
normalization, boundary extension, or a growth bound. Its other derivative-order
statements supply context; they are not additional open claims bundled into the
question. The update says no progress had been reported to the editors.

The selected pinned dataset record matches that scope. The full source corpus
and prior-results corpus have the SHA-256 values recorded in PROVENANCE.md;
I independently recomputed both hashes and sizes. The selected prior report
contains only a statement review and an unsuccessful literature search, not a
proof that the question remained unresolved.

## 2. Branches and transformed domain

For |z|<1, 1-z lies in the open right half-plane. Consequently the principal
logarithm used in the package is a single analytic branch with imaginary part
between -pi/2 and pi/2. With w=-Log(1-z), the inverse is z=1-exp(-w).
Squaring |1-exp(-w)|<1 and cancelling the positive factor exp(-x) gives
exp(-x)<2 cos(y). The image is therefore exactly

    Omega = {x+iy : -pi/2<y<pi/2, x>-log(2 cos(y))}.

The boundary function has second derivative sec(y)^2>0. Its epigraph, with the
coordinate order (y,x), is convex. The domain has imaginary width pi; its
unbounded real direction does not invalidate segment integration or this width
bound. The coordinate map and its stated inverse are both injective.

## 3. Global univalence, including exponential winding

Let b=1/100, c=1/10, a=b+ic. Direct differentiation gives

    f(1-exp(-w)) = a exp((1+a)w) [1-u(w)],
    u(w) = (b/a) exp(-icw).

The sign in exp(-icw) and its modulus exp(cy) are correct. Uniformly on Omega,
|u|<exp(pi/20)/sqrt(101)<1/8. The displayed elementary comparison
exp(s)<1/(1-s), together with pi<4, proves that rational margin without a
floating-point assumption. Thus 1-u has a global analytic power-series logarithm.
For the package's L,

    L' = 1+a+ic u/(1-u),
    |L'-1| < 11/100 + (1/10)(1/8)/(7/8) = 87/700 < 1.

I independently checked the critical collision argument. If exp(L(w2)) equals
exp(L(w1)), segment integration gives B(w2-w1)=2 pi i k, where
|B-1|<=87/700. This rules out B=0. For k=0 it forces w2=w1. For k nonzero,
|B-1|<1 implies |B|^2<2 Re(B), hence Re(1/B)>1/2. Therefore
|Im(w2-w1)|>pi, contradicting the domain width. This eliminates all possible
nonzero winding numbers, rather than merely establishing local univalence.

An independent stronger margin is available: if |B-1|<=q<1, then
Re(1/B)>=1/(1+q). To check this algebraically, write B=x+iy; the disc bound
implies |B|^2<=2x-1+q^2, and x<=1+q then gives |B|^2<=(1+q)x.
For q=87/700, any nonzero collision would require imaginary displacement at
least (1400/787) pi, strictly larger than pi. This corroborates the proof; no
strengthening is necessary for acceptance.

Thus f is analytic and globally injective on the whole disc. No compactness,
boundary injectivity, sampled-point argument, or unproved univalence criterion
is being substituted for this step.

## 4. Nonnormality and zero-based primitive

At t_n=exp(-20 pi n), z_n=1-t_n with n>=1, the chosen branch is real on t_n>0.
Then exp(-ic log(t_n))=exp(2 pi i n)=1, so F(z_n)=0 and
f(z_n)=ic t_n^(-1-b). Consequently

    (1-|z_n|^2) F#(z_n)
      = (1/10)(2-exp(-20 pi n)) exp(pi n/5) -> infinity.

All points lie strictly inside the disc. The prefactor 1-|z_n|^2=2t_n-t_n^2
and the exponent pi n/5 are correct. Since F(0)=0 and F'=f, F is precisely the
primitive based at zero; there is no integration-constant mismatch.

The normality criterion is used in its standard Lehto–Virtanen sense. It is
also displayed in Section 3 of Gröhn's published-format PDF. The automorphism
family interpretation agrees: precomposing by a disc automorphism taking 0 to z
multiplies the spherical derivative at 0 by 1-|z|^2. Marty's criterion then gives
the equivalence used in the proof. Thus the divergent sequence disproves exactly
the claimed normality, not a different growth property.

## 5. Normalization challenge

Independent exact arithmetic gives

    f(0)=i/10,  d=f'(0)=-1/100+(51/500)i=(-5+51i)/500 != 0.

Hence h=(f-i/10)/d is univalent, h(0)=0 and h'(0)=1. Its based primitive
H=(F-(i/10)z)/d has bounded H(z_n). Its weighted derivative is
(c/|d|)(2t_n-t_n^2)(t_n^(-1-b)-1), which diverges because its leading term
is (2c/|d|)t_n^(-b). Dividing by the bounded denominator 1+|H(z_n)|^2 preserves
divergence. The normalization paragraph is valid even though the original
question does not require it.

## 6. Primary-publication and version checks

I reopened the [publisher's Lappan article page](https://academic.oup.com/jlms/article-abstract/s2-24/3/495/860269).
It gives the 1981 article *On the Normality of Derivatives of Functions, II*,
JLMS (2) 24(3), 495–501, DOI 10.1112/jlms/s2-24.3.495. Its abstract expressly
supports the univalent-integrand/nonnormal-integral conclusion. The original
paywalled full text remains uninspected; neither this audit nor the submission
claims otherwise.

I also reopened the
[author-hosted published-format Gröhn PDF](https://integraali.com/defense/defense4/suomeksi/papereita/Grohn%20-%20On%20non-normal%20solutions.pdf),
and made fresh local renders from both supplied source PDFs:

- Published-format PDF page 9, equation (12): the second exponent is -1/100.
  The adjacent attribution identifies Lappan's Theorem 5, reference [16].
- Published-format PDF page 12, reference [16]: the 1981 paper with “II” and
  the same DOI as the publisher page.
- [arXiv:1602.00161v1](https://arxiv.org/abs/1602.00161v1), page 9, equation
  (12): the second exponent is visibly -i/100.
- The arXiv bibliography on page 11 instead names the 1978 Math. Ann. paper
  without “II”.

These are genuine rendered differences, not OCR artifacts. The submitted
counterexample uses the published real exponent. I checked the extra argument
in PROVENANCE.md: for the misprinted expression J, its first term eventually
dominates the bounded second term as r=|1-z| tends to zero. The given estimates
and 1-|z|^2<=2r yield weighted spherical derivative O(r^(1/100)); away from 1
there is analytic continuation across the relevant compact boundary portion.
Thus that misprinted expression is normal. The warning is substantively correct.

The publisher's abstract and the later published-format citation support known
resolution despite the stale 2018 update. This is not an assertion of having
read Lappan's original proof, nor an inference of novelty from a catalogue.

## 7. Reproduction, limits, and corrections

The original `python3 verify.py` completed successfully. Every exact output
agrees with CHECKS.json, and this environment also reproduced all its stored
floating diagnostics. The script recomputes the diagnostics and tests their
thresholds; by design it compares only the `exact` object and the stored pass
flag with CHECKS.json. Its boundary-rounding warning is justified: already
z_1 rounds to 1 in binary64.

The separate `independent_diagnostics.py` uses exact Fraction arithmetic and
1000-decimal mpmath calculations. It evaluates the original z-plane formulas
directly at n=1,2,5,10,20, checks nonzero interior distances, and confirms the
weighted spherical derivatives and normalized variant. These are deliberately
finite, non-interval-certified diagnostics, not the justification for global
univalence or divergence. Their role is to challenge coefficient, sign,
normalization, and numerical-coordinate mistakes.

Required corrections: **none**. CORRECTIONS.md records one nonblocking wording
suggestion about what the default control script compares. The frozen files
remain untouched. Original source PDFs and page images are private evidence and
are excluded from the public audit whitelist.

## Audit log

- 2026-10-04 10:02 UTC: freeze and complete proof inspected; 25% of audit.
- 2026-10-04 10:04 UTC: source pages rendered and checked; 70% of audit.
- 2026-10-04 10:05 UTC: independent direct diagnostics and boundary challenges
  completed; 90% of audit.
- Final audit and hash sealing: 100% of this verification task. Repository
  publication is outside this audit's authority and has not been performed.
