# mc-survey-bot

Fills out the McDonald's Brazil (Arcos Dourados) McExperiência satisfaction
survey at mcexperienciasurvey.com for a given receipt, and prints the link
to redeem the resulting benefit.

## Requirements

```
pip install -r requirements.txt
```

Add `--debug` to any run to save every page's HTML to `debug/`.

## Usage

1. Edit `answers.py` with the visit you want to submit:
   - `VISIT`: CNPJ from the receipt, and the exact visit date/time (as
     logged by the store's POS - if it's rejected, double check the date
     against the actual receipt/totem printout, not memory).
   - The rest of the constants (order channel, ratings, personal info,
     etc.) - adjust to match how the visit actually went.

2. Dry run first - walks the whole flow and prints the final payload
   without submitting anything:

   ```
   python main.py
   ```

3. Once it looks right, submit for real:

   ```
   python main.py --confirm
   ```

   This prints a `mequi.onelink.me` link at the end - open it **on your
   phone** (it's an AppsFlyer deep link into the Méqui app; it won't
   redeem properly from a desktop browser).

## Important

- **Only one voucher is issued per receipt** (per the survey's Terms &
  Conditions). Running `--confirm` twice against the same CNPJ/date/time
  will walk the whole flow again but won't get you a second benefit.
- The site blocks requests where the hidden `JavaScriptEnabled` field is
  `"0"` (the default before a real browser's inline script flips it to
  `"1"`) - `client.py` sets it to `"1"` on every step to pass that check.
- Every refused step shows a `div.Error` banner ("não podemos continuar a
  pesquisa...", "ler e concordar com os termos..."). `client.py` raises
  `SurveyError` with that text, so the run stops at the step that failed.
- Before each answer, `client.answer()` checks the fields exist on the
  current page. If the survey reorders or adds a question, the run stops
  instead of sending an answer to the wrong page.
- Answer options are shuffled on every load: always answer by `value`
  (what `answers.py` does), never by position.

## Files

- `client.py` - thin `requests.Session` wrapper that walks the survey's
  page-by-page wizard (parses each form, tracks the next `action` URL).
- `answers.py` - the actual answers for one visit.
- `main.py` - drives the flow end to end using `answers.py`.

## Stack e técnica

**Stack:**
- Python 3.13
- `requests` - cliente HTTP com sessão/cookies
- `beautifulsoup4` - parser de HTML
- `faker` - nome/e-mail de exemplo quando `FAKE_PERSONAL_INFO = True`

Sem navegador nenhum (sem Selenium/Playwright/Puppeteer). Não precisou,
porque o site não depende de JS pra funcionar de verdade - só finge que
sim através de um campo escondido (`JavaScriptEnabled`).

**Técnica: *session replay* / *form-walking***

Também chamada de *screen scraping* orientado a sessão. Em vez de
simular clique em botão como um navegador faria, o código imita o
protocolo por baixo:

1. Mantém os cookies de sessão vivos (`requests.Session()`).
2. Lê o HTML de cada página pra extrair o `<form>` atual e seus campos
   escondidos (`hidden_fields()`).
3. Reenvia isso via POST puro, somado à resposta real daquela pergunta.

Funciona bem aqui porque o motor de pesquisa (SMG) é um wizard clássico
server-side: cada página é um form completo, sem SPA, sem chamadas
assíncronas escondendo estado. Contra um site em React/Next.js com tudo
via API JSON, a mesma técnica se aplicaria, só que direto nos endpoints
JSON em vez de HTML.

O `client.py` não sabe nada sobre McDonald's, CNPJ ou totem - ele só
sabe "ler formulário, guardar action, reenviar hidden fields". Toda a
lógica específica da pesquisa (quais perguntas existem, quais valores
escolher) fica isolada em `answers.py` e na sequência do `main.py`. Essa
separação é o que permite reusar `client.py` em qualquer outro site que
siga esse mesmo padrão de wizard, sem tocar na parte genérica.
