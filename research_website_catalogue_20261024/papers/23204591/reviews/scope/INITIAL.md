# Independent paper-first reconstruction: row138, record23204591

This INITIAL follows personal reading of all five published PDF pages, all329 lines of the sole controlling main.tex, and all five fresh individual own page rasters. It precedes native scientific code, native results, scientific support README bodies, archived audits/triage/opinions, current peer/root findings and new foreign scientific primary bodies. The source-custody utility has read source payloads as opaque bytes for hashes/CRC only; it neither imports nor executes them. Source-stage unread fields remain unchanged historical data.

The manuscript is **Bilinear ergodic Hilbert variation for commuting transformations as a consequence of annular triangular variation**, Alec Kriebel, printed October6,2026, with no printed version observed. The actual native metadata version is the string1.0.0. These are separate observations. This is an extensive independent AI review, not human peer review or formal certification. The root138 comparison gate is CLOSED.

## Exact target and hypotheses

On an arbitrary probability space, S and T are invertible measurable measure-preserving transformations with measurable inverses and ST=TS. For complex f,g in L3, the truncation is

    H_0=0,
    H_N(x)=sum_{0<|n|<=N} f(S^n x) g(T^n x)/n.

For every finite real r>2, the target is a universal L^(3/2) bound on the pointwise homogeneous r-variation over all increasing nonnegative integer endpoint lists, with the supremum inside the norm and no bound on list length. The constant depends on r and the imported analytic constant, not on the probability space, transformations or functions. The same constant controls the maximal function. The truncations converge almost everywhere and in L^(3/2) to a complex bilinear operator, and the L^(3/2) norm of the pointwise supremum of the tails tends to zero.

The specified imported hypothesis is the global full annular inequality for

    B_{a,b}(F,G)(u,v)=integral_{a<|t|<b} F(u+t,v)G(u,v+t) dt/t,

with F,G in L3(R2), output L^(3/2), every r>2, all positive rational endpoint partitions, arbitrary finite partition length, and a spatially dependent partition permitted in the pointwise supremum. The paper attributes that inequality to the October5 manuscript at exact source pin adc7f1241b42e322a6451854ab7e4b4c146bf78a. Its validity and exact interface are pending primary reading. A maximal theorem, variation only on dyadic radii, an inequality with the partition supremum outside the norm, or a fixed-length estimate would not establish the stated input. An older Lean maximal theorem does not certify it.

The task is to review the original full statement and that actual dependency. Merely proving a conditional implication from the displayed continuous inequality would leave the imported input unchecked; it is not a substitute final disposition. A defect in the imported theorem's required scope would affect the full claim and must be recorded/deferred, not hidden by replacing the target with a weaker corollary.

Success requires a genuine all-scale restriction and error-variation bound, a finite-window transfer with correct quantifiers and exponents, measure-theoretically sound passage to the supremum and limit, and direct examination of the exact necessary foreign theorem and attribution interfaces. No finite computation can establish those universal claims.

## Family A: reconstruct the fixed-width restriction for all phases and signs

Take h=1/8 and q=1/16. Around each lattice site place one square of side2h, extending finite arrays A,B as constant functions F,G and zero elsewhere. The input square area is4h²=1/16. At (i+a,j+b), |a|,|b|<q, fixed coordinates select the row j of F and column i of G. An overlap of moving-coordinate windows indexed by k,l would imply

    |k-l| <= 2h+|a-b| <= 3/8 < 1,

so k=l. The exact same-index overlap is I=[-h-min(a,b), h-max(a,b)]. Its length ell=2h-|a-b| lies between1/8 and1/4, and |s|<=3/16 on I. There is one lattice product on each window k+I. This proves the geometric identity uniformly on an output phase set of fixed positive area; it does not evaluate an almost-everywhere inequality on a null set of phases.

Let rho_N=N+1/2. For every nonzero integer k, the absolute-value image of k+I lies within [|k|-3/16,|k|+3/16]. Consequently the annulus rho_M<|t|<rho_N includes the entire window exactly when M<|k|<=N, and is disjoint from it otherwise. This argument uses |k| and applies to negative k without reversing an integration sign incorrectly. The central k=0 window lies in |t|<=3/16 and is excluded even for the smallest endpoint rho_0=1/2. No principal value is invoked in this exact identity.

