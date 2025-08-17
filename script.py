import os
import openai
import re

# Pega a chave secreta do GitHub Secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

def avaliar_site(codigo):
    """
    Analisa o HTML gerado com regras simples.
    Retorna feedback para a IA melhorar na próxima versão.
    """
    feedback = []

    # Regra 1: precisa ter título
    if "<title>" not in codigo:
        feedback.append("Adicionar uma tag <title> com o nome do site.")

    # Regra 2: precisa ser responsivo
    if "meta name=\"viewport\"" not in codigo:
        feedback.append("Adicionar <meta name='viewport'> para responsividade.")

    # Regra 3: precisa ter contraste mínimo
    if "color:" not in codigo:
        feedback.append("Adicionar estilos CSS com cores e contraste visível.")

    # Regra 4: rodapé
    if "<footer" not in codigo.lower():
        feedback.append("Adicionar um rodapé com créditos simples.")

    if not feedback:
        return "O site está bom. Continue melhorando o design e adicionando novas seções."
    else:
        return "Melhore o site corrigindo os seguintes pontos:\n- " + "\n- ".join(feedback)

def gerar_site(prompt, codigo_anterior=None):
    """
    Usa a IA para gerar ou corrigir o site.
    Se já existir código, pede melhorias em cima dele.
    """
    if codigo_anterior:
        mensagem_usuario = f"O código atual do site é:\n\n{codigo_anterior}\n\n{prompt}"
    else:
        mensagem_usuario = prompt

    resposta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um gerador de sites responsivos e acessíveis."},
            {"role": "user", "content": mensagem_usuario}
        ],
        max_tokens=1500,
    )
    codigo = resposta["choices"][0]["message"]["content"]
    return codigo

def salvar_site(codigo):
    """
    Salva o HTML em ./public/index.html
    """
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(codigo)

def main():
    # Se já existe versão anterior, carrega
    caminho = "public/index.html"
    codigo_anterior = None
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            codigo_anterior = f.read()

    # Feedback da versão anterior
    prompt = "Crie a primeira versão do site com boas práticas."
    if codigo_anterior:
        feedback = avaliar_site(codigo_anterior)
        prompt = f"Baseado no site atual, melhore-o.\n{feedback}"

    # Gera novo site
    novo_codigo = gerar_site(prompt, codigo_anterior)
    salvar_site(novo_codigo)

    print("✅ Nova versão do site gerada e salva em ./public/index.html")

if __name__ == "__main__":
    main()
