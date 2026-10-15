# Independent initial reconstruction: PR 445 / 30002737

Reviewer: whole_math_adversary2. Frozen head: `3242c84e06db7e99012c7fe581adde5c3f89fc89`.

This checkpoint was written after reading all twelve frozen candidate files, and independently obtaining and inspecting the indicated primary PDF pages. No current root notes, current reviewer reports, peer packets, or repair code have been opened. The frozen package's old independent audit is one of the twelve required candidate artifacts; its conclusion has not been treated as independent evidence. This is a reconstruction before exposure to a completed integrated repair, not an acceptance verdict on that repair.

## Original target and precise theorem

OWR 53/2014, PDF pages 10–11 (printed 2996–2997), places Conjecture 1 in van Enter's contribution. It asserts the implication from absence of an absolutely continuous diffraction component to absence of an absolutely continuous dynamical component. The surrounding discussion involves translation bounded Dirac combs and the unitary translation action in the invariant L2 space. There is no dimension-one condition in that conjecture or its preceding paragraph. The subsequently numbered Gibbs conjectures impose dimensional conditions on different assertions. In the precursor arXiv:1310.0267v2, pages 2–3, the configuration domain is explicitly Z^d and the Fourier measures live on R^d or d-dimensional tori. The precursor poses the same spectral absence question. The unrestricted planar interpretation is therefore defensible from direct primary context. This is not a proof of the originator's unprinted intent or any present-day novelty/priority claim.

The candidate's exact mathematical assertion is existence of a deterministic unweighted, aperiodic, repetitive FLC Meyer set Lambda in R^2, with a uniquely ergodic full R^2 translation hull, such that its physical diffraction is singular relative to two-dimensional Haar measure but some bounded L2 hull observable has nonzero spectral measure equivalent to two-dimensional Lebesgue measure. A one-dimensional restriction, purely absolutely continuous full representation, and spectral multiplicity are outside that assertion.

## Reconstruction of the mechanism

Let (X,S,mu) be the binary Rudin–Shapiro shift with (Sx)_i=x_(i+1). The necessary input is minimality and unique ergodicity, zero mean of x_0, and E[x_0 x_m]=1_{m=0}. These inputs are directly stated or derived on Baake–Grimm arXiv:0810.5750v2 pages 2–3. The paper also directly classifies line-supported measures in the plane as singular continuous, consistent with ambient Haar classification. Its Fourier convention is exp(-2 pi i k x).

The product action (m,n).(x,y)=(S^m x,S^n y) is an independent-coordinate Z^2 action. It is not the diagonal Z action. Every orbit is the Cartesian product of two dense orbits. For unique ergodicity, disintegrate an invariant probability over the second coordinate: invariance under (1,0), tested on a countable determining family, makes almost every conditional measure S-invariant, hence equal to mu. Invariance under (0,1) then forces the second marginal to mu. Thus the invariant probability is mu tensor mu. This applies even when the selected deterministic pair has x=y; diagonal joining measures do not survive independent-coordinate invariance.

The four rational residues are 0, e=(1/10,1/10), a=(1/3,0), b=(0,1/3). Anchors at Z^2 and e companions always occur. The a slot occurs exactly when x_i=+1, and the b slot exactly when y_j=+1. All four classes are distinct; the union is an actual weight-one set, contained in (1/30)Z^2 and containing Z^2. Its difference set is uniformly discrete; FLC, the Delone property and the Meyer property follow.

The directed difference e modulo Z^2 occurs among ordered residue pairs only as (0,e). Hence anchors are precisely p with p+e also present. This recognizes phase modulo the integer lattice and the two optional slot patterns from finite radius data. Injectivity does not rely on average frequencies: phase and every binary symbol are retained. With the negative-translation hull action, Phi([x,u],[y,v])=Lambda_(x,y)-(u,v) respects the unit suspension seam because Lambda_(Sx,y)=Lambda_(x,y)-(1,0). The analogous identity holds in the second coordinate. Continuity, independent shift orbit density, compactness, and the marker decoder prove a topological conjugacy with the product of two unit suspensions. The invariant measure is mu tensor du tensor mu tensor dv. No symbolic observable has been silently transferred through a noninjective factor.

Minimality of that full action gives repetitivity and unique ergodicity gives uniform finite patch frequencies. A translation period must preserve the decoded anchor lattice, so it is an integer vector (m,n). It would give S^m x=x and S^n y=y. If a nonzero shift period existed for any x in minimal X, then X would be a finite shift orbit, contradicting its zero nonzero-lag autocorrelations. Thus there is no nonzero planar period.

## Physical diffraction from actual occupancy pairs

