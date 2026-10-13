# Turn 4: multi-column retractions and their coupled labels

**Unreviewed partial,4/5 substantive author turns.** This resolves the multi-column coupling left open by Turn3, while preserving the restriction that addition has the form a+b=f(b). It does not classify general additions in the original source. No novelty is asserted.

## 1. All multiplicative left ideals in the explicit Rees presentation

Let S=I×G×Λ with

    (i,g,λ)(j,h,μ)=(i,g p_(λ,j)h,μ),

where I,Λ are nonempty, G is any group and every p_(λ,j) lies in G. No sandwich factorization or normalization is assumed.

Every nonempty left ideal has the form

    J=I×G×Λ0

for a nonempty subset Λ0⊆Λ. Indeed, containing one (i,g,λ) and being closed under arbitrary left multiplication forces it to contain every (j,h,λ): fix any μ and multiply on the left by (j,h g^(-1)p_(μ,i)^(-1),μ). Conversely any union of full columns is a left ideal.

Let f:S→J be an arbitrary retraction, so f is the identity on J. By Turn3§1, the addition a+b=f(b) is associative and satisfies the generalized semi-brace law. Thus this describes every compatible addition of this form over the presented multiplication.

Write, for b=(j,h,μ),

    f(b)=(F(b),Q(b),K(b)),       K(b)∈Λ0,
    h_f(b)=f(b)^- b.                                     (1.1)

The symbol h_f denotes a map, not the group coordinate h. The associated source map is r(a,b)=(a f(b),h_f(b)).

## 2. Exact criterion, without an endomorphism assumption

**Theorem.** The associated map is a Yang–Baxter solution if and only if

    F(j,h,μ)=j   for every (j,h,μ),                       (2.1)
    f(h_f(b))=f(b)^0   for every b.                       (2.2)

Condition(2.1) says f preserves the multiplicative row, or equivalently the Green R-class in this Rees presentation. Condition(2.2) includes a column compatibility condition and a local-group identity. Neither says that f is a multiplicative endomorphism.

### Necessity of row preservation

All first outputs of r lie in J, since J is a left ideal. For a,b,c, put

    u=a f(b),   v=h_f(b),   w=v f(c),   z=h_f(c).

As w∈J, the second output when r is applied to (u,w) is w^-w=w^0. Its row is the row of v, namely F(b).

For the other braid word, put p=b f(c)∈J. The second output of r(a,p) is p^0, whose row is the original row j of b. The first output of r(p^0,h_f(c)) retains that row j. Equality of the middle braid outputs therefore forces F(b)=j, for all b. This uses the actual middle coordinate and does not cancel semigroup elements.

### Complete braid calculation after row preservation

If f(b) and b have the same row, direct multiplication with the Rees local identity gives

    f(b)^0 b=b,      (a f(b))h_f(b)=ab.                  (2.3)

Also h_f(b) has the same row and column as b. For c=(l,z,ν), set δ=K(c). Then h_f(b)f(c) and b f(c) both have the original row j of b and column δ. Their local group identities are therefore equal:

    (h_f(b)f(c))^0=(b f(c))^0
                    =(j,p_(δ,j)^(-1),δ).                (2.4)

The complete braid outputs simplify to

    (abc_f, (b f(c))^0, h_f(c)),                         (2.5)
    (abc_f, (b f(c))^0 f(h_f(c)), h_f(h_f(c))),           (2.6)

where abc_f means ab f(c), without an additive operation.

Write f(h_f(c))=(l,q,ε), using row preservation again. The middle entry of(2.6) is

    (j,p_(δ,j)^(-1)p_(δ,l)q,ε).

It equals the middle entry of(2.5) exactly when ε=δ and q=p_(δ,l)^(-1). This is precisely f(h_f(c))=f(c)^0. Thus (2.2) is necessary.

Conversely, (2.2) makes the middle outputs agree and gives

    h_f(h_f(c))=(f(c)^0)^- h_f(c)
                 =f(c)^0 f(c)^-c=h_f(c),

