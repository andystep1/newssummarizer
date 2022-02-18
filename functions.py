import torch
import razdel
from transformers import AutoTokenizer, BertForTokenClassification

model_name = "IlyaGusev/rubert_ext_sum_gazeta"

tokenizer = AutoTokenizer.from_pretrained(model_name)
sep_token = tokenizer.sep_token
sep_token_id = tokenizer.sep_token_id

model = BertForTokenClassification.from_pretrained(model_name)


def getsummary(inputtext):
    article_text = inputtext

    sentences = [s.text for s in razdel.sentenize(article_text)]
    article_text = sep_token.join(sentences)


    inputs = tokenizer(
        [article_text],

        max_length=500,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )
    sep_mask = inputs["input_ids"][0] == sep_token_id

    # Fix token_type_ids
    current_token_type_id = 0 
    for pos, input_id in enumerate(inputs["input_ids"][0]):
        inputs["token_type_ids"][0][pos] = current_token_type_id
        if input_id == sep_token_id:
            current_token_type_id = 1 - current_token_type_id

    # Infer model
    with torch.no_grad(): 
        outputs = model(**inputs) 
    logits = outputs.logits[0, :, 1]

    # Choose sentences 
    logits = logits[sep_mask]
    logits, indices = logits.sort(descending=True)
    logits, indices = logits.cpu().tolist(), indices.cpu().tolist()
    pairs = list(zip(logits, indices))
    pairs = pairs[:3]
    indices = list(sorted([idx for _, idx in pairs]))
    summary = " ".join([sentences[idx] for idx in indices])
    return summary