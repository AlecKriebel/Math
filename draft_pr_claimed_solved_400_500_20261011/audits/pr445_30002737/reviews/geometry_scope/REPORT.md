# Independent geometry and source-scope review of PR 445

**Verdict: PASS within the precisely stated unrestricted, ambient-Haar scope.** I found 0 blocking findings, 0 required repairs and 0 central mathematical gaps in this review family. The verified construction is an unweighted, aperiodic, repetitive FLC Meyer set in R² with a uniquely ergodic translation hull, ambient-planar singular diffraction and a nonzero dynamical spectral measure equivalent to planar Lebesgue measure. This does not settle a separately restricted one-dimensional question, certify historical novelty, or constitute human peer review.

| Field | Frozen review identity |
| --- | --- |
| PR | 445 |
| Problem | 30002737 / OWR-13355-001, queue rank 480 |
| Eligible frozen head | `3242c84e06db7e99012c7fe581adde5c3f89fc89` |
| Reviewer | `/root/pr445_geometry_scope` |
| Gate supplied to this reviewer | Exact fresh `claimed_solved`, author 1/5, blank DOI columns, passed before source snapshot |
| New original proof-search attempts | 0 |
| Actual review scope | Primary-source interpretation; legal Rudin–Shapiro input; unweighted geometry; marker recognition; hull topology; strict ergodicity; repetitivity; aperiodicity; boundary cases |
| Files changed by this reviewer | Only this `reviews/geometry_scope/` folder |

The gate is an input to this assignment, not a claim that I independently re-ran the live queue eligibility check. The source receipt and PR metadata agree on the frozen head and selected row. The parent owns later source/queue/remote/action decisions. I made no Git state edit, commit, push, PR mutation, release, external comment or contact with another individual.

## Independence and method

I read the frozen candidate proof and its additive action/scope clarification, as the object under review, then independently obtained the primary PDFs. I recorded `INITIAL_RECONSTRUCTION.md` before consulting any other current review family's findings. I did not read the frozen historical independent audit or its checker. I subsequently read README, author manifest and research log to compare the public scope/attempt statements; their historical PASS claims were not evidence for my mathematical verdict.

The initial reconstruction identified the transverse row/column mechanism and its main failure mode: if unweighted decoration lost symbolic information, the dynamical product observable would not be justified. I tested the marker argument directly and supplied a negative control. The controls were authored afresh, use exact arithmetic, contain explicit exception checks rather than essential `assert` statements, and also pass under `python3 -O`. Finite checks supplement the analytic arguments below; they do not establish infinite ergodicity or zero correlations by sampling.

## Original target and source scope

