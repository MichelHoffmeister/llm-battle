from langchain_ollama.llms import OllamaLLM

model = "wizard-vicuna-uncensored:13b"
temperature = 0

model = OllamaLLM(model=model, temperature=temperature)

def get_response(index: int, end: bool, story: str):
    return model.invoke("USER: Tell me a short joke. ASSISTANT:")

def generate_test_story():
    story = []

    for i in range(3):
        response = get_response(index=i, end=False, story=" ".join(story))
        story.append(response)
        print(response)

    response = get_response(index=i, end=True, story=" ".join(story))
    story.append(response)
    print(response)
    return story
