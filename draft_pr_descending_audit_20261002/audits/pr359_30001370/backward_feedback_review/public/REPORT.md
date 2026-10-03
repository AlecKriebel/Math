# Independent backward-feedback audit of PR359 / problem30001370

## Scoped mathematical verdict

**PASS for the exact original common-boundary theorem.** I found no mandatory mathematical correction in the frozen candidate. For the specified two-branch Möbius maps on I=[-1/2,1/2], feedback G(m)=A tanh(Bm/A), 0<A<=2/5 and 6<B<=16, and D consisting of all probability densities with its relative L1 topology, the candidate proves

    W = boundary_D(B+) = boundary_D(B-),
    W = closure_D(union_{n>=0} F^{-n}({1})).

The second identity is the strongest precise intermediate statement independently checked here. No boundedness, positive lower bound, BV regularity, prescribed attraction rate, or independence of branch labels is required. The result uses credited global convergence, basin openness, and the boundary seed at1 from Bardet–Keller–Zweimüller. It does not establish historical priority, a smooth stable manifold on L1, or an analogous theorem for arbitrary feedback maps. All three candidate source-file hashes were verified after preserving an initial DNS failure and a successful native retry.

This is an independent AI-assisted adversarial audit, not journal certification. All files were inspected only after the timestamped source-first reconstruction had been sealed. No sibling review was read. The prior review packaged inside the candidate was read as part of the submitted material and was not accepted as an independent premise.

## Source-first independence and exact source binding

SOURCE_FIRST.md was sealed at 2026-10-03T22:02:35.020674Z, SHA256 b8f83b55b76c5a8ee65d37fd8dbcc94e2a48355d6ab249abba30ba3b8efebe14, before opening the candidate, its programs, verdicts, QUEUE record, or snapshot. The original Keller contribution is printed2713-2715 in OWR49/2009; the conjecture was visually inspected on printed2715. The precise topology is relative L1 on all D, rather than weak convergence or an ambient-L1 boundary. The independently identified gap was uniform backward lifting of a central orbit; the sealed note already distinguished that gap from one-step scalar inversion and from the known boundary theorem on the compact integral-representation class.

Primary sources:

