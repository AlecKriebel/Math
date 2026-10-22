# Independent categorical and bar comparison derivation

This audit checks the saved counterexample; it adds no new proof-search turn. All algebra is over k=F3. The exact claim is the nonvanishing of the original exact-monoidal-category degree -1 bracket on Ext_H^1(k,k) for H=k[x,y,z]/(x^3,y^3,z^3), with primitive x,y and Delta(z)=z tensor1+1 tensor z+x tensor y. The scope is the unrestricted universal question, with cohomological degree-one inputs included.

## 1. Hopf/category hypotheses

The basis has 27 residue monomials. In characteristic three, commuting summands cube separately, so Delta respects all three truncations. On z, the two triple coproducts each give z11+1z1+11z+xy1+x1y+1xy. Generator equality extends because the coproducts are algebra homomorphisms. S(x)=-x, S(y)=-y, S(z)=-z+xy satisfies both convolution inverse identities and S^2=id. The tensor powers of the usual free bar resolution P of k are resolutions by the field Kunneth theorem; they are projective because tensoring a regular Hopf module with a vector-space module with diagonal action is free. This verifies the power-flat condition for the source bracket. Finite-dimensional modules suffice here, including all bar terms.

H tensor H is commutative. Thus the defining quasitriangular equality Delta^op(h)=R Delta(h) R^-1 would imply cocommutativity. But Delta(z)-Delta^op(z)=x tensor y-y tensor x is nonzero in the tensor monomial basis. Equivalently, a braiding on all H-modules yields R by evaluation on the pair of regular modules, so this module category is not braided. This does not confuse a commutative algebra with a cocommutative coalgebra.

## 2. Make the functor and bracket naturality explicit

Put i(h)=sum h1 tensor S(h2) in H^e=H tensor H^op. The exact functor F(M)=H^e tensor_H M can be identified with M tensor H through

T((a tensor c) tensor_H m)=sum a1 m tensor a2 c.

Its inverse is m tensor b -> (1 tensor b) tensor_H m. Balancedness and the inverse identity follow from sum h1 tensor h2 S(h3)=h tensor1 and sum h1 tensor S(h2)h3=h tensor1. In this model,

a.(m tensor b).c=sum a1 m tensor a2 b c.

The functor is exact because the displayed model is tensoring vector spaces with H. Its objects are free right H-modules. They are also free left H-modules: a tensor m -> sum a1 m tensor a2 maps H tensor M with regular first-factor action to M tensor H with diagonal action; inverse is m tensor a -> sum a2 tensor S^-1(a1)m. Bijectivity of S is thus a sufficient explicit hypothesis, and holds here. F carries free H-modules to free H^e-modules, hence projectives to projectives.

The strong monoidal isomorphism is

eta: (U tensor H) tensor_H(V tensor H) -> (U tensor V) tensor H,
eta((u tensor a) tensor_H(v tensor b))=sum(u tensor a1v) tensor a2b,

with inverse (u tensor v) tensor c -> (u tensor1) tensor_H(v tensor c). Balancing uses the left diagonal action on the second factor. H-bimodule linearity and naturality follow by expansion; the associativity condition is exactly coassociativity of Delta. The unit identification F(k)=k tensor H -> H is scalar multiplication. Thus F lands in the left-right-projective exact monoidal category used by the OWR source, and F(P) remains projective and power flat.

For completeness, write a homotopy lifting for f as t_f, with d t_f-(-1)^(m-1)t_f d=(f tensor1-1 tensor f)Delta_P and the augmentation compatibility condition. Applying F, transporting Delta_P by eta^-1, and using naturality transforms the right side to (F(f) tensor1-1 tensor F(f))Delta_F(P). The augmentation condition transports by the unit identification as well. Composition is preserved, so the formula f t_g-(-1)^((m-1)(n-1))g t_f is preserved. This is the mechanism in KW Theorem3.3/Corollary3.5 and Theorem4.1. We require projective preservation specifically verified above; exactness alone would not suffice for an arbitrary functor.

This proves why the bracket transported here is the exact categorical bracket, rather than simply a chosen operation on Hochschild cohomology. The OWR final paragraph independently identifies this same induction functor and restriction.

## 3. Reconstruct and orient the actual degree-one comparison

Let P1=H tensor H with d_P(a tensor b)=ab-a epsilon(b). Let B1=H tensor H tensor H be the bimodule bar term and X1=H^e tensor_H P1. In coordinates (a,c,b) for (a tensor b) tensor_H(1 tensor c),

