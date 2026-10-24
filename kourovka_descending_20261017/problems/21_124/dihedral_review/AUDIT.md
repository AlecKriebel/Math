# Fresh adversarial audit: all-order dihedral holonomy obstruction

UTC: 2026-10-24T22:43:08Z. Reviewer: independent child agent
`/root/p21124_dihedral_adversary`, which did not author the proof or its
computational routines. **Verdict: PASS for the precisely restricted theorem.**
No outstanding substantive objection was found. The discovery estimate remains
**4% toward a complete resolution of 21.124**; this review does not warrant a
solved status, a preprint claiming resolution, publication, or a novelty claim.

The frozen input `nonabelian_holonomy/DIHEDRAL_OBSTRUCTION.md` has SHA256
`7d323b248aa9ecb3dccfb1ba204be6d146e65f2570283545ba3a6b21571be437`.
Every file and dependency in `DIHEDRAL_MANIFEST.json` matched its frozen hash.
The independent checker imports no author or earlier-reviewer code.

## What was checked mathematically

The group is the displayed four-edge, two-vertex tubular presentation with
`(p_i,q_i)=(3,2),(20,14),(119,84)`. The theorem concerns all finite orthogonal
actions whose invariant real decomposition has summands of dimension at most
two. In particular it concerns every finite dihedral group in every real
representation, regardless of group order and total dimension. It does not
concern all finite groups or all higher-dimensional irreducible representations.
The existing CAT(0) and free-by-cyclic eligibility results are dependencies;
neither assertion is newly proved in this audit.

1. **Affine rotations and powers.** Commutativity of `a,t` and of `b,t` in
   the actual affine image gives `(a^p t)^M=a^(pM)t^M` and its `b` analogue.
   Taking `M` to kill the finite quotient projections gives pure translations
   `A,B,T`. Stable-letter affine translation terms cancel when conjugating a
   pure translation, giving exactly `S_i(p_i A+T)=q_i B+T`. It is not necessary
   to assume that the original images of any vertex generators are pure
   translations. If the action of the abstract finite quotient has a kernel,
   choose `M` to kill its full quotient projections as well; this is an allowed
   common multiple and avoids any faithful-action convention. Alternatively a
   zero vector after killing only its effective linear part makes the element
   finite order, which also contradicts vertex injectivity.
2. **Invariant real planes.** An averaged inner product gives equivariant
   orthogonal projections. On a plane the orientation-preserving subgroup is
   finite cyclic. If a reflection is present, conjugate complex coordinates
   by a unit scalar so its phase is 1. Other reflection phases become ratios
   of two reflection phases, hence finite-order rotations. Rotation phases
   are unchanged. Thus the two free phases are roots of unity even when the
   original reflection phase itself is not a root of unity. The argument does
   not require the plane representation to be faithful or irreducible.
3. **Seven matrix patterns.** A reflection sends `z` to `lambda*conj(z)`;
   its conjugate equation has coefficient `lambda^-1`, with no extra minus
   sign. The real system is faithfully complexified by variables
   `A,bar(A),B,bar(B),T,bar(T)`. A nonzero real solution implies a zero
   determinant of that complexified system; the converse is not used.
   I independently constructed all seven matrices from these equations.
4. **Mann bound.** I checked the self-contained rational-coefficient minimal
   relation proof in the abelian dependency. For a prime power with exponent
   at least two, the degree-`p` cyclotomic extension forces separate vanishing
   residue subsums and eliminates that power by minimality. For a squarefree
   prime, the only dependence over the complementary cyclotomic field is the
   `1+X+...+X^(p-1)` relation; an empty class eliminates primes larger than the
   number of terms. This gives the stated squarefree bound. Repeated phases
   after specialization cause no problem: the partition is of term indices,
   and the theorem permits equal roots of unity.
5. **Necessary block tests.** The singleton, triangle-inequality, and
   equal-magnitude two-term exclusions are necessary. For three terms, absorb
   rational signs into the phases and use the relative `mu_6` bound. The
   noncollinear case has equal magnitudes, and the collinear case has largest
   magnitude equal to the sum of the other two. These tests only discard
   impossible blocks; they do not assume surviving blocks actually vanish.
