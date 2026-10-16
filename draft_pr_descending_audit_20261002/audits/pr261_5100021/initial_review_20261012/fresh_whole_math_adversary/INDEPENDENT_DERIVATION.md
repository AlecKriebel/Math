# Independent reconstruction and adversarial findings

Checkpoint: 2026-10-12 10:08 UTC. Completion estimate: 85%. This mathematical reconstruction was written before consulting submitted or current mathematical reviewer verdicts.

## 1. Exact hypothesis and geometry

The theorem actually stated in submitted PROOF.md assumes a noncircular ellipse, a strict nested nondegenerate confocal elliptical caustic, and **least primitive period N divisible by four**. The focus is a fixed original focus. The pedal uses original chord side lines. The antipedal uses consecutive intersections of lines through original vertices perpendicular to vertex-minus-focus vectors. Areas are cyclic signed shoelace areas, including stars and zero areas.

The mathematical claim survives this audit. The literal source-match claim requires a qualification discussed in section 9. This is a distinction of scope, not a counterexample to the mathematical theorem in section 1 of PROOF.md.

## 2. Global coverage, including primitive stars

Scale the caustic major semiaxis to one; its minor semiaxis is k'=sqrt(1-k²), where 0<k<1. Confocality gives a²-b²=k². Strict nesting gives b>k'. On (0,K), cn is strictly decreasing from 1 to 0, so there is a unique v with cn(v)=k'/b. With s=sn(v), c=cn(v), d=dn(v),

    d²/c² = (1-k²s²)/c² = k²+k'²/c² = k²+b² = a².

Thus the submitted coordinates a=d/c, b=k'/c are not a special geometric subfamily. Stachel's published Theorem 4.3(1), printed p.1614, parametrizes **all** billiards in this fixed ellipse with this caustic by

    P(u)=(-a sn(u), b cn(u)),   u -> u+2v.

The real map P covers the ellipse exactly once modulo 4K: its Jacobi amplitude is strictly increasing and the pair (sn,cn) is injective modulo 4K. Least period N therefore means N(2v)=4Kτ with gcd(N,τ)=1. Since 0<v<K, 0<τ<N/2. This covers every admitted positive primitive winding class, not just τ=1. The reverse billiard is obtained by reversing the ordering. No real phase is omitted.

Put N=2m and h=2K/m. For N divisible by four, m is even, τ is odd, and gcd(τ,m)=1. Since δ=2v=τh and mδ=2Kτ is 2K modulo 4K, the vertex sequence contains antipodal pairs. Reindexing makes either area δ-periodic. Reindexing by m makes either area 2K-periodic. Bezout's identity then makes it h-periodic. These facts hold for arbitrary primitive star winding.

## 3. Direct constructions, actual focus, and real finiteness

I independently verified the submitted antipedal coordinates against both line incidences by clearing rational denominators and reducing in the monic triangular quadratic relations

    C²=1-S², D²=1-k²S², d²=1-k²s², k'²=1-k², c²=1-s².

This does not import or execute submitted code. It verifies that the proposed point is on **both original antipedal lines**, rather than on a polar, an outer tangent line, or an inner contact construction. The same computation independently verifies

    det(P(x-v)-F, P(x+v)-F)
      = 2 k' s d D(1+kS)/(c L),  L=1-k²s²S².

For real x, c,s,d,k' are strictly positive, D>0, 1+kS>=1-k>0, and L>=1-k²s²>0. Every antipedal intersection is finite at every real phase. No signed-area assumption enters this calculation. The construction remains finite when the antipedal is self-intersecting or has zero area.

