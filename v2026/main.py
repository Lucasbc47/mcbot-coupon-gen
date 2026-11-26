"""Fills out the McDonald's (Arcos Dourados) McExperiencia satisfaction
survey for a single visit/receipt and prints the resulting voucher page.

Usage:
    python main.py            # dry run: walks the whole flow, stops right
                               # before the final (irreversible) submission
                               # and prints exactly what would be sent.
    python main.py --confirm  # does the same, then actually submits the
                               # last page and prints the voucher/result page.
    --debug                   # also saves every page's HTML to debug/.

Only one voucher is issued per real "cupom fiscal" (receipt), so re-running
with --confirm against the same receipt is expected to fail on a second try.
"""

import sys
from pathlib import Path

import answers
from client import SurveyClient, SurveyError

START_URL = "https://www.mcexperienciasurvey.com/Index.aspx?LanguageID=pt-BR"
DEBUG_DIR = Path(__file__).parent / "debug"

# One entry per wizard page, in the order the survey shows them.
QUESTION_PAGES: list[dict[str, str]] = [
    {"R000001": answers.ORDER_CHANNEL},
    {"R000002": answers.DINE_IN_OR_TAKEOUT},
    {"R000003": answers.WENT_WITH_CHILD_3_7},
    {"R000004": answers.OVERALL_SATISFACTION},
    answers.RATINGS,
    {"R000013": answers.ORDER_AS_REQUESTED},
    {"R000015": answers.RETURN_INTENT_30D, "R000016": answers.NPS_SCORE},
    {"S000019": answers.FREE_COMMENT},
    {"R000020": answers.HAD_PROBLEM},
]


def run(confirm: bool, debug: bool) -> None:
    c = SurveyClient(debug_dir=DEBUG_DIR if debug else None)
    c.get(START_URL)

    c.answer(NextButton="Continuar")                           # language page
    c.answer(Index_CountryPicker="3", NextButton="Continuar")  # 3 = Brasil
    # A refusal here ("não podemos continuar...") means the CNPJ was rejected.
    c.answer(**answers.VISIT, NextButton="Iniciar")

    for page in QUESTION_PAGES:
        c.answer(**page)

    final_payload = c.payload(**answers.PERSONAL_INFO)
    print("Personal-info payload about to be submitted:")
    for k, v in final_payload.items():
        print(f"  {k} = {v!r}")

    if not confirm:
        print("\nDry run only - pass --confirm to actually submit this.")
        return

    c.answer(**answers.PERSONAL_INFO)

    if "R000040" in c.field_names():  # optional marketing opt-in page
        c.answer(R000040=answers.MARKETING_OPTIN)

    print_benefit_link(c)


def print_benefit_link(c: SurveyClient) -> None:
    link = c.soup.select_one("#IncentiveButton a") if c.soup else None
    if link and link.get("href"):
        print("\nBenefit link (open on your phone):", link["href"])
    else:
        print("\n--- RESULT PAGE (no benefit link found) ---")
        print(c.text()[:3000])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Windows console mangles accents otherwise
    try:
        run(confirm="--confirm" in sys.argv, debug="--debug" in sys.argv)
    except SurveyError as e:
        print(f"Survey stopped: {e}")
        sys.exit(1)
