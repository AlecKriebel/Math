# Independent audit of the reconstructed circle minimum packet

Problem 2303014, rank 676. Audit date: 2026-10-05 UTC.

## Verdict

**PASS for the stated partial results, with two minor precision notes.** No
counterexample or substantive proof defect was found in Claims C1-C5 under the
packet's explicit hypotheses. The general positive-mean, nonconstant-data problem
remains unresolved. This verdict does not establish a solution to the problem
under every possible reading of its printed boundary condition.

The audited material is the new seven-file reconstruction identified in
`BINDING.json`. The original missing packet, its reported checks, and any prior
review were not used as mathematical or integrity evidence. No audited file was
modified. Suggested clarifications are isolated in `CORRECTIONS.md`.

## Scope of the verification

Every line of the reconstructed proof and its two Python/JSON check artifacts
was inspected. All six files listed by its manifest match their recorded byte
counts and SHA-256 values; the manifest itself matches the supplied target hash.
The checker was copied into a separate directory and replayed there. It completed
with 30,254 checks and produced bytes identical to the frozen `CHECKS.json`.

An independently written checker adds 47,419 exact rational checks, including
Poisson composition, reflection and rotation covariance, the arctangent boundary
map, dipole signs, and deliberate wrong-formula rejection controls. The two counts
refer to different checkers and are not a proof certificate for an analytic
statement. The independently authored checker and its result are supplied here.

Primary PDFs were retrieved anew from the exact public URLs. Both hashes already
recorded in the reconstruction match the newly retrieved bytes. The actual
printed statement and projection theorem were visually inspected, rather than
accepted from OCR alone. Retrieval and inspection metadata are recorded in
`SOURCE_INSPECTION.json`; source files and extracted source text are excluded.

## Boundary classes and the original question

