# Mathematical verdict seal: local and rank-one families

Seal time: 2026-10-03 07:52:53 UTC. Frozen head: `c683fc4b84266a6a153c087e182cf427ed502d6c`. **PASS for the examined restricted claims; no mathematical defect found.** This seal was written before reading or executing any author verifier or any old review. The independent deductions and code had already been sealed before candidate proof access.

Candidate path clarification: parent supplied `.../audits/pr374_30005116/snapshot/problems/30005116_induced_four_cycle_profile`; the letter A in the task was a placeholder. Two failed guessed-path searches read no candidate content. Candidate proof reading began after the exact 2026-10-03 07:48:41 UTC listing; read Turns 2,3,5, final summary, plus Turn 4's profile inequalities needed by Turn 5 and source-gate scope. No author code/check receipt or earlier independent review read yet.

## Exact target and normalization

Fresh OWR pp.1227-1228 binds the source claim; LMR Section 1.6 identifies the known low-density result and isolated knots. The target asks for the unrestricted induced-C4 maximum at fixed edge density, conjecturing the triangle-density multipartite construction above 1/2. For a graphon W the source quantity is the probability of the unlabeled four-vertex event:

`c(W)=3 int W12 W23 W34 W41 (1-W13)(1-W24)`.

The fixed labeled C4 integral is one third of c. Complementation changes C4 into 2K2. Neither ordinary C4 homomorphism density nor the semi-induced alternating-cycle quantity is interchangeable with c.

The exact January 8, 2026 Semi-Inducibility PDF was freshly fetched, read at definitions/Theorem 1.3/Question 1 and visually checked at pp.2,4. Its SHA256 is `e178ea4009a84fbe6a3da2959ee1ccead2fe598f19b490f4755c0b7140bc60f7`. AC4 specifies two edges and two nonedges and leaves two pairs unspecified, with labeled-embedding normalization. It does not resolve this induced six-pair target. This is a bounded literature/scope check, not novelty certification or proof that no other result exists.

## Turn 3: arbitrary measurable perturbations

The universal first-variation proof is valid. On fixed positive multipartite parts of masses ai, let q=sum ai^2 and h=W-W0. Feasibility forces h>=0 within parts, h<=0 across parts; density preservation forces addition and deletion masses both ||h||1/2. The six-edge conditional kernel is

`Kii=-(q-ai^2), Kij=(ai+aj)^2-q`.

Thus `D(h)=6 int hK`. For r equal large masses a and one smaller b, the relevant within/outside gap is exactly b(2a+b)>0, giving

`D(h)<=-3b(2a+b)||h||1`.

The polynomial remainder estimate is valid for arbitrary measurable h, including dependencies from shared endpoints: select one h factor and integrate its absolute value to ||h||1; bound every other h by its essential supremum. All higher-degree subsets of three six-factor products give the universal coefficient 171. With eta<=b(2a+b)/114, the resulting loss is at least (3/2)b(2a+b)||h||1. No block-constant restriction or finite-grid extrapolation occurs.

Boundary qualifications are correct: the theorem excludes knots and uses a fixed-density radius, which can vanish in limiting regimes. It does not use zero-mass parts as though they constrained h. At p=0 or1 fixed density forces the empty or full graphon a.e., so no nontrivial feasible h exists. At balanced knots a separate positive-part argument is possible but is not needed for, or claimed by, this theorem. No uniform all-density neighborhood is asserted.

## Turn 3 paths and Turn 2 tie/separation interplay

For 0<s<a-b set u=a-s, e=bs/(a-s), z=s-e and v=b+e. Algebra gives uv=ab, u+v+z=a+b and z>0. On the fixed probability space the added ordered-pair mass is 2ue=2bs and deleted mass is 2b(e+z)=2bs. Consequently ||Ws-W0||1=4bs and ||Ws-W0||infty=1. Direct join counting proves both p and c exactly unchanged for every parameter, rather than approximately preserved.

The stated linear term is `-12b^2 s(2a+b)`; since the actual change is zero, the remainder is the positive opposite, exactly order ||h||1. The example therefore falsifies an L1-uniform o(||h||1) remainder shortcut. It leaves the L-infinity theorem intact. Also cut distance <=L1, so these are cut-close ties too; no cut or L1 isolated uniqueness follows from the amplitude theorem.

