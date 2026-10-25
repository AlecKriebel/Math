"""Independent guard-mechanism review before reading sealed auditor cases."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json
P=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
S=P/'verification/local-cylinder-discotope-stage-sol-20261025';C=P/'verification/cylinder-discotope-checker-correction-root-20261025';A=P/'verification/cylinder-discotope-code-audit-sol-20261025'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(O/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
if (O/'EARLY_MECHANISM_SEAL.json').exists():raise RuntimeError('preserve_early_seal')
scope=json.loads((C/'SCOPE.json').read_text());old=(S/'final-content-check.proposed.py').read_text();new=(C/'final-content-check.proposed.py').read_text()
if sha(S/'final-content-check.proposed.py')!=scope['original_checker_sha256'] or sha(C/'final-content-check.proposed.py')!=scope['new_checker_sha256']:raise RuntimeError('exact_root_input_hash')
ops=difflib.SequenceMatcher(a=old.splitlines(True),b=new.splitlines(True),autojunk=False).get_opcodes();changed=[x for x in ops if x[0]!='equal']
if len(changed)!=1 or changed[0][0]!='insert':raise RuntimeError('only_one_insertion_required')
tag,i,j,k,l=changed[0];lines=new.splitlines(True);addition=''.join(lines[k:l]);stripped=''.join(lines[:k]+lines[l:])
if stripped!=old or l-k!=15:raise RuntimeError('excision_must_restore_whole_old_bytes')
tree=ast.parse(new);guards=[n for n in ast.walk(tree) if isinstance(n,ast.If) and ast.unparse(n.test)=='rid in CD_IDS' and n.lineno<=k+1 and n.end_lineno>=l]
if len(guards)!=1:raise RuntimeError('addition_not_inside_single_CD_guard')
old_ast=ast.parse(old);new_stripped_ast=ast.parse(stripped)
if ast.dump(old_ast,include_attributes=False)!=ast.dump(new_stripped_ast,include_attributes=False):raise RuntimeError('AST_not_restored')
frozen=json.loads((S/'FROZEN_INPUT_SET.json').read_text());oldids=frozen['old_configured_record_ids_in_order']
if len(oldids)!=59 or {'23387774','23074543'}&set(oldids):raise RuntimeError('59_legacy_IDs_must_be_disjoint')
protected=set()
for base in [S,C]:protected.update(p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for item in json.loads((S/'protected-before.json').read_text())['files']:protected.add(Path(item['path']))
save('protected-before.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Original sealed stage and its protected1113 originals plus root correction inputs; auditor package added only after final seal.','files':[{'path':str(p),'bytes':p.stat().st_size,'SHA256':sha(p)} for p in sorted(protected)]})
(O/'inputs').mkdir(exist_ok=True)
for name in ['final-content-check.proposed.py','checker-only.diff','SCOPE.json']:(O/'inputs'/name).write_bytes((C/name).read_bytes())
(O/'inserted-guard.txt').write_text(addition)
record={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'INDEPENDENT_MECHANISM_COMPLETE_BEFORE_AUDITOR_CASE_READ','root_corrected_checker':{'path':str(C/'final-content-check.proposed.py'),'SHA256':sha(C/'final-content-check.proposed.py')},'root_diff':{'path':str(C/'checker-only.diff'),'SHA256':sha(C/'checker-only.diff')},'original_stage_checker_SHA256':sha(S/'final-content-check.proposed.py'),'one_15_line_insertion':True,'insertion_new_lines':[k+1,l],'enclosing_condition':'rid in CD_IDS','exact_excision_restores_all_original_bytes_and_AST':True,'old59_IDs_disjoint_from_CD_IDS':True,'old59_record_ids':oldids,'guard_mechanism':{'date_header':'Compare exact normalized visible entry text, computed from approved declared date and edition; require the sole time datetime attribute to equal approved publication_date.','citation':'Compare first visible citation paragraph exactly with approved author/year/title/citation edition/DOI; require exactly two paragraphs and exact BibTeX label.','status':'Compare the complete ordered status paragraph list with all approved status/AI disclosure and optional edition-note strings.','optimization':'Three test() boolean comparisons append issues directly; they are not Python assert statements and remain active under -O.','variable_effect':'The inserted visible_text callable is confined in use to this block. The older loop assigns the ordinary visible_text string before every older record check; other added names are not consumed by older branches.','scope_limit':'Checks harden these approved exact HTML structures; no universal HTML/CSS visibility or adversarial parser security certification.'},'auditor_fault_checker_read':False,'auditor_final_seal_exists_at_checkpoint':(A/'FINAL_SEAL.json').is_file(),'full_old59_suite_rerun':False,'completion_estimate_percent':35,'production_installed':False,'overall203_complete':False}
save('EARLY_MECHANISM.json',record);save('EARLY_MECHANISM_SEAL.json',{'status':'IMMUTABLE_EARLY_GUARD_RECONSTRUCTION','EARLY_MECHANISM_SHA256':sha(O/'EARLY_MECHANISM.json'),'root_corrected_checker_SHA256':scope['new_checker_sha256'],'auditor_cases_not_read':True})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('* '+record['UTC']+' — Entire root diff and current CD checker block read; one15-line insertion only inside CD_IDS; excision restores original bytes/AST; old59 disjoint. Early mechanism sealed before auditor cases. Completion estimate35%.\n')
print(json.dumps({'status':record['status'],'early_seal_SHA256':sha(O/'EARLY_MECHANISM_SEAL.json'),'auditor_final_seal_exists':record['auditor_final_seal_exists_at_checkpoint']},indent=2))
