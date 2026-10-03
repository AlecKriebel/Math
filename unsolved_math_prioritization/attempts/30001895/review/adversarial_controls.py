"""Mutation controls for the audit and frozen author verifiers, outside author files."""
from pathlib import Path
import importlib.util, json, copy, tempfile
import independent_certificate_audit as independent
S=independent.SOURCE

def load(name):
    spec=importlib.util.spec_from_file_location(name,S/(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

author8=load('verify_degree8_certificate');author9=load('verify_link_certificate')
raw8=json.loads((S/'turn5_degree8_certificate.json').read_text());raw9=json.loads((S/'turn4_link_certificate.json').read_text())
controls=[]
def test(label,num,mutate,mode):
    data=copy.deepcopy(raw8 if num==8 else raw9);mutate(data)
    with tempfile.TemporaryDirectory() as folder:
        folder=Path(folder)
        (folder/'turn4_link_certificate.json').write_text(json.dumps(data if num==9 else raw9))
        (folder/'turn5_degree8_certificate.json').write_text(json.dumps(data if num==8 else raw8))
        old=independent.SOURCE;independent.SOURCE=folder
        try:
            try:
                if mode=='trace': independent.audit_traces(data)
                else: independent.audit_graphs()
            except (ValueError,IndexError,KeyError,TypeError): own=True
            else: own=False
        finally:independent.SOURCE=old
        try:(author8 if num==8 else author9).verify(folder/('turn5_degree8_certificate.json' if num==8 else 'turn4_link_certificate.json'))
        except (AssertionError,IndexError,KeyError,TypeError): frozen=True
        else:frozen=False
        assert own and frozen,(label,own,frozen)
        controls.append({'mutation':label,'fresh_checker_rejects':own,'frozen_checker_rejects':frozen})

def bad_iso(data):
    row=next(r for r in data['link_records'] if 'diamond_image' in r[-1]);row[-1]['diamond_image']=[0]*6

def bad_trace(data):
    row=data['trace_cases'][0]['witnesses'][0];row[1]=[row[1][0]]*3

def bad_star(data):
    row=data['trace_cases'][0]['witnesses'][0];row[2]=[row[2][0]]*3

test('degree9 omitted form',9,lambda d:d['records'].pop(),'graph')
test('degree8 omitted form',8,lambda d:d['link_records'].pop(),'graph')
test('degree8 invalid diamond isomorphism',8,bad_iso,'graph')
test('degree8 omitted private-cover system',8,lambda d:d['trace_cases'].pop(),'trace')
test('degree8 omitted trace-family packing',8,lambda d:d['trace_cases'][0]['witnesses'].pop(),'trace')
test('degree8 repeated nonstar trace index',8,bad_trace,'trace')
test('degree8 repeated star edge index',8,bad_star,'trace')
print(json.dumps({'controls':controls,'passed':True},indent=2))
