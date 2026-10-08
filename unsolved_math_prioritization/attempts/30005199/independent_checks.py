#!/usr/bin/env python3
"""Independent exact finite controls for the KK application; not analytic certification."""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import os, stat, unittest

def mat(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)
def eye(n): return mat([[int(i == j) for j in range(n)] for i in range(n)])
def zero(n): return mat([[0] * n for _ in range(n)])
def add(a,b): return tuple(tuple(x+y for x,y in zip(r,s)) for r,s in zip(a,b))
def neg(a): return tuple(tuple(-x for x in r) for r in a)
def sub(a,b): return add(a,neg(b))
def mm(a,b):
    if len(a[0]) != len(b): raise ValueError('matrix dimension mismatch')
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))) for i in range(len(a)))
def star(a): return tuple(zip(*a))
def diag(*entries): return mat([[x if i == j else 0 for j in range(len(entries))] for i,x in enumerate(entries)])
def block(a,b,c,d): return tuple(tuple(x+y) for x,y in zip(a,b))+tuple(tuple(x+y) for x,y in zip(c,d))
def conjugate(u,x): return mm(mm(u,x),star(u))
def ncadd(*ps):
    r=defaultdict(F)
    for p in ps:
        for w,c in p.items(): r[w]+=c
    return {w:c for w,c in r.items() if c}
def ncmul(a,b):
    r=defaultdict(F)
    for w,c in a.items():
        for v,d in b.items(): r[w+v]+=c*d
    return {w:c for w,c in r.items() if c}
def ncneg(p): return {w:-c for w,c in p.items()}