d_X(a,c,b)=sum ac1 tensor S(c2)b-epsilon(c)a tensor b.

Define

psi1(a tensor c tensor b)=sum(a tensor c2 b) tensor_H(1 tensor c1),
theta1((a tensor b) tensor_H(1 tensor c))=sum a tensor c1 tensor S(c2)b.

Their compositions are identities by the two antipode cancellation identities. Moreover d_X psi1(a tensor c tensor b)=ac tensor b-a tensor cb, the ordinary bar differential. Both are H-bimodule linear and lift the degree-zero identity. They are precisely the degree-one specialization of the actual inverse bar comparisons in K Lemma5.1. One may also extend them in every degree by applying coproducts separately to the interior bars; no alternative embedding has been substituted.

A scalar cocycle f on P induces F(f):X1->H given by (a,c,b)->af(c)b. Composing with psi1 yields a R_f(c)b, where

R_f(c)=sum f(c1)c2.

There is no unsupported choice of left-versus-right translation here. Since f(ab)=epsilon(a)f(b)+f(a)epsilon(b), R_f is an algebra derivation by applying Delta to a product. Applying epsilon gives epsilon R_f=f. If an R_f is a Hochschild boundary, it is inner, and its composition with epsilon is zero, so f=0. This proves degree-one injection without relying on a nonzero cochain alone. More generally the adjoint-module map k->H splits by epsilon, yielding the cohomology injection through induction.

## 4. Actual bracket, scalar closure, and nonboundary

For fx,fy,fz extracting the linear monomial coefficients, each f vanishes on1 and I^2, so it is an augmentation derivation. In the unnormalized scalar bar complex delta0(c)(a)=epsilon(a)c-c epsilon(a)=0. Thus B1=0 and fz(z)=1 proves its nonzero Ext class.

The induced derivations are

Dx(x)=1, Dx(y)=0, Dx(z)=y;
Dy(x)=0, Dy(y)=1, Dy(z)=0;
Dz(x)=0, Dz(y)=0, Dz(z)=1.

Their commutator is -Dz on all three algebra generators, hence on every element. In Hochschild degree one the ordinary Gerstenhaber insertion is composition, and the sign is (-1)^((1-1)(1-1))=1. Thus [Dx,Dy]=-Dz. By the naturality above and injection, the exact categorical bracket satisfies [[fx],[fy]]=-[fz] !=0. It is already in the scalar-cohomology image. This calculation does not project a potentially unrelated HH class into scalar cohomology.

Equivalently, if convolution means f*g=(f tensor g)Delta, then R_f R_g=R_(g*f), hence [R_f,R_g]=R_(g*f-f*g). Here fx*fy(z)=1 and fy*fx(z)=0. This is a separate orientation check. The other translation L_f=(id tensor f)Delta instead gives [L_fx,L_fy]=+L_fz. FS uses that other translation, so its formula cannot be silently substituted into the tensor-induction map above. Either sign is nonzero; the proof fixes the sign by the actual comparison.

## 5. Source scope and excluded variants

The complete Witherspoon contribution occupies printed1114-1117. It defines H*(C) by ordinary Ext^n for n>=0, defines the Hopf case over a field k, then asks whether the bracket always vanishes for nonquasitriangular Hopf algebras. Its final paragraph explicitly identifies the exact induction embedding above and the Hochschild restriction. This supports the unrestricted negative answer with cohomological degree-one inputs. In the shifted Lie grading these inputs have degree zero; that shift does not turn them into cohomological degree zero.

Characteristic zero is stated in the next, separately titled contribution on printed1117. It is not an assumption in Witherspoon's contribution. An infinite-dimensional characteristic-zero analog is outside this audit, as are a finite-dimensional characteristic-zero problem and a new input-degrees>=2 problem. No solution of those variants is claimed.

KW sections2-4 use a field and a bijective antipode. Their later characteristic-zero Taft setup is local to section5. K section5 likewise requires a bijective antipode without imposing characteristic zero there; the characteristic-zero truncated-polynomial Hochschild example in its section3 is separate. FS Theorems1.5/2.1 have no finite-dimensional restriction for the Hopf-to-Hochschild construction; its Drinfeld-double application is a different cohomology. No Hermann theorem beyond the identification explicitly supplied by OWR/KW is needed.

Strongest verified result: the candidate is a valid finite-dimensional characteristic-three counterexample to the complete unrestricted imported question and its printed OWR formulation. No central mathematical or source-scope gap remains for that claim. This is a bounded verification of a candidate, not a priority certification, formal proof-assistant certificate, or human review.
