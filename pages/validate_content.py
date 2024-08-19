# -*- coding: utf-8 -*-
import os
from taipy.gui import Gui, notify, Markdown
from supabase import create_client, Client

import utils.gemini as genai
import utils.config as config


def validar_plagio(state, id, action):
    state.resultado = "Waiting ..."
    resultado = None

    gemini = genai.Gemini()
    gemini.set_key(os.getenv("GEMINIAI_API_KEY"))
    prompt = f"""
    Dado o conteúdo abaixo, verifique se existe plágio. Os resultados possíveis são: 
    - O texto contem plágio, e aponte que trechos são plágio e se possível, qual é a fonte original; 
    - O texto é inspirado em outras obras, ou seja, é baseado fortemente em algo existente (mais de 50% de similaridade) 
      mas não contem elementos copiados, e aponte com qual texto ele possui similaridades; 
    - O texto é completamente original:
    {state.conteudo}
    """
    resultado = gemini.complete(prompt)
    if resultado:
        state.resultado = resultado
        notify(state, "success", "Geração de código concluída!")
    else:
        state.resultado = "Erro ao utilizar o Gemini. Verifique o Log"
        notify(state, "failure", "Código não gerado!")


def validar_iacont(state, id, action):
    state.resultado = "Waiting ..."
    resultado = None

    gemini = genai.Gemini()
    gemini.set_key(os.getenv("GEMINIAI_API_KEY"))
    prompt = f"""
    Dado o conteúdo abaixo, verifique se ele foi gerado por uma IA generativa. Aponte que trechos são indicativos de que o conteudo foi gerado por uma IA generativa:
    {state.conteudo}
    """
    resultado = gemini.complete(prompt)
    if resultado:
        state.resultado = resultado
        notify(state, "success", "Geração de código concluída!")
    else:
        state.resultado = "Erro ao utilizar o Gemini. Verifique o Log"
        notify(state, "failure", "Código não gerado!")


# Definição de Variável
conteudo = ""
resultado = ""

# Definição Pagina
val_q_md = Markdown(
    """<|container|
    
# Validar Conteúdo

<|c3|
**Conteúdo**
<|{conteudo}|input|label="Cole aqui o seu conteúdo:"|multiline=true|class_name=fullwidth|>
|>
<br/>
<center><|Validar Plagio|button|on_action=validar_plagio|><|Validar IA Ger|button|on_action=validar_iacont|></center>
<br/>
<br/>
<|{resultado}|input|multiline|label=Resultado|class_name=fullwidth|>
|>
"""
)
