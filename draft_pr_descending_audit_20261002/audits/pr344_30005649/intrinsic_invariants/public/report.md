# Intrinsic-invariants adversarial review of PR 344 / record 30005649

Review checkpoint: 2026-10-04 03:55:48 UTC.
Candidate head: `86a758b1cc9c94322ce6afc3d17150fa2c90327a`.
Independent family: Cartier-dual intrinsic invariants and cyclic-word structure.
Mathematical review complete; administrative closure awaiting parent approval.

## Verdict and scope

The submitted construction is a valid counterexample to the auxiliary
automatic-self-duality question following Takao's Proposition 2. For every
prime p > 3 and every n >= 3 it gives, over k = algebraic closure of F_p, a
p-killed finite flat commutative group scheme over W(k) of rank p^(2n) whose
special fiber is qss and is not Cartier self-dual. The lift is also not
self-dual. I found no mathematical defect in the construction or in the
quantifier scope of `TURN_1.md`.

This verdict does not establish priority, classify all qss group schemes or
perfect-field forms, construct a principally polarized Jacobian, or settle
the Coleman conjecture. The special-fiber hypothesis is crucial: the qss
filtration is not required to lift over W(k).

The exact question and distinction between the special fiber G and the group
scheme over W are pinned in the earlier source-only baseline. Takao's
Proposition 2 supplies the n <= 2 affirmative boundary for the original
ambient hypotheses. The minimum n for this failure is therefore 3, or rank
p^6, using that stated source theorem. Section 5 additionally derives the
algebraically closed rank-four special-fiber boundary independently; it does
not claim to reprove the theorem for all Witt-vector lifts over every perfect
field.

## 1. Intrinsic obstruction with all semilinear twists retained

Let D = (M,F,V) be a finite-dimensional module over any perfect field k, with
F sigma-semilinear and V sigma-inverse-semilinear. Use the contravariant dual
operators verified in Hoshi Definition 2.3:

    F_dual(phi)(x) = sigma(phi(V(x))),
    V_dual(phi)(x) = sigma^(-1)(phi(F(x))).

For every r >= 1, iteration gives

    F_dual^r(phi)(x) = sigma^r(phi(V^r(x))),
    V_dual^r(phi)(x) = sigma^(-r)(phi(F^r(x))).

Write U-perp for the annihilator of U in M-dual. These formulas show

    im F_dual^r = (ker V^r)-perp,
    im V_dual^r = (ker F^r)-perp.

For example, the first image is contained in the first annihilator directly
from evaluation. Its dimension equals rank V^r: the kernel of F_dual^r is
(im V^r)-perp, and perfectness makes the semilinear image a k-subspace of the
usual rank. Equality follows from the equal dimensions. This argument uses
no finite order assumption on sigma and no prime-field matrix simplification.

Consequently the invariant

    delta_r(D) = dim(im F^r intersect im V^r)

satisfies the general formula

    delta_r(D-dual) = dim M - dim(ker F^r + ker V^r).

A k-linear isomorphism respecting the two semilinear operators preserves all
the image and kernel spaces, and hence delta_r. This is an intrinsic
obstruction to any duality isomorphism, including ones not represented by an
alternating bilinear form.

## 2. Construction as a cyclic graph and direct invariant computation

Construct a six-vertex cycle with word `FFVFVV`. An F edge at position i maps
e_i to e_(i+1); a V edge maps e_(i+1) to e_i, with indices modulo six. This
gives exactly

    F(e0)=e1, F(e1)=e2, F(e3)=e4;
    V(e0)=e5, V(e3)=e2, V(e5)=e4,

and zero on the other basis vectors. This cyclic graph is merely an explicit
presentation; the verdict uses no unsupported completeness or equivalence
theorem for cyclic words.

The two mixed composites vanish. Both third iterates vanish. Directly,

    im F = ker V = span(e1,e2,e4),
    im V = ker F = span(e2,e4,e5).

Thus this is a deformable module in the precise sense of Hoshi Definition
3.4. Moreover,

    im F^2 = k e2,    im V^2 = k e4,
    ker F^2 = ker V^2 = span(e1,e2,e3,e4,e5).

Section 1 therefore gives delta_2(D)=0 and delta_2(D-dual)=1. This proves
non-self-duality over every perfect field on which this displayed module is
defined. Individual iterate ranks are equal and would not detect the
obstruction; the incidence of image and kernel spaces does.

