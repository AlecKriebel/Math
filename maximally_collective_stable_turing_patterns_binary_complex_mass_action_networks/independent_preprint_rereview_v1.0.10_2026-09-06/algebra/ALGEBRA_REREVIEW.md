# Independent algebra referee report: v1.0.10

Target: `953c836a12b9d9d474521feb4a96e218c1155203`, read from the current audit's frozen `source_snapshot`. Completed 2026-09-06 local time (2026-09-07 UTC).

**Verdict in this scope: no correction to the shipped mathematics required.** The algebra, topology, stationary diffusion-ray theorem, sharp linear contrast, and scaled minimax claims survive this fresh review. The previous missing-hypothesis finding is closed in both standalone exports. A subsequent reciprocal check confirms the certificate referee's new generator/reader disagreement described below; that bounded software repair is needed. This is a scoped mathematical verdict, not a substitute for the independent release, certificate, document, and literature reviews.

## Review method and independence

I reread the actual statements and proofs in main Sections 1–5, the physical contrast and minimax arguments in Section 7, relevant supplement sections, and the two standalone exports before consulting the previous algebra report. I reconstructed the graph and determinant arguments directly. A new program, `independent_exact_checks.py`, builds the literal source and product complexes and computes the Jacobian from stoichiometry, reaction flux, and source complexes. It imports no project implementation or certificate reader.

This round uses direct exact Hurwitz determinants for all retained small principal matrices, a mechanism distinct from the manuscript's strongly connected component proof and the previous referee's SCC enumeration. Finite checks corroborate the general proofs; they are not used to extrapolate the all-dimensional results.

## Previous finding N1: closed

The standalone theorem summary at `external_audit/theorem_summary.tex:51–55` now states `det J=0` and `D=diag(d_1,...,d_n)` with all `d_j>0`. The proof skeleton at `external_audit/proof_skeleton.tex:47–55` supplies the same assumptions before the determinant expansion. These statements now exclude both exact counterexamples from the previous round. The main theorem at `manuscript/main.tex:398–423` already had the correct hypotheses and remains consistent with the repaired exports.

No mathematical result is strengthened by these repairs; they restore the intended domain in the abbreviated documents.

## Verified proof chain

### Complete realization and maximal localization

At `manuscript/main.tex:176–185,210–271`, the positive-flux parameterization and its converse are correct: every positive equilibrium has `J=A_m(a,b)H`, and every positive a,b and positive diagonal H is realized by the stated positive rates. Binary molecularity holds on both sides of every reaction. The conservation covector is semipositive and excludes X1, exactly as stated; neither the flux argument nor the localization proof assumes a strictly positive conserved covector.

The SCC classification at `manuscript/main.tex:279–328` accounts for every possible feedback path in a retained set of fewer than m vertices. A proper chain segment cannot close without one complete long cycle, unless the feedback stays in the boundary triad. The separate m=3 case correctly handles the empty interior chain. The only positive-parameter edge cancellation, b=2a, cannot create a new SCC and leaves both long cycles intact.

For arbitrary positive H, both long-cycle modulus inequalities are strict throughout the closed right half-plane. The boundary triad and its principal blocks obey the required strict Hurwitz inequalities. The negative signed core determinant then guarantees a positive real core eigenvalue by the intermediate value theorem. Thus the minimum unstable principal order is exactly m=n−1 in every positive realization, including the cancellation surface. See `manuscript/main.tex:330–381` and supplement S2.

The corrected omission proof remains sound at `manuscript/main.tex:483–513`: right chain fragment, boundary triad, then left chain fragment gives block lower triangular form; empty fragments include m=3. Column scaling supplies the product of h entries. The two claimed zero minors have the stated restricted nullvectors. These identities imply the exact coefficient in the stationary law.

### General diffusion ray and singular boundaries

At `manuscript/main.tex:398–447`, diagonal multilinearity gives the stated polynomial coefficients. For k≥2 every contributing signed principal minor is strictly positive. Therefore the bracket after the factor s is strictly increasing on s≥0. Its positive zero exists exactly when beta_1<0 and is unique and simple.