6. **Unbounded to bounded orders.** Every minimal block has at most nine
   terms, so every relative monomial has order dividing 210. Every possible
   partition surviving the necessary tests has exponent differences spanning
   the full lattice `Z^2`. This implies `x^210=y^210=1`. The independent
   checker went beyond the index formula: it explicitly constructed integer
   combinations yielding `(1,0)` and `(0,1)` for every surviving partition.
   Thus the finite search is justified at every torsion order, rather than
   being a bounded numerical experiment.
7. **The singular endpoint.** At `x=y=1`, every plane matrix is either
   identity or ordinary conjugation. The two real character directions have
   signs in `{+1,-1}`. I checked directly that the coefficient matrix with
   rows `[p_i sign_i, -q_i, sign_i-1]` has rank three for all sign triples
   except the all-positive triple; there its rank is two and its kernel is
   exactly the `T` direction. Hence `A=B=0` even at the singular determinant.
   This conclusion does not require the whole finite quotient to be abelian.
8. **Dihedral representations and vertex injectivity.** Restricting a real
   representation of a finite dihedral group to its rotation subgroup and
   pairing inverse complex characters under a reflection produces real
   summands of dimension one or two. Degenerate characters give real lines;
   the remaining pairs give planes. Summing the proved zero horizontal
   projections gives `A=B=0` globally. Both vertex groups are the usual
   injected `Z^2` vertex groups in the tubular graph of groups, so their
   infinite-order elements `a,b` cannot acquire torsion in an injective
   image. This is exactly the claimed restricted nonexistence conclusion.

The Mann DOI landing page was not accessible through the available web tool.
No external verification of that primary paper is claimed; the self-contained
lemma was audited instead. Originality and a comprehensive priority search are
outside this audit.

## Independent computation

Run `python3 independent_check.py` from this directory, or run it by absolute
path. Standard-library Python 3 suffices. The checker regenerates only its own
`independent_results.json`; it does not mutate author artifacts.

* Determinants: subset dynamic programming and Laplace minors, rather than
  the author's 720-permutation expansion. All seven complete Laurent
  coefficient lists matched byte-independent canonical maps exactly. This
  checks the signs, phase assignments, coefficients, and zero monomials.
* Set partitions: a restricted-growth enumeration visited **66,949** complete
  partitions. Survivor counts were **12, 4, 131, 4, 131, 111, 12**, totaling
  **405**. Every survivor had lattice index one. All 405 explicit unit-basis
  constructions passed; their largest coefficient L1 norm was seven.
* Dihedral roots: the exact field was independently represented as
  `Q(zeta_3,zeta_5,zeta_7)` in its 48-element tensor basis. Here
  `-zeta_3*zeta_5*zeta_7` is a primitive 210th root. This differs from the
  author's monic-polynomial quotient representation. Screening used the
  different prime **211**, with primitive-order-210 element **2**. All
  **308,700** pairs across seven cases were checked. The 1,443 modular
  survivors were evaluated in the integral tensor basis, rejecting 1,436 of
  them. Each case had exactly the one zero `(0,0)` in exponent coordinates.
  Since the screen evaluates at a primitive root in characteristic not
  dividing 210, a genuine cyclotomic zero necessarily survives the screen.
* Commuting dependency: the independent tensor field
  `Q(zeta_4,zeta_3,zeta_5)`, prime **241**, and primitive-order-60 element **9**
  independently reproduced all **216,000** triples in the earlier abelian
  determinant. Its sole zero was `(0,0,0)`. All twenty candidate three-term
  blocks were independently excluded by the stated necessary test.
* Coordinate and normalization stress test: all **512** triples of matrices
  in a rational-coordinate `D4` were checked using direct real 6-by-6
  equations and rational elimination. The reflection coset used phase
  `(-7-24i)/25`, which is deliberately not a root of unity before
  normalization. Every kernel was purely vertical: the full/vertical rank
  pairs were `(4,0)` once, `(5,1)` 28 times, and `(6,2)` 483 times. This is a
  bounded falsification cross-check, not the premise of the all-order proof.

## Objections and exact remaining gap

No substantive objection survived. The harmless faithful-action convention
for the choice of `M` was resolved above without changing the claim or any
author file. No correction to the frozen theorem or algorithms is required.

The theorem excludes a large class of finite linear witnesses, including
unbounded finite dihedral holonomy. It leaves completely open a witness whose
finite linear representation has a real irreducible summand of dimension at
least three. No reduction of that central gap to the reviewed plane argument
has been established. It does not prove this CAT(0) free-by-cyclic group fails
to be virtually special, and it does not resolve Kourovka 21.124.