Write K_k=integral_I ds/(k+s)=ell/k+delta_k. For either sign of k,

    1/(k+s)-1/k = -s/[k(k+s)],
    |k+s| >= |k|-3/16 >= (13/16)|k|.

The second inequality follows universally from (3/16)(|k|-1)>=0. Integration therefore gives |delta_k|/ell <= (3/13)/k². These statements are interval inequalities for all phases and all nonzero integer k, not a conclusion from a phase grid. Reflection also gives I_{-a,-b}=-I_{a,b} and K_{-k}(-a,-b)=-K_k(a,b), a useful independent sign check.

For any integer endpoint list the radial shells of the error increments are disjoint. Since r>=1, their l^r norm is at most their l^1 norm. Thus the entire error variation divided by ell is bounded pointwise by

    e(i,j)=(3/13)sum_{k!=0}|A(i+k,j)B(i,j+k)|/k².

Hölder with exponents3,3 and output3/2, followed by Minkowski and translation invariance, yields ||e||_(3/2) <= (pi²/13)||A||_3||B||_3, since sum_{k!=0}1/k²=pi²/3. Bounding each error truncation separately would not by itself control arbitrary variation; disjoint shells are the necessary stronger mechanism.

Half-integer endpoints are positive rationals, so each restricted integer partition is admissible for the imported pointwise supremum W. The variation triangle inequality and ell^-1<=8 give V^r(h_N)(i,j)<=8W(i+a,j+b)+e(i,j) for almost every phase. All integer lists and sites form a countable family, allowing one common null set. Integrate over disjoint output squares of area4q²=1/64. The left-hand norm acquires factor(1/64)^(2/3), while ||F||_3||G||_3=(1/16)^(2/3)||A||_3||B||_3. Dividing the output area factor gives exactly

    D_r=8*4^(2/3)*C_r+pi²/13.

The analytic coefficient cubed, after factoring C_r, is8³*4²=8192. This is a scaling check, not a numerical estimate for C_r. The proof is provisionally coherent as a universal conditional restriction; the imported W inequality is still unverified at this stage.

## Family B: reconstruct the orbit-array transfer independently

Fix a finite endpoint cutoff M before choosing the orbit-window radius L. Let Q_L=[-L,L]² intersect Z², and use arrays

    A_x(i,j)=f(S^i T^j x) 1_{Q_(L+M)}(i,j),
    B_x(i,j)=g(S^i T^j x) 1_{Q_(L+M)}(i,j).

For (i,j) in Q_L and |n|<=M, the necessary array sites (i+n,j) and(i,j+n) belong to Q_(L+M). Commutation is used exactly in the second coordinate identity T^n S^i T^j=S^i T^(j+n); the first coordinate shift alone does not require it. The resulting equality h_N(A_x,B_x)(i,j)=H_N(f,g)(S^i T^j x) holds for every N<=M. Stabilizers, periodic actions and S=T cause repeated samples but no problem: no free action or ergodicity is required.

Let W_M be the maximum over endpoint lists contained in {0,...,M}. It is a finite maximum of measurable functions, with pointwise choice of the maximizing list retained. Raise the discrete norm inequality to p=3/2 and sum only over Q_L. The array l3 norms raised to p become powers1/2 of sums of |f|³ and |g|³. Integrate using invariance on the left and Cauchy–Schwarz on the right:

    |Q_L| ||W_M||_p^p
    <= D_r^p |Q_(L+M)| ||f||_3^(3/2) ||g||_3^(3/2).

Every right-hand integral is finite, so this inequality proves integrability rather than presupposing it. For fixed M, |Q_(L+M)|/|Q_L| tends to1 as L tends to infinity. Only afterward let M tend to infinity. W_M increases to the full countable pointwise variation because every finite list lies inside one such cutoff. Monotone convergence completes the transfer without assuming a measurable choice of an infinite partition.

This order of limits is material. Allowing M to grow with L would retain a boundary ratio, and allowing M to be infinite before finite-array restriction would lose the support hypothesis. The source states the correct fixed-M order.

## Family C: measurable representatives, convergence and bilinearity

L3 representatives are finite outside measurable null sets. Their preimages under all finite words in S,S^-1,T,T^-1 form a countable union of null sets; remove it to obtain an invariant full-measure set where every required orbit value is finite. If commutation holds modulo null sets, also remove word-preimages of its failure set. This uses measurable inverses and measure preservation. It does not require a standard probability space, completeness of the sigma algebra or a common exceptional set for uncountably many different input pairs.

