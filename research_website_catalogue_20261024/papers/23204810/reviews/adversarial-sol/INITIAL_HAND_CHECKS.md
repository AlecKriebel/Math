# Algebraic falsification checks, by hand

PRIVATE INITIAL. No source/support program, symbolic algebra package, imported
primary proof or scientific test was executed/read. Original author assertions
were necessarily visible before these checks. These calculations address local
algebra, generator counts, cancellations, duality and plateau boundaries.

## 1. A strict associated-graded example within the stated algebra class

Take any characteristic-zero k and A=k[x,y]/(x^2,y^5), with standard grading.
The monomial basis is 1,y,y^2,y^3,y^4,x,xy,xy^2,xy^3,xy^4. Thus dim A=10,
c=5, H_A=(1,2,2,2,2,1), h_p=2 and the LAST maximum is p=4.
Set f=x+y^2 and I=(f), which is nonhomogeneous. The products are

    yf=xy+y^3; y^2f=xy^2+y^4; y^3f=xy^3; y^4f=xy^4;
    xf=xy^2; xyf=xy^3; xy^2f=xy^4.

All further products vanish or lie in their span. Since y^2f-xf=y^4,
a basis of I is

    f, xy+y^3, xy^2, y^4, xy^3, xy^4.

These six vectors are independent by their distinct pivot monomials. A basis
of mI is the last five vectors in that list, so mu(I)=6-5=1 as required for
a nonzero principal ideal. Its lowest-degree initial ideal is

    J=(x,y^4), basis x,xy,xy^2,xy^3,y^4,xy^4.

Here mJ has basis xy,xy^2,xy^3,xy^4 and mu(J)=6-4=2. On the other hand
gr(mI) has those four monomials PLUS y^4, so

    mJ strictly contained in gr(mI), mu(I)=1<2=mu(J)=h_p.

Thus the often tempting equality gr(mI)=m(gr I) is false even for the exact
graded complete-intersection class. The manuscript uses the correct inclusion
and correct upper-bound direction. Using the filtration on mI induced from A
is essential; an unrelated m-adic filtration on the module would not give this
same identification. This is a genuine cancellation calculation, not a formal
copy of the manuscript's inequality.

## 2. Equal quotient Hilbert functions do not control ideal generator counts

Let B=k[x,y]/(x^4,y^4), I_1=(x^2,xy,y^3), I_2=(x^2,y^2). The quotient
B/I_1 has basis1,x,y,y^2, whereas B/I_2 has basis1,x,y,xy. Both have Hilbert
function(1,2,1). Nevertheless mu_B(I_1)=3: the two degree-two generators
x^2,xy are independent modulo mI_1, and y^3 is independent of their degree-three
multiples x^3,x^2y,xy^2. For I_2 the two degree-two generators are independent
and generate, so mu_B(I_2)=2. Both preimage ideals contain the full regular
sequence x^4,y^4. Thus even an EGH-style same-Hilbert-function transfer between
homogeneous ideals cannot be used to assert equal mu. The manuscript's proof
only transfers adjacent quotient dimensions for the ideal AV and uses shadow
growth; this stronger false inference is not needed.

## 3. Long plateau tests the last-maximum convention

Return to degrees(2,5), with monomial exponents0<=i<=1,0<=j<=4. Two symmetric
chains are

    (0,0),(0,1),(0,2),(0,3),(0,4),(1,4),
    (1,0),(1,1),(1,2),(1,3).

Their rank ranges are[0,5] and[1,4]. This gives H=(1,2,2,2,2,1) explicitly.
Both chains extend from rank3 to4, although3 lies above c/2=2.5. Consequently
the plateau matching step is valid there. At rank4 to5, V=A_4 is2-dimensional
but A_1 V=A_5 is1-dimensional. Matching without the condition h_j<=h_(j+1)
would be false. The proof's p=4 has c-p=1<=4; choosing the FIRST maximum p=1
would invalidate the later asserted comparison c-p<=p even though m^1 also
attains the same generator maximum. This distinguishes a theorem statement
from a proof step that specifically needs the last maximum.

