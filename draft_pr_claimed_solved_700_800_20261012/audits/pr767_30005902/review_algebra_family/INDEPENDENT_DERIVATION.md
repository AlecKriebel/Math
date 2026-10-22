# Independent algebra and cohomology reconstruction

This derivation was written after INITIAL_POSITION and before historical result or audit reports were read. The coefficient field is k=F3. The bar degrees below are cohomological degrees. The precise universal claim tested is vanishing for every nonquasitriangular Hopf algebra, without a characteristic-zero or degree-at-least-two restriction.

## Hopf structure and the obstruction to braiding

Use the monomial basis x^i y^j z^l, with 0<=i,j,l<3. Multiplication adds exponents and kills any exponent at least three. This defines a commutative 27-dimensional algebra. Expand the three coproduct generator images in this tensor basis. In characteristic three, cubing any sum of commuting terms is the sum of cubes, so the generator images satisfy all three quotient relations. The analogous check applies to S(x)=-x, S(y)=-y, S(z)=-z+xy.

Coassociativity on z has exactly six terms: z in any one of three tensor positions, and x tensor y tensor 1, x tensor 1 tensor y, 1 tensor x tensor y. Primitive x and y are immediate. The counit identities hold on generators. For z both antipode convolutions cancel because S(z)+z+S(x)y=0=z+S(z)+xS(y). Commutativity makes these convolution expressions algebra maps; hence generator checks suffice. S squared fixes x,y,z. These are analytic checks; the independent script also checks full basis inputs, not merely these generators.

The two basis tensors x tensor y and y tensor x differ, so Delta(z) differs from its flip. Every element of H tensor H is central. Consequently any invertible R satisfying the quasitriangular intertwining identity would force Delta=Delta^op, a contradiction. This rules out every R, not merely R=1. For the ordinary coproduct tensor category of H-modules, braidings correspond to such R matrices: evaluating a natural braiding on the regular module at 1 tensor 1 and using naturality reconstructs R, and module linearity imposes the intertwining identity. The regular module is finite dimensional here, so restricting to finite modules does not evade this obstruction.

## Scalar Ext in degree one

Write I=ker(epsilon). A scalar 1-cocycle satisfies f(ab)=epsilon(a)f(b)+f(a)epsilon(b). Setting a=b=1 gives f(1)=0. The remaining condition is exactly f(I^2)=0. Since I has dimension 26, and I^2 is spanned by the 23 monomials of total degree at least two, Ext_H^1(k,k) is three dimensional, with coefficient functionals fx,fy,fz as basis. The unnormalized differential has rank 24 because its domain has dimension 27; this includes the constraint f(1)=0. It is not the dimension of I^2.

The degree-zero scalar differential is epsilon(a)c-c epsilon(a)=0, so B^1=0. In particular fz(z)=1 proves a nonzero cohomology class. No Hochschild quotient or nonzero cochain shortcut is needed for this statement.

## Independent dual-algebra mechanism and orientation

The dual H* has convolution product (f*g)(b)=sum f(b1)g(b2). Augmentation derivations are its primitive elements. Direct expansion of Delta on every basis monomial, independently of differential-operator formulas, gives fx*fy-fy*fx=fz. This is the tangent Lie algebra of the noncommutative coproduct law. It predicts nonvanishing, but it alone does not identify the monoidal Ext bracket.

For right translation Rf(b)=sum f(b1)b2, coassociativity gives Rf Rg=R_(g*f). Thus right translation is an anti-representation of this convolution algebra, and [Rx,Ry]=-Rz. For left translation Lf(b)=sum b1 f(b2), composition has the other order, giving [Lx,Ly]=+Lz. The script checks both operators on all 27 basis vectors. Interchanging these conventions silently would give the wrong sign.

## The source bracket comparison, with hypotheses checked

