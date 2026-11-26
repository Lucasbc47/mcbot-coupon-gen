# MCBot v2026

Preenche a pesquisa de satisfação McExperiência do McDonald's Brasil (Arcos
Dourados), em mcexperienciasurvey.com, para um cupom fiscal e imprime o link
para resgatar o benefício.

## Requisitos

```
pip install -r requirements.txt
```

Qualquer execução aceita `--debug`, que salva o HTML de cada página em `debug/`.

## Como usar

1. Edite o `answers.py` com os dados da sua visita:
   - `VISIT`: CNPJ, data e hora que estão no seu cupom fiscal. Copie do
     cupom impresso, não de memória.
   - As outras constantes (canal do pedido, notas, dados pessoais etc.):
     ajuste conforme foi a visita de verdade.

2. Rode primeiro em modo de teste. Ele percorre o fluxo inteiro e mostra o
   que seria enviado na última página, sem enviar nada:

   ```
   python main.py
   ```

3. Se estiver tudo certo, envie de verdade:

   ```
   python main.py --confirm
   ```

   No fim ele imprime um link `mequi.onelink.me`. Abra **no celular**: é um
   deep link (AppsFlyer) para o app do Méqui e não funciona direito no
   navegador do computador. O link só pode ser usado uma vez.

## Importante

- **Cada cupom fiscal dá direito a um benefício só**, pelos Termos e
  Condições da pesquisa. Rodar `--confirm` de novo com o mesmo cupom percorre
  o fluxo outra vez, mas não gera um segundo benefício.
- O site bloqueia requisições em que o campo escondido `JavaScriptEnabled`
  vem como `"0"` (o valor padrão até o script do navegador trocar para
  `"1"`). O `client.py` manda `"1"` em todas as etapas.
- Toda etapa recusada mostra uma `div.Error` ("não podemos continuar a
  pesquisa...", "ler e concordar com os termos..."). O `client.py` lança
  `SurveyError` com esse texto, e a execução para na etapa que falhou.
- Antes de cada resposta, o `client.answer()` confere se os campos existem na
  página atual. Se a pesquisa mudar a ordem ou incluir uma pergunta, a
  execução para em vez de mandar a resposta para a pergunta errada.
- A ordem das opções muda a cada carregamento: responda sempre pelo `value`
  (como o `answers.py` faz), nunca pela posição.

## Arquivos

- `client.py`: wrapper fino sobre `requests.Session` que percorre o wizard
  da pesquisa página por página (lê cada formulário e guarda a URL do próximo
  `action`).
- `answers.py`: as respostas de uma visita.
- `main.py`: roda o fluxo de ponta a ponta usando o `answers.py`.

## Stack e técnica

**Stack:**
- Python 3.13
- `requests`: cliente HTTP com sessão e cookies
- `beautifulsoup4`: parser de HTML
- `faker`: nome e e-mail de exemplo quando `FAKE_PERSONAL_INFO = True`

Sem navegador nenhum (sem Selenium, Playwright ou Puppeteer). Não precisou,
porque o site não depende de JS para funcionar de verdade: só finge que
depende, com um campo escondido (`JavaScriptEnabled`).

**Técnica: *session replay* / *form-walking***

Também chamada de *screen scraping* orientado a sessão. Em vez de simular
clique em botão como um navegador faria, o código imita o protocolo por baixo:

1. Mantém os cookies de sessão vivos (`requests.Session()`).
2. Lê o HTML de cada página para extrair o `<form>` atual e seus campos
   escondidos (`hidden_fields()`).
3. Reenvia tudo isso por POST puro, junto com a resposta daquela pergunta.

Funciona bem aqui porque o motor da pesquisa (SMG) é um wizard clássico
server-side: cada página é um formulário completo, sem SPA e sem chamadas
assíncronas escondendo estado. Num site em React/Next.js com tudo via API
JSON, a mesma técnica valeria, só que direto nos endpoints JSON em vez do HTML.

O `client.py` não sabe nada de McDonald's, CNPJ ou totem: ele só sabe ler o
formulário, guardar o `action` e reenviar os campos escondidos. Toda a lógica
específica da pesquisa (quais perguntas existem, quais valores escolher) fica
no `answers.py` e na sequência do `main.py`. É essa separação que permite
reusar o `client.py` em outro site com o mesmo padrão de wizard, sem mexer na
parte genérica.
