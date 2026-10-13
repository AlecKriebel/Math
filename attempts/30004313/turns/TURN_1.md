# Turn 1: classify retracted right-zero additions and test the scope boundaries

**Scoped partial, unreviewed. Original Question 2 remains unresolved.** One substantive author turn has been used. The source and later papers are credited; no novelty is asserted. Expanding the Yang–Baxter equation into its three coordinates is a test, not itself the requested structural characterization.

## 1. Exact ambient definition

A generalized left semi-brace has associative operations + and multiplication (written by juxtaposition here), with multiplication completely regular. Its inverse a^- is the unique commuting group inverse satisfying aa^-a=a and a^-aa^-=a^-. Write a^0=aa^-=a^-a. The compatibility law is

    a(b+c)=ab+a(a^-+c).

The exact source map is

    r(a,b)=(a(a^-+b),(a^-+b)^-b).

Solutions need not be bijective or nondegenerate. A completely regular semigroup need not be an inverse semigroup or a Clifford semigroup. In particular, neither (ab)^-=b^-a^- nor a global identity is available without proof. The group-based semi-brace criterion in the literature cannot simply be inserted into this ambient definition.

## 2. Complete classification in a natural non-group subclass

Let (L,∧) be any nonempty meet-semilattice, not necessarily finite or bounded. Let f:L→L, define multiplication by meet, and define

    a+b=f(b).                                             (2.1)

### Generalized semi-brace criterion

These operations give a generalized left semi-brace if and only if f²=f and its image I=f(L) is downward closed in L.

Indeed, associativity of (2.1) is exactly f(c)=f(f(c)). The multiplicative inverse of each element is itself. The brace identity reduces to

    a∧f(c)=f(a∧f(c))                                     (2.2)

for all a,c. For an idempotent map, its fixed points are exactly its image. Equation (2.2) therefore says that every element below a member of I is again in I: if x≤f(c), take a=x; conversely a∧f(c)≤f(c). This proves the criterion.

### Yang–Baxter criterion

Assume these generalized semi-brace conditions. Then the associated map is

    r(a,b)=(a∧f(b), b∧f(b)).                              (2.3)

**Theorem.** Map (2.3) satisfies the braid Yang–Baxter equation if and only if f is order-preserving and f(x)≤x for every x.

Proof. Write r_12=r×id and r_23=id×r. Direct composition, using (2.2) to remove f from elements of I, gives

    r_12 r_23 r_12(a,b,c)
       =(a∧b∧f(b)∧f(c), b∧f(b)∧f(c), c∧f(c)),            (2.4)
    r_23 r_12 r_23(a,b,c)
       =(a∧b∧f(c),       b∧c∧f(c),    c∧f(c)).             (2.5)

Here the composition order convention is immaterial because both three-letter words are palindromes; the calculations apply the rightmost factor first.

Equality of first coordinates for every a is equivalent to

    b∧f(c)≤f(b)   for all b,c:                            (2.6)

necessity follows by choosing a=b∧f(c), and sufficiency by meeting both sides with a. Equality of middle coordinates, with b=f(c), forces f(c)≤c, since f(f(c))=f(c). If x≤y, then f(x)≤x≤y and (2.6) with b=y,c=x implies f(x)=y∧f(x)≤f(y). Thus f is order-preserving.

Conversely assume f is order-preserving and deflationary. The element b∧f(c) belongs to I by (2.2), so

    b∧f(c)=f(b∧f(c))≤f(b).

This proves (2.6), hence equality of the first coordinates. The middle coordinate on the left is then b∧f(c), and the one on the right is also b∧f(c) because f(c)≤c. Third coordinates already agree. This proves the theorem for all L.

One equivalent description is useful. Under the theorem's conditions, f(x) is the greatest member of I below x: any i∈I with i≤x satisfies i=f(i)≤f(x). Thus the classification asks for a downward-closed image admitting these greatest elements, not an arbitrary retraction onto that image.

### Bounded case

If L has a greatest element 1, the theorem is equivalent to the existence of e∈L with

    f(x)=x∧e,   e=f(1).                                  (2.7)

To prove necessity, monotonicity and deflationarity give f(x)≤x∧e. The latter lies in I because e∈I and I is downward closed, and is below x; the greatest-element characterization gives x∧e≤f(x). Conversely (2.7) is an idempotent monotone deflationary map with image the principal ideal below e. The associated solution is explicitly

    r(a,b)=(a∧b∧e,b∧e),

