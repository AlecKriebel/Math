"""Small private-stage primitives. Importing this module performs no I/O."""
from pathlib import Path
import hashlib,json,re

IDS=('23124601','23333046','23383952','23539734','22929857','23320818')
OWN=Path(__file__).resolve().parent
PROGRAMME=OWN.parents[1]
WEBSITE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
PUBLIC=WEBSITE/'public'
ROOT_ADOPTION=PROGRAMME/'verification/root-six-editorial-reading-20261114/ROOT_ADOPTION.json'
ROOT_ADOPTION_SHA='1ab177bed7047c45ebbef7abddb0f2e3aced9287ac04286eb1ca7984e7e6483c'
STATUSES={
 '23124601':'PASS_WITH_CLASSICAL_IMPORTS_AND_EXPLICIT_CHECKER_RUNTIME_LIMITS',
 '23333046':'PASS_WITH_KNOWN_ANTECEDENTS_AND_EXPLICIT_UNFRAMED_CATEGORY_LIMITS',
 '23383952':'PASS_WITH_CLASSICAL_METHOD_CREDIT_AND_EXPLICIT_SOURCE_VERSION_LIMITS',
 '23539734':'PASS_AT_DECLARED_CLASSICAL_INPUT_LEVEL_WITH_EXPLICIT_PRIORITY_AND_CONVENTION_LIMITS',
 '22929857':'PASS_WITH_EXPLICIT_METRIC_CLASSICAL_METHOD_AND_PRIORITY_LIMITS',
 '23320818':'PASS_WITH_EXPLICIT_STATIC_FOLIATION_BOUNDARY_VECTOR_AND_PRIORITY_LIMITS'}
DATES=dict(zip(IDS,['2026-10-03','2026-10-12','2026-10-13','2026-10-21','2026-09-23','2026-10-12']))
VERSIONS=dict(zip(IDS,['1.0','1.0','1.0.0','1.1','1.1','1.0']))
def require(ok,label):
    if not ok:raise ValueError('six_stage:'+label)
def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def sha(data):return hashlib.sha256(data).hexdigest()
def bind(path):
    data=Path(path).read_bytes();return {'bytes':len(data),'sha256':sha(data)}
def load(path):return json.loads(Path(path).read_bytes())
def contained(root,path):
    root=Path(root).resolve();p=Path(path);p=p if p.is_absolute() else root/p
    require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),'contained_regular_file:'+str(path))
    require(all(not q.is_symlink() for q in p.parents if q!=root and q.is_relative_to(root)),'no_symlink_parent')
    return p
def safe_name(name):
    require(type(name) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*',name) and name not in {'.','..'},'safe_basename')
    return name
def safe_output(path):
    p=Path(path).absolute()
    require(p.resolve().is_relative_to(OWN.resolve()) and p.resolve()!=OWN.resolve(),'private_output_root_only')
    require(all(not x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(OWN)),'output_symlink')
    return p
def authenticate_root():
    require(bind(ROOT_ADOPTION)['sha256']==ROOT_ADOPTION_SHA,'exact_root_six_authority')
    a=load(ROOT_ADOPTION)
    require(a['allowed_records']==list(IDS) and a['allowed_private_stage_root']==str(OWN) and a['render_authorized'] is True,'private_six_render_authority')
    require(a['production_install_authorized'] is False and a['AA_writes_authorized'] is False,'root_public_gates_false')
    rows=[a['previous106_adoption'],*a['new_five_adoptions']]
    for row in rows:require(bind(contained(PROGRAMME,row['path']))['sha256']==row['sha256'],'exact_individual_root_adoption')
    return a
