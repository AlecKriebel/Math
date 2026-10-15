#!/usr/bin/env python3
"""Purely local adversarial DOI/privacy and exact metadata-normalization controls.

Only selected function/expression ASTs are executed from read-only reference
sources. No operation module is imported; no CLI/network/cloud call occurs.
All row fixtures are synthetic. Reports omit their unrelated row contents.
"""
from pathlib import Path
import ast,hashlib,html,json,re,sys
sys.dont_write_bytecode=True
from scope_sheet_evidence import scoped_evidence
from metadata_rules import expected_description,expected_metadata,plain_text_eligible,MetadataRuleError,NORMALIZATION
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
TRACKER=ROOT/'audits/pr681_30003703/record_tracker.py'
KIT=ROOT.parent/'zenodo_deposit_tool/zenodo.py'
def sha(data):return hashlib.sha256(data).hexdigest()
def function(path,name,namespace=None):
 module=ast.parse(path.read_text());nodes=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name==name]
 if len(nodes)!=1:raise RuntimeError('Reference function not unique: '+name)
 scope={'re':re};scope.update(namespace or {})
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),scope)
 return scope[name]
def valid_fixture_doi(value):
 if re.fullmatch(r'10\.5281/zenodo\.\d+',value) is None:raise ValueError('Control DOI malformed')
