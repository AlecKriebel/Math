# Exact-one structure and elementary bounds

This newly authored reconstruction proves the exact-one formula, the exceptional one-defect upper construction, a reduction excluding defects above row two from improving the core phase, and unrestricted elementary bounds. It does not identify the unrestricted minimum with the one-defect minimum.

## 1. Definitions and conventions

For real X >= 1 let P_X = {(a,b) in Z_{≥0}^2: 2^a 3^b <= X}. Write A_b = floor(log_2(X/3^b)) for its nonempty rows. A complete triple anchored at (a,b) is

T_(a,b) = {(a,b),(a+1,b),(a,b+1)}, 0 <= a <= A_(b+1).

A hitting set H meets every complete triple; tau(X) is its minimum cardinality. With binary indicators x_(a,b), set D(H) = sum_T (|H intersect T| - 1). Define q0(X) as the minimum over D=0, and q1(X) as the minimum over D<=1. Consequently tau <= q1 <= q0.

Color (a,b) by a+2b modulo 3. Every triple contains one vertex of each color. Remove isolated vertices from each color class and call its cardinality C_r(X). For X<3 all vertices are isolated. For X>=3 the only possible isolated vertex is (A_0,0); it is isolated precisely when A_0-A_1=2. Indeed every b>=1 vertex is the north member of a triple, and the bottom vertices used by triples are exactly 0,...,A_1+1. Thus every adjusted color class is an exact-one hitting set and q0 <= min_r C_r.

All floor/log expressions specify integers; the certificate computes them by integer multiplication, never floating point.

## 2. Height-three rigidity

For exact-one constraints, the next row is forced by

x_(a,b+1) = 1 - x_(a,b) - x_(a+1,b).                         (1)

Consider a triangular stencil with four bottom vertices, three on the next row, then two, then one, all six supporting constraints exact. Starting with a binary word of length four, repeated use of (1) remains binary on this stencil if and only if that word is

0010, 0100, or 1001.

This is a sixteen-case calculation; checks/check_structure.py enumerates all sixteen words. Equivalently the first three bits sum to one and the fourth equals the first. When (a,3) belongs to P_X, the entire stencil based at (a,0) belongs to P_X because replacing one factor 3 by one factor 2 can only decrease the weight.

Suppose X>=27 and put k=A_3. Applying the stencil at a=0,...,k shows that the bottom prefix a=0,...,k+3 belongs to one color phase r. The overlapping stencils force a single phase throughout this prefix.

## 3. All-scale exact-one theorem

**Theorem.** For every X>=1, q0(X)=min_r C_r(X).

**Proof.** A minimum exact-one cover omits isolated vertices. For X>=27 its bottom prefix through k+3 is fixed by a phase r as above. There are at most two further bottom bits, because A_0-A_3 is four or five.

Compare this cover with the adjusted phase-r cover. Their difference d satisfies d_(a,b+1)=-d_(a,b)-d_(a+1,b). Since the bottom difference is supported at a>=k+4, a difference in row b can occur only at a>=k+4-b. At row three this requires a>=k+1, whereas A_3=k. Thus the difference vanishes in row three and every higher row. All changes are confined to the terminal portions of rows zero, one, and two.

Translate the terminal coordinates by a'=a-k, and put Y=X/2^k. Then 27<=Y<54 and the four possibilities for (A_0-k,A_1-k,A_2-k,A_3-k) are exactly

- 27 <= Y < 32: (4,3,1,0)
- 32 <= Y < 36: (5,3,1,0)
- 36 <= Y < 48: (5,3,2,0)
- 48 <= Y < 54: (5,4,2,0)

The phase changes from r to r-k modulo three. The size difference is entirely within this translated terminal region, so it is enough to check these four finite profiles. In the following table a tail is the word at bottom coordinates a'=4,...,A_0-k. The number in parentheses is its cardinality difference from the adjusted phase of the indicated color. Isolated bottom bits are required to be zero.

| Profile | Phase 0 | Phase 1 | Phase 2 |
|---|---|---|---|
| (4,3,1,0) | 0 (0) | 0 (0), 1 (0) | 0 (0), 1 (0) |
| (5,3,1,0) | 00 (0) | 00 (0), 10 (0) | 00 (0), 10 (0) |
| (5,3,2,0) | 00 (0) | 10 (0) | 00 (0), 10 (+1) |
| (5,4,2,0) | 00 (0), 01 (0) | 10 (0) | 00 (0), 01 (0), 10 (0) |

Every feasible bottom tail is listed. Equation (1) forces every other entry, so the enumeration is complete. No allowed tail has negative cost. Hence every exact-one cover has size at least the adjusted count of its core phase and therefore at least min C_r.

For 1<=X<27 the only distinct smooth cutoffs are 1,2,3,4,6,8,9,12,16,18,24. Exhaustive enumeration of the at most five bottom bits, followed by forced recurrence (1), gives respectively q0=0,0,1,1,1,1,2,2,2,3,3, equal to min C_r. Between consecutive smooth cutoffs P_X is unchanged. The color-class upper bound completes the proof. QED.

