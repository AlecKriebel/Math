# Second-batch geometry and analysis triage

Checkpoint: 2026-10-06 PDT. Triage completion estimate 95%; this is a research agenda assuming upstream theorem correctness, not independent verification of those theorems. No external individuals contacted.

## 1. K-moduli equals GIT moduli for cubic hypersurfaces in every dimension

**Target:** For every complex dimension n>=5, identify the K-moduli compactification of smooth cubic hypersurfaces in P^(n+1) with their classical GIT compactification. State the corresponding K-(semi/poly)stability versus GIT (semi/poly)stability equivalence only after checking the moduli theorem's exact scheme/stack and stability scope. At a minimum, obtain the KE/K-polystable compactification identification and existence of KE metrics on all smooth cubics. Dimensions <=4 are already known and should be background, not novelty.

**Input:** #037, `The-ordinary-double-point-gap-in-every-dimension-September-24-2026/build/sections/01-introduction.tex`, Theorem main, lines 35–48. Any singular boundary-zero complex algebraic klt n-fold germ has normalized volume <=2(n−1)^n, all n>=2; equality iff analytic ODP. Do not use the already-written global-volume Corollary as a new result: that corollary, including the second-largest global-volume classification, is already explicitly in the source.

**Mechanism and exact remaining work:** Spotti–Sun, *Explicit Gromov–Hausdorff compactifications...*, Theorem 1.3(2), explicitly deduces cubic K/KE-moduli=GIT from the ODP metric cone density gap in all dimensions k<=n. https://arxiv.org/html/1705.00377 . Match normalized volume to Ricci-flat cone volume density, via nvol/n^n; this bridge is standard Li–Liu/Li–Xu and is explained in the new input introduction. The new algebraic theorem is unrestricted and therefore supplies the required cone cases. Audit the existing theorem chain, update the interpretation to modern K-moduli language, and check semistable/nonclosed-point assertions. This is a short, concrete theorem-chain project, no new central inequality.

**Priority evidence:** https://arxiv.org/abs/2007.14320 establishes cubic fourfolds. The 2025 primary paper https://api.algebraicgeometry.nl/Article/21043/2025-3-011.pdf explicitly states that K-polystable limits of cubics remaining cubics is conjectural in general, known through dimension 4. Recent https://arxiv.org/abs/2510.14352 addresses canonical singularities of GIT semistable cubics, not full K/GIT agreement; do not claim that canonical-singularity assertion is new.

**Duplication audit:** No occurrence of `cubic` in the new all-dimensional ODP source. Corpus-wide focused searches for cubic within 50 characters of moduli/stability found only the distinct irrational-cubic/K3 work; no cubic K-moduli theorem was found. The source cites Spotti–Sun only in history; this is an obvious literature-derived application, so credit belongs to both upstream proofs and the established reduction.

**Impact:** 8.8; tractability very high. Strongest candidate from this scan. Publication priority is provisional.

## 2. Pointwise bilinear ergodic Hilbert convergence for arbitrary commuting actions

**Safest exact target:** Let S^t,T^t be the two commuting measure-preserving flows of a jointly measurable R^2-action on a probability space. For f,g in L^3 and r>2 prove an L^(3/2) bound for full annular r-variation of

H_(a,b)(f,g)(x)=integral_(a<|t|<b) f(S^t x) g(T^t x) dt/t.

Deduce joint a.e. and L^(3/2) principal-value convergence as a->0 and b->infinity. The discrete companion target for arbitrary commuting invertible S,T is convergence and r-variation of sum_(0<|n|<=N) f(S^n x)g(T^n x)/n.

**Input:** #082, `Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026/build/sections/introduction.tex`, equations bilinear-truncation/variation-definition and Theorem variation, lines 3–34. The norm is L3(R2)xL3(R2)->L3/2(R2). Crucially the supremum is inside the norm, partitions depend on the output point, and all positive scales are allowed.

