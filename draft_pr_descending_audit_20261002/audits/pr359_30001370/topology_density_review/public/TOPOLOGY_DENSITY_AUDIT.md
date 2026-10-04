# Fresh topology and rough-density audit of PR 359

Completed analytic audit; final package closure is recorded separately.
Independent reconstruction was sealed at
2026-10-03T22:02:20.327543+00:00, before candidate, QUEUE, or review access.
Its SHA256 is `0b4373bd5ad250a9a8a40a82f8100e3583b5a840d4a2da385937febc80c7178b`.

**Mathematical disposition: PASS within the exact source scope.** I found no
mandatory mathematical correction in the topology/rough-density mechanism.
The candidate proves the full relative-L1 boundary assertion, conditional on
the correctly credited original global-convergence and boundary-seed results.
This is an AI-assisted adversarial review, not human peer review or a
historical-novelty certificate. The source conclusions are hypotheses checked
against proofs, not consequences inferred from the existing review's verdict.

## Exact claim and source fidelity

Write I=[-1/2,1/2] and D={u in L1(I):u>=0 a.e., integral u=1}. Set
G(m)=A tanh(Bm/A), 0<A<=2/5 and 6<B<=16. The transfer map is
F(u)=P_{T_r}u, r=G(integral x u(x)dx), where
f_r(x)=((r+4)x+r+1)/(2rx+2), with branches f_r and f_r-1 separated
at -r/4. The precise target is

    W = boundary_D B+ = boundary_D B-,
    W={u:F^n u ->1 in L1}, B+ and B- the other fixed-point basins.