For each z>0 the one-edge triple density is 6abz. Every complete multipartite graphon has zero such triple density. Coupling the three sampled pair states gives the universal difference bound 3||W-V||1; hence the L1 distance to the entire multipartite set, including every relabeling, is at least 2abz. This is positive at every nonzero path parameter and tends to zero near s=0, as it should. The paw density is 24(r-1)a ab z, also positive. The claimed rational paw example (4,2,2,1)/9 has p=16/27, c=64/243, triangle=32/243, one-edge triple=8/243 and separation>=8/729; the normalization and constants check exactly. These ties attain the conjectured construction value, not a verified unrestricted maximum.

## Turn 5: full universal rank-one profile

For arbitrary measurable f in [0,1], let m=E f=sqrt(p), A=E f^2, B=E f^3. Expansion gives c=3(A^2-B^2)^2. For p>0, m^2<=A<=m, B<=A, and Cauchy-Schwarz gives Bm>=A^2. With t=A^2/p in [p,1],

`0<=A^2-B^2<=p t(1-t)`.

Maximizing this elementary quadratic gives the exact profile

`R(p)=3p^2/16 (0<=p<=1/2), R(p)=3p^4(1-p)^2 (1/2<=p<=1)`.

No unproved moment-region description is needed: the one-sided moment bound is sufficient and its extremizers are explicitly feasible. Equality in Cauchy-Schwarz forces f constant on positive support. Below 1/2 the positive value is 1/sqrt(2), support mass sqrt(2p). At and above 1/2 equality forces A=m^2 and therefore f=sqrt(p) a.e. Mean constraints settle both zero/full endpoints. Both branches give 3/64 at the junction and the equality descriptions coincide.

The feasible vertical interval is exactly [0,R(p)]: the two-valued family f=d on mass sqrt(p)/d gives c=3p^2d^4(1-d^2)^2, ranging continuously from R(p) to0 on the stated parameter intervals. Independent symbolic derivative check confirms the restricted peak 16/243 at p=2/3. Ordinary-graph realization via independent edge sampling and motif variance O(1/n) is sufficient for deterministic approximating sequences.

## Strict comparison on every interior density

The low branch gap (21/16)p^2 is exact. The dense comparison is independently valid without assuming unrestricted optimality. For k=r+1 parts, r>=2 equal largest masses a, and s=1-p, every ai^2/s<=1/r, so

`F(p)/(3s^2)=1-sum_i(ai^2/s)^2>=1-1/r>p^4`

because p<=r/(r+1) and r^2/(r+1)^2<1-1/r for r>=2. This independently proves R(p)<F(p) for every 1/2<p<1.

The author's alternate explicit constants also check: F>=3(1-p)^2/2; on [1/2,3/4], 3(1/2-(3/4)^4)=141/256. Above3/4, the algebraic bracket p^2(1+p+p^2+p^3)-1 is increasing and equals551/1024 at3/4, yielding1653/1024 as claimed. Both intervals cover their junction. Strictness is intentionally absent at p=0,1 where F=R=0.

## Evidence and limitations

The pre-candidate code checked all64 four-vertex masks,70 finite latent laws, literal first-variation enumeration for2/3/4 positive parts, and an exact rational tie. Post-candidate independent code checked all-parameter path/junction/gap identities symbolically and36 literal fixed-space paths with direct four-vertex integration. These are reproducibility controls; the infinite-family claims rest on the universal arguments above.

One control attempt failed because a SymPy expression was compared structurally rather than by simplifying its difference to zero. The complete failed script and stream are preserved; corrected algebraic comparison passes. A transient own __pycache__ was moved into ignored tmp and future executions use -B. Two estimated clock labels in sealed notes were future relative to exact tool clocks; exact timestamps and corrections are preserved, not silently overwritten.

Strongest checked result: the full rank-one fixed-density feasible profile/equality classification, together with a valid universal amplitude-local theorem and exact close equality deformations with quantitative edit separation. Exact gap: no inequality covers every arbitrary graphon with prescribed p>1/2. Promoting any restricted family/local argument to a global reduction transfers the central difficulty to an unsupported structural theorem and remains blocked until a materially new mechanism is supplied. The source conjecture is neither proved nor refuted.

Audit completion before replay: 85%. Restricted claim checking: 100%. Unrestricted discovery completion: 0% for this audit, with no new global-discovery claim.