The derivative with respect to a nonnegative real spectral variable is strictly positive because the only potentially signed order-(n−1) terms contribute their explicitly positive sum. Consequently the sign of the determinant gives the claimed positive-real-eigenvalue band, and the threshold zero is algebraically simple. This works at n=2, where the lower-order minor condition is just the empty minor. The three exact n=2 sign cases in the new program include a threshold, the equality case with no positive threshold, and a strictly positive beta_1 case.

For the reaction family, homogeneous stability on c-perp ensures a simple conservation zero and the needed positive omission sum; the assumption is not replaced by an unsupported claim that T(H)>1 is sufficient. The exact boundary checks confirm that T(H)=1 has geometric zero multiplicity one and algebraic multiplicity two. T(H)<1 has a positive real homogeneous eigenvalue. These boundaries are excluded from the stable-realization claim at `manuscript/main.tex:515–569`.

### Sharp contrast and minimax scope

For fixed stable H, the stationary inequality forces chi_D>T(H). The approaching sequence with all X diffusivities equal to one and d_Z=T(H)+epsilon has exactly that contrast because T(H)>1. It proves an infimum without asserting attainment. The unit realization at a=b=1 justifies sharpness over stable realizations; the argument does not need all a,b at H=I to be stable. The product lower bound follows term by term from h_Z/h_j≥1/chi_H. See `manuscript/main.tex:579–617`.

For the scaled family, the interior h entries decrease with species index and the interior physical diffusion entries increase. On the entire certified interval, all interior h entries are at least one and all interior diffusion entries are below every boundary diffusion entry. The stated extrema therefore give the exact contrast formulas in `manuscript/main.tex:835–908,1051–1060`. The diffusion contrast already exceeds the equilibrium contrast at the lower endpoint, so the maximum is uniquely minimized within this sufficient family at that endpoint. The stationary product bound establishes exponent optimality, while the text explicitly leaves constant optimality and the full frontier open. There is no assumption that the sufficient endpoint is an intrinsic dynamical boundary.

## Fresh adversarial wave-scope witness

The general diffusion-ray theorem does not assume homogeneous stability. Its explicit limitation concerning nonreal instability is necessary, and the paper correctly preserves it. Consider

\[
J=\begin{pmatrix}
-1&0&0&31\\
1&-1&0&0\\
-15/31&1&-1&0\\
0&-15/31&1&-1
\end{pmatrix}.
\]

All signed singleton and order-two minors are 1, the four order-three minors are 1,16,16,1, and det J=0. Its characteristic polynomial is

\[
\lambda(\lambda^3+4\lambda^2+6\lambda+34).
\]

Thus it satisfies every hypothesis of the general theorem. With D=I, beta_1=34>0 and no positive stationary threshold exists. At s=1/10 the complementary cubic is

\[
\lambda^3+\frac{43}{10}\lambda^2+\frac{683}{100}\lambda+
\frac{34641}{1000}.
\]

All coefficients are positive, so it has no positive real root, but its cubic Routh determinant is −659/125, implying a nonreal unstable pair. This is a scope check, **not a counterexample to any asserted conclusion**. The PDE referee independently reconstructed this matrix and confirmed every minor, polynomial, and sign. It prevents treating the ray theorem as a full-spectrum stability theorem.

## Exact computational coverage

The new program and `EXACT_RESULTS.json`/`exact_checks.log` record PASS for:

| Check | Fresh exact coverage |
|---|---|
| Literal reaction construction, flux balance, conservation, stoichiometric rank, binary complexes | Every dimension used below |
| Direct principal-matrix Hurwitz tests | 912 matrices, 3,172 strictly positive Hurwitz determinants, m=3,...,7 |
| Flux cases in the direct Hurwitz campaign | (a,b)=(2/3,5/7) and (3/5,6/5); the second is b=2a; nonuniform rational H |
| Complete omission identities | 85 minors, m=3,...,12 |
| Conservation singular boundaries | 30 exact cases, T=1/2,1,2, m=3,...,12 |
| General n=2 theorem boundary | Negative, zero, and positive beta_1 |
| Nonreal-instability scope witness | Exact n=4 matrix, all theorem hypotheses, exact negative shifted Routh determinant |
| Physical contrast extrema and ordering | 24 exact lower-endpoint, midpoint, and upper-endpoint cases through nu=10007 |

