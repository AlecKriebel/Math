# Adversarial check: the final Farinati–Solotar examples

Verdict: **the proposed implication is verified, with an essential convention qualification.** The 2004 result supplies a complete old counterexample class to the literal unrestricted-dimension, unrestricted-field, positive-cohomological-degree vanishing assertion. The tensor-induction bracket must be computed with the right translation below; it is not literally the bracket attached to the left translation used in FS. Their degree-one scalar brackets are negatives, so the nonzero example survives. This does not establish earlier publication of the exact finite27 model.

This is a narrow priority implication check. The previously passed mathematical gate is unchanged. I used the parent-specified target operation and independently checked the relevant conversion; I did not repeat the finite-model audit.

## Precisely inspected sources

[FS final journal PDF](https://bibliotecadigital.exactas.uba.ar/download/paper/paper_00029939_v132_n10_p2859_Farinati.pdf): Marco A. Farinati and Andrea L. Solotar, *G-structure on the cohomology of Hopf algebras*, Proc. Amer. Math. Soc. 132 (2004), 2859–2865, DOI 10.1090/S0002-9939-04-07274-0. Seven pages. The header dates electronic publication to 2 June 2004; receipt was 27 August 2002, revision 19 March 2003. Printed p.2864 was rendered and visually inspected in full.

On that page, Example 2.3 identifies the degree-one operation with convolution commutators of augmentation derivations. Example 2.4 treats coordinate algebras of connected affine algebraic groups and their tangent Lie brackets. The preceding embedding specializes in degree one to L_f=(id⊗f)Δ. These statements concern Ext_A(k,k); the later Drinfeld-double/GS application is separate.

[arXiv v1](https://arxiv.org/pdf/math/0207243v1), [dated record](https://arxiv.org/abs/math/0207243): submitted 25 July 2002, 23:54:48 UTC, five pages, with no later arXiv version listed. Direct inspection confirms the journal's Examples 2.3–2.4 are absent. Its Corollary 2.3 instead concerns GS cohomology. **The added examples are safely attributable by 2 June 2004, not to the arXiv submission date.** The receipt/revision dates do not date their insertion.

The final journal theorem numbering differs from v1: the embedding is Theorem 1.8 in the journal, 1.5 in v1. Theorem 2.1 and Corollary 2.2 concern the embedding/brace structure. No exact finite27 algebra is displayed in either inspected version.

For the target convention I checked [Karadağ–Witherspoon, author PDF, Theorem 4.1 and its induction setup](https://people.tamu.edu/~sjw/pub/KW13.pdf), dated 31 October 2021 on its title page and published in Pacific J. Math. 316 (2022), 395–407; and [Karadağ, §5, Lemma 5.1](https://arxiv.org/pdf/2010.07505), published in J. Pure Appl. Algebra 226 (2022), 106903. Bijectivity of the antipode suffices for that comparison; finite dimension is not imposed there.

## Independent construction and proof of the implication

Everything from here is a direct calculation, avoiding any generic smoothness or tangent-space convention needed in Example 2.4.

Let k=Q, H=k[x,y,z], and put

    Δx=x⊗1+1⊗x,   Δy=y⊗1+1⊗y,
    Δz=z⊗1+1⊗z+x⊗y,
    ε(x)=ε(y)=ε(z)=0,
    S(x)=-x,   S(y)=-y,   S(z)=-z+xy.

This is the coordinate Hopf algebra of the upper-unitriangular 3×3 group: the matrix with entries x,y,z at positions (1,2),(2,3),(1,3) multiplies according to

    (x,y,z)(x',y',z')=(x+x',y+y',z+z'+xy').

This gives the displayed coproduct, and matrix inversion gives S. Alternatively, direct coassociativity on z gives the same six terms in H⊗3; the antipode equations on z both reduce to -z+xy+z-xy=0. These identities hold on generators and extend multiplicatively. S²=id.

H⊗H is commutative. An ordinary quasitriangular structure would satisfy Δop(a)=RΔ(a)R^-1=Δ(a). But Δz−Δopz=x⊗y−y⊗x is a nonzero polynomial. Hence H is nonquasitriangular. No completed tensor product or topological notion of quasitriangularity is being used.

Let I=ker ε and f_x,f_y,f_z be the coefficient functionals of x,y,z. They vanish on 1 and I², so each is an augmentation derivation:

    f(ab)=ε(a)f(b)+f(a)ε(b).

Thus each is a scalar bar 1-cocycle representing Ext_H¹(k,k). In this complex δ⁰c(a)=ε(a)c−cε(a)=0, so B¹=0. In particular [f_z] is nonzero because f_z(z)=1. This explicitly verifies the cohomology class, not just a derivation in the Hochschild target.

Define L_f(a)=Σa₁f(a₂) and R_f(a)=Σf(a₁)a₂. Each is an algebra derivation when f is an augmentation derivation. Both split under ε: εL_f=εR_f=f. For convolution (f*g)(a)=Σf(a₁)g(a₂), coassociativity gives

    L_f L_g=L_(f*g),     R_f R_g=R_(g*f).

Consequently, with c=f*g−g*f,

    [L_f,L_g]=L_c,       [R_f,R_g]=-R_c.

Here c is again an augmentation derivation: expanding c(ab) cancels its two mixed scalar terms. Augmentation derivations on a polynomial algebra are determined by their values on x,y,z. For f=f_x and g=f_y, c(x)=c(y)=0 and c(z)=1; therefore c=f_z on all of H.

Explicitly the two embedded triples are

| f | L_f | R_f |
|---|---|---|
| f_x | ∂x | ∂x+y∂z |
| f_y | ∂y+x∂z | ∂y |
| f_z | ∂z | ∂z |

Their commutators are therefore

    [L_fx,L_fy]=+L_fz,    [R_fx,R_fy]=-R_fz.

The target operation is the latter. To see its orientation without an appeal to the names “left” or “right”, take the induced resolution X=H^e⊗_H P along h↦Σh₁⊗S(h₂). The degree-one bar comparison is

    ψ₁(a⊗b⊗c)=Σ(a⊗b₂c)⊗_H(1⊗b₁).

An induced scalar f evaluates (a⊗d)⊗_H(1⊗b) to af(b)d. Its pullback along ψ₁ is aR_f(b)c. This fixes the same tensor-induction convention as the target, rather than substituting FS's L_f embedding. The comparison theorem identifies the restricted degree-one Hochschild commutator with the target bracket. Applying the splitting ε gives exactly

    [[f_x],[f_y]]_target=-[f_z]≠0 in Ext_H¹(Q,Q).

There is also no hidden Hochschild-boundary issue: H is commutative, so all inner derivations vanish. More generally, applying ε to an inner derivation would already give zero. Both inputs have positive ordinary cohomological degree 1; in the shifted Lie grading they have degree 0, which is a different restriction.

## What this does and does not defeat

1. **Defeated:** a claim that a 2026 construction newly resolves the literal all-fields/all-dimensions yes/no question, or newly discovers the invariant-derivation obstruction. A smooth connected nonabelian coordinate group is already in the explicit 2004 theorem class; the displayed rational Heisenberg choice and convention check complete the implication.
2. **Not shown to be printed earlier:** the exact presentation F3[x,y,z]/(x³,y³,z³), its dimension 27, and that exact model's full reproducibility package. The generic augmentation-derivation result can be specialized to it, but generic inclusion does not establish that its exact presentation had appeared previously.
3. **Not settled by the rational example:** finite-dimensional characteristic-zero variants, or a restriction requiring both input degrees at least 2. The candidate finite27 addresses the finite-dimensional unrestricted-field case, while the rational model alone does not.
4. **Precision about priority language:** FS does not explicitly announce a resolution of the later OWR question, name this Heisenberg presentation, or identify its L operation with the later tensor-induction R operation. The supported statement is an earlier published counterexample class with a complete transparent implication, not a historical claim that its authors explicitly resolved that later wording.

Two source notational cautions do not break this argument. Example 2.4 prints I/I² as the tangent Lie algebra; the derivations used here are canonically (I/I²)*. Also, full duals of infinite-dimensional Hopf algebras need not themselves be ordinary Hopf algebras. Our convolution calculations are well-defined in Hom_k(H,k), and the concrete augmentation derivations lie in the finite dual because I² has finite codimension. Neither issue is used as an unsupported identification.

## Closure

The implication passes adversarial verification, with no error found in the parent's accepted finite-model mathematics. Only this shard's files were authored. No Git/index/ref, original packet, closed-review, global queue, or other shard was mutated, and no external communication was initiated. Retrieval hashes and page/version facts are retained; downloaded PDFs, extracted full text, and page rendering are removed at closure.
