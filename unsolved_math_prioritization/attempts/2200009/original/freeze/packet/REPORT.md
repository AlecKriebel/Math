# The fixed-degree mesh-preserver criterion is already proved

Problem 2200009 / AMR-021-0009, queue rank 1030. Disposition: **previously solved**, credited to Jonathan Leake and Nick Ryder. New mathematical search approaches: **0**. Independent review of this report: **pending**. No novelty claim.

## 1. Question recovered and status correction

The question concerns a real constant-coefficient operator built from finitely many integer backward translations. On polynomials of degree at most m, does preservation of real zeros separated by at least one reduce to a single test on the falling factorial of degree m? Shapiro's 2015 problem list presents this as Conjecture 5 and relates it to a finite-difference convolution conjecture. Its preprint location is page 3, Section V. [S]

The imported OPEN-TRIAGE note contains source lookup and an unsuccessful literature search, not a mathematical attempt. The bounded campaign duplicate gate found no substantive attempt. Its assertion that the problem was still open is superseded by the following primary theorem.

**Credited input.** Leake and Ryder prove that their backward-difference convolution preserves the class of real polynomials of degree at most m with root separation at least b, for b>0. This is Theorem 1.4 of their 2017 preprint. The theorem and definition are on page 2; the forward-difference convention is discussed on page 3. Two proofs occur on pages 13 and 17–19. The paper was subsequently published in Advances in Mathematics 374 (2020), article 107334. [LR]

The bibliographic match alone is not the reduction. Section 3 below derives the exact factorial and translation relating that theorem to the operator in the question.

## 2. Scope and boundary conventions

Work over the real numbers. Fix an integer m>=0 and let V_m be the polynomials of degree at most m. A nonzero polynomial is admissible if all its roots are real and consecutive distinct roots are at distance at least one; repeated roots are inadmissible. Nonzero constants and linear polynomials are admissible. We explicitly permit the zero polynomial as an output and include it in the closed admissible class, denoted H_m.

This treatment of low degrees is compatible with Brändén–Krasikov–Shapiro: their page 1 assigns infinite mesh in degrees at most one, and their page 2 treats the backward difference as a preserver, although it kills constants. They also allow zero in proper-position relations on page 5. The inspected sources do not provide a separate explicit numerical definition of mesh(0); we do not pretend that they do. [BKS]

If one instead requires every nonzero admissible input to have a nonzero admissible output, the criterion must additionally require degree T((x)_m)=m. Section 5 proves this stronger-convention statement. A zero-output definitional trap is not a counterexample to the intended conjecture.

## 3. Independently derived exact operator bridge

Put E f(x)=f(x-1), Delta=I-E, and

    F_j(x)=product_{i=0}^{j-1}(x-i),
    U_j(x)=product_{i=0}^{j-1}(x+i),
    F_0=U_0=1.

Let T=sum_{j=0}^k a_j E^j with real a_j. No bound k<=m is needed. On V_m, Delta^(m+1)=0, so expanding E=I-Delta gives

    T=sum_{s=0}^m c_s Delta^s,
    c_s=(-1)^s sum_{j=s}^k binom(j,s) a_j.                  (1)

The rising factorials obey

    Delta U_j=j U_{j-1}.                                  (2)

For j>=1, factor the common product x(x+1)...(x+j-2) from U_j(x)-U_j(x-1); the remaining difference is j. The case j=0 has zero difference. Repeated application gives Delta^s U_j=j!/(j-s)! U_{j-s}, with value zero when s>j.

Every U_j of positive degree vanishes at zero. Hence for 0<=s,j<=m,

    (Delta^s U_j)(0)=j! if s=j, and 0 otherwise.            (3)

Set h=T F_m and r(x)=h(x+m-1). Because T commutes with every translation and F_m(x+m-1)=U_m(x), including m=0, we have r=T U_m. Equations (1)–(3) imply

    (Delta^(m-s) r)(0)=m! c_s.                             (4)

Define the unnormalized convolution

    C_m(f,g)(x)=sum_{s=0}^m (Delta^s f)(x)
                              (Delta^(m-s)g)(0).

Substituting (4) proves the exact identity, for every f in V_m,

    T f(x) = C_m(f, h(.+m-1))(x) / m!.                    (5)

This proof is algebraic and does not assume real-rootedness. It also proves that h determines T on V_m, including when h has lower degree or is identically zero. In particular, h=0 implies T=0 on V_m. The empty stencil is allowed and represents that zero operator.

An independent convention check uses reflection Rf(x)=f(-x) and the forward difference Nabla f(x)=f(x+1)-f(x). Since Delta R=-R Nabla,

    C_m(Rf,Rg)=(-1)^m R C_m^+(f,g),                        (6)

where C_m^+ replaces Delta by Nabla. Alternatively, the same cyclic-basis proof with falling factorials gives T f=C_m^+(f,h)/m!. These identities remove any need to guess a forward/backward shift or a factorial normalization.

