# Author turn 1: ordered corrections and a point-pushing model

**Target:** 10400036 / Polyak Problem 2.14. **Outcome:** scoped partial results; the full original construction remains unresolved. One substantive author turn is used.

These deductions are elementary consequences of the classical Magnus definition and intersection conventions. No novelty is claimed. In particular the obstructions below do not refute a based or corrected interpretation, which the source explicitly permits.

## 1. The symmetric part is forced by lower invariants

For an ordered string link $L$ with components 1,2,3, use its canonical based meridians and preferred parallel of component 3. Write a word for this parallel to sufficiently high nilpotent order. Delete all other letters when computing the coefficients involving only $X_1,X_2$. Put

$$
a=\mu_{1,3}(L)=\operatorname{lk}(L_1,L_3),\quad
b=\mu_{2,3}(L)=\operatorname{lk}(L_2,L_3),\quad
c=\mu_{12,3}(L),\quad d=\mu_{21,3}(L).
$$

Then, **as an equality of integers**, without a lower-vanishing assumption,

$$
\boxed{c+d=ab.} \tag{1}
$$

To verify (1) directly, write the word as $x_{i_1}^{\epsilon_1}\cdots x_{i_N}^{\epsilon_N}$ with $\epsilon_j=\pm1$. In its Magnus expansion, the coefficient of $X_1X_2$ is

$$
c=\sum_{r<s,\ i_r=1,\ i_s=2}\epsilon_r\epsilon_s,
$$

and the coefficient $d$ is the analogous sum with the two labels reversed. A single factor has no mixed degree-two term. Every product of an occurrence of label 1 and an occurrence of label 2 belongs to exactly one of these two ordered sums. Their sum is the product of the two exponent sums, namely $ab$. The same argument applies after choosing any sufficiently deep nilpotent representative of the canonical longitude: the relevant coefficients are precisely the defined string-link invariants.

Equation (1) is the elementary distinct-index shuffle identity, consistent with the exponent identities in Mellor–Melvin (2003), §1. It is not a new invariant.

## 2. What an unmodified alternating intersection rule cannot do

For two oriented surfaces in an oriented three-manifold, the oriented transverse intersection changes sign when the surfaces are interchanged:

$$
F_2\cap F_1=-(F_1\cap F_2).
$$

Consequently a rule that uses an ordinary closed intersection curve, retains this sign under exchanging labels 1 and 2, and then takes its ordinary linking number with component 3, would produce numbers $A_{12,3}=-A_{21,3}$.

Such a rule **cannot equal both ordered integer invariants for all string links**, because (1) has nonzero right-hand side whenever $ab\ne0$. This is an obstruction to the stated alternating rule, not to all possible interpretations of Polyak's “appropriate sense.” Ordered boundary data or correction terms can and must alter that naive behavior.

There is also an integral obstruction to a particularly simple proposed correction. Suppose

$$
c=A_{12,3}+C_{12,3},\qquad d=A_{21,3}+C_{21,3},
$$

where $A_{12,3}=-A_{21,3}$ and $C$ is an integer correction symmetric under interchanging the first two labels at a configuration with identical pairwise linking data. Then a case with $a=b=1$ would require $2C=1$, which is impossible. Thus an integer correction depending symmetrically only on those lower linking data cannot suffice. This does not rule out an ordered correction, dependence on basing/clasp words, or a more general relative intersection construction.

## 3. An actual string-link family realizing the obstruction

Let $p_1,\ldots,p_r,p_*$ be distinct points in an oriented disk. Keep the first $r$ strands vertical. Move the last strand through a smooth based loop $\gamma$ in the disk punctured at $p_1,\ldots,p_r$:

$$
L_i(t)=(p_i,t)\quad(1\le i\le r),\qquad
L_*(t)=(\gamma(t),t),\qquad \gamma(0)=\gamma(1)=p_*.
$$

The time coordinate ensures that this is a smooth embedded pure braid even when the disk projection of $\gamma$ has self-crossings. Keep $\gamma$ constant near its endpoints. Fix the standard boundary basing; choose the meridian loops $x_i$ positively so that their linking with strand $i$ is $+1$. Read the word $w$ of $\gamma$ using those meridians and the corresponding path-composition convention.

After forgetting the last strand, the complement is the product of a punctured disk and an interval. The preferred parallel of the last strand, closed using the fixed boundary basing, projects to $\gamma$. Its zero-framing adjustment can only affect the meridian of the last strand, which disappears upon forgetting that strand. Therefore every Milnor coefficient whose word uses only $1,\ldots,r$ and whose distinguished component is $*$ is the corresponding Magnus coefficient of $w$.

For $r=2$ choose $w=x_1x_2$. Then

$$
E(w)=(1+X_1)(1+X_2)
=1+X_1+X_2+X_1X_2.
$$