For the pedal, the chord is tangent to the caustic with normal n=(-S,C/k') and equation n·X=1. Direct orthogonal projection from F=(k,0) gives

    q(x)=((k-S)/(1-kS), k'C/(1-kS)).

The independent symbolic audit checks both coordinates and q_x²+q_y²=1. For real x, 1-kS>=1-k>0; there is no real singularity. The q points lie on the unit circle centered at the original center, but the projection is from the original focus. These conventions agree with the source's pedal and antipedal definitions.

## 4. Complete complex pole divisor for the antipedal

The antipedal coordinate denominators are c²L and k'c²L. The constants c,k' do not vanish in the admitted geometry. In the x-variable, only L=0 can create a nonremovable singularity away from Jacobi poles.

On the lattice 2K Z+2iK' Z, sn² has one double pole, hence degree two. The equation sn²=1/(k²s²) consequently has exactly two roots counted with multiplicity. The imaginary-shift identity sn(iK'+z)=1/(k sn z) locates them at iK'±v. They are distinct: 2v is strictly between 0 and 2K. They are simple because

    L'=-2k²s² S C D,

and at either root S=±1/(ks), C²=1-1/(k²s²)≠0, D²=1-1/s²≠0. None of these local conclusions divides by a possibly zero area coefficient.

At a common pole of sn and cn, the antipedal numerators have order at most two, and L has exact order two with nonzero leading coefficient. Hence the ratio is removable. There are no poles coming from the canceled focal factor 1+kS: substituting S=-1/k into L gives c²>0, and the final coordinate formula has no such factor in its denominator.

In original phase w, an antipedal vertex has x=w+v+jδ. The two pole equations become

    w=iK'-jδ,   w=iK'-(j+1)δ.

Modulo the reduced period lattice h Z+4iK' Z, these are precisely the two possible rows p=iK' and p+2iK'. Each coordinate has order at most one; therefore each shoelace summand and their finite sum have order at most two. This is the complete possible divisor, not a selection of prominent poles.

## 5. Multiple coincidences and N=4: cancellation without local genericity

At w=p, antipedal indices j in {N-1,0,m-1,m} can be singular. For N=4 this is every index and every cyclic area edge can contain two singular endpoints. A proof that ignores the closing edge or assumes two isolated singular pairs would fail here. The submitted global argument does not make either assumption.

Central inversion maps the + focus construction to the - focus construction, and the antipodal vertex pairing is a cyclic relabeling. Thus the two focal area functions agree. Reflection in the y axis maps u to -u, exchanges the foci, and reverses cyclic order. The reflection and reversal each change signed-area sign, so B(-w)=B(w). Reflection in the x axis is the Jacobi shift 2iK': sn stays fixed, cn changes sign. It fixes the + focus and retains index order, so B(w+2iK')=-B(w). These equalities extend meromorphically because orthogonal reflections preserve the bilinear complexified line equations.

At p=iK',

    B(p+z)=B(-p-z)=-B(p-z).

Therefore its Laurent germ is odd. As the independent divisor audit gives order at most two, its z^-2 coefficient vanishes. The same applies at both imaginary rows and every real translate. This is valid when all four N=4 antipedal vertices are singular at once. If a residue itself vanishes, B is removable there; the argument still works. No generic-residue or nonzero-area assumption is present.

## 6. Complete pedal divisor and incident-edge cancellation

Away from Jacobi poles, the pedal denominator can vanish only when sn x=1/k. On the sn lattice 4K Z+2iK' Z, sn has degree two. The critical point r=K+iK' realizes this value with multiplicity two and exhausts its inverse image on that lattice. At common sn/cn poles, q is removable, because its numerator and denominator have order at most one with nonzero leading denominator coefficient.

At r+z the quarter-shift formulas are

    sn(r+z)=dn(z)/(k cn(z)),
    cn(r+z)=-i k'/(k cn(z)).

Both are even functions of z. Direct expansion gives

    q(r+z) = (2/k)(1,i) z^-2 + O(1),

and its entire germ is even. This leading vector was independently checked symbolically.

For a fixed singular q vertex, its two neighbors q(r+z±δ) are regular: 0<δ<2K, so neither δ nor -δ is a real 4K period. Primitive indexing means no other q index is singular at the same full-orbit phase. In particular, the antipodal q point has sn=-1/k and is regular. The two incident area edges, including the cyclic closing edge, combine to

    (1/2) det(q(r+z), q(r+z+δ)-q(r+z-δ)).

