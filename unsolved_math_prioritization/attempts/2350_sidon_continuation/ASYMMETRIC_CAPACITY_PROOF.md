# Exact overlap refinement and a sharp asymmetric relaxation barrier

12 October 2026. Erdős 864 / problem 2350 / queue row 1741.

## Scope and results

This note continues the reflected-core argument. It proves a finite refinement which retains a nonnegative core–unpaired overlap term and a nonnegative window-variance term. It then solves the corresponding colored macroscopic relaxation exactly, even after imposing the conjectured symmetric-core bound on every centered truncation.

The unrestricted conjecture is **not solved**. No unrestricted leading constant below sqrt(2), integer counterexample, or realization of a continuous profile is established. There is no publication or repository change in this work, and no novelty or priority claim.

The conditional implication from a symmetric-core theorem is

    |A| <= (1 + (1-1/sqrt(2)) kappa + o(1)) sqrt(N),       (C)

if every admissible reflected core of diameter at most N has size at most (kappa+o(1))sqrt(N). At the conjectured symmetric constant kappa=2/sqrt(3), the resulting unrestricted constant is

    1 + (2-sqrt(2))/sqrt(3) = 1.338203957451... .

It is not 2/sqrt(3). The continuous relaxation below attains this larger constant while obeying all of its difference/sum packing inequalities and the hypothesized sharp bound on every centered subcore. Thus even a symmetric theorem, combined with these macroscopic constraints, does not yield the full conjecture.

The finite implication (C) follows by substituting the hypothesized k<=kappa sqrt(N)+o(sqrt(N)) into the established W<=sqrt(N)+O(N^(1/4)) and using m=W+(1-1/sqrt(2))k. It does not require the continuous countermodel.

## 1. Finite notation and exact occupied-difference accounting

Let A be a subset of {1,...,N} having at most one repeated unordered sum; equal summands are included in this condition. If a repeated sum exists, denote it by T and put

    C = A intersect (T-A),    U = A\C,
    k = |C|,    u = |U|,    m = k+u.

If no sum repeats, set C empty and U=A. Let

    W = u+k/sqrt(2),    Q = u+k/2.

For d>0, write r_A(d) for the number of ordered pairs (a,b) in A^2 with a-b=d; define r_C and r_U similarly. Put

    x(d) = #{(a,b) in C x U : a-b=d}
         + #{(a,b) in U x C : a-b=d}.

The reflection identity from the controlling weighted proof states that a repeated positive difference has exactly two representations, both in C, and they are reflections of one another. A C-pair (a,b) is its own reflected pair exactly when a+b=T. Let

    p(d) = 1 if there are a>b in C with a-b=d and a+b=T,
           0 otherwise.

The equations specifying such a,b have at most one solution. It follows, including possible midpoint cases, that

    c(d) = (r_C(d)+p(d))/2

is the indicator of d being a positive difference of C. Furthermore,

    c(d) + x(d) + r_U(d) <= 1.                            (1)

Indeed any collision between two of these types, or two representations involving U, would be a repeated difference with an endpoint outside C. Consequently

    r_A(d) - r_C(d)/2
      = c(d)+x(d)+r_U(d)-p(d)/2
      <= 1-p(d)/2.                                       (2)

Unlike assigning a factor 1/sqrt(2) to each core endpoint, (2) uses the full capacity cost of a mixed C–U difference.

## 2. A finite variance-and-overlap inequality

Suppose A is nonempty and let L=max A-min A. For an integer h>=1 define

    F_C(x) = #{c in C : 0 <= x-c < h},
    F_U(x) = #{v in U : 0 <= x-v < h},
    F_A = F_C+F_U,    F_w = F_U+F_C/sqrt(2).

All functions are summed over the L+h integer points

    J = {min A,...,max A+h-1}.

Set

    S_h = sum_(x in J) F_C(x) F_U(x),
    P_h = sum_(d=1)^(h-1) (h-d)p(d),
    V_h = sum_(x in J) (F_w(x)-hW/(L+h))^2.

Then

    h^2 W^2/(L+h) + V_h + (2-sqrt(2)) S_h
       <= hQ+h(h-1)-P_h.                                (3)

Every retained term V_h, S_h, P_h is nonnegative. Empty A satisfies the natural zero version separately.