## 4. Proof of the intended equivalence using the credited theorem

Necessity is immediate: F_m belongs to H_m, so a preserver must send it to H_m.

For sufficiency, suppose h=T F_m belongs to H_m. If h=0, equation (5) makes T zero on V_m and the conclusion follows under the stated convention. Otherwise r(x)=h(x+m-1) has the same root gaps as h. For any nonzero f in H_m, the b=1 case of the credited Leake–Ryder theorem applies to f and r. Thus C_m(f,r) is admissible or zero. Multiplication by the nonzero scalar 1/m! does not change its roots, so equation (5) gives T f in H_m. Finally T0=0.

This proves the complete criterion for arbitrary real coefficients, any finite stencil length, all m>=0, and all lower-degree inputs. For m=0 or 1, every real polynomial in V_m already belongs to H_m and every such T preserves V_m, so the conclusion is also directly elementary.

The universal root-location theorem is a literature dependency. The explicit reduction (1)–(5), convention comparison (6), and edge-case arguments are independently proved here. The latter are explanatory verification, not a claim of a new solution.

## 5. Degree drops and the nonzero-only convention

Let A=sum_j a_j. On a polynomial f of degree d, every translate f(x-j) has the same leading coefficient. Therefore, if A!=0, T f has degree d and leading coefficient A times that of f. In particular, degree h=m, and T never kills a nonzero input.

If A=0, T kills the constant 1. Conversely, degree h=m is equivalent to A!=0 because F_m is monic. It follows that under the alternative convention excluding zero outputs, preservation is equivalent to both h in H_m\{0} and degree h=m.

The distinction is genuine: for m=2 and T=Delta, h=2(x-1) is a valid nonzero test polynomial, while T1=0. For Delta^2 the same test becomes the constant 2; Delta^3 annihilates V_2. These are degree-drop diagnostics, not disproofs of Leake–Ryder's theorem or of the intended source problem.

For additional algebraic checking, nonzero f,g of degrees d,e<=m satisfy C_m(f,g)=0 when d+e<m. Otherwise the first nonvanishing summand has index s=m-e and uniquely supplies the highest degree d+e-m. Its leading coefficient is

    lc(f) lc(g) d! e! / (d+e-m)!.

This proves all degree outcomes without numerical root approximation.

## 6. Verification and limits

The standard-library rational-arithmetic verifier performs 8,829 finite checks. These include 1,890 backward-bridge and 1,890 forward-bridge cases through ambient degree eight; coefficient recovery; Newton-factorial identities; exact degree and leading-coefficient formulas; reflection and convolution symmetry; and 1,600 quadratic mesh tests. In a real quadratic Ax^2+Bx+C, the exact test B^2-4AC>=A^2 certifies real roots at distance at least one. No floating-point root solver is used.

Explicit wrong-formula controls detect omission of the translation, omission of m!, and confusion of forward/backward differences. Hostile API inputs reject bool-as-int, floats, strings, null, subclasses of int or Fraction, wrong containers, noncanonical polynomials and excessive degrees. No test depends on Python assert statements.

The bootstrap authenticates the exact payload inventory against an externally pinned manifest before executing the verifier. The separate replay controls exercise normal, -O and -OO modes, source-free relocation, genuinely nonroot read-only execution with write-denial probes, byte corruption, missing/extra files, symlinks, nonregular files, forged metadata, hostile code/imports and exact-type claim mutations. The final receipt gives the observed results. Standard-library-only replay requires no source PDF or dataset. Historical source inspection is not misrepresented as a new online fetch during replay.

These computations corroborate the normalization and finite cases. They do not prove the universal mesh theorem, establish originality, constitute independent mathematical peer review, or show GitHub CI success. There is no remaining mathematical gap in this source-scoped prior-solution classification once the cited theorem is accepted. No five-approach search was needed after verifying a complete prior solution. No repository mutation or publication was performed for this report.

## References

[S] Boris Shapiro, *Problems around polynomials: the good, the bad and the ugly*, Arnold Mathematical Journal 1 (2015), 91–104. Conjectures 5–6, Section V of the preprint, page 3. https://arxiv.org/abs/1503.05295v1

[LR] Jonathan Leake and Nick Ryder, *Connecting the q-Multiplicative Convolution and the Finite Difference Convolution*, Advances in Mathematics 374 (2020), 107334. Pinned mathematical text: arXiv:1712.02499v1, Theorem 1.4. https://arxiv.org/abs/1712.02499v1 ; https://doi.org/10.1016/j.aim.2020.107334

[BKS] Petter Brändén, Ilia Krasikov and Boris Shapiro, *Elements of Pólya–Schur theory in the finite difference setting*, Proceedings of the American Mathematical Society 144 (2016), 4831–4843. Pinned preprint arXiv:1204.2963v2, pages 1–2, 5 and 9–10. https://arxiv.org/abs/1204.2963v2
