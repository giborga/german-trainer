def call_llm(prompt, client, model, temperature=0.7):
    response = client.chat.completions.create(
        model= model,
        messages=[{"role": "system", "content": "You are a trainer of German language."},
                  {"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content