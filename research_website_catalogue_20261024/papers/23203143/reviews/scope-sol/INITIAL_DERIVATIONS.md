# Independent source-first derivations — record 23203143

These calculations were made after the whole 212-line manuscript and eight native PDF pages were read, before current review findings, archived opinions/results/programs or new foreign mathematical bodies. They establish deductions conditional on precisely stated imported interfaces. They do not certify those imported inputs.

## 1. The restricted regular wreath construction

Assume a finitely generated group G and a,b in F₂[G] with ab=1 but ba≠1. Also assume an embedding G→H into a finitely generated Hopfian group. The map on group algebras is injective because distinct source group elements remain distinct target basis elements. Thus ab=1 and ba≠1 remain true in R=F₂[H].

Identify the ENTIRE finite-support base C₂^(H), rather than the single lamp C₂, with the additive group of R. The regular left action is h·r=[h]r and multiplication in the wreath product is (r,h)(s,k)=(r+[h]s,hk).

For every fixed t∈R, right multiplication r↦rt commutes with the left H action by associativity. Hence T_t(r,h)=(rt,h) is a group endomorphism. Finite supports are preserved because supp(rt)⊆supp(r)supp(t). This is precisely where using right, rather than left, multiplication is important.

Take Φ=T_b and Σ=T_a. Composition on a base element is ΦΣ(r)=r(ab)=r, so ΦΣ=id. Thus Φ is split surjective. The reverse composition is ΣΦ(r)=r(ba), which need not be r; a right inverse of Φ does not make Φ injective.

Set e=1−ba. Then e≠0, eb=b−b(ab)=0, and (ba)²=b(ab)a=ba. Consequently e²=e, in characteristic two as well as in any unital ring. The element (e,1_H) is a nonidentity kernel element. Moreover rb=0 implies re=r−(rb)a=r, while (se)b=s(eb)=0 for every s. Therefore ker(r↦rb)=Re, a principal LEFT ideal, and ker Φ=(Re)×{1_H}. No commutativity or centrality of e was used. H stabilizes Re by left multiplication, as kernel normality requires.

Lift a finite generating set of H and add the identity-coordinate lamp. Conjugating that lamp by h produces the basis lamp [h]; finite products give every finite-support configuration. Thus the wreath is finitely generated. C₂ is finite and hence Hopfian; H is Hopfian by the imported embedding theorem. Neither finite presentability of H/the wreath nor torsion-freeness of H is deduced.

The manuscript's stronger group-algebra input has ab=1, ac=0 and c≠0. If ba=1, then c=(ba)c=b(ac)=0, contradiction. It therefore supplies the needed one-sided inverse defect IF the actual external input theorem has those identities over F₂ in a finitely generated group. A different coefficient field, torsion example, permutational action, unrestricted base or nonabelian lamp is not a substitute.

### Hand-checkable side/order control

On V=⊕_{j≥0}F₂v_j, let S(v_j)=v_{j+1}, T(v_0)=0 and T(v_{j+1})=v_j. Then TS=I and ST=I−P₀. In End(V), set a=T,b=S,e=P₀. This concretely checks the same multiplication order, nonzero idempotent and split projection: r↦rS has right inverse r↦rT and kernel End(V)P₀. This is an algebraic calibration, NOT a group-algebra witness or a construction of the claimed H.

A finite H cannot supply the defect: its finite-dimensional F₂-algebra has ab=1 only if multiplication by a is invertible, forcing ba=1. Thus trying finite-group enumeration cannot certify the actual infinite-group claim. No enumeration is needed or performed.

## 2. Exact Fourier models and lattice lower bounds

