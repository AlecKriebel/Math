# PR329 / problem20000450: independent arithmetic audit

Prepared2026-10-04T09:08Z, finalized2026-10-04T09:16:47Z; original source gate08:44:46Z and first candidate assessment08:51:56Z remain frozen. This is a verification of the released first substantive attempt, not a continuation of an unfinished proof search or a historical-priority certification. Arithmetic verification and evidence packaging complete; external root review/closure remain pending.

**Verdict: PASS for the stated characteristic-zero regular-pencil normalization and its full5-torsion arithmetic.** The central modular-cover dependency is verified directly from Fisher's primary article, with the exact labeled-point interpretation needed for smooth specializations. No arithmetic gap was found. This family does not certify the independent historical attribution, unnormalized/nonregular variants, a new Tate–Shafarevich class, publication clearance, or the whole project. The cubic-to-plane identification and exceptional geometric locus were read and their exact identities independently reproduced with the immutable candidate verifier; root separately adjudicates the full geometric proof.

## Exposure, target and scope

First read only original AIM Question17 and all four remarks on physical/printed51, in both extracted text and original render. The question asks for the5-torsion of a regular-pentagon quintic with five double points; it notes the five points at infinity, suggests torsor/modular and pencil interpretations, and asks about nonregular/starpentagon variants. It does not fix a field, origin or scale. The source-only gate records these distinctions and conditional arithmetic tests. A prospective cyclic-subgroup mechanism there was a test conditional on a stable line, not an extra requirement imposed on every possible answer.

After root acknowledged that gate, candidate exposure began2026-10-04T08:48:15.930236Z at frozen head96395a4f506af6a6045e3cd59afcba2db6b7e2e7. Read only the full permitted TURN_1.md, FINAL_RESULT.md, SOURCE_THEORY.md and verify_turn1.py. Froze the first candidate assessment and test/closure plan before primary Fisher reading, verifier execution, inherited reviewer/author verdicts, imported report, root baseline or sibling scientific material. Those inherited scientific verdicts remain unread. Root later supplied only an existing SymPy-runtime path; its dependencies were used without reading geometry scientific files. All writes stay in this arithmetic namespace. No Git/index/branch/PR/publication mutation, installation, outside-person contact or other-chat message occurred. All PR344 files are untouched by this agent.

The assessed curve has the candidate's specified rational origin O=[0:1:0] over K=Q(r), r²=5. Set

\[
\phi=(1+r)/2,\quad c=\phi^5=(11+5r)/2,\quad d=5+2r,\quad
\delta^2=d,\quad M=K(\delta),\quad L=K(\delta,\zeta_5).
\]

For a finite parameter lambda in K, remove exactly the candidate's nonelliptic-normalization values0,−5r,−c. For arithmetic on the cubic this is equivalently the smooth Tate parameter locus below. The cusp parameter −(25+10r)/4 of the plane model is retained: its normalization is still elliptic. Lambda=∞, characteristic5 and a=0 are excluded; no field/module statement is made for them. The claims tested are all25 geometric points, the actual torsion field and Galois module, split/nonsplit specializations, and rational torsion over K and M.

## Direct primary input and the formerly central gap

