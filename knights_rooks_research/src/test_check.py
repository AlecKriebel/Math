#!/usr/bin/env python3
import copy, json, unittest
from pathlib import Path
from check import inspect
ROOT = Path(__file__).resolve().parents[1]

class DefinitionTests(unittest.TestCase):
    def setUp(self):
        self.example = json.loads((ROOT/'data/source_N1R1.json').read_text())
    def test_source_example(self):
        r=inspect(self.example,1,1)
        self.assertTrue(r['valid'],r['errors'])
        self.assertEqual(sum(len(a['attacks_rooks']) for a in r['attacks'] if a['piece']=='K'),2)
    def test_source_is_not_target(self):
        self.assertFalse(inspect(self.example)['valid'])
    def test_missing_rook(self):
        d=copy.deepcopy(self.example);d['rooks'].pop()
        self.assertFalse(inspect(d,1,1)['valid'])
    def test_added_rook_attack(self):
        d=copy.deepcopy(self.example);d['rooks'].append([0,1])
        r=inspect(d,1,1)
        self.assertFalse(r['valid'])
        self.assertTrue(any(a['attacks_rooks'] for a in r['attacks'] if a['piece']=='R'))
    def test_added_knight_attack(self):
        d=copy.deepcopy(self.example);d['knights'].append([0,2])
        r=inspect(d,1,1)
        self.assertFalse(r['valid'])
        self.assertTrue(any(a['attacks_knights'] for a in r['attacks'] if a['piece']=='K'))
    def test_first_occupied_stops_ray(self):
        d={'knights':[[1,0],[2,0]],'rooks':[[0,0],[3,0]]}
        r=inspect(d,0,1)
        self.assertTrue(r['valid'],r['errors'])
        self.assertEqual(r['attacks'][2]['attacks_knights'],[(1,0)])
        self.assertEqual(r['attacks'][2]['attacks_rooks'],[])
    def test_knights_jump(self):
        d={'knights':[[0,0]],'rooks':[[1,0],[1,1],[2,1]]}
        r=inspect(d,1,0)
        self.assertEqual(r['attacks'][0]['attacks_rooks'],[(2,1)])
    def test_overlap_rejected(self):
        d=copy.deepcopy(self.example);d['rooks'].append([1,0])
        with self.assertRaises(ValueError):inspect(d)
    def test_duplicate_rejected(self):
        d=copy.deepcopy(self.example);d['knights'].append([1,0])
        with self.assertRaises(ValueError):inspect(d)
    def test_noninteger_rejected(self):
        d=copy.deepcopy(self.example);d['knights'][0]=[1.5,2]
        with self.assertRaises(ValueError):inspect(d)
    def test_empty_rejected(self):
        d=copy.deepcopy(self.example);d['knights']=[]
        with self.assertRaises(ValueError):inspect(d)

if __name__=='__main__':unittest.main(verbosity=2)
