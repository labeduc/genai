# -*- coding: utf-8 -*-
import os
from taipy.gui import Gui, notify, Markdown
from supabase import create_client, Client

import utils.gemini as genai
import utils.config as config


def send_database(state, id, action):
    try:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        tbl = supabase.table("questoes_gemini")
        tbl.insert(
            {
                "area": state.area,
                "tipo": state.tipo,
                "nivel": state.nivel,
                "prompt": state.prompt,
                "resultado": state.resultado,
            }
        ).execute()
        notify(state, "sucesso", "Questão salva!")
        state.salvar = False
    except:
        notify(state, "error", "Erro ao salvar a questão")


def send_question(state, id, action):
    state.resultado = "Waiting ..."
    resultado = None
    if state.objetivo == "":
        notify(state, "error", "Defina a ementa da questão!")
        return None

    gemini = genai.Gemini()
    state.prompt = gemini.build_prompt(
        state.nivel,
        state.objetivo,
        state.tipo,
        state.area,
        state.tem_introducao,
        state.tem_resposta,
    )
    gemini.set_key(os.getenv("GEMINIAI_API_KEY"))
    resultado = gemini.complete(state.prompt)
    if resultado:
        state.resultado = resultado
        notify(state, "success", "Questão criada!")
        state.salvar = True
    else:
        state.resultado = "Erro ao utilizar o Gemini. Verifique o Log"
        notify(state, "success", "Questão criada!")
        state.salvar = False


# Definição de Variável
area = "Ciência de Dados"
nivel = "Fácil"
tipo = "Escolha Simples"
objetivo = "Lógica de Programação com Python: if, for, dicionários e listas"
tem_resposta = "Sim"
tem_introducao = "Sim"
lkp_tipos = config.QST_TIPOS
lkp_niveis = config.QST_NIVEIS
lkp_areas = config.QST_AREAS
salvar = False

prompt = ""
resultado = ""

# Definição Pagina
gen_q_md = Markdown(
    """<|container|
    
# Gerador de Questões

<|layout|columns=1fr 250px|gap=5px|class_name=card|
<|c1|
**Área**
|>
<|c2|
**Parâmetros**
|>
<|c3|
<|{area}|selector|lov={lkp_areas}|dropdown|label=Selecione a Área da Questão|class_name=fullwidth|>
<br/>
<|{objetivo}|input|label="Descreva os conteúdos que a questão deve abordar:"|multiline=true|class_name=fullwidth|>
|>
<|c4|
<|{tipo}|selector|lov={lkp_tipos}|dropdown|label=Selecione o Tipo da Questão|>
<br/>
<|{nivel}|selector|lov={lkp_niveis}|dropdown|label=Selecione o Nível da Questão|>
<br/>
Inclui Introdução?<br/><|{tem_introducao}|toggle|lov=Sim;Não|>
<br/>
Inclui Resposta?<br/><|{tem_resposta}|toggle|lov=Sim;Não|>
|>
|>
---
<br/>
<center><|Gerar Questão|button|on_action=send_question|> <|Salvar Questão|button|on_action=send_database|active={salvar}|></center>
<br/>
<br/>
<|{prompt}|input|multiline|label=Prompt|class_name=fullwidth|>
<br/>
<|{resultado}|input|multiline|label=Resultado|class_name=fullwidth|>
|>
"""
)
