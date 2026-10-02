# Turn 3: an explicit connected pathological spectrum

Substantive author turn **3/5**, for the **explicitly modified infinite-spectrum question**. This turn constructs a connected compact metrizable spectrum with the source's nonminimal tensor-product pathology. It uses a mapping torus of Wassermann's fully proved pair and a witness localized inside an open-interval ideal. It does not claim that the space is an interval, or that every connected compact space is realizable.

Let A_0,D_0,S and Π_0 be the credited seed from turn2. Choose one free generator a of F2 and let u=λ_a in A_0. The inner automorphism θ=Ad(u) preserves A_0 and D_0, sending e_g to e_ag. Form

 A_θ={F in C([0,1],A_0):F(1)=θ(F(0))},
 D_θ={F in C([0,1],D_0):F(1)=θ(F(0))}.                           (1)

Then D_θ is a MASA in the unital C*-algebra A_θ. There is a C*-norm α_θ such that D_θ⊗D_θ is not a MASA in A_θ⊗_β A_θ for every β>=α_θ, including max. Its spectrum is the connected mapping-torus space described in §5.

## 1. MASA and interior ideal

Let J=C0((0,1),A_0), identified with the sections in A_θ vanishing at both endpoints. It is a closed two-sided ideal. If F in A_θ commutes with D_θ, then at any interior t it commutes with every d in D_0: choose a scalar continuous bump equal to1 at t and zero at the endpoints, multiply it by the constant section d, and use that this section belongs to D_θ. Thus F(t) lies in D_0 for every interior t. Continuity and the closedness of D_0 give the same conclusion at the endpoints, so F is in D_θ. This proves maximal abelianness without incorrectly treating all constant D_0 sections as satisfying the twisted boundary condition.

Evaluation e at t0=1/2 is a surjective unital *-homomorphism A_θ→A_0. Surjectivity follows by multiplying any constant A_0-valued function by an interior bump equal to1 at t0. There is no assumed *-homomorphic constant-section splitting of e.

## 2. Why maximal tensor products are injective on ideals here

We require the canonical inclusion

                        J⊗_max J → A_θ⊗_max A_θ                 (2)

to be isometric. This is the ideal-specific fact, and the proof matters: the analogous assertion for arbitrary subalgebras is false.

More generally let I and K be closed two-sided ideals of C*-algebras A and B. A pair of commuting nondegenerate representations π of I and ρ of K extends uniquely to representations of A and B on the same Hilbert space. For example the extension of π is determined densely by

                       π_bar(a)π(i)ξ=π(ai)ξ.

It is bounded by ||a|| and equals the strong limit of π(ae_λ) for a contractive approximate identity e_λ of I. Every π(ae_λ) commutes with ρ(K), so π_bar(A) does also. Similarly ρ_bar(B) is obtained as strong limits of elements of ρ(K), proving that the extended ranges commute. In the universal commuting-representation definition of the maximal tensor norm one can restrict to the common essential subspace, so degenerate parts do not affect the norm on I⊙K. Every testing pair for I⊙K therefore extends to a testing pair for A⊙B. This proves that its maximal norm is preserved by the inclusion; the reverse norm inequality is functorial contractivity. Applying this to I=K=J gives (2).

By maximal-tensor associativity and the nuclearity of the abelian function algebras, there is the canonical identification

 J⊗_max J ≅ C0((0,1)², A_0⊗_max A_0).                           (3)

One can obtain it by first reordering the four commuting tensor factors C0((0,1)), A_0, C0((0,1)), A_0, then using the unique tensor norm of the two function factors. This is a standard universal-property identification, not a claim about exchanging arbitrary tensor norms with fibers.

## 3. A localized nonzero kernel element

Let q_max:A_0⊗_max A_0→A_0⊗_min A_0. The source's representation Π_0 is not minimal-norm continuous. Therefore its extension to the maximal completion cannot vanish on ker(q_max): otherwise it would factor as a representation of the minimal quotient. Choose

 x0 in ker(q_max) with Π_0(x0)≠0.                               (4)

The source compact-ideal argument from turn2 shows that **every** element of this kernel commutes with D_0⊗1 and1⊗D_0. If desired x0 can be replaced by x0* x0, preserving (4) and making it positive.