The inspected Problem 3.14 prescribes integrable boundary data and a
nonpositive circle infimum, without specifying a boundary topology or Poisson
majorization. Its 2018 update is a historical report of no progress known to the
authors, not evidence of the state of the literature in 2026. The reconstruction
correctly distinguishes this ambiguity from its chosen classes.
[Hayman and Lingham, printed p.65](https://arxiv.org/pdf/1809.07200v2).

In this audit, A_F means finite, interior-continuous subharmonic functions with
almost-everywhere radial trace F, pointwise ceiling P[F], and the condition on
**every** centered circle. W_F removes only that ceiling. Neither an a.e. trace
nor an integrable datum alone supplies the ceiling. The dipole construction
explicitly demonstrates why silently making that deduction would be wrong.

Interior continuity has several separate uses: actual circle minima, passage
to the origin, continuity of slit extensions, compactness of a contact set, and
bounded stopped values on smaller closed disks. The audit does not remove it.
Requiring continuity on the entire closed unit disk would exclude the positive
constant examples: uniform positivity near a positive constant boundary makes
the circle condition impossible. The exceptional slit endpoint is therefore
important, not an overlooked boundary defect.

## C1 General L1 slit construction

**PASS.** The change of angle on the right semicircle and odd reflection produce
an L1 function g. In fact its full-circle L1 norm equals the full-circle L1 norm
of G. Its Poisson integral is finite and smooth at every interior point. Under
the reflection R(w)=-conj(w), kernel covariance and g(R xi)=-g(xi) imply
h(Rw)=-h(w); h vanishes on the entire imaginary diameter.

The factor 1/(4 pi) in the paired integral is correct: the ordinary Poisson
normalization is 1/(2 pi), and the substitution t=2 arg(xi) contributes another
factor 1/2. For xi on the right unit semicircle and Re(w)>0, the difference
between the reflected and original squared denominators is
4 Re(w) Re(xi)>0. Hence the paired kernel is positive. This argument needs no
boundedness or smoothness of G, only nonnegativity and integrability.

Across a nonzero slit point, the two square-root limits lie on the imaginary
diameter, where h=0. At the tip, h(0)=0 and smoothness give
|h(sqrt(z))|=O(sqrt(|z|)). Thus the extension is continuous, including at zero.
It is harmonic off the slit and nonnegative with value zero at every slit point.
The local submean criterion therefore proves subharmonicity on the entire disk.
It need not be harmonic or smooth across the slit.

For the upper bound, Q(xi)=G(xi squared) is integrable. The two-sheet identity

P_(w squared)(xi squared) = (P_w(xi)+P_w(-xi))/2

is also directly verifiable for every unit xi and every interior w. Integrating
it, or applying the Fourier argument in the packet, proves the required Poisson
composition. The left-side values of g need not equal -Q at the same point;
the proof correctly uses only g<=0<=Q there. This avoids an otherwise tempting
reflection error for non-even G.

The standard radial limit theorem is applicable to g in L1. Square rooting a
radial path gives another radial path, and the angle change preserves null sets.
The slit endpoint adds only one exceptional angle. These facts justify the trace
for arbitrary L1 data, not merely continuous or trigonometric data.

Subtracting P[F minus] preserves subharmonicity and supplies the correct trace
and ceiling P[F]. On the slit the result is nonpositive, which certifies every
radius exactly. Rotation covariance gives the stated rotated competitors. The
bounds on the supremum are finite because at least one finite competitor exists
and P[F] is finite at every interior point. No optimality of radial slits for
nonconstant F follows from this construction.

## C2 Weak trace unboundedness

**PASS.** For unit eta, the kernel difference d_eta is a finite harmonic function
inside the disk, although it is unbounded near its boundary atoms. Its radial
trace is zero outside those two atoms. For every 0<r<1, its values at the positive
and negative eta radii are respectively 4r/(1-r squared) and its negative.

Choosing the previously constructed competitor with slit on the negative eta
radius preserves a nonpositive witness on every circle after adding A d_eta,
for every A>0. At any prescribed nonzero point on the positive radius, this
increases the value without bound. The construction retains interior continuity,
subharmonicity and the a.e. trace. It is not asserted to retain the majorization
condition; indeed for sufficiently large A it cannot do so. At zero the dipole
vanishes, and the proposition expressly makes no unboundedness claim there.

## C3 Nonpositive mean

**PASS.** If m=P[F](0)<=0, the harmonic mean-value identity makes the average on
every centered circle equal to m. Continuity on that circle then forces a
nonpositive minimum. Thus P[F] itself lies in A_F. Its pointwise majorization
property gives the maximum at any prescribed interior point. If another
competitor agrees at one such point, u-P[F] is subharmonic, bounded above by zero,
and attains its maximum in the connected disk. The strong maximum principle
forces equality everywhere. This covers zero mean and evaluation at the center.
The result is specifically about A_F; it would be false for W_F away from zero.

## C4 Positive constant sharp value

**PASS.** The potentially disconnected contact set is covered by the actual
cited theorem. In Øksendal's Theorem 1, K is an arbitrary compact subset of the
closed annulus, and the comparison is between harmonic measures of K and its
circular projection. Taking inner radius zero gives the closed-disk setting;
connectedness is absent. The theorem and proof were inspected on printed
pp.192-193. Lawler's inspected alternative explicitly assumes connectedness and
is correctly not used as a substitute here.
[Øksendal, Theorem 1](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7393-11512_2006_Article_BF02384309.pdf),
[Lawler, Section 7.1](https://www.math.uchicago.edu/~lawler/harmonicpaper.pdf).

Here is the stopping argument with the minor convention made explicit. When
u(z)>0, z is outside K={u<=0} intersected with the closed R-disk. This K is compact,
contains zero, and projects onto [0,R]. Let tau_R be disk exit, T_K the first hit,
and tau=min(tau_R,T_K). Finite continuity bounds u above and below on the closed
disk. The subharmonic stopped process and bounded convergence give

u(z) <= E_z[u(B_tau)] <= C Pr_z(tau_R<T_K).

An exit point in K counts as contact, including when T_K=tau_R. On that event its
value is nonpositive. Since the disk is bounded, tau is finite almost surely;
no unproved uniform integrability of unbounded boundary data is being used.
No regularity of every point of K or connectedness of K is required.

After rotating z to -|z|, the projection theorem bounds the last probability by
escape past the radial segment [0,R]. Scaling and reflecting put the observation
point at |z|/R with the slit on the negative radius. Under the square root this
becomes a right half-disk. The stated harmonic function there is correct.
One direct verification is to put T(w)=(1+iw)/(1-iw). For w=x+iy,

Re T(w)=(1-|w| squared)/((1+y) squared+x squared),
Im T(w)=2x/((1+y) squared+x squared).

Inside the right half-disk both are positive. On its semicircular boundary the
first is zero, and on its imaginary diameter the second is zero with the first
positive. The analytic arctangent branch at zero consequently gives values
between zero and one after multiplying Re arctan(w) by 4/pi, with the required
boundary values. The two corners have harmonic measure zero. Evaluation on the
positive axis yields b(|z|/R).

For A_c, the ceiling c holds on every smaller closed disk. Letting R increase to
one supplies the upper bound. The slit competitor and its rotations attain it
at each specified nonzero point; at zero they attain zero, already the universal
upper bound. This proves exactly (4c/pi) arctan(sqrt(|z0|)). No uniqueness or
novelty claim is needed.

The general-data corollary also holds. Its ceiling C_R is guaranteed on the
closed R-disk. That is all the lemma's proof requires. If the word 'there' in
the lemma is read as demanding the ceiling on a whole neighborhood, apply the
lemma with C_R+epsilon, which does hold on a sufficiently small neighborhood,
and let epsilon decrease to zero. If C_R=0, use u<=0 directly. The wording change
in `CORRECTIONS.md` makes this compatibility immediate.

## C5 Nonconvexity and finite sampling

**PASS.** For positive constant data, strict positivity of the paired kernel
away from the slit makes each extremizer's zero set exactly its slit. Different
slit directions have disjoint zero sets on each positive-radius circle. The
mean and maximum of two such nonnegative functions are therefore everywhere
positive on that circle. Compactness and continuity make their circle minimum
strictly positive, not merely pointwise positive. Their other basic subharmonic,
trace, and ceiling properties do not repair that failure. The class is neither
convex nor maximum-closed. Its radial pointwise supremum is likewise infeasible.

For any nonempty finite sample of radii, the polynomial q_a in the packet has
positive Laplacian, ceiling c and the required constant trace, while passing
every sampled radius and failing all radii above a. Thus even exact all-angle
checks on the sampled circles cannot certify feasibility. For an empty sample
the same conclusion is immediate by choosing any 0<a<1. The independent control
uses a=3/4 and c=1: it passes radii 1/4, 1/2 and 3/4 but has value 13/28 at 7/8.

## What this audit does not establish

- A sharp formula or all optimizers for general positive-mean nonconstant F.
- Equivalence of A_F with an intended boundary interpretation of the source.
- A version with interior continuity removed.
- Current literature completeness, historical novelty, or priority.
- Validity of the missing historical packet or its reported control count.
- A formal proof-assistant certificate or continuum verification by sampling.

The appropriate status is **independently audited partial results for the
explicit class**, with the general target still unresolved.
