from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# 使用本地路径加载模型
def load_model():
    model_path = "./m2m100_418M"
    tokenizer = M2M100Tokenizer.from_pretrained(model_path)
    model = M2M100ForConditionalGeneration.from_pretrained(model_path)
    return tokenizer, model


def translate_text(text, src_lang="ja", tgt_lang="zh"):
    tokenizer, model = load_model()
    tokenizer.src_lang = src_lang  # 源语言是日语

    encoded = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
    output = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return output