The actual three-string link has

$$
\operatorname{lk}_{12}=0,\qquad
\operatorname{lk}_{1*}=\operatorname{lk}_{2*}=1,\qquad
\mu_{12,*}=1,\quad\mu_{21,*}=0. \tag{2}
$$

Thus the obstruction in §2 is realized by a finite smooth string link, not merely by a formal power series.

### Why the unbased closure also loses necessary data

The point-pushing braids for $x_1x_2$ and $x_2x_1$ are conjugate: $x_1^{-1}(x_1x_2)x_1=x_2x_1$. Moving a braid prefix around its closure gives an ambient isotopy of their ordered, oriented closures; the conjugating braid is pure, so labels are not permuted. Yet their ordered coefficients $\mu_{12,*}$ are 1 and 0 respectively. Therefore no invariant that forgets the boundary basing and depends only on this unbased ordered closed link can recover the integer string-link coefficient in general. This is consistent with the closed-link triple indeterminacy, whose gcd here is 1.

### Direct failure of the bare disk-intersection recipe

The closures of the first two vertical strands are an unlink and bound disjoint disks. If those disks are used while allowing the last component to pierce them, their intersection curve is empty and its linking number with the last component is 0, contrary to (2). If instead one requires each disk or Seifert surface to avoid the last component, no such surface exists: its algebraic intersection with that component must equal the nonzero corresponding linking number. This explains two distinct failures of simply carrying over the vanishing-lower-invariant recipe. Neither failure precludes a corrected, based, or relative prescription.

## 4. A geometric ordered-intersection formula for the restricted family

For the point-pushing family in §3, choose disjoint oriented cuts in the punctured disk from the puncture boundaries to the outer boundary, avoiding the base point. Fix the basing so that crossing cut $i$ positively reads $x_i$. In general position $\gamma$ meets the cuts in a finite sequence

$$
(i_1,\epsilon_1),\ldots,(i_N,\epsilon_N),\qquad \epsilon_j\in\{+1,-1\}.
$$

For any ordered tuple $I=(j_1,\ldots,j_k)$ of distinct labels, define the signed ordered-intersection count

$$
\nu_I(\gamma)=
\sum_{1\le a_1<\cdots<a_k\le N\atop i_{a_\ell}=j_\ell\ (1\le\ell\le k)}
\epsilon_{a_1}\cdots\epsilon_{a_k}. \tag{3}
$$

This has a direct geometric meaning: count ordered $k$-tuples of crossings of the moving strand with the fixed vertical cut surfaces, with the product intersection sign.

**Proposition.** For this point-pushing family,

$$
\nu_I(\gamma)=\mu_{I,*}(L),
$$

with no lower-vanishing assumption. The count is unchanged by based homotopy of $\gamma$ in the punctured disk and by changes of cuts preserving the chosen based meridians.

**Proof.** Work modulo monomials containing a repeated variable. Each Magnus factor $(1+X_i)^{\epsilon}$ becomes $1+\epsilon X_i$. The coefficient of the distinct-index monomial $X_{j_1}\cdots X_{j_k}$ in the ordered product is exactly (3), because one chooses the linear term at each selected crossing position and the constant term at the others. Section 3 identifies this coefficient with the actual string-link invariant.

One can also see based-homotopy invariance directly. A generic cancellation introduces or deletes adjacent crossings of the same cut with opposite signs. A term in (3) cannot use both crossings because its labels are distinct. Terms using exactly one cancel in pairs; terms using neither are unchanged. The punctured disk cut open along the cuts is simply connected, so these word reductions describe the homotopy class with the basing fixed. A change of cuts preserving the same meridians gives another word representing the same element of the free group. This proves the proposition. ∎

The count remembers the order along the moving strand. It is **not** claimed to be an ordinary linking number with a choice-independent iterated Seifert intersection curve. It is a fully checked model for the additional ordered information such a construction must retain.

## 5. Exact gap and next route

This turn proves a necessary correction identity, a precise obstruction to two naive rule classes, explicit realizations, and a geometric ordered-intersection formula on a restricted point-pushing family. The first results use classical Magnus algebra and the last is its elementary cut-surface interpretation; all are credited deductions rather than novelty claims.

The full target remains: for **arbitrary** string links, construct intrinsic based/relative derived intersection data that gives a well-defined linking expression and prove exact equality with $\mu_{12\cdots n-1,n}$ despite nonzero lower invariants. No implication from the point-pushing family to all string links is assumed. No replacement of the source target by a Gauss-diagram formula, an invariant of the unbased closure, or a circular curve encoding of a precomputed $\mu$ is made.

A next route is to examine based C-complex longitude formulas and their ordered lower corrections, retaining the source's surface requirements. No final unresolved disposition is made after this first turn.
