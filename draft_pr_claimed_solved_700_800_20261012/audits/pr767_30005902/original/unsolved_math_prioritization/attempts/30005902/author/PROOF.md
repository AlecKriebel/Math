# A finite-dimensional counterexample to the unrestricted vanishing statement

Problem 30005902 / OWR-14298370-002. Date: 2026-10-05 UTC.

## Precisely what is proved

There is a **27-dimensional, non-quasitriangular Hopf algebra over F₃ with involutive antipode** for which the degree −1 bracket on **Ext_H^*(F₃,F₃)** is nonzero on a pair of classes in cohomological degree one.

Consequently, the statement with an unrestricted ground field is false. This is not a resolution of a variant requiring **both finite dimension and characteristic zero**. The calculation is a reconstruction from established Hopf-to-Hochschild machinery; no originality, priority, journal acceptance, or expert-review claim is made. Independent review of this packet is pending.

## 1. The Hopf algebra

Let k=F₃ and

H=k[x,y,z]/(x³,y³,z³).

The residue classes x^i y^j z^l, 0≤i,j,l≤2, form a basis, so dim_k H=27. Define algebra homomorphisms Δ:H→H⊗H and ε:H→k on generators by

Δx=x⊗1+1⊗x,
Δy=y⊗1+1⊗y,
Δz=z⊗1+1⊗z+x⊗y,
ε(x)=ε(y)=ε(z)=0.

These maps respect the defining relations: in characteristic three the cube of a sum of commuting elements is the sum of their cubes. In particular (Δz)³=0 in H⊗H.

Coassociativity is immediate for x and y. For z, either iterated coproduct is the sum

z⊗1⊗1 + 1⊗z⊗1 + 1⊗1⊗z
+ x⊗y⊗1 + x⊗1⊗y + 1⊗x⊗y.

Equality on generators proves equality everywhere because the iterated coproducts are algebra homomorphisms. The two counit identities also hold on generators, hence everywhere.

Define an algebra antihomomorphism (equivalently here an algebra homomorphism)

S(x)=−x, S(y)=−y, S(z)=−z+xy.

Its images satisfy the cube relations. Both antipode identities on z read −z+xy+z−xy=0; those on x and y are immediate. Since H is commutative, both convolution products m(S⊗id)Δ and m(id⊗S)Δ are algebra maps, so the generator checks prove the identities on H. Finally S² fixes all three generators. Thus S is bijective, indeed involutive.

The algebra H is commutative but its coproduct is not: Δz−Δ^op z=x⊗y−y⊗x≠0. If an invertible R∈H⊗H made H quasitriangular, its relation Δ^op(a)=RΔ(a)R⁻¹ would force Δ^op(a)=Δ(a), because H⊗H is commutative. This contradiction proves that H is not quasitriangular. Equivalently, its ordinary module category with the coproduct tensor product admits no braiding. No commutativity-to-braiding inference is used.

## 2. Scalar cohomology classes, including the boundary check

Use the augmented bar cochains C^n=Hom_k(H^{⊗n},k), with the trivial H-action defined by ε. This complex computes Ext_H^*(k,k). In degree one,

(δf)(a,b)=ε(a)f(b)−f(ab)+f(a)ε(b).

Let f_x,f_y,f_z pick out the coefficients of the basis monomials x,y,z respectively. Each vanishes on 1 and on (ker ε)²; therefore

f_t(ab)=ε(a)f_t(b)+f_t(a)ε(b),  t∈{x,y,z}.

They are all 1-cocycles. Their classes are nonzero: for any c∈C⁰=k, the 1-coboundary is

(δc)(a)=ε(a)c−cε(a)=0.

Thus **B¹=0**. In particular f_z(z)=1 already certifies that [f_z]≠0 in Ext_H¹(k,k). Equivalently, the reduced bar chain [z] is a 1-cycle and pairs to 1 with f_z. This checks cohomology, rather than merely displaying a nonzero cochain.

## 3. Identify the exact bracket and its embedding

The bracket under discussion has degree −1:

Ext_H^m(k,k) × Ext_H^n(k,k) → Ext_H^{m+n−1}(k,k).

For a Hopf algebra with bijective antipode, the tensor-induction embedding into Hochschild cohomology used in the OWR report identifies this bracket with the restricted Gerstenhaber bracket. This comparison is Theorem 4.1 of Karadağ–Witherspoon [KW]; the explicit bar comparison is also given in §5 of Karadağ [K]. Their assumption on the antipode is satisfied here.

For completeness, the degree-one embedding and its orientation can be read directly from that comparison. Write P₁=H⊗H for the left-module bar resolution of k, and X₁=H^e⊗_H P₁ for the induced bimodule resolution, where H→H^e is a↦Σa₁⊗S(a₂). The degree-one bar comparison is

ψ₁(a⊗b⊗c)=Σ(a⊗b₂c)⊗_H(1⊗b₁).

