import json
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer, DataCollatorForTokenClassification

MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"
LABEL_LIST = ["O", "B-NAME", "I-NAME"]  # Adjust if needed

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def preprocess_notes(raw_data, tokenizer):
    processed = []
    for entry in raw_data:
        tokens = tokenizer.tokenize(entry["note"])
        ner_tags = [0] * len(tokens)  # Placeholder: all "O"
        processed.append({"tokens": tokens, "ner_tags": ner_tags})
    return processed

def tokenize_and_align_labels(examples, tokenizer):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])
            else:
                label_ids.append(label[word_idx])
            previous_word_idx = word_idx
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

def main():
    print(" Loading raw notes...")
    raw_data = load_jsonl("augmented_notes_30K.jsonl")

    print(" Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print(" Preprocessing notes...")
    processed_data = preprocess_notes(raw_data, tokenizer)
    dataset = Dataset.from_list(processed_data)

    print(" Tokenizing and aligning labels...")
    tokenized_dataset = dataset.map(lambda x: tokenize_and_align_labels(x, tokenizer), batched=True)

    print(" Loading model...")
    model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME, num_labels=len(LABEL_LIST))

    
    args = TrainingArguments(
        output_dir="./clinicalbert-ner",
        #evaluation_strategy="no",
        learning_rate=3e-5,
        per_device_train_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        save_strategy="epoch",
        logging_dir="./logs",
    )

    data_collator = DataCollatorForTokenClassification(tokenizer)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    print(" Starting training...")
    trainer.train()
    print(" Training complete.")

if __name__ == "__main__":
    main()
