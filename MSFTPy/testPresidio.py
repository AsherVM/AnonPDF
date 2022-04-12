# https://microsoft.github.io/presidio/samples/python/presidio_notebook/
from presidio_analyzer import AnalyzerEngine, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import json
from pprint import pprint

text_to_anonymize = "His name is Mr. Jones and his phone number is 212-555-5555"




analyzer = AnalyzerEngine()
analyzer_results = analyzer.analyze(text=text_to_anonymize, entities=["PHONE_NUMBER"], language='en')

print(analyzer_results)






analyzer_results = analyzer.analyze(text=text_to_anonymize, language='en')

analyzer_results






anonymizer = AnonymizerEngine()
anonymized_results = anonymizer.anonymize(text_to_anonymize, analyzer_results)
# anonymized_results = anonymizer.anonymize(
#     text=text_to_anonymize,
#     analyzer_results=analyzer_results,    
#     operators={"DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMIZED>"}), 
#                         "PHONE_NUMBER": OperatorConfig("mask", {"type": "mask", "masking_char" : "*", "chars_to_mask" : 12, "from_end" : True}),
#                         "TITLE": OperatorConfig("redact", {})}
# )

print(f"text: {anonymized_results.text}")
print("detailed response:")

pprint(json.loads(anonymized_results.to_json()))