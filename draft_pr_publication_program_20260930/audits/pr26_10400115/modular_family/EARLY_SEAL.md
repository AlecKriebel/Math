# Independent modular-family seal

This document was written before reading any historical review, candidate proof,
OBSTRUCTION, original verification program, sibling audit, root audit narrative,
or original source_record/readiness contents. Directory names and the assignment
are the only original-packet information used so far. The seal timestamp and
SHA-256 are recorded separately in `early_seal_receipt.json`.

## Literal target and success criteria

The primary source is T. Ohtsuki (editor), *Problems on invariants of knots and
3-manifolds*, Geometry & Topology Monographs 4 (2002), printed p. 470, physical
PDF page 98 (zero-based 97):
https://msp.org/gtm/2002/04/gtm-2002-04-024p.pdf . The complete relevant page was
extracted and visually inspected. Problem 6.7, attributed to S. J. Bigelow,
asks whether B_n admits a faithful finite-dimensional matrix representation over
the algebraic closure of Q. The adjacent remark states existence of a faithful
B_3 representation in GL(2,Z), then describes n >= 4 as open at the source's
time. It also discusses the Laurent-polynomial representation and the unknown
faithfulness of algebraic parameter specialization. Those historical statements
are not evidence of present worldwide openness.

Criteria fixed now:

1. Prove the twisted B_3 representation faithful for every braid, not just a
   bounded list. Establish the projective quotient injectivity without assuming
   faithfulness of the proposed twist.
2. Check B_1 and B_2 and explicitly delimit any conclusion to n <= 3.
3. Treat the literal GL(2,Z) remark as a separate falsifiable assertion. If it is
   false, supply a proof covering reducible and irreducible representations.
4. Distinguish GL(2,Z), whose inverses must be integral, from GL(2,Q), and make no
   claim excluding higher integral dimensions.
5. Use exact rational calculations, negative words, center powers, quotient
   normal forms, projective signs, exponent ambiguity, and deliberate defective
   twists as implementation controls. Finite search can check an implementation
   but cannot establish universal injectivity.
6. Do not promote a low-strand result to a solution of the all-n source question.
   Newness of a derivation is not a novelty claim about the mathematics.

## Independent derivation

Write x = sigma_1, y = sigma_2 and B_3 = <x,y | xyx=yxy>. Put A=xyx and B=xy.
Then A^2=B^3. Conversely, in H=<A,B | A^2=B^3>, set x=B^-1 A and
y=A^-1 B^2. Direct multiplication gives xy=B, xyx=A, and
yxy=A^-1 B^3=A. These constructions are inverse on all generators. Thus
B_3 is H; no representation's injectivity was used.

Set z=A^2=B^3=(xy)^3. It commutes with A and B, hence is central. The
homomorphism e:B_3 -> Z sending x and y to 1 is well-defined because both
sides of the defining relation have exponent 3. Since e(z)=6, z has infinite
order. Factoring by <z> gives exactly <a,b | a^2=b^3=1>=C_2*C_3, because the
normal closure of the central z is already its cyclic subgroup. Hence the
quotient's kernel is exactly <z>, not some unidentified normal subgroup.

Reduced free-product words show the quotient has trivial center. Indeed, a
word commuting with a must lie in <a>: remove a terminal a from the word, if
present; otherwise conjugating a by a nonempty word ending in the b-factor
produces a reduced word of length greater than one. The remaining element a
does not commute with b. Therefore Z(B_3)=<z>.

Let U=[[1,1],[0,1]], V=[[1,0],[-1,1]]. Matrix multiplication gives
UVU=VUV=S=[[0,1],[-1,0]] and UV=R=[[0,1],[-1,1]], with S^2=R^3=-I.
There is consequently a homomorphism phi:B_3 -> SL(2,Z) and a quotient
homomorphism C_2*C_3 -> PSL(2,Z), a -> [S], b -> [R].

Here is an independent injectivity proof for that quotient map. On the real
projective line, S(t)=-1/t and R(t)=1/(1-t). For X_a=(-infinity,0) and
X_b=(0,infinity), S(X_b) is contained in X_a, while R(X_a)=(0,1) and
R^2(X_a)=(1,infinity) are contained in X_b. Both factor generators have the
stated exact projective orders. Every odd-length reduced word beginning and
ending in the same factor carries the other factor's domain into its own,
and so cannot be the identity. For an even-length reduced word, cyclically
rotate it to begin in the a-factor and end in b^r, r=1 or 2. Conjugate by b^t
with t in {1,2} different from r. The resulting reduced word begins and ends
in the b-factor, so the preceding domain argument applies. Single-factor
words also act nontrivially. Thus no nonempty reduced word acts trivially.
This is a universal proof, not a sampled-word inference.

The image is all of PSL(2,Z). Since R^-1 S=U, the image contains [S] and [U].
Left multiplication by U^m and S performs the Euclidean algorithm on the
first column (a,c) of any determinant-one integer matrix. Since gcd(a,c)=1,
these operations reduce it to (+/-1,0), leaving an upper unipotent matrix up
to sign; -I=S^2 is also generated in SL(2,Z). Therefore U,S generate
SL(2,Z), and the quotient is isomorphic to PSL(2,Z). This generation proof
is logically separate from injectivity. It follows that
ker(B_3 -> PSL(2,Z))=<z>, phi(z)=-I, and ker(phi)=<z^2>.

