# Independent review of the known sharp convexity radius

**Verdict: PASS_COMPLETE_CREDITED_SHARP_RADIUS. No mandatory correction.** The exact class radius is sqrt(2sqrt(3)-3), with a valid universal lower bound and an admissible sharp extremal. Recommend **already_solved**, retaining classical attribution and the stated access limitation for the 1963 original.

Reviewed on 2026-09-30 by a separate GPT-6 Astra agent at xhigh reasoning. This is an adversarial AI audit, not human peer review or a new-discovery claim.

## 1. Frozen artifacts

`KNOWN_RESULT.md` SHA-256:
`bc199dc9d84f7982a4e7574af4ddaba8385226434cd77480f9723a8f00f100a0`.

Submitted verifier SHA-256:
`43b1ede11aba4a4426d7871043cc1329d0890d0de0a4b54c2ff10405225da055`.

Submitted receipt SHA-256:
`acc49f0dc741bc9d8dfe709591e3aa11b5db059024235134b398775e23cedc6e`.

## 2. Exact source and known-result status

I checked the complete statement of [Hayman–Lingham Problem 6.22](https://arxiv.org/abs/1809.07200v2), printed pp.122–123, including its normalization and displayed equivalent positive-real-part expression. The source asks for the uniform convexity radius of normalized univalent functions starlike of order 1/2. It is not asking for one radius shared by every individual function as its own maximal radius. The 2018 statement that no progress had been reported to the editors is an editorial update, not evidence overriding a published earlier theorem.

The full [Singh–Goel 1971 paper](https://www.jstage.jst.go.jp/article/jmath1948/23/2/23_2_323/_pdf) was read at the class definition (1.1), the relevant derivative estimates, and Theorem 4.2 with extremal (4.6), pp.330–331. The rendered theorem page confirms all coefficients and the piecewise parameter range. Its transition polynomial is negative at zero and positive at beta=1/2, so its smallest positive root is below 1/2. Thus the theorem's second branch applies.

At beta=1/2, equation (4.9) becomes

    -(r^4+6r^2-3)/2=0.

Formula (4.11) has squared radius

    (3/2)/(3/2+sqrt(3))=2sqrt(3)-3.

The source states sharpness for the whole class and identifies the extremal family used in the submission. This independently establishes the known-result status, even without the 1963 paper.

[Bhowmik–Biswas, arXiv:2606.20872v1](https://arxiv.org/abs/2606.20872v1), p.3 and reference [11], explicitly attributes this exact radius to MacGregor's Theorem 1. Its preprint status and different convolution question are correctly disclosed. The original MacGregor full text was not available in the submitted source cache or obtained in this audit. Its historical attribution is therefore supported indirectly by this primary paper; the complete sharp theorem was verified directly in Singh–Goel. No new 2026 convolution assertion is a proof dependency.

## 3. All-function lower bound

For an admissible f, univalence implies that its only zero is the simple zero at the origin and that f' never vanishes. Thus q=zf'/f is holomorphic with q(0)=1. The harmonic minimum principle upgrades Re q>=1/2 to strict inequality on the disk. The transform w=1-1/q is therefore a holomorphic disk map vanishing at zero.

Let r=|z| and rho=|w(z)|. Schwarz's lemma gives rho<=r. Apply Schwarz–Pick to phi=w/z, interpreted at zero by its removable value. Since

    z*w'-w=z^2*phi',

the bound is exactly

    |z*w'-w| <= (r^2-rho^2)/(1-r^2).

If phi has a unimodular constant value, both sides are zero, so this case is not omitted. The submitted logarithmic-derivative identity

    1+z*f''/f'=(1+z*w')/(1-w)

is correct. Splitting its numerator as 1+w+(z*w'-w) gives the positive-real-part term (1-rho^2)/|1-w|^2 and the controlled perturbation. Because r^2-rho^2>=0, substituting |1-w|<=1+rho in its negative contribution has the claimed inequality direction. The numerator factors as

    (1+rho)*(rho^2-(1-r^2)*rho+1-2r^2).

Completing the square leaves

    (rho-(1-r^2)/2)^2+(3-6r^2-r^4)/4.

It is strictly positive for r<R=sqrt(2sqrt(3)-3). No assumption that the minimizing rho belongs to [0,r] is required for this lower bound; a global lower bound suffices. At zero the convexity expression is one. The classical analytic convexity criterion then gives a convex image of the open disk of radius R. For each smaller circle, continuity and pointwise strict positivity give the positive minimum requested in the original formulation.

## 4. Extremal admissibility and sharpness on every larger disk

Put rho_*=2-sqrt(3) and a=rho_*/R. The identities a^2=2/sqrt(3)-1 and 0<a<1 are correct. The roots of 1-2az+z^2 lie on the unit circle, so its square root has a holomorphic nonzero branch on the disk, normalized to one at zero. Consequently

    f_*(z)=z/(1-2az+z^2)^(1/2)

is holomorphic, has a simple zero at zero, and satisfies f_*'(0)=1.

The submitted Blaschke-product argument correctly proves Re(z*f_*'/f_*)>1/2 throughout the disk. There is also a direct independent positive-real-part check: choose theta with a=cos(theta), put eta=exp(i*theta), and write

    P(z)=(1-z^2)/(1-2az+z^2)
        =((1+eta*z)/(1-eta*z)
           +(1+conj(eta)*z)/(1-conj(eta)*z))/2.

Both terms have positive real part on the disk. Since z*f_*'/f_*=(1+P)/2, the extremal belongs to the full stated starlike class and is univalent by the standard starlikeness criterion. Direct differentiation also gives f_*'=(1-az)/(1-2az+z^2)^(3/2), which has no zero in the disk.

The second logarithmic derivative has precisely the cubic numerator B displayed in the submission. At R, the identities R^2=1-2rho_* and rho_*^2-4rho_*+1=0 give B(R)=0 and R*B'(R)=-6rho_*<0. Its denominator is strictly positive for real 0<z<1. Thus the convexity expression is negative at real points immediately beyond R, not merely zero on the boundary. Every larger disk contains such a point. The same normalized univalent extremal therefore excludes every radius larger than R.

This establishes global sharpness for the class. Equality at a boundary point is consistent with convexity on the open radius-R disk. Nothing here asserts that every admissible function loses convexity at R.

## 5. Reproducibility and publication recommendation

The submitted exact SymPy verifier passes **467 assertions**, with a byte-identical receipt. The independent standard-library checker uses rational complex arithmetic for **3,840 admissible Schwarz–Pick jets**, and exact arithmetic in Q(sqrt(3)) for the threshold, sharp contact, derivative sign and source specialization. It passes **8,443 assertions**. It also checks negativity beyond the radius at 91 exact scaled points inside the disk. These are finite controls; Sections 3–4 provide the all-function and sharpness reasoning.

The mathematics resolves the exact source question as a credited classical result. Preserve the distinction between the directly verified 1971 theorem and the indirectly corroborated 1963 attribution. No correction to the frozen mathematical artifact is required, and no novelty, human-peer-review or new convolution theorem claim follows from this audit.