def main():
 pins={str(path.relative_to(ROOT.parent)):{'bytes':path.stat().st_size,'sha256':sha(path.read_bytes())} for path in (TRACKER,KIT,OUT/'expected_state.py',OUT/'scope_sheet_evidence.py',OUT/'analyze_readbacks.py',OUT/'metadata_rules.py',Path(__file__))}
 normalizers={name:function(OUT/name,func) for name,func in [('expected_state.py','normalize_doi'),('scope_sheet_evidence.py','normalize_doi'),('analyze_readbacks.py','doi_value')]}
 reviewed=function(TRACKER,'doi_matches',{'valid_doi':valid_fixture_doi})
 verify=next(x for x in ast.parse(KIT.read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='verify')
 expressions=[x.value for x in ast.walk(verify) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='escaped_plain_text' for t in x.targets)]
 if len(expressions)!=1:raise RuntimeError('Kit escaped_plain_text expression not unique')
 expression=expressions[0]
 expression_code=compile(ast.Expression(body=expression),str(KIT),'eval')
 def kit_plain_escaped(local,remote):return bool(eval(expression_code,{'html':html,'re':re,'key':'description','value':local,'remote_value':remote}))
 controls=[]
 def check(label,ok,detail=None):
  if not ok:raise RuntimeError('Preparation control failed: '+label)
  item={'control':label,'pass':True}
  if detail is not None:item['detail']=detail
  controls.append(item)
 doi='10.5281/zenodo.23387442'
 bases=[doi,doi.upper(),'https://doi.org/'+doi,'http://doi.org/'+doi,'https://DX.DOI.ORG/'+doi.upper(),'HTTP://dx.doi.org/'+doi,'doi:'+doi,'DOI:  '+doi,'dOi:\t'+doi.upper(),'DoI:\n'+doi]
 forms=[wrap+base+suffix+wrap for base in bases for suffix in ('','/') for wrap in ('',' \t','\n')]
 negatives=['10.5281/zenodo.23387443','https://example.org/'+doi,'doi : '+doi,'doi: https://doi.org/'+doi,doi+'//','https://doi.org/'+doi+'?x=1','Some text '+doi,'https://doi.org/ '+doi,doi+' trailing text','DOI:'+doi+' /','doi:'+doi+':']
 for name,normalize in normalizers.items():
  for i,value in enumerate(forms):
   check(f'DOI:{name}:valid_form_{i+1}',normalize(value)==doi and reviewed([['','',value]],doi)==[1])
  for i,value in enumerate(negatives):
   check(f'DOI:{name}:nonmatching_form_{i+1}',normalize(value)!=doi and reviewed([['','',value]],doi)==[])
 marker='SYNTHETIC_UNRELATED_ROW_CONTENT_NOT_TO_RETAIN'
 rows=[['Original Problem','Solution Chat URL','DOI','Notes']];entries=[]
 for i,n in enumerate((618,623,662,681),2):
  target=doi if n==681 else '10.5281/zenodo.90000'+str(n)
  row=['SYNTHETIC_OWN_'+str(n),'','https://doi.org/'+target,'SYNTHETIC_OWN_NOTE_'+str(n)]
  entries.append({'pr':n,'doi':target,'tracker_row':row,'tracker_range':f"'Math Puzzles'!A{i}:D{i}"});rows.append(row)
 for value in forms+negatives:rows.append([marker,'',value,marker])
 raw={'checked_utc':'SYNTHETIC_ONLY','command':['PURE_LOCAL_FIXTURE'],'returncode':0,'response':{'range':"'Math Puzzles'!A:D",'majorDimension':'ROWS','values':rows}}
 filtered=scoped_evidence('tracker_all_A_D',raw,json.dumps(raw).encode(),entries)
 wanted=reviewed(rows,doi);evidence=next(x for x in filtered['response']['global_DOI_uniqueness_checks'] if x['pr']==681)
 for name,normalize in normalizers.items():
  hits=[i+1 for i,row in enumerate(rows) if len(row)>2 and normalize(row[2])==doi]
  check('DOI:'+name+':all_form_duplicates_match_actual_reviewed_helper',hits==wanted and len(hits)==len(forms)+1,{'matching_rows_count':len(hits)})
 check('DOI:scoped_global_duplicate_evidence_matches_reviewed_helper',evidence['normalized_column_C_match_rows']==wanted and evidence['normalized_column_C_match_count']==len(forms)+1)
 check('Privacy:unrelated_synthetic_rows_not_retained',marker not in json.dumps(filtered) and len(filtered['response']['selected_own_rows'])==4)
 def receipt(norms=None,record='23387442',**changes):
  result={'environment':'production','state':'published','id':int(record),'doi':'10.5281/zenodo.'+record,'metadata_normalizations':NORMALIZATION if norms is None else norms};result.update(changes);return result
 def reject(label,pr,local,r):
  try:expected_description(pr,local,r)
  except MetadataRuleError:check(label,True)
  else:check(label,False)
 positives=['n > 1','x < 2 and y > 1','A & B > C','"quoted" and \'single\' > 1','unknown &unknownentity; > 1']
 for i,local in enumerate(positives,1):
  exact=html.escape(local,quote=False)
  check(f'Metadata:eligible_plain_escape_{i}',plain_text_eligible(local) and kit_plain_escaped(local,exact) and expected_description(681,local,receipt())==exact)
  check(f'Metadata:eligible_escape_matches_kit_expression_{i}',kit_plain_escaped(local,exact) and not kit_plain_escaped(local,exact+' altered'))
 for i,local in enumerate(['<p>x > 1</p>','<!-- comment --> x > 1','<?xml version="1.0"?> x > 1','<BR> x > 1','x &gt; 1','x &#62; 1','x &copy; > 1'],1):
  reject(f'Metadata:HTML_or_existing_entity_rejected_{i}',681,local,receipt())
  check(f'Metadata:HTML_entity_eligibility_matches_kit_{i}',not plain_text_eligible(local) and not kit_plain_escaped(local,html.escape(local,quote=False)))
 for n,record in ((618,'23331709'),(623,'23356540'),(662,'23384924')):
  local='<p>Literal metadata remains exact &gt; here.</p>'
  check(f'Metadata:other_PR{n}_empty_list_means_literal_exact',expected_description(n,local,receipt([],record))==local)
  reject(f'Metadata:other_PR{n}_cannot_use_PR681_escape',n,'n > 1',receipt(NORMALIZATION,record))
 check('Metadata:PR681_empty_list_forbids_implicit_escape',expected_description(681,'n > 1',receipt([]))=='n > 1' and expected_description(681,'n > 1',receipt([]))!=html.escape('n > 1',quote=False))
 reject('Metadata:unknown_normalization_kind_rejected',681,'n > 1',receipt([{'field':'description','kind':'other'}]))
 reject('Metadata:additional_normalization_rejected',681,'n > 1',receipt(NORMALIZATION+[{'field':'title','kind':'other'}]))
 reject('Metadata:extra_dictionary_key_rejected',681,'n > 1',receipt([{'field':'description','kind':'plain_text_html_entities','extra':True}]))
 reject('Metadata:duplicate_normalization_rejected',681,'n > 1',receipt(NORMALIZATION+NORMALIZATION))
 reject('Metadata:unknown_normalization_type_rejected',681,'n > 1',receipt('plain_text_html_entities'))
 missing=receipt();del missing['metadata_normalizations'];reject('Metadata:missing_actual_normalization_list_rejected',681,'n > 1',missing)
 reject('Metadata:actual_stage_receipt_cannot_authorize_escape',681,'n > 1',receipt(state='draft'))
 reject('Metadata:sandbox_receipt_cannot_authorize_escape',681,'n > 1',receipt(environment='sandbox'))
 reject('Metadata:wrong_record_cannot_use_record23387442_rule',681,'n > 1',receipt(record='23387443'))
 reject('Metadata:receipt_DOI_id_mismatch_rejected',681,'n > 1',receipt(doi='10.5281/zenodo.23387443'))
 reject('Metadata:unnecessary_escape_receipt_rejected',681,'plain words',receipt())
 reject('Metadata:nontext_description_rejected',681,['n > 1'],receipt())
 local='"quoted" > 1';wanted_description=expected_description(681,local,receipt())
 check('Metadata:quote_true_or_content_edit_not_accepted',wanted_description!=html.escape(local,quote=True) and wanted_description!=html.escape(local+' changed',quote=False))
 metadata={'title':'UNCHANGED_TITLE','description':local,'version':'1.0','creators':[{'name':'UNCHANGED_CREATOR'}]};before=json.dumps(metadata,sort_keys=True);mapped=expected_metadata(681,metadata,receipt())
 check('Metadata:only_description_transformed_local_preserved',json.dumps(metadata,sort_keys=True)==before and {k:v for k,v in mapped.items() if k!='description'}=={k:v for k,v in metadata.items() if k!='description'} and mapped['description']==wanted_description)
 changed_native=dict(mapped,title='ALTERED_TITLE');check('Metadata:other_field_edit_remains_mismatch',mapped!=changed_native)
 check('Sources:all_read_only_references_unchanged',all((ROOT.parent/rel).stat().st_size==pin['bytes'] and sha((ROOT.parent/rel).read_bytes())==pin['sha256'] for rel,pin in pins.items()))
 report={'status':'PASS','scope':'Purely local synthetic DOI/privacy and record-specific description controls; no actual publication outcome assumed','controls':len(controls),'DOI_valid_forms':len(forms),'DOI_nonmatching_forms':len(negatives),'DOI_normalizers_compared':3,'reviewed_tracker_function':'doi_matches AST only; canonical-fixture DOI validation stub','kit_expression_reference':'verify.escaped_plain_text AST only','record_specific_description_allowlist':'PR681 actual production published record23387442 with exact singleton receipt only','external_requests_made':0,'unrelated_row_contents_retained':False,'source_pins':pins,'results':controls}
 print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
