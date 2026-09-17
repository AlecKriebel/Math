#!/usr/bin/env python3
import copy,hashlib,itertools,json,random,tempfile,unittest
from pathlib import Path
from check import inspect
from check_sorted import reconstruct
from verify_unsat import verify
from local_cnf import build
from dpll_prove import solve
ROOT=Path(__file__).resolve().parents[1]

class IndependentVerification(unittest.TestCase):
    def test_published_examples_both_checkers(self):
        for f,n,m in [('source_N1R1.json',1,1),('source_N4R1.json',4,1)]:
            d=json.loads((ROOT/'data'/f).read_text());a=inspect(d,n,m);b=reconstruct(d,n,m)
            self.assertTrue(a['valid']);self.assertTrue(b['valid']);self.assertEqual(a['attacks'],b['attacks'])
    def test_source_gif_bytes(self):
        for name,expected in [('N1R1','c5a73fb1608603107683f8c176b06111a08b2771'),('N4R1','34035bef1f04e6e53fed5371998111e70ad0422a')]:
            b=(ROOT/'sources'/f'{name}.gif').read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),expected)
    def test_directed_counts_need_not_balance(self):
        d=json.loads((ROOT/'data/5x5_N2R3_none_p0_s1_candidate.json').read_text())
        a=inspect(d,2,3);b=reconstruct(d,2,3)
        self.assertTrue(a['valid']);self.assertEqual(a['attacks'],b['attacks'])
        out_k=sum(len(x['attacks_rooks']) for x in a['attacks'] if x['piece']=='K')
        out_r=sum(len(x['attacks_knights']) for x in a['attacks'] if x['piece']=='R')
        self.assertEqual((out_k,out_r),(16,18))
    def test_2000_random_attack_reconstructions(self):
        rng=random.Random(20260913);board=list(itertools.product(range(-4,5),repeat=2))
        for _ in range(2000):
            sample=rng.sample(board,rng.randrange(2,35));cut=rng.randrange(1,len(sample))
            d={'knights':sample[:cut],'rooks':sample[cut:]}
            a=inspect(d);b=reconstruct(d)
            self.assertEqual(a['valid'],b['valid']);self.assertEqual(a['attacks'],b['attacks'])
    def test_translations_and_dihedral_symmetries(self):
        d=json.loads((ROOT/'data/source_N4R1.json').read_text())
        for flip_x,flip_y,swap in itertools.product((False,True),repeat=3):
            def tr(p):
                x,y=p
                if swap:x,y=y,x
                return [(-x if flip_x else x)+1000,(-y if flip_y else y)-2718]
            q={'knights':list(map(tr,d['knights'])),'rooks':list(map(tr,d['rooks']))}
            self.assertTrue(inspect(q,4,1)['valid']);self.assertTrue(reconstruct(q,4,1)['valid'])
    def test_cnf_reproduces_exact_bytes(self):
        c=build();s=f'p cnf {len(c.names)} {len(c.clauses)}\n'+''.join(' '.join(map(str,a))+' 0\n' for a in c.clauses)
        self.assertEqual(s,(ROOT/'certificates/local_relaxation.cnf').read_text())
    def test_unsat_certificate(self):
        stats=verify(ROOT/'certificates/local_relaxation.cnf',ROOT/'certificates/local_unsat_tree.json')
        self.assertEqual(stats,{'nodes':3,'unit_steps':151,'conflicts':2,'splits':1})
    def test_corrupt_certificates_rejected(self):
        orig=json.loads((ROOT/'certificates/local_unsat_tree.json').read_text())
        altered=[]
        a=copy.deepcopy(orig);a['cnf_sha256']='0'*64;altered.append(a)
        a=copy.deepcopy(orig);a['tree']['units'][0][0]*=-1;altered.append(a)
        a=copy.deepcopy(orig);a['tree']['split']=abs(a['tree']['units'][0][0]);altered.append(a)
        a=copy.deepcopy(orig);a['tree']['true']['conflict']=0;altered.append(a)
        a=copy.deepcopy(orig);del a['tree']['false'];altered.append(a)
        with tempfile.TemporaryDirectory() as tmp:
            for i,cert in enumerate(altered):
                p=Path(tmp)/f'bad{i}.json';p.write_text(json.dumps(cert))
                with self.assertRaises((ValueError,KeyError)):
                    verify(ROOT/'certificates/local_relaxation.cnf',p)
    def test_sat_controls(self):
        c=build()
        variants={
            'remove_rook_ray_cap':[cl for cl,r in zip(c.clauses,c.reasons) if 'at most 2 locally occupied rays' not in r],
            'remove_rook_nonattack':[cl for cl,r in zip(c.clauses,c.reasons) if not r.startswith('rooks ')],
            'remove_knight_degree_requirements':[cl for cl,r in zip(c.clauses,c.reasons) if 'at least 4 rook targets' not in r]
        }
        for name,clauses in variants.items():
            tree=solve(clauses,{},[19]);self.assertIn('satisfying_assignment',tree,name)
            assignment=tree['satisfying_assignment']
            self.assertTrue(all(any(assignment.get(abs(l))==(l>0) for l in cl) for cl in clauses),name)

if __name__=='__main__':unittest.main(verbosity=2)
