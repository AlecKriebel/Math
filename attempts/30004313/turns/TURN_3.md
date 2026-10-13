# Turn 3: exact retraction classification over arbitrary Rees multiplication

**Unreviewed partial,3/5 substantive author turns. Original general characterization remains unresolved.** This turn treats a genuine interaction between a freely chosen additive retraction and arbitrary completely simple multiplicative sandwich data. In particular it allows nonhomomorphic retractions and does not replace the group inverse by an invalid inverse anti-homomorphism.

## 1. Retractions onto multiplicative left ideals

Let S be any completely regular semigroup and f:S→S a map. Define a+b=f(b). As in Turn1, associativity is equivalent to f²=f. In the full noncommutative setting, the brace identity is exactly

    a f(c)=f(a f(c))   for all a,c.                       (1.1)

Consequently these laws form a generalized left semi-brace if and only if f is an idempotent retraction onto a nonempty multiplicative left ideal J=f(S). No additive cancellation or multiplicative homomorphism condition on f is required. The associated map is

    r(a,b)=(a f(b), f(b)^- b).                            (1.2)

This observation describes the entire a+b=f(b) family over arbitrary completely regular multiplication, before imposing Yang–Baxter.

A left ideal J of a completely regular semigroup is closed under group inverses: for x∈J, x^-=(x^-)²x∈J. Thus J itself has completely regular multiplication. This fact will be used only with its actual stated hypothesis.

## 2. Normalize one column-ideal in a Rees presentation

Take any Rees multiplication from Turn2,

    (i,g,λ)(j,h,μ)=(i,g p_(λ,j) h,μ)

on I×G×Λ, with G a group, I and Λ nonempty and every p_(λ,j)∈G. Fix λ0∈Λ. The set J=I×G×{λ0} is a multiplicative left ideal.

There is no loss in normalizing p_(λ0,j)=1 for every j. Specifically, put v_i=p_(λ0,i), replace P by

    p'_(λ,j)=p_(λ,j) v_j^(-1),

and use the bijection N(i,g,λ)=(i,v_i g,λ). Direct multiplication shows that N is a semigroup isomorphism from P to P'. Conjugating f by N preserves its being a retraction onto J and preserves the associated braid property. This normalization does not assert that the whole sandwich matrix factors or that the multiplication is a rectangular group.

Henceforth assume the λ0 row of P is all1. Let f be an arbitrary retraction onto J. Write

    f(i,g,λ)=(F(i,g,λ), ψ(i,g,λ), λ0).                    (2.1)

On J it is the identity, so F(i,g,λ0)=i and ψ(i,g,λ0)=g. By §1, every such f gives a generalized left semi-brace through a+b=f(b).

## 3. Complete Yang–Baxter criterion in this family

**Theorem.** In the setting of §2, the associated map satisfies Yang–Baxter if and only if

1. F(i,g,λ)=i for all i,g,λ;
2. for each i,λ the map H_(i,λ):G→G defined by

       H_(i,λ)(g)=ψ(i,g,λ)^(-1)g

   is idempotent under composition.

Here H_(i,λ0) is necessarily the constant map1. The other H_(i,λ) can be arbitrary idempotent set maps of G: they need not be group homomorphisms, need not fix1 and need not have subgroup images.

### Proof by all three braid coordinates

For a=(i,g,λ), b=(j,h,μ), write f(b)=(k,q,λ0). Because the normalized λ0 row is1, the group inverse of f(b) is (k,q^(-1),λ0), and the literal source formula becomes

    r(a,b)=((i,g p_(λ,k)q,λ0),(k,q^(-1)h,μ)).             (3.1)

Let c=(l,z,ν), f(c)=(m,t,λ0). Also put

    f(m,t^(-1)z,ν)=(n,u,λ0).

Every first output in(3.1) belongs to J, where f is the identity. Three direct applications therefore give

    r_12 r_23 r_12(a,b,c)
      =((i,g p_(λ,k)h p_(μ,m)t,λ0),
        (k,1,λ0),
        (m,t^(-1)z,ν)),                                  (3.2)

    r_23 r_12 r_23(a,b,c)
      =((i,g p_(λ,j)h p_(μ,m)t,λ0),
        (j,u,λ0),
        (n,u^(-1)t^(-1)z,ν)).                            (3.3)