**Proof.** Expanding sliding-window squares gives

    sum_x (F_A(x)^2-F_C(x)^2/2)
       = hQ + 2 sum_(d=1)^(h-1) (h-d)(r_A(d)-r_C(d)/2).

Apply (2) to obtain the right side of (3). Pointwise,

    F_A^2-F_C^2/2 = F_w^2+(2-sqrt(2))F_C F_U.

Since sum_x F_w(x)=hW, the exact variance identity is

    sum_x F_w(x)^2 = h^2 W^2/(L+h)+V_h.

Combining these identities proves (3). No limiting argument is used. QED.

Dropping V_h, S_h, P_h recovers the previously established finite weighted inequality. Keeping S_h gives the explicit strengthening

    W^2 <= (L+h)(Q+h-1)/h
           -(2-sqrt(2))(L+h)S_h/h^2.                    (4)

This is an unconditional estimate with an explicitly measurable mixing penalty. It is not a uniform improvement of the leading constant, since that penalty can vanish macroscopically.

## 3. Necessary colored continuum constraints

Consider a sequence with N tending to infinity and translate its rescaled interval to I=[-1/2,1/2]. Define

    gamma_N = N^(-1/2) sum_(c in C) delta_(c/N-1/2),
    upsilon_N = N^(-1/2) sum_(v in U) delta_(v/N-1/2).

The difference multiplicity bound gives m=O(sqrt(N)), so subsequential weak limits gamma and upsilon exist. Denote reflection about zero by a tilde and Lebesgue measure by lambda. The following measure inequalities hold on the entire real line:

    (1/2) gamma*tilde(gamma)
       + gamma*tilde(upsilon)+upsilon*tilde(gamma)
       + upsilon*tilde(upsilon) <= lambda,               (D)

    (1/2)(gamma+upsilon)*(gamma+upsilon) <= lambda.      (S)

For a sequence with T/N tending to 1, gamma is symmetric about zero. More generally its center is the limit of T/(2N)-1/2. No symmetry of upsilon is required or inferred.

**Proof of (D).** For d nonzero, the coefficient of the relevant convolution measure at d/N is (r_A(|d|)-r_C(|d|)/2)/N and is at most 1/N by (2). Its atom at zero has mass Q/N=o(1). Bound the remaining measure by the lattice Riemann-sum measure and pass to the weak limit. All displayed convolution components are nonnegative, despite the equivalent expression using a subtraction.

**Proof of (S).** The half ordered sum count differs from the unordered count only by a diagonal measure of total mass m/(2N)=o(1). Every nonexceptional unordered sum has capacity one; the exceptional sum contains at most floor(m/2)+1 representations and therefore contributes only o(1) after division by N. Translation of sums by the chosen interval midpoint changes no capacity bound. Pass to the Riemann-sum limit. QED.

Inequality (D) implies gamma=g dx and upsilon=v dx for nonnegative L^2 functions supported on I. For example (1/2)gamma*tilde(gamma)<=lambda bounds the L^2 norm of each mollification of gamma by sqrt(2); weak L^2 compactness identifies its limit as gamma. The same argument gives v in L^2 with norm at most one.

Mollify (D) with the triangular approximate identity obtained by convolving a normalized symmetric interval indicator with itself, and evaluate at zero. L^2 convergence of the mollifications gives

    integral_I (g^2/2 + 2gv + v^2) <= 1.               (5)

Put K=integral g, U=integral v, and W=K/sqrt(2)+U. The length of I is one, and therefore (5) is equivalently the following refined necessary bound:

    W^2
      + integral_I (g/sqrt(2)+v-W)^2
      + (2-sqrt(2)) integral_I gv <= 1.                (6)

In particular W<=1. Equality requires both

    g/sqrt(2)+v=1 almost everywhere on I,
    gv=0 almost everywhere.

Hence every equality profile has the form

    g=sqrt(2) 1_E,    v=1_(I\E)                       (7)

for a measurable subset E of I. When gamma is symmetric, E is symmetric up to null sets. This is a profile-level segregation statement; it is not an assertion that every such E is realizable by integer sets.

### 3.1 A stronger bound when one component is macroscopically uniform

If either g=K almost everywhere on I or v=U almost everywhere on I, Cauchy–Schwarz applied to the other component in (5) yields

    M^2-K^2/2 <= 1,    where M=K+U.                     (6a)