Hoshi Proposition 2.5 gives the contravariant equivalence with p-torsion
finite commutative group schemes over k and identifies this module duality
with Cartier duality. Therefore the corresponding k-group H is not
self-dual. Choosing algebraically closed k in the next section guarantees the
exact qss condition of Takao's definition, without asserting its descent to
every perfect field.

## 3. Exact qss and finite-Honda gates

The adapted vectors

    u=e1+e3+e5, v=e2+e4, w=2e1+e3,
    z=e2, a=e0, b=e1

form a basis over every characteristic. The inverse has integer coefficients:

    e0=a, e1=b, e2=z, e3=w-2b, e4=v-z, e5=u-w+b.

The subspaces span(u,v) and span(u,v,w,z) are stable under F and V. On their
successive two-dimensional quotients, and on the final quotient, the operators
have a basis (x,y) satisfying

    F(x)=V(x)=y, F(y)=V(y)=0.

Their exactness is checked directly, and im F = im V in each factor. Hoshi
Lemma 4.9, with its standing deformability hypothesis, identifies them as
superspecial. Definition 4.8 is geometric over a general perfect field; here
k is algebraically closed, so its dimension-two case gives actual E_i[p]
over k. Contravariant exactness reverses the module flag and produces an
actual group-scheme filtration with those elliptic p-torsion quotients.
This proves qss membership in Takao's Definition 1(3), including the nonsplit
quotients. The rank of H is p^6, also directly obtained as the product of its
three quotient ranks p^2; no additional rank convention is needed.

For lifting, take L=span(e0,e3,e5). It is complementary to im F. The images
V(e0), V(e3), V(e5) are the independent vectors e5,e2,e4, and V restricted
to L is injective because k is perfect. Viewed through W(k) -> k, M is a
finite-length W-module killed by p, F and V have the required Witt-Frobenius
semilinearity, and their mixed composites equal multiplication by p (zero).
Also pL=0 and L/pL -> M/im F is an isomorphism.

These are all the finite-Honda conditions of Hoshi Remark 3.5.1. Together
with exactness, they put (M,L) in Definition 3.6's category. Proposition
3.11(2) gives the anti-equivalence with p-torsion finite flat group schemes
over W for p != 2, and (5) identifies reduction with forgetting the
deformation subspace. Its base assumptions are exactly p prime and k
perfect; there is no finite-field, polarization, or qss-lifting hypothesis.
Hence this datum gives a valid lift over W(k) for every allowed p > 3.

Finite-flat rank equals its special-fiber rank. Cartier duality commutes with
base change: reducing any self-duality isomorphism of the lift would give a
self-duality isomorphism of H. The latter has been excluded. This completes
the Witt-vector part of the counterexample.

For n > 3, add n-3 direct summands I with F(x)=V(x)=y and the Honda line
span(x). The conditions hold blockwise, the elliptic factors extend the qss
filtration, and both second iterates vanish on the extra factors. Thus
delta_2 remains 0 and its dual value remains 1 for every n >= 3. This is a
symbolic argument for all n and p, not an extrapolation from finite tests.

## 4. Source verification and submission weakness

The supplied official Takao PDF and all five corresponding rendered pages
were read before candidate exposure. After release I read only the four
authorized candidate files, froze the first independent assessment, then
checked the primary Hoshi manuscript through its native extraction and
supplied renders of pp. 5--9 and 13. I also read Definition 1.1's base/category
assumptions and Definition 4.8's geometric superspecial convention in the
extraction. The exact source and candidate pins are retained privately.

The submitted degree-two F25 pairing test uses a field where sigma equals
sigma inverse. It therefore cannot distinguish the direction of Frobenius
twists. This is a limited finite control, not a defect in the all-field
symbolic proof. The independent control below repairs that coverage gap.
No universal result or minimal-rank conclusion rests on prime enumeration.

## 5. Independent low-rank structure and meaningful positive controls

For n=0 the object is zero. For n=1 the qss special fiber is elliptic
p-torsion by definition and is self-dual. Over algebraically closed k, Takao
Lemma 1 gives the following complete rank-four special-fiber normal form in
an adapted basis e1,f1,e2,f2:

    F(e1)=V(e1)=f1, F(f1)=V(f1)=0,
    F(e2)=f2+A e1, V(e2)=f2+B f1, F(f2)=0.

