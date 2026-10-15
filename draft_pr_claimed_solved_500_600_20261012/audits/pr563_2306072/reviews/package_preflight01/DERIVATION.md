# Independent derivation and falsification record

This derivation was begun from the frozen manuscript, archived original proof and primary problem, before reading the prior component verdicts. It assesses the exact statement about every global maximizer of Re[a2+i·10^-24(a4−3a3)]. Classical analytic results remain stated inputs; this is an independent mathematical review, not a formal proof certification or a novelty decision.

## 1. Exact domain and hypotheses

S consists of normalized analytic injective maps of the open unit disk, with the topology of locally uniform convergence. Normal-family compactness and preservation of injectivity under a nonconstant normalized limit give compact S. Coefficient extraction is a continuous complex-linear map on H(D), by Cauchy's integral formula. Therefore L is continuous and has an attained real maximum. Koebe k has L(k)=2−5iε; the identity has L(z)=0. The real part is nonconstant, so each maximizer falls under the support-point theorem. This is a global extremal argument and assumes neither a solver nor a unique extremizer.

For Pfluger's formulation (1971 introduction (3)–(5)), the finite Laurent kernel is K(z)=z^-3+iε(z^-5−3z^-4). Its only singularity is at zero and it is holomorphic outside any sufficiently small circle. Thus it is an instance of the permitted functional, with nontrivial real part on S. No real-coefficient, subclass, rational-extremizer or additional uniqueness hypothesis is introduced.

## 2. Coefficients and the odd root

For each actual maximizer, Re a2−ε Im(a4−3a3)≥2. The coefficient bounds through n=4 give |a4−3a3|≤13. Hence Re a2≥2−13ε. Since |a2|≤2,

|a2−2|²=|a2|²−4 Re a2+4≤52ε,

and 0≤1−|a2|²/4≤13ε, using Re a2>0. In particular |a2−2|<8η, where η²=ε.

The holomorphic root exists because f(z)/z extends holomorphically, is nonzero on D, and has value 1 at zero. One can write g(z)=z sqrt[f(z²)/z²] with normalized root; g is odd. If g(z1)=g(z2), injectivity of f forces z1²=z2². The negative pair would have opposite g-values, so equality forces g=0 and z1=z2=0. Thus g is univalent. Inversion yields the normalized exterior map

1/g(1/ζ)=ζ−(a2/2)ζ^-1+(3a2²/8−a3/2)ζ^-3+… .

The exterior area theorem applies because inversion has no pole in |ζ|>1: g has no zero there except at the excluded interior coordinate zero. It gives |a3−3a2²/4|≤2 sqrt(13/3)η<5η. Also |a2²−4|≤4|a2−2|, so |a3−3|<29η. Setting A=2a3+a2²−6a2 and B=3a2−3 gives |A+2|<106η and |B−3|<24η. All these estimates are uniform across all maximizers.

## 3. The actual tip gate

H=sqrt(z/f(z)) is analytic and nonzero on D, normalized by H(0)=1. The same exterior map is ζH(ζ^-2), giving sum_{n≥2}(2n−1)|c_n|²≤13ε. Weighted Cauchy–Schwarz on |z|≤2/3 gives the two explicit bounds

sum r^(2n)/(2n−1)≤16/135<1/4,

sum n²r^(2n−2)/(2n−1)≤56/25<9/4.

The coefficient of z contributes at most 4ηr to H−(1−z) and 4η to its derivative; sqrt(13)<4 supplies the remaining costs. Consequently |H−H0|<5η and |H′−H0′|<10η. At z*=−2/3, H0=5/3, so 3/2<|H|<11/6 and |H+H0|<7/2. The stronger upper bound is necessary for the latter numerator, and the revised manuscript explicitly supplies it.

Using f=z/H² and f′=(H−2zH′)/H³, the value cost is less than (2/3)(14/5)η<2η. The derivative numerator cost is less than (5+40/3)η<19η; division by |H|³>27/8 costs less than 6η. The reciprocal-cube cost is at most (1/3)(5·11)/(125/8)η<2η. Thus |f(z*)−k(z*)|<2η and |f′(z*)−k′(z*)|<8η.

