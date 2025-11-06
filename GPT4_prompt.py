import openai

openai.api_key = "your-api-key"

def gpt4_deidentify(text, mode="few-shot"):
    if mode == "zero-shot":
        prompt = f"""You are a clinical de-identification system. Identify and mask PHI entities. Preserve medical eponyms like 'Parkinson's disease' and 'Hodgkin lymphoma'.\n\nText:\n{text}"""
    else:
        prompt = f"""You are a clinical de-identification system. Examples:\n\nInput: 'Mr. Parkinson was diagnosed with Hodgkin disease.'\nOutput: '[NAME] was diagnosed with Hodgkin disease.'\n\nInput: 'Chiari malformation was noted.'\nOutput: 'Chiari malformation was noted.'\n\nNow process:\n{text}"""

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=2048,
    )
    return response["choices"][0]["message"]["content"]