Define rho_c(w)=c^{e(w)} phi(w) for nonzero rational c. Equivalently its
generator images are cU and cV. This is well-defined for positive and
negative words, with rho_c(x^-1)=c^-1 U^-1 and similarly for y. In particular,
rho_2 has matrices in GL(2,Q), determinant det(rho_2(w))=4^{e(w)}, and
rho_2(z)=-64I. If rho_2(w)=I, its projective class is trivial, so w=z^k.
Then (-64)^k=1 implies k=0, including negative k. Equivalently determinants
first force e(w)=0, and the quotient-kernel result forces e(w)=6k=0.
Either proof establishes injectivity for every braid without assuming B_3
torsion-freeness. More generally rho_c is faithful exactly when -c^6 has
infinite multiplicative order. For rational c this means c not in {1,-1}.

Projective torsion is not a counterexample: a and b have finite order in the
quotient, while their lifts satisfy A^2=B^3=z. A finite-order free-product
element is conjugate into a factor (cyclically reduce; a reduced length >=2
word has powers of strictly increasing length). If w were torsion in B_3,
e(w)=0. Its nontrivial finite-order quotient would have exponent modulo 6
equal to 3, 2, or 4, a contradiction. A trivial quotient leaves w=z^k, also
forcing k=0. This provides a further check on the lifting argument.

B_1 is trivial and embeds in GL(1,Q). B_2=<x> is infinite cyclic and the
map x -> [2] embeds it in GL(1,Q). Together with rho_2 these give the
source's requested algebraic-coefficient existence only for n <= 3. Nothing
in this derivation constructs or rules out a faithful representation for
any n >= 4.

## Falsification of the literal integral assertion

For a nonscalar C in M_2(Q), choose v for which v,Cv are independent. Such
a vector exists, since an operator preserving every one-dimensional subspace
is scalar. A commuting operator T is determined by T(v)=a v+b Cv, and
commutation forces T(Cv)=C T(v). Therefore T=aI+bC, and the entire
centralizer of C is the commutative algebra Q[C]. No diagonalizability,
irreducibility, eigenvalue splitting, or Schur lemma is needed.

Suppose f:B_3 -> GL(2,Z) were injective. Since z is infinite-order central,
f(z) must have infinite order. If f(z) is scalar, integral entries and
determinant +/-1 force f(z)=+/-I, a contradiction. If f(z) is nonscalar,
both f(x) and f(y) lie in its commutative rational centralizer, so they
commute. But B_3 is nonabelian, as U and V do not commute. This also
contradicts injectivity. Hence B_3 does not embed in GL(2,Z).

The unimodular determinant condition is essential here. rho_2(x) and
rho_2(y) have integer entries but determinant 4; their inverse entries have
denominators, so they are not elements of GL(2,Z). Scalar matrices in
GL(2,Q) can have infinite order; -64I is precisely the central image which
permits our faithful rational representation. In dimensions greater than
two the centralizer of a nonscalar matrix need not be commutative, so this
proof does not exclude integral embeddings in higher degree. The argument
is over Q and characteristic zero. Reduction over a finite field cannot
give a faithful representation of infinite B_3 in its finite GL(2), and
the c=2 twist is not even invertible in characteristic 2.

## Prespecified adversarial controls

The forthcoming program will independently reduce C_2*C_3 words and compare
projective actions, and track the integer exponent alongside them. It will
check central powers on both sides of zero, phi(z)=-I versus phi(z^2)=I,
the commutator with exponent zero but nontrivial projective image, words
differing by z with identical projective images but different exponents,
and the relation's lifts. Defective twists c=1,-1 must retain a kernel,
whereas c=2,-2,1/2 must distinguish center powers. Unequal generator scales
2U and 3V must fail the braid relation. Exact centralizer controls will
include nonsplit, Jordan, and determinant-minus-one matrices. The program
will label its bounded enumeration as a consistency check only.

## Sources read independently before seal

- Ohtsuki's complete printed p. 470 / PDF 98, as above.
- J. S. Milne, *Modular Functions and Modular Forms*, version 1.31 (2017),
  Theorem 2.12 and Remark 2.14, printed pp. 32-33:
  https://www.jmilne.org/math/CourseNotes/MF.pdf . This supplies a primary
  author's exposition of modular generators and their full presentation.
- I. Tuba and H. Wenzl, *Representations of the braid group B_3 and of
  SL(2,Z)*, arXiv:math/9912013v1, section 1.1 and the introduction, pp. 1-2:
  https://arxiv.org/pdf/math/9912013 . This supplies the braid presentation,
  infinite central generator, and modular quotient. The independent matrix
  multiplication above fixes our multiplication convention explicitly.

Source URLs, download times, and full-file hashes are in
`sources/source_receipts_preseal.json`. PDF renders were inspected locally.

## Provisional verdict at seal

The universal low-strand rational construction is valid. The printed
GL(2,Z) assertion is false. The all-n question is not resolved by the
construction. Historical packet comparison, exact artifact provenance,
new implementation controls, and isolated replay remain outstanding.
Best-guess completion of this audit family's assignment: 40%. Best-guess
completion of the all-n research goal from this work: 5%, explicitly
heuristic and not a proportion of cases proved.
