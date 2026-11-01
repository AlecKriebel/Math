# Independent mathematical acceptance report

Review date: 21 October 2026.

Reviewed artifact: `ETALE_AUDIT.md`.

Byte count: **12061**.

SHA256: **38e6b3e8f614a8c29a635b249556084bb7606ca2c0043bea37f2a97d7bbdb359**.

## Verdict

**Accepted for the mathematical claims and explicitly limited conclusions stated in this exact artifact. No mathematical repair is required.** This is an independent adversarial mathematical review, not proof-assistant certification, an exhaustive literature search, or a claim of new mathematical priority. A change to the reviewed bytes requires a new hash-bound review.

## Checks performed

### 1. Complete Tambara structure and lifting

The characteristic-two construction satisfies the full C2 Tambara-pair identities, including norm additivity, multiplicativity, restriction, transfer, Weyl, zero and unit identities. These supply complete norms, not only a Green structure. The functor-of-points calculation correctly uses a top idempotent with zero restriction; no omitted norm equation appears, because every bottom element belongs to the base algebra. Consequently the finite presentation and unique square-zero lifting argument are valid in both the Green and complete Tambara categories. The nilpotent-kernel extension also works by iterating Frobenius. These assertions do not require k to be a field or reduced.

### 2. Nonflatness against arbitrary modules

The modules D and E satisfy both the Mackey identities and the scalar Frobenius identities required of modules over the constant base. The inclusion D into E is genuinely monic. The displayed formula for D box_C M follows from all balanced pairing relations, including the zero-restriction constraint in the target. Therefore the two calculated tensor products, the module splitting S=C direct-sum D, and the nonzero tensor kernel are correct. This proof does not substitute orbitwise flatness for box-flatness and does not assert an impossible top-supported Tambara product factor.

### 3. Constant tensor formula for nonconstant modules

The stronger identity in Section 5 is valid for every A-module M and every c_G(A)-module X, with no flatness or finite-generation assumption:

(c_G(M) box_{c_G(A)} X)(G/H) = M tensor_A X(G/H).

To check this independently, choose any presentation A^(J) -> A^(I) -> M -> 0. Constantization preserves its cokernel and direct sums, and takes each free summand A to the unit c_G(A) of the module tensor product. Tensoring with X therefore produces the cokernel of the corresponding scalar matrix X^(J) -> X^(I). Evaluation at each orbit gives exactly M tensor_A X(G/H). Restrictions, transfers and conjugations are induced by those of X and commute with the scalar matrix. This establishes the claimed identity, including its natural Mackey structure.

It follows directly that an A-flat B gives a box-flat c_G(B), since exactness of Mackey module sequences is tested orbitwise. Conversely, testing constant-module injections and evaluating at G/e detects ordinary flatness. The report's alternative filtered-free argument is also valid. There is no group-order invertibility hypothesis.

### 4. Green and genuine differential detection

The constant tensor identity identifies the multiplication kernel with c_G(J), where J is the ordinary multiplication kernel of B tensor_A B -> B. Its Green square is c_G(J²), giving the stated constant Green differential quotient.

At the free orbit genuine decomposables give exactly J². In particular, a norm generator from a proper subgroup, when restricted to the free orbit, becomes a product with at least two factors from J. Transfers and multiplication by ambient elements do not move these restrictions outside J²; ordinary binary products give the reverse inclusion. Thus genuine differential vanishing implies ordinary differential vanishing. Ordinary vanishing implies Green vanishing and then genuine vanishing by the quotient map. This validates the exact equivalence needed in the report, without asserting an unwarranted general orbitwise criterion.

The definitions agree with [Hill, Section 5](https://arxiv.org/html/1701.06219v1). The free-orbit identification is also explicitly used in [Wisdom, Theorem 2.14](https://arxiv.org/html/2508.09365v2).

### 5. Finite presentation, classical étaleness and scope

Reflection of finite presentation follows from full faithfulness and filtered-colimit preservation, applied in the respective categories of algebras over the fixed base. Preservation is an existing theorem: the statement and proof of Theorem C / 4.29 were independently inspected in [Schuchardt–Spitz–Wisdom, Algebraically Closed Fields in Equivariant Algebra](https://www.math.ucla.edu/~jasonsch/pdfs/Schuchardt,%20Spitz,%20Wisdom%20-%20Algebraically%20Closed%20Fields%20in%20Equivariant%20Algebra.pdf). The result covers compact morphisms, not merely compact absolute objects.

Combining these facts with the classical finite-presentation, flatness and differential criterion proves the stated constant Tambara étaleness test. The algebraic-closure-of-F_p example correctly separates finite presentation from flatness plus zero differentials.

The report consistently credits the lifting counterexample to [Ferudun's existing preprint](https://eulersolve.org/papers/aim-algebraic-geometry-0162/) and the ghost construction to its earlier source. It explicitly distinguishes five audit routes from five novel discoveries. Its refusal to claim a solution of the separate diagonal, spectral or broad geometric programme is appropriate.

## Verification boundaries

The two quoted source-PDF byte counts and SHA256 values were recomputed and match the reviewed artifact. No claim is made here that these checks establish scholarly priority, peer review, or authenticity beyond identifying the inspected files. The preprint's supplementary finite test count was not reproduced. Acceptance rests on the general mathematical arguments, not that computational claim. No copied third-party source documents or source text are included in this acceptance report.