Because q(r+t) is even, the second vector is odd and holomorphic:

    q(r+z+δ)-q(r+z-δ)=2z q'(r+δ)+O(z³).

An even order-two pole times this odd regular vector has order at most one. This remains true for N=4, where a neighbor is a removable common-Jacobi expression. If the resulting simple coefficient vanishes, the area is regular. Thus no hidden simple-pole division is needed.

As a contact-phase function, the pedal area has period h, imaginary antiperiod 2iK', and possible simple poles at r-jδ. These are exactly the possible poles of T(x+K), where T is the trace below. As an original-phase function, the corresponding trace is T(w+K+v).

## 7. Trace uniqueness and the complementary product

Define T(w)=sum_{j=0}^{N-1} dn(w+jδ). The correct Jacobi identities used here are dn(w+2K)=dn(w) and dn(w+2iK')=-dn(w). Near iK', dn(iK'+z)=-i cn(z)/sn(z), so the residue is -i. On the reduced h-by-4iK' torus, only indices 0 and m have a pole at w=iK': jδ is 0 modulo 2K iff jτ is 0 modulo m. Their residues have the **same** sign and sum to -2i. The other imaginary row has residue +2i. Thus T has exactly two simple poles, and T is nonzero. This is a general arithmetic proof; finite N sampling is not used.

If an h-periodic, 2iK'-antiperiodic meromorphic area has only these two possible simple poles, matching its residue at one pole with a scalar multiple of T cancels the second as well. The difference is holomorphic on the compact torus, hence constant; antiperiodicity forces the constant to be zero. The matching scalar may be zero. This yields

    B(w)=b_F T(w),
    A_F(w)=p_F T(w+K+v).

The only division is by T's known nonzero residue, not by a potentially vanishing B, p_F, b_F, or area.

Because K=(m/2)h and v=(τ/2)h, for m even and τ odd,

    K+v = (m+τ)h/2 = h/2 modulo h.

T is even by index reversal. At z0=h/2+iK' it is regular and

    T(z0)=T(-z0)=T(z0-h-2iK')=-T(z0),

so it vanishes there and at z0+2iK'. A nonzero meromorphic function on a compact torus has equal total zero and pole multiplicities. Since T has two simple poles, these two distinct zeros exhaust its divisor and are simple. Every pole of T(w) is canceled by a simple zero of T(w+h/2), and conversely. Therefore

    T(w) T(w+h/2)=constant.

It is strictly positive on the real line because every real dn term is positive. The claimed area product follows for every admitted phase and least primitive N divisible by four.

## 8. Positivity, zeros, stars, and limits

For real contact phase, q-F=(1-n·F)n/(n·n), with 1-n·F=1+k sn(x)>0. The normal angle is strictly increasing because det(n,n')=dn(x)/k'>0. Also n(x+2K)=-n(x). Thus a contact step 0<δ<2K rotates its outward normal through an angle strictly between zero and π, regardless of phase or primitive winding. Each cyclic determinant of q_i-F and q_{i+1}-F is positive. Translation leaves signed shoelace area unchanged, hence A_F>0. This also proves p_F>0 since the real trace is positive.

B=b_F T has a fixed sign, or is identically zero, on the whole real family. An isolated zero of B cannot occur under this theorem, but b_F=0 is permitted and produces an identically zero area product. The proof never divides by B or the product. Coincident antipedal vertices and self-intersections cause no defect; their shoelace terms are defined and finite.

The excluded limits are real domain boundaries, not missing admitted cases: k=0 is circular, k=1 degenerates the caustic, v=0 makes the ellipses coincide, and v=K corresponds to nonfinite outer semiaxes after normalization. For every fixed admitted parameter, all divisor-leading coefficients claimed nonzero above are indeed nonzero. A coefficient may approach zero in an excluded limit without invalidating the interior proof. Uniform estimates in those limits are not claimed.

Independent non-interval 115-digit stress checks include N=4,8,12,16,20,28,44; high primitive star windings 3/8,5/12,7/16,9/20,13/28,19/44; k=.001 and .9999; both focus symmetries; regular complex phases; and phases 10^-14 away from each pole row. Maximum scaled error in product/symmetry checks: 2.245432537e-69. Local zB converges while z²B tends to zero, including N=4. These diagnostics supplement the analytic proof and do not establish the universal result by sampling.

## 9. Source qualifier and exact repeated-orbit counterexample

Both original tables visually state k403,b, A_m A_m*, original foci, and N congruent to zero modulo four: arXiv v11 printed p.7, final paper printed p.348. The sources explicitly use signed polygon areas and warn that antipedals can self-intersect. Their constructions match the submitted original-side-line and original-vertex line constructions.

Neither table literally states **least period**, and a whole-text search of both source PDFs finds no explicit primitive, coprime, or least-period qualification. Context strongly supports an intended unrepeated winding-one family: the preliminaries say that N determines a distinct caustic parameter, and the experimental initialization places N vertices evenly around the ellipse. The submitted theorem extends to every primitive star winding. Nevertheless, the assertion in TARGET.json that both source editions *explicitly agree on least period* is stronger than the evidence. The original imported statement also says N-periodic without a literal least-period clause.

An exact independent counterexample shows why interpreting N-periodic as mere closure after N steps cannot be promoted unconditionally. For a=3,b=1, let λ=9/16, so the caustic semiaxes are 3sqrt(15)/4 and sqrt(7)/4. The focus is (2sqrt(2),0). Two positively ordered primitive six-orbits on this same ellipse/caustic are:

    V=( (3,0), (9/4,sqrt(7)/4), (-9/4,sqrt(7)/4),
        (-3,0), (-9/4,-sqrt(7)/4), (9/4,-sqrt(7)/4) ),

    W=( (0,1), (-3sqrt(15)/4,1/4), (-3sqrt(15)/4,-1/4),
        (0,-1), (3sqrt(15)/4,-1/4), (3sqrt(15)/4,1/4) ).

Direct exact computations verify all outer incidences, common-caustic tangencies, and specular reflections. All six vertices are distinct, so each orbit has least period six. Direct original chord projections and original antipedal line intersections give

| Phase | Pedal signed area | Antipedal signed area | Product |
|---|---:|---:|---:|
| V | 441sqrt(7)/128 | -6sqrt(7) | -9261/64 |
| W | 315sqrt(15)/128 | -30sqrt(15)/7 | -10125/64 |

Both focus constructions yield the same values. Listing V twice and W twice yields sequences closed after twelve steps. Each signed area doubles, giving products -9261/16 and -10125/16, whose difference is exactly 54. Thus a closure-only N=12 assertion is false.

This does **not** falsify the submitted least-primitive-period theorem; it validates the necessity of making the qualifier explicit. The source's intended minimal-period convention is a reasonable inference from its context, but must be labeled an inference. A scope statement should say: "We prove the primitive least-period formulation of source row k403,b, under the conventional unrepeated interpretation of N-periodic. A closure-only interpretation is false." If the repository requires the imported literal target to include every repeated N-step sequence, that target needs correction rather than a solved status under the stronger claim.

## 10. Strongest verified result and remaining gaps

**Verified mathematical result:** the complete theorem as explicitly stated in PROOF.md section 1 is established for all admitted parameters, all least primitive N divisible by four, both original foci, every real phase, and all admitted star windings. Its pole divisor, double-pole cancellation, torus uniqueness, complementary trace product, and real finiteness withstand the independent attack. No unsupported all-N numerical extrapolation or hidden division was found.

**Remaining scope issue:** the source-match prose and TARGET.json source_correction overstate literal primary-source evidence for the least-period qualifier. A documented conventional interpretation/correction is necessary before calling this an unqualified solution of the imported wording. The repeated-six-as-twelve counterexample is exact and reproducible.

**Not assessed:** novelty, priority, whether a later publication already proves this theorem, and publication readiness. No conclusion in this report establishes those matters.
