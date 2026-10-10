# Independent audit: EP-509 / problem 2150

## Verdict and scope

**ACCEPTED as a rigorous restricted-family result and a componentwise-route obstruction. The unrestricted problem remains unresolved.** No mathematical correction is required to the submitted proof.

The reviewed manuscript is *EP-509 / problem 2150: a bounded component-clustering attempt*, SHA-256 `4f26e97b47115cdc5037db91ab9f87ff6f3c9ae0b1ad4823b48319b576d26a6c`, 14,418 bytes. The frozen submission manifest is SHA-256 `3000e53e198c84b3ecf3000f155fbbb85925df4ba22bc27799c50978f788992d`, 9,571 bytes, listing 36 members. This audit assesses that exact text, not a later revision.

The full authored manuscript was read. The mathematical reasoning below was checked independently, without importing or executing the submission's checking programs. The result is an ordinary mathematical audit, not a proof-assistant formalization, an exhaustive novelty search, or a solution of the general conjecture.

## 1. Finite-component reduction and the exact endpoint

For a nonempty compact set K having finitely many connected components K_1,...,K_m, the claimed equality is

C(K) = min_P sum_{B in P} rad(union_{j in B} K_j),

where C is the infimum of the sum of radii over finite or countable closed-disk covers and P ranges over partitions of the component indices.

The finite-cover proof is valid. If two closed disks intersect and neither contains the other, let d be their center distance and r,s their radii. Their common containing disk with center on the line of centers has radius (d+r+s)/2 <= r+s. If one contains the other, keep the larger. This includes external tangency, internal tangency, and radius-zero disks. Each replacement reduces the number of disks, so repeated merging terminates even if newly created disks meet additional disks.

The surviving closed disks are pairwise disjoint. Because there are finitely many, they have positive pairwise separation. A connected subset of their union therefore lies wholly inside one disk. This supplies a genuine partition of the components; a surviving disk need not equal a component's circumdisk, but replacing it by the circumdisk of its assigned union can only lower the required sum. Empty assigned disks may be discarded. Conversely every component partition supplies a disk cover. Existence of each circumdisk follows from compactness and coercivity of the center objective, and the set of partitions is finite.

The countable-cover step does not assume a finite subcover by the original closed disks. Given total radius R < infinity, replace disk j by the open disk of radius r_j + epsilon 2^(-j), for j >= 1. These open disks cover K. Compactness supplies a finite subcover, whose corresponding closed disks cost at most R + epsilon. The finite partition minimum is consequently <= R + epsilon for every positive epsilon, hence <= R. Covers of infinite total radius cannot improve a finite candidate cover. This is the required direction; finite covers are already countable covers in the other direction.

It follows that the optimum is attained by at most m disks. For a fixed K, covers of cost 2 + epsilon for every epsilon > 0 do imply an attained cover of cost <= 2. The proof correctly does not infer this from one positive epsilon or from varying the underlying polynomial.

### Polynomial components and touching

For nonconstant p, each component U of {|p| < 1} is bounded. Every boundary point of U has |p| = 1: a boundary point with |p| < 1 has a connected small neighborhood inside the open sublevel set, placing it inside the same component, a contradiction. The minimum of |p| on the compact closure of U occurs at an interior point and is less than 1. If U contained no root, the minimum-modulus principle would be contradicted. Thus distinct open components contain distinct roots, giving at most deg(p) open components.

The open-mapping theorem shows {|p| <= 1} is the closure of {|p| < 1}. Since there are finitely many open components, this is a finite union of their connected compact closures. Some closures may touch and merge; that can only reduce the number of closed-region components. The partition proposition applies to the actual connected components of the closed region. There is no erroneous treatment of touching lobes as disjoint components.

## 2. Fractional-power disk mapping

The integral representation of w^alpha, 0 < alpha < 1, on Re(w) > 0 is valid. On compact subsets of this half-plane, its integrand is uniformly integrable near zero like t^(alpha-1) and near infinity like t^(alpha-2). The integral is holomorphic there and agrees on the positive axis with the principal power after a real change of variable. The identity theorem therefore applies on this connected half-plane.

Here is an independent algebraic check of the geometric ingredient. A disk with real diameter [ell,u] is described by

|w|^2 - (ell+u) Re(w) + ell*u <= 0.

For h(w) = w/(t+w), L = ell/(t+ell), and U = u/(t+u), direct expansion gives