Use ĝ(ξ)=∫g(x)exp(−2πi⟨x,ξ⟩)dx. L_n is the infimum of g(0) over real Schwartz g with ĝ(0)=1, ĝ≥0 everywhere and g≤0 for |x|≥1. Let D={0}∪[1,∞). P_n is the infimum of F(0,0) over real Schwartz F on R^n×R^n with F̂(0,0)=1, F̂≥0 and F≤0 whenever |x|,|y|,|x−y|∈D except (x,y)=(0,0). There is no |x+y| condition. No symmetry or optimizer attainment is built into these definitions. Real nonnegative Fourier transforms themselves give central evenness, but this is weaker than imposing radiality or arbitrary triangle symmetries.

For Λ=Z(1,0)+Z(1/2,√3/2), detΛ=d=√3/2. Squared lengths are m²+mn+n²=(m+n/2)²+3n²/4. For integer m,n not both zero this is a positive integer, hence at least one. So every nonzero lattice vector is in the two-point negative-sign region, including shortest vectors at equality. Schwartz Poisson sums converge absolutely and give g(0)≥Σ_Λg=d^(-1)Σ_{Λ*}ĝ≥d^(-1)=2/√3.

For any nonzero pair (u,v)∈Λ², u,v,u−v are lattice vectors. Their norms are either zero or at least one. This includes (0,v), (u,0), u=v, collinear pairs and length-one boundary pairs. Therefore F(0,0)≥Σ_{Λ²}F=d^(-2)Σ_{(Λ*)²}F̂≥d^(-2)=4/3. Removing the zero-coordinate or coincident configurations would break this argument; the manuscript actually retains them.

These objectives are raw number densities. Multiplying 2/√3 by the disk area π/4 yields the covered-area density π/(2√3). Substituting that packing fraction into L₂ would change normalization. The AIM displayed square-root convention means √P₂=L₂, while the present unrooted objective is P₂=4/3.

### Explicit control against the naive tensor-product shortcut

In dimension two, set c=1−1/π>0 and g(x)=(1−|x|²)e^(−π|x|²)/c. Fourier differentiation of the Gaussian gives ĝ(ξ)=(c+|ξ|²)e^(−π|ξ|²)/c. Hence this is a concrete feasible two-point Schwartz function, with ĝ(0)=1 and g≤0 on |x|≥1. For u=(2,0), the pair (u,−u) belongs to the triangle sign set but g(u)g(−u)=9e^(−8π)/c²>0. Thus F(x,y)=g(x)g(y) is not an admissible conversion. This analytic control also shows L₂≤π/(π−1), without supplying the sharp external certificate.

## 3. Product-program comparison reconstructed conditionally

Let C_square={|x|,|y|∈D} minus the origin. Then C_triangle⊆C_square: square feasibility is stronger, so its infimum bounds the triangle infimum ABOVE. The needed comparison is P_n≤P(C_square)≤L_n², not the reversed inequality.

Take compact cubes Q_r=[0,r]^n with edges between distinct points at distance <1. Assume the stated theta-prime finite-measure primal/continuous-kernel dual equality. A feasible product measure μ is symmetric, nonnegative and positive definite, supported on the full diagonal/nonedges, with full diagonal mass one. Put D_i={x_i=y_i}, A=μ(D_1)≥1, B=μ(total). The first marginal divided by A has diagonal mass one, total mass B/A and is feasible on the first factor. The second marginal of μ restricted to D_1 has diagonal mass one and total mass A, feasible on the second factor. Support follows directly from the disjunctive-product edge rule.

Restriction positivity cannot be justified by declaring the discontinuous diagonal indicator an admissible test kernel. Instead, for each continuous positive definite K₂, test exp(−t|x₁−y₁|²)K₂(x₂,y₂). This product is continuous positive definite and uniformly bounded on the compact domain. Dominated convergence against the finite measure gives a nonnegative integral for the restriction as t→∞. Thus both marginal bounds apply and B=(B/A)A≤theta'(Q_r)². Supremizing gives product submultiplicativity.

