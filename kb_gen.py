from langchain_ollama import OllamaLLM

def kbArticleGenerator(input_file, output_file):
    f = open(input_file, "r")
    reply_chain = f.read()

    model = OllamaLLM(model='llama3')

    kb_article = model.invoke(input=reply_chain)

    f = open(output_file, "w")
    f.write(kb_article)
    f.close()

    print("KB article successfully generated!")

    return True