The map induced by f on X₁ sends (a⊗c)⊗_H(1⊗b) to af(b)c. Its composition with ψ₁ is therefore aR_f(b)c, where

R_f(b)=Σ f(b₁)b₂.

This fixes the right-translation convention; replacing it by Σb₁f(b₂) reverses the degree-one convolution-commutator sign. It does not affect nonvanishing.

An augmentation derivation f gives an ordinary derivation R_f. Indeed, using that Δ and ε are algebra maps,

R_f(ab)=Σ f(a₁b₁)a₂b₂=R_f(a)b+aR_f(b).

It is therefore a Hochschild 1-cocycle. Moreover εR_f=f. In degree one this splitting also proves injectivity on cohomology, since applying ε to an inner derivation gives zero.

## 4. Compute the nonzero cohomology bracket

Set D_x=R_{f_x}, D_y=R_{f_y}, D_z=R_{f_z}. Their values on algebra generators are

D_x(x)=1, D_x(y)=0, D_x(z)=y;
D_y(x)=0, D_y(y)=1, D_y(z)=0;
D_z(x)=0, D_z(y)=0, D_z(z)=1.

Equivalently D_x=∂_x+y∂_z, D_y=∂_y and D_z=∂_z. These derivations are well defined on the quotient because the derivatives of x³,y³,z³ vanish in characteristic three.

In Hochschild degree one the Gerstenhaber bracket is the ordinary commutator of derivations. Computing on x,y,z gives

[D_x,D_y]=D_xD_y−D_yD_x=−D_z.

A derivation of H is determined by its values on the algebra generators, so this is an equality of cochains on all of H. The bracket is visibly in the embedded scalar-cohomology subspace. By the bracket comparison and injection in §3,

[[f_x],[f_y]]=−[f_z] ≠ 0 in Ext_H¹(k,k).

The last inequality was proved in §2 by the explicit boundary calculation. Evaluating its representative at z yields −1=2 in F₃. This completes the counterexample.

## 5. Scope and interpretation

- Both inputs have positive **cohomological** degree, namely one. This is the grading used for H^*(C)=⊕_{n≥0}Ext_C^n(1,1) in the source. A separately restricted question excluding cohomological degree one is not asserted to be settled by this packet.
- The Hopf algebra is finite dimensional, and S²=id. Neither finite dimension nor bijectivity of the antipode removes this example.
- It is commutative, not cocommutative. Cocommutative Hopf algebras are quasitriangular via R=1⊗1 and are outside the example.
- The same presentation and argument work over every field of characteristic three, including an algebraic closure of F₃. No rational-point or algebraic-closure assumption is needed.
- This is Ext_H(k,k), not the full HH^*(H,H). The latter is used only as a bracket-compatible target, with the image explicitly checked. It is not Gerstenhaber–Schack cohomology of H, and no passage through the Drinfeld double is used.
- A finite-dimensional characteristic-zero interpretation is a different question. The source passage inspected here does not state that additional restriction; its surrounding Hopf-algebra definition is over a field k without a stated characteristic assumption. The next contribution's characteristic-zero convention is not imported across contributions.

## 6. Verification

Run `python3 verify_counterexample.py` from any directory, with the path adjusted as needed. It exhaustively checks the finite Hopf identities, scalar cocycles, the Hochschild derivations and their commutator. It separately computes rank δ¹=24 on the 27-dimensional unnormalized 1-cochain space, yielding dim H¹=3 because δ⁰=0. Four deliberate false alternatives are detected. The exact output is `results.json`.

These checks supplement the generator-level and cohomological proof above; they do not claim formal proof-assistant verification or human peer review.

## References

[OWR] Sarah Witherspoon, “Cohomology of monoidal categories,” in Hochschild (Co)Homology and Applications, Oberwolfach Reports 20/2024, contribution pp. 1114–1117. https://doi.org/10.4171/owr/2024/20 . Publisher PDF: https://ems.press/content/serial-article-files/49480 .

[KW] Tekin Karadağ and Sarah Witherspoon, Lie brackets on Hopf algebra cohomology, Pacific J. Math. 316 (2022), 395–407, especially §2 and Theorem 4.1. https://doi.org/10.2140/pjm.2022.316.395 . Inspected author PDF: https://people.tamu.edu/~sjw/pub/KW13.pdf . Preprint record: https://arxiv.org/abs/2101.09805 .

[K] Tekin Karadağ, Gerstenhaber bracket on Hopf algebra and Hochschild cohomologies, J. Pure Appl. Algebra 226 (2022), 106903, especially §5. https://doi.org/10.1016/j.jpaa.2021.106903 . Inspected preprint: https://arxiv.org/abs/2010.07505 .

[FS] Marco Farinati and Andrea Solotar, G-structure on the cohomology of Hopf algebras, Proc. Amer. Math. Soc. 132 (2004), 2859–2865, Theorems 1.5 and 2.1 in the inspected preprint. https://arxiv.org/abs/math/0207243 . This uses the other translation orientation; it is not silently identified with ψ₁ above.