For this A, m^4 has basis y^4,xy^3,xy^4 and m^5 has basis xy^4, so
mu(m^4)=3-1=2. For I=(xy^4), mI=0 and J=Ann(mI)=A. Then
mu(I)=mu(J)=1 and truncating J to m^4 increases mu to2; the bounds do not
presume equality at each step.

## 4. Truncation identity and annihilator direction

For a homogeneous ideal I in a STANDARD graded algebra, (mI)_d=A_1 I_(d-1).
Indeed A_u is spanned by products of u degree-one elements, and I is an ideal.
If alpha is its first nonzero degree and I'=direct sum_(d>=alpha+1) I_d,
all degree contributions to mu agree except alpha and alpha+1. The former
loses dim I_alpha; the latter gains dim A_1 I_alpha. Therefore

    mu(I')-mu(I)=dim A_1 I_alpha-dim I_alpha.

This justifies both the identity and why matching is applied before p. The
zero ideal needs a separate immediate case, rather than a nonexistent alpha.
For I=A, alpha=0 is legitimate; if p=0 no truncation is attempted.

Let lambda be projection onto the one-dimensional socle A_c, normalized by a
nonzero basis vector. Perfect graded pairings make (a,b)->lambda(ab) a perfect
pairing of ALL of A. For any ideal U, if lambda(aU)=0, then for u in U and
b in A, ub lies in U, so lambda((au)b)=0 for every b. Nondegeneracy gives
au=0. Thus U-perp=Ann(U) and dim Ann(U)=dim A-dim U, including U=0,A and
nonhomogeneous U. If J=Ann(mI), then for t in m, j in J, i in I,
(tj)i=j(ti)=0, hence mJ subset Ann(I). The resulting inequality is

    mu(J)=dim J-dim mJ >= dim Ann(mI)-dim Ann(I)
          =dim I-dim mI=mu(I).

It has the direction required for an upper bound after truncating J. For
0<=u<=c+1, degree gives m^(c-u+1) subset Ann(m^u). If a has a nonzero
component a_j with j<=c-u, pair a_j nontrivially with b in A_(c-j), which
lies in m^u. The socle projection of ab isolates a_j, so a is not in Ann(m^u).
This proves the reverse inclusion. The endpoints give Ann(A)=0=m^(c+1)
and Ann(0)=A=m^0, so neither endpoint requires a negative power of m.

## 5. Product-of-chains induction and subspace test

For a rectangle0<=i<=a,0<=j<=b with a<=b, chain r consists of vertical
points(r,0),...,(r,b-r), followed by(r+1,b-r),...,(a,b-r),0<=r<=a.
Its endpoint ranks are r and a+b-r. A point(i,j) belongs uniquely to chain
r=i if j<=b-i, and otherwise to r=b-j<i. These cases also show there is no
double counting at the corner, whose repeated notation is omitted once.
Thus the chains are saturated, disjoint, exhaustive and symmetric. For an
old symmetric chain with global start d and length c-2d, multiplying by a new
factor of length b gives new endpoint-rank sums2d+(c-2d)+b=c+b. Swapping the
two rectangle axes when necessary preserves rank.

Above half the total rank no symmetric chain can START. If equal adjacent
rank sizes occur there, no chain can END between them either. Hence every
chain meeting rank j extends whenever h_j<=h_(j+1), even after the middle.
Successors inject every subset of bounded exponent monomials into its shadow.

For a vector subspace W, echelonize with respect to a multiplicative monomial
order. A surviving variable multiple of a leading monomial remains the leading
monomial of that product: multiplying lower terms cannot overtake it, and
discarding pure-power-zero terms cannot remove the surviving top term. Distinct
shadow monomials supply independent pivot positions in B_1W. This avoids
assuming that a subspace is itself spanned by monomials or that a single linear
form supplies all injections. For q=0 there is only rank0; positive-rank W=0,
while h_0<=h_1 is false, so no spurious matching step is demanded.

## 6. Empty, all-linear, one-variable and linear-elimination boundaries

For n=0 the algebra is k, ideals are0 and A, and generator counts are0,1.
For n homogeneous independent linear forms in n variables the invertible
coefficient matrix gives A=k, with exactly the same answer. Excluding A from
the definition would instead make the field's maximum0; the stated inclusion
of A is essential. The empty product and m^0=A make the written witness correct.

For n=1 and degree d>=1, a nonzero homogeneous form is cx^d with c invertible.
Every ideal of k[x]/(x^d) is the image of a principal ideal containing(x^d),
hence is (x^r),0<=r<=d. Each nonzero ideal needs one generator. Its Hilbert
list consists of d ones, p=d-1, and m^p=(x^(d-1)) realizes1. For d=1 this
again means A. No assumption that arbitrary ideals have homogeneous chosen
generators was needed to classify these ideals.

If r linear members of a full regular sequence were linearly dependent, their
ideal together with the other n-r forms would be generated by fewer than n
elements but have height n, contradicting the height bound. A linear change
of variables eliminates r variables. No remaining defining form can become
zero: that would leave fewer than n-r equations for an Artinian quotient of
a polynomial ring in n-r variables. Nonzero homogeneous restrictions retain
their degrees. For instance degrees(1,2,5) can be represented by
(x+y,z^2,y^5), giving k[y,z]/(z^2,y^5), with H=(1,2,2,2,2,1), maximum2.
Its linear Hilbert factor is exactly1. Regularity, positive degree and standard
grading are substantive assumptions; merely writing n forms is insufficient.

## 7. Arbitrary field quantifier and a forbidden stronger conclusion

For a fixed homogeneous Q, finite generation permits a coefficient field k_0
finitely generated over Q, containing all chosen Q generators and g_i. Include
g_i among those generators to retain containment over k_0. Each regularity
injection descends along faithfully flat k/k_0. A finitely generated char0
field embeds into C: choose images of a finite transcendence basis that remain
algebraically independent, then embed the finite algebraic extension in the
algebraically closed field C. This does not assert an embedding of arbitrary
k (which can have greater cardinality than C). If the complex pure-power
counterpart is only homogeneous, take an initial ideal; its monomial powers
remain contained and its Hilbert function stays unchanged. The bounded
monomial exponent set defines the same quotient dimensions over any field.

The quantifier is 'for each Q choose k_0', not 'choose one finite k_0 handling
every ideal of A'. The final bound depends only on degrees, so that allowed
dependence does not obstruct a universal ideal bound. Alternatively extension
of a particular I preserves I/mI by flatness. Arbitrary extension-field ideals
need not descend, and that stronger assertion is unnecessary.

In characteristic2, B=k[x,y]/(x^2,y^2) has H=(1,2,1) and the same box/Sperner
argument applies, but every degree-one ell=alpha x+beta y has ell^2=0. Hence
ell^2:B_0->B_2 is never an isomorphism, despite both spaces being1-dimensional.
This explicit failure of strong Lefschetz shows why a matching/Sperner proof
cannot simply be relabeled as a Lefschetz proof. It is outside the theorem's
char0 scope and is not a counterexample to its stated conclusion.

## 8. What these checks do and do not establish

They verify the listed finite algebras, a strict filtration example, the
plateau mechanism and a conditional algebraic proof route. They do not prove
the central imported EGH theorem. A first-principles attempt to replace EGH
with merely H_A=H_B fails at the exact subspace-growth step: the Hilbert series
does not determine the rank of multiplication A_1 tensor V->A_(j+1). This
transfers the central burden to an unsupported assertion if used alone. No
such alternate unconditional route is promoted. Actual primary EGH proof and
the declared attribution interfaces remain for an explicitly resumed review.
