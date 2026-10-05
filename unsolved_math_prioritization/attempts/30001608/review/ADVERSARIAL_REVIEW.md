# Independent adversarial review: problem 30001608, turn 4

Reviewed 2026-10-02. **Verdict: PASS for the stated all-load six-rate chain.** No mathematical gap or counterexample was found in the frozen proof. The argument supplies a single coercive Foster function and proves positive recurrence for every fixed real lambda>0. No author revision is required to repair a mathematical defect identified by this review.

This verdict is a mathematical review, not a formal proof-assistant certificate or a worldwide novelty certification. The finite controls below are supplemental falsification tests, not a replacement for the all-state argument. No files were published as part of this review.

## Frozen inputs and source scope

The reviewed proof is `TURN_4.md`, SHA-256

    34e043b456ddc25cc37d86d3e5a39d10243de91c6a5d5002952252d2eab1b0fa

It is also available at the immutable research checkpoint:

https://github.com/AlecKriebel/Math/blob/fdfc1de61e7a912219a07445cdf1d247c1cef88b/unsolved_math_prioritization/attempts/30001608/TURN_4.md

The author's checker SHA-256 is

    53aab7ce990f4b70d6d1ea3a3665e8e8375685407589e021f50a4695f075acae

Its saved output, independently rerun byte-for-byte, has SHA-256

    316f8ba5809137781ca116431c0671a907b2a66d6d0d1867f25acc29e3519418

The recovered prior source audit has SHA-256

    bfa6a95301775d8f9d70a58fe664cfb48d6cb08dff481084ef7d7e5882bf8b50

The new source recheck has SHA-256

    dec4b8596fa35011cfd3b9cad39814af727d328f8c9b92671e30bbce08316932

I independently reopened these primary source texts:

1. Norros, Oberwolfach Report 48/2010, printed pp. 2782-2783, https://ems.press/content/serial-article-files/46306. Its deterministic-first-chunk paragraph states the stochastic stability question, contrasting it with the unstable large-system limit. The following Enforced Friedman paragraph defines a different algorithm. The proof under review addresses the former only.
2. Norros-Reittu-Eirola, arXiv:0910.5577v1, Figure 2, PDF page 8, https://arxiv.org/pdf/0910.5577v1. Its figure gives the exact two arrivals and four download/departure rates used here. In particular, the denominator is x+y+1, not a+b+x+y+1, and all seed terms are retained. Its historical instability conjecture is not the controlling later conjecture.

Fresh HAL download and PDF screenshots were unavailable. I do not claim a fresh visual inspection of the 2011 author proof or a new byte-level verification of its PDF. The pinned 2011 audit identifies the final Conjecture 3.6; the independently accessible OWR statement and historical exact generator are consistent with it. The prior manifest records source PDF hashes 9e6cd0dbf890c1fc339afee66be6c941852ac5b55f4aee71125a313fce92cb15 (OWR), 52e045a4e47c7b9ee1be8ed134124599cd52bfec580bba691945f53af520a6ec (arXiv), and 756ea0a12020eb8d7bc142322563358d823afb8e27bb8b2da58b741a3b87eddb (HAL). These are inherited provenance records, not hashes recomputed from new PDF downloads in this review.

The scope is exactly the displayed four-coordinate continuous-time Markov chain, for fixed lambda>0. It is not every chunk-selection rule, the many-chunk system, Enforced Friedman, a changed denominator, or a claim of uniform bounds in lambda. The known large-system instability is credited source material; it is not silently substituted for a stochastic proof.

## 1. Generator identities and smoothing: pass

For W=2a+2b+x+y, each arrival adds two and each of the four other transitions subtracts one, so LW=2lambda-u-d. For Z=a+x-b-y, first downloads leave Z invariant; the two arrivals cancel in drift and the two departures give LZ=(y-x)/D. Its unit-jump quadratic variation rate is lambda+d. These identities were checked directly from the six event vectors, not by a fluid approximation.

The rounded absolute value has a derivative clipped to [-1,1] with global Lipschitz constant 1/m, including at its two junctions. Therefore its scalar quadratic upper bound is valid even for a jump crossing a junction. With m=4c, the second-order contribution is (lambda+d)/8 after multiplication by c, giving exactly beta=17lambda/8 and q=7/8. No factor of two is missing.

When Z>=m and x>=3(y+1), h'(Z)=1 and (x-y)/D>=1/2, so the signed imbalance drift is at most -c/2. The proof uses this only after establishing the required sign of Z. Elsewhere it uses the valid upper bound c, without assuming a favorable sign.

## 2. Finite corrector and domination: pass

The reflecting finite birth-death chain has detailed-balance weights gamma^k. Its truncated geometric mean increases to gamma/(1-gamma)=theta+1, so a finite R satisfying both strict requirements exists for every real lambda>0. The integer R need not be uniform in lambda.

The prefix sum defining each t_k is strictly negative for k<R because the weighted mean below the cutoff is strictly smaller than the full truncated mean. Thus g is nonnegative and decreasing, with g(R)=0. Flux telescoping gives Qg(k)=k-mu, including the terminal equation at R. I also reconstructed this solution independently from the terminal equation backward and checked every finite state.

For the actual y process, births are at least gamma(y+1) precisely in the stated b/D>=gamma region; their g-increments are nonpositive. Death rates are at most y, with nonnegative g-increments. Both replacements therefore give upper bounds in the claimed direction. At y=R the upward increment is zero, so no suppressed-birth error is hidden. At y>R, even the downward step from R+1 reaches g(R)=0, so Lg=0. The symmetric x argument is identical. No equilibrium substitution for the original chain is made.

## 3. Cutoff interface signs and constants: pass

