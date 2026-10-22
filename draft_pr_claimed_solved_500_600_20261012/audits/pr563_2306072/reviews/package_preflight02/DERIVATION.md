# Independent mathematical adversary: PR563 / 2306072

This is an independently reconstructed argument for the frozen constructive theorem, followed by independently reconstructed source-comparison implications. The first theorem derivation preceded reading the previous whole-package verdict. The 44 controls in independent_checks.py are exact finite supplementary checks, not a universal proof or a formal certification of the classical inputs.

## Claim, premises and possible failure mechanisms

Let S be the full normalized schlicht class on the unit disk. With ε=10^-24 and η=10^-12, every global maximizer of Re L, L=a2+iε(a4−3a3), is claimed to have an actual omitted arc on which a continuous polar argument θ, signed outward radial angle β, and ordinary unsigned outward radial angle |β| are nonmonotone. Existence, every-maximizer uniformity, and membership of the tested curve in the actual omitted arc are part of this claim.

The classical inputs are compactness of S in the compact-open topology; |an|≤n; the exterior area theorem; the classical support-point theorem giving a single analytic omitted arc Γ from a finite tip to infinity with increasing radius and Q(w)dw²>0, Q=L(f²/(f−w))/w². Ordinary complex-analytic facts used below are analytic square-root selection on a zero-free disk, Rouché, the implicit-function theorem, Schwarz's lemma, and Cauchy bounds. This review checks applicability and the new deductions; it does not reprove the original classical source theorems.

The main attempted falsifications were: nonattainment; convergence only for a chosen extremizer; an invalid odd-root area application; a reversed distance inequality; continuity of tips smuggled into the proof; a Schiffer sign error; a local inverse mistaken for a disk-wide inverse; an arbitrary trajectory mistaken for a support slit; continuation past the real tip; unstable division near t=0; principal-argument jumps mistaken for genuine reversal; tangent orientation mistakes; and a finite rational calculation mistaken for a universal analytic proof. None survives the reconstruction below.

## 1. Genuine extremizers and quantitative coefficient control

Each coefficient is a continuous complex-linear functional on H(D), by Cauchy's formula on a fixed interior circle. L is consequently continuous. Koebe k(z)=z/(1−z)² has Re L(k)=2 because a4−3a3=−5 is real; the identity has Re L=0. Thus Re L is nonconstant on S and compactness gives at least one global maximizer. Everything below begins with an arbitrary one of them.

For such f, Re a2−ε Im(a4−3a3)≥2. The coefficient bounds give |a4−3a3|≤4+9=13, hence Re a2≥2−13ε. Since |a2|≤2,

    |a2−2|² = |a2|²−4Re a2+4 ≤ 52ε,
    1−|a2|²/4 ≤ 1−(1−13ε/2)² ≤ 13ε.

In particular |a2−2|<8η. There is no maximizing-selection assumption.

The analytic nonvanishing function f(z²)/z² has a normalized square root, so g(z)=z sqrt(f(z²)/z²) is analytic and odd, with g'(0)=1 and g²=f(z²). If g(z1)=g(z2), univalence of f implies z1²=z2². The negative possibility forces g(z1)=−g(z1)=0, and f has no zero except its normalized zero, so z1=z2=0 in that case. Therefore g is genuinely univalent. The exterior map 1/g(1/ζ) is analytic and univalent for |ζ|>1. Its first two negative-power coefficients are −a2/2 and 3a2²/8−a3/2. The weighted area inequality yields

    3 |3a2²/8−a3/2|² ≤ 1−|a2|²/4 ≤ 13ε.

Consequently |a3−3a2²/4|≤2sqrt(13/3)η<5η and |a3−3|<5η+(3/4)(8η)4=29η. Defining A=2a3+a2²−6a2 and B=3a2−3 gives A+2=2(a3−3)+(a2−2)(a2−4); |a2−4|≤6, so |A+2|<106η and |B−3|<24η. These bounds apply to all actual maximizers.

## 2. The actual tip, without a continuity assumption