and both braid words send (a,b,c) to (a∧b∧c∧e,b∧c∧e,c∧e).

This is a complete all-size result within (2.1), not a characterization of arbitrary associative additions or arbitrary completely regular multiplication.

## 3. Two exact failures that prevent overgeneralization

### A middle-coordinate obstruction

Let L={0,p,q}, with 0 below the two incomparable atoms p,q, and p∧q=0. Set f(0)=0, f(p)=p, f(q)=p. Its image {0,p} is downward closed and f²=f, so (2.1) is a valid generalized left semi-brace. The map is order-preserving but f(q) is not below q.

For every b,c in this example, b∧f(c)≤f(b), so the first braid coordinate agrees identically; the third coordinate in (2.4)–(2.5) always agrees. Nevertheless, at (a,b,c)=(0,p,q), the two braid outputs are

    (0,p,0) and (0,0,0).

Thus checking the two outside coordinates does not suffice even for a three-element multiplicative semilattice. The failure comes entirely from the middle coordinate. This is a counterexample to that shortcut, not to the source's classification question.

### Monotonicity is also necessary

On the chain 0<p<1, take f(0)=0, f(p)=p, f(1)=0. Again the image is downward closed and f is idempotent, so this is a generalized left semi-brace. It is deflationary but not order-preserving. At (p,1,p), (2.4) and (2.5) have distinct first coordinates, 0 and p. Thus deflationarity alone does not repair the problem.

## 4. Product preservation is not necessary in the unrestricted target

Let multiplication be meet on {0,1} and addition be constantly 0. This is the case f≡0 above. The associated r is the constant pair (0,0), hence is a Yang–Baxter solution. At (1,1), the product of the two output coordinates is 0 whereas the input product is 1.

Consequently the common brace factorization identity

    lambda_a(b) rho_b(a)=ab

is not necessary for the generalized target. A strategy imposing it from the outset loses legitimate solutions. Likewise the group-style homomorphism and antihomomorphism identities for lambda and rho are not automatic in the full class. The finite controls include two-element examples, but no universal conclusion is based on those samples alone.

## 5. Projection-addition normalization checks

For any completely regular multiplicative semigroup, if addition is right zero (a+b=b), the defining formula gives

    r_R(a,b)=(ab,b^0).

The two braid words give, respectively,

    (abc,(b^0c)^0,c^0),   (abc,(bc)^0 c^0,c^0).

Since (bc)c^0=bc, left multiplication by (bc)^- gives (bc)^0 c^0=(bc)^0. Thus r_R is a solution exactly when

    (bc)^0=(b^0c)^0  for all b,c,

the right-cryptogroup condition announced in the original contribution. Also r_R²=r_R.

For left-zero addition (a+b=a), the defining formula instead gives

    r_L(a,b)=(a^0,ab).

Its braid outputs are (a^0,a^0(ab)^0,abc) and (a^0,(ab^0)^0,abc). The identity a^0ab=ab, multiplied on the right by (ab)^-, gives a^0(ab)^0=(ab)^0. Hence the corresponding condition is

    (ab)^0=(ab^0)^0  for all a,b,

and r_L²=r_L. These direct computations keep the two conventions separate. The later paper's paragraph about right-zero addition also displays the pair (a^0,ab), which is the left-zero substitution; our calculations use the defining map throughout rather than propagating that mismatch. The source's right-zero criterion itself agrees with the direct computation.

## 6. Finite diagnostics and remaining gap

The standalone finite_catalogue.py enumerates all labeled binary operations on at most three elements, filters exact associativity, commuting group-inverse and brace identities, and evaluates both braid words. There are22 labeled generalized left semi-braces of order2, all passing the braid test, and622 of order3, of which508 pass and114 fail. These are labeled-table counts, not isomorphism counts or an all-size structure theorem. The separate verify_turn1.py checks the written subclass criteria, explicit braid formulas and counterexamples using exact finite operations.

The original classification still requires structural conditions for general addition and completely regular multiplication. The present class permits degenerate non-product-preserving maps and exposes a genuinely independent middle-coordinate obstruction. No reduction from all generalized left semi-braces to this subclass or to a strong semilattice of ordinary semi-braces has been proved. One of five substantive turns is complete; further routes must address those remaining possibilities rather than restate the three coordinate equations.
