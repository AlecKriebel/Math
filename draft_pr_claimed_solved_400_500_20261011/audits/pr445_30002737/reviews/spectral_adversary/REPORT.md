# Independent spectral adversarial review of PR 445 / problem 30002737

**Sealed verdict: PASS for the original dimension-unrestricted claim, using absolute continuity with respect to the ambient two-dimensional Haar measure. Blocking findings: 0. Required mathematical repairs: 0. Central mathematical gaps: 0.**

Frozen eligible head: `3242c84e06db7e99012c7fe581adde5c3f89fc89`. Reviewer: `/root/pr445_spectral_adversary`. This is a review, with zero new original proof-search attempts; the author count remains 1/5. The result is an unrefereed independently reconstructed mathematical check. It establishes neither novelty nor historical priority, and does not resolve the question after adding a dimension-one restriction. The parent reviewer owns gates and later disposition. No publication, source mutation, remote mutation, branch operation, message to an outside individual, or outreach occurred in this review.

The assessed original claim is the frozen `author/attempts/turn_01.md`, together with the additive action and source clarifications actually present at this head. The package's earlier audit is an object of review, not a premise for this verdict. My initial mechanism was a deterministic occupancy-by-slot calculation retaining finite overlaps, followed by a separate suspension interval calculation. No peer findings were supplied before that mechanism was established.

## 1. Exact target and success criterion

