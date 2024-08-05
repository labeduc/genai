# -*- coding: utf-8 -*-
import os
from taipy.gui import Gui, notify, Markdown
from supabase import create_client, Client

import utils.gemini as genai
import utils.config as config


def send_question(state, id, action):
    state.resultado = "Waiting ..."
    resultado = None

    gemini = genai.Gemini()
    gemini.set_key(os.getenv("GEMINIAI_API_KEY"))
    resultado = gemini.complete(state.prompt)
    if resultado:
        state.resultado = resultado
        notify(state, "success", "Geração de código concluída!")
    else:
        state.resultado = "Erro ao utilizar o Gemini. Verifique o Log"
        notify(state, "failure", "Código não gerado!")


# Definição de Variável
prompt = ""
resultado = ""

# Definição Pagina
code_q_md = Markdown(
    """<|container|
    
# Análise de Conteúdo

<|c3|
**Prompt**
<|{prompt}|input|label="Pergunte algo sobre o arquivo que foi feito upload:"|multiline=true|class_name=fullwidth|>
|>
---
<br/>
<center><|Gerar Código|button|on_action=send_question|></center>
<br/>
<br/>
<|{resultado}|input|multiline|label=Resultado|class_name=fullwidth|>
|>
"""
)
