from faker import Faker

VISIT = {  # dados do seu cupom fiscal
    "InputCNPJ": "00.000.000/0000-00",
    "Index_VisitDateDatePicker": "DD/MM/AAAA",
    "Index_VisitDateFormattedDate": "AAAAMMDD",
    "InputDay": "DD", "InputMonth": "MM", "InputYear": "AAAA",
    "InputHour": "HH", "InputMinute": "MM",
    "Index_OptIn": "1",
}

ORDER_CHANNEL = "4"       # Balcao - Totem de Autoatendimento e Entrega a mesa
DINE_IN_OR_TAKEOUT = "1"  # Consumiu dentro da loja
WENT_WITH_CHILD_3_7 = "2"  # Nao
OVERALL_SATISFACTION = "5"  # Muito satisfeito (nota 10)

RATINGS = {  # qualidade comida, limpeza, cordialidade, rapidez, sabor, custo-beneficio
    "R000009": "5", "R000010": "5", "R000007": "5",
    "R000006": "5", "R000008": "5", "R000012": "5",
}

ORDER_AS_REQUESTED = "1"  # Sim
RETURN_INTENT_30D = "5"   # Muito provavel
NPS_SCORE = "10"          # 10 - Certamente recomendaria
FREE_COMMENT = ""         # deixado em branco a pedido do usuario
HAD_PROBLEM = "2"         # Nao

MARKETING_OPTIN = "2"  # Nao

FAKE_PERSONAL_INFO = True  
# True = gera nome/telefone/email falsos com Faker, 
# False = usa os dados reais abaixo

_fake = Faker("pt_BR")

REAL_PERSONAL_INFO = {
    "S000036": "Nome",                # Nome*
    "S000028": "Sobrenome",           # Sobrenome
    "S000035": "11999999999",         # Telefone
    "S000033": "voce@exemplo.com",    # E-mail*
    "S000034": "voce@exemplo.com",    # Confirme o e-mail
}


def build_personal_info(fake_data: bool) -> dict:
    if not fake_data:
        return dict(REAL_PERSONAL_INFO)

    email = _fake.email()
    return {
        "S000036": _fake.first_name(),
        "S000028": _fake.last_name(),
        "S000035": f"11{_fake.random_number(digits=9, fix_len=True)}",
        "S000033": email,
        "S000034": email,  # tem que bater com o email acima
    }


PERSONAL_INFO = build_personal_info(FAKE_PERSONAL_INFO)