|h(w)|^2 - (L+U) Re(h(w)) + L*U
= t^2 (|w|^2 - (ell+u) Re(w) + ell*u)
  / ((t+ell)(t+u)|t+w|^2).

For t > 0 and 0 < ell < u the factor multiplying the original disk inequality is positive. Thus h maps the entire closed input disk into the disk with diameter [L,U], including its boundary. Integrating the centered disk inequalities against the positive weight t^(alpha-1)/I_alpha gives the manuscript's fractional-power disk bound. The center and radius integrals converge individually; no conditional rearrangement is needed.

The boundary of the input disk stays strictly inside the right half-plane when ell > 0. Therefore neither the integral formula nor the principal branch encounters a cut or zero in the disconnected-family application. The optional ell = 0 extension is also valid: apply the positive-ell result to w+delta and the diameter [delta,u+delta], then let delta decrease to zero. The principal power is continuous on the closed right half-plane with its value at zero set to zero. Alpha = 1 is the identity map.

## 3. Regular-polygon lemma

The lower bound for any selected k >= 2 vertices of a regular n-gon of circumradius b is valid for every selection, consecutive or otherwise.

After setting b = 1, disks of radius rho >= 1 immediately satisfy rho >= k/n. For rho < 1, a disk meeting the unit circle has a nonzero center distance d and intersects the circle in an arc with half-angle theta satisfying

cos(theta) = (1+d^2-rho^2)/(2d) >= sqrt(1-rho^2).

This is exactly the nonnegativity of (d-sqrt(1-rho^2))^2. Hence the arc length in angular measure is at most 2 arcsin(rho), strictly less than pi. Any arc containing k distinct n-th roots of unity spans at least 2 pi (k-1)/n. Consequently

rho >= sin(pi(k-1)/n) >= 2(k-1)/n >= k/n.

The sine bound is the concavity chord on [0,pi/2]; its use is justified by the preceding arc-span bound. The case k=n, and specifically the antipodal n=k=2 case, cannot occur in the rho<1 branch and is already covered by rho>=1. Rotation and rescaling preserve the result.

## 4. Exact translated-binomial formula

Translation and rotation are isometries, reducing the problem to E(n,t) = {|z^n-t| <= 1}, t >= 0. The degree-one region is a unit disk and has content 1. All following family formulas and the corollary use n >= 2, as in the theorem.

For 0 <= t <= 1, E(n,t) is star-shaped at zero by the displayed convex-combination estimate. It lies in the radius-b disk, b=(t+1)^(1/n), and contains the full regular n-gon with vertices b*omega_j. For any proposed center w, averaging squared distances to these vertices gives b^2+|w|^2, so their circumradius is at least b. The connected-set partition formula therefore makes C(E(n,t))=b. This handles t=0 and the touching-lobe parameter t=1 directly.

For t>1, the base disk D(t,1) is disjoint from zero and the branch cut. The n maps omega_j w^(1/n) are continuous on the closed disk and analytic on a neighborhood. Each image is connected and compact. Two different images cannot intersect: taking n-th powers identifies their base points, after which equality of their nonzero branch values would force the same root of unity. Their finite disjoint compact union is the whole inverse image, so these are exactly its n components.

Set a=(t-1)^(1/n), b=(t+1)^(1/n), r=(b-a)/2, and s=(a+b)/2. The fractional-power lemma places component j in D(s*omega_j,r). The endpoints a*omega_j and b*omega_j belong to that component, so their distance b-a proves its circumradius is exactly r. This is a certified cover of every point of each closed component, not just boundary samples.

There are two explicit covers, with total radii b and n*r. To bound an arbitrary partition, write mu=min(r,b/n). A singleton block costs r >= mu. A block of size k>=2 contains k of the outer regular-polygon vertices, so it costs at least k*b/n >= k*mu. Summing over every block gives total cost >= n*mu = min(n*r,b). This simultaneously covers all block counts, all block sizes, asymmetric groupings, and mixtures of singleton and nonsingleton blocks. No symmetry assumption on an optimal cover is made.

Combining upper and lower bounds proves the exact stated formula, for finite and countable disk covers alike.

## 5. Worst parameter and explicit route obstruction

For t>1, b increases strictly and n(b-a)/2 decreases strictly, because 1/n-1<0. For n>2, immediately above t=1 the second expression exceeds the first; at large t it tends to zero while b diverges. Their unique crossing is determined by a/b=1-2/n. For n=2 the crossing is the endpoint t=1 and the separate-component expression is strictly smaller thereafter.