The independently downloaded [official EMS report](https://ems.press/content/serial-article-files/46543), DOI [10.4171/OWR/2014/53](https://doi.org/10.4171/OWR/2014/53), was rendered locally. I visually inspected complete printed pp.2996–2997 (PDF pages 10–11), including van Enter's full contribution and references. Conjecture 1 states:

> If the diffraction spectrum has no absolutely continuous component, then neither has the dynamical spectrum.

Its surrounding discussion concerns configurations represented by Dirac combs and the translation representation on L² of an invariant probability measure. The statement imposes no dimension-one, spectral simplicity, irreducibility, positive-temperature, finite-range, isotropy, or “all local factors have singular diffraction” restriction. The subsequent d=2 and d≥3 Gibbs conjectures are separately numbered claims. They do not add hypotheses to Conjecture 1.

I also independently downloaded and visually read complete pp.1–4 of [van Enter's cited precursor, arXiv:1310.0267v2](https://arxiv.org/abs/1310.0267v2). Its setup on p.2 uses finite single-site alphabets indexed by Z^d. On p.3 the relevant pair-correlation Fourier measures live on R^d or d-dimensional tori, before the same spectral question. The equilibrium setting supplies motivation; the target is not limited to positive-temperature finite-range Gibbs measures. This supports the dimension-unrestricted interpretation used here. A separately imposed d=1 condition would invalidate this example's applicability, but no such condition occurs in these primary passages.

The target is instantiated with the full R² translation action. Absolute continuity therefore means absolute continuity with respect to Haar measure on its dual R². One-dimensional densities on horizontal or vertical lines are singular for this ambient Haar measure. This is also consistent with the explicit lower-dimensional-support classification on p.2 of [Baake–Grimm, arXiv:0810.5750v2](https://arxiv.org/abs/0810.5750v2), whose complete pp.1–3 I rendered and visually inspected. A line-continuous reinterpretation would change the claim being tested.

The live catalogue body at `unsolvedmath.com/problems/30002737` was not independently recovered. The web tool reported inaccessible, and a separate HTTPS attempt returned HTTP 429. The raw failure metadata and private response are preserved. This current failure differs from the older 403 recorded in the frozen package. The accessible original conjecture supplies the exact target; I do not certify what text the live catalogue currently displays. PDF/render hashes, page identities and acquisition methods are in `SOURCE_ACQUISITION.json`; foreign source bytes, extracted text, renders and catalogue response remain in `private/` and are excluded from the public manifest.

## Credited one-dimensional input and substitution legality

Let X be the binary Rudin–Shapiro shift hull, with shift `(Sx)_i=x_(i+1)` and unique invariant measure μ. The required input is minimality, unique ergodicity, balanced signs and

\[
\int x_0x_m\,d\mu=\delta_{m,0}.
\]

These are established ingredients, credited to the primary Baake–Grimm source rather than claimed as this result's new contributions. Its pp.2–3 state strict ergodicity and balanced signs, give the exact bilateral recursion with w(0)=1 and w(−1)=−1, and derive the delta autocorrelation. The candidate uses no independence among entries of a single Rudin–Shapiro sequence. Unique ergodicity gives uniform interval averages for the continuous cylinder functions x₀ and x₀xₘ.

I independently matched the proposed four-letter substitution

\[
\rho:a\mapsto ab,\quad b\mapsto ac,\quad c\mapsto db,\quad d\mapsto dc
\]

and coding a,b↦+1, c,d↦−1 to the primary bilateral sequence. The exact squared images are

\[
\rho^2(a)=abac,\quad\rho^2(b)=abdb,\quad
\rho^2(c)=dcac,\quad\rho^2(d)=dcdb.
\]

Every ρ³(letter) contains all four letters, establishing primitivity directly. The pair ca occurs in ρ²(c). Since ρ²(c) ends in c and ρ²(a) starts in a, iterating the central legal seed c|a gives a bilateral ρ² fixed configuration. In these aligned images, even positions contain only a,d and odd positions only b,c. Their coded four-letter images are +++−, ++−+, −−+−, −−−+, respectively. Consequently, for every integer n, including negative n,

\[
w(4n+r)=\begin{cases}
w(n),&r=0,1,\\
(-1)^{n+r}w(n),&r=2,3.
\end{cases}
\]

The initial values agree with the primary source. The recursion determines the bilateral sequence: for each index other than the two initial indices, the reduced index has smaller absolute size, with the exceptional reductions resolving to an initial value. This identifies the legal coded seed with the credited primary sequence and its hull, avoiding an unsupported change of Rudin–Shapiro convention. The finite control checks 8,192 letter-parity sites and 8,192 recursion sites. The infinite identification follows from the structural image argument, not these counts.

The claimed 16-letter product block substitution also has the stated primitivity: the image of (c,d) under its third iterate contains each pair from ρ³(c)×ρ³(d), hence all 16 letters. Its row/column product form is legal. No extra dynamical properties of a multidimensional substitution are needed; the proof obtains them from X×X and the explicitly recognized geometric realization.

## Geometry: a Delone Meyer set with FLC

Write

\[
e=(1/10,1/10),\quad a=(1/3,0),\quad b=(0,1/3),
\]

and place the two mandatory slots 0,e in every integer cell, the optional slot a when xᵢ=+1, and the optional slot b when yⱼ=+1. All occupied points carry weight 1. The four residue classes are distinct, so the decomposition introduces neither collisions nor disguised multiplicities.

Each Λ₍ₓ,ᵧ₎ lies in (1/30)Z² and contains Z². Thus it is uniformly discrete and relatively dense. A stronger exact separation bound is distance ≥√(1/50), obtained by minimizing all nonzero differences between motif residues and neighboring cell translates; the anchor lattice bounds the covering radius by √(1/2). These numbers are checks, not required sharp constants. The difference set lies in (1/30)Z², so it is uniformly discrete. This proves the Meyer property. For every radius, only finitely many possible differences exist; since every patch is a subset of these finite positions relative to its center, finite local complexity follows.

None of these conclusions assumes the optional slots actually occur in a particular finite patch. All-minus local data, all-plus local data and one missing decoration are included in the controls. The underlying infinite sequences are balanced; the average density is 2+1/2+1/2=3.

## The marker recovers the complete hull information

Let C={0,e,a,b}. Reducing differences modulo Z² gives

\[
\{(c,d)\in C^2:d-c\equiv e\pmod{\mathbb Z^2}\}=\{(0,e)\}.
\]

This is an exhaustive 16-pair residue calculation. Hence, for every x,y and every real translation t,

\[
\{p\in\Lambda_{x,y}-t:p+e\in\Lambda_{x,y}-t\}=\mathbb Z^2-t.
\]

There are no false anchor pairs involving optional slots, even across cell boundaries. Both slots in the unique anchor pair are mandatory, so no true anchor is lost. Looking for e is directional; it does not confuse the marker with the reverse vector −e.

The recovered lattice determines t modulo Z². At its anchor `(i,j)-t`, membership at +a recovers xᵢ, and membership at +b recovers yⱼ. The tests use bounded geometric neighborhoods. If two decorated translates are equal, their marker lattices are equal, so their phases differ by an integer pair. After this phase adjustment, their optional membership tests force equality of both sequences. Thus the encoding is injective up to the required integer suspension identifications.

The independent control examines all 1,024 arbitrary assignments of five row and five column signs, at 16 exact rational phases. It checks 16,384 pattern-phase cases and 294,912 optional slot decodes. A deliberately faulty recognition using an optional a-displacement after removing the mandatory e marker finds no anchors in an all-minus patch despite the actual anchor lattice being present. This negative control distinguishes the proof's essential mandatory marker from a false marker argument.

## Actual conjugacy, including section boundaries

Let Σ(X) be the unit suspension with `(x,1)~(Sx,0)`. The identity

\[
\Lambda_{S^mx,S^ny}=\Lambda_{x,y}-(m,n)
\]

holds exactly. Therefore

\[
\Phi([x,u],[y,v])=\Lambda_{x,y}-(u,v)
\]

is well-defined on Σ(X)×Σ(X), and increasing suspension time intertwines with negative translation of point sets. The frozen additive clarification gives this convention explicitly. Reversing the convention changes the signs of spectral variables, but not the relevant spectral type.

Continuity in the local topology is direct: a bounded geometric patch depends on finitely many x- and y-indices; a sufficiently small phase change is absorbed by the permitted small translation. At an edge u=1 or v=1, the displayed exact identity gives the same point set in the adjacent suspension chart. The control checks 400 exact representative changes, including negative integer changes and simultaneous changes of both coordinates, using a legal bilateral sequence and buffered geometric windows. The analytic identity covers all edges and corners, not just the sampled phases.

The domain is compact and the geometric hull is Hausdorff. The image contains the original real translation orbit. Integer translations yield the independent product shift action, whose orbit is dense in X×X; fractional phases cover both suspension directions. Thus the image is exactly the geometric hull. Equivalently, the compact image is closed and equals the closure of this dense orbit. Marker recovery proves injectivity. A continuous bijection from the compact domain to the Hausdorff hull is a homeomorphism, and the translation identity proves equivariance. This is a topological conjugacy, not a lossy factor map. Every limit in the hull retains this recognition because it is in the compact image.

## Strict ergodicity, repetitivity and aperiodicity

Under the full Z² action `(m,n):(x,y)↦(S^mx,S^ny)`, the orbit is the Cartesian product of two dense one-dimensional orbits, giving minimality. To verify unique ergodicity without confusing this with a diagonal action, disintegrate any Z²-invariant probability over y. Invariance under `(1,0)` makes its conditional measures on X S-invariant almost everywhere; unique ergodicity forces each to equal μ. The measure is therefore μ×ν. Invariance under `(0,1)` forces ν=μ. The product measure is the only invariant probability.

Unit-roof suspension preserves minimality and has the unique invariant measure obtained from μ and uniform phase. For the product R² action, the same independent-coordinate argument gives μ×μ×du×dv in canonical `[0,1)²` coordinates. The conjugacy transfers these properties to the geometric hull. Minimality of an FLC Delone hull gives repetitivity: the return sets of a patch neighborhood are relatively dense by compactness and minimality. The invariant measure gives uniform patch frequencies through uniform ergodic averages, with local patch boundaries handled by the common phase and FLC description.

For aperiodicity, first observe that X has no periodic element. If it had a period-q point with q≠0, minimality would make X that finite orbit. The credited correlation at q would then be 1, contradicting δ₍q,0₎=0. Any point-set translation period must preserve the recovered marker lattice, hence must be an integer pair `(m,n)`. The optional slot decoding then imposes `S^mx=x` and `S^ny=y`. Neither factor has a nonzero period, so m=n=0. The zero-coordinate cases do not leave a hidden row or column period. This argument concerns translations; no rotation or reflection is included in the source action.

## Spectral bridge and boundary checks

Although the main review family concerns geometry and scope, I reconstructed the two spectral claims to verify that the conjugacy delivers the advertised counterexample.

Decompose the unweighted comb into the periodic motif mean

\[
D=\delta_0+\delta_e+\tfrac12\delta_a+\tfrac12\delta_b,
\]

and the two centered row/column contributions. This is an algebraic decomposition of an unweighted measure, not a weighted construction substituted for it. Uniform zero means kill all periodic-centered cross terms; the mixed row-column term separates into a product of vanishing one-dimensional means. The centered self-correlations are `(1/4)δ₀⊗δ_Z` and `(1/4)δ_Z⊗δ₀`. Fixed motif offsets alter only O(N) boundary sites in a square with area O(N²), so they do not change any limiting coefficient. The discrete difference lattice makes coefficient convergence sufficient for vague convergence. Thus

\[
\gamma=(D*\widetilde D)*\delta_{\mathbb Z^2}
 +\tfrac14(\delta_0\otimes\delta_{\mathbb Z}
 +\delta_{\mathbb Z}\otimes\delta_0).
\]

Fourier transform yields lattice atoms plus `(1/4)(λ⊗δ_Z+δ_Z⊗λ)`. The entire diffraction is carried by `(R×Z)∪(Z×R)`, a countable union of planar-null lines. The line terms have no point atoms, even at line intersections. Hence the ambient absolutely continuous part is zero. The zero-displacement coefficient is 3 and the origin Bragg intensity is 9, agreeing with density and its square.

On a unit suspension, the bounded measurable section function h([x,u])=x₀ has conditional correlation δ₍floor(u+t),0₎. Its phase integral is

\[
C_h(t)=\int_0^1 1_{\{0\le u+t<1\}}du=(1-|t|)_+.
\]

This covers negative times, integer times and endpoints; the section edge has measure zero. Its spectral density is sinc²(k), with the continuous value 1 at k=0. Multiplying the two suspension observables gives correlation `(1−|t₁|)₊(1−|t₂|)₊` under the full R² action, and density sinc²(k₁)sinc²(k₂). The zero set is the countable union of lines where either coordinate is a nonzero integer, hence is planar null. The density integrates to 1 and is positive almost everywhere. The measure is equivalent to planar Lebesgue measure. The established actual conjugacy transports this measurable L² observable to the unweighted point-set hull. Its discontinuity across the section is permitted for dynamical spectral measures.

The complete dynamical representation need not be purely absolutely continuous; a single nonzero absolutely continuous spectral measure suffices to contradict the target. The argument asserts no exact multiplicity. The full R² action is essential: restricting to a single direction changes both the reference Haar measure and the spectral question. Likewise, replacing two independent product coordinates by the same sequence under a diagonal action would require a different argument. The proof does neither.

## Adversarial outcomes and exact remaining limits

| Attack | Evidence and result | Status / remaining gap |
| --- | --- | --- |
| Hidden d=1 restriction | Complete OWR contribution and d-dimensional precursor inspected | Rejected for the printed target; separate d=1 claim unaddressed |
| Lower-dimensional density incorrectly called planar AC | Physical diffraction supported on countable transverse lines; primary classification checked | Rejected; ambient Haar convention explicit |
| Slot collisions or false directed markers | Exact residue enumeration, exhaustive local controls and mandatory-marker negative control | Rejected; no geometry gap |
| Observable lost under decoration | Explicit phase and sign recovery; compact equivariant bijection | Rejected; actual conjugacy established |
| Illegal bilateral seed / wrong RS convention | Legal ca seed, ρ² gluing, parity/image derivation, exact primary recursion | Rejected; credited infinite input applies |
| Product joining used without justification | Independent coordinate invariance and disintegration | Rejected for full Z²/R² product action |
| Period survives in one direction | Marker lattice forces integer period; each factor has no nonzero period | Rejected |
| Section edges, negative times or sinc zeros break AC | Exact gluing, triangle formula for all real times, planar-null zero lines | Rejected |
| Finite checks substituted for infinite proof | Controls explicitly limited; analytic topology and credited input separated | Rejected |
| Claimed novelty or live catalogue verification | Neither certified here; current catalogue access failed | Open historical/data-access limits, not central mathematical gaps |

The strongest verified result is the complete planar counterexample within the unrestricted ambient-Haar formulation, using the established Rudin–Shapiro input. No central mathematical claim was transferred to an equivalent unproved assertion. I found no mandatory repair within this assigned family. A deep historical-priority audit, present-day openness certification, human review and an independently recovered live catalogue statement remain outside this result. Those limits must remain visible if the result is promoted.

Reproduction: run `python3 geometry_controls.py` or `python3 -O geometry_controls.py` from this folder. The adjacent result JSON is deterministic. The final authored payload list is `PUBLIC_FILES.json`; it excludes every private/foreign file. This report is sealed for this frozen head and this review scope only.
