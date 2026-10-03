# Attempt 4/5: the normalizer obstruction and a certified failed odd adaptation

Date: 2026-10-03 UTC. Objective: turn a proper pi-overgroup into a contradiction via normalizers, then adapt the classical even-prime counterexample if the contradiction fails. Outcome: a useful positive nilpotence criterion and two exact controls, but no odd-prime counterexample.

Set A=H∩N as before. The ambient realization makes A strongly pi-submaximal in N, and hence pi-submaximal in the standard (subnormal-embedding) sense.

## 1. Use the strongest available normalizer obstruction

The Wielandt–Hartley theorem states that N_N(A)/A is a pi'-group for a pi-submaximal A. The applicable result and the distinction between normal and subnormal embeddings are stated in Guo–Revin–Vdovin, arXiv:1808.10107v2 §1.2 and §1.4; the modern proof is credited there to Revin–Skresanov–Vasilev, Monatshefte für Mathematik 193 (2020), 143–155. This is used as an established theorem, not reproved or claimed new here.

Suppose A<B≤N with B a pi-group. Then

N_B(A)/A ≤ N_N(A)/A.

The group on the left is a pi-group and the one on the right is a pi'-group, so N_B(A)=A. Thus any proposed proper pi-overgroup of A must contain A as a self-normalizing subgroup.

This is restrictive, but odd solvability alone does not contradict it.

## 2. Positive nilpotence criterion

A proper subgroup U of a finite nilpotent group B is strictly contained in N_B(U). One direct proof uses the upper central series Z_0=1≤Z_1≤...≤Z_c=B. Choose the first j with Z_j not contained in U. Then Z_{j-1}≤U. For z∈Z_j\U and u∈U, the commutator [z,u] belongs to Z_{j-1}≤U, so z normalizes U while not belonging to U.

Combining this normalizer condition with §1 proves: if every pi-subgroup of N is nilpotent, then A is pi-maximal in N. More locally, no proper nilpotent pi-overgroup of A can exist. In particular, the singleton-prime case pi={p} is settled, consistent with Sylow theory.

Also A cannot be subnormal in any proper pi-overgroup B: in a subnormal chain from A to B, the first strictly larger term normalizes A. This again contradicts N_B(A)=A.

## 3. Why the normalizer route stops: an odd Frobenius control

Take B=C_7⋊C_3, with multiplication

(a,b)(c,d)=(a+2^b c modulo 7, b+d modulo 3).

Let A={(0,b):b∈Z/3}. Then |B|=21 and |A|=3, so A is a proper pi-subgroup for pi={3,7}. Nevertheless N_B(A)=A. For example, conjugating the generator (0,1) by (a,b) changes its first coordinate by a nonzero multiple of a unless a=0; hence an element normalizing A must have first coordinate0.

The exact checker independently tests all 21 elements and confirms this equality. Thus the conclusion of the Wielandt–Hartley theorem by itself cannot prove maximality, even for an odd solvable overgroup. This does NOT make A a counterexample to the original problem: A has not been realized as H∩N for a pi-maximal H in an extension of N. Indeed turn 1 forbids such a realization with N=B.

## 4. Reproduce the genuine even-prime mechanism

For comparison, the known example from Guo–Revin–Vdovin §1.4 takes G=PGL_2(7), N=PSL_2(7), pi={2,3}, and H a Sylow2-subgroup of order 16. Then H is pi-maximal in G but A=H∩N has order 8 and lies in a subgroup B≤N of order 24.

The independent small exact script constructs all 336 projective-line permutations from nonsingular2×2 matrices over F_7. It identifies the 168 square-determinant permutations as N, verifies N is normal, builds H from an element of order 8 and an inverting involution, and finds B explicitly. For every one of the 320 elements g outside H it computes <H,g>; every generated group has order 336. Thus H is in fact an ordinary maximal subgroup, and in particular pi-maximal. This gives an exact control for the extension-based failure mechanism without assuming a library's subgroup classification.

This is credited reproduction of a known even-prime example. It does not answer the requested odd-prime problem.

## 5. The odd adaptation fails for a structural reason

Deleting 2 from pi in this same ambient pair destroys the obstruction. Since [G:N]=2, every odd-order subgroup H of G maps trivially to G/N, so H≤N. If such H is pi-maximal in G it is automatically pi-maximal in N, and H∩N=H. The outer involution that makes the even example work cannot belong to an odd H.

The odd-order nonpronormal example of Zhang–Su–Revin 2024 is also not by itself a normal-intersection counterexample. Its ambient group is simple, so the only normal subgroups are1 and the whole group; both intersections are trivially pi-maximal in their respective normal subgroups. Nonpronormality concerns a different obstruction and does not supply the required extension.

## Verification and result

Run: python verify_controls.py. Output: control_results.json. Only336-element and21-element controls are used; no large exhaustive search. The checker verifies the controls, not any universal statement or novelty.

Remaining gap: realize a self-normalizing, nonmaximal odd pi-subgroup A as an actual normal intersection of a globally pi-maximal H, or prove that odd outer/extension actions always prohibit it. No full solution. Budget used: 4/5.