so the third outputs agree as well. The first outputs already agree by(2.3) and the fact f is the identity on J. This proves both directions with all three coordinates checked.

## 3. Structural parametrization by residual maps and column labels

The criterion has a complete set-theoretic parametrization. For every row i∈I and original column μ∈Λ, choose maps

    H_(i,μ):G→G,          κ_(i,μ):G→Λ0.

Require

    H_(i,μ)²=H_(i,μ),      κ_(i,μ)∘H_(i,μ)=κ_(i,μ).       (3.1)

For μ∈Λ0 prescribe specifically

    H_(i,μ)(g)=p_(μ,i)^(-1),      κ_(i,μ)(g)=μ.            (3.2)

For the other columns, H is any idempotent transformation of the set G, and κ is any label assignment constant on its H-fibers. The image of H need not be a subgroup, and neither H nor κ is assumed to respect multiplication.

Define

    f(i,g,μ)=
       (i, g H_(i,μ)(g)^(-1)
                p_(κ_(i,μ)(g),i)^(-1), κ_(i,μ)(g)).        (3.3)

Equations(3.2) make f the identity on J, so it is a retraction onto J. Its residual map is exactly

    h_f(i,g,μ)=(i,H_(i,μ)(g),μ).                         (3.4)

To verify this, write δ=κ(g), q=g H(g)^(-1)p_(δ,i)^(-1). The group inverse of (i,q,δ) is

    (i,p_(δ,i)^(-1)q^(-1)p_(δ,i)^(-1),δ).

Multiplying it by (i,g,μ) cancels the adjacent sandwich factors and yields group coordinate p_(δ,i)^(-1)q^(-1)g=H(g), in the displayed order.

Using(3.3) on h_f(i,g,μ), condition f(h_f(b))=f(b)^0 is equivalent to the two equations in(3.1): its output column must remain κ(g), and its group coordinate must be p_(κ(g),i)^(-1), which after the column equality is precisely H(H(g))=H(g).

Thus every choice(3.1)–(3.2) produces a solution, and every solution retraction in §1 arises uniquely this way: recover κ from its output column and H from the group coordinate of h_f. This is an exact parametrization of the entire retracted-addition family over every presented Rees semigroup, not a rephrasing of three unknown braid maps.

When Λ0 is a singleton, κ has no freedom and this reduces to Turn3 after the row normalization there. For multiple columns, the condition κ∘H=κ is the additional compatibility; arbitrary pointwise column choices can fail it.

## 4. A concrete coupled-column failure

Take G=C2={1,s}, a single row, three columns {0,1,2}, and all sandwich entries1. Let Λ0={0,1}; f fixes those two columns. On column2 let H be the constant map1, but choose κ(1)=0 and κ(s)=1. Formula(3.3) still defines a retraction, hence a valid generalized left semi-brace, but its labels violate κ(H(s))=κ(s).

Explicitly f(1,2)=(1,0) and f(s,2)=(s,1), where the row is suppressed. For b=(s,2),

    h_f(b)=(1,2),     f(h_f(b))=(1,0),
    f(b)^0=(1,1).

They differ in column, so the theorem proves that r is not a solution. This shows why idempotence of each residual map alone is insufficient when several image columns are present. The obstruction is separate from the single-column group-coordinate condition already handled in Turn3.

## 5. Boundary of the result and exact remaining gap

This turn classifies all additions a+b=f(b) on any Rees-matrix completely simple multiplication. It covers every nonempty left-ideal image, arbitrary sandwich data, arbitrary groups and arbitrary index cardinalities, and it explicitly allows nonhomomorphic retractions and non-bijective solutions.

It does not classify additions genuinely depending on both arguments, such as the four-element failure in Turn2. Nor does it show that an arbitrary completely regular multiplicative semigroup, with its interactions among completely simple components, can be handled by independent retractions of this kind. The source's full question remains unresolved after4/5 substantive turns. The last turn must address that remaining structural issue or preserve it precisely; this theorem is not promoted to a full answer.