The correct conformal-radius direction is dist(f(z),∂Ω)≤(1−|z|²)|f′(z)|. For a disk of radius d contained in Ω about f(z), compose f with the disk automorphism taking 0 to z; its inverse on that disk, scaled to D, has derivative d/[(1−|z|²)|f′(z)|]. Schwarz's lemma bounds it by 1. Let d tend to the boundary distance. This is the upper bound needed here; replacing it by a Koebe lower bound would not justify a tip estimate.

The omitted set Γ=C\f(D) is closed and nonempty. Its distance from f(z*) is attained at a finite boundary point, or equivalently can be approached by a minimizing sequence. Triangle inequality gives min_Γ|w|≤|f(z*)|+dist(f(z*),∂Ω). Since k(z*)=−6/25 and k′(z*)=9/125, the resulting bound is 7/25+(58/9)η<7/25+7η<3/10. Classical increasing-modulus geometry identifies this minimum as the actual finite tip. No continuity of tips with ε has been assumed.

## 4. Exact source sign and natural coordinate

Duren1981 p352 has Φ(w)dw²/w²>0 and Φ=L(f²/(f−w)). Pfluger1971 (50) p23 gives L(f_w)−L(f)=w²Q_P(w), where f_w=wf/(w−f). But f−f_w=f²/(f−w), so Q_D=Φ/w²=−Q_P. Pfluger's negative trajectory condition in §4.1 and Satz5 therefore describes the same arc. His §4.5 gives increasing modulus. This reconciles the sign rather than treating either sign as arbitrary. At ε=0, Q_D=−w^-3 is positive on the negative Koebe ray and negative on the positive ray, an immediate independent sign control.

Direct coefficient division gives [z²]=−1/w, [z³]=−2a2/w−1/w², [z⁴]=−(2a3+a2²)/w−3a2/w²−1/w³. Therefore

Q_D=−a/w³−b/w⁴−c/w⁵,

a=1+iεA, b=iεB, c=iε.

Under w=−v^-2, dw=2v^-3dv, and Q dw²=4(a−bv²+cv⁴)dv². The plus double-cover sign would give the wrong trajectory condition. Also u=1/w transforms Q dw² to (−a/u−b−cu)du²: the pole at infinity is simple and a≠0 by the coefficient estimate.

On |v|≤3, |P−1−iεP0|≤322εη, P0=−2−3v²+v⁴, |P0|≤110, and |P−1|≤111ε. Thus P is nonzero on a neighbourhood of this closed disk. Its unique analytic square root p near 1 has positive real part and |p−1|≤111ε, since |p+1|≥1. The primitive G(v)=∫p has |G−v|≤333ε.

On |v|=3 and |t|<2, |v−t|>1>333ε. Rouché gives exactly one root of G(v)=t; G′=p≠0 makes the inverse local and holomorphic. The uniqueness makes these inverses patch to V on the entire |t|<2. No pointwise numerical inverse is substituted. G is odd because p is even; V is odd. The inverse bound is |V−t|≤333ε and V′=1/p(V).

## 5. Actual-slit identification: the central obligation

For 0<t≤7/4, W=−V^-2 is regular, satisfies Q(W)W′²=4, and tends to infinity as −a/t². V(t) cannot vanish at a nonzero t because G(V)=t. Equality W(t1)=W(t2) forces V(t1)=±V(t2); applying odd G gives t1=±t2, so the positive segment has no self-intersection.

The actual support slit, supplied by the classical theorem for the actual maximizer, has a distant tail tending to infinity. Its continuous double-cover lift approaches v=0. Positivity of 4p(v)²dv² makes Im G constant along that tail, and the limit at zero forces that constant to be zero. The sign of its nonzero real G-value is fixed on a sufficiently distant tail. The positive and negative real inverse rays project to the same W-arc by oddness. Thus W lies on Γ near infinity. This is a deduction about Γ; it is not a converse sufficient condition for an arbitrary trajectory to be extremal.