The product identity uses the post-jump value g(y'), which is essential. In a first download, the common denominator increases and neither waiting numerator increases. Both cutoff factors are nonincreasing, and post-jump g is nonnegative; hence every corresponding interface error is nonpositive. This remains true when a or b is arbitrarily large. The potentially large first-download rates can indeed be omitted from an upper bound for the interface cost.

At arrivals only one cutoff changes, at most ell/D; the aggregate arrival rate is lambda. At a departure D>=2. If the current ratio is saturated the cutoff increment is zero. Otherwise w<eta D yields an increment at most ell eta/(D-1)<=2ell/D. Summing two cutoff factors, each with post-jump g<=G, gives 4ell G/D per departure. The stated ell G(lambda+4d)/D remainder is correct.

The coarser bound also holds: first downloads decrease each entire product, an arrival raises J by at most G, and a departure raises it by at most 2G. Thus LJ<=G(lambda+2d) globally, including D=1, where no departure occurs. The independent controls test both the exact post-jump decomposition and these bounds.

## 4. Exhaustive regions and finite exceptional set: pass

All constants in the N and B definitions are finite, eta<1, and N can be chosen as a finite integer. There is no circular dependence of R or G on N.

- Region I: if both x,y>=R+1, every current and one-step successor g-value vanishes. Thus LJ=0 exactly, including the boundary R+1. The identity D(d-y)=y(x-y)+x for x>=y gives d>=min(x,y). The chosen R then gives LV<-2.
- Region II: take y<=R and x>=N. The x corrector and all its successors vanish. The inequalities d<=2R+1, (x-y)/D>=1/2, and qd>=y hold. In the last inequality, x>=3(y+1) gives x/D>=3/4 and hence qd>=(21/32)(2y+1)>=y. The interface remainder is at most one by the N choice.
- In the saturated band b/D>=eta, the negative corrector mean gives beta+c-mu+1<-3. In the unsaturated band, b<eta D and a>=0 give Z>=(1-eta)x-(1+eta)y-eta>=m. The imbalance term is then favorable. Since 0<=f<=1 and mu>0, f(y-mu)<=y regardless of the sign of y-mu. This gives beta-c/2+1=-3. The ramp band is fully included, with no uncharged switch.
- Region III: after the first two cases fail, min(x,y)<=R and max(x,y)<N, so x+y<=N+R. The proof deliberately uses a loose upper bound here. Then d<=x+y and u>=(a+b)/(N+R+1). The displayed B gives LV<=-1 whenever a+b>B.

These are exhaustive cases. Outside the stated finite set F, either a visible count triggers one of the first two estimates, or the waiting count triggers the third. A noninteger B causes no issue because F is defined on the integer lattice. The proof does not claim negative drift inside F or rely on any approximate threshold.

## 5. Nonexplosion, irreducibility, and Foster conclusion: pass

On a fixed finite time interval the arrival count is Poisson with finite parameter. Each initially present peer has at most two remaining non-arrival transitions, and each arrival adds at most three total jumps including its arrival. Hence the total jump count is almost surely finite. All individual rates at finite states are finite.

The permanent seed makes all needed download and departure steps positive. Any finite state can reach zero by a prescribed finite sequence avoiding arrivals, and zero can reach any finite target by prescribing arrivals and first downloads while avoiding departures. Each such finite sequence has positive probability. Irreducibility for lambda>0 is therefore proved, rather than assumed. Lambda=0 is correctly excluded from this assertion.

V is nonnegative and satisfies V>=W>=a+b+x+y; each finite sublevel set is finite. The six-neighbor structure makes the localized generator sums finite. Applying stopped Dynkin on finite population sets is valid; population localization tends to infinity almost surely on bounded time intervals by the nonexplosion estimate. Fatou followed by monotone convergence yields E_s tau_F<=V(s) for s outside F.

The continuous-time Foster criterion applies. To make the finite-set hypothesis entirely explicit, every finite set of this irreducible chain is small: for any fixed t>0 and any target state o, each i in F has P_t(i,o)>0 by a finite path completed before t and a final no-jump period, so the finite minimum is positive. V and LV are bounded on F. Taking b=max(0,1+max_F LV) produces the global drift form LV<=-1+b 1_F. Thus this is the usual nonexplosive irreducible countable-state Foster setting. It yields positive recurrence and the unique stationary probability law. No stationary moment estimate or uniform-in-lambda conclusion is being smuggled in.

## 6. Independent controls

The independent standard-library program `independent_check.py` imports no author code. It uses the closed-form truncated geometric mean and solves the finite Poisson equation backward from

    g(R)=0,  g(R-1)=1-mu/R,

then reconstructs all earlier increments. It directly evaluates the six-rate generator and each interface decomposition with rational arithmetic. New noninteger loads are 1/7, 7/3, and 13/2. For each load it checks 636 states, including both sides of gamma/eta cutoffs, g support boundaries, N-1/N/N+1, and waiting rooms beyond B. Total: 36,709 exact assertions over 1,908 states; all passed.

The author's original checker was separately rerun at its five loads. Its 71,165 assertions passed, and the output exactly equals its frozen receipt. The independent checker also passes Python syntax compilation. These controls are not exhaustive over the state space; the preceding analytic review is what addresses arbitrary states and arbitrary real lambda>0.

## Disposition

No mandatory mathematical correction. A polished manuscript could add a precise reference for the standard continuous-time Foster criterion and state the finite-set smallness observation explicitly, but the supplied localization and recurrence discussion are sufficient for this discrete finite-neighbor setting.

The result is a complete proof candidate that passes this independent adversarial review for the exact six-rate target. Historical priority and publication status remain separate questions. Fresh 2011 PDF access remains an explicitly disclosed source-access limitation; it is not replaced by an assertion about a different protocol.
