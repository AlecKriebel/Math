# Sealed independent mathematical assessment — PR 179, problem 10800007

Written before inspection of either verification program, any original review verdict, any parent opinion, or any sibling result. First assessment timestamp: 2026-10-13 04:43 UTC. Own audit progress: 25%; overall case estimate 5% and counts 36 completed / 20 published are untouched. Input documents read: authenticated original `problem.json` and `NO_COVER.md` only. Authenticated-head identifier supplied by parent: 090b45356f5d6829f755fbc7c5b1fde5565de695. This identifier is provenance information, not independently established by this assessment.

## Exact claim, hypotheses, and independent verdict

Let p=(a1,a2,a0,b1,b2,b0) in R^6, F_p(x,y)=x^2-y^2+a1*x+a2*y+a0 and G_p(x,y)=x*y+b1*x+b2*y+b0. Under the ordinary Euclidean topology, an admissible U is open and supports a continuous phi:U->R^2 for which F_p(phi(p))=G_p(phi(p))=0 exactly for every p in U. The claim is that every open U containing p=0 is inadmissible, hence no admissible open cover of R^6 exists, including infinite covers.

Independent verdict at this stage: the written local obstruction is correct for this explicitly stated polynomial family and these exact quantifiers. The proof is elementary, complete, and stronger than failure of one global section. Its claim to match the primary printed formulation has not yet been independently checked against the primary source; the dataset statement by itself suppresses definitions of f_a and g_b. No priority or novelty conclusion follows from this proof.

## Re-derived coefficient slice and exact solution equivalence

Put zeta=u+i*v and p(zeta)=(0,0,-u,0,0,-v/2). This is continuous, linear, injective, maps 0 to 0, and has coefficient norm sqrt(u^2+v^2/4)<=|zeta|. Restricting the equations yields x^2-y^2=u and x*y=v/2, precisely (x+i*y)^2=zeta. Both directions are equivalences of real equations, so no other real solution is concealed by the complex notation. At zeta=0, x^2=y^2 and xy=0 force x=y=0. At nonzero zeta a exhibited square root w has exactly the roots w and -w, since (z-w)(z+w)=0 in the field C. This establishes the two branches algebraically without a sampled root finder.

If U is open and contains p=0, continuity of p implies p^{-1}(U) is an open neighborhood of 0. Thus there is r>0 for which D_r subset p^{-1}(U), where D_r={|zeta|<r}. A selection would restrict to continuous s:D_r->C satisfying s(zeta)^2=zeta.

## Independent loop and sharp path bounds

Use gamma(t)=(1-t)+i*t on [0,1] and gamma(t)=(1-t)+i*(2-t) on [1,2]. Both definitions equal i at t=1. On the first piece, |gamma|^2=2*(t-1/2)^2+1/2; on the second, |gamma|^2=2*(t-3/2)^2+1/2. Therefore 1/2<=|gamma|^2<=1 throughout, gamma never vanishes, gamma(0)=1, and gamma(2)=-1.

Choose any c>0 such that c^2<r; the positivity and strict inequality matter. Let zeta(t)=c^2*gamma(t)^2. Then c^2/2<=|zeta(t)|<=c^2<r, so the entire loop lies strictly inside the required disk and avoids the branch point. The two pieces of gamma^2 are (1-2t)+i*(2t-2t^2), and (2t-3)+i*(2t^2-6t+4), respectively. At t=0 and t=2, zeta=c^2, while at t=1 zeta=-c^2. The midpoint and endpoint formulas agree exactly. The lifted roots along this loop are ±c*gamma(t).

For a hypothetical selection define q(t)=s(zeta(t))/(c*gamma(t)). It is defined and continuous because c*gamma(t) is continuous and nonzero, and q(t)^2=1. The only complex roots of q^2=1 are ±1; any continuous map from the connected interval to this discrete two-point set is constant. But zeta(0)=zeta(2), hence the numerator agrees at those endpoints and the denominator is its negative. Thus q(2)=-q(0), contradicting q(2)=q(0) and q(0) in {±1}. No numerical sample establishes this connectedness step. It is the decisive mathematical proof.

## Jacobian and where local regularity holds

The solution-variable Jacobian of (F,G) is [[2x+a1,-2y+a2],[y+b1,x+b2]], with determinant

2x^2+2y^2+(a1+2b2)*x+(2b1-a2)*y+a1*b2-a2*b1.

On the constant-coefficient slice this is 2*(x^2+y^2). At nonzero zeta, x^2+y^2=|zeta|, so the determinant is 2*|zeta|>0. At the zero root it is 0. Thus the loop lives entirely among simple roots although it encloses a parameter with a ramified solution. The implicit function theorem supplies local branches near a given simple root; it does not supply a branch on a full neighborhood containing the zero parameter. A general discriminant, a global regular parameter set, or its covering number has not been computed here.

## Boundary checks and scope limits

* Openness at zero is essential. A cover of R^6 must have a member containing zero, and that member contains a full neighborhood, regardless of its connectedness. No cardinality increase evades this local contradiction.
* Covering C\{0} with two open slit domains supplies square-root branches. One branch globally is impossible by the same endpoint contradiction. This proves the square-root model has sectional cover number two on the punctured plane only. It says nothing by itself about the regular part of the six-parameter family.
* Adding zero to a slit domain yields a domain that is not open at zero, even though a chosen root may extend continuously there. Changing allowed covers can therefore change the answer.
* Continuity of a square root along an interval is possible; continuity around the closed loop fails at the required identification of endpoints. Sampling values can miss this distinction.
* When c=0 the denominator is zero and this particular proof is invalid. When c^2=r the loop touches the excluded disk boundary; retain c^2<r. When roots are selected approximately, exact q^2=1 is unavailable.
* The root distance to 0 on this slice is sqrt(|zeta|). For fixed epsilon>0, selecting 0 is within epsilon of some root throughout |zeta|<epsilon^2. This defeats any attempt to transfer this exact local obstruction unchanged to an approximate-selection problem.
* A finite checker can establish specified identities or rational controls. Unless it also performs a symbolic or otherwise universal proof, passing finitely many samples does not establish all-t path inequalities, solution equivalence, continuity, or nonexistence of sections.

## Planned falsification after this seal

Inspect the two original programs only after sealing this document. Reproduce their unmodified runs from owned copies in normal and optimized Python. Change scientifically essential constants, path pieces, endpoint values, and bounds; test whether the guards detect such changes. Distinguish (i) scripts using assertions disabled by optimization, (ii) incomplete sampling blind spots, (iii) genuinely invalid written arguments, and (iv) documentation/provenance defects. Develop an independent universal polynomial-control checker where it adds evidence. Preserve all pilots, inputs, outputs, commands, hashes, interpreter versions, and exact gaps. Any guard repair stays entirely in this folder and never replaces an original. This audit will not edit Git, remotes, PRs, published records, or other researchers' files and will not contact another individual.