Writing q_n=(1-2/n)^n gives

t_n=(1+q_n)/(1-q_n),
M_n^n=2/(1-q_n).

The connected range increases to 2^(1/n), no larger than M_n. Since 0<=q_n<=1-2/n, one has M_n^n<=n<2^n. The maximum is attained and is strictly below 2 for every n>=2. The stated degree-three and degree-four values are exact.

For the quartic, t=65537/65536, a=1/16, and b^4=131073/65536. The lower comparison has numerator gap 131073-130321=752 over denominator 65536. The upper comparison with (6/5)^4 has cross-multiplied numerator gap

1296*65536 - 131073*625 = 3014031 > 0.

Thus 19/16 < b < 6/5. The exact separate-component cost is 2(b-1/16)>9/4, while b>1/8 ensures 2(b-1/16)>b and the optimal shared cover costs b<6/5. This is a valid counterexample to a componentwise-additive proof route and is not a counterexample to EP-509.

In the degree-n extension, a=1/16 and b=(2+16^(-n))^(1/n)>1. Each component's diameter is at least b-1/16>15/16, making separate total cost >15n/32. The common covering radius b tends to 1. Hence the multiplicative penalty for requiring separate covers is unbounded. Covering each connected component by several disks does not circumvent the obstruction, by Section 1.

## 6. Historical source and limits of the inference

The retained Pommerenke article was checked independently at printed pp.143 and 147-149, with visual inspection of those pages. Page 143 attributes a contour-length obstruction at 8.248 times capacity to earlier work. Pages 147-148 optimize the contour estimate at r=sqrt(e); p.149 applies a one-quarter length-to-radius factor and states the 2.59 bound. The manuscript's historical attribution matches these passages.

The underlying 1959 construction was not independently retrieved or reproved in this audit. The contour obstruction is accepted only as a report credited to Pommerenke. In particular, it obstructs the universal surrounding-contour-length target described there; it is not a direct disk-cover counterexample and does not exclude different geometric proof strategies. Sections 1-5 of the manuscript do not depend on that source claim.

Reference: Ch. Pommerenke, *Einige Sätze über die Kapazität ebener Mengen*, Mathematische Annalen 141 (1960), 143-152. https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0141/LOG_0031.pdf

The retained Erdős problem page was also visually checked for the original whole-region disk-cover statement and the historical 2.59/connected-case bounds. Reference: P. Erdős, *Some unsolved problems* (1961), printed p.246. https://users.renyi.hu/~p_erdos/1961-22.pdf

The supplied Hayman catalog alias is retained as an identifier; no fresh audit of the full Hayman book or exhaustive priority determination is claimed.

## 7. Acceptance boundaries

- Accepted: finite-component partition equality, countable-cover equivalence, attainment, fractional-power disk lemma, polygon lower bound, exact binomial-family formula, its attained worst parameter, and the separate-component obstruction.
- No proof correction is required. The corollary's n>=2 convention is inherited from its preceding theorem; degree one was explicitly handled separately.
- Unresolved: proving the partition minimum <=2 for every monic polynomial, or producing an unrestricted counterexample.
- No claim: novelty, a new general bound, a verified 1959 construction, a proof-assistant certificate, or complete lifetime attempt history.
- Supplementary exact checks test arithmetic and an algebraic identity. They do not replace the topological and analytic proofs.
- Source PDFs, scans, OCR, retained terms, and private checking records are excluded from publication. Only authored audit text and approved verification metadata are publication-eligible in content.

## Publication-edition scope

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI mathematical audit, without external human peer review, journal acceptance,
or proof-assistant certification. The complete original written mathematics
above is preserved without correction. It is independently checkable as prose,
including the analytic quartic construction and its exact comparisons.

Supplementary checking programs, scalar certificates, raw computational data,
and copied scholarly PDFs, scans, OCR, and source text are not included. The
supplementary computational runs cannot be replayed from this edition alone;
their hashes and aggregate results are verification metadata, not substitutes
for proof. The analytic and topological conclusions rest on the complete
written arguments. Source-inspection descriptions refer to the original
attempt and independent audit, with no new source inspection for this edition.
The 1959 construction is credited through Pommerenke's report and remains
unverified here. No novelty, priority, improved general bound, or unrestricted
solution is claimed.