The operative primary reading is [Fisher, JEMS3(2001),169–201](https://ems.press/content/serial-article-files/31488): printed172–182 and194–195 read in full, with original renders172–173,179,194–195 inspected. Native extraction of191–195 was also captured, but the combined display of191–193 was partly truncated and those pages are not claimed as a complete additional reading. The Q-specific Selmer/rank statements are not used as the arithmetic theorem for K.

At printed172 Lemma1.1 gives the unique pointed Tate normal form and absence of pointed automorphisms for an order-five point. At printed179 §2.1 the full-level parameter represents triples(E,P,Q) with specified primitive Weil pairing; equation(14) acts by Q→Q+P and has quotient X1(5). Printed181–182 constructs the universal elliptic normal family and its explicit action. At printed194 Lemma3.4's proof gives the universal coordinate map to the marked Tate family. These are separate necessary inputs: the polynomial identity alone would not identify a torsion-point field. [Fisher's article](https://ems.press/content/serial-article-files/31488)

The division-polynomial and separability input was checked in [Sutherland's official Lecture5](https://math.mit.edu/classes/18.783/2023/LectureNotes5.pdf), operative pages10–14/§§5.5–5.6, including Theorems5.21 and5.25. The pairing input was checked in [official Lecture23](https://math.mit.edu/classes/18.783/2023/LectureNotes23.pdf), operative pages12–14 and original page13: Theorem23.29 and Corollaries23.30–31 supply nondegeneracy, Galois equivariance and the full-torsion root-of-unity consequence. The notes explicitly refer the standard nondegeneracy proof to cited references; those reference books/papers were not separately read here. No new claim depends on treating that standard theorem as an independently novel proof. Native direct retrieval succeeded for all three primary PDFs; the browser tool's earlier Lecture5 open failed, but the native PDF access and operative reading succeeded.

## Actual finite étale fibers, including specializations

Write

\[
\beta=\frac{(11-5r)\lambda}{2(\lambda+5r)},\qquad
D_\beta:y^2+(1-\beta)xy-\beta y=x^3-\beta x^2,
\quad P=(0,0).
\]

The discriminant is beta⁵(beta²−11beta−1). Its four projective cusps are0,∞,c,−1/c, since c−1/c=11. The fractional linear beta(lambda) maps lambda=0,−5r,−c,∞ to those four values respectively. Thus every retained finite lambda is a smooth Tate fiber; there is no extra excluded value hidden in a denominator or j=0/1728.

Over a field containing zeta, the complement set

\[
\mathcal T_\beta=\{Q\in D_\beta[5]:e_5(P,Q)=\zeta\}
\]

contains five distinct points Q+jP. Each is independent of P and determines all25 points. Conversely a labeled torsion basis determines its unique cover point. On the smooth family, [5] is finite of degree25 and has invertible differential5; its kernel is finite étale. The pairing fiber is therefore a finite étale degree-five torsor. An automorphism fixing P is the identity, so there is no quotient ambiguity that could reduce the coordinate field. These statements hold on each smooth fiber, including split fibers and extra-j-automorphism fibers, not merely in the generic function field.

Let

\[
f(t)=t^4+3t^3+4t^2+2t+1,\quad
g(t)=t^4-2t^3+4t^2-3t+1,\quad
\epsilon(t)=\frac{\phi t+1}{t-\phi},\quad
\iota(v)=\frac{cv+1}{v-c}.
\]

The primary universal family identifies this labeled cover by beta=t f(t)/g(t). Both epsilon and iota are involutions and

\[
\iota(\epsilon(t)^5)=t f(t)/g(t),\qquad
\iota(\beta(\lambda))=-\frac1{\lambda+c}.
\]

This was independently checked as an identity in a free beta coefficient over Q(r), rather than interpolation: with N=(phi t+1)⁵, D=(t−phi)⁵ and s=−(c²+1),

\[
(\beta-c)N-(\beta c+1)D=s(t f-\beta g).
\]

Thus the entire projective finite fiber, after the invertible change u=epsilon(t), is

\[
u^5=-1/a,\qquad a=\lambda+c\ne0.
\]

The derivative5u⁴ never vanishes there. Its projective branch values correspond only to beta=−1/c,c, already excluded cusps. Potential t=∞ maps to beta=∞, another excluded cusp; the t=phi pole maps to beta=c. No specialization loses a smooth cover point through these charts. Therefore the labeled finite étale fiber algebra and the torsion-complement field agree on all retained specializations. This is the check that closes the first assessment's central gap; it was not inferred from a generic polynomial splitting field alone.

If theta⁵=a then u=−1/theta is a root. Over a field containing zeta, the splitting field of this torsor is exactly the field obtained by adjoining theta, including when a is already a fifth power. Since P is rational on D_beta, adjoining one Q suffices for the entire basis and its25 linear combinations. Consequently

\[
L(D_\beta[5])=L(\theta).
\]

Precision about the extension class: in the displayed coordinate it is [−1/a] in L*/L*⁵. Since −1=(−1)⁵, this equals [a]⁻¹. It has the same generated Kummer field and the same split criterion as [a], but is not the same literal element of the fixed cohomology group unless the class is trivial (or one explicitly inverts the generator identification). The candidate expressly says “after inversion”; that is correct for its field/basis statement. It must not be read as an equality of two fixed-generator nontrivial classes.

## Quadratic twist, lower inclusions and exact division field

The candidate gives an actual isomorphism, not just a matching j-invariant. With k=4(lambda+5r)/r and q=dk²,

\[
\xi=q(x-\beta),\qquad
\eta=(k\delta)^3\bigl(y+((1-\beta)x-\beta)/2\bigr).
\]

Its exact polynomial identity was reproduced unchanged by native018. Replacing delta by−delta negates the elliptic point. Hence the cubic is the d-twist of the Tate curve, the isomorphism is valid on every retained fiber, and

\[
L(E_\lambda[5])=L(\theta).
\]

It remains essential to remove the artificially prefixed L. At infinity the original normalized homogeneous polynomial is2X(X⁴−10X²Y²+5Y⁴), giving O and four points with slopes±sqrt(5+2r),±sqrt(5−2r). Their complete field is M: sqrt(5−2r)=r/delta. The roots are distinct and the infinity points are smooth. Rotation72° preserves the explicit regular pencil and cycles these five points. The origin-fixing part of an automorphism of order5 is trivial in characteristic0: after a short Weierstrass form it scales(x,y) by(u²,u³), where nonsingularity forces the scaling order to divide4 or6. A homomorphic image of a group of order5 cannot have such nontrivial order. The rotation is therefore translation by an exact order-five point. Its infinity orbit is the order-five subgroup. Thus the actual full torsion field contains delta. Nondegeneracy and Galois equivariance of the Weil pairing imply that it also contains zeta. [Sutherland, Theorem23.29 and Corollary23.30](https://math.mit.edu/classes/18.783/2023/LectureNotes23.pdf)

Combining those lower inclusions with the torsor and twist upper inclusion proves the exact equality

\[
\boxed{K(E_\lambda[5])=K(\delta,\zeta_5,\theta),\qquad\theta^5=\lambda+c.}
\]

This proof uses actual points and a labeled finite étale fiber. Counting x-roots alone, knowing the two composition factors, or specializing a generic degree would not supply either inclusion.

## Fifth-power descent, degrees and Galois group

The rational norm of d is5. If d were a square in K, its norm would be a rational square, a contradiction. Hence M/K is quadratic and real. K is the real quadratic subfield of Q(zeta5), so K(zeta5)/K is imaginary quadratic and is distinct from M. Therefore L/K is biquadratic of degree4.

For a in K*, a fifth power in L already was a fifth power in K. Indeed u⁵=a in L gives N_{L/K}(u)⁵=a⁴, and

\[
\left(a/N_{L/K}(u)\right)^5=a.
\]

This does not assume u generates L or use an incorrect degree2 norm. Conversely a fifth power in K is one in L. Over L, which contains zeta, the root-extension Galois group of x⁵−a embeds in the cyclic group of order5; it is trivial precisely when a has a fifth root in L, and otherwise has degree5. Thus the degree is4 or20 precisely according to the stated K-fifth-power criterion.

For a not a fifth power choose its real fifth root theta. N=K(zeta,theta) has degree10 over K; its order-five subgroup multiplies theta by zeta and complex conjugation fixes theta, inverts zeta and inverts that subgroup. Hence Gal(N/K)=D10 (order10). Its unique quadratic subfield is K(zeta), by the unique index-two subgroup of D10. Therefore N and M are disjoint over K and the full group is D10×C2. In the split case the full group is C2×C2. Over K(lambda) the valuation of a at lambda=−c is1, so a is not a fifth power and the generic degree is20. This divisor argument proves the generic claim; the fiberwise proof above separately proves all specialized claims.

Concrete number-field split fibers include a=1,32,r⁵=25r; their corresponding finite lambda=a−c are smooth. Concrete nonsplit fibers include a=2 and a=r: their norms4 and−5 have prime valuations incompatible with a rational fifth power, so a cannot be a fifth power in K. These illustrate the descent boundary without pretending that finite-field tests establish number-field irreducibility.

## The full module, extension and rational torsion

Let psi be the quadratic character of M/K and chi the mod-five cyclotomic character. The infinity line has character psi. The pairing forces the quotient character chi/psi=chi psi. Thus the composition factors are

\[
0\longrightarrow\mathbf F_5(\psi)\longrightarrow E[5]
\longrightarrow\mathbf F_5(\chi\psi)\longrightarrow0.
\]

For an upper-triangular representation with diagonal entries psi and chi psi, the normalized off-diagonal cocycle takes values in the character ratio chi⁻¹. Accordingly the extension lies in H¹(K,F5(chi⁻¹)); the quadratic twist cancels in this ratio. After restricting to L both diagonal characters are trivial and the labeled complement torsor gives the Kummer class above. Composition factors alone leave this class undetermined; the universal torsor is the materially additional input.

In the nonsplit case a suitable basis and choices of generators give

\[
S=-I,\qquad V=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad
U=\begin{pmatrix}1&1\\0&1\end{pmatrix}.
\]

Here S changes delta and fixes N, V is complex conjugation, and U generates the Kummer subgroup. S is justified by disjointness and the actual twist isomorphism. Complex conjugation fixes the marked line, has determinant−1 and is an involution; replacing the second vector by a multiple of the first makes it anti-invariant, since2 is invertible mod5. The nontrivial Kummer action fixes P and the pairing quotient; it is a nonzero transvection, whose generator can be scaled to U. They satisfy S central, VUV=U⁻¹ and generate20 matrices. In the split case omit U and obtain four matrices. The determinant is chi in both cases. These matrices are a normalized description of the actual module, not an extra arbitrary assumption.

The presence of S=−I kills every nonzero K-fixed vector, even in split fibers. Over M, the remaining V (and U in nonsplit fibers) fix exactly the first line, giving E(M)[5]=C5. Equivalently the real-field pairing determinant bounds real5-torsion by five points and the infinity subgroup attains it. The module therefore supports both rational-torsion assertions in every retained specialized case.

Splitting the extension after trivializing its characters is not the same as full rationality over K, or even over M. The degree-four split fibers still require both delta and zeta for all25 points. This distinction survived direct negative tests.

## Reproduction and adversarial controls

Native018 executes the original immutable verify_turn1.py with the approved existing Python3.14.6/SymPy1.14.0 runtime. It exactly reproduces88,918 assertions,388 smooth finite-field fibers,30,012 affine points,28,460 inverse-plane checks,68 full-torsion and320 cyclic-torsion fibers. The two initial available runtimes genuinely failed for missing SymPy (native013/014); these failures are preserved, not relabeled mathematical failures. No installation occurred.

The independently written check_arithmetic.py uses only the Python standard library. Native019 passes5,432 exact checks on1,364 smooth fibers over nine primes19,29,31,59,71,79,109,131,181 and both embeddings of r, with306,424 enumerated affine points and1,364 cover fibers. It verifies a free-beta polynomial identity over Q(r), split specializations and norm powers, faithful matrix groups and fixed subspaces. Its group-law enumeration acts directly on the completed-square Tate cubic and the d-twist, with no candidate R_beta polynomial, candidate inverse-plane formula or SymPy dependence. This exercises nonsquare-twist and missing-root-of-unity cases absent from the candidate verifier.

Six character/splitting categories were exercised. In characteristic p with p≡1 mod5, the untwisted rational5-torsion has25 or5 points according to the radical; a nonsquare d-twist instead has only the identity. For p≡−1 mod5, both twist choices have exactly five rational5-torsion points, although the defined-over-K polynomial cover has a rational parameter: the fixed-pairing interpretation requires zeta in the ground field. This is a falsifiable guard against a misapplied specialization rule.

| Deliberate mutant | Actual native failure | Implication |
|---|---|---|
| Omit quadratic twist | native020, p31/r6/lambda2, exit1 | Tate curve has5 rational points but the twist has1 |
| Replace a=lambda+c by lambda | native021, p181/r27/lambda1, exit1 | Wrong fifth-power class predicts25 instead of5 |
| Omit cyclotomic condition | native022, p19/r9/lambda1, exit1 | Rational cover parameter cannot supply25 points without zeta |
| Use degree2 norm | native023, exact norm descent, exit1 | The degree-four exponent is essential |

Full stdout/stderr, actual exits, actual argv/clean environment/cwd, UTC start/end and unchanged pinned-input checks are retained in each named native execution. The later replay driver additionally checks full stored dependency bindings before/after reproducing the six mathematical streams. Finite-field evidence supplements the proof; no finite sample or assertion count is used to infer the number-field theorem.

## Exact remaining gap and closure boundary

No unresolved arithmetic mechanism remains within this normalized characteristic-zero scope. The report's strongest result is the checkable proof of the fiberwise field/module/splitting/rationality claims together with independent exact falsification controls. Historical novelty, generalized pentagons, twists without the chosen rational origin and arithmetic claims about Sha are outside the candidate's stated result and outside this verdict. The source did not prescribe a field or normalization; accepting this explicit convention as the intended problem answer is a root/user scope judgment, not hidden arithmetic descent.

The full local verify_readonly.py requires raw private original-source PDF/render bindings, these directly retrieved primary PDFs, the frozen four-file candidate, the approved runtime dependencies and the complete native evidence. It is not a public verification-package default. The mathematical check_arithmetic.py is a portable self-contained control in form; no public release is authorized. Manifest preparation records are internally assembled packaging records, not independent native evidence of their own process exit.

Final report/code/source bindings/manifest/closure plan must be read in full and independently replayed/adjudicated by root before one-time external closure. This namespace remains unsealed. This agent will not run a sealer or write after root's closure. No closure conveys priority/publication approval or authority for shared Git/index/PR mutations.
