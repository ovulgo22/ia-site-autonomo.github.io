import os
import openai

# Pega a chave secreta que você colocou no GitHub Secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_site():
    prompt = """
    Crie um site em HTML e CSS que seja moderno, responsivo
    e com um título "Site da IA Autônoma". Coloque também uma
    seção de boas-vindas e um rodapé simples.
    """
    
    resposta = openai.ChatCompletion.create(
        model="gpt-4o",  # ou "gpt-4-turbo" se preferir
        messages=[{"role": "system", "content": "Você é um gerador de sites."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    
    codigo = resposta["choices"][0]["message"]["content"]
    return codigo

def salvar_site(codigo):
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(codigo)

if __name__ == "__main__":
    site = gerar_site()
    salvar_site(site)
    print("✅ Site gerado e salvo em ./public/index.html")