Run the program using Python with SymPy from this directory. It uses explicit failure conditions, so optimization does not remove its checks. The finite campaign provides falsifiable supporting evidence; all-dimensional validity still rests on the proofs above.

## Reciprocal PDE check

I independently reviewed the potentially delicate high-frequency step at `manuscript/main.tex:808–828`, where the patterned reaction Jacobian is spatially varying. No missing assumption was found. On the fixed integrated-mass L2 space, the linearization has fixed Neumann H2 domain and positive diagonal diffusion. The small H2 branch is continuous in one dimension, so its reaction derivative is a uniformly bounded multiplication operator. The conservation identity preserves the integrated-mass constraint.

The diffusion part has real nonpositive quadratic form. Therefore the imaginary part of an eigenvalue is bounded by the multiplication-operator norm, while the real numerical-range upper bound is also uniform. Spectrum that could become critical lies in a fixed compact region. Compact resolvent and continuous resolvent perturbation then reduce persistence to finitely many isolated eigenvalues, rather than assuming that spatial Fourier modes remain uncoupled along the patterned branch. The isolated center sign and complementary gap, together with the one-dimensional H1-to-L2 smoothness of the quadratic reaction map, support the stated local nonlinear stability step.

## Reciprocal certificate finding: conflicting parameter fields change the identity

The certificate referee's data-only mutation adds `coefficient_in_U_ascending: ["1"]` to the 84-term spatial row with powers `[6,1,0]`, while retaining its correct `coefficient_in_A_ascending: ["8281/24300"]`. The exact readers use the A field. In contrast, `computation/generate_tables.py:69–75` prefers a U field whenever one is present, regardless of which table is being rendered. It therefore prints 1 for this row. After regenerating the table, the aggregate symbolic check accepts the disagreement; the certificate referee separately reproduced acceptance by the source and PDF audits.

I independently derived the defining polynomial

\[
E_{84}=(91/90)^2(1+Ax+z/3)|F(x+i\sqrt z,1+s)|^2
-|G(x+i\sqrt z,1+s)|^2
\]

directly from the printed boundary factors, without importing project code, and parsed all 84 rows from both the shipped and mutated TeX tables. The shipped table equals E84 exactly, while

\[
E_{\mathrm{mutant}}-E_{84}=\frac{16019}{24300}x^6z.
\]

The defining coefficient is 8281/24300. It can also be recovered without full expansion: the highest homogeneous part of F is lambda cubed, so the relevant degree-eight term comes only from `(91/90)^2(z/3)|lambda^3|^2`. This proves that the generated mutation is a false exact identity, rather than ignored metadata. The scripts and results are `check_conflicting_field_mathematics.py`, `CONFLICTING_FIELD_MATH_RESULTS.json`, and `conflicting_field_math.log`.

The current release's correct data and tables remain unaffected, and fixed immutable hashes contain post-release changes. The defect concerns accepting and regenerating a conflicting representation. The bounded remedy is to select the coefficient field and parameter explicitly per table, reject conflicting coefficient fields in the reader and generator, and retain the exact dual-field mutation as a regression test. A generator check against the mathematically defining table, in addition to freshness against the same generator, closes the demonstrated disagreement.

## Strongest conclusion and limitations

No new defect in the shipped mathematics, hidden assumption, or incorrect sharpness quantifier was found in this review scope. N1 is closed, and no revision of the main topology, theorem endpoint, exact diffusion law, or exponent claim is required. The separate conflicting-field generator repair above is independently confirmed. This report does not independently rerun every nonlinear coefficient certificate, every release build, or the literature-priority search; those are assigned to separate review families. It does not assert a global solution theory or a full characterization of the stable realization region, neither of which the paper claims.
