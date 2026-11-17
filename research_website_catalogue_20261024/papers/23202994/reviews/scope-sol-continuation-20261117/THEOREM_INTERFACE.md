# Independent finite/periodic/surface interface

This records deductions checked by hand, with dependencies separated. The original five-page note and333-line TeX were read before support or primary material in the sealed INITIAL. These calculations were then compared with the actual support and fetched primary sources after RESUME. No repair of the source manuscript is made.

## 1. Periodic disk functional, fixed configuration first

Fix s>2, a finite distinct motif F={f_1,…,f_q} in [0,L)², and C=F+LZ². For each motif label, the translated square cells centered at its coset points enclose B_(R−d) and lie within B_(R+d), d=L√2/2. Hence n_i(R)=πR²/L²+O(R) and n_i(R)/N_R→1/q. Density is q/L². Every representation is unique; positive minimum separation follows for this fixed finite motif modulo a fixed period, without any uniform-in-N premise.

Define the full outgoing row h_i=Σ_{j,k:(j,k)≠(i,0)}|f_i−f_j−Lk|^(-s). For ||k||∞=m≥2, the distance is≥L(m−1)≥Lm/2; the tail is bounded by q(2/L)^sΣ_{m≥2}8m^(1−s). Thus h_i is finite. Completing each disk row gives S_R≤Σ_i n_i(R)h_i. For a fixed interaction cutoff T, every outgoing displacement≤T from B_(R−T) stays in B_R, so S_R≥Σ_i n_i(R−T)h_i^T. First R→∞, then T→∞, gives the **ordinary** disk limit H_s(C)=q^(-1)Σ_i h_i. This proves the exact centered-disk/ordered-pair interface rather than substituting a torus or area functional.

Dilation by λ sends density to λ^(-2)q/L² and per-point energy to λ^(-s)H_s(C). The latter has no further density multiplier. Both facts also follow directly from the disk definition by replacing R with R/λ.

## 2. Lower bridge and its order of limits

For any distinct N-point X⊂[0,1]², set y_i=√N x_i and L=(1+ε)√N with ε>0. The motif fits strictly in [0,L)² even when X contains closed-square endpoints. The within-cell energy per point is N^(-1-s/2)E_s(X). For every nonzero k with ||k||∞=m, |y_i−y_j−Lk|≥√N[(1+ε)m−1]≥ε√N m. This includes i=j interactions with nonzero copies. Summing all N² ordered motif pairs and8m cells gives

I_(N,ε)≤8ε^(-s)ζ_R(s−1)N^(1−s/2).

The periodic density is(1+ε)^(-2). Compress by λ=(1+ε)^(-1), obtaining density1 and energy(1+ε)^s[N^(-1-s/2)E_s(X)+I_(N,ε)]. Applying the now proof-checked periodic specialization of the OpenAI bound yields

a_N≥(1+ε)^(-s)Z_s−8ε^(-s)ζ_R(s−1)N^(1−s/2).

The disk radius limit is taken for each fixed N,ε. Next N→∞ at fixed ε, and only then ε↓0. No joint family of radii, unknown minimizer separation, or uniform local occupancy is used. At ε=0 boundary-copy collisions would invalidate the argument; that case is never used. At s=2 the shell majorant ceases to converge; this method gives no critical-s conclusion.

## 3. Exact-N upper construction and centrality check

Choose a bounded fundamental parallelogram P⊂[−D,D]² for the covolume-one triangular lattice. Cells covering [D,t−D]² have their lattice vertices in[0,t]², so the crop contains at least(t−2D)² points. Put t=√N+2D, choose any exact-N subset, and scale by1/t. Positive full lattice row sums give a_N≤Z_s(1+2D/√N)^s. No crop with exactlyN lattice points is assumed. Combined with the lower bridge this yields the actual unit-square limit Z_s.

For comparison, let P_s be the infimum of row energies over density-one square-periodic motifs. Repeating the gap argument with P_s and cropping each fixed motif shows unconditionally lim a_N=P_s≤Z_s. The reverse crop uses n_i^square(t)=t²/L²+O(t), then full rows to bound the chosen exact-N subset. Thus merely renaming the central task P_s=Z_s is not an independent solution. The INITIAL primary-free route remains blocked there. The present closure comes from the actual Fourier construction, not from this equivalent formulation.

The INITIAL rough conditional-rate algebra remains valid: ε_N=N^(-α), α=(s−2)/(2(s+1)), balances the two explicit error powers, and (1+ε)^(-s)≥1−sε gives its stated bound. It is not used to assert a sharp rate, a second term, a uniform estimate as s↓2, or novelty for an optional follow-up.

## 4. Squared-radius singular kernel and mixture limits

Direct application is permitted by the primary theorem's actual unbounded/singular class. As an independent check avoiding any issue at t=0, write p=s/2 and use bounded positive Gaussian mixtures

g_[a,b](t)=Γ(p)^(-1)∫_a^b u^(p−1)e^(-ut)du, 0<a<b<∞.

They are nonnegative completely monotone in the squared distance t and bounded at0. Termwise H_s(C)≥H_g[a,b](C), then the corresponding primary comparison gives the lattice truncated-mixture sum. Increasing intervals[a,b] to(0,∞) and applying monotone convergence only to the nonnegative lattice series yields H_s(C)≥Z_s. This is an additional interface check; it uses the Gaussian theorem already established and does not exchange a configuration liminf and the mixture integral in an invalid direction. For the full class the primary shifted/Fatou proofs are checked separately in PRIMARY_PROOF_CHECKS.md.