Set H=sqrt(z/f(z)) with H(0)=1. This square root is analytic on D, and 1/g(1/ζ)=ζH(ζ^-2). Writing H=1−a2 z/2+Σn≥2 cn z^n, the same exterior area inequality gives Σ(2n−1)|cn|²≤13ε. Weighted Cauchy–Schwarz on |z|≤2/3 gives a uniform H-tail bound and derivative-tail bound. The respective squared weight sums are at most 16/135<1/4 and 56/25<9/4. For the derivative sum the termwise inequality n²/(2n−1)≤n is valid for n≥2. Combining these tails with the first-coefficient error and sqrt(13)<4 gives |H−(1−z)|<5η and |H'+1|<10η.

At z*=−2/3, H0=5/3, H0'=−1. These imply 3/2<|H|<11/6 and |H+H0|<7/2. From f=z/H², the difference of reciprocal squares has modulus at most

    5η(7/2) / [(3/2)²(5/3)²] = (14/5)η.

Multiplication by 2/3 gives |f(z*)−k(z*)|<2η. The derivative formula f'=(H−2zH')/H³ has numerator error <5η+(4/3)10η<19η. Dividing by |H|³ makes that contribution <6η. The remaining reciprocal-cube contribution is bounded using |H²+HH0+H0²|<11, |H|³H0³>125/8, and the Koebe numerator 1/3; its cost is <2η. Thus |f'(z*)−k'(z*)|<8η.

