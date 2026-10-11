# Independent primary-source consequence audit: Silverman (1995)

**Verdict: PASS.** Silverman's exact printed cubic already supplies an algebraic postcritically finite dynamical conjugacy class with absolute field of moduli **Q** and **no real model**. Consequently its field of moduli is not a field of definition. More generally, every member of his printed class

\[
\phi_d(z)=i\left(\frac{z-1}{z+1}\right)^d,\qquad d\ge3\text{ odd},
\]

has these properties. This is an independently verified consequence of an old printed construction, with **0 new candidate attempts**.

## Scope and evidence gate

The required first source read was the literal live AIM URL `http://aimpl.org/finitedynamics/2/`. Its current Problem 2.6 asks, "Are all PCF maps defined over their field of moduli?" A direct HTTP retrieval succeeded after the web fetch timed out. The HTML is retained locally as `tmp/live_aim_moduli.html` in ignored temporary storage.

Primary source: Joseph H. Silverman, *The field of definition for dynamical systems on P1*, Compositio Mathematica **98** (1995), 269-304, [primary archive](https://www.numdam.org/item/CM_1995__98_3_269_0/). The independently downloaded PDF at [the primary PDF URL](https://www.numdam.org/item/CM_1995__98_3_269_0.pdf) is byte-identical to the supplied parent copy:

`0a405ab1fbe4fc04e73439ecc31db4afaae3d8e38ce58bfd49f65442c6e88116`.

The independent PDF is retained locally at `tmp/silverman_1995_independently_retrieved.pdf`; extracted source text and rendered pages are at `tmp/pdfs/`. All foreign source content is excluded from the authored publication manifest. `reading_ledger.json` records paths, source URLs, source hashes, visual-inspection locators and the confirmed ignore rule. The scientific proof is unchanged by this retention correction. The initial proof seal remains a historical authored record at `historical_seals/20261002T064712Z_proof_seal.json`; the complete initial closure snapshot is retained in ignored `tmp/historical_initial_closure/`.

Before writing any audit conclusion, I rendered and visually inspected printed p. 271, Eq. (1), and printed pp. 295-298 (PDF pages 4, 28-31), reading the operative arguments. The cubic occurs at Eq. (1); the general odd-degree class occurs in the example on p. 296. The source discusses its descent obstruction. The PCF proof below was reconstructed directly, without assuming PCF from the source or another audit. No original PR36 report or other priority opinion was read before this proof was sealed.

## Exact claim and definitions

Maps are compared by dynamical conjugacy under `PGL_2`, so `phi^h=h^{-1} phi h`. A model over a field K means a conjugate rational map with coefficients in K. The holomorphic centralizer here means `Aut(phi)={h in PGL_2(C): h phi=phi h}`, not the much larger semigroup of all rational maps commuting with phi. PCF means every critical point has finite forward orbit. The absolute arithmetic field of moduli is the fixed field of the subgroup of `Gal(Qbar/Q)` preserving the dynamical conjugacy class.

All claims below are deductions in characteristic zero. The only scope restrictions are `d>=3` and d odd; even degrees and degree one are deliberately excluded. No numerical approximation is part of the proof.

## Proof: degree, critical points and finite orbits

In homogeneous coordinates the map is

\[
F_d[X:Y]=[i(X-Y)^d:(X+Y)^d].
\]

Its two coordinate polynomials have no common projective zero: `X-Y=X+Y=0` implies `X=Y=0`. Thus its degree is exactly d, and its coefficients lie in Q(i).

Write `P=i(z-1)^d` and `Q=(z+1)^d`. Direct differentiation gives

\[
P'Q-PQ'=2id(z-1)^{d-1}(z+1)^{d-1}.
\]

Equivalently, the map is the composition of the Mobius map `T(z)=(z-1)/(z+1)`, the power map `w->w^d`, and multiplication by i. Its only critical points are `1` and `-1`, each of ramification multiplicity `d-1`; the latter is a pole of order d. Infinity is not critical: in the local coordinate `u=1/z`, the map is `i((1-u)/(1+u))^d`, whose derivative at `u=0` is `-2id`, nonzero. The critical multiplicities sum to `2d-2`, as required.

For odd d,

\[
\phi_d(1)=0,\quad \phi_d(0)=-i,\quad
\phi_d(-1)=\infty,\quad \phi_d(\infty)=i,
\]

and `T(i)=i`, `T(-i)=-i`. Hence:

- If `d=3 mod 4`, the distinct six points form the cycle
  `1 -> 0 -> -i -> -1 -> infinity -> i -> 1`.
- If `d=1 mod 4` and `d>=5`, there are two distinct three-cycles
  `1 -> 0 -> -i -> 1` and `-1 -> infinity -> i -> -1`.

Both critical points are periodic in every allowed degree. Therefore phi_d is PCF, indeed all its critical points are periodic. For the exact cubic printed in Eq. (1), both lie in the same six-cycle. This checks the previously unassumed PCF hypothesis directly.

## Proof: trivial holomorphic centralizer

Suppose `h phi_d=phi_d h`. A commuting Mobius map preserves local ramification, so h permutes the two critical points `{1,-1}`. Commutation then forces it to permute their respective images `{0,infinity}` in the same way.

If h fixes the critical points individually, it fixes 1, -1, 0 and infinity; a Mobius map fixing three distinct points is the identity.

If h swaps 1 and -1, it swaps 0 and infinity. The latter condition gives `h(z)=a/z`, and `h(1)=-1` gives `a=-1`. Thus the only possible nonidentity map is `g(z)=-1/z`. But

\[
T(g(z))=-T(z)^{-1},\qquad
\phi_d(g(z))=-iT(z)^{-d},\qquad
g(\phi_d(z))=iT(z)^{-d}.
\]

The two rational maps are distinct in characteristic zero. Hence `Aut(phi_d)={1}`. The argument does not assume a classification of finite Mobius groups or the correctness of the source's stabilizer assertion.

## Proof: field of moduli exactly Q

Let the bar denote conjugation of coefficients. The same computation, using `g^{-1}=g`, gives

\[
g^{-1}\phi_d g=-iT(z)^d=\overline{\phi_d}(z).
\]

Every `sigma in Gal(Qbar/Q)` sends i to i or -i. In the first case it fixes the printed map; in the second it sends it to its conjugate under g. Thus every sigma preserves its dynamical conjugacy class. Its absolute arithmetic field of moduli is the fixed field of the full group, which is Q. In particular the field of moduli lies in R. A conjugator exists over Q for the nontrivial automorphism of Q(i)/Q; no unproved rationality assertion about a moduli space is required.

This field-of-moduli calculation is intentionally separated from field of definition. An individual conjugacy witnessing Galois invariance need not satisfy the descent condition for a real model.

## Proof: no real model

Let `C(z)=conjugate(z)` and define the antiholomorphic Mobius involution

\[
J=gC,\qquad J(z)=-1/\overline z.
\]

The coefficient-conjugacy relation above, or direct substitution, gives `J phi_d=phi_d J`. Also `J^2=1`. It has no fixed point: a finite nonzero fixed point would satisfy `|z|^2=-1`, while it swaps 0 and infinity.

Any other antiholomorphic Mobius map A commuting with phi_d would give a holomorphic commuting map `A J^{-1}`. Triviality of the holomorphic centralizer therefore forces `A=J`.

If a real model existed, write `psi=h^{-1} phi_d h` with real coefficients and `h in PGL_2(C)`. Ordinary conjugation C commutes with psi, so `R=h C h^{-1}` would be an antiholomorphic involution commuting with phi_d. It has fixed points: for example `h(0)` is fixed. But uniqueness forces `R=J`, whose fixed set is empty. Contradiction.

Thus no real model exists, even allowing conjugacy over all of C. In particular no Q-model exists, so its absolute field of moduli Q is not a field of definition. More generally no subfield of R is a field of definition.

## Actual executed checks and adversarial controls

`python3 exact_checks.py` uses exact pairs of Python `Fraction`s for Q(i), homogeneous orbit evaluation including infinity, and exact coefficient-array multiplication for rational-map equality. It uses no floating point arithmetic. The final execution completed with exit code 0 and `status: PASS`, recorded in `exact_checks_output.json`.

The execution checked d=3,5,7,9: complete critical orbit cycles, derivative numerator and the nonzero infinity derivative, coefficient conjugacy, failure of g to commute holomorphically, and success of J to commute antiholomorphically. For d=3 the holomorphic-commutation cross-product residual is exactly `2(z^2-1)^3`, nonzero. Finite degree samples check the implementation; the equations and parity argument above prove the general claim.

Controls and mutants actually executed:

- **Even degree d=2:** g commutes holomorphically; the asserted coefficient conjugacy and J commutation fail. This catches a parity-blind extension of the proof.
- **Degree d=1:** the degree-at-least-two condition fails and the alleged critical multiplicities are zero. The centralizer proof cannot be applied in degree one.
- **Real phase control `((z-1)/(z+1))^3`:** it is a real PCF map with a four-cycle through the two critical points. Both g and J commute, as does ordinary conjugation. This proves that a fixed-point-free commuting antiholomorphic involution alone does not obstruct a real model; the trivial-centralizer step is essential.
- **Wrong-sign six-cycle mutant:** the erroneous sequence placing i immediately after 0 is rejected by exact equality.

Two preliminary runs failed due to incorrectly specified expectations for the real phase control. Those expectations were corrected after exact computation showed the extra symmetry. The research log records both failures; neither is represented as passing evidence.

## Strongest priority consequence and precise limitations

The old primary source contains the exact cubic, and independent elementary calculations verify the missing PCF property. Therefore a negative answer to the literal AIM Problem 2.6 is already obtainable from Silverman's 1995 printed example. Any proposed contribution consisting only of existence of an algebraic PCF class with real field of moduli and no real model cannot be promoted as a new existence result in light of this source.

This audit does **not** claim that Silverman explicitly described the map as PCF on the inspected pages, that the PCF consequence was previously emphasized in the literature, or that this is the earliest example worldwide. It does not establish acceptance, author intent, an exhaustive priority history, or any claim about an unread PR36 manuscript beyond that existence-level obstruction. No original PR36 report or other priority opinion was used. Independent comparison with an actual new theorem would need its exact statement. No proposed repair or new route was pursued here.

The field-of-moduli claim is about unmarked dynamical conjugacy classes; markings can change both the stabilizer and the field of moduli. Degree one, even degrees, and arbitrary changes of coefficient phase are not covered by the theorem proved above.

