# Independent root reconstruction

Date: 2026-10-12 America/Los_Angeles. PR810, original head
5820e9784dbcfeda0acabaa435cb38cf6a4576df; problem2307042.
Acceptance/publication completion estimate at this checkpoint: 25%.

This reconstruction was performed before receiving the fresh adversarial agents'
conclusions. It does not certify priority or replace their review.

## Kernel and normalization

Let S=sin(pi*x), C=cos(pi*x), U=cosh(pi*t), V=sinh(pi*t),
D=U-C. The proposed strip density is p=S/(2D). Direct differentiation gives

    p_x = pi*(C*U-1)/(2*D^2),
    p_xx = -pi^2*S*(U^2+C*U-2)/(2*D^3),
    p_tt =  pi^2*S*(U^2+C*U-2)/(2*D^3).

The last equality uses V^2=U^2-1. Thus p is harmonic, independently of its
conformal-map derivation. At x=1/2 it has value1/(2U) and x derivative
-pi/(2U^2). Pairing opposite horizontal separations cancels the y derivative.

Pulling back the half-plane Green function yields

    g_S = (1/2)*log[(cosh(pi*(y-eta))-cos(pi*(x+s))) /
                    (cosh(pi*(y-eta))-cos(pi*(x-s)))].

Differentiation at s=0 gives pi*S/D=2*pi*p. This confirms the density
normalization and its cancellation in the Martin ratio. Exponential decay in
horizontal separation allows periodization with period2*pi and all derivatives
used in the proof. The first variable remains on an interior compact set; eta
is near pi and s is small. The uniform Taylor expansion has a common factor s
in numerator and denominator, so a highly tangential boundary approach cannot
invalidate the Martin limit.

## Minimality and hidden assumptions

Near the exceptional boundary point, expanding the explicit formula gives
p=x/(pi*(x^2+t^2))+O(x), uniformly in direction. Other period terms are smooth,
odd in x and O(x). Any nonnegative harmonic minorant is squeezed to continuous
zero boundary values elsewhere. Its odd reflection in a punctured disc is
single-valued and O(1/r). Circle Fourier coefficients rule out negative powers
of order>=2; oddness removes the log and tangential dipole. The remaining
normal-dipole coefficient B lies in[0,1/pi]. Subtracting pi*B*P leaves a
harmonic function continuously zero on the compact boundary. The maximum
principle gives zero. No assertion about arbitrary unbounded harmonic minorants
or multiply-valued angular functions is used.

## Global competitors and all directions

The four competitors descend to the annulus because they are periodic. The
affine-in-x pair is strictly above1/2; the angular pair is at least1/2 because
b*cosh(x-1/2)<=1/2. Their gradients are(+-1,0),(0,+-b), b>1/4.

The proposed kernel gradient is(-c,0), where c=pi*S2/S1. S2/S1 is a positive
weighted mean of q_k<=sech(pi^2), so c<8/83 without truncating the infinite
series. For d=(u,v), M=max(|u|,b|v|), the largest first-order improvement is
M+c*u>=(1-c)*M. Since M>rho/8, the uniform margin is>75*rho/664. Exact rational
arithmetic gives75/664-1/10=43/3320>0. One common Hessian remainder bound for the
finite family then yields strict improvement at every sufficiently small
nonzero displacement. This argument permits the competitor index and direction
to vary with radius and does not differentiate the envelope.

## Target and limits

The root read the exact source problem and update at
https://arxiv.org/pdf/1809.07200v2, printed173–174. The disc example specifies
equality along a radius, and the question asks whether the corresponding
Green-line property persists in multiply connected domains. The local theorem
negates that universal property. It does not answer a separate question about
some isolated contact point farther from the base. Current worldwide openness
and historical priority require the separate literature audit.

Strongest verified root result: the analytic proof is internally coherent and
establishes the stated local counterexample, pending independent falsification.
No mathematical defect was found by this reconstruction. The reflection,
compact maximum principle and Harnack-chain facts are classical inputs; no
formal proof-assistant verification or human peer review is claimed.