The relation VF(e2)=0 forces V(f2)=-A^(1/p) f1. Choose c with
c^(p^2)-c=B^p; such a root exists over algebraically closed k. Replacing
e2 by e2+c e1 and f2 by f2+c^p f1 removes B. If A=0, the module is the
split sum of two elliptic modules.

If A != 0, choose nonzero t satisfying

    t^(p^4-1) = -A^(p-p^3).

Set x0=t e2, x1=F(x0), x2=F^2(x0), x3=V(x0) after the preceding
normalization. These are independent, and V^2(x0)=F^2(x0)=x2. The result
is the `FFVV` module:

    F(x0)=x1, F(x1)=x2, V(x0)=x3, V(x3)=x2.

It is self-dual by the explicit k-linear permutation
x0 -> x2-dual, x1 -> x3-dual, x2 -> x0-dual, x3 -> x1-dual. This map
commutes with the properly semilinear dual operators; its coefficients are
in the prime field. Thus all rank-four qss special fibers over algebraically
closed k are split or of this nonsplit type and are self-dual. This is an
independent consequence of the source lemma, with its field restriction
retained.

The nonsplit module itself is qss over algebraically closed k: its first
factor is span(x1+x3,x2), and the quotient has F(x0)=x1,
V(x0)=-x1. Rescale x0 by lambda with lambda^(p^2-1)=-1 to obtain the
equal-image elliptic basis in the quotient. The module has F^2 != 0, unlike
the split sum, so it is a meaningful nonsplit control.

With Honda subspace span(x0,x3), the above permutation maps the subspace
onto its evaluation annihilator, which is the Honda dual subspace by Hoshi
Definition 3.10. Hence this particular nonsplit rank-four lift is also
self-dual. The elliptic module with its standard Honda line has the analogous
swap isomorphism. These are verified positive controls, not a classification
of all Honda subspaces over arbitrary perfect fields.

## 6. Independent computation and evidence limits

`verify_intrinsic.py` is a standalone, standard-library, read-only verifier.
It constructs the module from the cyclic word; it imports no submitted code.
It checks the integer inverse and qss identities, Honda ranks, kernel/image
invariants, elliptic and nonsplit rank-four duality isomorphisms, direct-sum
controls at p=5,7,11 and n=3,4,9, and a broken-edge exactness mutant.

The semilinear control uses F125 = F5[t]/(t^3+t+1), an irreducible cubic
since it has no F5 root. Frobenius is exponent 5 and inverse Frobenius is
exponent 25. A diagonal basis change gives genuinely nonprime coefficients.
The general dual matrices are sigma(V)-transpose and sigma-inverse(F)-transpose.
The verifier checks 4,756 evaluation-pairing controls, including all field
coefficients on individual basis coordinates and 256 deterministic full
vectors. It detects the plain-transpose mutant in 744 controls and an
inverse-direction mutant in 360. The computed intrinsic values remain 0
for the module and 1 for its dual.

The submitted checker was also executed once and passed 9,014 assertions;
that run is recorded separately and is not treated as independent proof.

The first independent verifier run failed because I transcribed two inverse
basis columns incorrectly. Before rerunning, I also corrected the program's
unreached numerical expression for the annihilator intersection, replacing
dimension minus stacked rank by rank(F^2)+rank(V^2)-stacked rank. The symbolic
formula in the frozen first assessment was correct throughout. Exact failed
inputs, actual failure stderr, and the corrected successful run are retained.
No receipt has been synthesized from a claimed execution.

Every retained child-run receipt contains actual argv, interpreter/executable
pins, exact sanitized environment, UTC start/end times, full stdout/stderr,
exit code, before/after code/input pins, and stability. Private source
extraction is retained privately; the public verifier itself writes nothing.

## References

* Naotake Takao, contribution in OWR 42/2023, printed pp. 2476--2480:
  [official PDF](https://ems.press/content/serial-article-files/47479),
  [DOI](https://doi.org/10.4171/OWR/2023/42).
* Yuichiro Hoshi, *Pseudo-rigid p-torsion finite flat commutative group
  schemes*, J. Number Theory 229 (2021), 261--276; March 2021 revised
  [author manuscript](https://www.kurims.kyoto-u.ac.jp/~yuichiro/rims1911revised.pdf).
  Definitions 2.1--2.4, Proposition 2.5, Definitions 3.4--3.6 and 3.10,
  Remark 3.5.1, Proposition 3.11, Definition 4.8, Lemma 4.9.

These primary classification results are used and credited, not reproved or
claimed as new. No current-literature or novelty certification is made.