Every W-point on this segment has |V|<9/5, hence |W|>25/81. The actual tip has radius <3/10, leaving the strict gap 25/81−3/10=7/810. Let E={t∈(0,7/4]:W(t)∈Γ}. It is nonempty and relatively closed by closedness of Γ. At a member, the point is neither the actual finite tip nor a zero/pole of Q. A local square-root primitive of nonzero Q maps positive trajectories to horizontal intervals, so the actual analytic arc and W coincide locally. E is relatively open, including at the selected endpoint 7/4. Connectedness gives E equal to the whole interval. Local continuation also makes the two selected points interior regular points of Γ. Neither universal tip continuity nor a characterization of maximizing trajectories has replaced this argument.

The radial orientation is independently fixed for ALL positive t in the interval, not merely at sign points. Let Z=tV′/V= [G(V)/V]/p(V). The radial-segment average gives |G(V)/V−1|≤111ε. Thus |Z−1|≤222ε/(1−111ε)<223ε and Re Z>0. Consequently d log|W|/dt=−2 Re Z/t<0; t increases inward and −W′ points outward.

## 6. Uniform analytic errors and angles

The square-root identity sqrt(1+x)−1−x/2=−x²/[2(sqrt(1+x)+1)²] on the selected branch bounds the remainder by |x|²/2. Coefficient uncertainty contributes 161εη and the square-root Taylor term (111²/2)ε², less in total than 162εη. Integrating on |v|≤3 gives G=v−iεd+R with |R|≤486εη, where d=v+v³/2−v⁵/10.

Because |d′|≤55 on the convex |v|≤3 disk and |V−t|≤333ε, evaluating d(V) instead of d(t) costs ≤18315ε². This proves |V−t−iεd(t)|≤487εη uniformly. For V′, the inverse-square-root second derivative is (3/4)(1+x)^-5/2. On |x|≤1/4 it has modulus <4, so Taylor's integral remainder is ≤2|x|². The uncertainty cost is 161εη, the quadratic cost 24642ε², and the replacement of P0(V) by P0(t), using |P0′|≤126 on the same convex disk, costs 20979ε². Their total is <162εη. Each ε²/εη ratio is η, not ε; the manuscript's absorptions use the correct scale.

Subtract before division: V[Z−1−iεq]=tR_{V′}−R_V−iεq(V−t), with q=d′−d/t=t²−2t⁴/5. For 1≤t≤7/4, |V|>1/2 and |q|<7; the error is ≤1541εη+4662ε²<2000εη. A fresh propagation using the actual denominator 1−333ε produces a tighter multiplier <800, independently checked in the supplemental file. The claimed conservative bound is therefore safe.

Exactly q(1)=3/5 and q(7/4)=−441/640. The relative error 2000η=2·10^-9 is much smaller than either margin to ±1/2. Hence Im Z(1)>ε/2 and Im Z(7/4)<−ε/2. Finite fraction arithmetic checks the constants; the disk estimates and holomorphic deductions above justify their universal applicability.

For any continuous polar lift θ, θ′=−2 Im Z/t. Its opposite nonzero derivative signs at two actual regular slit points rule out either monotone direction. For the outward radial angle, (−W′)/W=(2/t)Z. Since Re Z>0, β=arg Z has one unambiguous continuous branch in (−π/2,π/2). V(t)=a^-1/2 t+O(t³) implies β→0 at infinity. β is positive at 1 and negative at 7/4; with the initial zero limit this excludes either monotone direction. A β-zero between them gives a strict interior minimum of |β| between positive endpoint values, ruling out unsigned monotonicity even on the compact subarc. Ordinary inward vector angle is π−|β| and the acute tangent-line angle is |β|, so neither convention rescues monotonicity. Neither angle at the finite tip nor any undefined tangent at infinity is needed.

At ε=0 these strict signs vanish; the Koebe control is consistent. For ε<0 the complex-conjugation correspondence mirrors the geometry. The arithmetic controls also survive η=1/50000, showing that 10^-24 is comfortably inside a sufficient positive parameter regime; this consistency check is not an amendment of the manuscript's exact theorem. Double precision cannot resolve the chosen angle scale and is not evidence for it.

An additional independent formal check at A=−2,B=3 gives G=v−iεd+ε²e+O(ε³), with e=∫P0²/8. Reversion yields V=t+iεd+ε²h+O(ε³), h=−d′d−e. Expanding Z gives ε² coefficient h′−h/t+(d/t)d′−(d/t)², which is real. The exact polynomials in INDEPENDENT_CONTROLS.json confirm the first-order imaginary q and check the second-order origin coefficient h′(0)=−3/2. These formal checks explain the signs but do not replace the analytic remainders.

