from transformers import pipeline

llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=-1
)

def ask_huggingface(prompt):
    result = llm(
    prompt,
    max_length=300,
    temperature=0.3,
    do_sample=True)
                                                                                                                                                                  
    return result[0]["generated_text"]
