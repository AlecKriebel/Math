"""Seal independent correction mechanism before reading auditor variant code."""
from pathlib import Path
from html.parser import HTMLParser
import ast,datetime,difflib,hashlib,json
O=Path(__file__).resolve().parent;P=O.parents[1];S=P/'verification/local-spanning-sos-gin-stage-sol-20261025';C=P/'verification/spanning-sos-gin-checker-correction-root-20261025';A=P/'verification/audit-spanning-sos-gin-code-sol-20261025'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
if (O/'EARLY_MECHANISM_SEAL.json').exists():raise RuntimeError('preserve_early_mechanism')
scope=json.loads((C/'SCOPE.json').read_text());old=(S/'final-content-check.proposed.py').read_text();new=(C/'final-content-check.proposed.py').read_text()
if sha(C/'final-content-check.proposed.py')!='aceef187f34f5d1029a19e4e2e9b2b15472535a07cf224134adbd2ddb16fd6c4' or sha(S/'final-content-check.proposed.py')!=scope['original_checker_sha256']:raise RuntimeError('exact_root_and_original_input_hash')
ops=[x for x in difflib.SequenceMatcher(a=old.splitlines(True),b=new.splitlines(True),autojunk=False).get_opcodes() if x[0]!='equal']
if len(ops)!=1 or ops[0][0]!='insert':raise RuntimeError('one_insertion_required')
_,i,j,k,l=ops[0];lines=new.splitlines(True);stripped=''.join(lines[:k]+lines[l:])
if l-k!=13 or stripped!=old or ast.dump(ast.parse(stripped),include_attributes=False)!=ast.dump(ast.parse(old),include_attributes=False):raise RuntimeError('13_line_exact_excision')
guards=[n for n in ast.walk(ast.parse(new)) if isinstance(n,ast.If) and ast.unparse(n.test)=='rid in SG_IDS' and n.lineno<=k+1<=l<=n.end_lineno]
if len(guards)!=1:raise RuntimeError('one_SG_IDS_guard')
frozen=json.loads((S/'FROZEN_INPUT_SET.json').read_text());ids=frozen['authorized_new_record_ids'];oldids=frozen['old_configured_record_ids_in_order']
if len(oldids)!=61 or set(oldids)&set(ids):raise RuntimeError('old61_disjoint')
class Body(HTMLParser):
    def __init__(self,text):super().__init__(convert_charrefs=True);self.depth=0;self.bodies=0;self.skip=0;self.parts=[];self.h1=False;self.headings=[];self.current_h1=[];self.anchor=None;self.links=[];self.feed(text)
    def handle_starttag(self,t,a):
        if t=='body':self.depth+=1;self.bodies+=1
        if not self.depth:return
        if t in ['script','style']:self.skip+=1
        if self.skip:return
        self.parts.append(' ')
        if t=='h1':self.h1=True;self.current_h1=[]
        if t=='a':self.anchor=[dict(a).get('href'),[]]
    def handle_endtag(self,t):
        if not self.depth:return
        if t in ['script','style']:self.skip-=1;return
        if self.skip:return
        self.parts.append(' ')
        if t=='h1':self.h1=False;self.headings.append(' '.join(''.join(self.current_h1).split()))
        if t=='a' and self.anchor:self.links.append([self.anchor[0],' '.join(''.join(self.anchor[1]).split())]);self.anchor=None
        if t=='body':self.depth-=1
    def handle_data(self,text):
        if self.depth and not self.skip:
            self.parts.append(text)
            if self.h1:self.current_h1.append(text)
            if self.anchor:self.anchor[1].append(text)
    def handle_comment(self,text):pass
