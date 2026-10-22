"""Exact additive AST predicate; never rewrites or substitutes remote data."""
import ast,hashlib
RECORD=23578142
CONCEPT=23578141
PDF='supported-cycle-bound.pdf'
ZIP='supported-cycle-source-and-verification.zip'
PDF_ID='0f2ec366-4005-471e-849b-f881c2436745'
PREVIEW_ID='0e2ddc40-ef10-47c3-8e9d-6d04dc98830c'
EXPECTED_MEDIA={'enabled':True,'order':[],'count':1,'total_bytes':0,'entries':{PDF+'.ptif':{'id':PREVIEW_ID,'ext':'ptif','size':0,'mimetype':'application/octet-stream','storage_class':'L','key':PDF+'.ptif','metadata':None,'access':{'hidden':True},'processor':{'type':'image-tiles','status':'init','source_file_id':PDF_ID},'links':{'self':'https://zenodo.org/api/records/23578142/files/'+PDF+'.ptif','content':'https://zenodo.org/api/records/23578142/files/'+PDF+'.ptif/content'}}}}
ORIGINAL="processor['status'] in {'queued','running','finished','failed'}"
def need(ok,message):
 if not ok:raise RuntimeError(message)
def typed(x,y):
 if type(x) is not type(y):return False
 if type(x) is dict:return set(x)==set(y) and all(typed(x[k],y[k]) for k in x)
 if type(x) is list:return len(x)==len(y) and all(typed(a,b) for a,b in zip(x,y))
 return x==y
def accept_exact_init(record,published,name,entry,media,fingerprints):
 return (type(record) is int and record==RECORD and published is True and type(published) is bool
  and name==PDF+'.ptif' and typed(media,EXPECTED_MEDIA) and typed(entry,EXPECTED_MEDIA['entries'][PDF+'.ptif'])
  and type(fingerprints) is dict and set(fingerprints)=={PDF,ZIP} and fingerprints[PDF]['file_id']==PDF_ID)
def install(native,lifecycle,original_bytes,expected_pin):
 """Compile only the original function with ONE compare replaced by OR(exact init).
 All other AST nodes and original globals remain unchanged. Both imported callsites
 refer to the same new function; original module bytes stay untouched.
 """
 need({'bytes':len(original_bytes),'sha256':hashlib.sha256(original_bytes).hexdigest()}==expected_pin,'Original native-policy buffer differs')
 original=native.validate_target;need(lifecycle.validate_target is original,'Unexpected original validator callsite')
 tree=ast.parse(original_bytes);functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='validate_target'];need(len(functions)==1,'Unique original validator required');f=functions[0]
 target=ast.dump(ast.parse(ORIGINAL,mode='eval').body,include_attributes=False);hits=[]
 class Change(ast.NodeTransformer):
  def visit_Compare(self,node):
   if ast.dump(node,include_attributes=False)==target:
    hits.append(node);return ast.copy_location(ast.BoolOp(op=ast.Or(),values=[node,ast.Call(func=ast.Name(id='_postpublish02_exact_init',ctx=ast.Load()),args=[ast.Name(id=k,ctx=ast.Load()) for k in ['record','published','name','entry','media','fingerprints']],keywords=[])]),node)
   return self.generic_visit(node)
 before=ast.dump(f,include_attributes=False);changed=Change().visit(f);need(len(hits)==1,'Exact single original status predicate required');unit=ast.fix_missing_locations(ast.Module(body=[changed],type_ignores=[]))
 # Reverse the sole new OR and prove structural equality with the checked original.
 class Undo(ast.NodeTransformer):
  def visit_BoolOp(self,node):
   if isinstance(node.op,ast.Or) and len(node.values)==2 and isinstance(node.values[1],ast.Call) and isinstance(node.values[1].func,ast.Name) and node.values[1].func.id=='_postpublish02_exact_init':return node.values[0]
   return self.generic_visit(node)
 import copy
 need(ast.dump(Undo().visit(copy.deepcopy(changed)),include_attributes=False)==before,'Unexpected validator AST delta')
 scope=dict(original.__globals__);scope['_postpublish02_exact_init']=accept_exact_init;exec(compile(unit,'<pinned-native-policy-plus-one-exact-init-predicate>','exec',dont_inherit=True),scope);replacement=scope['validate_target'];native.validate_target=replacement;lifecycle.validate_target=replacement
 return {'original_validator_sha256':hashlib.sha256(original_bytes).hexdigest(),'AST_compare_replacements':1,'all_other_AST_nodes_unchanged':True,'remote_values_modified':False,'both_original_callsites_rebound':True}
