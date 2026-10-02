# Turn 1 — A signed affine-section case and an obstruction to sum-of-squares compression

AI-assisted mathematical proof candidate; independent review pending. Original unresolved1/5. The source permits arbitrary pairs of multi-affine polynomials; this turn treats a genuine restricted class and does not replace the general question by it.

## 1. Theorem

Let F be a nonconstant affine polynomial on R^n and let G be multi-affine. Suppose G has one sign on the entire hyperplane H={F=0}, for example G|H≥0. Then {F=G=0} is empty or an affine subspace. In particular it has at most one connected component, independently of n and of deg G.

More precisely, let S be the variables with nonzero coefficient in F and write x for these active variables and z for the others. Then

G(x,z)=Q(x)+F(x)R(z),

where Q is multi-affine of total degree at most2 in the active variables and R is multi-affine in the inactive variables. The restriction Q|H is a nonnegative quadratic polynomial. For a nonpositive G, apply the assertion to −G.

The factor F(x)R(z) may have arbitrarily high total degree, so the statement is a quadratic restriction/modulo-F theorem, not a claim that the original G always has degree≤2.

## 2. Full-support hyperplane lemma

First suppose F uses all r variables. Translating a point of H to0 and separately scaling the coordinates preserves multi-affinity and reduces F to L=x1+…+xr. Let P be the transformed G and assume P≥0 on L=0. We show deg P≤2.

If the degree d were at least3, let P_d be its nonzero highest homogeneous part. For every y with L(y)=0, taking t→+∞ in t^(−d)P(ty) shows P_d(y)≥0. Write P_d=Σ_|U|=d c_U x^U. Choose any d-element support S, choose ℓ∈S and i∈T=S\{ℓ}. Because |T|=d−1≥2, there is a point y supported exactly on T, with every y_j for j∈T nonzero and Σy_j=0. For example set all but the last active entry to1 and the last to−(d−2).

Every degree-d square-free monomial vanishes at y, so P_d(y)=0. This is a global minimum of P_d on the linear hyperplane. The derivative in the tangent direction e_ℓ−e_i must therefore vanish. At y, the derivative with respect to i vanishes because only d−2 other coordinates can be nonzero. The derivative with respect to ℓ has exactly one possible surviving monomial, namely the support S, and equals

c_S Π_(j∈T)y_j.

The product is nonzero, so c_S=0. This holds for every support S, contradicting P_d≠0. Therefore d≤2. The argument includes odd d without a separate parity assumption. If r≤2, multi-affinity already bounds the degree by2.

## 3. Inactive variables and affine constants

Return to arbitrary F. For any fixed active point x∈H and all but one of the inactive coordinates fixed, G(x,z) is an affine function of the remaining real coordinate and is nonnegative on the whole line. Its slope must be zero. Repeating for every inactive coordinate shows that G|H is independent of z. Let Q(x)=G(x,0). Then G−Q vanishes identically on H×R^(n−|S|), hence is divisible by the nonconstant affine polynomial F:

G−Q=F R.

This divisibility also follows by polynomial division in any active coordinate and evaluating the remainder on the hyperplane. For each active variable x_i, deg_(x_i)(FR)=1+deg_(x_i)R when R≠0, since the coefficient of x_i in F is a nonzero scalar. But G−Q is multi-affine, so R is independent of every active variable. For an inactive variable, the same degree argument shows R has degree at most1. Finally Q is multi-affine and nonnegative on its active hyperplane, so Section2, after translation/scaling, gives deg Q≤2. This proves the decomposition, including a hyperplane using only one active variable.

## 4. Connectedness and sharp scope

Choose affine coordinates y on the active hyperplane. A globally nonnegative quadratic q(y)=Q|H has an empty zero set or an affine-subspace zero set. Indeed, if y0 is a zero then it is a global minimum, so the linear part of q(y0+h) vanishes. Its quadratic matrix A is positive semidefinite, and q(y0+h)=hᵀAh. Thus the zeros are y0+ker A. The inactive coordinates remain free. This proves the theorem, including the identically-zero restriction case.

The sign assumption cannot simply be dropped. For n≥2, let

F=x1+…+xn,
G=−x1(x2+…+xn)−1.

Both are multi-affine, with degrees1 and2. On H, G=x1²−1, so the common zero set has two connected affine components. This is a scope control, not a counterexample to the source's existence of some degree-only bound.

The quadratic conclusion is exact rather than a disguised constancy theorem. Every quadratic in r−1 variables has a multi-affine quadratic lift to L=0. For diagonal coefficients q_ii and cross coefficients q_ij (with no factor2 convention), choose

a_(i,r)=−q_ii,
a_(i,j)=q_ij−q_ii−q_jj for i<j<r.

Then Σ_(i<j≤r)a_ij x_i x_j restricts under x_r=−Σ_(i<r)x_i to Σq_ii x_i²+Σq_ij x_i x_j. Linear and constant terms lift directly. This includes every nonnegative quadratic on H.

## 5. Relation to the known three-equation example

Basu–Perrucci's Example2.2 fixes the first two elementary symmetric functions, then uses a third multi-affine equation to obtain Σ x_i²(x_i−1)²=0 and binomially many isolated points. If one keeps an affine first equation and tries to replace the other two equations by one multi-affine polynomial that is nonnegative on the entire affine hyperplane, the theorem above prevents that strategy: the resulting common zero set must be affine and connected when nonempty. This is a specific obstruction to global sum-of-squares-style compression. It does not rule out a sign-changing second polynomial, two nonlinear equations, local minima, or a different counterexample mechanism.

## 6. Checks, credit and status

Run `python turn1/check_affine_sign.py`; stdout is frozen in turn1/verification.json. It checks3,747 exact coefficient-isolating derivative identities,210 arbitrary quadratic lifts with exact evaluations, and the two-component scope example, with7,447 assertions total. Nonnegativity and connectedness follow from the proof, not numerical sampling.

Primary source question: OWR9/2025 printed445–446, https://ems.press/content/serial-article-files/51353. The prior one-polynomial and three-polynomial results, including the Newton identities motivating the attempted compression, are credited to Basu–Perrucci, https://arxiv.org/abs/2204.01595, Theorem2 and Example2.2. The current proof uses elementary polynomial and positive-semidefinite quadratic facts; no historical novelty certification is claimed. Original unresolved1/5, informal completion estimate15%.