## 7. Independent Brown actual-support waver bridge

Brown1979 pp374–375 (9)–(11) identify B=f(z0) for the actual maximizing point-evaluation support point. With R=1/2, r=tanh(1/4), θ0=π/2+δ and χ=θ0+R sinθ0, z0=r exp(iχ) lies in the upper disk. The map θ↦θ+R sinθ has derivative ≥1−R=1/2 on [0,π], so the chosen θ0 is the unique prescribed solution. Taking real parts of Brown (9) gives |B|=r/(1−r²) exp(R cosθ0)=(1/2)sinh(1/2)exp(−sinδ/2). Thus |B|≥(25/96)(1−δ/2)>1/4. Point evaluation at nonzero z0 has nonconstant real part on S (vary a small rotated Koebe parameter), and compactness supplies the actual maximizer before any trajectory calculation.

Brown p376 (12)–(16) gives W(s)=−B csch²(sE), E=exp(−iθ0/2), by reparametrizing his logarithmic spiral near infinity. Direct calculation with Q=B²/[w²(B−w)] yields W′/W=−2E coth(sE), B−W=B coth²(sE), and Q(W)W′²=4BE²=4|B|>0. Its asymptote −B/(s²E²)=−B²/(|B|s²) has the correct Brown half-line direction.

For |u|≤1/2, the sinh/u and cosh tail bounds ≤1/3 make sinh/u and cosh nonzero. This validates the log derivative and analyticity throughout the chosen small segment. The same Schwarz inverse argument at f(0)=0 gives actual tip radius≤1. Meanwhile |sinh(sE)|≤s exp(s)≤s/(1−s), so |W|>(1−10^-5)²/[4(10^-5)²]=9999800001/4>1. Infinity-germ uniqueness and the same open/closed continuation therefore put BOTH sign points on the actual omitted support slit. No arbitrary support-realizability assertion is used.

For φ=arg W′, φ′=Im{E[−3coth(sE)+tanh(sE)]}. The outward tangent −W′ adds a constant π. Set h(u)=3−3u coth u+u tanh u. Independent exact division through degree 12 gives

h=−4u⁴/15+8u⁶/63−4u⁸/75+136u¹⁰/6237−171368u¹²/19348875+… .

On |u|=1/2, |u coth u|≤2, |u tanh u|≤1/2, hence |h|≤19/2<10. Cauchy gives |c_n|≤10·2^n and the n≥8 tail divided by u is ≤2560s⁷/(1−2s). The singular −3/s term is real, while Im E⁴=sin2δ and Im E⁶=cos3δ for this θ0. Consequently

φ′(s)/s³=−(4/15)sin2δ+(8/63)cos3δ·s²+error,

|error|≤2560s⁴/(1−2s).

Exact sine/cosine Taylor inequalities give a negative upper bound at 10^-7 and a positive lower bound at 10^-5. Both are recorded in the independent controls. This is a genuine tangent waver. Brown pp375/380 Theorems1–2 nevertheless prove monotone polar argument and positive outward A=arg(w/w′), so signed β=−A and |β| are monotone. Orientation reversal in s preserves monotonicity and only reverses its direction.

This actual-support example disproves the logical implication “tangent waver implies either target counterexample.” It does NOT prove that Zemyan's unread construction is Brown's example, lacks additional results, or fails to answer the target questions. Exact primary fulltext comparison remains required.

## 8. Falsification boundaries

Dropping the quartic term removes this q sign reversal; using w=+v^-2 makes the selected real curve a negative trajectory; allowing a tip bound beyond 25/81 destroys the actual-slit continuation certificate; ε=0 destroys strict signs; sufficiently large coefficient uncertainty destroys the sign margins. These are meaningful failures of the mechanism. The supplemental finite checks are not proof of compactness, the area theorem, de Branges, Pfluger's entire proof, or universal analytic continuation. The strongest reviewed conclusion is the exact stated theorem under the applicable classical inputs, with no required mathematical repair found. Publication and priority remain separately held.