Equality of middle row indices forces k=j for every b. Thus F preserves the row index; this necessity uses a coordinate actually present in the equation and no cancellation of arbitrary semigroup elements. Once F preserves rows, the first outputs in(3.2)–(3.3) agree, m=l, and n=m. The remaining condition is u=1, namely

    ψ(l, ψ(l,z,ν)^(-1)z, ν)=1.                           (3.4)

It is also sufficient: the middle group coordinates become1 and the third outputs agree. If H(g)=ψ(g)^(-1)g, condition(3.4) says ψ(H(g))=1, which is equivalent to

    H(H(g))=H(g),

by cancellation in the group G only. This proves the theorem.

Conversely, starting with arbitrary idempotent maps H_(i,λ), with H_(i,λ0)≡1, set

    ψ(i,g,λ)=g H_(i,λ)(g)^(-1),
    f(i,g,λ)=(i,ψ(i,g,λ),λ0).                            (3.5)

It is a retraction onto J. Equation(3.4) follows from H²=H, and the theorem gives a solution. Equations(3.5) recover every retraction in the classified family. This is a structural parametrization by idempotent transformations, rather than a renamed full braid identity.

The sandwich matrix P is arbitrary after normalization; in particular the result includes nonorthodox completely simple multiplication. The theorem classifies all f with this fixed one-column image, not all possible additive semigroup laws or all multi-column images.

## 4. A simple nonhomomorphic retraction that yields a solution

Take the normalized rectangular group with G=C2={1,s}, I and Λ each of size2, and let λ0 be one column. Put H_(i,λ0)≡1 and H_(i,λ1)=id_G for both rows. Then

    f(i,g,λ0)=(i,g,λ0),
    f(i,g,λ1)=(i,1,λ0).

This gives a solution by the theorem. It is not a multiplicative endomorphism: with a=(i,s,λ0), b=(j,1,λ1), one has

    f(ab)=(i,1,λ0),    f(a)f(b)=(i,s,λ0).

Thus an endomorphism requirement would discard genuine solutions, even in this elementary completely regular setting. The same parametrization permits idempotent maps with images that are merely subsets of a nonabelian group.

## 5. A complementary exact criterion when the retraction is an endomorphism

There is also a useful all-completely-regular statement, although its endomorphism hypothesis is genuinely restrictive by §4.

Let f be an idempotent multiplicative endomorphism of an arbitrary completely regular S whose image J is a left ideal, and use a+b=f(b). Then the associated map is a Yang–Baxter solution if and only if J satisfies

    (xy)^0=(x^0 y)^0   for all x,y∈J.                     (5.1)

This is precisely the source's right-zero-addition criterion on the image J.

Proof. A multiplicative homomorphism preserves the commuting group inverse by uniqueness. Since a f(b) belongs to J,

    a f(b)=f(a f(b))=f(a)f(b).

Define h(b)=f(b)^-b. Write p=f(a), q=f(b), t=f(c). Then

    f(h(b))=q^0,    h(h(b))=h(b).

The second identity follows by substituting the first and using q^0 q^-=q^-. Also b t=f(b)t=q t because b t belongs to J. A direct calculation of the braid words gives

    (pqt,(q^0t)^0,h(c)),
    (pqt,(qt)^0 t^0,h(c)).

The identity (qt)t^0=qt implies (qt)^0 t^0=(qt)^0, by left multiplication by (qt)^-. Thus(5.1) is sufficient. Necessity follows either from this calculation and surjectivity onto J, or by restricting r to J, where f is the identity. No general inverse anti-homomorphism is used.

This statement does not claim that every solution in §1 has an endomorphic f; §4 proves otherwise. It also does not claim that every completely regular multiplication automatically satisfies(5.1).

## 6. Finite checks and remaining original gap

verify_turn3.py checks the entire one-column retraction family for two normalized eight-element Rees semigroups over C2, including a nonfactorizing sandwich matrix. It compares the structural criterion with all three braid outputs. It also checks selected arbitrary idempotent transformations over the noncommutative group S3, tests normalization of sandwich matrices, and validates the nonhomomorphism example. These are finite diagnostics for the displayed all-size proofs.

The original target still allows arbitrary associative additions and completely regular semigroups outside a single completely simple presentation. The one-column retraction theorem does not classify multi-column retractions or all additions on that presentation. No theorem reduces every generalized semi-brace to the families here. Three substantive turns are complete, with two remaining; no final full-resolution or novelty claim is made.