For feasible g, periodize with T=r+1: K_T(x,y)=T^n Σ_{k∈Z^n}g(x−y+Tk). Its Fourier coefficients are ĝ(k/T), with the constant coefficient one. Hence K_T−1 is positive definite. At a distinct nonedge, the unshifted distance is ≥1. Every nonzero lattice translate has some coordinate with absolute value ≥T−r=1. Thus all summands are nonpositive, including the boundary. Its diagonal is T^nΣg(Tk); Schwartz tails tend to zero. Dividing by r^n and taking r→∞ yields limsup theta'(Q_r)/r^n≤g(0), then ≤L_n after taking the infimum over g. The order of limits does not require an optimizing g.

For V=Q_r×Q_r of volume W=r^(2n), let K be a product dual kernel with diagonal maximum M arbitrarily near the compact optimum. K−1 positive definite implies K itself positive definite. Zero extension of K preserves finite-matrix positive semidefiniteness; the extension need not be pointwise continuous at the boundary. Define h(z)=∫K(t+z,t)dt. Changing variables in each quadratic-form summand gives Σc_i c_j h(z_i−z_j)=∫Σc_i c_j K(s+z_i,s+z_j)ds≥0.

A continuous Hilbert feature map φ for K on compact V is bounded. Extend φ by zero. It belongs to L², and h is its autocorrelation, so translation continuity gives continuity of h; compact support gives h∈L¹. Plancherel identifies ĥ with the nonnegative integrable scalar function ||φ̂||² (interpreted in the Hilbert-valued sense), giving both Fourier nonnegativity and integrability, not merely a formal Fourier sign. The real symmetric setting gives real h.

For displacement z∈C_square, every pair (t+z,t) in V² is a distinct product nonedge, so h(z)≤0. The exact normalizations are h(0)≤MW and ĥ(0)=∫_{V²}K≥W², since K−1 paired with constant functions has nonnegative quadratic integral. Thus h/ĥ(0) has objective at most M/W. A denominator W rather than W² would lose a power of volume. Together with product submultiplicativity, this yields a continuous square-program upper value ≤L_n².

The continuous-to-Schwartz value comparison is still a precise imported interface to inspect: its admissible class and closed sign-set hypotheses must cover this h and C_square. The compact strong-duality theorem's measure model and graph topological hypotheses also remain to inspect. No attainment or triangle optimizer is needed.

## 4. Exact remaining input obligations and falsifiers

If an actual admissible planar Schwartz g has g(0)=2/√3, the lower bound forces L₂=2/√3; the comparison plus lower bound gives 4/3≤P₂≤L₂²=4/3. This does NOT produce a triangle optimizer or solve arbitrary dimensions/conversion/symmetry questions.

Before a full-original conclusion, inspect: (i) the embedding theorem for arbitrary finitely generated G, without assuming G already Hopfian; (ii) the actual pinned OpenAI torsion-free F₂ group-algebra theorem and its substantive existence/nonzero-c proof; (iii) the actual pinned sharp planar certificate, its Schwartz/Fourier/sign/normalization claims and the infinite-system/continuum estimates behind finite gates; (iv) the exact compact duality and continuous-to-Schwartz interfaces. The manuscript's own archived PASS or claim that an audit checked these is not a proof substitute. Related Lean files with another field/torsion construction cannot certify this input.

Falsifiers include wrong multiplication side or lost finite support; a coefficient-field mismatch; an embedding that loses finite generation/Hopfianity; a hidden permutational action; a weaker-than-Schwartz sharp planar function or wrong Fourier scale; missing boundary/zero/coincident triangle signs; reversing sign-set inclusion; a diagonal restriction without valid positive definiteness; missing W² normalization; or finite computations replacing infinite inverse/tail/global-sign arguments. Any central unsupported obligation precludes a full-original PASS; no narrowed replacement or repair is authorized.

At this source-first boundary, the displayed conditional algebraic and analytic deductions have been reconstructed, with the two explicit hand-checkable controls above. Foreign inputs are uninspected, so an unconditional scientific verdict remains OPEN. Follow-up defaults none.
