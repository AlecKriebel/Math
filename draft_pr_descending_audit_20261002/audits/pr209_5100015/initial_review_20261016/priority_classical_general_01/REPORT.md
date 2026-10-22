# Classical/general priority audit of PR209 / 5100015 / k303,b

Frozen candidate head:fd09a95b479f376234835a4494693bb1316c85ec. Original PROOF SHA256:4f2eac23212f3fdf1c0c17ba79081e6dc9790907d1725c7359e9461052eabfc2. Assigned audit only; no result promotion, whole-preprint clearance or absolute-priority certification.

## Strongest verified findings

1. The candidate's odd cyclic dn trace lemma is an immediate corollary of a precise earlier all-phase identity, already displayed in Khare–Lakshminarayan–Sukhatme's primary2002 preprint. It must not be described as a new special-function result. The original candidate already calls its elliptic-function inputs classical; the audit supplies a much more exact citation and constant.
2. The center tangent-foot/edge-vector mechanism also has a precise earlier explanation. Akopyan–Schwartz–Tabachnikov's Theorem4 proof gives the velocity-difference relation and Joachimsthal factor; its next section states the classical skew-hodograph transformation. Bialy–Tabachnikov independently treats the actual center feet and the same telescope. Our canonical same-caustic phase normalization and signed-area assembly are written explicitly in CLASSICAL_BRIDGE.md. These are a checkable synthesis, not evidence that either old paper states the full target.
3. Chavez-Caliz's old even original/outer area-product theorem gives a second all-phase route to the odd trace lemma through an auxiliary2q-periodic family. Its theorem concerns different polygons. Identifying its theorem directly with k303,b would be an error.
4. A recent public page explicitly claiming exact full k303,b coverage surfaced in the first independent broad search and was immediately reported to root. Contemporary PDF/version/publication chronology is a separate assigned family. Root later reported having read its exact covering theorem. This report does not adjudicate absolute historical priority or earlier website visibility.
5. No directly read pre2026 source in this bounded audit explicitly states and proves the entire target with its exact construction/parity/signed traversal conventions. This is a search result with stated limits, not a firstness or novelty conclusion. The ability to assemble a proof from old ingredients is distinct from locating an old full target proof.

Assigned-audit disposition: **classical inputs and explicit bridges established; no older explicit exact-target theorem authenticated in this family; historical full-target priority remains for root's combined evidence assessment.**

## Frozen exact target and independence

The target is a fixed strict noncircular outer ellipse a>b>0 and a fixed strictly interior nondegenerate confocal ELLIPTICAL caustic. P_i are actual billiard vertices in traversal order; R_i are intersections of the outer tangents at consecutive P_i. Q_i are perpendicular feet from the center O onto the tangent side lines of this OUTER polygon. The claim is constancy of area(R)*area(Q), both signed shoelace areas, for every phase when listed N is odd or2 mod4. Primitive stars, reverse traversal and repetitions are included. Circle has a separate rotational proof; hyperbolic, focal and degenerate caustics are excluded.

The scope/questions were frozen in the initial tool transcript before any campaign priority report was read. ENOSPC initially prevented mkdir/write; they were persisted as soon as possible in FROZEN_SCOPE.md. No campaign priority report was subsequently read. Parent INTAKE, original PROOF/SOURCES/pinned problem/report and root mathematical acceptance were read; the acceptance JSON was separately inspected during the audit. Parent's later contemporary-source message is disclosed as parent-supplied evidence, not independent source reading by this family.

The log preserves mistaken manually typed05:02/05:16/05:24 labels together with an explicit actual-clock correction. Those steps occurred during04:54–04:57:01UTC. They were clerical timestamp errors, not actual future events. Neither the original entries nor the independence-freeze record were silently replaced.

## Exact earlier formulas and checkable bridges

Use parameter m=k² and K=K(m); this differs from Stachel's printed modulus, which is k itself. Put k_c=sqrt(1-m), and for odd q define

    U_q(z)=sum_(j=0)^(q-1)dn(z+2Kj/q|m),
    C_q=product_(n=1)^((q-1)/2)cs²(2Kn/q|m).

KLS arXiv:math-ph/0207019v1,15 July2002, Appendix A p20 Eq.(86), explicitly gives product_j dn(z+2Kj/q)=C_q U_q(z). The same formula is v2 Eq.(85),p19. The arbitrary base point and master-identity derivation make this an identity for all phases and all odd q, not a numerically tested finite range. The primary v1 equation was visually checked. Its introduction distinguishes earlier finite numerical checks from II's rigorous general identities. [Primary v1](https://arxiv.org/pdf/math-ph/0207019v1), [primary v2](https://arxiv.org/pdf/math-ph/0207019v2), [journal DOI10.1063/1.1560856](https://doi.org/10.1063/1.1560856).

The standard quarter-period formula dn(t+K)=k_c/dn(t) immediately yields

    U_q(z)U_q(z+K)=k_c^q/C_q².

C_q is positive and finite for0<m<1; q=1 uses an empty product. CLASSICAL_BRIDGE.md independently verifies the coefficient by a complete residue argument. This reproof is attribution checking, not a novel identity.