Choose f in C_c((0,1)) with 0<=f<=1 and f(t0)=1. Under (2)–(3), the function

                           X(t,s)=f(t)f(s)x0                     (5)

gives an element X in A_θ⊗_max A_θ. It is nonzero. For F,G in D_θ, multiplication on the ideal is pointwise in (3), and

 [X(t,s),F(t)⊗G(s)]=0

by the seed commutation property. Hence X commutes with D_θ⊗D_θ. Natural compatibility of the maximal-to-minimal maps with the ideal inclusion gives

       Ψ_max(X)=0 in A_θ⊗_min A_θ,                              (6)

since under the corresponding function-algebra identification it is the function f(t)f(s)q_max(x0)=0. This does not require recovering X by its fibers in an unspecified intermediate norm.

Define on the algebraic tensor product

 ||w||_(αθ)=max{||w||_min, ||Π_0((e⊙e)(w))||}.                   (7)

As in turn2, this is a C*-crossnorm: the second term is a representation seminorm bounded by the product norm on elementary tensors, and the minimal term is a faithful crossnorm. Its witnessing representation extends from the maximal completion, and evaluation at (t0,t0) sends X to x0. Thus

                    Π_0((e⊗e)(X))=Π_0(x0)≠0.                   (8)

In particular X has nonzero image in the αθ completion.

## 4. Every larger tensor norm remains bad

Let β>=αθ, and let X_β be the image of X under the canonical surjection from the maximal completion to the β completion. The map from that completion onto the αθ completion and (8) show X_β≠0. Its commutation with D_θ⊗D_θ survives the quotient, and its image in the minimal completion is zero by (6).

The minimal quotient is isometric on the closed copy of D_θ⊗D_θ, because D_θ is abelian. Hence X_β cannot belong to that copy. It is therefore a genuine extra element of the relative commutant, proving the claimed pathology for every β>=αθ. This argument handles intermediate norms by quotients of one explicitly localized maximal witness, instead of presuming that evaluation describes every fiber of those completions.

## 5. The spectrum is connected, and its exact topology is stated

Write σ(g)=ag for g in F2 and σ(infinity)=infinity on S. The automorphism on D_0=C(S) is θ(h)=h∘σ^(−1). Therefore the spectrum of D_θ is

                  Y=(S×[0,1])/((s,1)~(σ^(−1)(s),0)).            (9)

Continuous functions on this quotient are exactly the functions obeying (1), so the spectrum identification follows directly. The equivalence relation only pairs the two endpoint copies via a homeomorphism; it is closed. Thus Y is compact Hausdorff, and it is metrizable, for instance by the standard mapping-torus construction over the compact metrizable space S.

The point infinity is fixed by σ, so its suspension in Y is a copy of the circle. Every orbit of a finite point g is {a^n g:n in Z}, since a has infinite order. The suspension of this discrete orbit is homeomorphic to the real line. It is an open subspace: the orbit is an open invariant subset of S, and the quotient restriction has the corresponding mapping-torus topology.

For each such line L_g, its closure contains the entire infinity circle. To see this, hold the interval parameter t fixed and take n→infinity in a^n g; these points escape every finite subset of F2, so converge to infinity in S. Their images in Y approach the circle point with parameter t. The closure of each L_g is connected, since L_g is connected, and all these closures contain that circle. Their union covers Y. Therefore Y is connected.

The infinity circle is embedded and closed. In particular Y is not homeomorphic to an interval. More simply, the positive result here concerns the exactly specified space (9), and no local-connectedness, manifold or interval identification is used. The report's announced [0,1] example remains a separately attributed statement.

## 6. What this adds, and what is not justified

Turn2 produced disconnected convergent-sequence products and Cantor cubes. The interior-ideal argument supplies a connected example while retaining all the source tensor-norm quantifiers. It can also be used for other explicitly defined continuous-section algebras when the same interior ideal and diagonal commutation conditions have been verified.

It does not show that arbitrary quotients of a realized spectrum are realized, or that an arbitrary compact Hausdorff space can be obtained as this mapping torus. Replacing the twisting by a quotient that collapses diagonal points can alter both the ambient algebra and the kernel witness. No such transfer is being assumed. The explicitly infinite-spectrum realization problem remains **unresolved3/5**, with two substantive turns left.
