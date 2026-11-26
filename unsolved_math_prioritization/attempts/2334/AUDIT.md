# Independent mathematical audit of EP-839 / 2334

## Decision and scope

**Accept with the single boundary-wording correction recorded in CORRECTION.patch and already incorporated in PROOF.md.** The original packet is unchanged. Its manifest SHA-256 is `b36ac515383501830bfe77f06956da84b5bef309d4f9c0534a0abe6fc960a414`; the original proof SHA-256 is `84569672464364bd298fafad242a5de76acfbe4ed4bce67ba9ea1b5856b458fb`.

The accepted results are a sharp logarithmic-logarithmic mass bound for a specified separated-block architecture, an admissible width-two example attaining its coefficient, a verified defect in the stated 1993 extension recipe, a sufficient one-endpoint repair, and the resulting example's exact upper density and reciprocal-mass asymptotic. Neither original question is solved for arbitrary admissible sequences. No novelty claim is accepted or made.

The correction is small but necessary: for T=4 the left bridge term is C's first term, so the original proof's claim that both bridge terms are *strictly* inside C is false. Membership and consecutiveness are unaffected. No theorem statement, constant, endpoint repair, or substantive conclusion requires changing.

## 1. Primary-source verification

The complete four-page article by Robert Freud, *Adding Numbers*, James Cook Mathematical Notes (1993), printed pp. 6199–6202, was independently read from the retained images of PDF spreads 10–12. In particular, the source uses positive integers x,y, imposes x >= 17y-2 for the finite construction, chooses equality for the stated count, and sets y=T² for an already constructed prefix in the infinite extension. No congruence restriction on T or exclusion of the finite y=1 construction is stated.

The printed fourth interval has lower endpoint 8x-8y+3T+1, hence 4L+3T+1 after L=2x-2y=32y-4. The image confirms the final +1. The preceding three intervals and all upper endpoints agree with the candidate's transcription.

Paul Erdős's *Some forgotten problems* (1992), printed pp. 42–43, was independently read from the retained page images. The lower-natural-density and logarithmic-density questions are separate from the upper-density-1/2 speculation. The already known possibility of logarithmic-logarithmic reciprocal growth is not a solution to either question and is not claimed here as new.

Public sources:

