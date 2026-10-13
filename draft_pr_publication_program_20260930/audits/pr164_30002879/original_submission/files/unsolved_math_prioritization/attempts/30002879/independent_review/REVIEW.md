# Independent adversarial review: the seven-dimensional Hochschild Lie algebra

**Problem:** 30002879 / OWR-13681-013.  
**Verdict:** **PASS_COMPLETE_ALL_DEGREE_LIE_ALGEBRA_AND_GAMMA_MAP**.  
**Mandatory mathematical corrections:** none.  
**Reviewed mathematical snapshot:** `PROOF.md`, SHA-256 `439bb5ac541dcc7cb0e6fbf5b30a22501f23f330b4f970fe641fb54234bd46be`.

This is an independent AI audit of the stated algebra and map, not human peer review or a certification of historical priority. The proof answers the original intended seven-dimensional example in all cohomological degrees over any field of characteristic two. The credited earlier ring computation and structural theorems are essential background.

## 1. Source, algebra, and module conventions

I inspected the rendered original Question 5 and the surrounding coefficient sequence on printed p. 1363 of [OWR 24/2015](https://ems.press/content/serial-article-files/46571?nt=1). The question asks for the precise Lie structure of the Hochschild cohomology of the upper triangular algebra with diagonal entries `K(Z₂×Z₂)` and `K`, off-diagonal module `KZ₂`, and lower-right stratifying idempotent. It also asks whether the displayed coefficient sequence can determine that structure. The complete Lie algebra and identification of its map are therefore the right targets; a positive-degree dimension formula alone would not suffice.

The original matrix display does not by itself specify the action on its two-dimensional off-diagonal module. The candidate correctly resolves that convention using the same example in [Hermann, arXiv:1411.0836v2](https://arxiv.org/abs/1411.0836v2), §9.6 and Lemma 9.7, and [Xu, arXiv:0805.3295v2](https://arxiv.org/abs/0805.3295v2), §3.1. In the two-arrow permutation module, one order-two generator swaps the arrows and the other fixes them. Taking `x=g−1`, `y=h−1` gives

`A=K[x,y]/(x²,y²),   M=A/(y),   B=[[A,M],[0,K]]`.

Thus `dim_K B=4+2+1=7`. This is not the direct sum of two trivial modules. A different nontrivial quotient of the elementary abelian group is carried to this one by a group automorphism. The right-module convention visible in the category arrows and the left-module convention in the displayed triangular algebra differ by passage to the opposite algebra if composition is fixed the other way; reversal signs disappear in characteristic two. The candidate computes the displayed upper triangular algebra directly, so it does not rely on an unmentioned orientation change for its chain formulas.

Hermann §9.4 records the ambient characteristic-two Gerstenhaber algebra. Proposition 6.12 supplies Happel's sequence and Gerstenhaber compatibility. More specifically, Lemma 6.9(3), with its proof, identifies the map to the module Ext algebra with tensoring a bimodule extension by `M`. I checked this identification rather than infer it merely from the shape of a long exact sequence.

## 2. Ambient resolution and exact cup-coordinate normalization

For `D=K[t]/(t²)`, put `z=t_L+t_R` in `D^e`. Multiplication by `z` has image and kernel both spanned by `t_L+t_R` and `t_Lt_R`. The kernel of the augmentation `D^e→D` is the same image. Since `z²=0`, the asserted one-generator-per-degree bimodule complex is exact. This uses characteristic two genuinely.

Tensoring the two complexes over the field gives the resolution with degree-`n` generators `e_(i,j)`, `i+j=n`, and differential

`d e_(i,j)=(x_L+x_R)e_(i−1,j)+(y_L+y_R)e_(i,j−1)`.

After applying `Hom_(A^e)(−,A)`, the differential is zero. Each coefficient on each generator therefore specifies a distinct cohomology class; there is no residual coboundary quotient that could change the proposed coordinates.

I checked the claimed comparison to the normalized bar resolution directly. Sum all words with `i` copies of `x` and `j` copies of `y`. Every internal adjacent unlike-letter multiplication occurs twice with the same remaining tensor and cancels. Equal adjacent letters multiply to zero. The surviving left and right endpoint terms are precisely the four terms in the displayed small differential. The degree-zero comparison is the identity on the augmentation, so the comparison theorem applies.

Evaluating the cup cochain `∂_x^cup i cup ∂_y^cup j` on that shuffle gives one: only the word with the first `i` inputs equal to `x` and the remaining `j` equal to `y` survives. Evaluation on another degree-`n` summand is zero. In particular there is **no binomial or factorial coefficient** that could disappear in characteristic two. This verifies the exact algebra coordinates

`HH*(A)=K[x,y,u,v]/(x²,y²),   u=[∂_x], v=[∂_y]`.

The derivation/function and derivation/derivation brackets fix `[u,x]=[v,y]=1` and all other generator brackets as zero. The Gerstenhaber biderivation identity then uniquely determines the canonical Poisson formula in the candidate. All signs become plus in characteristic two. This is valid for every polynomial, not just for derivations or square-free positive-degree generators.

## 3. All-degree characteristic map

The module resolution `Q_n=A`, with differential multiplication by `y`, is exact because `ann_A(y)=yA`. Its cochain differential after applying `Hom_A(−,M)` is zero. The period-one identity shift lifts the generator `η`, so the Yoneda algebra is exactly `M[η]`, with no relation on positive powers of `η`.

The bimodule resolution `P` remains exact after tensoring on the right with `M`. To justify this without a flatness assumption on `M`, regard the augmented resolution of `A` as a complex of right `A`-modules: its terms are projective, its augmentation target `A` is projective, and successively splitting the short exact sequences makes it split exact. Tensoring preserves that splitting. Each term of `P⊗_A M` is free as a left `A`-module, because it is a direct sum of `A⊗_K M`.

The comparison

`j_n(1)=e_(0,n)⊗1`

is left `A`-linear, induces the identity on `M`, and commutes with the differential: the `y_R` term annihilates `1∈M`, and only `y_L` remains. Thus it compares two actual projective resolutions of `M`, in every degree. A coefficient cochain on `e_(i,j)` evaluates after this comparison to zero for `i>0`, and to the coefficient modulo `y` for `i=0`. The normalized identification of §2 now gives

`χ(x)=x, χ(y)=0, χ(u)=0, χ(v)=η`.

This derivation verifies both the map and its coordinates. It does not depend on finite tests or on choosing an arbitrary polynomial-ring isomorphism. The map is onto in every degree, with kernel `(y,u)`.

## 4. Why the original gamma map is injective, including degree zero

Happel's sequence, with the characteristic map identified above, gives injectivity of `HH^n(B)→HH^n(A)` for every positive `n`, since the preceding characteristic map is onto. For `n=1`, the preceding map is instead

`A⊕K → End_A(M),   (a,c)↦(a mod y)−c`,

which is also onto. The degree-zero center consists exactly of diagonal pairs with `a mod y=c`. Commutation with the two corner idempotents first removes every off-diagonal central component. Projection to `A` is then injective and has image `K+yA`. This is why the answer contains `1` but not `x` in degree zero.

I also rederived the restriction/coefficient-map comparison from the relative complex, to rule out a map-identification gap. Let `E=Kf⊕Ke`, and use normalized `E`-relative Hochschild cochains. Since `E` is separable, this computes ordinary Hochschild cohomology. For positive degree `n`, admissible inputs are either all in `A/K`, or `n−1` such inputs followed by one `M` input. There is no positive-degree `K/K` input and no second `M` input. Consequently

`C_B^n = C_A^n ⊕ D^(n−1)` for `n≥1`,

where `D^q=Hom_K((A/K)^tensor q ⊗ M,M)` is the cochain complex of the left-module bar resolution. In degree zero there is `A⊕K`. In characteristic two the mixed component of the differential consists of the module-bar differential plus the characteristic cochain

`(a₁,…,a_n,m) ↦ F(a₁,…,a_n)m`.

This is the mapping-cone origin of the same sequence and tensor characteristic map. With **coefficients in `A=B/BeB`**, the mixed component is forced to zero by the corner idempotents. The coefficient complex is just `C_A`, and the coefficient homomorphism is projection to the all-`A` component. Thus it is exactly the original question's gamma, not merely another map with the same dimensions.

The same corner argument handles insertions. On all-`A` inputs, every intermediate output has the `A` corner; mixed cochains cannot contribute. At arity zero, the `K` corner is killed by the all-`A` projection and relative normalization. Restriction therefore commutes with cup products and insertions, including brackets with degree-zero classes. This proves bracket compatibility directly in this example and agrees with the credited general theorem.

Finally `eBe=K`, and `Be⊗_K eB→BeB` is an isomorphism with no higher Tor. The stratifying hypothesis for the original coefficient sequence holds. Its additional coefficient-Ext descriptions in equation (10) follow from this sequence and injectivity; in particular `Ext^0_(B^e)(B,BeB)=0`, while `Ext^1` has dimension one. There is no missing kernel class or hidden Lie extension.

## 5. Image and bracket closure

Combining the positive-degree kernel with the degree-zero calculation gives precisely

`L=K·1+(y,u)R`, where `R=K[x,y,u,v]/(x²,y²)`.

The ideal `(y,u)` need not be a Lie ideal of all of `R`; that stronger assertion is neither used nor true in general. What is needed is its closure under brackets of its **own** elements. This follows by expanding brackets of `yF` and `uG`, and of two multiples of the same generator: the generator-generator bracket is zero, and every other term retains at least one factor `y` or `u`. Adding scalar constants leaves closure unchanged.

The monomial formula (4) is exactly formal differentiation of this Poisson bracket. Exponents reaching two in `x` or `y` vanish in the quotient; negative exponents arise only in summands with zero differentiation coefficient. The formula therefore handles every listed basis element, including all degree-zero/positive-degree pairs. The dimensions are `3` in degree zero and `4n+2` in positive degree, consistent with Xu's earlier calculation, but the audit accepts the result for the all-degree map and bracket proof, not for that numerical agreement.

The requested graded Lie structure has been completely determined. Extra characteristic-two squaring and higher operations are not part of this verdict; their exclusion in the candidate is appropriate to the question.

## 6. Independent exact diagnostics

The submitted checker was replayed in an isolated directory. Its **26,405 assertions** pass, and the generated receipt is byte-identical to the submitted receipt. The proof and verifier hashes match the frozen submission.

The separate standard-library `independent_checks.py` contains no import of the submitted checker. Its **166,464 assertions** pass. In particular it:

- constructs actual relative Hochschild cocycles for **33 basis classes** in degrees zero through three, solving for their mixed-component corrections rather than assuming that an ambient cochain extends;
- computes **884 actual relative-bar bracket pairs** with total input degrees at most five, including degree-zero insertion cases, then compares their shuffle-resolution coordinates with the claimed all-degree formula;
- verifies those bracket cochains are cocycles on all admissible inputs;
- checks the shuffle chain-map identity through degree ten, using cancellation of explicit normalized-bar terms;
- computes the bimodule and tensor-with-`M` differential ranks through degree twelve, verifies consecutive differentials compose to zero, and checks the `Q→P⊗M` comparison.

These are finite controls over the prime field. The proof above, not bounded testing, establishes all degrees and arbitrary characteristic-two coefficient fields.

## 7. Attribution and final disposition

Xu (2008) supplies the earlier example and ring calculation. Hermann (2016) supplies the general map and Gerstenhaber machinery, including the characteristic-two ambient presentation. Both are fully credited in the candidate.

An additional primary prior-work lead inspected during review is T. N. Oke's [2021 dissertation, *On the Lie Algebra Structure on Hochschild Cohomology of Koszul Quiver Algebras*](https://oaktrust.library.tamu.edu/server/api/core/bitstreams/5eb5d270-8ca9-435a-b7a6-c46d048dd123/content). Its related quiver-family discussion and low-degree homotopy-lifting examples reinforce the need for a cautious novelty statement. The inspected passages do not establish that the particular all-degree characteristic-two gamma presentation here was first obtained in this work. No such priority claim is accepted or needed. The dissertation's characteristic-not-two quotient theorem is not substituted for this problem.

**Final verdict: full mathematical PASS for the stated intended seven-dimensional algebra, its all-degree Lie presentation, and the original injective gamma map. No mandatory correction to the frozen mathematical snapshot.** A `claimed_solved` queue disposition is mathematically supportable for this exact source question, retaining the candidate's two approaches and all existing attribution/priority qualifications.
