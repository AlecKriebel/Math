#!/usr/bin/env python3
"""Data-integrity check against the complete frozen primary HTML tables."""
import re,html,json,pathlib,hashlib,ast
from check_triangulation import V,C,normal,inner,minus,vector
root=pathlib.Path(__file__).resolve().parent.parent
data=(root/'local_sources/mizhaev-v1.html').read_bytes()
s=data.decode()
def rows(table_id):
    t=re.search(r'<table id="'+re.escape(table_id)+r'".*?</table>',s,re.S).group()
    t=re.sub(r'<annotation\b.*?</annotation>','',t,flags=re.S)
    return [[html.unescape(re.sub('<[^>]+>','',c)).strip()
             for c in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',r,re.S)]
             for r in re.findall(r'<tr\b[^>]*>(.*?)</tr>',t,re.S)]
table1=rows('S4.T1.2');verts={}
for row in table1:
    if len(row)==8 and row[0].isdigit():
        q=[int(x.replace('−','-')) for x in row]
        verts[q[0]]=tuple(q[1:4]);verts[q[4]]=tuple(q[5:8])
assert len(verts)==24 and [verts[i] for i in range(1,25)]==V
table_ids=re.findall(r'<table id="([^"]+)"',s)
face_id=next(x for x in table_ids if x.startswith('S4.T2'))
table2=rows(face_id)
walks=[]
for row in table2:
    if len(row)==2 and row[1] and row[1][0].isdigit():
        walks.append([int(x)-1 for x in row[1].replace('−','-').split('-')])
assert walks==C
code=ast.parse((root/'author/verify_witness.py').read_text())
planes=next(ast.literal_eval(n.value) for n in code.body if isinstance(n,ast.Assign)
            and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='PLANES')
assert planes==[(21,3,-10,-1440),(21,3,10,1440),(3,0,1,234),
               (3,0,-1,-234),(0,3,-1,234),(0,3,1,-234),
               (3,-21,10,-1440),(3,-21,-10,1440)]
for p,c in zip(planes,C):
    assert all(inner(p[:3],V[i])==p[3] for i in c)
    assert not any(vector(p[:3],normal([V[i] for i in c])))
print(json.dumps(dict(status='PASS',coordinate_entries_checked=72,face_walk_entries_checked=72,
    plane_equations_checked=8,source_html_sha256=hashlib.sha256(data).hexdigest()),indent=2))
