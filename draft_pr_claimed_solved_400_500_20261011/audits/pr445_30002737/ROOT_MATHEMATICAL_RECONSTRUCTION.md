# Root reconstruction of the planar spectral counterexample

This is verification of the frozen one-attempt candidate, not a new original
proof-search attempt. Original head: `3242c84e06db7e99012c7fe581adde5c3f89fc89`.
The exact hypothesis is that absence of an absolutely continuous component of
the physical diffraction forces its absence in the full translation
representation. The tested counterexample uses ambient two-dimensional Haar
measure. It makes no claim about a separately one-dimensional assertion.

## Credited infinite input and exact scope

The original OWR report, printed2996, states Conjecture1 without a dimensional,
irreducibility or all-factor-diffraction qualifier. Its preceding discussion
uses the translation representation on the invariant probability space. The
precursor1310.0267v2, printed2–3, explicitly sets up Z^d configurations and their
R^d or d-torus correlation spectra. Root retrieved all three original PDFs and
visually read complete OWR10–11, precursor2–3 and Baake–Grimm2–3 pages; byte
bindings are in ROOT_PRIMARY_SOURCE_RECEIPT.json. The planar reading is a
source-backed interpretation, not an assertion of the author's unstated intent.

The Baake–Grimm Rudin–Shapiro input supplies a minimal uniquely ergodic binary
system (X,S,mu), a coordinate f(x)=x_0 in {-1,1}, zero mean and correlations
int f(x)f(S^m x)dmu=1_{m=0}. These are prior results. Primitive substitution
strict ergodicity and its binary factor justify uniform averages for the
continuous cylinders f and f*(f composed with S^m). This does not assume IID
symbols. The four-letter coding and bilateral seed must agree with the cited
recursion; independent reviewers are checking that bridge.

## The physical hull retains both coordinates

Let C={0,e,a,b}, e=(1/10,1/10), a=(1/3,0), b=(0,1/3). Insert both unconditional
slots0,e at every lattice cell, the a slot when x_i=1, and b when y_j=1. All
slots are distinct. The set contains Z^2 and is contained in (1/30)Z^2, hence
is Delone, Meyer and FLC. The positive, unit-mass comb has no multiplicities.

The directed difference e modulo Z^2 occurs among C only as e-0. Therefore
the local physical test p,p+e present recovers exactly the anchors, even for
cross-cell pairs and every translated hull member. Reading the a and b slots
at recovered anchors then recovers both entire binary sequences. Both signs
are distinguished by presence versus absence after the anchor is known.

With (Sx)_i=x_{i+1}, Lambda_(S^m x,S^n y)=Lambda_(x,y)-(m,n). Consequently
Phi([x,u],[y,v])=Lambda_(x,y)-(u,v) respects the unit-suspension seams and is
equivariant for increasing suspension time and negative translation. Integer
orbit closure is X times X under independent coordinate shifts; fractional
translations provide both phases. Compactness gives surjectivity. Anchors fix
the phase modulo integers; fixing representatives in [0,1)^2 fixes x,y. Thus
Phi is injective modulo precisely the suspension identifications. Local
continuity plus compact-to-Hausdorff bijectivity proves a conjugacy, not a
factor with an unobserved symbolic fiber.

Disintegrate any Z^2-invariant probability over y. Invariance under (1,0)
makes almost every x-conditional S-invariant and thus mu. The y marginal is
also mu by (0,1) invariance, so the measure is mu times mu. Product minimality
uses two independent dense orbits, not diagonal dynamics. The suspensions
inherit minimality and unique invariant probability mu*mu*du*dv. This proves
repetitivity and uniform patch frequencies for the physical hull.

Any period must preserve the recovered anchor lattice and thus be an integer
pair. Decoding forces periods in the corresponding one-dimensional systems.
A periodic point in a minimal binary hull would make that hull finite, whereas
its nonzero-period correlation would then equal1, contradicting the input
delta correlation. The only translation period is0.

## Direct physical pair calculation

