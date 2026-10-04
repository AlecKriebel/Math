# Independent exact-algebra and uniform-parameter review of PR359

Final sealed review after root approval. Mathematical family assessment: **PASS within the exact original model and parameter range; no mandatory mathematical correction found.** Final package sealed at 2026-10-03T22:26:56.169015+00:00. This is an AI-assisted research audit, not human peer review. Historical novelty and priority remain unverified.

The strongest verified result in this family is the probability-space inverse contraction, uniformly over the full continuous parameter domain, together with the exact Möbius transfer identities and the accumulated-distortion bounds needed by the candidate's full-density approximation. The candidate's complete boundary proof is consistent with these results and its stated analytic regularity. All three submitted source-manifest payloads were freshly byte-verified, including an ESI download succeeding after two preserved native DNS failures. The full author-hosted paper preceded candidate access, but the full arXiv variant reading followed it; that procedural limitation is recorded below.

## Binding and independent baseline

Target is problem30001370, PR359, frozen head `6be98eac0ba508368218179ecf80020c037dbece`, base `efd29c05204703acca9a0860812f54b94fae54b1`. All 37 files in `problems/30001370_basin_boundaries` and `unsolved_math_prioritization/QUEUE.md` were checked: 38 total. The frozen snapshot is distinct from the historical author checkpoint `be4730c4f09b4fe5cc82bbedb8cb154894124dfd`.

Before candidate proof, code or verdict access, an independent source/model baseline was sealed at 2026-10-03T22:01:56.518962+00:00. Its SHA256 is `16b2d280f5c94652d1b902119c2fd8fcfb7010764bb64cc24ec3c7b4137fda9c`; see SOURCE_FIRST_BASELINE.md and SOURCE_FIRST_SEAL.json. No sibling family analysis was read. The full author-hosted BKZ logical sections were read before candidate access; the arXiv model was cross-checked before access, and its full text was read subsequently. The source-first baseline explicitly recorded that variant cross-check was still in progress, rather than claiming premature completion. This preserved independence of the primary model and author-hosted paper analysis, but did not satisfy a strict requirement to finish every version's full text before candidate access.

