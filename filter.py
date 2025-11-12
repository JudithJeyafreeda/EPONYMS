import re

# Hard exclusions: literary, psychiatric, non-disease
EXACT_EXCLUDE = {
    "alice in wonderland", "miss havisham", "aguecheek", "cotard delusion", "capgras",
    "fregoli delusion", "diogenes", "ganser", "munchausen", "munchausen syndrome by proxy",
    "victor skumin", "william broadbent", "curling's ulcer", "plyushkin", "pathological jealousy",
    "receptive aphasia", "expressive aphasia", "delusional parasitosis", "peculiar tumour",
    "cock's peculiar tumour", "infantile cortical hyperostosis", "white sponge nevus"
}

# Partial exclusions: non-disease entities
PARTIAL_EXCLUDE = [
    "sign", "reflex", "test", "procedure", "maneuver", "contracture", "hernia", "ulcer",
    "delusion", "tumour", "fracture", "lesion", "triad", "complex", "focus", "gangrene",
    "nevus", "carcinoma", "joint", "diverticulum", "paralysis", "gland", "angina", "infarct"
]

# Inclusion suffixes: disease-like terms
INCLUDE_SUFFIXES = [
    "disease", "syndrome", "disorder", "malformation", "anomaly", "dystrophy", "atrophy",
    "amyotrophy", "encephalopathy", "myopathy", "sclerosis", "anemia", "lymphoma", "leukemia",
    "myelopathy", "neuropathy", "nephritis", "vasculitis", "osteodysplasia", "lipodystrophy",
    "progeria", "amyloidosis", "fibrosis", "thrombasthenia", "telangiectasia", "macroglobulinaemia",
    "osteopetrosis", "neurofibromatosis", "retinopathy", "hypophosphatemia", "lymphoproliferative",
    "encephalitis", "pancreatitis", "neutropenia", "neurodegeneration", "atrophy", "spectrum"
]

def load_raw_dictionary(path="eponym_dictionary.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def is_valid_eponym(term):
    if term in EXACT_EXCLUDE:
        return False
    #if any(p in term for p in PARTIAL_EXCLUDE):
        #return False
    #if len(term.split()) > 5:
    #    return False
   # if not re.search(r"[a-z]", term):  # skip numeric-only or symbol-only
   #     return False
    if any(suffix in term for suffix in INCLUDE_SUFFIXES):
        return True
    return False

def filter_eponyms(raw_terms):
    return sorted(set(term for term in raw_terms if is_valid_eponym(term)))

def save_filtered_eponyms(filtered_terms, output_path="filtered_eponyms.txt"):
    with open(output_path, "w", encoding="utf-8") as f:
        for term in filtered_terms:
            f.write(term + "\n")

def main():

    raw_terms = load_raw_dictionary("eponym_dictionary.txt")
    
    print(" Applying strict filtering...")
    filtered = filter_eponyms(raw_terms)
    print(f"Retained {len(filtered)} filtered eponyms.")

    
    save_filtered_eponyms(filtered)
    

if __name__ == "__main__":
    main()