**Mechanism:** Apply finite-window Calderón transference to F_x(u,v)=f(S^uT^v x), G_x(u,v)=g(S^uT^v x); at point (u,v), shifting the first coordinate of F and the second of G is the desired commuting bilinear orbit integral. Let the window size tend to infinity after taking a fixed finite annular family, then use monotone convergence over rational families. Finite r-variation forces a Cauchy limit at each endpoint and the maximal bound supplies dominated norm convergence. There is no need for a difficult dense-subclass convergence argument once genuine pointwise variation is transferred. For the discrete statement, give a careful continuous-to-discrete transference/step-function lemma with an absolutely summable 1/n^2 kernel error; this has not yet been written and should be explicit. Continuous actions alone are already an exact immediate theorem.

**Boundary:** DO NOT state that this by itself proves ordinary one-sided Cesàro averages (1/N)sum f(S^n x)g(T^n x) converge. Odd Hilbert annuli do not automatically control even averaging kernels. A varying-frequency modulation conversion would need a new argument. Do not claim arbitrary noncommuting actions or arbitrary multiple averages.

**Literature:** Demeter https://arxiv.org/abs/math/0601277 proves bilinear ergodic Hilbert convergence for powers of one transformation, not arbitrary commuting generators. Durcik–Kovač–Škreb–Thiele's *Norm variation of ergodic averages with respect to two commuting transformations* gives norm variation, not pointwise-supremum variation. A useful primary transference reference is Blasco–Carro–Gillespie https://www.uv.es/~oblasco/Investigacion/BO/BCG.pdf and Berkson–Blasco–Carro–Gillespie https://www.uv.es/oblasco/Investigacion/BO/BBCG.pdf; their exact multi-parameter vector-variation adaptation remains a check. The recent https://arxiv.org/abs/2603.20173 deals with shifted bilinear transforms and needs a final scope/priority check before publication.

**Duplication audit:** #082 manuscripts mention commuting transformations only as motivation in introductions; no ergodic transference theorem or ergodic Hilbert statement is in their conclusions. Corpus catalogue #154 concerns mixing transformations and ordinary multiple averages, so it is distinct.

**Impact:** 8.0–8.5 for arbitrary commuting discrete actions with quantitative variation; 7.8 for continuous-only clean corollary. Tractability high for continuous, moderately high for discrete after discretization verification. Do not market the more famous unresolved ordinary-average statement as solved.

## 3. Lower-priority reserve: nef-tangent compact Kähler structure in Albanese relative dimension <=6

#067 proves Fano sixfolds with nef tangent are rational homogeneous. Together with known dimensions <=5 and Demailly–Peternell–Schneider's structure theorem, every compact Kähler manifold with nef tangent bundle whose maximal-irregularity finite étale cover has Albanese relative dimension <=6 has homogeneous Fano fibers. Rigidity of G/P and Fischer–Grauert then make this a holomorphically locally trivial G/P-bundle over a torus. This includes all total dimensions <=6 but also higher total dimension with small Albanese fibers. The DPS theorem is summarized by primary authors in https://arxiv.org/abs/1101.4192 and https://www-fourier.ujf-grenoble.fr/~demailly/manuscripts/tifr.pdf . Need final source duplication and local-triviality check; do not assert global product or flat monodromy without proof. Impact ~7.2, very short standard corollary, probably less valuable than other agents' top candidates.

## Rejected shortcuts

Fujita freeness does not establish sharp very ampleness or relative pluricanonical generation without new hypotheses. Nagata does not solve SHGH. Mahler does not settle arbitrary Lagrangian-product Viterbo. The #037 singular global anticanonical volume bound and global second-largest-volume classification are already in the input and must not be recycled as new. Broad KLS does not follow from the simplex isotropic-constant theorem plus the subgaussian log-Sobolev theorem without overcoming non-subgaussian directions.

## Independent adversarial audit of #374 weighted log-concave Brenier extension

Checkpoint: 2026-10-06 PDT. Assigned reduction audit completion estimate: 100% (not a completed proof or priority clearance).

Read the entire source `moments.tex`, `cells.tex`, `finite_stability.tex`, and `gradient.tex` independently of the proposing agent. The bounded positive log-concave extension passes the main reduction checks:

