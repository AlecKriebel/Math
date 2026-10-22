#!/usr/bin/env python3
"""Exact, record-specific metadata rule; never read a stage as publication proof.

Plain-text eligibility and escaping match zenodo_deposit_tool/zenodo.py verify:
no match for <(?:/?[A-Za-z]|[!?])[^>]*>, html.unescape(text)==text,
and exact html.escape(text, quote=False). No other normalization is accepted.
"""
import hashlib,html,re
NORMALIZATION=[{'field':'description','kind':'plain_text_html_entities'}]
NORMALIZED_PR681_RECORD_ID='23387442'
class MetadataRuleError(ValueError):pass
def require(ok,message):
 if not ok:raise MetadataRuleError(message)
def plain_text_eligible(value):
 return isinstance(value,str) and not re.search(r'<(?:/?[A-Za-z]|[!?])[^>]*>',value) and html.unescape(value)==value
def expected_description(pr,description,publication_receipt):
 """Return exact expected native description from an actual publication receipt."""
 require(type(publication_receipt) is dict,'Actual publication receipt must be an object')
 require(publication_receipt.get('environment')=='production' and publication_receipt.get('state')=='published','A stage/draft receipt cannot authorize metadata normalization')
 record_id=str(publication_receipt.get('id',''))
 require(re.fullmatch(r'\d+',record_id) is not None and publication_receipt.get('doi')=='10.5281/zenodo.'+record_id,'Actual publication receipt DOI/record identity mismatch')
 require('metadata_normalizations' in publication_receipt,'Actual publication receipt must explicitly record metadata_normalizations')
 require(isinstance(description,str),'Local description must be text')
 normalizations=publication_receipt['metadata_normalizations']
 require(type(normalizations) is list,'Actual metadata_normalizations must be a list')
 if normalizations==[]:return description
 require(pr==681 and record_id==NORMALIZED_PR681_RECORD_ID,'Only actual published PR681 record23387442 may use the recorded description normalization')
 require(normalizations==NORMALIZATION,'Unknown, additional or changed metadata normalizations are forbidden')
 require(plain_text_eligible(description),'Local description fails the unchanged kit plain-text eligibility conditions')
 escaped=html.escape(description,quote=False)
 require(escaped!=description,'Recorded plain-text normalization must be an actual escaping change')
 return escaped
def expected_metadata(pr,metadata,publication_receipt):
 """Copy metadata and apply only the permitted exact description transformation."""
 result=dict(metadata)
 result['description']=expected_description(pr,metadata['description'],publication_receipt)
 return result
def description_rule_evidence(pr,description,publication_receipt):
 expected=expected_description(pr,description,publication_receipt)
 return {'actual_publication_record_id':str(publication_receipt['id']),'actual_publication_doi':publication_receipt['doi'],'actual_receipt_metadata_normalizations':publication_receipt['metadata_normalizations'],'comparison':'EXACT' if publication_receipt['metadata_normalizations']==[] else 'EXACT_HTML_ESCAPE_QUOTE_FALSE_OF_ELIGIBLE_LOCAL_PLAIN_TEXT','local_plain_text_eligible':bool(plain_text_eligible(description)),'local_description_sha256':hashlib.sha256(description.encode()).hexdigest(),'expected_native_description_sha256':hashlib.sha256(expected.encode()).hexdigest(),'all_other_metadata_fields_remain_exact':True}