class ApplicationChecks(unittest.TestCase):
    def test_01_noncommutative_error_and_missing_term_negative(self):
        one={():F(1)}
        d,ds,x,y=({(s,):F(1)} for s in ('d','d*','x','y'))
        lhs=ncadd(ncmul(ncmul(ncadd(one,d),x),ncadd(one,ds)),ncneg(y))
        partial=ncadd(x,ncneg(y),ncmul(d,x),ncmul(x,ds))
        self.assertEqual(lhs,ncadd(partial,ncmul(ncmul(d,x),ds)))
        self.assertNotEqual(lhs,partial)

    def test_02_nonessential_error_norm_is_preserved_inside_ideal(self):
        # E=M2 direct-sum C, D=M2 direct-sum 0; lambda discards C.
        u=mat([[0,-1],[1,0]]); x=diag(1,3); y=diag(2,5)
        err=sub(conjugate(u,x),y)
        self.assertEqual(err,diag(1,-4))
        self.assertEqual(max(abs(err[0][0]),abs(err[1][1]),F(0)),F(4))
        self.assertEqual(max(abs(err[0][0]),abs(err[1][1])),F(4))

    def test_03_multiplier_equality_without_ideal_difference_negative(self):
        # Phi(z)=(z I, z), Psi(z)=(z I,0) are *-maps C -> M2 direct-sum C.
        # Same multiplier images, but the ambient maps remain distance one at 1.
        phi=(eye(2),F(1)); psi=(eye(2),F(0))
        self.assertEqual(phi[0],psi[0])
        self.assertNotEqual(phi[1],psi[1])
        self.assertEqual(abs(phi[1]-psi[1]),F(1))

    def test_04_corner_lift_and_omitted_complement_negative(self):
        p=diag(1,1,0); w=mat([[0,-1,0],[1,0,0],[0,0,0]])
        lift=add(w,sub(eye(3),p))
        self.assertEqual(mm(w,star(w)),p)
        self.assertNotEqual(mm(w,star(w)),eye(3))
        self.assertEqual(mm(lift,star(lift)),eye(3))
        self.assertEqual(mm(star(lift),lift),eye(3))

    def test_05_compression_does_not_destabilize(self):
        u=mat([[F(3,5),F(-4,5)],[F(4,5),F(3,5)]])
        self.assertEqual(mm(u,star(u)),eye(2))
        self.assertEqual(u[0][0]**2,F(9,25))
        self.assertNotEqual(u[0][0]**2,F(1))

    def test_06_range_projection_typo_is_genuinely_false(self):
        s=mat([[F(3,5),F(-4,5)],[F(4,5),F(3,5)]])
        correct=mm(s,star(s)); printed=mm(star(s),star(s))
        self.assertEqual(correct,eye(2))
        self.assertEqual(mm(correct,correct),correct)
        self.assertNotEqual(printed,star(printed))
        self.assertNotEqual(mm(printed,printed),printed)

    def test_07_forcing_initial_unitary_one_changes_conjugacy(self):
        # This refutes a naive normalization, not a uniqueness theorem.
        w=mat([[0,-1],[1,0]]); x=diag(1,2); y=conjugate(w,x)
        normalized=mm(w,star(w))
        self.assertEqual(normalized,eye(2))
        self.assertNotEqual(conjugate(normalized,x),y)
        self.assertEqual(conjugate(w,x),y)

    def test_08_reverse_path_by_adjoint(self):
        u=mat([[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]); x=diag(2,7)
        y=conjugate(u,x)
        self.assertEqual(conjugate(star(u),y),x)

    def test_09_technical_rotation_and_swap(self):
        n=diag(1,0); m=diag(0,1); z=zero(2)
        u=block(n,m,neg(m),n)
        x=diag(7,2); y=diag(7,5)
        self.assertEqual(add(mm(n,n),mm(m,m)),eye(2))
        self.assertEqual(mm(u,star(u)),eye(4))
        self.assertEqual(mm(n,sub(x,y)),zero(2))
        self.assertEqual(conjugate(u,block(x,z,z,y)),block(y,z,z,x))

    def test_10_wrong_rotation_sign_is_not_unitary(self):
        n=diag(F(3,5),F(3,5)); m=diag(F(4,5),F(4,5))
        good=block(n,m,neg(m),n); bad=block(n,m,m,n)
        self.assertEqual(mm(good,star(good)),eye(4))
        self.assertNotEqual(mm(bad,star(bad)),eye(4))

    def test_11_quotient_unitary_lift_is_only_contractive_upstairs(self):
        # E=M2 direct-sum M2, quotient is second summand, W=(0,1).
        w=(zero(2),eye(2))
        wstarw=(mm(star(w[0]),w[0]),mm(star(w[1]),w[1]))
        self.assertEqual(wstarw[1],eye(2))
        self.assertNotEqual(wstarw,(eye(2),eye(2)))
        self.assertEqual(sub(wstarw[1],eye(2)),zero(2))

    def test_12_delayed_telescoping_indices(self):
        m={-1:0,0:0,1:3,2:6,3:9,4:12}
        # Scalar symbols e_j=j suffice to test the telescoping algebra only.
        correct=sum(F(m[k-1]-m[k-2]) for k in range(1,5))
        wrong=sum(F(m[k]-1-(m[k]-2)) for k in range(1,5))
        self.assertEqual(correct,F(m[3]))
        self.assertNotEqual(wrong,correct)

    def test_13_fixed_dyadic_margin(self):
        for n in range(1,101):
            s=sum((F(1,2**k) for k in range(1,n+1)),F())
            self.assertEqual(s*s,(1-F(1,2**n))**2)
            # One strict term supplies a fixed gap in the infinite majorant.
            self.assertLessEqual(s*s-F(1,16),F(15,16))
        self.assertEqual(sum((F(1,2**k) for k in range(1,101)),F())+F(1,2**100),F(1))

    def test_14_small_terms_without_summability_negative(self):
        self.assertLess(F(1,16),F(1))
        self.assertGreater(sum((F(1,16) for _ in range(25)),F()),F(1))

    def test_15_projection_defect_obstructs_absorbing_zero(self):
        p=diag(1,0); swap=mat([[0,1],[1,0]])
        defect=sub(eye(2),conjugate(swap,p))
        self.assertEqual(defect,diag(1,0))
        self.assertEqual(max(abs(defect[0][0]),abs(defect[1][1])),F(1))

    def test_16_actual_unprivileged_read_only_execution(self):
        f=Path(__file__).resolve(); directory=f.parent
        self.assertNotEqual(os.getuid(),0); self.assertNotEqual(os.geteuid(),0)
        self.assertEqual(os.getuid(),1000); self.assertEqual(os.geteuid(),1000)
        self.assertEqual(stat.S_IMODE(f.stat().st_mode),0o444)
        self.assertEqual(stat.S_IMODE(directory.stat().st_mode),0o555)
        self.assertFalse(os.access(f,os.W_OK)); self.assertFalse(os.access(directory,os.W_OK))
        with self.assertRaises(PermissionError):
            with f.open('ab'):
                pass
        probe=directory/'WRITE_PROBE_MUST_NOT_EXIST'
        with self.assertRaises(PermissionError):
            with probe.open('xb'):
                pass
        self.assertFalse(probe.exists())

if __name__ == '__main__':
    print('UID=%d EUID=%d; exact finite controls only; no analytic theorem certificate.' % (os.getuid(),os.geteuid()),flush=True)
    unittest.main(verbosity=2)
