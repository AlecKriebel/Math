# Pass 2: a precise failure of naive isotropic determinant truncation

E-6322, 2026-10-16. This is an admissible-map obstruction to a proposed proof step, not a minimizer counterexample and not a no-go theorem for every possible comparison construction.

## 1. An exact family in the full class

On B_1 in R^3, let r=|x| and 1/3<=alpha<1/2. Define

y_alpha(x)=(r^{-alpha}x_1,r^{-alpha}x_2,r^{5alpha}x_3), x not zero,
y_alpha(0)=0.

The trace is the identity. Continuity at zero follows since 1-alpha>0. Set beta=(-alpha,-alpha,5alpha), n=x/r. The rows of its derivative are

F_{i dot}=r^{beta_i}(e_i^T+beta_i n_i n^T).

The rank-one determinant formula gives exactly

J=r^{3alpha}(1-alpha+6alpha n_3^2).

The angular factor lies between 1-alpha and 1+5alpha. Hence J>0 away from zero, and J is comparable to r^{3alpha}.

For fixed alpha in this range,

|F| is comparable to r^{-alpha},
|cof F| is comparable to r^{-2alpha}.

For the lower cofactor bound, the minor formed by the first two rows and first two columns equals

r^{-2alpha}(1-alpha[n_1^2+n_2^2]) >= (1-alpha)r^{-2alpha}.

All other derivative and cofactor entries have the corresponding upper bounds. Consequently

P(F) is comparable to r^{-6alpha},
B(F)=dJ^{-2} is comparable to r^{-6alpha}.

The displayed derivative is in L^6 exactly when alpha<1/2. The function is genuinely W^{1,6} across zero: its classical derivative is integrable, it is continuous there, and the boundary term from removing a small sphere tends to zero. All four energy terms are finite. Thus y_alpha belongs to the full admissible class for all positive coefficient quadruples.

Nevertheless,

P(F)/J is comparable to r^{-9alpha},

which is not in L^1(B_1) for alpha>=1/3, including the logarithmic endpoint alpha=1/3.

## 2. Consequence for a proposed hard truncation

Under a material change of variables with derivative A and k=det A, the positive transformed density is k P(FA^{-1}). If A=k^{1/3}I is isotropic at a point, homogeneity gives exactly

k P(FA^{-1})=P(F)/k,

while the transformed barrier density is k^3 B(F).

A tempting prescription to raise J to epsilon on {J<epsilon} is k=J/epsilon there. For this ideal isotropic correction, its positive cost would be

epsilon P(F)/J.

For y_alpha above this cost has infinite integral on every neighborhood of the origin, whereas the original energy is finite. Thus even before solving the gradient compatibility and boundary problems, this particular isotropic hard-truncation formula is not guaranteed to stay in the finite-energy class.

Important limits of this conclusion:

- A variable scalar matrix field k(x)^{1/3}I is generally not the gradient of a deformation. This note does not pretend that the prescription already defines a comparison map.
- An anisotropic or otherwise structured comparison might have much smaller positive-energy cost. The example does not rule that out.
- The maps y_alpha are not minimizers: their affine trace has the affine map as the unique full-class global minimizer. The example cannot refute E-6322.
- Matching the powers of the positive and barrier energy does not prove stationarity; different components of the stress can have different leading orders.

## 3. The finite pointwise balance is weaker than hard truncation

If one temporarily ignores compatibility and allows only scalar material multipliers, the pointwise transformed energy is

P/k+B k^3.

Its minimizer over k>0 satisfies k^4=P/(3B). This can reduce a pointwise imbalance but does not generally set J/k above a fixed positive threshold. Since B=dJ^{-2}, the formal updated determinant is

J/k=(3d)^{1/4} J^{1/2} P^{-1/4}.

No uniform lower bound follows from that expression under the target assumptions. Turning these independent scalar choices into a global trace-preserving deformation remains a separate, unproved gradient-compatibility problem.

The safe finite radial comparison in `FINITE_COMPARISON.md` avoids these unsupported prescriptions, but supplies only the stated barrier-mass estimate, not determinant truncation or a gradient-integrability improvement.

## 4. What fixed-distortion compositions preserve

Let phi and its inverse have Lipschitz constant at most K. Under material composition, A=Dphi has singular values between K^{-1} and K, and k=det A lies between K^{-3} and K^3. For every p>=1,

K^{-(p+3)} integral |Dy|^p
<= integral |D(y composed with phi^{-1})|^p
<= K^{p+3} integral |Dy|^p.

This holds also when either integral is infinite. Likewise, a target composition by a K-bi-Lipschitz diffeomorphism preserves membership in every W^{1,p} gradient class, with constants K^{-p} and K^p. Such a target comparison must still fix the prescribed trace to be admissible.

The determinant transforms by multiplication or division by a factor bounded above and below. Bi-Lipschitz changes of material coordinates preserve null sets. Hence these comparisons also preserve the property ess inf J=0 versus ess inf J>0.

Thus a single fixed-distortion composition cannot literally truncate an unbounded gradient tail or convert a vanishing essential Jacobian infimum into a positive one. This does not say that minimality under all such comparisons cannot imply regularity. It says that any proposed literal regularizing sequence must allow nonuniform distortion and must estimate the resulting energy costs rather than appealing only to fixed-distortion admissibility.