For a fixed input pair choose r=3. Finite r-variation forces a scalar sequence to be Cauchy: a non-Cauchy sequence supplies an epsilon>0 and arbitrarily late ordered pairs separated by epsilon. Choose J strictly separated pairs recursively. A partition containing their endpoints has variation at least epsilon*J^(1/r), a contradiction as J grows. Completeness of C supplies a finite limit. The limit and each countable supremum tail are measurable.

Because H_0=0, H_*:=sup_N|H_N|<=V^3(H_N), so H_* is in L^(3/2). The limit satisfies |H|<=H_*, and sup_{N>=m}|H_N-H| is bounded by2H_* and tends pointwise to zero. Dominated convergence applied to the pth power proves the stated supremum-tail norm convergence, which is stronger than mere convergence of each H_N in norm. Norm limits of the exact complex bilinear identities for finite H_N give a complex bilinear operator on L3 equivalence classes; no joint pointwise representative for every input is claimed.

## Family D: falsifiers and boundary controls

1. A bounded alternating scalar sequence has infinite finite-r variation. For a_N=1 at odd N and0 at even N, a_0=0, the full variation through M has cube M at r=3, while maximal size is1 and dyadic variation remains bounded. This rules out replacing the full imported input by a maximal or dyadic estimate.
2. Uniform bounds for individual partition norms do not imply a bound for the norm of the pointwise supremum. On atoms of masses2^-j, the functions2^(j/p)1_{atom j} each have Lp norm1, while their supremum has infinite Lp norm. This is a logical counterexample to moving the supremum, not a constructed counterexample to the actual Hilbert theorem.
3. Point evaluation on lattice phases is not controlled by an Lp(R²) norm: an indicator of Z² is zero almost everywhere but equals1 on every lattice point. The fixed positive output area avoids precisely this problem.
4. A one-sided harmonic sum with S=T=id and nonzero f*g diverges. Symmetric truncation and the odd kernel are essential to the claimed scope. The actual theorem does not assert one-sided convergence.
5. For S=T=id the actual symmetric H_N is identically zero. For S=id it reduces to f times the ordinary ergodic Hilbert sums of g; for T=S^-1 it falls within the opposite-power setting. These limiting cases should be consistent with the full proof. No r=2, noncommuting or different-exponent theorem is inferred.
6. A small noncommuting permutation action should make the orbit-array equality fail at its identified commutation step. This is a negative control for the transfer mechanism, not a failure of a hypothesis-satisfying example.
7. The k=0 window, negative k windows, phases at the closed edges of the larger rational phase grid, M=0, N=1 and zero arrays are useful exact bookkeeping boundaries. Actual proof constants are uniform over the full open phase square, not just those checks.

## Primary and attribution obligations after this seal

Read the actual pinned annular manuscript and its exact statement/definitions and proof mechanism; check global versus localized scales, pointwise versus norm variation, partition cardinality, rational endpoints, complex functions, normalization and uniform constants. A source URL, title, search snippet, old audit PASS or older maximal Lean statement cannot discharge this obligation.

Read actual critical comparison bodies: Demeter's cited v1 Theorem1.2, Becker–Durcik's cited v1 Corollary1.4 and discussion of(1.8), Demeter–Thiele Section6/footnote36, Durcik–Kovac–Skreb–Thiele Section5 and the classical transference context. Identify exact editions and categories. The paper explicitly credits existing transference/restriction machinery and the new continuous input. No worldwide absence or earliest-public-disclosure conclusion follows from its printed dates or a bounded search.

Only after this INITIAL and an actual separate own-results freeze should supplied code/results or new foreign bodies be read. The other owner alone executes the native scientific checker. I will not execute it, its duplicates, a builder, old campaign, renderer from the package or any source helper. Fresh own exact controls and a proof note can test the independent mechanisms above; their finite scope and actual execution chronology must be explicit.

## Status and remaining gap at INITIAL

The local all-phase restriction, transfer and convergence mechanisms have been reconstructed in ordinary mathematics and subjected to the distinct attempted falsifiers above. No hypothesis-satisfying counterexample to those local implications is presently identified. The complete original theorem is not yet endorsed: the new imported continuous theorem and exact attribution/edition interfaces remain to be checked in their actual bodies. No follow-up research question is justified at this stage; the default is null. No repair, narrowed replacement or publication decision has been made.