KS's generalized Landen transformation gives the independent representation U_q(z)=eta^(-1)dn(z/eta|m_t), eta=1/U_q(0), with

    m_t=(m-2)eta²+2eta³ sum_j dn³(2Kj/q|m),
    K(m_t)=K(m)/(q eta).

In arXiv:math-ph/0312074v1 the precise references are Eqs.(13)–(15),p4; Eq.(61),p12; Eq.(74),p13. In the retained published Pramana63(2004) extraction they are Eqs.(7)–(9),p923; Eq.(54),p930; Eq.(61),p931. For odd q, shifting z by K shifts the reduced argument by qK(m_t), an odd reduced quarter-period, giving eta^(-2)sqrt(1-m_t). Omitting eta would be a normalization error. [Primary author preprint](https://arxiv.org/pdf/math-ph/0312074v1), [publisher metadata/DOI10.1007/BF02704331](https://link.springer.com/article/10.1007/BF02704331).

The fresh published KS PDF was not authenticated: tested IAS routes returned403; the Springer PDF request returned subscription-preview HTML, retained privately with its true type; a search-indexed mirror URL returned404. The retained published extraction was read in place, with hash recorded. The directly fetched primary2002/2003 PDFs independently establish every identity actually needed, so the target bridge does not depend on inaccessible published bytes. The publisher metadata also has an incorrect-looking shorthand bibliography year/page for KLS II; this audit uses the primary arXiv version dates and its explicit journal reference44(2003),1822–1841 instead.

For geometry, write e_i for the outgoing unit velocity, n_i for outward unit normal, h_i=P_i dot n_i and J=sin(delta_i)/h_i. Reflection gives

    e_(i-1)-e_i=2 sin(delta_i)n_i,
    Q_i=h_i n_i=[e_(i-1)-e_i]/(2J).

AST's Theorem4 proof,p4, displays the equivalent relation using the polar vector P_i*, and Lemma3.1/Remark3.2,p5, states the skew-hodograph transformation S e_i, S=diag(a,b), back to a billiard in the original boundary ellipse. AST credits Veselov1988/1991; those originals were not independently read here. [AST primary](https://arxiv.org/pdf/2001.02934v2). BT's published Theorem4.1 proof,pp1348–1349, treats Q_i as the actual center feet on the outer tangents and uses the corresponding telescope; its theorem proves centroid/squared-distance invariance, not this area product. [BT published PDF](https://par.nsf.gov/servlets/purl/10408490), [DOI10.1007/s40879-020-00428-7](https://doi.org/10.1007/s40879-020-00428-7).

Stachel's Theorem4.3/(4.9),p1614, gives P(z)=(-a sn z,b cn z), step2v with v=2tau K/N, coprime tau,N. Direct quarter-period normalization then gives

    S e_i=P(u+(2i+1)v+K),
    J b=cn(K-v).

Thus the old velocity mechanism becomes precisely the submitted pointwise fixed-linear-map reduction of Q to edges of a shifted SAME-CAUSTIC billiard. The last same-caustic/phase identification is explicitly derived here; it must not be silently attributed as an already printed target theorem. [Stachel DOI10.1007/s40879-021-00524-2](https://doi.org/10.1007/s40879-021-00524-2).

With f(t)=sn(t)cn(t)/dn(t), elementary determinant expansion/Jacobi addition and conic polarity now give

    area(Q)=[2f(v)-f(2v)]T(u+v+K)/(4J²),
    area(R)=a²b² f(v)T(u+v)/(alpha beta),
    T(z)=sum_(i=0)^(N-1)dn(z+2iv).

For a primitive winding, q=N/gcd(N,2), r=N/q, T=rU_q. N odd or2 mod4 is exactly q odd. Multiplying the two equations and using the OLD trace identity proves the candidate result. No convexity, spatial vertex sorting, division by a polygon area or numerical sampling enters this all-phase deduction. All signed-area factors, star/repeat arithmetic, units and constant are checkable in CLASSICAL_BRIDGE.md.

Chavez-Caliz Theorem6,pp104–105 (also stated as Theorem3,p93), proves even original/tangent area PRODUCT for concentric ellipses in general position. Take an auxiliary strict confocal boundary with v_aux=K/q and primitive N_aux=2q,tau=1. Its two areas are nonzero fixed coefficients times U_q(z),U_q(z+K/q). For odd q, K-K/q is in the2K/q subgroup, so this gives U_q(z)U_q(z+K) constancy. q>=3 is valid; q=1 is elementary. Four distinct complex intersections verify general position. This is a second complete bridge for the lemma, not a claim that the original/pedal polygons are the same objects. [Published primary](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf), [DOI10.1007/s40598-020-00154-8](https://doi.org/10.1007/s40598-020-00154-8).

## Coverage and exact gaps

Here “input” means an all-phase old ingredient that covers the indicated arithmetic after the EXPLICIT bridge, not an old statement of the target. “Different” means the printed theorem concerns other objects/quantities.

| Source/mechanism | Odd N |2 mod4 N| Primitive stars | Repeats | Domain / exact gap |
|---|---|---|---|---|---|
| KLS2002 odd product-to-sum | Input:q=N | Input:q=N/2 | Coprime shifts permute subgroup | Multiplicity r and area-square scaling |0<m<1, arbitrary complex phase; no geometry theorem |
| KS2003/2004 Landen | Input | Input | Same subgroup arithmetic | Same | Argument scale eta essential; no target polygon identification |
| AST2020 velocity reflection + skew hodograph | Mechanism applies | Mechanism applies | Physical unit velocities retain traversal order | Pointwise mechanism repeats | Boundary ellipse; same-caustic phase and final area assembly supplied here |
| AST Theorem3 odd original/outer ratio | Different area ratio | Not this theorem | Indexed grid mechanism; no new target conclusion | No unrestricted padding certificate used | Concentric pair; not area(R)*area(Q) |
| BT2020 Theorem4.1 | Different invariants | Different invariants | Reflection/telescope uses actual directed edges | Pointwise telescope repeats | Actual outer tangent feet; centroid/squared distances do not determine pedal area |
| Chavez-Caliz2020 Theorem6 | Via auxiliary2q bridge for trace | Printed even original/outer theorem gives trace | Signed oriented algebra; auxiliary winding1 suffices | No unsupported central-symmetry claim on padded odd walk | General-position concentric ellipses; different polygon pair |
| Stachel2021/2022 | Parametrization input | Parametrization input | Explicit gcd(N,tau)=1 | Extension separately justified | Nondegenerate elliptical caustic; no exact target area theorem located |
| RGS pedal-like curves / Steiner | Different quantifier | Different quantifier | No discrete winding theorem | Not applicable | Whole curve or fixed polygon, moving pedal point; no phase-varying finite billiard proof |
| Roitman–Garcia–Reznik2021 | Different theorem | Different theorem | No target inference | No target inference | Bicentric limiting-point pedal PERIMETERS/focal polar images |
| Schwartz2014/2015 monodromy | Different invariant class | Different invariant class | No automatic star extension claimed here | Not used | Target's Euclidean pedal product not identified with monodromy invariant |
| Original2021 Table4 | Target conjecture | Target conjecture | Signed Eq1 verified | Literal listed-period issue settled by math audit | Strict confocal ellipse pair; printed “?” is a source-date status only |
| Contemporary Ferudun v1.1 | Exact claim on live page | Exact claim on live page | Explicit claim | Explicit claim | Root reports exact Theorem2 coverage; priority/public visibility assessed separately |

RGS source is [Area-Invariant Pedal-Like Curves Derived from the Ellipse](https://arxiv.org/pdf/2009.02581v3), especially pp3–6 and Theorem1. Bicentric source is [published Theorem2,pp625–627 and polar/pedal AppendixA](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf), DOI10.1007/s40598-021-00188-6. Schwartz's [primary author preprint](https://www.math.brown.edu/~res/Papers/poncelet_monodromy.pdf), Theorem1.2,p4 and proof outline,p5, establishes the general old meromorphic/compact-torus method for its invariant class. That method itself is also used by KLS/AST/Chavez-Caliz and the bicentric paper, and should not be presented as new here.

The published original Table4/Section3.4,p346, and signed-area Eq1,p343, were visually/read-text checked against the same bytes accepted by root. [Original published source](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf). The contemporary live page is [Outer-Pedal Area Products in Elliptic Billiards](https://eulersolve.org/papers/amr-050-0014/). No contact or outreach occurred.

## Reproducible artifacts, limitations and recommendation

bridge_verify.py ran using only the assigned existing scientific interpreter with -B, mpmath1.3.0 at90 digits. It checked18 trace families/108 real-complex phase cases and24 physical families/120 phase cases, including coprime stars, reversal and triple traversal scaling. The maximum normalized residual was below7.4e-89 against tolerance1e-65. Direct tangent intersections and actual perpendicular feet were used. Primitive excluded N4/N8 products had nonzero phase spreads about0.6848814553 and0.0005661183 at m=.6. These finite controls corroborate normalizations; the written all-phase derivations are the proof evidence.

SOURCE_RECEIPTS.json records URLs, DOIs, access dates, bytes, SHA256 and precise read scope for each fetched/retained source, and explicitly separates failed HTML/PDF access. Private third-party PDFs/extractions/renders are excluded from AUTHORED_MANIFEST.json. The manifest is self-excluding and covers every public authored payload. All work stays in this assigned folder; no queue/database/target/Git/index/ref/environment/install/cache/tracker/deposit actions were used. No scientific evidence was deleted or compacted. Initial ENOSPC and the source-access/timestamp errors remain disclosed.

The remaining historical question is whether an independently authenticated older exact target statement/proof exists, or whether the target is a new explicit synthesis/corollary of these old tools. This audit does not resolve that question by search absence. It does establish precise attribution that downstream writing should retain: KLS's odd trace identity; generalized Landen normalization; AST's reflected-velocity and skew-hodograph mechanism; BT's actual-foot telescope; conic polarity/Jacobi addition; and the existing meromorphic invariant method. The exact contemporary covering source must also be addressed by root's priority/chronology assessment. No first-proof, novelty, entire-list or release clearance is issued.
