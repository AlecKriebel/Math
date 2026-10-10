# Independent audit: projective closed-immersion height counts

Problem 30002439, OWR-12725-016. Audit date: 2026-10-06.

## Decision

ACCEPT AS PARTIAL, NOT SOLVED. The audited author archive is 11,301 bytes with SHA-256 `94ec6adf37a9b6cdd4532ef448ae72ed46ac739b50c81c69686ffa34370e7304`. No mathematical or executable correction is required. The original archive, external manifest, external bootstrap, validation receipt, and authored files were not modified. This audit is a separate artifact; historical statements in the original packet that an audit was pending remain historical.

The accepted deductions are coefficient-uniform ambient-dimension reduction, the stated elementary and curve subcases, the surface exponent 7/(2d)+epsilon, and the quadratic-surface exponent 43/28+epsilon. The general exponent (n+1)/d+epsilon remains unproved here. No novelty, best-known bound, general counterexample, or comprehensive literature-status certification is accepted or claimed.

## Original problem and conventions

The independently retrieved original [OWR report](https://ems.press/content/serial-article-files/46482?nt=1), Problem 11, printed pp. 3031-3032, distinguishes a map-dependent height-count bound from a conjectural constant indexed only by d, n, and epsilon. It uses rational points and primitive-integral maximum-coordinate height and explicitly requires a closed immersion for the uniform conjecture. It records d=1 and n=1 as known. The author's reading over Q, with homogeneous forms and no common geometric projective zero, makes the projective-morphism conventions explicit. The original's abbreviated word “polynomials” does not justify arbitrary nonhomogeneous polynomials or merely the absence of rational basepoints.

The source date is the 2013 workshop/report, notwithstanding the catalog citation's 2014 label. The full corpus inputs match their recorded byte counts and hashes. The unique problem record and the corresponding absent research-result entry reproduce the specified review digest using Python's default JSON serialization with sorted keys. No dataset record or copied source text is included in this audit.

The degree d is the degree of the forms, equivalently the pullback of O(1) is O(d). For a closed immersion its image has degree d^n. Confusing these two degrees would invalidate both exponent substitutions. Counts are over source Q-points, but a Q-defined closed immersion is a Q-isomorphism onto its scheme-theoretic image and therefore gives the required bijection with image Q-points.

## Ambient dimension and height: accepted

Let V be the Q-span of the coordinate forms and choose a basis from those forms themselves. If the chosen forms vanished at a geometric point, every original coordinate would vanish there; thus the reduced map is everywhere defined. The coefficient matrix expressing all original forms in this basis has identity rows, hence rank r=dim V. It induces a closed linear embedding i and f=i composed with g.

To make the closed-immersion conclusion scheme-theoretic, pull back the closed immersion f along i. Since i is a monomorphism and f already factors through i, that base change identifies with g. Thus g is a closed immersion. Equivalently, identify the linear subspace i(P^(r-1)) with P^(r-1) and regard the same closed subscheme inside it. This uses no bound on the entries of the coefficient matrix.

For a primitive integral output vector y of f(x), the selected coordinate subvector y_I represents g(x). It is nonzero. It need not be primitive: (6,10,15) has primitive full vector but subvector (6,10) has gcd 2. Dividing by the positive gcd can only lower the maximum absolute coordinate. Consequently H(g(x))<=H(f(x)), and n_f(B)<=n_g(B). No rational change-of-basis height estimate is being smuggled in. Arbitrary linear combinations would not work: [1:1] can become [101:1].

The section-space dimension is binomial(n+d,d), so the possible reduced ambient dimensions form a finite set bounded only by n,d. A maximum of finitely many constants depending on degree, reduced ambient dimension, and epsilon depends only on n,d,epsilon. Nondegeneracy of the reduced image also follows from linear independence, if a source theorem were to require it.

## Special cases and sharpness: accepted

For d=1, the basepoint-free linear system has rank n+1, since a rank-deficient coefficient matrix has a nonzero kernel. The reduced map is a Q-projective automorphism, permutes source rational points, and gives the claimed elementary count O_n(B^(n+1)).

For the full monomial Veronese, any prime dividing all coordinates would divide every pure power and hence every source coordinate. The monomial vector is therefore primitive. Its maximum is the d-th power of the source maximum because pure powers occur. This proves the exact height and threshold identities. The proposed coprime-pair lower bound is valid: the union bound over divisors gives at most (3/4)T^2 noncoprime positive pairs, and the extra coordinates and sign convention produce distinct projective points. The estimate floor(t)>=t/2 for t>=1 extends the lower bound to all real B>=1.

Precomposing with any Q-projective automorphism reindexes all source rational points and leaves the output counting function unchanged. The shear family correctly disproves a coefficient-uniform positive pointwise lower comparison with the original source height. It cannot be a counting counterexample, and the author explicitly does not present it as one.

[Walsh's Theorem 1.1](https://arxiv.org/abs/1308.0574v2) applies uniformly to all irreducible degree-delta projective curves over Q, with constants depending only on delta and ambient dimension, and exponent 2/delta. The primary PDF and first-page pixels were inspected. The reduced image of P^1 has degree d and dimension at most d, so the claimed O_d(B^(2/d)) follows. The [publisher record](https://academic.oup.com/imrn/article-abstract/2015/14/5644/781658) confirms IMRN 2015, pp. 5644-5658; online publication was in 2014.

## Surface inputs and exceptions: accepted

The independently inspected primary [Salberger article](https://doi.org/10.1112/plms.12508) uses the same height. Theorem 0.9(b), p. 1095, supplies O_(D,N)(B^(3/(2 sqrt(D))) log B+1) geometric integral curves of bounded degree, and a complementary count O_(D,N,eta)(B^(3/sqrt(D)+eta)). The bound is uniform in the surface's coefficients. Part (b) has no smooth-hypersurface restriction and no deletion of hyperplane sections. Part (a)'s stronger special hypotheses are not used.

Theorem 0.8 counts away from lines. Its degree-four case with a two-dimensional conic family has the uniform exponent 43/28+epsilon. The separate exponent 3/2 in that case has a surface-dependent constant; it cannot be substituted for the uniform claim. Theorem 0.3 gives the uniform dimension-growth exponent for degree at least four.

For the application, X=g(P^2) is smooth and geometrically integral, D=d^2, and N<=binomial(d+2,2)-1. A geometric integral curve C pulls back to an integral plane curve E of positive degree e. Degree of the restricted line bundle gives deg(C)=deg(O(d)|E)=de. This argument holds for every geometric integral curve, not just rational or smooth curves. In particular every curve degree is at least d, and X has no geometric lines when d>=2.

For a covering curve defined over Q, apply Walsh directly to the curve in its given projective embedding. A rational parametrization of the curve is unnecessary. Its degree delta lies between d and a bound K(d); maximizing Walsh's constants over that finite degree range and the finite ambient-dimension range is legitimate. The inequality B^(2/delta)<=B^(2/d) holds for B>=1.

If a geometric covering curve is not defined over Q, it has a distinct Galois conjugate. Rational points on the first curve lie on the conjugate too, because their coordinates are Galois-fixed. The Q-defined isomorphism g identifies their inverse images with distinct integral plane curves of the same degree e. Plane Bezout bounds their finite intersection by e^2. Since e=delta/d<=K(d), this is a coefficient-independent O_d(1). Thus the author's descent/intersection treatment closes, rather than overlooks, the non-Q curve case.

The resulting sum is bounded by a uniform multiple of B^(3/d+eta)+(B^(3/(2d))log B+1)B^(2/d). Taking eta=epsilon/2 and using log B=O_epsilon(B^(epsilon/2)) proves the stated 7/(2d)+epsilon exponent for B>=2. Monotonicity treats 1<=B<2 uniformly. There is no estimate hidden in the number or coefficients of the curves beyond the source theorem's explicitly uniform bounds.

For d=2, images of lines form an algebraic two-dimensional family: the usual universal family of lines on P^2 transports under the isomorphism g to a flat family of embedded curves, with distinct lines giving distinct members. Their degree is two. Hence X satisfies the exceptional branch of Theorem 0.8, while its line complement is all of X. This proves the advertised 43/28+epsilon bound. The fixed gaps are respectively 1/(2d) and 1/28, so neither bound supplies the conjecture for all epsilon>0.

## Other source scope and stopping condition

The general-dimensional image has degree d^n>=4 for n,d>=2. Its dimension-growth exponent n exceeds (n+1)/d, since dn>n+1 in this range. Therefore that application is sound but insufficient. The precise [Cluckers-Debes-Hendel-Nguyen-Vermeulen Theorem 4.21](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/improvements-on-dimension-growth-results-and-effective-hilberts-irreducibility-theorem/A7BCAEBF00B8B165D6DDB3FFB9B40B97) was checked on the publisher page: its statement concerns integral hypersurfaces over global fields. It is not the requested embedding theorem. [Liu's 2026 preprint](https://arxiv.org/abs/2601.10895), Theorems 1.1-1.2, concerns projective/affine cubic surfaces and conics, not the degree-four images used here. These checks support only the author's limited scope claims.

The four documented approaches are correctly distinguished from a general solution. This audit verifies those approaches and does not introduce a fifth attempt or turn a negative literature search into a theorem of present-day openness.

## Executable and packaging acceptance

The original bootstrap, checker, builder, and validation harness were fully read before running any original candidate code. Only the bootstrap and its verified in-memory checker payload were executed; original builder/validation scripts were not used to generate the independent results.

Fresh author-packet validation passed 65 controls. Coverage includes normal and optimized isolated interpreters, relocation of the extracted root and all external trust-root files, hostile current-directory and environment imports, caches and extra directories, every member digest, missing members, a malicious checker sentinel, symlink members/roots/ancestors/archives/manifests, directory/FIFO substitutions, external-root constraints, corrupt ZIP/manifest, unsafe startup flags, and direct or runpy entrypoints. The original code checks explicit conditions rather than relying on assertions, so -O does not disable validation. It executes the bytes already checked, not a reopened checker pathname. No malicious marker or root cache appeared.

The external bootstrap is the trust root. Its hash and manifest pin must be obtained from a trusted source; a token embedded in the checker is an accidental-entrypoint guard, not a sandbox against an attacker who can replace the trusted bootstrap or arbitrary interpreter code. These controls are not claims of safety against a compromised Python installation, operating system, or concurrent hostile filesystem modification.

The independent diagnostic implementation uses multiset monomial enumeration and Mobius-inversion coprime counting, rather than copying the author's corresponding algorithms. It also checks larger shears, fractional thresholds, subvector primitivity, degree and exact exponent arithmetic. It passed in normal and optimized isolated mode. Finite arithmetic checks do not prove the general statements, the cited literature theorems, novelty, or completeness of research.

The publication-safe audit package contains authored analysis/code and public verification metadata, plus the unchanged author safe archive. It contains no third-party PDFs, extracted pages, screenshots, raw corpus data, credentials, or private coordination. No publication, commit, push, or PR action was performed in this audit.