checks=[]
for rid in ids:
    c=json.loads((P/'papers'/rid/'publication.json').read_text());path=S/'public/research'/c['slug']/'index.html';parser=Body(path.read_text());normalized=' '.join(''.join(parser.parts).split());digest=hashlib.sha256(normalized.encode()).hexdigest();ref=scope['actual_approved_rendered_body_bindings'][rid]
    if sha(path)!=ref['actual_rendered_HTML_sha256'] or digest!=ref['normalized_whole_body_text_sha256'] or parser.bodies!=1 or parser.headings!=[c['title']]:raise RuntimeError('independent_actual_body_contract:'+rid)
    if rid=='23395703' and parser.links.count(['https://zenodo.org/api/records/23395703/files/seven_plane_gin.tex/content','Zenodo original published TeX source'])!=1:raise RuntimeError('independent_Gin_TeX_link_label')
    checks.append({'record_id':rid,'actual_HTML_SHA256':sha(path),'independent_HTMLParser_body_text_SHA256':digest,'exact_h1':parser.headings,'actual_body_count':parser.bodies,'matches_fixed_approved_hash':True})
protected=set(p for base in [S,C] for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for x in json.loads((S/'protected-before.json').read_text())['files']:protected.add(Path(x['path']))
save('protected-before.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':str(p),'bytes':p.stat().st_size,'SHA256':sha(p)} for p in sorted(protected)],'scope':'Current immutable3stage/current492 source/core custody plus exact root correction; no historical1113 maps followed.'})
(O/'inputs').mkdir(exist_ok=True)
for n in ['final-content-check.proposed.py','checker-only.diff','SCOPE.json']:(O/'inputs'/n).write_bytes((C/n).read_bytes())
(O/'inserted-guard.txt').write_text(''.join(lines[k:l]))
record={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'INDEPENDENT_MECHANISM_COMPLETE_BEFORE_AUDITOR_VARIANT_CODE_READ','root_corrected_checker_SHA256':sha(C/'final-content-check.proposed.py'),'one_13_line_insertion_inside_existing_SG_IDS':True,'exact_excision_restores_original_bytes_and_AST':True,'old61_IDs_disjoint':True,'old61_record_ids':oldids,'independent_whole_body_hash_h1_and_Gin_link_checks':checks,'mechanism':'Require exactly one normal body and its fixed approved normalized text hash; independently require exactly one expected h1 and the exact visible Gin original-TeX label. Existing source/metadata/section/attribute checks remain intact. Direct test() comparisons remain active under -O.','text_contract_limits':['Whitespace and entities are normalized; comments and script/style bodies are excluded.','Fixed current approved article text; any future template/body/copyright revision needs separate approval and fresh hashes.','Does not prove arbitrary CSS visibility, accessibility rendering, browser behavior, JavaScript effects, malformed/hostile parser equivalence, or all head/attribute/PDF invariants. Those are separate existing checks or later gates.'],'auditor_variant_code_read':False,'full_old61_suite_rerun':False,'completion_estimate_percent':35,'overall203_complete':False}
save('EARLY_MECHANISM.json',record);save('EARLY_MECHANISM_SEAL.json',{'status':'IMMUTABLE_EARLY_INDEPENDENT_BODY_CONTRACT_RECONSTRUCTION','EARLY_MECHANISM_SHA256':sha(O/'EARLY_MECHANISM.json'),'root_guard_SHA256':record['root_corrected_checker_SHA256'],'auditor_variant_code_not_read':True})
(O/'RESEARCH_LOG.md').write_text('* '+record['UTC']+' — Entire root diff/current SG block read. One13-line guarded insertion/exact byte+AST excision verified. Independent HTMLParser reconstructs all3 fixed body hashes, exact h1 and Gin label. Early mechanism sealed before auditor variant code. Completion estimate35%.\n')
print(json.dumps({'status':record['status'],'early_seal_SHA256':sha(O/'EARLY_MECHANISM_SEAL.json'),'auditor_seal_files_currently_present':[n for n in ['FINAL_SEAL.json','SEAL.json','SEAL.sha256'] if (A/n).is_file()]},indent=2))