The primary OWR contribution defines its cohomology as Ext of the unit, graded by nonnegative cohomological degree, over a field. Its closing paragraph explicitly links the monoidal bracket to Hochschild restriction through tensor induction for bijective antipode. See [OWR](https://ems.press/content/serial-article-files/49480), contribution pp.1114-1117, fully inspected including the boundary with the next contribution. That next contribution's characteristic-zero convention is outside Witherspoon's contribution.

The required comparison is [Karadag-Witherspoon](https://people.tamu.edu/~sjw/pub/KW13.pdf), Sections 2-4, especially Corollary 3.5 and Theorem 4.1. Its standing hypotheses are a field and bijective antipode; the homotopy construction uses a power flat projective resolution. Here S squared is identity. The bar resolution is power flat: tensoring over a field is exact, and a Hopf-module tensor product of projectives is projective. For the latter assertion, the diagonal module H tensor V is isomorphic to a free H module by h tensor v -> sum h1 tensor h2 v, with inverse h tensor v -> sum h1 tensor S(h2)v. Tensor powers of free resolutions, and their direct summands, therefore retain projectivity. Tensor induction is exact and preserves projectives under the paper's Section 2 lemmas. This is the specific comparison, rather than an assumption that arbitrary exact functors preserve projectives.

To fix its actual bar orientation, use [Karadag](https://arxiv.org/pdf/2010.07505), Section 5, Lemma 5.1: inducing through a -> sum a1 tensor S(a2) gives the inverse bar comparison

psi1(a tensor b tensor c)=sum (a tensor b2 c) tensor_H (1 tensor b1).

A scalar f induces the map (a tensor c) tensor_H (1 tensor b) -> a f(b)c. Composing with psi1 gives exactly a Rf(b)c. The degree-one map is therefore right translation, not the opposite one. The alternative map in [Farinati-Solotar](https://arxiv.org/pdf/math/0207243), Theorems 1.5 and 2.1, uses left translation and confirms the other orientation; it is not used to equate the two signed brackets. No characteristic-zero hypothesis from a truncated-polynomial example in an earlier section of Karadag is imported into Section 5.

## Nonzero cohomology bracket

The right-translation values on x,y,z are Rx=(1,0,y), Ry=(0,1,0), Rz=(0,0,1). All are derivations of the cubic quotient, since 3=0. Thus Rx=partial_x+y partial_z, Ry=partial_y, Rz=partial_z. Their commutator is -Rz. In Hochschild degree one the Gerstenhaber bracket is this ordinary commutator. Its value is still inside the explicit embedded scalar space. Also epsilon Rf=f; applying epsilon to an inner derivation is zero, giving an independent degree-one injection check. The comparison above therefore implies

    [[fx],[fy]]=-[fz] != 0 in Ext_H^1(k,k).

The scalar output evaluates to 2 at z in F3 and has zero scalar bar differential. Since B^1=0 it cannot become zero in cohomology. This proves the counterexample for the source's unrestricted question. The same argument survives extension to every field of characteristic three, including an algebraic closure.

## Falsifiable checks and limits

`verify_algebra.py` reconstructs structure constants using only the standard library. It computes the exact 729-by-27 scalar differential rank, all basis Hopf checks, six translation derivation checks, both signs, and the dual primitive commutator. Six negative controls expose false cocommutativity/R=1, an antipode missing xy, wrong orientation sign, a false constant coefficient cocycle, invalid characteristic-five cubic relations, and a malformed cross term x tensor y^2 violating coassociativity. The analytic centrality argument, not the R=1 control alone, excludes all quasitriangular structures.

The source comparison is a separately inspected mathematical theorem, not certified by finite computation. This is not a full Hochschild-cohomology counterexample substituted for scalar Ext, and no Gerstenhaber-Schack or Drinfeld-double cohomology is involved. The calculation gives no characteristic-zero result and does not settle a separately restricted question requiring both input degrees at least two. It does not certify novelty, priority, expert review, or formal proof-assistant verification.