Write the random variables here as invariant-space coordinate functions, not
independent symbols. The a and b occupancies are (1+x_i)/2 and (1+y_j)/2.
For slots c,d and integer displacement(m,n), the pair average equals the
product of mean occupancies, plus1/4 for c=d=a,m=0 or c=d=b,n=0. Mixed a-b
terms factor into separate spatial interval means and vanish. Uniform unique
ergodicity gives every required one-dimensional average.

Equivalently, D=delta_0+delta_e+(delta_a+delta_b)/2 and
delta_Lambda=D*delta_Z2 + delta_a*(omega_x tensor delta_Z)/2
+ delta_b*(delta_Z tensor omega_y)/2. The autocorrelation is

    gamma=(D*D_tilde)*delta_Z2
          +(delta_0 tensor delta_Z + delta_Z tensor delta_0)/4.

Each fixed motif shift changes only O(N) points at a square's boundary. All
weights are bounded and normalization is O(N^2), so the contribution vanishes.
Coincident motif differences are summed, not treated as distinct physical
displacements. Local finiteness of the difference support upgrades coefficient
limits to vague convergence. Standard unique-ergodic FLC autocorrelation theory
also identifies the canonical van-Hove limit; the square calculation suffices
to produce the displayed diffraction.

For Fourier kernel exp(-2*pi*i*k.t), the transform is

    sum_(k in Z2) |D_hat(k)|^2 delta_k
       +(lambda tensor delta_Z + delta_Z tensor lambda)/4.

It is supported on (R times Z) union (Z times R), a planar null set. The line
terms have no atoms, including at intersections. They are ambient singular
continuous measures, while the first term is pure point. The zero-lag mass is
5/2+1/2=3, matching density3; the origin Bragg mass is |D_hat(0)|^2=9.
These equalities independently check the normalization and use the actual
unweighted comb, not the preliminary weighted model.

## A genuine continuous-action spectral measure

On the first suspension choose bounded Borel h([x,u])=x_0 for 0<=u<1.
The seam has zero invariant measure. Suspension time t changes x to
S^floor(u+t)x. Conditional correlation is1 precisely when floor(u+t)=0.
The intersection [0,1) intersect [-t,1-t) has length(1-|t|)_+, including
negative and integer t. Thus C_h is the triangle function. It is the
convolution of a unit-interval indicator and its reflection, whose Fourier
transform is sinc^2(k), with sinc(0)=1. Its integral is1 by Plancherel.

The product observable H=h tensor h on the two-coordinate suspension has
correlation C_H(t1,t2)=C_h(t1)C_h(t2) by the invariant product probability.
Its finite probability spectral measure has density sinc^2(k1)sinc^2(k2).
This is positive except where a coordinate is a nonzero integer, a planar
null set; hence it is equivalent to planar Lebesgue measure. The established
conjugacy transfers H to the physical point hull. There is no need to assume
that the full spectrum is purely absolutely continuous or has multiplicity1.

The original diffraction sees the separate row and column fluctuations, while
the product observable sees both directions. An additional locally decoded
signed factor x_i*y_j has delta autocorrelation and planar Lebesgue diffraction.
This does not contradict reconstruction from a family of factor diffractions
or equivalence of pure-point diffraction and pure-point dynamics: the original
physical diffraction has a nonzero singular continuous part.

## Verification boundary and current gaps

The preceding reconstruction identifies no central mathematical gap at the
specified planar ambient-Haar level. This is a provisional root conclusion,
pending the complete independent geometric, spectral and reproduction reports
and a new whole-candidate adversary. Historical priority has not been accepted.
No paper, submission, DOI, tracker entry or merge is authorized by this note.

The reproduction family reports actual optimized-Python false success on
invalid original inputs, grouped as a verification reliability defect. Those
raw histories and the frozen source bytes will be preserved. A publication
package would require explicit-exception verification and honest historical
labels, followed by the user's fresh whole-package adversarial review loop.
This code defect is not silently converted into a mathematical-proof failure.