- For normalized weighted restrictions to perturbed convex cells U,V, the triangular quantile diagonal products are exactly alpha/r(X) and beta/r(Z). At H=(X+Z)/2, determinant AGM and log-concavity imply r(H)prod_k dH_k/ds_k >= sqrt(alpha beta). Coordinatewise substitution with g*r therefore yields sqrt(alpha beta)Law(H)<=rho restricted to the unperturbed cell. The normalization is exact; no density-ratio factor spoils second variation.
- The source's quadratic identity with Phi=R^2−|x|^2, summation over partitions, and derivative limit then gives the identical stationary moment constant 162. No uniform density assumption remains in that algebra.
- Continuous positive r replaces 1/|K| in face integrals by r. The same weighted mass/moment face coefficients are symmetric and positive exactly on the same full faces, so connectivity and the restricted Laplacian inversion still apply. Initial smooth-density formulation is fully safe. Bounded positive log-concave r is continuous in the interior, and boundary intersections have zero face measure, suggesting the C1 argument can be extended directly; it still needs a written proof or approximation.
- Gradient interpolation is a separate fixed-function step where M/m comparison is legitimate. With m|K|<=1<=M|K|, constants can be expressed using K,Y,M/m. This does not improperly compare transport maps for different sources.
- The stronger potential statement can use the canonical normalization integral u d rho=0: finite_stability first produces coupling-dependent constants with the Lipschitz pairwise estimate. Subtracting each potential's own rho-mean applies the orthogonal projection onto mean-zero L2 to their difference, which cannot increase its norm. Thus canonical mean-zero Brenier potentials inherit the same Lipschitz W2 estimate, rather than an ill-defined pair-dependent normalization.
- Uniform sharpness over the source class is supplied by its uniform-density subclass. Sharpness for every individual nonuniform density has not been established and must not be claimed.

No new central inequality was found missing from this proposed adaptation. The remaining tasks are weighted cell calculus, density limits, finite-target limits, and literature-priority verification.

### Cubic-moduli precision addendum

The safe headline is the natural identification of the GH/KE compactification with the classical GIT compactification of cubics. Do not silently strengthen a topological identification to an isomorphism of stacks or a scheme-theoretic statement. Those may follow with modern moduli theory but require explicit argument. The complete all-dimensional K-(semi/poly)stability equivalence is the desired strengthened package to verify, rather than something to infer solely from equality of sets of closed points. Abban–Zhuang's smooth Fano index-two result does not cover all smooth cubic n-folds: a cubic n-fold has index n−1. Primary deVleming notes https://people.math.umass.edu/~devleming/research/introtokmoduli.pdf state Conjecture 4.14, GIT=K for cubic hypersurfaces, and the known n<=4 cases immediately before it.

### Discrete ergodic Hilbert transfer: explicit discretization check

The discrete transfer gap above has a concrete short resolution. Fix epsilon=1/4, and for finitely supported arrays a,b on Z^2 let F,G be constant with those array values on the squares (m,n)+[0,epsilon]^2, and zero elsewhere. At output (m+x,n+y), x,y in [0,epsilon/2], each nonzero integer k contributes a(m+k,n)b(m,n+k) times

`c_k(x,y)=integral_[k−min(x,y), k+epsilon−max(x,y)] dt/t`.

The interval has length ell=epsilon−|x−y|>=epsilon/2, and uniformly c_k/ell=1/k+O(1/k^2). Annular endpoints at half-integers include complete intervals and exclude the k=0 term. Consequently the discrete symmetric truncated Hilbert sum is the continuous truncated transform divided by ell, minus a kernel error. The full r-variation of the error is at most a constant times

`sum_(k nonzero) |k|^(-2)|a(m+k,n)b(m,n+k)|`.

Its l^(3/2) norm is bounded by C||a||_l3||b||_l3 through triangle inequality, Hölder, translation invariance, and summability of k^(-2). Average over the fixed fractional-coordinate square and apply Minkowski to the continuous variation bound. All factors are absolute because epsilon is fixed. Thus #082 gives discrete triangular Hilbert r-variation with a short explicit proof, after which standard finite-box Z^2 Calderón transference gives the arbitrary commuting-transformation statement. This is high-tractability and does not require an unknown discrete harmonic-analysis theorem. It still does NOT give ordinary Cesàro convergence.
