# -*- coding: utf-8 -*-
import os
from taipy.gui import notify, Markdown
from supabase import create_client, Client
import pandas as pd


def return_dados():
    tbl = None
    df = None
    try:
        tbl = supabase.table("questoes_gemini").select("*").order("id").execute()
        df = pd.DataFrame(tbl.data)
    except:
        pass
    return df


# Definição de Variável
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
dados = return_dados()
areas = dados.groupby("area")["id"].count().reset_index()
areas.rename(columns={"id": "contagem_ids"}, inplace=True)
tipos = dados.groupby("tipo")["id"].count().reset_index()
tipos.rename(columns={"id": "contagem_ids"}, inplace=True)


def refresh_dados(state):
    state.dados = return_dados()
    state.areas = state.dados.groupby("area")["id"].count().reset_index()
    state.areas.rename(columns={"id": "contagem_ids"}, inplace=True)
    state.tipos = state.dados.groupby("tipo")["id"].count().reset_index()
    state.tipos.rename(columns={"id": "contagem_ids"}, inplace=True)


# Definição Pagina
sum_q_md = Markdown(
    """<|container|
        
# Dashboard

<center><|Atualizar|button|on_action=refresh_dados|></center>

<|layout|columns=1fr 1fr|gap=5px|class_name=card|
<|c1|
<|{areas}|chart|type=pie|values=contagem_ids|labels=area|>
|>
<|c2|
<|{tipos}|chart|type=pie|values=contagem_ids|labels=tipo|>
|>
|>
|>
"""
)
