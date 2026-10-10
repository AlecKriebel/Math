# Exact v1-to-v2 proof delta

Only the three required edits from the independent audit correction were applied. No optional prose changes, theorem changes, new proof attempts, or code changes were made.

```diff
--- v1/PROOF.md
+++ v2/PROOF.md
@@ -133,11 +133,11 @@
     M_x ≥ ∫_(B(x,r)∩X) |Df^n|^κ dν
         ≥ (a_x/r)^κ ν(B(x,r)∩X).
 
-Consequently ν(B(x,r))≤C_x r^κ for all sufficiently small r, with C_x=M_x/a_x^κ. One can replace X₀ by the countable union of sets E_j on which C_x≤j and r_x≥1/j. If A is H^κ-null, cover A by sets U_i of positive diameter d_i<1/(2j), with Σ_i d_i^κ arbitrarily small. For each U_i meeting A∩E_j choose x_i in that intersection. Then U_i⊂B(x_i,2d_i), and
+Consequently ν(B(x,r))≤C_x r^κ for all sufficiently small r, with C_x=M_x/a_x^κ. One can replace X₀ by the countable union of sets E_j on which C_x≤j and r_x≥1/j. If A is H^κ-null, cover A by sets U_i of diameters 0≤d_i<1/(2j), with Σ_i d_i^κ arbitrarily small. For each positive-diameter U_i meeting A∩E_j choose x_i in that intersection. Then U_i⊂B(x_i,2d_i), and
 
     ν*(A∩E_j) ≤ Σ_i ν(B(x_i,2d_i)) ≤ j 2^κ Σ_i d_i^κ.
 
-Thus ν*(A∩E_j)=0. Singleton members can be replaced by arbitrarily small positive-diameter balls; the growth estimate rules out atoms on E_j. Countable union and the conull property give ν(A)=0, hence m(A)=0. ∎
+Thus ν*(A∩E_j)=0. Any zero-diameter cover member meeting A∩E_j is a singleton {x} with x∈E_j, and ν({x})≤j r^κ for every 0<r<1/j, so ν({x})=0. There are at most countably many such members. Discard their zero-mass contribution and apply the preceding estimate to the positive-diameter members. Countable union and the conull property give ν(A)=0, hence m(A)=0. ∎
 
 Here ν* is the outer measure induced by ν. Consequently no measurable selection of n(x,r), a_x, M_x, or r_x is needed, and the E_j need not themselves be measurable.
 
```
