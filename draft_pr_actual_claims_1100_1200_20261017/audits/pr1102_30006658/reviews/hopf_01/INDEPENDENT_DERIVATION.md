# Independent algebra derivation, before reading earlier audits

Recorded: 2026-10-17T16:27:50Z (09:27:50 America/Los_Angeles).
Reviewer scope: PR #1102, `MATHEMATICAL_REPORT.md`, Lemma 1 and the
algebraic step of Proposition 3. No earlier `MATHEMATICAL_AUDIT.md`,
`ACCEPTANCE.json`, or other review was read before this derivation.
Best-guess completion for this assigned algebra audit: 75%.

## Ordinary finite-ideal theorem

Let B be a Hopf algebra over a field, with an arbitrary antipode S (possibly
nonbijective). Let I be a finite-dimensional nonzero right ideal. Define
J to be the span of all first legs of coproducts of elements of I, equivalently
J = span{(id tensor f) Delta(i) : i in I, f in B*}.

* J is finite-dimensional: finitely many coproduct expansions suffice for a
  basis of I, and every slice lies in the span of their first factors.
* I is contained in J, by applying the counit to the second factor.
* Delta(J) is contained in J tensor B. Indeed, Delta(i) belongs to J tensor B
  (expand each coproduct with linearly independent second factors and slice
  by dual functionals). Coassociativity and slicing the third factor give
  the assertion for every generator of J.
* J is a right ideal. For each i,b,f, use the iterated coproduct of b to get
  sum i_1 b_1 f(i_2 b_2 S(b_3)) = sum i_1 b f(i_2).
  The left side is a sum of slices of Delta(i b_1), using the functionals
  z -> f(z S(b_2)); each i b_1 belongs to I. The antipode identity used is
  sum b_1 tensor b_2 S(b_3) = b tensor 1. It does not use S inverse.

There is an elementary completion of the proof that also checks the cited
Hopf-module step. A nonzero right coideal J has epsilon(J) nonzero: if
epsilon vanishes on J, applying epsilon tensor id to Delta(j) proves j=0.
Choose j in J with epsilon(j) nonzero. Because J is a right ideal and
Delta(j) lies in J tensor B, sum j_1 S(j_2) = epsilon(j) 1 belongs to J.
Thus 1 belongs to J and J=B. Consequently B is finite-dimensional.
This avoids importing any bijectivity assumption through a variant of the
fundamental theorem of Hopf modules.

For a left ideal, B^(op,cop) has both product and coproduct reversed and
the SAME antipode S. Its antipode identities are precisely the two original
antipode identities with the factors reversed together. A left B-ideal
becomes a right B^(op,cop)-ideal. Reversing only product or only coproduct
would generally require an inverse antipode; the report reverses BOTH.

## Grading and bosonization

For characteristic 2 the Koszul signs equal 1, so forgetting the grading
really gives an ordinary Hopf algebra. For other characteristics, reduce
the integer grading modulo 2 and let g act by parity. On B=H#k[C2], the
report uses

  (h#g^i)(a#g^j) = (-1)^(i|a|) ha#g^(i+j),
  Delta(h#g^i) = sum (h_1#g^(|h_2|+i)) tensor (h_2#g^i),
  S_B(h#g^i) = (1#g^(i+|h|))(S_H(h)#1).

The products are associative because the parity action is by algebra
automorphisms. Coassociativity follows by comparing the g exponents in
three coproduct factors: they are respectively |h_2|+|h_3|+i,
|h_3|+i, and i on either side.

Here is the potentially dangerous bialgebra sign calculation. Write
r=|h_1|, s=|h_2|, u=|a_1|, v=|a_2|. Applying Delta to the product has
sign i(u+v)+su, by the super bialgebra identity. Multiplying the two
coproducts in the ORDINARY tensor-product algebra has sign
(s+i)u+iv, which is the same expression. Its group exponents also agree:
s+v+i+j in the first factor and i+j in the second.

For the left antipode identity, set t=|h|=r+s. On the term
(h_1#g^(s+i)) tensor (h_2#g^i), applying S_B to the first factor gives
(1#g^(t+i))(S_H(h_1)#1). The total product is
(1#g^(t+i))(sum S_H(h_1)h_2#g^i). The sum is epsilon(h)1; the counit is
zero unless t=0. Hence it equals epsilon(h)(1#1). For the other antipode
identity the middle g factors cancel directly, leaving
sum h_1 S_H(h_2)#1. No inverse of S_H occurs.

If I is a graded right ideal, (x#g^i)(a#g^j) has coefficient
(-1)^(i|a|)xa in I. If I is a graded left ideal, the reversed product has
coefficient (-1)^(i|x|)ax in I. The parity homogeneity needed to span the
left product is available because I is graded. Thus I#k[C2] is a
one-sided ideal on the same side, finite-dimensional and nonzero, whereas
the bosonization is infinite-dimensional whenever H is. Lemma 1 follows.

## Proposition 3 image ideal

For left A-modules, an A-linear degree-zero derived map P->A induces a
degree-zero map of graded left H_*(A)-modules. Its image I is a graded
left ideal: for homogeneous a in H_*(A) and image z=f_*(y),
a z = f_*(a y). The equality is the module-action naturality square;
it makes no commutativity, cocommutativity, or chain-level Hopf assumption.
Finite TOTAL dimension of H_*(P) gives finite total dimension of I.
The finiteness of each separate degree alone would not suffice, but the
report explicitly proves total finiteness from P in thick(k).

Every x in H_*(M) factors on homology through such a P, under Lemma 2's
filtered-colimit assertion. The image ideal must be zero by Lemma 1,
and therefore f_*(x)=0. Arbitrary integer degrees cause no change.

## Adversarial boundary checks

* Infinite-dimensional bialgebras without antipodes do admit nonzero
  finite-dimensional ideals (for example a monoid algebra of an infinite
  monoid with a two-sided absorbing element z; kz is an ideal). Thus the
  antipode is a real hypothesis, present here.
* Finite-dimensional Hopf algebras do admit nonzero finite-dimensional
  ideals, so the infinite-dimensional hypothesis is indispensable.
* The extension from fields to rings is false. No such extension is used.
* A graded algebra at odd characteristic cannot in general be ungraded
  while keeping its tensor coproduct multiplicative; the bosonization
  repairs exactly this issue. A pair of odd primitives is a useful exact
  countercheck for a missing crossing sign.
* Neither S bijectivity nor commutativity/cocommutativity is used anywhere
  above. The right-to-left conversion and both bosonized antipode
  identities are checked without S inverse.
* This proves vanishing on homology of maps, not that the maps are zero
  in the derived category. The report makes the same distinction.

Strongest verified statement so far: Lemma 1 in its full stated graded,
arbitrary-field scope, and Proposition 3 conditional on its compact-proxy
factorization input. No algebraic defect found. Remaining work: exact
small-model convention check, primary-source cross-check, and comparison
with earlier review after this independent record.
