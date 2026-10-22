"""Two additional exact predecessor comparisons. Standard library; no writes.
Reuses authenticated polynomial/rank routines from the earlier priority audit.
"""
from pathlib import Path
import argparse,ast,hashlib,json

def reconstruct():
    source=Path(__file__).resolve().parent.parent/'priority_audit_01/compare_known_examples.py'
    raw=source.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='b2fcfaca9dcd5230e564021fa7f9e6bc9140d93f78a0d731a1efab24745f2e1c'
    tree=ast.parse(raw)
    stop=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='examples' for x in n.targets))
    scope={}
    exec(compile(ast.Module(body=tree.body[:stop],type_ignores=[]),str(source),'exec'),scope)
    analyze=scope['analyze']
    nn=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[0,1,0,1],[0,0,1,1],[-1,1,0,1],[-1,0,1,1],[-1,1,1,1]]
    walther=[[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,1,0,0],[1,0,1,0],[1,0,0,1],[1,1,1,0],[1,1,0,1],[1,0,1,1]]
    return {
        'NN_SIMIS_SECTIONAL_CERTIFICATE.json':analyze('Nasrollah Nejad–Simis2026 Example3.4',nn,[[1,0,0],[0,1,0],[0,0,1],[1,2,3]],[[1,0],[0,1],[2,3],[7,11]],[8,9,10]),
        'WALTHER_SECTIONAL_CERTIFICATE.json':analyze('Walther2017 Example5.7 bracelet',walther,[[1,0,0],[0,1,0],[0,0,1],[5,11,23]],[[1,0],[0,1],[13,29],[304,678]],[8,9,10])}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    data=reconstruct()
    for name,r in data.items():
        assert r['normal_rank']==4
        for d,values in [('2',{8:5,9:2,10:0}),('3',{8:41,9:43,10:42})]:
            assert r['sections'][d]['pairwise_nonproportional'] is True
            for k,v in values.items():
                m=r['sections'][d]['macaulay'][str(k)]
                assert m['quotient_hilbert_function']==v
                assert m['rank']==min(m['rows'],m['columns'])
        if args.verify:assert json.loads((Path(__file__).resolve().parent/name).read_bytes())==r,name
    if args.verify:print(json.dumps({'verified':True,'examples':2,'binary_cutoffs':[10,10],'earlier_largest_third_variable_generators':[False,False],'writes':False}))
    else:print(json.dumps(data,indent=2))

if __name__=='__main__':main()