- [Official OWR2009/49](https://ems.press/content/serial-article-files/46250), 320856 bytes, SHA256 b4a8d328316d093cde2d23a9b13e8b869e33b46626735494de473045bbc26169.
- [Full author-hosted BKZ paper](https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf), 36 native pages, rendered19December2008, 541479 bytes, SHA256 c1b9ca5c4edbba4d06513634a649589185a63a53f0b0a9f14ebb8a9fc8289642.
- [Exact arXiv0812.4040v1](https://arxiv.org/pdf/0812.4040v1), 36 native pages, 462269 bytes, SHA256 6a182868c1d2d4a09c8cfaa513ba9314cce522c3b08fe71728264399df7d7861. Submission history identifies v1 as21December2008 17:31:12UTC. The downloaded rendering says10November2018 and its native PDF metadata says2022; these dates are not the submission date. Its bytes differ from the author-hosted paper. Neither file is represented as the inspected final journal PDF.

The source dependencies were read in their complete relevant proofs: Theorem2/Example1; finite-system inverse expansion in Section3/Lemma4; integral-representation identities in Section4.1; IFS continuity, monotonicity and convergence in Section4.2-4.4; all-density shadowing/convergence/openness in Section5.1; restricted boundary statement in Section5.2/Proposition4 and its Lemmas12-13; derivative-space qualifications in Section5.3/Lemma14/Proposition5. The full author paper was acquired. Raw sources, extracted text, source-render images, native extraction streams and the full version differences are private.

## Independent stronger exact inverse certificate

The highest-risk submitted step is the dimension-independent inverse contraction on an arbitrary probability space. I reconstructed it through a sharp two-dimensional Hilbert-space calculation, instead of the candidate's cross-term maximization or either of the submitted covering tables.

Let b_r=f_r^{-1} on J=[-1/2,3/2]. For a J-valued bounded random variable Z, solve

    r=G(E b_r(Z)),        V(Z)=b_r(Z).

The residual r-G(E b_r(Z)) strictly increases by at least the parameter increment because b_r decreases in r and G increases. It changes sign at±A, so the root exists uniquely. This argument is genuinely self-consistent: it solves the feedback of the new law, rather than inserting the old orbit's feedback.

Along the bounded path Z_t=(1-t)Z+tZ', write X_t=V(Z_t), q=1-4X_t^2, beta=G'(E X_t)/(4-r_t^2), D=f'_{r_t}(X_t). Scalar implicit differentiation gives

    dot X = A D^{-1} dot Z,
    A = Id - beta q E/(1+beta E q).

All differentiations are under bounded smooth scalar derivatives on the relevant compact rectangle. They do not assert an L1 or L2 Fréchet stable-manifold theorem.

Put m=E q, s=E q^2, C=1+beta/4. Since0<=q<=1, m^2<=s<=m. If s>m^2, use the orthonormal basis consisting of the constant function1 and (q-m)/sqrt(s-m^2). The matrix of A on their span is

    [ 1/(1+beta m)                         0 ]
    [ -beta sqrt(s-m^2)/(1+beta m)          1 ].

A is the identity on the orthogonal complement. Its Gram matrix satisfies

    (C Id-A* A)_{22}=C-1=beta/4,
    det(C Id-A* A)
      = beta^2 [(C m-1/4)^2+C(m-s)]/(1+beta m)^2 >=0.

For beta>0 the positive lower diagonal and nonnegative determinant imply positive semidefiniteness. beta=0 is immediate. If q is constant, the same conclusion follows directly or by a limit. Therefore, on every real probability-space L2,

    ||A||^2 <= 1+beta/4.                                  (I)

This bound is sharp for the rank-one operator itself: take q Bernoulli with m=s=1/(beta+4). It is a universal analytic identity, not an empirical grid. The standard-library checker independently expands and verifies its polynomial determinant identity exactly.

The tanh feedback identity along the path gives, for a=|r_t|,

    0<=G'(E X_t)<=16-100a^2,
    beta<=(16-100a^2)/(4-a^2),
    ||D^{-1}||<=(2+a)/(2(2-a)),        0<=a<=2/5.

Combining these bounds with(I) gives

    ||dot X||_2^2 <= W(a)||dot Z||_2^2,
    W(a)=(2+a)(4-13a^2)/(2(2-a)^3) < 7/10.

The full continuous interval is certified by the single exact identity

    7(2-a)^3-5(2+a)(4-13a^2)
      =172(a-13/43)^2+12/43+58a^3 >0.

Integrating the path derivative yields

    ||V(Z)-V(Z')||_2 <= (21/25)||Z-Z'||_2,

because7/10<(21/25)^2. This is stronger than the candidate's24/25. It supplies an independent certificate for the central mechanism even if the submitted CSV and prior400-row envelope are discarded. The candidate's weaker bound and its40-row certificate also replay correctly; no correction is required.

For scope sensitivity, at r=0 and B=100 the same sharp rank-one calculation would allow inverse derivative norm squared29/16>1 on an endpoint/midpoint distribution. Interior approximations retain the expansion. This does not refute the requested parameter range. It shows why simply generalizing the contraction assertion to arbitrary feedback strengths would be invalid.

## Uniform self-consistent backward construction

Fix u in W and work on the original probability space(I,u dx). Let X_j be its actual nonlinear orbit, r_j=G(E X_j), and A_j in{0,1} its original branch label. Then

    f_{r_j}(X_j)=X_{j+1}+A_j.

For epsilon=||F^n u-1||_1, the terminal cumulative transform J_n sends the absolutely continuous law of X_n to uniform measure on I, including when its density vanishes. It is AC, nondecreasing, endpoint-fixing, and ||J_n-id||_infinity<=epsilon. Set Y_n=J_n(X_n), then recursively

    Y_j=V(Y_{j+1}+A_j),       rho_j=G(E Y_j).

The sublaw of Y_{j+1} on each event{A_j=a} is dominated by its unconditional law, so it is absolutely continuous whenever that law is. The appropriate smooth inverse branch preserves absolute continuity. This downward induction starts with the uniform terminal law. It proves that every Y_j has a density, that rho_j is exactly its feedback, and that the density v_n of Y_0 satisfies F^n v_n=1.

The comparison uses the same label on the same original probability space. Thus

    (Y_{j+1}+A_j)-(X_{j+1}+A_j)=Y_{j+1}-X_{j+1}

exactly, without label independence. Original X_j also solves the implicit inverse equation by uniqueness. With the independently certified kappa21/25,

    ||Y_j-X_j||_2<=kappa^{n-j}epsilon,
    Delta_j=|rho_j-r_j|<=16kappa^{n-j}epsilon,
    sum Delta_j<=84epsilon.                              (II)

This removes the genuine source-first gap: all accumulated backward parameter changes are bounded independently of n. No attraction-rate estimate is inserted.

## Transport, flat intervals, and all-L1 closure

The backward variables admit deterministic global transports H_j. On the old branch a,

    H_j(x)=b_{rho_j}(H_{j+1}(T_{r_j}(x))+a),       H_n=J_n.

At every cut both limits are the new cut-rho_j/4. Hence each finite-stage transport is continuous, nondecreasing, onto and endpoint-fixing. AC is justified branchwise: the inner old branch is a smooth bi-Lipschitz map, and the outer inverse branch is smooth Lipschitz. A generic claim that arbitrary AC compositions are AC would be insufficient; the specific maps here have the needed properties. Finitely many cuts glue the branchwise maps. Flat intervals remain allowed.

The exact inverse bounds |partial_z b|<=3/4 and |partial_r b|<=25/96 give, with d_j=||H_j-id||_infinity,

    d_j <= (3/4)d_{j+1}+(25/96)Delta_j.

Using(II) gives the independently strengthened bounds

    d_0<=(183/8)epsilon,
    sum_{j<n}d_j<=(181/2)epsilon.

All old finite-cylinder maps preserve Lebesgue null sets in both directions. Their chain rule therefore remains legitimate when the terminal density u_n is merely integrable:

    H_0'(x)=u_n(X_n(x))R_n(x),
    R_n=product_{j<n} f'_{r_j}(X_j)/f'_{rho_j}(H_j(X_j)).

Using |partial_x log f'|<=1 and |partial_r log f'|<=35/24 yields

    |log R_n|<=213epsilon.                               (III)

The candidate's constants384,403,101 and964 are looser but valid.

The unweighted Lebesgue estimate is indispensable. For the original external parameter sequence, let a_n=P_{r_{n-1}}...P_{r_0}1. The primary source's full-branch integral-representation identity keeps a_n in the normalized mixture class with |y|<=2/3, so1/2<=a_n<=2. Transfer duality, first for bounded truncations if necessary, gives

    integral |u_n(X_n(x))-1|dx
      =integral |u_n(y)-1|a_n(y)dy<=2epsilon.

This never integrates a square of u_n under its own law. Combined with(III), it gives

    ||H_0'-1||_1<=2epsilon exp(213epsilon)+exp(213epsilon)-1.

For every AC monotone onto H, H_*(H'dx)=dx follows by applying the fundamental theorem of calculus to antiderivatives of continuous tests. It remains true when H has flats. Consequently, for continuous g,

    ||H_*(gdx)-gdx||_TV
      <=omega_g(||H-id||_infinity)+||g||_infinity||H'-1||_1.

The norm is full total variation, equal to L1 for densities. Possible atoms in the auxiliary measure H_*(gdx) do not break the signed-measure inequality; the actual H_*(u dx) already has an absolutely continuous law by the preceding induction. Approximating fixed u in L1 by continuous g now yields

    ||v_n-u||_1 <=2||u-g||_1+omega_g((183/8)epsilon)
      +||g||_infinity[2epsilon exp(213epsilon)+exp(213epsilon)-1] ->0.

Only epsilon=||F^n u-1||_1->0 is used. This proves the all-density closure statement.

As an adversarial check on the argument's necessity, mere uniform displacement would not suffice: H_N(t)=t+alpha sin(2pi Nt)/(2pi N),0<alpha<1, converges uniformly to id on[0,1], while ||(H_N)_*dt-dt||_TV=2alpha/pi remains constant. The candidate avoids precisely this failure by controlling derivatives and total variation.

## Open-map and boundary completion; separate linear turn

Turn1's factorization is valid: T_r=T_0 composed with h_r, where h_r(x)=(x+r/4)/(1+rx) is an increasing endpoint-fixing diffeomorphism. Its density pushforward is an L1 isometry. Joint strong continuity follows by continuous approximation and isometry. The feedback transport K(u)=Q_{G(phi(u))}u has a continuous inverse because its scalar inverse residual is increasing and its root is Lipschitz with coefficientB/2.

The positive section of doubling is valid also on a zero-output fiber: both old branch densities are then zero, and the equal allocation q=1 makes P_0q=1. The section is an L1 isometry and passes through the prescribed density. Thus F is a continuous open surjection. Openness plus F^{-1}(B±)=B± proves complete invariance of each relative basin boundary. The source boundary seed at1 places every F^{-n}({1}) in both boundaries. Their closedness and the transport approximation put every u in W in both. Conversely, disjointness/openness of B± and global trichotomy put their boundaries in W.

Turn2 is not used in this nonlinear proof. Its separate linear statement checks correctly. For f=x^3-3x/20, integral f=phi(f)=0 but phi(P_0f)=1/320; this independently confirms that the inspected preprint's one-step kernel estimate cannot simply be iterated as an invariant-kernel proof. The corrected resolvent functional has the required eigenfunctional relation and gives strong L1 stability on its actual kernel. Symmetric high-frequency modes exclude uniform operator-norm contraction there. None of this is promoted to nonlinear L1 differentiability.

## Mechanism map and exact remaining gaps

| Approach family | Mechanism/evidence | Status | Exact gap or limit |
|---|---|---|---|
| Ordered integral representations | Complete source Proposition4 proof and Lemmas12-13 | Established on W intersect D0 | D0 compact; assuming L1 density of D0 would be invalid |
| Linear/smooth stable manifold | Explicit unstable line and resolvent stable functional; exact kernel counterexample | Linear statement verified; nonlinear route blocked | No uniform nonlinear L1 differentiability or stable contraction supplied |
| One-step feedback sections | Monotone implicit scalar inversion; positive sections including zero fibers | Verified, open map | Continuity alone has no modulus uniform in iterated sections |
| Backward probability-space contraction | Sharp Gram determinant identity and one polynomial positivity certificate | Independently verified | Bound is limited to the parameter/feedback rectangle used |
| Monotone transport/full L1 | Uniform accumulated distortion, unweighted source-core bound and full variation estimate | Independently verified | No remaining analytic gap within the exact original scope |

The source-first blocked routes were not reopened by assuming their missing premise. The new inverse contraction supplies materially new control, and the derivative/measure estimate supplies the second independent obstacle needed for rough densities.

## Native reproductions and custody

Frozen head H=6be98eac0ba508368218179ecf80020c037dbece and base B=efd29c05204703acca9a0860812f54b94fae54b1 were inspected read-only on main. All38 submitted scope files, including QUEUE, match disk, immutable local Git blobs, GitHub listings, and decoded GitHub blob API bytes, including Git/disk executable modes. Every old author file was compared in full against commitbe4730c4f09b4fe5cc82bbedb8cb154894124dfd and the frozen head; all25 old files are unchanged. Full old and new QUEUE bytes and their complete difference are retained privately.

All nested manifests were read and audited with complete recursive schemas, duplicate-key rejection, safe relative paths, duplicate-path checks, actual sizes/SHA256, and previous/author-manifest links. The recorded89 entries include86 public-file references and3 source references; the source-file verification status is separately recorded. Count totals are custody evidence, not mathematical proof. The manifests do not themselves bind modes; the independent Git/API/disk inventory does.

All three author programs and the prior independent program replay byte-for-byte under an existing /opt/homebrew/bin/python3.11 with SymPy1.14. Author outputs are60278,445,211 controls; the prior checker reports18678. The portable wrapper passes in public-only mode. Initial default-Python failures due to absent SymPy were preserved, including stdout, stderr, exit code, command, and UTC. No package was installed and no candidate artifact was modified. The exact independent checker reports19123 finite/exact controls and2160 separately labeled numerical controls; the latter cover720 unequal-weight feedback cases at A=.4,.001,1e-9 and B=6.000001,16 with correlated labels. Its two floating summary fields differ slightly between preexisting Python3.14 and3.11: squared-ratio maxima0.29448946075301 versus0.2944894607530101, and residual maxima4.286393288921442e-16 versus4.2991326644481465e-16. Complete original outputs and the failed whole-byte comparison are preserved. All other fields are exact across these runtimes. The read-only verify_controls.py requires every exact field to agree, permits absolute1e-12 differences only in these two labeled floating summaries, and independently enforces ratio<=.7+1e-12 and residual<1e-12. This tolerance equals the existing residual experiment threshold and is far smaller than the squared-ratio experiment's margin; it is a reproducibility convention for numerical corroboration, not a validated numerical theorem. The portable verifier itself outputs identical693 bytes under both existing runtimes. The analytic polynomial certificate supplies the universal bound; the numerical summaries do not supply the proof.

Complete native program streams and expected old output bytes are private. Public REPLAY_RECEIPTS.json records every program attempt, including failures, and complete comparison offsets/lengths/hashes. PACKET_CUSTODY.json records113 complete read-only native commands and all bindings/schemas. The official OWR and exact arXiv source hashes match the candidate's SOURCE_MANIFEST. The author-hosted full paper is an additional independently obtained source. Retrieval of the candidate's optional ESI file at its old URL initially failed in DNS through urllib; that failure is retained in the conversation's native tool output. A subsequent native curl request to the identical URL succeeded with1544891 bytes and SHA2560628d7a9acb61435d6513d919966502821ee8a38f4a9ec0a49f8e55264af1dd4. Its complete native stdout/stderr, UTC and exit metadata are retained privately, and SOURCE_CUSTODY.json binds all three exact source bytes. The source-enabled original wrapper also passes. No replacement was substituted.

## Completion estimate and publication limits

Best-guess mathematical audit completion:100% for this assigned backward-feedback family. Best-guess package completion:100%. Best-guess closure of the original discovery goal:100% within the exact theorem and credited prerequisites; historical priority and novelty remain unverified. The parent auditor read the complete draft and repaired portability checker before authorizing one final public/private closure. Root MANIFEST.json enumerates every public/private file and directory, and SEAL.json binds that manifest. Read-only final verification follows sealing; no subsequent writes are permitted in this family namespace. No merge, PR mutation, release, preprint, publication, sheet edit, or external communication was performed.