## 5. Corrected classical theorem and actual chart class

Fresh Hardin–Saff arXiv math-ph/0311024v3 is exactly the native recorded325401-byte PDF, with the four-page addendum before the paper. In the paper, equation2 counts ordered pairs and uses the ambient Euclidean norm; the measure normalization before Theorem2.1 makes a unit d-cube have measure1. Equation10 defines C_(s,d) by that cube limit. Definition19 requires A=∪_(k=1)^n φ_k(K_k), each K_k compact in R^d and φ_k bi-Lipschitz on an **open neighborhood** G_k⊃K_k. Theorem2.4 transfers equation9 for s>d. The extra containment in a C¹ manifold is stated for s=d and is not imported here. I read the actual definitions, theorem and Section8 proof, the relevant hypersingular unit-cube/compact-set arguments, and all four addendum pages; six fresh pixels (physical1–4,10–11) were individually viewed to check notational/boundary issues. This is not a claim to have visually read every page of the 33-page PDF.

For a compact smooth embedded surface with smooth boundary, choose local parameterizations including half-plane boundary charts. A smooth embedding with boundary has a smooth local extension across that boundary with rank2 derivative T. On a sufficiently small convex full parameter ball, arrange ||Dφ−T||<σ_min(T)/2. Integrating Dφ along a segment gives |φ(x)−φ(y)|≥σ_min(T)|x−y|/2 and an upper Lipschitz bound. This proves an extension bi-Lipschitz on the full open ball. Finitely many compact chart pieces cover the compact surface. Their preimages are compact in those balls and their images cover exactly the surface. The extension outside the selected compact preimage need not lie in the surface. Thus definition19 is satisfied, including smooth boundary. Finite unions/disconnected compact surfaces are covered. Positive area is necessary for the displayed finite coefficient.

## 6. Addendum: compact application versus unrestricted wording

The addendum repairs equation83 in Proposition8.3. Its auxiliary Lemma1 is printed for any relatively open neighborhood G of a compact K in a closed d-regular set, without explicitly requiring compact closure. Step1 claims dist(cl G, Atilde\V)>0, and Step2 takes energy minimizers on cl G. Those assertions require the compact application. The unrestricted statement is false: in Atilde=R^d take K=[0,1]^d, a small bounded collar of K, and disjoint tiny balls with centers tending to infinity and total outside volume<δ. G is open, containsK, and its closure has outside volume<δ, but it is unbounded. For anyN chooseN arbitrarily far separated centers, so E_s(G,N)=0 and its normalized lower constant is0, contradicting the lemma's positive bound forK. This is a concrete wording limitation, not evidence that the surface theorem fails.

To ensure the needed hypothesis, for each chart compact K_k choose finitely many closed parameter cubes whose interiors coverK_k and whose closures lie inG_k. Their images have compact union Atilde containing A. A cube has uniform two-sided local d-volume estimates, preserved by a bi-Lipschitz map. For finite unions a component containing the center supplies a uniform lower bound and summing component upper bounds supplies a uniform upper bound; components not containing a center can be bounded by doubling radius from an intersecting point. Hence Atilde is a compact d-regular thickening. In that compact metric measure space use Radon outer regularity to choose small relative neighborhoods of each compact ψ_i(K_i) with closure outside measure<δ; e.g. shrinking distance neighborhoods have intersection exactlyK, so continuity from above supplies the measure limit. All closures and minimizers are compact, and a larger relative openV has positive buffer distance.

The actual deletion argument starts with k greater than the **upper** normalized energy ofK (confirmed in fresh page3 pixels), giving an eventual upper bound forG by monotonicity. Deleting close neighbors loses≤kρ^sN points; regular disjoint balls away fromK lose≤2δN/[c0(νρ)^d]. Moving survivors toK by at mostνρN^(-1/d) preserves distinctness and changes pair distances by at most factor1−2ν. Thus

lower_g(G)≥(1−2ν)^s(1−kρ^s−2δ/[c0(νρ)^d])_+^(1+s/d)lower_g(K).

With ρ=ν=δ^(1/(4d)), this factor tends1. This proves the compact version needed for equation83, and removes the apparent gap without using an unbounded neighborhood or a liminf-to-eventual-upper conversion. The rest of Section8 uses finite almost-isometric compact pieces, positive-distance upper estimates, nonnegative union lower estimates, and the small-measure energy bound from finite bi-Lipschitz charts. Those conventions match the present hypersingular branch. Standard rectifiability/measure theorems in that classical proof are retained classical inputs, not a newly reproduced proof of Federer's theorem.

## 7. Surface/sphere coefficient and scaling falsifiers

Using the now identified cube constant, equation9 gives Z_s[H²(M)]^(-s/2)N^(1+s/2). With the planar-normalized H² this is ordinary surface area. Ambient dilation M↦rM multiplies the coefficient by r^(-s), exactly as the actual energy does; substituting area r²A gives the same factor. The unit sphere has area4π, hence coefficient Z_s/(4π)^(s/2). Ordered pairs occur on both sides throughout, so no extra one-half factor appears. A future unordered convention would divide all finite and infinite per-point constants by2. No geodesic-distance theorem has been silently substituted.

Strongest checked result: the precise consequence is mathematically supported within the reviewed primary chain; the former central external premise is supported by actual proof and the atomic finite pass. No material unresolved gap was identified for that scope. Limits remain the absence of a formal kernel proof, a fresh MAIN finite run in this family, a complete current priority survey, or validation of excluded jellium/critical/uniqueness statements. These are not repaired or promoted by this packet.