The correct distance direction can be checked independently. For any disk of radius d around y=f(z) contained in Ω=f(D), compose its affine parametrization with f^-1 and the disk automorphism taking z to zero. This disk self-map fixes zero and has derivative d/[(1−|z|²)|f'(z)|]. Schwarz implies that derivative≤1, hence d≤(1−|z|²)|f'(z)|. Passing to the maximal radius gives distance≤conformal radius, not its reverse.

The boundary Γ is closed. A nearest boundary point exists because it is a nonempty closed subset of the plane and a distance-minimizing sequence can be confined to a bounded disk. Its radius is at most |y|+distance(y,Γ). Because the classical support arc has increasing radius, the minimum boundary radius is its actual finite tip. Using k(z*)=−6/25 and k'(z*)=9/125,

    rtip ≤ |f(z*)|+(5/9)|f'(z*)|
         < 6/25+(5/9)(9/125)+(2+40/9)η
         < 7/25+7η < 3/10.

This controls the actual omitted tip of every maximizer directly. It invokes neither continuity of the tip with ε nor a putative tip of an independently drawn trajectory.

## 3. Exact finite Schiffer differential and source sign

Near z=0, for any fixed omitted w≠0,

    f²/(f−w)=−f²/w−f³/w²−f⁴/w³+terms of z-degree≥5.

Exact power multiplication gives [z²]f²=1, [z³]f²=2a2, [z⁴]f²=2a3+a2², [z³]f³=1, [z⁴]f³=3a2, and [z⁴]f⁴=1. Thus

    Q(w)=−a/w³−b/w⁴−c/w⁵,
    a=1+iεA, b=iεB, c=iε.

This finite coefficient extraction is exact, not an asymptotic truncation of the differential. Terms of higher z-degree are killed by L. Away from the omitted slit it is the meromorphic continuation of the same expression.

Duren1981 printed pp352–355 explicitly uses the denominator f−w and the positive trajectory condition. His p353 records L(f²)≠0 and a simple pole at infinity. The Koebe control Q=−1/w³ is positive on the negative real omitted ray and negative on the positive ray, independently fixing the sign. Pfluger1971 §§4.1–4.5 uses the opposite differential and negative trajectories. In his identity L(f_w)−L(f)=w²Q_P(w), f_w=wf/(w−f), one has f−f_w=f²/(f−w), whence Q_D=−Q_P. These conventions are compatible. His single-arc and strict radial-increase conclusions on printed pp28–29 apply to this finite coefficient functional; the coefficient Laurent kernel has only its permitted singularity at zero.

With w=−v^-2 and dw/dv=2v^-3, the pullback is exactly 4(a−bv²+cv⁴)dv². Calling this polynomial P, its real-reference perturbation is P0=−2−3v²+v⁴. On the entire complex disk |v|≤3, |P−1−iεP0|≤(106+24·9)εη=322εη, |P0|≤110, and |P−1|≤111ε. The disk bound, rather than a real-axis bound, permits the analytic arguments below.

## 4. A single holomorphic inverse, and identification with the actual arc

Since P lies in the disk centered at 1 of radius 111ε<1, it is zero-free and admits the square root p with positive real part. The identity (p−1)(p+1)=P−1 gives |p−1|≤111ε. Its primitive G(v)=∫0^v p(s)ds is odd and satisfies |G−v|≤333ε on |v|≤3. For each complex |t|<2, Rouché on |v|=3 compares G(v)−t with v−t; the error is <1 while |v−t|>1. Therefore exactly one root exists inside that circle. G'=p≠0 makes the root simple; local implicit functions patch by uniqueness into one holomorphic inverse V on |t|<2. Oddness gives V(−t)=−V(t), V(0)=0, V'(0)=a^-1/2, |V−t|≤333ε, and V'=1/p(V).

For 0<t≤T=7/4, W=−V^-2 is regular, solves Q(W)W'²=4, and has W∼−a/t² at infinity. Its radius is >25/81 since |V|<9/5. This lies strictly above 3/10 by 7/810. Equality of W at two positive t-values forces V(t1)=±V(t2); applying G and oddness implies t1=±t2, hence t1=t2. There is no self-intersection.

The crucial actual-slit step is independent of any converse trajectory criterion. Lift the distant actual Γ-tail under v²=−1/w. Its lift tends to zero; the positive differential condition makes Im G constant, and the limit forces that constant to be zero. Both real G-rays project to the same W-arc because V is odd. Thus W coincides with Γ near infinity. Define E={t∈(0,T]:W(t)∈Γ}. It is nonempty and relatively closed because Γ is closed. At any point of E, the radius gap excludes the finite endpoint of Γ, and P≠0 excludes differential singularities and zeros. A local analytic primitive of sqrt(Q) maps positive trajectories to horizontal lines. This proves uniqueness of the local trajectory through the point, and gives local equality of Γ and W on both sides. E is consequently relatively open. Connectedness gives E=(0,T]. In particular the point t=T is a regular interior point of the actual slit, despite being the endpoint of the chosen proof segment.

## 5. Uniform orientation, remainders and the division step

Writing Z=tV'/V gives the exact identity Z=[G(V)/V]/p(V). G(v)/v is the average of p along a radial segment. Hence |Z−1|≤222ε/(1−111ε)<223ε uniformly for all 0<t≤T, including the limit towards infinity. This avoids dividing the coarse |V−t| bound by a small t. Re Z>0, so d log|W|/dt=−2Re Z/t<0: increasing t is inward, and −W' is outward.

Let d(t)=t+t³/2−t⁵/10, so P0=−2d' and q=d'−d/t=t²−2t⁴/5. For x=P−1, the selected-branch identity

    sqrt(1+x)−1−x/2=−x²/[2(sqrt(1+x)+1)²]

is exact. Its error costs ≤(111²/2)ε² in addition to the coefficient uncertainty 161εη. Since ε=η² and (111²/2)η<1, |p−1−iεP0/2|≤162εη. Integration over a segment of length≤3 gives G(v)=v−iεd(v)+R(v), |R|≤486εη. The entire disk has |d'|≤55. Substituting V into G(V)=t and using the straight segment from t to V, which remains within the disk, contributes ≤55·333ε². The resulting inverse error is |V−t−iεd(t)|≤487εη.

For inverse-square-root expansion, the complex integral Taylor remainder is valid on the segment from 0 to x. Its second derivative is bounded by (3/4)(4/3)^(5/2)<4 on |x|≤1/4; thus the remainder is ≤2|x|². The coefficient uncertainty costs 161εη, the quadratic term 24642ε², and replacing P0(V) by P0(t), with |P0'|≤126, costs (126·333/2)ε²=20979ε². Their ε² cost totals 45621ε²<εη. Hence |V'−1−iεd'(t)|≤162εη.

Write these two errors RV and RV'. Multiplying before division gives the exact cancellation

    V(Z−1−iεq)=tRV'−RV−iεq(V−t).

For 1≤t≤T, |V|>1/2 and |q|<7. The error is at most 2(T·162+487)εη+2·7·333ε²=1541εη+4662ε²<2000εη. No central uncertainty is lost in division. All absorptions are exact rational inequalities at η=10^-12, independently checked in the supplied code.

## 6. The three target quantities and boundary cases

Exact endpoint values q(1)=3/5 and q(T)=−441/640, with 2000η=2·10^-9, imply Im Z(1)>ε/2 and Im Z(T)<−ε/2. For a continuous polar argument lift, θ'=Im(W'/W)=−2Im Z/t. Thus its derivative takes both signs at regular points of the actual omitted arc and θ is not monotone. A principal-argument branch jump is neither used nor needed.

