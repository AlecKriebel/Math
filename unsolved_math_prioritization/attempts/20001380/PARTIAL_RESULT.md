# Explicit differents and upper ramification bounds for the zero-rooted tree

**20001380 / AIM-DYNAMICAL_SYSTEMS-0038. Scoped partial theorem; original image/size question unresolved. One substantive approach. Separate adversarial review pending.** No historical novelty is claimed. The zero basepoint is an explicit interpretation of the original question, whose text omits a basepoint.

## 1. Source, conventions, and prior work

[The live AIM section](http://aimpl.org/galarithdyn/12/) contains Problem 12.2 about the arboreal representation of $f(z)=z^2+1$ over $\mathbb Q_2$. Neither that problem nor its section introduction specifies the root. The record's descriptive title adds a zero-rooted interpretation; we retain it explicitly rather than treating it as recovered source text. Adjacent Problem 12.1 asks broadly about wild ramification and an arboreal analogue of Sen's theorem.

The imported prior report already establishes, for root zero, regularity, the first two splitting-field degrees, branch-valuation denominators, the rank-three level-sign quotient, infinite index, and infinite wild ramification. Those results are credited prior material, not rediscovered here. Its discriminant calculation concerns the iterate polynomial; the present argument identifies the full integer ring of each single-root field and uses its **field different** to bound the splitting-field upper ramification breaks.

[Anderson–Hamblen–Poonen–Walton, *Local arboreal representations*](https://math.mit.edu/~poonen/papers/arboreal.pdf), IMRN2018,5974–5994, Theorem2.1, proves infinite index for a local arboreal image. Their Theorem7.3 gives infinite wild ramification in our case $p=2,c=-1,v_2(c)=0$; this is also Theorem1.3(c)'s applicable regime. Their §5.2 specifies the lower/upper ramification conventions and the compatibility with finite quotients used below. The complete primary paper was retrieved; these sections and proofs were read. We do not identify infinite index or infinite wild ramification as new conclusions.

The recent [Barcau–Paşol preprint, arXiv:2606.29310v1](https://arxiv.org/abs/2606.29310), Theorem1.1, states an unramified/deeply-ramified dichotomy for a fixed inverse branch under hypotheses satisfied by $f$. Its hypotheses and different-growth section were inspected, but its entire proof is not independently certified here. This qualitative overlap is acknowledged; that theorem is not a premise of our explicit formulas, and no new qualitative deep-ramification discovery is claimed.

Fix $v_2(2)=1$, an algebraic closure, and a compatible branch

$$\alpha_0=0,\qquad f(\alpha_j)=\alpha_{j-1}.$$

Write $P_n=f^n$, $E_n=\mathbb Q_2(\alpha_n)$, and $L_n=\mathbb Q_2(f^{-n}(0))$. The $E_n$ are nested single-root fields and the $L_n$ are nested finite Galois splitting fields. Distinctness of roots follows also from the Eisenstein calculation below and characteristic zero; the forward orbit of zero is a sequence of positive integers after its first step, so the zero-rooted preimage graph is the regular binary tree.

For a finite extension $M/K$ of local fields, write $d(M/K)=v_M(\mathfrak D_{M/K})$, with $v_M$ normalized to take value one on a uniformizer. This is a different exponent, not the valuation of a splitting-field polynomial discriminant. Put

$$e_n=e(L_n/\mathbb Q_2),\quad G_n=\operatorname{Gal}(L_n/\mathbb Q_2),\quad m=\lfloor n/2\rfloor,$$

and let $b_n=\sup\{u\ge0:G_n^u\ne1\}$ in the usual upper numbering. Inertia is $G_n^0$; its order is $e_n$, possibly smaller than $|G_n|$.

## 2. Partial theorem

For every branch and every $n\ge1$:

1. $E_n/\mathbb Q_2$ is totally ramified of degree $2^n$. If $\varepsilon_n=0$ for even $n$ and $1$ for odd $n$, then

   $$\mathcal O_{E_n}=\mathbb Z_2[\alpha_n-\varepsilon_n].$$

2. The exact single-root-field different is

   $$\boxed{d(E_n/\mathbb Q_2)=2^n\left(n+\frac{1-4^{-m}}3\right).} \tag{1}$$

3. The splitting fields satisfy

   $$\boxed{b_n\ge n-1+\frac{1-4^{-m}}3+\frac1{e_n}.} \tag{2}$$

   In particular their largest upper breaks are unbounded. For $L_\infty=\bigcup_nL_n$ and $G_\infty=\operatorname{Gal}(L_\infty/\mathbb Q_2)$, **every** upper ramification subgroup $G_\infty^u$, $u\ge0$, is infinite.

The theorem does not determine the exact splitting-field degrees, their full ramification filtrations, a presentation of $G_\infty$, or its Hausdorff dimension. It makes no assertion that the Galois tower is APF or strictly APF: infinite upper groups are not the same assertion as open upper groups.

## 3. Alternating Eisenstein generators

Modulo2, induction using $(x+y)^2=x^2+y^2$ gives

$$P_n(x)\equiv x^{2^n}+(n\bmod2).$$

Consequently $Q_n(x):=P_n(x+\varepsilon_n)$ reduces to $x^{2^n}$. Let $a_j=f^j(0)$. The recurrence $a_{j+1}=a_j^2+1$ gives

$$a_j\equiv\begin{cases}1\pmod4,&j\text{ odd},\\2\pmod4,&j\ge2\text{ even}.\end{cases}$$

For even $n$, $Q_n(0)=a_n\equiv2\pmod4$; for odd $n$, $Q_n(0)=f^n(1)=a_{n+1}\equiv2\pmod4$. Thus $Q_n$ is Eisenstein of degree $2^n$.

It follows that $\pi_n=\alpha_n-\varepsilon_n$ is a uniformizer of $E_n$, and $E_n/\mathbb Q_2$ is totally ramified of degree $2^n$. For completeness, the integer-ring conclusion does not assume an unverified global monogenicity property. Every element has a unique expansion $\sum_{i=0}^{2^n-1}c_i\pi_n^i$ with $c_i\in\mathbb Q_2$. The valuations $2^nv_2(c_i)+i$ of its nonzero summands are pairwise distinct modulo $2^n$. Their minimum is the valuation of the sum. If the sum is integral, every one is nonnegative, forcing all $c_i\in\mathbb Z_2$. This proves the asserted local integral basis.

## 4. Exact single-root different

For a monogenic local integer ring, the different is generated by the derivative of the minimal polynomial; see [Sutherland, Lecture12, Proposition12.24](https://ocw.mit.edu/courses/18-785-number-theory-i-fall-2021/mit18_785f21_full_lec.pdf). Therefore

$$d(E_n/\mathbb Q_2)=v_{E_n}(Q_n'(\pi_n))=2^n v_2(P_n'(\alpha_n)).$$

The chain rule and branch compatibility give

$$P_n'(\alpha_n)=2^n\prod_{j=1}^n\alpha_j.$$

The Eisenstein generators imply $v_2(\alpha_j)=2^{-j}$ for even $j$, and $v_2(\alpha_j)=0$ for odd $j$, since then $\alpha_j=1+\pi_j$. It follows that

$$v_2(P_n'(\alpha_n))=n+\sum_{r=1}^{m}4^{-r}=n+\frac{1-4^{-m}}3,$$

which proves (1). The first four different exponents are $2,9,26,69$. Because these single-root extensions have residue degree one, these also equal the valuations of their local field discriminants. This equality is not asserted for the full splitting fields.

## 5. From differents to upper breaks

The tower formula for differents gives

$$d(L_n/\mathbb Q_2)=d(L_n/E_n)+e(L_n/E_n)d(E_n/\mathbb Q_2).$$

The first term is nonnegative. Since $e(E_n/\mathbb Q_2)=2^n$, division by $e_n=e(L_n/E_n)2^n$ yields

$$\frac{d(L_n/\mathbb Q_2)}{e_n}\ge n+\frac{1-4^{-m}}3. \tag{3}$$

The tower formula is [Sutherland, Proposition12.28]. No Galois assumption is needed on $E_n/\mathbb Q_2$.

Here is the normalization of the ramification identity used next. For a finite Galois extension $L/K$, set $G_t=\{\sigma:v_L(\sigma x-x)\ge t+1\text{ for all }x\in\mathcal O_L\}$ for $t\ge0$, and

$$\varphi(t)=\int_0^t\frac{|G_v|}{|G_0|}\,dv,\qquad G^{\varphi(t)}=G_t.$$

Let $e=|G_0|$. Hilbert's different formula is $d(L/K)=\sum_{i\ge0}(|G_i|-1)$. It can be seen directly here by passing to the maximal unramified intermediate field, choosing a uniformizer $\pi$ of $L$, and using the monogenic derivative product

$$d(L/K)=\sum_{1\ne\sigma\in G_0}v_L(\pi-\sigma\pi).$$

The uniformizer test determines each lower group because inertia fixes the maximal unramified field and its integer ring together with $\pi$ generates $\mathcal O_L$. Counting the positive integer valuations in that product gives the displayed group sum. Thus the tame term and the positive-parameter integral are

$$\frac{d(L/K)}e=1-\frac1e+\int_0^\infty\frac{|G_t|-1}{e}\,dt
=1-\frac1e+\int_0^\infty\left(1-\frac1{|G^u|}\right)du. \tag{4}$$

Endpoints of the step functions have no effect on either integral. For $L=L_n$, the final integrand is between zero and one and is zero for $u>b_n$. Combining (3) and (4) proves (2). In particular $b_n>n-1$.

## 6. Every upper group in the infinite tower is infinite

Upper numbering commutes with Galois quotients, so the restriction maps $G_{n+1}^u\to G_n^u$ are surjective and

$$G_\infty^u=\varprojlim_nG_n^u.$$

For any fixed $u\ge0$, choose $n$ with $b_n>u$. Then $G_n^u\ne1$, and surjectivity in the finite inverse system makes the projection from $G_\infty^u$ onto it surjective. Thus $G_\infty^u\ne1$ for every $u$.

Moreover $\bigcap_{v\ge0}G_\infty^v=1$: its image in each finite $G_n$ belongs to all of that group's upper ramification groups and hence is trivial. This is also [AHPW, Lemma5.4]. If one $G_\infty^u$ were finite, each of its finitely many nonidentity elements would disappear by some larger upper parameter. Taking the largest of these finitely many parameters would make a subsequent upper group trivial, a contradiction. Every $G_\infty^u$ is therefore infinite.

## 7. Exact remaining gap and attribution

This is one partial ramification route for the explicitly chosen zero basepoint. The imported report's size and sign-quotient bounds remain credited prior results. The present deduction uses classical Eisenstein, different, and Herbrand theory, and its historical priority is unconfirmed. It should not be described as an exact computation of the arboreal image.

There is still no description here of $G_n$ for general $n$, no recursive presentation, no exact splitting-field ramification filtration, and no Hausdorff-dimension calculation. Bounds on single-root fields do not by themselves determine their Galois closures. The broader literal AIM request remains **unsolved, 1/5**.

The exact checker verifies finitely many shifted iterates and discriminant valuations, the derivative and geometric-sum identities, and lower/upper normalization controls on abstract finite filtrations. These support the general proof but neither enumerate Galois images nor replace the infinite inverse-limit argument. Run `python verify.py`; the required SymPy dependency is recorded in its receipt.