The conjecture is on printed p.2715 of Keller's contribution, printed
pp.2713-2715, in [OWR49/2009](https://ems.press/content/serial-article-files/46250).
The same report supplies exhaustive convergence and open stable basins.
The full [BKZ author preprint](https://mat.univie.ac.at/~zweimueller/MyPub/bkz.pdf)
was independently read: Sections 2-6 and Appendix A, including the actual
proofs of Proposition 3, Proposition 4, Lemma 4, and the branch formulas.
These hypotheses also occur in [arXiv:0812.4040v1](https://arxiv.org/abs/0812.4040).
The exact model and topology match; no ambient-L1 boundary is substituted.

The retrieved author PDF has 36 pages and a December 19, 2008 title-page
date. The retrieved arXiv v1 PDF has 36 pages and a November 10, 2018
rendered title-page date; its abstract records a December 21, 2008 v1
submission and a comment saying 37 pages. Those are distinct observations.
The two PDFs have distinct bytes. A full raw-text word comparison showed
the additional arXiv banner/date and extraction artifacts, without a changed
substantive theorem or proof in the inspected dependency chain. Neither
is represented as an inspected final publisher PDF. SHA256 identities and
native extraction evidence are preserved privately and summarized publicly.

The source's analytic mixture class D0 uses
w_y(x)=(1-y^2/4)/(1-xy)^2, |y|<=2/3. Its old two-sided boundary result is
only on W intersect D0. Each mixture lies between 1/2 and 2, and D0 is
L1-compact. Thus it is not dense in D, or even in W: the symmetric density
equal to 4 on the two endpoint intervals of length 1/8 and zero elsewhere
is in W but at L1 distance at least 1 from D0. This obstruction was sealed
before candidate access. The candidate does not use the false density claim.

## Complete relative-topology verification

For h_r(x)=(x+r/4)/(1+rx), h_r fixes the endpoints, is increasing, and
h_r^-1=h_-r. Its density pushforward Q_r is a signed-L1 isometry, and
T_r=T0 composed with h_r away from the cut. Define K(u)=Q_{G(phi(u))}u.
For target v solve

    rho = G(integral h_-rho(x) v(x)dx).

The mean on the right decreases with rho. Hence the residual increases
by at least the parameter increment, and changes sign at +/-A. Its unique
root depends continuously on v, with Lipschitz bound B/2 in the L1 metric.
Consequently K^-1(v)=Q_-rho(v)v. Joint strong continuity of Q_r follows
from continuous-function approximation and its isometry; operator-norm
continuity is unnecessary. This works for every density in D, including
unbounded functions and functions with positive-measure zero sets.

For w in D and v=P0w, define q(x)=w(x)/v(T0x) on positive output fibers,
and q=1 on zero output fibers. Both inverse-branch values of w vanish on
almost every zero fiber. Their q-values therefore have average 1 there
as well; everywhere P0q=1 and 0<=q<=2. The section R_w(z)=q(z composed
with T0) satisfies P0R_w(z)=z, R_w(v)=w, and

    ||R_w(z)-w||1=||z-v||1.

Null-set choices cause no problem because every branch is nonsingular.
The nonunique fiber allocation is an explicit selected section, not a
claimed unique inverse. P0 is relatively open, so F=P0 composed with K
is a continuous open surjection. Through each prescribed density, F has
a continuous exact section, and sections compose for each fixed finite
iterate.

The tail-equivalence identity F^-1(B)=B holds for each stable basin.
Continuity and openness now prove F^-1(boundary_D B)=boundary_D B:
openness makes every image neighborhood of a preimage boundary point meet
B, while continuity maps approaching basin points into the basin closure.
All these statements use relative neighborhoods in D. Since the basins
are disjoint and open and convergence is exhaustive, each boundary lies
in W. Also W is closed. Openness alone is not the missing density step;
the candidate correctly supplies a separate quantitative mechanism.

## Rough-density extension, independently checked analytically

Fix u in W and work on the probability space (I,u(x)dx). Every random
variable X_j=T_{r_{j-1}} composed ... composed T_{r_0}(x) is bounded,
even when the density u is not in L2. Its law has density u_j=F^j u.
For a fixed n, put epsilon=||u_n-1||1 and
J_n(y)=-1/2+integral_{-1/2}^y u_n. This is continuous, nondecreasing,
onto and absolutely continuous; it need not be Lipschitz or invertible.
The probability integral transform is uniform for a nonatomic law even
when J_n has flats. Its displacement is at most epsilon.

Keep the original branch labels A_j, with f_{r_j}(X_j)=X_{j+1}+A_j.
For a J=[-1/2,3/2]-valued variable Z, let V(Z)=b_r(Z), where b_r=f_r^-1
and r=G(E b_r(Z)). The scalar equation is strictly monotone and unique.
The candidate's probability-space contraction calculation is valid on
arbitrary probability spaces. Differentiation is along a bounded path;
all scalar derivatives are bounded on a compact rectangle, so differentiation
under expectation and the scalar implicit function theorem apply. No
Frechet differentiability on L1 or on an L2 neighborhood is claimed.

The rank-one norm bound uses 0<=q<=1, E q>=||q||2^2 and Cauchy-Schwarz;
rescaling a vector to q-p with p perpendicular to q and taking the
perpendicular limiting case is valid. The parameter derivative bound
g<=16-100|r|^2 follows from tanh feedback throughout the interpolation.
The exact covering certificate provides ||V(Z)-V(Z')||2<=24/25||Z-Z'||2.
I read the certificate code, checked its monotonic envelope mechanism,
and reproduced its complete output, rather than treating sampled values
as a bound on the interval.

Starting with Y_n=J_n(X_n), define backward Y_j=V(Y_{j+1}+A_j).
For each branch event, the sublaw of Y_{j+1} is dominated by its entire
law. It is therefore absolutely continuous whenever the latter is, and
its smooth inverse-branch pushforward remains absolutely continuous.
Starting from uniform Y_n proves this for every Y_j. The selected parameter
is exactly G(EY_j), so the resulting initial density v_n obeys F^n v_n=1.
Independence between branch labels and later variables is not assumed.
Endpoints and cuts have zero probability under these laws. Keeping the
same labels makes their differences cancel in the L2 contraction estimate.

The backward variables are also generated by deterministic maps H_j:

    H_n=J_n,
    H_j(x)=b_rho_j(H_{j+1}(T_{r_j}(x))+A_j(x)).

The two one-sided images at every old cut both equal the new cut -rho_j/4.
Thus each H_j is continuous, nondecreasing, onto, and fixes the endpoints.
Absolute continuity is preserved here because the inner branch is smooth
and bi-Lipschitz and the outer inverse branch is smooth; this is not an
unsupported assertion about arbitrary compositions of AC maps. Each
finite cylinder is bi-Lipschitz before terminal correction, so preimages
of derivative-exception null sets are null. Flats are retained explicitly.

The L2 parameter estimate gives sum |rho_j-r_j|<=384 epsilon. The sup
displacement recurrence with inverse derivative bounds 3/4 and 25/96
gives d_0<=101 epsilon and sum d_j<=403 epsilon. Differentiating on the
finite cylinders yields

    H_0'(x)=u_n(X_n(x)) R_n(x),
    exp(-964 epsilon)<=R_n<=exp(964 epsilon).

The displayed constants follow by summing the log-derivative bounds 1
and 35/24. They are independent of n and of density roughness.

The decisive integral is against Lebesgue measure, not u(x)dx. For the
original external parameter sequence, P_{r_{n-1}}...P_{r_0}1 is in D0
and bounded by 2. Consequently

    integral |u_n(X_n(x))-1| dx <=2 epsilon,
    ||H_0'-1||1 <=2 epsilon exp(964 epsilon)+exp(964 epsilon)-1.

This uses the actual branch formulas of the source, which preserve
|y|<=2/3. It requires neither square integrability of u_n nor positivity
away from zero. No division by u_n occurs.

For any AC nondecreasing onto H, H_*(H' dx)=dx follows by continuous test
functions and the fundamental theorem of calculus. It holds with flats.
For a continuous g, signed-measure pushforward contraction therefore gives

    ||H_*(g dx)-g dx||TV
      <=omega_g(||H-id||infinity)+||g||infinity||H'-1||1.

Possible atoms from pushing g through flats do not invalidate this measure
inequality. H_*(u dx) is already absolutely continuous by the law argument.
Approximate the fixed u by continuous g, take epsilon->0 as n->infinity,
then take the approximation error to zero. It follows that ||v_n-u||1->0.
This order of limits adds no rate hypothesis. Hence W is exactly the L1
closure of the finite preimages of 1. The credited boundary seed at 1,
complete boundary pullback, and boundary closedness prove the target.

## Independent attempts to falsify strengthened statements

The following obstructions are real, but none is an assumption of the final
proof. D0 is not dense, as established above. Uniform convergence H_n->id
alone does not imply total-variation convergence: for 0<c<1,
H_n(x)=x+c sin(2 pi n(x+1/2))/(2 pi n) has derivative 1+c cos(...), yet
||H_n*(dx)-dx||TV=integral |1-H_n'|dx=2c/pi. Thus the candidate's derivative
control is essential, and is actually supplied. A branch conditional law
need not be independent of its label; domination suffices. A cumulative
map can have flats; asserting it is a homeomorphism would fail. The
candidate never makes that assertion. Strong continuity of Q_r does not
mean operator-norm continuity, and the proof never uses the latter.

The separate Turn 2 polynomial example correctly shows ker(phi) is not
invariant under the linearized operator. Its corrected resolvent kernel,
strong L1 convergence, BV estimate, and high-frequency obstruction to
uniform L1 contraction are valid. This turn is not needed for the nonlinear
proof; no L1 stable-manifold theorem is inferred from it.

`check_topology.py` adds independent exact examples rather than reproducing
the author's rational parameter mesh. Twelve piecewise constructions use
terminal densities with a central zero interval, repeated through 1,2,4,8
doubling cylinders. They verify gluing, flat intervals, zero mass on every
flat, exact corrected uniform laws, zero feedback and exact TV errors.
Three analytical unbounded-density families use
(1-theta)+theta/(2 sqrt(2|x|)); rational polynomial integrals after
x=s^2/2 verify the cumulative pushforward and error theta/2. A separate
nonuniform branch allocation puts the entire target mass on an old zero
output fiber. All 10,116 exact controls pass. These examples test hidden
strengthenings; they do not replace the analytic proof above.

## Reproduction, packet semantics and exact remaining scope

Frozen scope: H=`6be98eac0ba508368218179ecf80020c037dbece`,
B=`efd29c05204703acca9a0860812f54b94fae54b1`. All 38 submitted files,
including the entire QUEUE bytes, match local Git blobs, decoded GitHub
API blobs, disk byte counts/SHA256 and mode 100644. PR and Git-diff path
sets match that scope. All 86 entries in the six nested manifests and
both historical predecessor edges match. Public receipts identify the
native imported captures; their complete stdout/stderr and hashes were
rechecked. Historical pending-review states are preserved historical facts;
the additive disposition and QUEUE claim are semantically consistent.

Every candidate program was read in full. The three author replays match
their complete frozen stdout byte-for-byte (60,934 assertions); the old
independent checker matches all 18,678 controls. The unchanged wrapper
passes public verification. Default Python and bundled Python lacked SymPy;
all initial failed replays are preserved. An existing Python 3.11.8 with
SymPy 1.14 completed the successful native runs without installation.

Current source custody verifies **all 3 PDFs in the candidate's source
manifest**. The first ESI download failed with native exit 6 (DNS), and the
first source-enabled candidate wrapper failed for that missing file. Those
failures remain preserved. Subsequently the exact 1,544,891-byte ESI payload
from the original URL's successful native retry was imported with parent
authorization and its source-custody receipt. SHA256
`0628d7a9acb61435d6513d919966502821ee8a38f4a9ec0a49f8e55264af1dd4`
matches the candidate manifest. The recovered source-enabled wrapper passes
with all 3 source identities verified. The full author-hosted BKZ PDF is
separately retrieved and checked; the ESI copy remains outside the
mathematical dependency chain. No sibling mathematical verdict was read.

No mathematical gap remains in this mechanism under the exact A,B rectangle
and credited prior theorems. Scope beyond that rectangle, quantitative
large deviations, arbitrary feedback maps and historical priority remain
unproved and are not claimed. The family map and current packaging status
are recorded in `research_log.md`. Exact public/private closure uses the
one-shot sealer after parent approval; all source PDFs and raw native
outputs stay private. The closure file records whether sealing occurred.
