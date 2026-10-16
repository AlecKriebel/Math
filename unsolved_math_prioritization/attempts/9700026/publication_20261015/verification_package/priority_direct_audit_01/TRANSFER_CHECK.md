# Exact transfer from Ferudun's current two-city result

Audited 15 October 2026. This is a priority implication check, not a new central proof attempt.

The primary reading is Alper Ferudun, *On Conjecture 1 of Aldous for a Spatial Model of City Growth: A Proof of Part (a), and Counterexamples to Parts (b) and (c) for 2α/√3 < β < 2α*, EulerSolve AMR-096-0023, version 1.0, dated 14 October 2026, [paper page](https://eulersolve.org/papers/amr-096-0023/), [PDF](https://eulersolve.org/papers/amr-096-0023/paper.pdf?v=319a8f49e0c4). The PDF SHA-256 is `319a8f49e0c4de0247e76da33f6476d4085e21267002ee02484f73cee6992e5a`.

## Same vector field

For two fixed sites and positive normalized weights `(z,1-z)`, its section 4 defines

`f_x(z) = area{y in [0,1]^2 : |y-x_1| <= (z/(1-z))^(α/β)|y-x_2|}`.

This is exactly `A_1(z,1-z)` of the frozen proof and of Aldous's 2007 section 6.4, with `A_2=1-f_x`. Hence the displayed frozen ODE becomes `z'=f_x(z)-z`. There is no stochastic approximation or change of time in this identity. No assertion about the stochastic city-founding process is needed below.

## Independent check of the geometric ingredients

Write `k=2α/β` and use centered sites `(-a,0),(a,0)` in the centered unit square. For `z=1/2+h`, let `σ=(z/(1-z))^(k/2)`, `c=(σ²+1)/(σ²-1)`. The left boundary of the complement of city 1's cell at height `u` is

`ψ(u)=ac-sqrt(a²c²-a²-u²)=(a²+u²)/(ac+sqrt(a²c²-a²-u²))`.

For sufficiently small positive `h`, the disc intersects every horizontal line across the square exactly as used in the source. Thus `f(1/2+h)-1/2=∫[-1/2,1/2]ψ(u)du`. Since `c^-1=tanh(k artanh(2h))=2kh+O(h³)`, expansion gives the slope `k(a+1/(12a))`. This confirms the source's Lemma 4.1(iii), including its exponent and factors. The interval estimate in Lemma 4.1(ii) follows by the stated lower bound on the square root and `tanh(kv)<=k tanh(v)` for `k>=1`. This last condition is why its proved quantitative strip result has `k>=1`.

The position-perturbation estimate in Lemma 4.3 is also checkable directly: outside radius-`r` discs around the two reference sites, moving each site by at most `ρ` changes its distance by multiplicative factors between `1-ρ/r` and `1+ρ/r`. The excluded set has area at most `2πr²`. Its upper and lower area inclusions therefore hold uniformly over all positive `σ`.

The resulting Corollary 4.4 has `η>0` and

`f_x(z)-z <= -η` for `z in [1/2+δ/2,1/2+δ]`,

`f_x(z)-z >= η` for `z in [1/2-δ,1/2-δ/2]`,

uniformly for site pairs in an open product of two small discs. I checked the proof on printed pages 8-9 and the explicit constants on page 10. These strict strips give a barrier for **every** solution beginning in the central closed interval: a differentiable trajectory exiting upwards would have to increase while crossing the upper strip where its derivative is strictly negative; the lower case is reversed. Continuity supplies local existence, and staying in a compact positive interval allows global continuation. Uniqueness is unnecessary for this noncollapse conclusion. The two coordinates stay in `[1/2-δ,1/2+δ]`, so neither tends to one. The open set of site positions and open initial interval cannot be excluded by an ordinary genericity qualification.

Section 8, printed page 13, explicitly makes this deterministic transfer and names Conjecture 32(a). This is not merely an implication noticed by this audit.

## Checkable numerical instance from the source

Use `α=2`, `β=3`, `k=4/3`, `a=1/4`, `δ=1/20`, `r=1/100`, `ρ=1/100000`. The reference sites are `(1/4,1/2)` and `(3/4,1/2)`. Then

`q_a(h)=(7/9)/(1-(160/9)h²)`, `h_a=3/20`, `q_a(2δ)=35/37<1`,

`ε=(3/4) artanh(1/1000)`,

`η=(δ/2)(1-q_a(δ+ε))-ε-2πr² > 0.0032441`.

The included checker verifies a rational lower bound for `η`, using `x+x³/3 <= artanh(x) <= x+x³/[3(1-x²)]` and the classical bound `π<355/113`. It does not use quadrature, simulation, downloaded code, or source self-verification reports. The preserved explicit constants yield the invariant interval `[9/20,11/20]` for all site pairs within the stated small discs. This provides a concrete current counterexample at a point in the original `β<2α` alternative. Section 8 also includes the line `β=2α, α>1` through `k=1`.

## Same-regime qualitative consequence of the proved lemmas

The source labels its explicit quantitative-strip extension to `k<1` as an unwritten sketch. **That label does not prevent a qualitative same-regime transfer from the lemmas already proved.** Lemma 4.1(iii) is explicitly valid for every `k>0`. With `a=1/4` it gives `f'_(x0)(1/2)=7k/12`. Thus when `β>2α`, so `0<k<1`, the scalar drift `g=f-z` has `g(1/2)=0` and derivative `7k/12-1<0`. By differentiability, for all sufficiently small positive `δ`, `g(1/2-δ)>0` and `g(1/2+δ)<0`.

The area map is jointly continuous in distinct site positions and positive weights: pairwise ties are a line or circle of zero area, so dominated convergence applies to its indicator. Alternatively, the source's Lemma 4.3 supplies the required position control. Therefore these two strict endpoint signs persist for all site pairs in a sufficiently small open neighborhood of the reference pair. The same scalar barrier argument makes `[1/2-δ,1/2+δ]` forward invariant for every initial share there and every such site pair. This is a generic two-city noncollapse counterexample in **the same** `α>1, β>2α` region as the frozen theorem. It uses only the already proved derivative and continuity lemmas, and does not require carrying out the sketched quantitative bound or any stochastic theorem.

The exact source and derivative calculation were located and read independently before this stronger transfer was checked. The implication above was independently re-derived in adversarial reassessment. A previous inference that the sketch label ruled out a same-regime proved overlap was too weak and is superseded.

## Exact nontransfer

Both versions of the source-based argument are two-city and local in sites and initial weights. They are not the theorem that **every** finite distinct interior-site configuration and **every** positive initial vector has all-coordinate uniform persistence when `β>2α`. They do not supply the candidate's all-coordinate configuration-dependent lower bound or its explicit time-dependent integrating-factor estimate. The separate ratio-invariance observation shows incompatible conjectural predictions, rather than giving these bounds. The stochastic Theorems A-D are outside this check's scope and are not certified here.
