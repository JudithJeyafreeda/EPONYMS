import re
import spacy

nlp = spacy.load("en_core_sci_md")  # Use SciSpaCy for clinical syntax
EPONYM_DICT = set([e.lower() for e in open("eponym_dictionary.txt").read().splitlines()])

def is_eponym_context(span):
    suffixes = {"disease", "syndrome", "disorder", "malformation", "anomaly"}
    tokens = [t.text.lower() for t in span.doc[max(0, span.start-3):span.end+3]]
    return any(s in tokens for s in suffixes)

def is_honorific_context(span):
    honorifics = {"mr", "mrs", "dr", "patient"}
    prev_token = span.doc[span.start-1].text.lower() if span.start > 0 else ""
    return prev_token in honorifics

def filter_name_entities(doc):
    filtered = []
    for ent in doc.ents:
        if ent.label_ == "NAME":
            ent_text = ent.text.lower().strip(".,")
            if ent_text in EPONYM_DICT and is_eponym_context(ent) and not is_honorific_context(ent):
                continue  # Preserve eponym
        filtered.append(ent)
    return filtered
