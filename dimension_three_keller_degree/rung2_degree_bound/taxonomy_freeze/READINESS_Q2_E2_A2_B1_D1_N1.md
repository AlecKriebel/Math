# Promotion readiness: `Q2-E2-A2-B1-D1-N1`

**Reviewed (UTC):** 2026-07-25T22:26:29Z.

**Verdict:** **NO-GO.  Do not promote this frozen row.**

**Correction (2026-07-25T23:08:00Z):** the three displayed
marked-\(h\) shapes below remain useful representatives, but the claimed
two-orbit companion split (15) is false.  Mixed projective companions need
not be removable by a pencil shear.  Consequently the “six missing
branches” language is retracted: the full stabilizer quotient of the
marked pencil together with
\([G]\in\mathbb P(\ell\langle h,s\rangle)\) must be frozen independently
before lower-identity exclusion resumes.

**Freeze addendum (2026-07-25T23:28:00Z):** that reconstruction is now
complete.  `FROZEN_Q2_E2_MARKED_COMPANION_v1.md` and
`FREEZE_CERTIFICATE_Q2_E2_MARKED_COMPANION_v1.md` freeze thirteen stable
strata with nonzero orbit space \(3+\mathbb P^1+3\).  This repairs the
internal denominator but does not change this report's NO-GO promotion
verdict.

The missing object is not merely a `C00`--`C44` wrapper.  The
hostile-audited top obstruction leaves a marked minimal quadratic pencil
\[
(\langle p,q\rangle,\ [h])
\]
in which the fixed divisor \(h\) is itself a pencil member and the pencil
has a unique double-line member \(s=\ell^2\).  The lower packages silently
replace the marked member \(h\) by \(s\).  They therefore cover only
\[
\boxed{h=s}
\]
and omit the genuine branches
\[
\boxed{h\ne s}.
\]

This is a scope gap in the assembled theorem, not a defect in any of the
hostile-certified lower calculations on their stated normal forms.
Exact top-identity points occur on the omitted locus, including one
already recorded in the audited top-obstruction note.

Accordingly, I did **not** draft a candidate promotion bridge or checker.
The route is not genuinely complete, which is the gate imposed for this
readiness audit.  No frozen status ledger, source proof, commit, or remote
state was changed.

This review was materially AI-assisted and is not peer review.  Exact
checks are evidence about the encoded algebra, not peer review.

## 1. What the frozen row gives uniformly

The frozen tuple is
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)
=(2,2,2,1,1,1).                                      \tag{1}
\]
The canonical-pencil theorem therefore gives an exact factorization
\[
H_4=h\,A(p,q),                                        \tag{2}
\]
where

- \(h\) is the component gcd and \(\deg h=2\);
- \(p,q\) are coprime degree-two forms and form the minimal pencil;
- \(A=(A_0,A_1,A_2)\) is a basepoint-free binary triple of degree one.

Write
\[
A(u,v)=a\,u+b\,v,\qquad a,b\in\mathbb C^3.
\]
Basepoint freeness makes \(a,b\) linearly independent.  Completing them
to a target basis and applying its inverse gives, pointwise,
\[
\boxed{H_4=(hp,hq,0)^T}.                              \tag{3}
\]
This is the exact leading normal form required by
`fixed_divisor_verticality/WORKING_FIXED_DIVISOR_VERTICALITY_PRINCIPLE.md`.
The construction uses target-rank minors, not a frozen coefficient
\(c_i\), and retains arbitrary \(H_3,H_2,L\).

For a deterministic future bridge, let \(v_1,v_2,v_3\in\mathbb C^{15}\)
be the coefficient vectors of the three components of \(H_4\).
Their span has dimension two.  On each frozen pivot stratum, choose the
lexicographically first nonzero \(2\times2\) coefficient minor
\[
\Delta_{rs;kl}
=(v_r)_k(v_s)_l-(v_r)_l(v_s)_k.                       \tag{4}
\]
The ordered charts
\[
\Delta_{rs;kl}\ne0,\qquad
\text{all earlier }\Delta=0
\]
are disjoint and exhaustive.  They provide an explicit invertible target
matrix taking two independent components to the first two rows and killing
the third.  Every denominator is a declared nonzero minor in (4); no
coefficient of a lower homogeneous term is used.

Thus the frozen-to-line-pencil normalization is available.  It is not the
reason for the no-go verdict.

## 2. All 45 frozen pivots

