from langchain_ollama import OllamaLLM

f = open("test_input.txt", "r")
reply_chain = f.read()

model = OllamaLLM(model='llama3')


kb_article = model.invoke(input=reply_chain)

f = open("test_output.txt", "w")
f.write(kb_article)
f.close()

print("KB article successfully generated!")