The same conclusion holds if g=Kp and v=Up for a common nonnegative density p of mass one: the left side of (5) is then (M^2-K^2/2) integral p^2, and integral p^2>=1. These are extra profile hypotheses, not consequences of the original problem. With a symmetric-core theorem of constant kappa, (6a) gives the conditional estimate

    M <= sqrt(1+kappa^2/2).

At kappa=2/sqrt(3), this is sqrt(5/3)=1.290994448736... . It improves (C) in these additional subclasses, but still exceeds the conjectured full constant.

## 4. An exact maximizer satisfying all the displayed constraints

Fix 0<=K<=sqrt(2), set s=K/sqrt(2), and let

    E_s = [-1/2,-(1-s)/2] union [(1-s)/2,1/2],
    g_s = sqrt(2) 1_(E_s),
    v_s = 1_(I\E_s).

Boundary choices are immaterial. These have masses

    integral g_s=K,    integral v_s=1-s,
    M=integral(g_s+v_s)=1+(1-1/sqrt(2))K.              (8)

They satisfy (D), (S), core symmetry, and (6) with equality. Thus for fixed core mass K, the exact maximum total mass in the relaxation (D),(S) with symmetric core is the value in (8).

Here is a direct check of the convolution inequalities. For t>=0 define

    z_s(t) = measure{x in I : x+t in I,
                    1_(E_s)(x) != 1_(E_s)(x+t)}.

The density in (D) is

    H_s(t) = (1-t)_+ + (sqrt(2)-1)z_s(t).             (9)

To verify this, in the overlap I intersect (I-t), pairs with both endpoints in E_s contribute g*g/2=1 per unit length; pairs with both endpoints outside E_s contribute v*v=1; mixed pairs contribute sqrt(2). All kernels are reflection symmetric in t.

For 0<=t<=1, a mismatched pair must cross at least one of the two interior boundaries of E_s. For each boundary the set of possible x has length at most t. Therefore

    z_s(t)<=2t,
    H_s(t)<=1-t+2(sqrt(2)-1)t
           =1-(3-2sqrt(2))t<=1.

For t>1 there is no overlap, so H_s(t)=0. This proves (D) at every t, not merely close to zero.

Both g_s and v_s are symmetric, so convolution with their reflection is the same as ordinary convolution. The density in (S) is

    (1/2)g_s*g_s + g_s*v_s + (1/2)v_s*v_s,

which is no larger than H_s since their difference is g_s*v_s+(1/2)v_s*v_s>=0. Thus (S) holds as well.

The functions g_s and v_s have disjoint supports and g_s/sqrt(2)+v_s=1_I, proving equality in (6).

## 5. Adding the full centered symmetric-core bound does not close the gap

Grant hypothetically that every symmetric admissible set of diameter at most D has at most (kappa+o(1))sqrt(D) points, with 0<=kappa<=sqrt(2). Applying it to every centered truncation of an actual core would give, in the continuum normalization above,

    integral_[-r,r] g <= kappa sqrt(2r)
       for 0<=r<=1/2.                                 (B_kappa)

The hypothesized theorem also implies this bound for any symmetric subcore, using the diameter of that subcore; bounding all centered truncations is at least as strong for their masses. The assertion is hypothetical here: the conjectured kappa=2/sqrt(3) is not proved by this note.

Impose (B_kappa) on the relaxation from Section 4. Its exact optimum remains

    M_max = 1+(1-1/sqrt(2))kappa.                       (10)

For the upper bound, r=1/2 yields K<=kappa; (6) then gives

    M=W+(1-1/sqrt(2))K
       <=1+(1-1/sqrt(2))kappa.

For attainment, use Section 4 with K=kappa and s=kappa/sqrt(2). Write t=2r. The truncated core mass is

    sqrt(2) max(0,t-1+s).

When t>=1-s, the claimed bound is equivalent to

    t-1+s <= s sqrt(t).

On writing z=sqrt(t), the difference between the two sides is

    (z-1)(z+1-s)<=0

for 0<=z<=1. The case t<1-s is immediate. This proves every inequality (B_kappa), not only the full-interval one.

For kappa=2/sqrt(3), the core occupies a fraction s=sqrt(2/3) of I, the central unpaired-profile interval has length 1-sqrt(2/3), and (10) equals 1.338203957451... . The proposed unrestricted constant is 2/sqrt(3)=1.154700538379... .