The source claim comes from Keller's contribution, printed pp. 2713–2715 in [OWR49/2009](https://ems.press/content/serial-article-files/46250). It asks whether the basin of 1 equals both stable basins' boundaries, relative to all probability densities in L1, for 0<A<=2/5 and 6<B<=16. The credited [Bardet–Keller–Zweimüller paper](https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf), CMP 292(2009), 237–270, establishes global convergence and openness and the boundary result within its analytic mixture class. [arXiv 0812.4040v1](https://arxiv.org/abs/0812.4040) supplies a separately identified version. The full finite-system limiting-mixture question alpha = 1/2 is a different conjecture and is not answered by this candidate.

Fresh source SHA256 identities are: OWR `b4a8d328316d093cde2d23a9b13e8b869e33b46626735494de473045bbc26169` (320856 bytes); author-hosted BKZ `c1b9ca5c4edbba4d06513634a649589185a63a53f0b0a9f14ebb8a9fc8289642` (541479 bytes); arXiv v1 `6a182868c1d2d4a09c8cfaa513ba9314cce522c3b08fe71728264399df7d7861` (462269 bytes). The author's rendered manuscript date is December 19, 2008; the downloaded arXiv PDF renders November 10, 2018 while its version identifier/submission timestamp is v1/December 21, 2008. No equivalence of byte-distinct versions or inspection of the final journal PDF is asserted. Raw PDFs and extraction output remain private.

## Exact reconstruction and sensitivities

Let I=[-1/2,1/2], J=[-1/2,3/2], and

\[
 f_r(x)=\frac{(r+4)x+r+1}{2rx+2},\qquad
 b_r(z)=\frac{2z-r-1}{r+4-2rz}.
\]

The two branches of T_r are f_r and f_r-1, separated at-r/4. The inverse branches on I are b_r(y) and b_r(y+1). Direct algebra gives

\[
 f'_r(x)=\frac{4-r^2}{2(1+rx)^2},\quad
 \partial_z b_r(z)=\frac{2(4-r^2)}{(r+4-2rz)^2},\quad
 \partial_r b_r(z)=-\frac{1-4b_r(z)^2}{4-r^2}.
\]

All denominators are separated from zero on |r|<=2/5: 1+rx>=4/5 on I, and r+4-2rz>=16/5 on J. The minimum branch expansion is 2(2-|r|)/(2+|r|)>=4/3. The sharp uniform inverse spatial bound is 3/4, and the inverse parameter bound is 25/96. The negative sign in the last derivative is correct and makes the implicit feedback residual increasing. There is no omitted moving-cut derivative in the branchwise pushforward formula: the two increasing full branches cover I, and the cut is null for absolutely continuous laws.

For h_r(x)=(x+r/4)/(1+rx), h_r^{-1}=h_{-r} and f_r=2h_r+1/2. Thus F=P_0 K with K(u)=P_{h_{G(phi(u))}}u. For target v, the inverse parameter solves r=G(integral h_{-r}v); monotonicity and endpoint signs establish a unique root. Its bound B/2 in the L1 distance of targets and joint strong transport continuity give the homeomorphism used in turn1. Strong continuity uses approximation by continuous functions and transport isometry; operator-norm continuity on all L1 is not asserted.

The mixture branch formulas independently simplify to

\[
\sigma_r(y)=\frac{2(y+r)}{(r+1)y+r+4},\quad
\tau_r(y)=\frac{2(y+r)}{(r-1)y-r+4},\quad
p_r(y)=\frac12-\frac{r+y}{4+ry}.
\]

Both derivatives in r and y are positive on |r|<=2/5, |y|<=2/3. Their corners preserve [-2/3,2/3]. The normalized branchwise pushforwards of w_y(x)=(1-y^2/4)/(1-xy)^2 equal p_r(y)w_sigma and(1-p_r(y))w_tau, respectively, not merely an unnormalized resemblance. Each w_y lies between 1/2 and 2. Therefore every external parameter product applied to 1 has the same bounds. This calculation is enough for the candidate's unweighted derivative estimate; no regularity of its original density is inferred from the mixture core.

## Uniform inverse contraction on arbitrary probability spaces

For a J-valued bounded random variable Z, solve r=G(Eb_r(Z)), then set X=V(Z)=b_r(Z). The scalar residual derivative is 1+G'(Eb_r(Z))E[(1-4b_r(Z)^2)/(4-r^2)]>=1. For a bounded linear interpolation of Z, differentiation under expectation is valid for each fixed A>0 because b_r and its derivatives are bounded on the compact rectangle. The rank-one differentiated inverse is

\[
 \dot X=\left(I-\frac{\beta qE}{1+\beta Eq}\right)D^{-1}\dot Z,
 \qquad q=1-4X^2\in[0,1],\quad \beta=\frac{G'(EX)}{4-r^2},
\]

where D multiplies by f'_r(X). It acts on real probability-space L2 with arbitrary, unequal or continuous probability weights.

The norm estimate is valid. For a vector with nonzero projection onto q, rescale it to q-p with p perpendicular to q. Put v=||q||^2<=Eq and t=||p||. Its transformed norm squared is bounded by v(1+beta t)^2/(1+beta v)^2+t^2, because |Ep|<=t. The cross term uses 2sqrt(v)t<=v+t^2. The maxima of beta sqrt(v)/(1+beta v)^2 and beta^2 v/(1+beta v)^2 over v>=0 are 9sqrt(beta)/(16sqrt(3)) and beta/4. Thus the claimed bracket bound follows. Vectors perpendicular to q follow by a limit; q=0 and beta=0 give the identity directly. No rescaling exception or denominator-zero case is missing.

The tanh feedback identity is essential. If a=|r|, then

\[
G'(EX)=B(1-r^2/A^2)\le16-100a^2,\qquad
\beta\le\beta(a)=\frac{16-100a^2}{4-a^2},\quad0\le a\le2/5.
\]

This uses r=A tanh(BEX/A), not an arbitrary independent r,g pair. Combining multiplication and rank-one bounds, and 9/(16sqrt(3))<1/3, gives the continuous squared envelope

\[
 U(a)=\frac{(2+a)^2}{4(2-a)^2}
       \left(1+\frac{\sqrt{\beta(a)}}3+\frac{\beta(a)}4\right).
\]

The author's forty intervals really cover [0,2/5], with no holes or open endpoint exception. beta'(a)=-768a/(4-a^2)^2 is nonpositive and the other factor increases. The integer root ceilings bound sqrt(beta) in the required direction and are minimal. All forty rational row values were independently regenerated and compared with the complete CSV. Their maximum is 31935269/35322000<91/100<(24/25)^2. Hence||V(Z)-V(Z')||_2<=24/25||Z-Z'||_2 follows by integrating the bounded path derivative. The counting of intervals or assertions alone is not the proof; the monotonicity, coverage and integer inequalities are.

### Distinct continuous certificate

As a separate mechanism, eliminate the square root. Write L(a)=(2+a)^2/[4(2-a)^2] and C(a)=91/[100L(a)]-1-beta(a)/4. Algebra gives

\[
C(a)=\frac{R(a)}{25(2-a)(2+a)^2},\quad
9C(a)^2-\beta(a)=\frac{P(a)}{625(2-a)^2(2+a)^4},
\]

with R(a)=559a^3+1846a^2-1292a+328, and

\[
P(a)=2749829a^6+18324452a^5+17679340a^4-38590240a^3
     +26922160a^2-7787968a+808256.
\]

The Bernstein coefficients of R over[0,2/5] are 328,2336/15,2048/25,17792/125, all positive. The Bernstein coefficients of P are all positive over both [0,1/5] and [1/5,2/5]; the complete exact lists are in UNIFORM_CERTIFICATE.json. The smallest coefficient on the second interval is 770957248/46875>0. Since Bernstein basis functions are nonnegative and sum to 1, this proves C>0 and9C^2>beta everywhere, hence U(a)<91/100 everywhere. check_uniform_algebra.py derives these coefficients with Fraction arithmetic and no imported candidate code; check_symbolic_equations.py independently verifies the displayed polynomial numerator identities. This is a continuous proof, distinct from either submitted grid certificate. The extra 80 feedback-boundary and 1764 Gram-matrix controls are finite falsification controls only.

## Boundary and limiting parameter checks

The estimates survive A tending to 0 through positive values: they need G'<=16 and its algebraic relation to r, not a uniform G'' bound. G'' scales as 1/A, so claiming a uniform second-derivative estimate would fail; the candidate makes no such claim. A=0 is outside the theorem and does not define the same feedback formula. For fixed A the interpolation differentiation is ordinary smooth differentiation, and its resulting first-derivative bound is uniform in A.

The inverse constants remain uniform as B decreases to 6 from above. The basin theorem still uses B>6 to have two noncentral stable states. At B=6 these states coalesce, so its boundary formulation does not extend merely because the inverse estimate persists. B=16 is included explicitly. At r=0 the envelope is 2/3 and the actual differentiated inverse is well-defined. At a=2/5, beta(a)=0 and U(a)=9/16; this closed saturation endpoint is covered despite finite tanh values actually satisfying |r|<A. Near saturation beta decreases to 0 and all implicit denominators remain >=1. Both signs of r are handled by a=|r|. No division by B-6, r, A-dependent norm, or small terminal density enters the distortion proof.

Source Assumption I is separately compatible with the domain:25-50a-(16-100a^2)=100(a-1/4)^2+11/4>0. The global convergence and boundary seed are credited source theorems; this audit does not relabel its exact inverse certificate as a new independent proof of every numerical assertion in the source's appendix.

## Distortion, mass, regularity and total variation

Using the same original branch labels on the fixed original probability space cancels them in the input difference. It requires no independence. The L2 estimate yields Delta_j<=16 kappa^{n-j}epsilon and sum Delta_j<=384epsilon. The global lifts glue at every original cut because b_r(1/2)=-r/4 and the later lift fixes both endpoints. The uniform recurrence d_j<=3d_{j+1}/4+(25/96)Delta_j gives d_0<=101epsilon and sum d_j<=403epsilon. The latter follows by summing the recurrence with the terminal term 3epsilon; no index is dropped.

The logarithmic derivatives satisfy

\[
|\partial_x\log f'_r|\le1,\qquad
|\partial_r\log f'_r|\le\frac{35}{24}.
\]

Consequently the derivative product has |log R_n|<=403epsilon+(35/24)384epsilon=963epsilon. The candidate's weaker 964 is valid. The ratio contains no u_n denominator, so zero-density intervals do not invalidate it.

For each finite n, the original cylinder maps are smooth with derivatives bounded above and below. Composing an absolutely continuous later lift with these smooth bi-Lipschitz maps preserves absolute continuity and pulls its exceptional derivative-null sets back to null sets. A generic composition-of-absolutely-continuous-functions rule, which would be false without qualifications, is not being used. The lift need not be strictly increasing. Its terminal derivative u_n need not be bounded or square integrable.

The cumulative terminal correction sends the absolutely continuous terminal law to uniform law, even if that law vanishes on intervals. Each branch-event sublaw at a backward step is dominated by the next absolutely continuous law. Its smooth inverse-branch image remains absolutely continuous; the parameter solved by the inverse is the mean feedback of that image law. Thus the backward law is a genuine F-orbit with F^n v_n=1.

The unweighted transfer identity gives integral|u_n(X_n)-1|dx=integral|u_n-1|a_n dy<=2epsilon because a_n=P_sequence1<=2. Replacing dx by u dx here would require an uncontrolled square of u_n; the candidate correctly avoids that replacement. It follows that||H'_0-1||_1<=2epsilon exp(964epsilon)+exp(964epsilon)-1.

For nondecreasing, onto, absolutely continuous H, the identity H_*(H'dx)=dx follows from the fundamental theorem of calculus applied to antiderivatives of continuous test functions; flats are allowed. Pushforward contracts full variation of finite signed measures. Comparison with a continuous density approximation g gives the candidate's estimate

\[
\|v_n-u\|_1\le2\|u-g\|_1+\omega_g(101\epsilon)
 +\|g\|_\infty[2\epsilon e^{964\epsilon}+e^{964\epsilon}-1].
\]

This proves L1 convergence after first fixing g, then letting n tend to infinity, then letting its approximation error tend to 0. The intermediate pushforward of gdx may have atoms; the inequality is measure-level, while the v_n law was separately proved absolutely continuous. The order of limits requires no uniform rate of convergence of F^n u. Thus arbitrary roughness, zero sets and unbounded densities do not introduce an analytic gap in this family.

Turn1's exact positive sections on zero fibers and open-map factorization establish completely invariant stable-basin boundaries. Credited boundary contact at 1 propagates to every finite preimage, and closedness plus the preceding approximation puts all W in each boundary. The disjoint open stable basins and global convergence provide the converse. This is the original relative-L1 conclusion.

Turn2 is not a dependency. Its polynomial witness confirms ker(phi) is not invariant under P_0, and its resolvent functional defines the correct stable kernel. Strong L1 stability and BV exponential stability are distinguished. The program's Fourier-control comment overstates what it executes: it checks integer frequency recurrence, not a symbolic trigonometric cancellation identity. That cancellation is directly valid from the two branches and is analytically stated in the turn; this is a minor description issue, not a mandatory mathematical correction or evidence for a nonlinear L1 stable manifold.

## Native reproduction and full manifest semantics

All five submitted Python programs were fully read and run with their original frozen bytes, with SymPy 1.14.0 supplied by the already existing private runtime. No installation or runtime alteration occurred. Complete stdout and stderr are retained privately. The three author programs and prior independent checker all exit 0 with empty stderr; their entire stdout bytes equal their saved receipts, with SHA256 9ea3d3...,215607...,58d0e8...,98f4c1..., respectively. The wrapper exits0 with empty stderr and has no saved original wrapper-stdout receipt to compare; its stdout honestly says source hashes not checked. All candidate snapshot bytes remain unchanged. See NATIVE_REPLAY_RECEIPT.json. Counts 60278+445+211=60934 and 18678 agree with submitted declarations; they establish reproduction, not analytic proof.

check_frozen_namespace.py is read-only and restricts itself to the exact submitted namespace. It independently verifies the 38 raw lengths/SHA256/Git SHA1/modes100644, all 123 root native-capture stream lengths/hashes/exits, 38 Git tree identities,38 raw Git blobs and 38 decoded GitHub API blobs. All complete streams match their root receipts. The only root capture with nonempty stderr is the successful fetch progress stream, 121 bytes; it is preserved and not hidden.

The nested manifests contain 86 byte/hash declarations: 7+5+7 in the historical turns,24 in the final author manifest,7 in the review manifest and36 in the publication manifest. Every one validates. Previous-manifest references and the review's author-manifest binding validate. The 25 historical remote-author entries have correct Git blob identities. The publication's author_head refers to that historical checkpoint and its fresh_main_parent equals B; neither is silently relabelled as H. Pending-review language in historical author files and claimed-solved labels in later disposition files are intentionally distinct declarations. They are not independent proof or fresh novelty evidence. QUEUE's only diff changes this target's state from queued 0/5 to claimed_solved 3/5.

The fresh OWR, arXiv and ESI payloads match all three submitted SOURCE_MANIFEST source entries. Python native acquisition of the ESI URL twice failed DNS Errno8; the repeat has complete native streams with exit 1, 33 stdout bytes and 4573 stderr bytes in SOURCE_FAILURE_RECEIPT.json. The initial direct tool traceback was not saved as a separate native file and is explicitly disclosed. A later fresh curl download of the original URL succeeded at 2026-10-03T22:22:35.198159+00:00: 1544891 bytes, SHA256 `0628d7a9acb61435d6513d919966502821ee8a38f4a9ec0a49f8e55264af1dd4`, exit 0 and empty stdout/stderr. No sibling mathematical analysis or source import was read for that acquisition.

The original wrapper was then run with all three payloads at 2026-10-03T22:23:08.163134–22:23:10.517480+00:00. It exited 0 with empty stderr and 510 stdout bytes, SHA256 `7f08bd970b49b4b39b2422b3def4a4250f43411b3f2c096cd6086476e3422007`; all four receipt comparisons and all three source hashes passed. There is no original saved wrapper stdout to compare, so no such equality is claimed. Snapshot bytes remained unchanged. SOURCE_REPLAY_RECEIPT.json records the full metadata, with raw streams private; both earlier failures remain retained. This resolves the earlier ancillary source-byte gap.

## Mechanism/evidence/status map and exact remaining gap

| Family mechanism | Evidence | Status | Exact gap or limit |
|---|---|---|---|
| Primary model reconstruction | Sealed source-first equations and credited input comparison | Verified | Final journal PDF and global historical novelty are not certified |
| Source-first reading order | Full author-hosted paper before candidate access; arXiv model before access and full variant afterward | Qualified | Strict full-reading-before-access requirement was not met for the arXiv variant |
| Direct Möbius inversion and transfer |26 exact symbolic identities, hand sign/denominator derivations | Verified | No implication for other maps |
| Continuous inverse norm | Hand probability-space rank-one derivation, original exact covering CSV, independent Bernstein proof | Verified | The theorem excludes A=0 and needs B>6 for its basin interpretation |
| Rough-density distortion/TV route | Unweighted transfer bound, finite-cylinder AC argument, signed-measure pushforward estimate | Verified in analytic family audit | Depends on the cited global convergence/open-basin source theorem |
| Pure continuous sections alone | Turn1's quantitative gap correctly isolated | Blocked as a standalone proof route | An unproved uniform modulus for growing backward section compositions would transfer the central difficulty |
| Linear L1 stable-manifold route | Correct stable functional and high-frequency obstruction | Blocked as a standalone nonlinear route | Strong convergence is not uniform contraction; no L1 Frechet smoothness supplied |
| Native computation | Five original replays, complete four receipt equalities, separate controls | Verified reproduction | Counts do not establish infinite-dimensional topology |
| Submitted identity/semantics |38 file bindings,123 native root captures,86 nested declarations | Verified | Historical head differs from final head by design |
| Ancillary ESI payload retrieval | Initial native DNS failures retained; later fresh curl payload and source-enabled original wrapper | Verified | Full ESI text was not independently reread as a separate mathematical dependency |

The strongest supported mathematical conclusion is a full scoped PASS for the original candidate argument, with no central algebra, parameter, inverse-distortion, cancellation or regularity gap found. Root independently reproduced the continuous and symbolic outputs byte-exactly and reviewed the draft, frozen checker and package verifier before approving final sealing. This family audit is complete: mathematical audit completion 100% and package custody completion 100%. Subjective audit completion estimate 100%; it is not a probability of correctness. There was no outside communication, Git mutation, publication, PR write or sheet write by this family.