The occupancy functions per lattice cell are q_0=q_e=1, q_a=(1+x_i)/2 and q_b=(1+y_j)/2. Their mean weights are D=(1,1,1/2,1/2). For an ordered c-to-d slot pair with integer displacement (m,n), the limiting cell pair coefficient is D_c D_d plus 1/4 if c=d=a and m=0, plus 1/4 if c=d=b and n=0. This uses exactly the one- and two-point RS moments; it does not use IID within a sequence. Mixed a-b pairs average independently over i and j and have only the mean product. Every physical displacement must sum contributions from all compatible ordered slot pairs, including repeated motif differences.

Write D as the finite measure delta_0+delta_e+(delta_a+delta_b)/2. Then

    gamma = (D*D_tilde)*delta_(Z^2)
            + (delta_0 tensor delta_Z + delta_Z tensor delta_0)/4.

For each fixed physical displacement, restriction to a square changes only O(N) possible cell pairs along its boundary, uniformly in the symbolic configurations. Bounded occupancies and O(N^2) area remove this correction. The same argument handles motif shifts, with all compatible pairs summed. The difference support is locally finite, so coefficient convergence implies vague convergence. The O(N) assertion is a fixed-displacement assertion, not uniform in displacements growing with the window.

Fourier transformation gives the lattice Bragg term |D_hat(k,l)|^2 delta_(k,l), summed over integer pairs, plus (lambda tensor delta_Z + delta_Z tensor lambda)/4. This is supported by the countable union (R tensor Z) union (Z tensor R), a planar Lebesgue-null set. Each line term is nonatomic even at intersections. Zero AC physical diffraction is therefore correct under the stated ambient measure. At displacement zero, sum_c D_c^2=5/2 and the two exceptional terms add 1/2, giving gamma({0})=3. Density is 3 and the origin Bragg intensity is 9. The line terms add no atom to that Bragg mass.

## Dynamical measure and endpoint normalization

On the unit suspension, h([x,u])=x_0 for 0<=u<1 is bounded measurable. It need not be continuous at the seam; the seam is null. Under time t, the new symbol is x_floor(u+t). Its correlation after integrating x is the indicator floor(u+t)=0. The measure of u in [0,1) satisfying 0<=u+t<1 is (1-|t|)_+, including negative t and integer t. Half-open endpoint choices do not change the measure.

The triangle is the convolution of 1_[0,1] with its reflection, so its Fourier transform in the source convention is (sin(pi k)/(pi k))^2, with removable value 1 at zero and integral 1. On the product suspension, H=h tensor h has product correlation and density sinc^2(k_1)sinc^2(k_2). That finite spectral probability vanishes only on nonzero-integer coordinate lines, a planar null set, so it is equivalent to planar Lebesgue measure. The previously established conjugacy makes H a bona fide physical hull observable. This confirms the central tensor-product mechanism independently of the candidate's finite scripts.

## Source bridge and support status

The stated substitution a->ab, b->ac, c->db, d->dc is primitive (third iterates contain all letters), and its sign coding is the source RS sequence. For the legal rho^2-fixed seed c|a, the even-index letters are a,d and odd-index letters b,c. Binary rho^2 images are +++-, ++-+, --+-, ---+, matching the source four-adic recursion and seeds w(0)=1, w(-1)=-1. Thus a coding mismatch is not visible. The source correlation recurrences first solve b_1=b_1/4 and a_1=-b_1/4, then remove the remaining small indices and induct on the others. Strict ergodicity supplies uniform averages of continuous cylinder functions on all X.

Both frozen scripts were run in an owned isolated copy. Both exited 0 with empty stderr; their raw stdout/stderr and structured replay record are preserved under controls/. The first is exact finite pair-moment algebra, not an infinite proof. The independent script builds actual deterministic physical point sets and retains finite imbalance and truncation in its finite comparison. Its PASS does not by itself certify public result manifests, byte bindings, scope statements, or complete proof validity. All twelve original bytes were separately hashed in FROZEN_READ_RECEIPT.json.

## Falsifiable risks and present gaps

I find no central mathematical gap in the reconstructed frozen theorem at this checkpoint. The principal attack surfaces for the forthcoming integrated package are: replacing independent Z^2 action by a diagonal action; losing the marker injectivity at seams; failing to sum colliding physical displacements; treating finite RS means as zero; using boundary domains inconsistent with actual crop; taking line AC as planar AC; or mishandling floor/section endpoints or Fourier units. They remain explicit checks, not assumptions to suppress.

Support claims must be checked anew after exposure. In particular, successful historical scripts do not establish integrity or sufficiency of an unseen repair. Historical priority remains unverified. An unrestricted source refutation is not a separately one-dimensional resolution. Outside people have not been contacted, and no status, Git, PR, DOI, queue or source artifact has been changed.

Checkpoint completion estimate: 40% of the assigned fresh whole-package review. The independent reconstruction and primary source inspection are complete; repair exposure and full math/support adversarial review remain.