The signed outward angle is β=arg((-W')/W)=arg Z. Uniform orientation fixes its continuous branch in the right half-plane. V(t)=a^-1/2 t+O(t³) implies Z→1 and β→0 as t↓0. β is positive at 1 and negative at T. A nonincreasing function with initial limit zero cannot take the positive value; a nondecreasing one cannot take the negative value. Therefore β is nonmonotone on the actual slit. Continuity supplies an interior zero between the two nonzero endpoints; |β| has two positive endpoint values and an interior zero, so is nonmonotone even on that compact arc. Reversing the tangent gives the ordinary supplement π−|β|, which is also nonmonotone. The acute tangent-line convention gives |β| because |β| is very small.

At ε=0, the strict sign bounds vanish and the reference trajectory is a Koebe ray; the limiting case does not contradict the theorem. Complex a2,a3 are permitted throughout every disk-wide uncertainty bound. The theorem does not assert uniqueness or an explicit maximizing function. The argument excludes branch zeros, finite-pole problems on the tested segment, and passing the actual tip. These are analytic exclusions; floating-point resolution of an angle of size 10^-24 is unnecessary.

## 7. Brown actual-support tangent-waver nonimplication

The audit-only Brown construction is independently support-realizable. Brown1979 pp374–376 determines the actual global point-evaluation maximizer with B=f(z0), angle θ0 satisfying θ0+R sinθ0=arg z0, and |B|=r exp(R cosθ0)/(1−r²), R=log((1+r)/(1−r)). For r=tanh(1/4), R=1/2, θ0=π/2+δ, δ=10^-12, choose χ=θ0+(1/2)sinθ0 and z0=r exp(iχ). The θ-map has derivative≥1/2, so the specified θ0 is its unique solution. Also 0<χ<π. The exact identity r/(1−r²)=(1/2)sinh(1/2) yields |B|≥(25/96)(1−δ/2)>1/4.

With E=exp(−iθ0/2), W(s)=−B csch²(sE) is Brown's trajectory after reparametrizing his spiral towards infinity. Independently Q=B²/[w²(B−w)] and W'/W=−2E coth(sE) give Q(W)W'²=4BE²=4|B|>0. The actual tip has radius≤1 by applying Schwarz to the inverse of an inscribed disk about f(0)=0. For 0<s≤10^-5, |W|>(1−10^-5)²/[4(10^-5)²]>1. The same unique-infinity-germ and local continuation argument therefore places both sign points on the actual Γ before its tip.

On |u|≤1/2, the elementary hyperbolic series bound both |sinh(u)/u−1| and |cosh u−1| by 1/3. Thus no relevant nonzero denominator vanishes there. The tangent-log derivative is

    φ'(s)=Im{E[−3coth(sE)+tanh(sE)]}.

Independently dividing the series gives h(u)=3−3u coth u+u tanh u=−4u⁴/15+8u⁶/63+O(u⁸). The same disk bounds give |u coth u|≤2, |u tanh u|≤1/2 and |h|≤19/2<10. Cauchy's estimate bounds coefficients by 10·2^n, so the omitted tail divided by u is ≤2560s⁷/(1−2s). Using E^4=exp(−2iθ0), E^6=exp(−3iθ0),

    φ'(s)/s³=−(4/15)sin(2δ)+(8/63)cos(3δ)s²+e(s),
    |e(s)|≤2560s⁴/(1−2s).

The rational sine/cosine bounds yield a negative upper bound at s=10^-7 and a positive lower bound at s=10^-5; my fresh series division and exact margin controls reproduce them. Outward tangent −W' differs by a constant argument π and has the same derivative. Brown's Theorems1–2 simultaneously give monotone polar argument and monotone nonnegative radial angle A=arg(w/w'); the signed outward angle is −A and is monotone too. Thus even an actual S-support tangent waver does not logically imply either target failure.

This is an implication counterexample, not a comparison of Zemyan's unread construction. It does not establish which family he used, whether he included additional polar/radial conclusions, or whether his later papers imply the target by another route.

## 8. H1996 and Friedland–Schiffer implications independently checked

I read all seven H1996 extracted pages and inspected the critical original pages. Its two-evaluation functional J=h(ζ1)+h(ζ2) has Φ=a²/(a−w)+b²/(b−w). The Koebe-rotation expansion is a+b+2ct+c²(1/a+1/b)t²+c³(1/a²+1/b²)t³+…, confirming the missing printed factor2 and the follow-up's degenerate-case repair: when a+b=0, the next odd coefficient forces a² real, giving real or pure-imaginary conjugate a,b. A zero-J pair b=−a gives Q=−2a²/[w(w−a)(w+a)], as in the source. On the unit circle (z−u)²/(zu)=−|1−z/u|² confirms the follow-up's corrected boundary sign. These repairs do not yield an angle reversal.

For p=(11−4sqrt7)/3, 3p²−22p+3=0 gives k(p)=3/16 and k(−1/3)=−3/16. Both point evaluations have unique Koebe maximizers by Brown's inspected interval theorem; summing proves genuine J-extremality with J(k)=0. The coalesced choice ζ1=ζ2=−3/4 reduces to twice Brown's point evaluation, and supplies non-Koebe/conjugate nonuniqueness with both target monotonicities. For a straight outward half-line w=u(x+iy), x'=1 and x>0, θ'=−y/(x²+y²), β'=y/(x²+y²), and |β|'=−|y|/(x²+y²); the signs are fixed. H1996's rational-line conclusion is therefore positive geometry. Its undetermined cases and analytically continued trajectory conjecture do not identify an actual on-slit target reversal. This does not classify every member of the two-evaluation family.

I independently checked the critical Friedland–Schiffer primary pages139–140,149–152,156–157 and164–165, alongside the sealed complete44-page follow-up. Corollary4.2 is an actual global degree-four coefficient inequality with weights λ4=x², λ3=6x(1−x), λ2=2(7x²−12x+5). Koebe saturates the bound 14x²−30x+20; λ2 is negative for 5/7<x<1, so this is substantive mixed-coefficient work. The ratio λ3²/(λ2λ4), when defined, is real and is invariant under normalized rotation and common complex scaling. The candidate ratio is 9iε. This excludes exact functional identity with the explicit family, including rotated forms and zero-weight endpoints. It does not classify shared support points or all instances of the paper's general machinery.

The source's power-matrix formula Av=Σ(∂F/∂ak)[z^k]f^v with F=Re L gives Av=L(f^v)/2 under ordinary Wirtinger derivatives. Therefore its exterior differential is −Q_candidate/2, and its nonpositive convention is compatible with the positive one here. This is real classical-method overlap, correctly credited in the revised manuscript. On p139 the supporting set is distinguished from the full coefficient-body boundary; p140's Teichmüller extremality fixes the lower coefficients. Theorem5.1 contains nonlinear endpoint conditions involving the unknown extremizer coefficients. Its equivalence does not solve this mixed complex instance or establish any angle sign. Treating it as a prior negative solution without that solved instance would transfer the central difficulty to an equivalent unsupported claim. Theorem5.4's local coefficient-modulus estimate concerns changing functions near Koebe, not the radius/tangent angles on an actual omitted arc. These source-specific checks support the follow-up's limited implications, without pretending to have independently reproved all44pages or clearing uninspected literature.

The strongest result remains the verified constructive theorem within its stated classical premises. Historical firstness and global novelty/publication clearance remain separate and unclosed.
