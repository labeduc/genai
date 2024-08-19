# -*- coding: utf-8 -*-
import os

from taipy.gui import Gui
from dotenv import load_dotenv

load_dotenv()

from pages.generate_content import cont_q_md
from pages.generate_question import gen_q_md
from pages.visualize import tbl_q_md
from pages.report import sum_q_md
from pages.validate_content import val_q_md

# from pages.generate_code import code_q_md

pages = {
    "/": "<center><|navbar|></center>",
    "Gerador": gen_q_md,
    "Visualizar": tbl_q_md,
    "Dashboard": sum_q_md,
    "Analisar": cont_q_md,
    "Validar": val_q_md,
}


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------
if __name__ == "__main__":
    Gui(pages=pages).run(
        title="Demonstração GenAI",
        host="0.0.0.0",
        port=os.getenv("PORT"),
        use_reloader=True,
    )
