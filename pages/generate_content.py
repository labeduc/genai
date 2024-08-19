# -*- coding: utf-8 -*-
import os
from taipy.gui import Gui, notify, Markdown
from supabase import create_client, Client

import utils.gemini as genai
import utils.config as config


def upload_file(state):
    notify(state, "success", f"Arquivo {state.arquivo} carregado com sucesso!")


def send_question(state, id, action):
    state.resultado = "Waiting ..."
    resultado = None

    gemini = genai.Gemini()
    gemini.set_key(os.getenv("GEMINIAI_API_KEY"))
    arquivo_bin = gemini.upload_to_gemini(state.arquivo)
    resultado = gemini.analyze(state.prompt, arquivo_bin)
    if resultado["success"]:
        state.resultado = resultado["text"]
        notify(state, "success", "Análise concluída!")
    else:
        state.resultado = (
            f"Erro ao utilizar o Gemini. Verifique o Log abaixo:\n{resultado['text']}"
        )
        notify(state, "failure", "Análise não concluída!")


# Definição de Variável
arquivo = ""
prompt = ""
resultado = ""

# Definição Pagina
cont_q_md = Markdown(
    """<|container|
    
# Análise de Conteúdo

<|c1|
**Arquivo**
|>
<|c3|
<|{arquivo}|file_selector|label=Select File|on_action=upload_file|extensions=.png,.jpg,.jpeg,.pdf,.csv,.xlsx|drop_message=Arquivo carregado|>
<br/>
**Prompt**
<|{prompt}|input|label="Pergunte algo sobre o arquivo que foi feito upload:"|multiline=true|class_name=fullwidth|>
|>
<br/>
<center><|Analisar|button|on_action=send_question|></center>
<br/>
<br/>
<|{resultado}|input|multiline|label=Resultado|class_name=fullwidth|>
|>
"""
)
