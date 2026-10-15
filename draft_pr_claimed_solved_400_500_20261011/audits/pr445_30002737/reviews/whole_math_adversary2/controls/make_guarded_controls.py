#!/usr/bin/env python3
"""Preserve the normal-only checkpoint; author a separately guarded version."""
from pathlib import Path
import ast,hashlib,json

ROOT=Path(__file__).resolve().parent
source=ROOT/'independent_whole_controls.py'
if hashlib.sha256(source.read_bytes()).hexdigest()!='7e2229db5fc79b13d3f2ce897a7b9b7c1307a00bbaccbb77582ebbdc729a91c3':
    raise ValueError('historical diagnostic changed')
text=source.read_text()
replacements=[
 ('import hashlib, json, math','import hashlib, json, math, argparse\nFAULT = None'),
 ("def main():\n", "def main():\n    global FAULT, SLOTS\n    parser=argparse.ArgumentParser()\n    parser.add_argument('--diagnostic-fault',choices=['marker','physical_pairs','section'])\n    FAULT=parser.parse_args().diagnostic_fault\n    if FAULT=='marker': SLOTS=((0,0),(5,0),(10,0),(0,10))\n"),
 ('            exact=independent_pair_count(crop,r,xs,ys)','            if FAULT==\'physical_pairs\':direct+=1\n            exact=independent_pair_count(crop,r,xs,ys)'),
 ('    return sum((b-a) for a,b in zip(cuts,cuts[1:]) if math.floor((a+b)/2+t)==0)',
  '    answer=sum((b-a) for a,b in zip(cuts,cuts[1:]) if math.floor((a+b)/2+t)==0)\n    return 2*answer if FAULT==\'section\' else answer'),
 ("'independent_whole_controls_results.json'", "'independent_whole_controls_guarded_results.json'")]
for old,new in replacements:
    if text.count(old)!=1:raise ValueError('ambiguous authoring replacement')
    text=text.replace(old,new)
class GuardAssertions(ast.NodeTransformer):
    def visit_Assert(self,node):
        message=node.msg or ast.Constant('Independent explicit guard failed: '+ast.unparse(node.test))
        return ast.copy_location(ast.Expr(ast.Call(ast.Name('require',ast.Load()),[node.test,message],[])),node)
tree=GuardAssertions().visit(ast.parse(text))
guard=ast.parse('def require(condition,message):\n    if not condition:raise ValueError(message)\n').body[0]
tree.body.insert(1,guard)
ast.fix_missing_locations(tree)
target=ROOT/'independent_whole_controls_guarded.py'
target.write_text('#!/usr/bin/env python3\n'+ast.unparse(tree)+'\n')
if any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(target.read_text()))):raise ValueError('assert remains')
print(json.dumps({'preserved_normal_only_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                 'new_explicit_guard_sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))
