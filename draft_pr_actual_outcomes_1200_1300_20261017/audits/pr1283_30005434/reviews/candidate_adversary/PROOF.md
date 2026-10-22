# Independent reconstruction of the exact existence theorem

This proof was reconstructed after exposure to the submitted candidate and its formula. It is an independently checked derivation, not a blind discovery, human refereeing, or formal proof certification. The source convention and evidence boundaries are in REPORT.md. Work takes place in ordinary classical set mathematics.

## Claim and assumptions

Let X carry an associative, commutative, idempotent binary operation m, denoted x∧y. Put x≤y when x∧y=x. The relation is reflexive (idempotence), antisymmetric (commutativity), and transitive (associativity). Moreover x∧y is the greatest lower bound of x,y: it is a lower bound by the meet laws, and if t≤x,y then t∧(x∧y)=(t∧x)∧y=t. Thus t≤x∧y iff t≤x and t≤y. No joins are assumed.

For a point e∈X and a total binary operation ·, the printed semibrace conditions are:

(S1) x·(y∧z)=(x·y)∧(x·z);
(S2) e·x=x;
(S3) (x∧y)·z=(x·y)·(x·z);
(S4) x·e=e.

The additional L-algebra conditions are:

(L1) e·x=x and x·x=x·e=e;
(L2) (x·y)·(x·z)=(y·x)·(y·z);
(L3) [x·y=e and y·x=e] iff x=y.

The result to prove is: (i) a printed semibrace exists on exactly the nonempty meet-semilattices, with every prescribed e allowed; (ii) a joint structure exists exactly on those with a greatest element, and in every joint structure e is greatest and x≤y iff x·y=e. If the additional convention e∧x=x is imposed, both existence answers require a greatest element.

## First existence question

For a given e in nonempty X define x·y=y. For S1 the two sides are y∧z; S2 is immediate; for S3 the two sides are z; S4 is immediate. This works for every e and needs no maximum, minimum, or comparability. On the empty set there is no possible e. On a singleton the operation also satisfies all L axioms; otherwise its diagonal x·x=x prevents it from being the joint construction. Selecting one element of one nonempty set requires no axiom of choice for a family of sets.

## Necessity by local substitutions

Assume the printed semibrace and L-algebra axioms. This derivation does not use translation injectivity or L2. Fix x,y, put m=x∧y and p=x·y.

If m=x, evaluate S3 at z=y. It gives p=p·p=e by L1.

Conversely suppose p=e. S1, S3, and L1 give

x·m = (x·x)∧(x·y) = e∧e = e,

m·x = (x·y)·(x·x) = e·e = e.

L3 applied to x,m gives x=m. We have therefore proved, without any preexisting meet identity,

x∧y=x iff x·y=e.

Now S4 gives x·e=e for every x, hence x∧e=x for every x. Thus e is greatest. The displayed equivalence proves equality of the meet and logical orders. The point is unique since a greatest element is unique. Even if one initially permits different points for the two structures, S4 at the semibrace point makes its diagonal equal to that point, whereas the L diagonal law makes it equal to the L point; therefore they agree.

For comparison, the candidate's different translation proof is also valid. If T_a=T_b, diagonal evaluations at a,b yield b·a=a·b=e, hence a=b by L3. S3 with y=e then gives T_(x∧e)=T_x, proving the same conclusion. This is injectivity of the assignment a↦T_a, not injectivity of each individual map T_a.

## Sufficiency by principal-ideal maps

Assume e is greatest. Define

F_x(y)=x·y=e if x≤y, and F_x(y)=x∧y otherwise.

The operation is total. Its only outputs are existing elements e or x∧y. The predicate x≤y is used in a classical case distinction; no ordering algorithm, enumeration, or well-ordering of X is assumed.

First F_e(y)=y: for y=e the output is e, and for y≠e one has e≰y and e∧y=y. Also F_x(x)=F_x(e)=e. If F_x(y)=e in the second branch, x∧y=e, so e≤x,y; since e is greatest, x=y=e, contradicting the branch. Consequently

F_x(y)=e iff x≤y.

This proves S2, S4, L1, and L3 by antisymmetry.