Consequently a proof based only on (D), (S), core symmetry, and all the hypothesized centered symmetric-core bounds cannot eliminate this larger relaxed value. This is a counterexample to that analytic implication, not to the integer conjecture.

Even the fully uniform-profile subclass of Section 3.1 retains a strict gap. Indeed take

    g=kappa 1_I,
    v=(sqrt(1+kappa^2/2)-kappa) 1_I.

The second coefficient is nonnegative for 0<=kappa<=sqrt(2). The density in (D) is exactly (1-|t|)_+, while that in (S) is ((1+kappa^2/2)/2)(1-|t|)_+, also at most one. A centered truncation has core mass kappa(2r)<=kappa sqrt(2r). Thus all these constraints hold and the bound sqrt(1+kappa^2/2) is attained within this more restrictive continuous subclass. Macroscopic mixing alone, even in this particularly regular form, is insufficient to transfer the symmetric target to the full problem.

## 6. What remains discrete, and what is not asserted

For every finite input, U intersect (T-U) is empty. The example nevertheless gives upsilon a symmetric weak density. There is no contradiction: disjoint lattice occupancies and their reflections may have overlapping, even equal, weak densities. The continuous example supplies no finite integer U, no sequence of admissible A, and no claim that this specific profile can actually arise.

The exact occupied-site identities in Section 1 retain information that is absent from their weak limits. For example

    c(d) r_U(d)=0,
    c(d) x(d)=0,
    x(d) r_U(d)=0,

with every factor an integer in {0,1}. These identities concern simultaneous occupancy at the same lattice difference, not merely the marginal limiting convolution densities. At a relaxed equality profile the mixed term vanishes at zero and the core and U difference densities there add to one. An actual sequence approaching that profile would therefore need nearly complete complementary packing of their short differences, in the averaged sense encoded by (3), while also satisfying the sum exclusions. No contradiction to such microscopic packing is proved here.

In particular it would be invalid to replace these exact disjoint occupancies by disjointness of the limiting convolution densities. It would also be invalid to infer that symmetry of v_s makes U a second reflected core. Neither passage through the weak limit is justified.

A new discrete incompatibility, or a stronger symmetric-core theorem controlling more than the size of every centered truncation, is needed to rule out this profile. This note does not identify a proved additional universal discrete inequality which does so. The finite overlap refinement quantifies the alternative: positive limiting overlap or nonconstant weighted density spends additional capacity in (6), but the endpoint/core and middle/unpaired profile makes both expenditures exactly zero.

## 7. Provenance and verification scope

The controlling weighted proof and scoped acceptance in the prepared public edition were read, together with the prior original weighted argument and its symmetric continuum barrier. The reflection identity is taken from and re-explained in that supplied material. No fresh scholarly claim or current literature-status claim is made, and no external theorem is needed for Sections 1–6 beyond elementary finite identities, Cauchy–Schwarz, convolution, and L^2 approximate-identity facts proved or described above.

The companion check.py exhausts every A subset of {1,...,N} for 1<=N<=16, keeps the inputs satisfying the original diagonal-inclusive unordered-sum condition, and checks (1), (2), the exact window identity, and the finite refinement (3) for the stated finite h choices. Inequalities involving sqrt(2) use exact rational quadratic-field comparisons. It also independently checks the interval-overlap formulas for rational s,t, and the centered-truncation inequality using exact rational arithmetic after squaring its nonnegative sides.

These are implementation diagnostics, not substitutes for the proofs or an extremal computation record. The precise verification counts and interpreter modes are saved separately.

## Public edition notice

The preceding text is the complete accepted historical proof or audit, with only the locator edits recorded in [EDITION_MAP.md](EDITION_MAP.md). Statements about accompanying diagnostic programs, original input records, or the absence of publication describe the original research or review stage. This prose-only edition distributes no executable program, detailed diagnostic collection, source PDF or image, or private record. Original and accepted file identities are recorded in [INPUT_PINS.json](INPUT_PINS.json); public-file identities are recorded in [MANIFEST.json](MANIFEST.json). [VERIFICATION.json](VERIFICATION.json) distinguishes exact finite checks, floating-point diagnostics, and integrity checks. This notice changes no mathematical argument, verdict, or hypothesis.