The frozen monomial order is
\[
\begin{split}
&(m_0,\ldots,m_{14})=(
x^4,x^3y,x^3z,x^2y^2,x^2yz,x^2z^2,xy^3,xy^2z,xyz^2,xz^3,\\
&\hspace{37mm}y^4,y^3z,y^2z^2,yz^3,z^4).
\end{split}                                           \tag{5}
\]

For `C00`--`C29`, an arbitrary point, if the stratum is nonempty, reaches
(3) by the uniform rank-minor construction.  It then reaches the
horizontal/all-vertical split, but its all-vertical \(h\ne s\) descendant
is not covered by the lower packages.  For `C30`--`C44`, the first two
target components are zero, so \(JH_4\) has at most one nonzero row and
rank at most one.  Those strata are empty inside the rank-two frozen row.

| Pivot | First allowed coefficient | Frozen-row status | Exact route/readiness |
|---|---|---|---|
| `C00` | \(H_{4,1}:x^4\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C01` | \(H_{4,1}:x^3y\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C02` | \(H_{4,1}:x^3z\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C03` | \(H_{4,1}:x^2y^2\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C04` | \(H_{4,1}:x^2yz\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C05` | \(H_{4,1}:x^2z^2\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C06` | \(H_{4,1}:xy^3\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C07` | \(H_{4,1}:xy^2z\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C08` | \(H_{4,1}:xyz^2\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C09` | \(H_{4,1}:xz^3\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C10` | \(H_{4,1}:y^4\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C11` | \(H_{4,1}:y^3z\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C12` | \(H_{4,1}:y^2z^2\) | nonempty at leading level; see (12) | blocked on \(h\ne s\) |
| `C13` | \(H_{4,1}:yz^3\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C14` | \(H_{4,1}:z^4\) | potentially nonempty | (3), then blocked on \(h\ne s\) |
| `C15` | \(H_{4,2}:x^4\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C16` | \(H_{4,2}:x^3y\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C17` | \(H_{4,2}:x^3z\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C18` | \(H_{4,2}:x^2y^2\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C19` | \(H_{4,2}:x^2yz\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C20` | \(H_{4,2}:x^2z^2\) | nonempty at leading level; see (13) | blocked on \(h\ne s\) |
| `C21` | \(H_{4,2}:xy^3\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C22` | \(H_{4,2}:xy^2z\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C23` | \(H_{4,2}:xyz^2\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C24` | \(H_{4,2}:xz^3\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C25` | \(H_{4,2}:y^4\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C26` | \(H_{4,2}:y^3z\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C27` | \(H_{4,2}:y^2z^2\) | nonempty at leading level; target shift of (12) | blocked on \(h\ne s\) |
| `C28` | \(H_{4,2}:yz^3\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C29` | \(H_{4,2}:z^4\) | potentially nonempty | permute target rows, use (3), then blocked |
| `C30` | \(H_{4,3}:x^4\) | empty | \(H_{4,1}=H_{4,2}=0\Rightarrow\operatorname{rank}JH_4\le1\) |
| `C31` | \(H_{4,3}:x^3y\) | empty | same rank contradiction |
| `C32` | \(H_{4,3}:x^3z\) | empty | same rank contradiction |
| `C33` | \(H_{4,3}:x^2y^2\) | empty | same rank contradiction |
| `C34` | \(H_{4,3}:x^2yz\) | empty | same rank contradiction |
| `C35` | \(H_{4,3}:x^2z^2\) | empty | same rank contradiction |
| `C36` | \(H_{4,3}:xy^3\) | empty | same rank contradiction |
| `C37` | \(H_{4,3}:xy^2z\) | empty | same rank contradiction |
| `C38` | \(H_{4,3}:xyz^2\) | empty | same rank contradiction |
| `C39` | \(H_{4,3}:xz^3\) | empty | same rank contradiction |
| `C40` | \(H_{4,3}:y^4\) | empty | same rank contradiction |
| `C41` | \(H_{4,3}:y^3z\) | empty | same rank contradiction |
| `C42` | \(H_{4,3}:y^2z^2\) | empty | same rank contradiction |
| `C43` | \(H_{4,3}:yz^3\) | empty | same rank contradiction |
| `C44` | \(H_{4,3}:z^4\) | empty | same rank contradiction |

The labels `C00`--`C29` do not themselves distinguish \(h=s\) from
\(h\ne s\).  Hence no coefficient-pivot routing can repair the missing
marked-member theorem.

## 3. The certified chain up to the gap

Starting from (3), factor \(h\) into primes.

1. If some prime component of \(h\) is horizontal for the minimal pencil,
   `fixed_divisor_verticality/WORKING_FIXED_DIVISOR_VERTICALITY_PRINCIPLE.md`
   applies.  Its independent hostile report is **PASS**.
2. If every prime is vertical, the exhaustive leading shapes are:

   - \(h\) irreducible and a member \(p=h\);
   - \(h=\ell^2,\ p=\ell m\), including \(m\sim\ell\);
   - \(h=\ell_1\ell_2\), with the two vertical components on the same or
     distinct pencil members.

3. `fixed_divisor_verticality/all_vertical_top_obstruction/NOTE.md` and
   its hostile **PASS** report exclude:

   - the genuine \(h=\ell^2,\ p=\ell m,\ m\not\sim\ell\) shape;
   - the distinct-member split shape;
   - \(p=h\) when the pencil has no double-line member.

   In each exclusion, \(G=(H_3)_3=0\), so the hostile-audited
   quadratic-component exit applies.

4. The exact remaining top frontier is
   \[
   \boxed{
   p=h,\qquad
   \langle p,q\rangle\text{ has a unique double member }s=\ell^2,
   \qquad
   G\in\ell\langle p,q\rangle.
   }                                                   \tag{6}
   \]
   The two unmarked pencil normal forms
   \[
   \langle s,r\rangle
   =\langle x^2,yz\rangle
   \quad\text{or}\quad
   \langle x^2,y^2+xz\rangle                           \tag{7}
   \]
   and their complete cubic kernels are hostile-certified.

Every step through (6) is supported by a retained hostile report.  The
coverage failure occurs only when (6) is transferred to the lower
packages.

## 4. Exact marked-member scope leak

In (6), \(p=h\) means that the fixed component gcd is the marked pencil
member \(h\).  In the proof of the top obstruction, the **different**
member \(s=\ell^2\) is then normalized to \(x^2\).

The lower row note begins instead with
\[
H_4=(p^2,pq,0),\qquad
p=x^2,\qquad
\langle p,q\rangle\in
\{\langle x^2,yz\rangle,\langle x^2,y^2+xz\rangle\}.
\tag{8}
\]
Thus its \(p\) is the double member \(s\), and its component gcd is
\(s=x^2\).  The notation \(p\) has been rebound:
\[
\boxed{
\text{top }p=h
\quad\not\Longrightarrow\quad
\text{lower }p=s=h.
}                                                       \tag{9}
\]

After putting the double member first, a general point of (6) has
\[
\boxed{
H_4=(hs,hr,0),\qquad
G=\ell(\alpha s+\beta r),
}                                                       \tag{10}
\]
not
\[
(s^2,sr,0).
\]
The latter is only the subcase \(h=s\).

This cannot be repaired by a target pencil shear.  The component gcd is
preserved up to a nonzero scalar by an invertible target change, and a
source linear change carries \(h\) to \(h\circ S\).  In particular the
rank and factorization type of the quadratic gcd are invariant.  A
rank-two or rank-three \(h\) cannot become the rank-one double line \(s\).

## 5. Exact omitted leading points

These are top-identity witnesses, not claimed Keller maps.  Their role is
to disprove the asserted coverage transfer.

### Audited-note witness: irreducible marked member

Take
\[
h=p=x^2+y^2+z^2,\qquad q=s=z^2,
\]
\[
H_4=(h^2,hs,0),\qquad
G=z^3\quad\text{or}\quad G=zh.                        \tag{11}
\]
Then:

- \(\gcd(H_{4,1},H_{4,2})=h\) has degree two and rank three;
- the generic pencil member
  \(h-ts=x^2+y^2+(1-t)z^2\) has determinant \(1-t\), so the pencil is
  minimal over \(\mathbb C(t)\);
- \(JH_4\) has generic rank two;
- \(\operatorname{Jac}(h^2,hs,G)=0\);
- \(h\ne s\), and rank invariance prevents reduction to (8);
- \(h^2\) has first frozen monomial \(x^4\), so this gives an omitted
  leading point in `C00`.

This is the witness explicitly recorded in the hostile-audited
all-vertical top-obstruction package.

### Rank-two pencil, reducible marked member

Take
\[
s=x^2,\qquad h=r=yz,
\]
\[
H_4=(h^2,hs,0)=(y^2z^2,x^2yz,0),\qquad
G=x^3\quad\text{or}\quad G=xh.                        \tag{12}
\]
The generic conic \(h-ts=yz-tx^2\) is smooth over
\(\mathbb C(t)\), so the pencil is minimal.  The gcd \(h=yz\) has rank
two and cannot become \(x^2\).  This point has frozen pivot `C12`;
placing a zero first target row gives pivot `C27`.

### Rank-one pencil, smooth marked member

Take
\[
s=x^2,\qquad h=r=y^2+xz,
\]
\[
H_4=(h^2,hs,0),\qquad
G=x^3\quad\text{or}\quad G=xh.                        \tag{13}
\]
The determinant of the generic conic \(h-ts\) is \(-1/4\), so the
pencil is minimal.  The gcd has rank three.  Since
\[
h^2=y^4+2xy^2z+x^2z^2,
\]
the point has pivot `C05`; placing a zero first target row gives `C20`.

Fresh exact expansion confirmed the gcds, generic rank two, the displayed
pivots, and both top Jacobian identities for (11)--(13).

## 6. The exact missing lower denominator

The marked member \(h\) must be classified under the stabilizer of the
unmarked pencil (7).

For
\[
\langle s,r\rangle=\langle x^2,yz\rangle,
\]
the pencil has three marked-member orbits:

1. \(h=s=x^2\), the double line;
2. \(h=r=yz\), the other singular, reducible member;
3. \(h=s+r=x^2+yz\), a smooth member.

The rank types distinguish the three.  Diagonal source scalings act
transitively on the nonzero smooth parameter, so no further smooth
modulus remains.

For
\[
\langle s,r\rangle=\langle x^2,y^2+xz\rangle,
\]
there are two marked-member orbits:

1. \(h=s=x^2\), the double line;
2. \(h=r=y^2+xz\), a smooth member.

The shear \(z\mapsto z+\lambda x\) fixes \(s\) and replaces
\(r\) by \(r+\lambda s\), proving transitivity on non-double members.

Only the first orbit in each list is covered by the existing lower
packages.  The three omitted marked-\(h\) orbits are
\[
\boxed{
\begin{aligned}
&\langle x^2,yz\rangle,\quad h=yz,\\
&\langle x^2,yz\rangle,\quad h=x^2+yz,\\
&\langle x^2,y^2+xz\rangle,\quad h=y^2+xz.
\end{aligned}}
\tag{14}
\]

For each marked orbit, \(G=0\) exits through the quadratic-component
theorem.  For \(G\ne0\), however, choosing a new pencil basis does not by
itself normalize the marked triple \((h,s,[G])\): returning the leading
form to \(H_4=(h^2,hs,0)\) restores the mixed coefficient.  For example,
\[
h=yz,\qquad s=x^2,\qquad
G=x(h+s)=xyz+x^3
\tag{15}
\]
satisfies the top identity, while the quadratic \(G/x=x^2+yz\) has rank
three and cannot be equivalent to either the rank-two form \(h\) or the
rank-one form \(s\) under a source transformation preserving the intrinsic
double line.  Thus the two pure companions on each displayed marked shape
are only computable slices.  Promotion first requires a complete
stabilizer-orbit or invariant-moduli description of all mixed companions.

## 7. Provenance ledger

| Input or claim | Actual certification status | Scope used here |
|---|---|---|
| `FROZEN_TAXONOMY_v1.md` | frozen and independently replayed | canonical inclusive row and 45 pivots only |
| frozen table label “excluded-audited” | **legacy historical label**, not a post-freeze certificate | not used as evidence |
| `CERTIFIED_EXCLUSION_STATUS.md` entry | correctly **provisional** | current authoritative promotion state |
| `fixed_divisor_verticality/WORKING_FIXED_DIVISOR_VERTICALITY_PRINCIPLE.md` | hostile **PASS** | all points with a horizontal prime component |
| `fixed_divisor_verticality/all_vertical_top_obstruction/NOTE.md` | hostile **PASS** | complete top obstruction and marked frontier (6) |
| quadratic-component exit | independently hostile-audited | every branch where \(G=0\) |
| `fixed_divisor_e2_quadratic_pencils/NOTE.md`, mixed sections | hostile **PASS** on the two displayed \(h=s\) mixed shapes | does not cover \(h\ne s\) |
| `ranktwo_triple/NOTE.md` | hostile **PASS** after three repaired rank drops | only \(H_4=(x^4,x^2yz,0),G=x^3\) |
| `rankone_triple/NOTE.md`, \(A=0\) | external hostile **PASS** after the \(a_3=0\) repair | only \(H_4=(x^4,x^2(y^2+xz),0),G=x^3\) |
| `rankone_triple/aopen_independent/` | exact independent PARI replay, accepted in the external full-coverage ledger | the \(A\ne0\) half of that same displayed shape |
| `rankone_triple/verify_all_strict.sh` | full strict replay **PASS** | assembles \(A=0\) and \(A\ne0\) only after \(h=s\) is assumed |
| main `fixed_divisor_e2_quadratic_pencils/NOTE.md` “complete row theorem” | **legacy provisional assembly claim** | its row-closure paragraph is not established |
| main `RESEARCH_LOG.md` “entire row closed” | historical progress claim, not independent evidence | overstates the combined scope |
| main `VERIFICATION.md` “complete row replay” | exact replay of four \(h=s\) companion packages | not a frozen-row or marked-member replay |
| `CANDIDATE_INCIDENCE_MANIFEST.md` eight-leaf list | obsolete pre-freeze proposal; known overlap in `RECONCILIATION.md` | cannot supply a bridge |
| standalone post-freeze assembly audit | **absent** | required after the marked-companion quotient is frozen and all resulting strata close |

All currently retained strict suites were replayed during this review:

- fixed-divisor verticality SymPy, PARI, and fail-closed runners;
- all-vertical top SymPy, PARI, dependency-free modulo-\(101\), and guards;
- mixed-companion SymPy, PARI, and mutation tests;
- rank-two triple SymPy, PARI, and mutation tests;
- the complete rank-one aggregate, including both independent PARI
  packages, external hostile replay, and all mutations.

Every suite passed.  Those passes validate the narrower certified scopes;
they do not repair (9).

## 8. Coverage and provenance gaps

The complete blocker list is:

1. **No retained post-freeze `C00`--`C44` bridge.**
   Section 1 supplies the needed leading normalization and Section 2 the
   pivot routing, but a promotion artifact was intentionally not drafted
   because the lower route fails.
2. **The legacy lower assembly loses the marked fixed member.**
   The transition from (6) to (8) identifies \(h\) with the unique double
   member without proof and is false for (11)--(13).
3. **The corrected thirteen-stratum internal denominator is not
   excluded.**
   The three marked pairs and their companion quotient are now frozen in
   `FROZEN_Q2_E2_MARKED_COMPANION_v1.md`, but the discrete open orbits and
   the parameterized `CTAU` stratum remain lower-identity targets.
4. **Every middle-family parameter survives through \(E_6\).**
   The endpoint and uniform exact calculations yield no exclusion at that
   stage; no complete \(E_5\) compatibility atlas exists.
5. **There is no independent full-row assembly audit.**
   Existing hostile reports stop at either the top frontier or one
   \(h=s\) normal form.
6. **The legacy row note and logs overstate their scope.**
   Their algebraic subtheorems are retained, but their “complete row”
   conclusion must be demoted until items 2--5 are resolved.
7. **The old eight-leaf incidence list cannot be reused.**
   It predates the frozen denominator, contains the documented
   `L02`/`L04` overlap, and does not provide a canonical marked-member
   proof or frozen-pivot routing.

There is no currently visible defect in the horizontal valuation theorem,
the all-vertical top theorem, or any of the four \(h=s\) lower
certificates.  The failure is precisely their union.

## 9. Promotion gate and next work

Promotion becomes eligible only after all of the following are present:

1. exact lower theorems covering all thirteen stable strata in
   `FROZEN_Q2_E2_MARKED_COMPANION_v1.md`, with a uniform homogeneous
   treatment of `CTAU` and every parameter divisor rebuilt;
2. two methodologically independent exact checks for each asserted
   terminal obstruction;
3. a post-freeze bridge that pins the frozen taxonomy and all lower inputs,
   enumerates `C00`--`C44`, uses ordered target-minor charts for
   `C00`--`C29`, and proves `C30`--`C44` empty;
4. a hostile assembly audit beginning from an arbitrary frozen-row point
   and independently recovering the marked-member classification;
5. only then, an update to `CERTIFIED_EXCLUSION_STATUS.md`.

The highest-information next experiment is the homogeneous middle family
\[
H_4=(h^2,hx^2,0),\qquad
h=x^2+yz,\qquad
(H_3)_3=x(uh+vx^2),                                  \tag{16}
\]
through the \(E_5\) compatibility ideal.  It must retain the frozen
boundaries \(u=0\), \(v=0\), and \(u+v=0\), and use division-free or
explicitly charted pivots.

Until (16), both discrete open-orbit strata, and all remaining frozen
boundaries are closed, the correct status is:
\[
\boxed{\texttt{Q2-E2-A2-B1-D1-N1}\text{ remains provisional}.}
\]