- [Freud, complete issue containing Adding Numbers](https://webhomes.maths.ed.ac.uk/cook/iss_no60.PDF)
- [Erdős, Some forgotten problems](https://hrj.episciences.org/125/pdf)

Both URLs were independently reopened during this audit. All 13 candidate-manifest members and all 100 source-handoff members passed byte-count and SHA-256 checks. Source PDFs remain separate from authored public deliverables. The later Coppersmith–Phillips paper was not inspected and supplies no premise of this acceptance.

## 2. General prefix-sum-separated mass bound

Write m_r=min B_r, h_r=|B_r|, T_r=sum of the first r blocks, with m_(r+1)>T_r and B_r contained in [m_r,Cm_r]. This orders the blocks even if C is large, since T_r is at least every preceding term. The integral estimate

sum_(a in B_r) 1/a <= log C + 1/m_r

is valid also for a partially counted block. From T_r >= 2T_(r-1)+1 we have m_r >= 2^(r-1), so the accumulated 1/m_r errors are bounded independently of the particular sequence.

For u_r=log m_r >=16, classify a block as small when h_r <= m_r/u_r². The total reciprocal mass of small blocks is at most sum 1/u_r², which converges by the preceding geometric growth of m_r. Blocks with m_r<e^16 account for a uniformly bounded reciprocal mass because their minima strictly increase geometrically; equivalently, they contain disjoint integers in a bounded interval depending only on C.

For successive non-small blocks, including intervening small blocks, m_next > m²/(log m)². Hence their log-minima satisfy

u_next >=2u-2log u >=(3/2)u.

Also log u_next >=log u+log 2-2(log u)/u. The sum of the error terms is bounded uniformly, because u increases at least geometrically from 16 and (log u)/u decreases there. Consequently at most (log log x)/(log 2)+O(1) non-small blocks begin below x. Summing their masses proves

H_A(x) <= (log C/log 2) log log x+O_C(1).

No avoidance hypothesis was used. The coefficient is genuinely sharp for the class without avoidance: full integer blocks [m,floor(Cm)], with each next m one more than the preceding total sum, have next minimum ((C²-1)/2)m²+O_C(m). Each block has reciprocal mass log C+O_C(1/m); thus the leading coefficient is log C/log 2. This elementary sharpness observation checks the constant and does not assert avoidance for C other than the separately verified C=2 construction.

For lower natural density, if N_r is the count through a block, then T_r >=N_r(N_r+1)/2. At the integer m_(r+1)-1 the counting function equals N_r and its ratio to that integer is at most 2/(N_r+1). This proves lower density zero for prefix-sum separation alone. It proves nothing about sequences for which that separation is unavailable.

## 3. Width-two admissible sharpness construction

For a finite admissible prefix P of total T and count N, set m=T+1 and append [m,2m-1] after deleting m+s for each nonempty suffix sum s of P. The N suffix sums are distinct integers in [1,m-1]. Exactly N new candidates are deleted, m survives, and the full new count is m-N>=1. The cumulative count after appending is therefore exactly m.

Every old-only sum is below m. Any sum containing at least two new terms exceeds 2m-1. A consecutive sum crossing the boundary and using only one new term must use the first new term m, together with an old suffix; its possible target was deleted. This exhausts the obstruction and establishes admissibility by induction, beginning with the block {1}.

Distinct positive integers give N=O(sqrt(m)); deleting N terms of size <2m from the full interval gives

m_next=(3/2)m²+O(m^(3/2)),

and the new reciprocal mass is log 2+O(m^(-1/2)). Since m grows at least geometrically, these mass errors are summable. Writing u=log m, the recurrence becomes u_next=2u+log(3/2)+o(1). The bounded increments show u_r=kappa 2^r+O(1). Positivity of kappa follows by taking a sufficiently large r for which m_next>=m² and u_r>0. Hence r log 2=log log m_r+O(1).

For every x between successive minima, H_A(x) differs from its value at the first minimum by a bounded amount, and log log x ranges over an interval of bounded length. Therefore H_A(x)=log log x+O(1) for all real x tending to infinity, not merely for an endpoint subsequence.

The first two terms of the constructed sequence are 1 and 2, so its prefix sums begin 0,1,3. Thus the suffix values T and T-1 exist, while T-2 does not once the prefix has at least two terms. The two largest interval candidates 2m-1 and 2m-2 are deleted and 2m-3 survives. Endpoint count m divided by endpoint 2m-3 tends to 1/2. Within a block, the count is at most N_old+t-m+1, and N_old=o(m); this gives an upper bound 1/2+o(1), uniformly for m<=t<=2m. In gaps the density decreases. Both density claims and sharpness at C=2 are valid.

## 4. Complete finite Freud construction

Substitution x=17y-2 yields the stated A, B, C and D, for every integer y>=1. Their sizes are 4y+1, 4y, 4y-1 and 72y-5. Their sums are respectively

- 136y²+18y-4;
- 204y²-24y;
- 272y²-100y+8;
- 7776y²-1188y+45.

The only short sums that can be retained terms are as follows.

1. A-pairs are odd, above the end of B and below the beginning of D, so cannot be C terms.
2. A-triples and B-pairs coincide in I, the step-three progression from 96y-9 to 108y-15.
3. A-quadruples and C-pairs coincide in III, the step-four progression from 128y-10 to 144y-22.
4. The three boundary pairs and the two A/B boundary triples are, respectively, 84y-9, 118y-13, 144y-16, 120y-14, and 132y-13.

Five terms beginning in A have sum at least 160y-10>U. Any triple beginning in B or later has sum at least the first B-triple, 144y-11>U. Among four-term blocks crossing A/B, the smallest has the last three A terms and the first B term, with sum 156y-20>U. Larger lengths or later starts only increase these bounds. Pairs of distinct D terms exceed U.

Thus the list is complete. The three deletion sets are disjoint and strictly inside D. Removing terms inside D changes no sum at most U: its first term remains, while every sum containing two D terms and every triple beginning in B or later is too large. This justifies the deletion step without assuming that arbitrary removal preserves avoidance.

The removed sums are

- I: 408y²-150y+12, from 4y-1 elements;
- III: 544y²-336y+32, from 4y-2 elements;
- V: 598y-65, from five elements.

Subtracting from the four block sums gives exactly

|F_y|=76y-7,

sum F_y=7436y²-1406y+70.

In particular F_1 has 69 terms, total 6100, and satisfies every stated finite source hypothesis, including x=15>0. The finite 19/36 asymptotic is sound.

## 5. Printed-rule witness, including the source's own seed

For T divisible by 4 with T>=4, y=T² and L=32y-4, set

a=2L+T-2, b=2L+2T+2, z=a+b=4L+3T.

C starts at 2L+2 and ends at 2L+8y-2. Hence a belongs to C (equality with its first term occurs exactly at T=4), and b is strictly below its last term. Both are even. Every C term strictly between a and b is in J2=[2L+T,2L+2T+1], and a,b lie immediately outside it. No other original block has terms in that interval. They therefore are consecutive surviving terms, including at T=4; the preceding B term does not lie between them.

The target z lies strictly inside D and above I. Its residue is 0 modulo 4, whereas all III deletions are 2 modulo 4. It lies strictly between the V entries 120y-14 and 132y-13, hence is different from all five V values. It also lies above J3 and exactly one below the printed J4. In detail, the relevant positive differences include 20T²+3T-1 from the top of I, 8T²+3T-2 above 120y-14, 4T²-3T+3 below 132y-13, and 32T²-7 above the top of J3. Thus z is retained by the printed rule.

The source's valid F_1 seed has total T = 7436 - 1406 + 70 = 6100 by the full sum polynomial. Since 6100 is divisible by 4 and at least 4, the symbolic membership, adjacency, residue and deletion arguments above apply directly. No enumeration of the next block is needed. The displayed source rule therefore really has the stated endpoint defect. This does not refute the source's finite construction or the existence of an infinite example of upper density 19/36.

## 6. Exhaustive universal repair proof

Assume T>=3, y=T². J1 deletes the T elements immediately following L in A, leaving the first four new terms

L, L+T+1, L+T+2, L+T+3.

It does not approach the A/B boundary: T+3<4T². J2 begins after C's first term and ends before its last, since T>2 and 2T+1<8T²-2. Both J3 and the repaired J4 lie strictly inside D: for example J3's first term exceeds D's first by 24T²+2T-3, while U minus J4's last is 16T²-4T-2>0. They neither change D's first term nor affect the preceding blocks.

Any new consecutive block of length at most four within A that was not present before the deletion must contain L and the first surviving terms following it. Its pair, triple and quadruple sums are

2L+T+1, 3L+2T+3, 4L+3T+6.

These lie in J2, J3 and the repaired J4 respectively. All other short A blocks and boundary blocks are unchanged.

The sole new C-pair straddles J2. For even T it is

(2L+T-2)+(2L+2T+2)=4L+3T;

for odd T it is

(2L+T-1)+(2L+2T+2)=4L+3T+1.

Both targets lie in the repaired interval [4L+3T,4L+4T+6]. The boundary case T=3 leaves C's first term in place, as required. Any triple beginning in C is already too large. The B/C and C/D pairs remain unchanged. Deleting inside D cannot create a new sum at most U, for the same reason as in the finite proof.

A forbidden consecutive block crossing the old/new boundary consists of an old suffix s with 1<=s<=T followed by the first k surviving new terms. For k=1,2,3,4, its sum is contained in

- [L+1,L+T];
- [2L+T+2,2L+2T+1];
- [3L+2T+4,3L+3T+3];
- [4L+3T+7,4L+4T+6].

Each interval is contained in the corresponding deleted J interval. Five or more new terms exceed U, including without the positive old suffix. Every old-only sum is at most T<L and cannot create a new target; the old prefix was admissible. These cases include every possible obstruction. The repaired extension theorem is proved for every admissible finite prefix of total T>=3.

The extra condition T>=3 is material to this proof. For T=1, deleting C's first term changes its B/C boundary and the repaired formula can fail. This excluded case is a negative control, not a counterexample to the stated theorem.

## 7. Corrected Freud mass and full-x density claims

On a fixed arithmetic progression of asymptotic density rho in [alpha y+O(1),beta y+O(1)], the reciprocal mass is rho log(beta/alpha)+O(1/y). Applying this to A,B,C,D and the two long deletion progressions gives

h_F=log 2+(19/12)log(9/8).

The isolated five deletions change this by O(1/y). The lengths of the repaired J intervals are T, T+2, T+1 and T+7, totalling 4T+10. Their actual union can only be smaller; every affected term is of order y. Their reciprocal cost is O(T/y)=O(y^(-1/2)) and their ordinary-sum cost is O(Ty)=O(y^(3/2)). Therefore

T_next=7436y²+O(y^(3/2)),

y_next=7436²y⁴(1+O(y^(-1/2))).

The positive rapidly growing sequence, beginning with the valid F_1 seed, consequently satisfies log log y_r=r log 4+O(1). Its reciprocal block errors are summable, so the accumulated mass is r h_F+O(1). On every intervening block or gap, the changes in both H_A and log log x are bounded. Thus, for all x tending to infinity,

H_A(x)=[log 2+(19/12)log(9/8)]/(log 4) · log log x+O(1).

The accepted coefficient is approximately 0.6345239594751639. Numerical approximations are not premises of the proof.

Before a new block, the old count is at most T while the new minimum is 32T²-4, giving lower density zero. A new block has 76y+O(sqrt(y)) terms; the old terms contribute O(sqrt(y)). U=144y-12 survives all deletions, so endpoint densities tend to 19/36.

To check that this is the upper density, the limiting count profile at scaled arguments 32,36,48,54,64,72,96,108,128,144 has values 0,4,4,8,8,12,36,44,64,76. Between these coordinates it is affine. The ratio of an affine function to its positive argument is monotone or constant on each interval, so its maximum occurs at a displayed endpoint. Direct cross-multiplication verifies that every endpoint ratio is at most 19/36, with equality at 144. Integer endpoints and fixed isolated deletions contribute O(1) uniformly; the extra deletion intervals and all old terms contribute O(sqrt(y)). In the gaps the density decreases. The claimed exact upper density follows.

## 8. Historical independent finite validation and limits

The audit's checker was authored independently from the mathematical source formulas and the written proof. No candidate program was source-read, imported or executed. Candidate-program bytes were used only for integrity hashing. No third-party program was downloaded or run for this audit.

The historical exact checks passed in normal Python, `-O` and `-OO`, with identical certificate hashes. They were not rerun for this edition; the following is verification metadata rather than distributed executable evidence:

- 83 finite Freud parameters: y=1 through 80, then 101, 137 and 256;
- 162 corrected extensions, with the complete bounded sweep and singleton-range coverage recorded in the historical audit;
- exact symbolic C-bridge checks for all T=3 through 10,000 and four consecutive integers of size 10^50;
- the T=6100 source-own-seed witness without materializing its next block;
- six width-two stages, ending with 40,191 terms;
- an independent prefix-difference oracle on small sequences, checking the main consecutive-sum oracle;
- 21 deliberately invalid or boundary controls: known bad sequences, reinsertion of every F_1 deleted value, both printed-rule small witnesses, omission of each correction interval, the excluded T=1 case, and the T=4 non-strict-interior boundary.

All mathematical test gates use explicit exceptions rather than assertions. An intentional unconditional failure is required to fail under each Python optimization mode. Integrity mutation controls separately reject changed manifest bytes, substituted member bytes, truncated member bytes and absent member files.

During checker development, its independent symbolic membership formula initially had two mistranscribed expressions for the finite boundary-deletion set. The directly generated construction and symbolic-membership cross-check rejected that draft. The checker formulas were corrected from the A/B boundary sums, and all final tests were rerun. This was an audit-code defect, not a defect in the candidate's finite formulas or mathematical conclusions.

These finite tests support the case analyses; they do not establish universal or asymptotic claims. The universal arguments above provide those proofs. Raw code, test certificates, source images/PDFs and coordination records are not distributed with this edition. Accordingly, the historical computational runs are not reproducible from these files alone; the complete written proofs remain inspectable and self-contained. Hashes establish byte identity and recorded match results, not mathematical truth. No new mathematical tests or scholarly-source inspection were performed for edition preparation.

This AI-assisted audit is unrefereed. Acceptance means independent internal AI mathematical review, not external human peer review, journal acceptance, or proof-assistant certification. Both original questions remain unresolved, and no novelty or priority is claimed.