This four-profile reduction proves an all-scale statement; its finite cases are exhaustively enumerated by the checker.

## 4. Exceptional single-defect upper construction

For each integer m>=0 and 24*2^m <= X < 27*2^m, take the adjusted color r=m+2 modulo three. Remove

R = {(m+2,0),(m+3,1),(m+1,2)}

and add

A = {(m+3,0),(m+1,1)}.

All removed vertices belong to that phase, all added vertices are outside it, and all five lie in P_X. The construction decreases cardinality by one.

A direct incidence check proves that every triple still has exactly one hit except the triple anchored at (m,1), which has two. The only potentially affected anchors are

- (m+1,0): remove its east member (m+2,0), add its north member (m+1,1)
- (m+2,0): remove its anchor member (m+2,0), add its east member (m+3,0)
- (m+3,0): remove its north member (m+3,1), add its anchor member (m+3,0)
- (m+1,1): remove its north member (m+1,2), add its anchor member (m+1,1)
- (m,1): add its east member (m+1,1), yielding the sole extra hit

All other would-be affected triples require weights at least 27*2^m and are absent. In particular the triple at (m+2,1) requires its north member of weight 36*2^m. More explicitly, the removed north vertex (m+1,2) could be east of anchor (m,2), but that triple requires weight 27*2^m and is absent; its own anchored triple requires 54*2^m. The removed (m+3,1) could be an anchor only at weight 72*2^m, also absent. Thus all complete affected triples are covered by the four cancellations and the one extra hit listed above.

Define epsilon_r(X)=1 if X lies in [24*2^m,27*2^m) for an integer m>=0 with r=m+2 mod 3, and zero otherwise. These intervals are disjoint. The proved conclusion is

q1(X) <= min_r (C_r(X) - epsilon_r(X)).                     (2)

The finite patch instances in fixtures/check_structure.json check many m and all smooth changes in those intervals, but the all-scale justification is the incidence calculation above. Equality in (2) is not established by this construction alone.

## 5. Defects above row two cannot improve the core phase

**Lemma.** Let H have D(H)=1, with its unique double-hit triple anchored at (u,v), v>=3. Then |H|>=C_r(X) for a core phase r.

**Proof.** The height-three bottom stencils use only anchors in rows zero through two, so their rigidity is unaffected. As in Section 3, the bottom boundary deviations vanish by row three. Up to row v the cover is therefore the same phase r; the bottom boundary contribution relative to C_r is nonnegative by the four-profile check.

Relative to that phase, the defect introduces a +1 difference at (u,v+1), and every higher row follows the homogeneous recurrence d_(a,b+1)=-d_(a,b)-d_(a+1,b). The phase value at this first changed vertex must be zero. If both (u,v+2) and (u-1,v+2) exist, they have differences -1 and both would have to have phase value one. They are adjacent vertices of different colors, which is impossible. Thus there is at most one surviving next vertex.

If u=0, any surviving support is a vertical chain on a=0. If u>=1, the only possible surviving vertex is (u-1,v+2), necessarily at the right boundary; every subsequent surviving vertex moves one step northwest, since each row width decreases by at least one. In either case the support is a single chain, with differences +1,-1,+1,... . Along it the phase color advances by two (vertical) or one (northwest) modulo three. A fourth changed vertex would have the same phase color as the first, but would require phase value one instead of zero. Hence the chain has length at most three. Its total difference is one, zero, or one, always nonnegative. Adding the nonnegative bottom-boundary contribution proves the lemma. QED.

This reduces any possible improvement over a core phase to sole defects anchored in rows zero, one, or two. It does not by itself classify those low defects.

## 6. Unrestricted bounds and pure-power jumps

Let Psi(X)=|P_X| and B(X)=Psi(X)-3*tau(X). The raw three color classes give tau<=Psi/3, so B>=0.

The triples whose anchors have any one fixed color are pairwise vertex-disjoint. Indeed the three possible anchors containing a given vertex are itself, its west neighbor, and its south neighbor, and their colors are pairwise distinct. The number of all anchors is Psi(X/3). Therefore

tau(X) >= max_r #{anchors of color r} >= Psi(X/3)/3,

and hence

0 <= B(X) <= Psi(X)-Psi(X/3) = floor(log_2 X)+1.

This bound does not prove that B is unbounded.

At the cutoff 2^a the new vertex (a,0) is isolated: it cannot be a north member, its potential west anchor would require the missing north vertex of weight 3*2^(a-1)>2^a, and its own anchored triple would require 3*2^a. No new complete triple is created. Consequently tau has zero jump there, whereas Psi and the independence number f=Psi-tau each have jump one (including a=0 from the empty prefix).

## 7. Reproduction and scope

Run `python3 -I -B checks/check_structure.py`. Its exact output is recorded in `fixtures/check_structure.json`: the exhaustive stencil words, eleven small base cases, four complete suffix profiles, patch-incidence tests, and disjoint-matching examples. The written reductions, rather than the size of the tested range, justify the all-scale statements. The original irrationality question remains unresolved.