To check S1, consider the principal ideal D_x={u:u≤x}. The map M_x(y)=x∧y preserves binary meets, by associativity, commutativity, and idempotence. Define J_x:D_x→X by J_x(x)=e and J_x(u)=u for u<x. This map preserves binary meets. Indeed, if both arguments equal x, both images meet to e; if exactly one equals x and the other is u<x, both sides are u; if both are below x, their meet is below x and the map fixes both arguments and their meet. The inequality u∧v<x in the last case follows from u∧v≤u<x. This reasoning still holds when x=e, in which case J_e is the identity. Since F_x=J_x∘M_x, every F_x preserves binary meets. This is S1, including all mixed and incomparable branches.

The following absorption lemma supplies S3:

For a≤x, F_a(F_x(z))=F_a(z) for every z.

If x≤z, both sides equal e since F_x(z)=e, a≤z, and F_a(e)=e. If x≰z, put b=x∧z. Then F_x(z)=b. Since a≤x, a≤b iff a≤z. If this comparison holds, F_a(b)=F_a(z)=e. If it fails, F_a(b)=a∧b=a∧x∧z=a∧z=F_a(z). This proves the lemma in all branches, including a=x.

Set a=x∧y. If x≤y, then a=x and F_x(y)=e, so

F_(F_x(y))(F_x(z))=F_e(F_x(z))=F_x(z)=F_a(z).

If x≰y, then F_x(y)=a, and the absorption lemma gives the same equality. Written without map notation, this is exactly

(x·y)·(x·z)=(x∧y)·z.

Finally commutativity of meet and S3 yield

(x·y)·(x·z)=(x∧y)·z=(y∧x)·z=(y·x)·(y·z).

This is L2. Every joint axiom has now been verified. No appeal to finite checks occurs in the proof.

## Convention with a meet identity

The extra equation e∧x=x is equivalent to e being greatest. Its necessity is independent of multiplication. If such a greatest point exists, projection solves the first existence question and the F construction solves the joint question. Therefore both answers under this convention are exactly the meet-semilattices with a greatest element. The empty set still fails the point requirement.

## Boundary and adversarial examples

An infinite example without a least element is the chain of nonpositive integers, with meet minimum and greatest point 0. The formula applies directly; no infimum of all elements is used.

An infinite example without all joins has elements 0,a,b,e,c_n (n≥0), ordered by 0<a,b<c_n<e, a incomparable with b, and c_(n+1)<c_n. Its meets are determined by comparability, a∧b=0, and c_m∧c_n=c_max(m,n). Common upper bounds of a,b are e and the c_n. No such bound is least because every c_n has the smaller upper bound c_(n+1). Thus a∨b does not exist, and the theorem still applies. The candidate's example is sound.

M3 and N5 satisfy the construction. For instance in M3 with three distinct atoms a,b,c, meet a∧(b∨c)=a differs from (a∧b)∨(a∧c)=0, so distributivity cannot be a hidden condition of the proof. Explicit finite checks are supplementary.

The separation condition is essential to the necessity statement. On V={0,a,b} with 0 below incomparable a,b, choose e=a and the multiplication rows, in order 0,a,b,

    a a a
    0 a b
    a a a

The meet table is

    0 0 0
    0 a 0
    0 0 b

Every row except the e row is constant e, and the e row is identity, so S1 holds. The table directly satisfies S2-S4, all diagonal laws, and L2; verify_algebra.py checks every triple. Yet V has no greatest element. L3 fails at 0,b, whose mutual products are e. This control pinpoints the indispensable use of separation.

For the different Problem 10 formula G_x(y)=e if x≤y and y otherwise, use the four-element Boolean lattice {0,a,b,e} with a,b incomparable. Then G_a(a∧b)=G_a(0)=0, but G_a(a)∧G_a(b)=e∧b=b. Thus meet preservation fails. The source poses this as an L-algebra trivialization; failure of the additional semibrace identity does not refute its L-algebra assertion. Replacing its second branch by x∧y is a mathematical change, correctly explicit in the candidate.

Products of joint examples satisfy the equations componentwise, and mutual products equal to the product point imply equality in every coordinate by L3. This works for arbitrary products of specified pointed examples without selecting new coordinates. The constructed operation need not equal the componentwise product operation: in the product of two two-element chains, x=(0,1),y=(1,0) have componentwise product (1,0), whereas the present formula gives (0,0). The candidate's nonidentity qualification is correct.

## Exact remaining gap

There is no remaining mathematical gap in the displayed existence theorem under either inspected convention. These arguments do not classify every compatible operation, establish self-similarity, prove a claim about group braces, or establish historical novelty. Those are distinct questions and are not transferred into this theorem.
