"""Gemini API connector."""

# Import from standard library
import logging
import traceback

# Import from 3rd party libraries
import google.generativeai as genai

import utils.config as config

# Suppress openai request/response logging
# Handle by manually changing the respective APIRequestor methods in the openai package
# Does not work hosted on Streamlit since all packages are re-installed by Poetry
# Alternatively (affects all messages from this logger):
logging.getLogger("gemini").setLevel(logging.WARNING)


class Gemini:
    """Gemini Connector.
    This class provides methods for interacting with the Gemini AI model.
    Methods:
      build_prompt(nivel, objetivo, tipo, area, tem_introducao, tem_resposta):
        Builds a prompt string based on the provided parameters.
      set_key(key):
        Sets the API key for the Gemini AI model.
      upload_to_gemini(path, mime_type=None):
        Uploads a file to the Gemini AI model.
      complete(prompt):
        Calls the Gemini AI model to generate a response based on the provided prompt.
      analyze(prompt, arquivo):
        Calls the Gemini AI model to generate a response based on the provided prompt and file.
    Attributes:
      model:
        The Gemini AI model instance.
    """

    model = None

    @staticmethod
    def build_prompt(
        nivel: str,
        objetivo: str,
        tipo: str,
        area: str,
        tem_introducao: str,
        tem_resposta: str,
    ):
        """
        Builds a prompt string based on the provided parameters.
        """
        if tipo in [
            "Escolha Simples",
            "Escolha Múltipla",
            "Dissertativa",
            "Completar as Lacunas",
            "Lógica - O que Faz",
            "Lógica - Qual o Resultado",
            "Lógica - Qual o Erro",
        ]:
            base_prompt = config.PROMPTS[tipo].format(
                nivel, objetivo, tipo, area, tem_introducao, tem_resposta
            )
        else:
            base_prompt = f"""Você é um especialista em Ciência de Dados.
        Elabore uma questão de nível {nivel} sobre a ementa descrita abaixo:
        Ementa: {objetivo}
        A questão deve ser do tipo: {tipo}
        A questão aborda a área: {area}
        A questão deve ser estruturada da seguinte forma:"""

            if tem_introducao == "Sim":
                base_prompt = (
                    base_prompt + """\n- Apresenta-se uma introdução ao conteúdo"""
                )

            if tipo == "Código SQL":
                base_prompt = (
                    base_prompt
                    + """\n- Apresenta-se o enunciado da questão seguindo o formato:
            - Gera-se uma tabela de dados ficticios
            - Imprime-se a tabela de dados
            - Faz-se uma pergunta que o aluno deve responder com uma instrução SQL"""
                )
            elif tipo == "Código Python":
                base_prompt = (
                    base_prompt
                    + """\n- Apresenta-se o enunciado da questão seguindo o formato:
            - Gera-se uma tabela de dados ficticios
            - Mostra-se a tabela de dados
            - Faz-se uma pergunta que o aluno deve responder com um script Python que pode utilizar as bibliotecas pandas, matplotlib, requests e todas as biliotecas nativas do python"""
                )
            else:
                base_prompt = (
                    base_prompt + """\n- Apresenta-se o enunciado da questão"""
                )

            if tem_resposta == "Sim":
                base_prompt = (
                    base_prompt
                    + """\n- Apresenta-se a resposta correta, e explique a resposta."""
                )

        competencias = "\n".join(
            [
                f'{comp["titulo"]} - {comp["descricao"]}'
                for comp in config.bncc_competencias
            ]
        )
        bncc = f"""\n- Relacione a questão gerada com até duas competências da BNCC que estão listadas abaixo: 
                    - Apresente as duas competências selecionadas com o seguinte formato
                    Compentencia <numero>. <titulo competência> - <descricao competência> - <explicacao sobre como a questão se relaciona com a competência>
                    {competencias}"""

        objetivos = """\n Gere dois objetivos de ensino, seguindo a taxonomia de Bloom, para a questão."""
        return base_prompt + bncc + objetivos

    @staticmethod
    def set_key(key: str):
        """
        Sets the API key for the Gemini AI model.
        """
        global model
        genai.configure(api_key=key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            safety_settings=config.safety_settings,
            generation_config=config.generation_config,
        )

    @staticmethod
    def upload_to_gemini(path: str, mime_type: str = None) -> any:
        """
        Uploads a file to Gemini.
        Args:
          path (str): The path of the file to upload.
          mime_type (str, optional): The MIME type of the file. Defaults to None.
        Returns:
          any: The uploaded file object.
        """
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    @staticmethod
    def complete(prompt: str) -> str:
        """Call Gemini AI with text prompt.
        Args:
            prompt: text prompt
        Return: predicted response text
        """
        global model
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return None

    @staticmethod
    def analyze(prompt: str, arquivo: any) -> str:
        """Call Gemini AI with text prompt and file.
        Args:
            prompt: text prompt
            arquivo: file object
        Return: predicted response text and status
        """
        global model
        result = {"success": None, "text": None}
        try:
            history = {
                "role": "user",
                "parts": [arquivo],
            }
            chat_session = model.start_chat(history=[history])
            master_prompt = f"Usando o arquivo: {arquivo.display_name}, responda o questionamento abaixo:\n{prompt}"
            response = chat_session.send_message(master_prompt)
            chat_session = None
            result["success"] = True
            result["text"] = response.text
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            result["success"] = False
            result["text"] = traceback.format_exc()
        return result
