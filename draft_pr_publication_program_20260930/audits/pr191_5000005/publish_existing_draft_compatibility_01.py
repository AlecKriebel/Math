"""Correct the actual kit publish argv; preserve frozen runtime and the existing draft."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess
A=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('compat191',A/'lifecycle_common.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def main():
 def action():
  g=m.gate();m.original_ready();private=A/'lifecycle_private';old=(private/'ZENODO_publish.stderr').read_text()
  m.require('error: unrecognized arguments: --check-doi' in old and (private/'ZENODO_publish.stdout').read_bytes()==b'','Earlier failed invocation not the proven parser-only failure')
  stage=m.read(A/'ZENODO_STAGE_READBACK.json');m.require(stage['id']==23389367 and stage['gate_sha256']==m.pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Exact approved staged ID/gate drift')
  kit=m.R/'zenodo_deposit_tool/zenodo.py';m.require(hashlib.sha256(kit.read_bytes()).hexdigest()=='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca','Exact kit source drift')
  draft=m.kit_call(g,'inspect',subprocess.run,check_doi=True);m.require(draft['id']==stage['id'] and draft['state']=='ready_to_publish','Existing draft is not unpublished; reconcile without a write')
  projected=m.sanitize_zenodo(draft)|{'gate_sha256':stage['gate_sha256']};m.validate_kit_receipt(g,projected,'draft')
  marker=private/'CORRECTED_PUBLISH_ATTEMPT_STARTED.json'
  with marker.open('x') as f:json.dump({'UTC':m.now(),'id':stage['id'],'gate_sha256':stage['gate_sha256'],'prior_failure':'ARGPARSE_BEFORE_RUN_NO_PUBLICATION_REQUEST','command':'publish --confirm-id 23389367','automatic_second_corrected_write_forbidden':True},f,indent=2)
  raw=m.kit_call(g,'publish',subprocess.run,confirm_id=stage['id'],check_doi=False)
  m.require(raw['id']==stage['id'],'Published ID differs from existing draft')
  out=m.save_published(g,raw,'publish')
  m.write(A/'ROOT_KIT_PUBLISH_COMPATIBILITY_01.json',{'UTC':m.now(),'PR':191,'gate_sha256':stage['gate_sha256'],'id':stage['id'],'status':'UNSUPPORTED_PUBLISH_ARG_REMOVED_SAME_DRAFT_ACTUAL_PUBLICATION_ACCEPTED','runtime_unchanged':True,'exact_kit_unchanged':True,'previous_command_rejected_by_argparse_before_run':True,'actual_published_DOI':out['doi'],'canonical_receipt':m.exact_binding('ZENODO_PUBLICATION_READBACK.json')})
  return out
 return m.production_entrypoint(action)
if __name__=='__main__':print(json.dumps(main()))