I independently fetched the official report and visually inspected printed p.2996 (PDF page 10). Conjecture 1 reads: “If the diffraction spectrum has no absolutely continuous component, then neither has the dynamical spectrum.” It imposes no dimension-one qualification. Its preceding context concerns Dirac combs and the translation representation on an invariant-measure L² space. The subsequent dimension-specific conjectures concern Gibbs states, rather than restrictions on Conjecture 1. [Official OWR 53/2014](https://ems.press/content/serial-article-files/46543).

The precursor explicitly discusses finite-alphabet configurations on Z^d and correlation Fourier measures on R^d or d-dimensional tori immediately before the same question. This supports the higher-dimensional interpretation independently of the isolated statement. [Van Enter, arXiv:1310.0267v2, pp.2–3](https://arxiv.org/abs/1310.0267v2).

The exact success criterion is an actual positive, weight-one planar Delone comb with a canonical hull measure whose physical diffraction has zero planar Lebesgue absolutely continuous part, but whose full R² representation admits a nonzero finite spectral measure absolutely continuous with respect to planar Lebesgue measure. A spectral measure merely continuous along a line would fail this criterion. A weighted preliminary model alone would also fail the weight-one criterion. The candidate meets the stronger criterion that its exhibited dynamical spectral measure is equivalent to planar Lebesgue measure.

## 2. Credited input, without IID assumptions

Let X be the binary Rudin–Shapiro hull with shift `(Sx)_i=x_(i+1)` and invariant probability μ. The only infinite input needed is strict ergodicity, sign balance, and

\[
\int_X x_0\,d\mu=0,\qquad
\int_X x_0x_m\,d\mu=\delta_{m,0}.
\]

I freshly fetched and rendered Baake–Grimm pp.2–3. Page 2 states strict ergodicity and equal sign frequencies for its two-sided recursion, and page 3 proves the delta autocorrelation by recurrences. The paper also explicitly classifies line-concentrated diffraction in the plane as singular continuous, consistent with the ambient convention here. [Baake–Grimm, arXiv:0810.5750v2](https://arxiv.org/abs/0810.5750v2).

An independent exact bridge checks that the candidate's substitution supplies that system. For `ρ: a→ab, b→ac, c→db, d→dc`, code a,b as +1 and c,d as −1. Each substitution image places a/d at even sites and b/c at odd sites. The legal `ρ²`-fixed seed `c|a` preserves this parity assignment. The coded `ρ²` images are `+++−`, `++−+`, `−−+−`, `−−−+`. Hence, at every integer n, not just a finite sample,

\[
w(4n+r)=w(n)\quad(r=0,1),\qquad
w(4n+r)=(-1)^{n+r}w(n)\quad(r=2,3),
\]

with `w(0)=1,w(−1)=−1`, matching the primary recursion. The substitution is primitive (every third iterate contains every letter), so its standard strictly ergodic substitution hull and binary factor agree with the credited binary input.

For completeness, the primary correlation recurrences have a triangular solution: with `a_m=E[w_nw_(n+m)]`, and the parity-weighted `b_m`, the m=1 equations give `a_1=−b_1/4` and `b_1=b_1/4`, so both vanish. The m=2 and m=3 equations then vanish, and all larger positive indices depend only on smaller ones. With `a_0=1,b_0=0`, induction gives the delta correlations; reflection handles negative indices. The parity observable is available in the four-letter extension, so the auxiliary averages do not invoke a random-sign model.

Unique ergodicity makes averages of the continuous cylinder functions `x_0` and `x_0x_m` uniform in x and in interval starting position. In particular, every deterministic x in the hull obeys the required mean and correlation limits. The two coordinate sequences may even be the same fixed sequence; independent translations of the coordinates, not a random choice of sequences, are what matter below.

## 3. Preliminary positive weighted comb

Set `W(i,j)=4+x_i+2y_j`. Its values 1,3,5,7 are positive and identify the ordered pair of signs. For a rectangle, put horizontal overlap `I_m=I∩(I+m)` and vertical overlap `J_n=J∩(J+n)`, and write `x_i'=x_(i−m)`, `y_j'=y_(j−n)`. The exact finite pair sum is

\[
\begin{aligned}
\sum_{i\in I_m,j\in J_n}W(i,j)W(i-m,j-n)
={}&16|I_m||J_n|
 +4\sum_{I_m}(x_i+x_i')|J_n|
 +8\sum_{J_n}(y_j+y_j')|I_m|\\
&+\sum_{I_m}x_ix_i'|J_n|
 +4\sum_{J_n}y_jy_j'|I_m|\\
&+2\left(\sum_{I_m}x_i\sum_{J_n}y_j'
         +\sum_{I_m}x_i'\sum_{J_n}y_j\right).
\end{aligned}
\]

No finite mean or boundary term has been suppressed. Dividing by rectangle area and taking both side lengths to infinity gives uniformly

\[
\eta_W(m,n)=16+\delta_{m,0}+4\delta_{n,0}.
\]

With kernel `exp(−2πik·t)`, `δ_Z` transforms to itself and `δ_0` transforms to one-dimensional Lebesgue measure λ. Therefore

\[
\widehat\gamma_W=16\delta_{\mathbb Z^2}
 +\lambda\otimes\delta_{\mathbb Z}
 +4\delta_{\mathbb Z}\otimes\lambda.
\]

The checks `γ_W({0})=21`, mean weighted density 4, and central Bragg mass 16 agree. On the Z² system the product cylinder `x_0y_0` has correlation `δ_(m,0)δ_(n,0)` and normalized Haar spectral measure on T². This preliminary model is correct, but the verdict below is about the physical weight-one set.

## 4. Every physical pair coefficient, including collisions

Use slots `C={0,e,a,b}` with `e=(1/10,1/10)`, `a=(1/3,0)`, `b=(0,1/3)`, and occupancies

\[
p_0=p_e=1,\quad p_a(i,j)=(1+x_i)/2,\quad p_b(i,j)=(1+y_j)/2.
\]

These slots are distinct modulo Z², so their union is an actual set and has no hidden multiplicities. At displacement `z=(m,n)+c−d`, the ordered c,d contribution is the uniform limit of `p_c(i,j)p_d(i−m,j−n)`. Set `q_0=q_e=1,q_a=q_b=1/2`. Its value is precisely

\[
q_cq_d
 +\tfrac14\mathbf1_{c=d=a}\delta_{m,0}
 +\tfrac14\mathbf1_{c=d=b}\delta_{n,0}.
\tag{1}
\]

This formula covers all 16 ordered slot pairs. The 0/e pairs are constant; a with 0/e or b with 0/e uses one balanced mean; a-a and b-b use the two-point correlation; a-b and b-a factor into horizontal and vertical sign means because the two indices range independently. The last factorization is an exact finite Cartesian sum, and remains valid when x=y. It is not a statistical-independence assumption about entries within an RS sequence.

There are 13 directed residue differences modulo Z². Twelve off-diagonal residues are distinct. The zero residue has exactly four ordered self-slot contributions. Thus at a lattice displacement `(m,n)` the coefficient is

\[
2+\tfrac14+\tfrac14
 +\tfrac14\delta_{m,0}+\tfrac14\delta_{n,0}
 =\tfrac52+\tfrac14\delta_{m,0}+\tfrac14\delta_{n,0}.
\]

All nonlattice coefficients have their unique off-diagonal value from (1). Even if motif differences had collided, their contributions would have to be added; treating slot differences as distinct without checking them would be unsafe. The finite controls explicitly enumerate these collisions.

Define `D=δ_0+δ_e+(δ_a+δ_b)/2`. Equation (1) yields

\[
\gamma_\Lambda=(D*\widetilde D)*\delta_{\mathbb Z^2}
 +\tfrac14\left(\delta_0\otimes\delta_{\mathbb Z}
                 +\delta_{\mathbb Z}\otimes\delta_0\right).
\tag{2}
\]

The candidate's decomposition `δ_Λ=P+A+B` is exactly the same occupancy identity, where `P=D*δ_Z²`, `A=δ_a*(ω_x⊗δ_Z)/2`, `B=δ_b*(δ_Z⊗ω_y)/2`. Its nine correlations are: P-P gives the first term of (2); A-A and B-B give the two displayed corrections; each of P-A, A-P, P-B, B-P, A-B, B-A is zero in the limit. The motif translations cancel in the two self-fluctuation correlations. In finite physical windows the six cross terms need not be zero; the control computes and preserves them. For one test their normalized P-A maximum is 0.109375 and A-B maximum is approximately 0.0045573, so the checker is demonstrably not imposing asymptotic cancellation on finite data.

## 5. Uniform squares and all van Hove windows

For a square of side O(N), replacing physical motif restrictions by the cell rectangle changes at most O(N) points for each fixed slot and fixed displacement. Weights are uniformly bounded, and each point has finitely many possible partners at that displacement. Consequently the pair-sum error is O(N), and normalization by area O(N²) removes it. The constant is uniform in x,y and in fractional phase. Integer phases become shifts of x,y, already included in uniformity. The same proof works for rectangles with both side lengths tending to infinity.

Here is a checkable extension to any van Hove sequence `(V_r)` of bounded measurable sets with positive volumes tending to infinity. Fix the displacement z and an error ε. By the uniform square result choose a large square side L such that its normalized coefficient differs from (1), after summing coincident slot differences, by less than ε for every symbolic pair and phase. Partition the plane into L-squares. Every whole square contained in V_r has this same estimate. Every partially intersecting square lies in a boundary thickening of V_r with a radius depending only on L. The number of grid-supported points in these boundary squares is bounded by a constant times the volume of a further fixed thickening, using the common uniformly discrete grid. Its normalized contribution tends to zero by the van Hove property.

Counting pairs inside the whole squares rather than the whole union loses only partners crossing square edges. For fixed z their loss per square is O_z(L), hence O_z(1/L) after volume normalization; choose L also large enough to make this less than ε. Pairs with one endpoint in a boundary square are covered by the same boundary estimate. Thus the limiting normalized coefficient over V_r equals the square value, uniformly in x,y and translation phase. This argument applies also to each signed P/A/B cross correlation because the absolute weights remain bounded.

Finally, `(C−C)+Z²` is locally finite. A compactly supported test function encounters finitely many possible displacements. Uniform convergence of their coefficients therefore gives vague convergence of the autocorrelation measures. No unproved interchange of infinitely many displacement sums or assumed convergence on arbitrary thin non-van-Hove windows is needed.

## 6. Diffraction and ambient measure classification

Fourier transforming (2) gives

\[
\widehat\gamma_\Lambda
=\sum_{k,l\in\mathbb Z}
\left|1+e^{-2\pi i(k+l)/10}
 +\tfrac12e^{-2\pi i k/3}+\tfrac12e^{-2\pi i l/3}\right|^2\delta_{(k,l)}
 +\tfrac14\left(\lambda\otimes\delta_{\mathbb Z}
                +\delta_{\mathbb Z}\otimes\lambda\right).
\tag{3}
\]

The phase signs are consistent with `D*D̃`, since its transform is `|D̂|²`. A fixed motif shift produces no phase in an A-A or B-B intensity. Every measure in (3) is carried by `E=(R×Z)∪(Z×R)`, a planar null set. The Bragg term is atomic; the line terms are nonzero, diffuse, and singular relative to planar Lebesgue measure. Intersections of lines do not create atoms: each singleton still has zero line measure. They have zero two-dimensional absolutely continuous part, even though individual line densities are absolutely continuous with respect to length on their lines.

At zero displacement, the four periodic self-slot weights contribute `1+1+1/4+1/4=5/2`, and the two fluctuation corrections contribute 1/2. Hence `γ_Λ({0})=3`, equal to the density `2+1/2+1/2`. At zero frequency the Bragg mass is `|D̂(0)|²=9`. The line terms add no atom there. These checks falsify the plausible but wrong omission of the two self-slot corrections, which would give density 5/2.

## 7. Actual real-action conjugacy, not a lossy factor

The directed residue relation `d−c=e mod Z²` holds only for `(c,d)=(0,e)`. Therefore the set of p for which both p and p+e occur is exactly the anchor lattice, in every translated decoration. Its phase is recovered modulo Z²; the a/b occupancies then recover the complete x/y sequences. These are fixed-radius local tests. There is no extra invisible complement, swap, or rotation fiber.

Let `Σ(X)=(X×[0,1])/(x,1)~(Sx,0)`, and define

\[
\Phi([x,u],[y,v])=\Lambda_{x,y}-(u,v).
\]

Since `Λ_(S^m x,S^n y)=Λ_(x,y)−(m,n)`, this map respects both suspension seams. The product suspension flow at t=(t₁,t₂) uses integer changes `floor(u+t₁)`, `floor(v+t₂)`, so direct substitution gives `Φ(T_t ξ)=Φ(ξ)−t`. Thus the real action, including its sign, is correct. Fractional translations and independent dense symbolic orbits give surjectivity onto the physical hull. Equality of two images first gives equality of anchor phases modulo integers; using representatives in `[0,1)²` gives equal phases, and decoding gives equal symbolic sequences. Consequently Φ is injective modulo precisely the suspension identifications. It is continuous, including the seams, so compactness and the Hausdorff hull topology make it a homeomorphism.

The product Z² action has only μ⊗μ as invariant probability: invariance under each coordinate shift forces its conditional measure on that factor to μ, and then forces the other marginal. Minimality follows from the Cartesian product of independent dense shift orbits. For an invariant probability on the product suspension, the phase projection is Haar on T². Conditional symbolic laws at almost every phase are invariant under the two unit-time maps and hence equal μ⊗μ. Thus its unique invariant law is `μ⊗μ⊗du⊗dv`. This proves that the subsequent observable genuinely belongs to the physical hull's representation.

The auxiliary geometric hypotheses also hold: the set contains Z², lies in `(1/30)Z²`, and hence is Delone, FLC and Meyer. Minimality gives repetitivity. A period must preserve anchors and so be an integer pair; decoding would make one symbolic factor periodic. A periodic point in a minimal binary hull would make the whole hull finite, contradicting the delta correlations at its nonzero period. Therefore the physical set is aperiodic.

## 8. Suspension spectrum for all signs and endpoints

On Σ(X), choose the unique representative with `0≤u<1` and set `h([x,u])=x_0`. This is a bounded Borel observable. It is not required to be continuous at the section: the section has invariant measure zero, and an L² observable suffices for spectral type. For every real t and almost every u,

\[
E_\mu\left[x_0 x_{\lfloor u+t\rfloor}\right]
=\mathbf1_{\lfloor u+t\rfloor=0}.
\]

The admissible interval of u is exactly `[0,1)∩[−t,1−t)`. Its length is 1−t for `0≤t≤1`, 1+t for `−1≤t≤0`, and zero outside. At t=0 the length is 1; at t=±1 and all other nonzero integer times it is zero. Endpoint representatives do not change the integral. Hence

\[
C_h(t)=(1-|t|)_+.
\]

Let `b=1_[0,1]`. Then `C_h=b*b̃`, and

\[
\widehat b(k)=e^{-\pi ik}\frac{\sin(\pi k)}{\pi k},\qquad
\widehat C_h(k)=|\widehat b(k)|^2=\operatorname{sinc}^2(k).
\]

The removable value at k=0 is 1. Plancherel gives `∫sinc²(k)dk=||b||²_2=1`, which also equals `||h||²_2=C_h(0)`. This independently fixes all Fourier constants. With either common sign convention for the Koopman action the spectral measure is the same, because the correlation and density are even.

For `H([x,u],[y,v])=x_0y_0`, the invariant product law gives, for the full R² action,

\[
C_H(t_1,t_2)=(1-|t_1|)_+(1-|t_2|)_+,\qquad
 d\sigma_H(k_1,k_2)=\operatorname{sinc}^2(k_1)\operatorname{sinc}^2(k_2)\,dk_1dk_2.
\]

Its total mass is 1. The density is strictly positive except on the countable union of lines where one coordinate is a nonzero integer. That zero set has planar Lebesgue measure zero. Therefore the finite σ_H and planar Lebesgue measure have exactly the same null sets. Transferring H through the proven conjugacy exhibits the required nonzero absolutely continuous component of the actual unweighted point-set dynamics.

This conclusion is about the full R² representation, not a restriction to a single flow direction. It asserts neither pure absolute continuity of the whole representation nor any spectral multiplicity. Constants and phase eigenfunctions coexist harmlessly with this component.

## 9. Product factor and comparison with positive theorems

At every recovered anchor `(i,j)−(u,v)`, assign the local weight `x_i y_j`, determined by the two a/b occupancies. This gives a continuous equivariant map into translation-bounded signed combs

\[
\Omega_{x,y,u,v}=\sum_{i,j}x_i y_j\,\delta_{(i-u,j-v)}.
\]

Its autocorrelation coefficient at `(m,n)` is the product of the two deterministic RS two-point averages, hence `δ_(m,0)δ_(n,0)`. Fractional phase cancels from pair differences. Its diffraction is planar Lebesgue measure. The map is a legitimate local weighted factor; no recovery of the original hull from this factor is asserted or required. Finite source data needs only its two occupancies, and the marker establishes their location.

This explicit factor confirms that the richer dynamical spectrum can be visible in additional factor diffraction even when the original physical diffraction is singular. The reconstruction theorem of Baake–Lenz–van Enter concerns a total family of factor diffractions, not a claim that the original single diffraction carries every spectral measure; this was independently checked in Definition 3 and Theorem 13 (p.21), and Theorem 15/Corollary 16 (p.22). [Primary factor paper, arXiv:1307.7518v2](https://arxiv.org/abs/1307.7518v2).

The pure-point equivalence also does not contradict (3), which has a nonzero singular continuous line part. In the product suspension, the separate observables h in the first and second coordinates have spectral measures `sinc²(k₁)dk₁⊗δ_0` and `δ_0⊗sinc²(k₂)dk₂`, each singular in the plane, while their product H has the full planar density. This is a directly computed failure of closure under multiplication of the ambient-singular spectral subspace; assuming such closure would be the false step behind the proposed implication here.

## 10. Reproduction, limits, and original versus repair verdict

Run `python3 -O controls.py` from this review directory. Essential guards are explicit exceptions, so optimization cannot remove them. The script reads the frozen source receipt and checks all 12 source byte counts and hashes before and after. It imports neither frozen checker, writes only `CONTROL_RESULTS.json`, and uses deterministic primary recursion/substitution data.

The sealed run returned PASS:

- 32,768 bilateral substitution/recursion sites and 16,384 positive bit-formula sites agree.
- All 13 difference-residue classes are enumerated, including the fourfold zero-residue collision and unique directed marker.
- 1,300 physical weight-one pair counts agree exactly with independently factored finite counts across phase-shifted squares/rectangles, negative symbolic offsets, and cases with x=y. The largest sample has 49,408 points, density 3.015625, and maximum finite deviation about 0.06213. The limiting density is not forced onto these samples.
- 1,053 signed P/A/B cross counts and 243 positive-weighted counts agree exactly with finite expressions retaining all boundaries and imbalance terms.
- 301 rational suspension times and 432 rational time pairs agree by exact interval partition, including negative times and integer endpoints.
- Independent cosine quadrature verifies nine triangle Fourier values with largest error below 8×10⁻¹⁵; truncated sinc masses obey the analytic tail bound `2/(π²R)`. These numerical diagnostics supplement, rather than replace, the convolution/Plancherel proof.
- Negative controls reject both the missing self-correlation correction and the naive observable rule that ignores a suspension seam.

**Original verdict:** supported as stated in the frozen package, for the unrestricted ambient-Haar claim. No original central gap remains. **Proposed repair verdict:** no repair is necessary; this report has not substituted a new construction or assumption for the original. The detailed van Hove and endpoint calculations above are independent verification and exposition, rather than a prerequisite amendment. The dimensional and ambient-measure scope must remain explicit in any promoted description. A one-dimensional result, exhaustive current priority search, novelty certificate, and human peer review are outside this conclusion.

All foreign primary PDFs, their extracted text, and rendered pages are under `private/` and excluded from the public manifest. `PUBLIC_FILES.json` lists only positively selected authored report, typed verdict, log, independent control code, control results, and source-receipt metadata. Nothing in this review changes the queue or source package.
