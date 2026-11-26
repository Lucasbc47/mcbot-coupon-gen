# MCBot 

> [!WARNING]
> **Projeto arquivado (2026).** Este script não funciona mais e não recebe
> manutenção. Ficou aqui só como registro de um estudo de automação com Selenium.

MCBot é uma ferramenta em Python para gerar códigos de desconto do
MC Sundae. O cupom de desconto lhe permite comer 2 sorvetes MC Sundae pelo preço de R$ 14,90. Em outras palavras, ele automatiza o processo do questionário de experiencia que o próprio MC Donald's disponibiliza. Clique [aqui](https://mcexperienciasurvey.com/) para ver o site que é automatizado e preenchido.

# Exemplo de Cupom
![Cupom](https://mcexperienciasurvey.com/Projects/MCD_LATAM_ARC/images/Coupons/Incentive_BRA.png)

- Abaixo do cupom possui o código do cupom, o script busca extrai-lo juntamente da data de validade.

# Preview

![Preview](https://s12.gifyu.com/images/SQYiG.gif)

## Requisitos
- **Python 3.8 ou mais recente.**
- **Selenium (instalar com pip)**
- **ChromeDriver**


## Instalação

- [Python](https://www.python.org/downloads/) na hora de instalar não esqueça de incluir o **pip** para ser instalado junto no setup da instalação.

- **Selenium** pacote pip para utilizar no script, abra seu terminal e rode o seguinte comando:

 ```bash
pip install selenium
```

- [ChromeDriver](https://chromedriver.chromium.org/downloads) antes de instalar
verifique sua versão do chrome [aqui](chrome://settings/help) em **"Version":** -> **caso não encontre a sua, pegue uma anterior ou próxima.**
descompacte o zip e copie o diretório do executável do selenium.

No **config.json** abra com editor de código que deseja ou bloco de notas
e edite com suas configurações

## Configuração e Utilização

```json
{
    "diretorio_webdriver": "Cole o caminho do ChromeDriver aqui",
    "esconder_webdriver": false,
    "country": "brasil",
    "cnpj_mc_donalds": "CNPJ do MC Donalds, somente numeros",
    "quantia": 1
}
```
Salve o arquivo e pronto! agora você pode executar o script no terminal e gerar os códigos.

```bash
python example.py
```

O script irá imprimir o código gerado e até quando o mesmo é válido, 
tambem será salvo no arquivo **códigos.txt**.

## Exemplo de utilização

```py
from bot.mcbot import MCBot

## vai gerar 2 códigos, esconder webdriver ativado.
bot = MCBot(
    hidden=True,
    country="brasil",
    cnpj_mc="CNPJ do MC Donalds, somente numeros",
    quantia=2
)

## caso você esteja no Linux 
bot.executable_path=config["diretorio_webdriver"]
## se nao, remova a linha acima

## caso você esteja no Windows 
bot.service = Service(config["diretorio_webdriver"])
## se nao, remova a linha acima

## Começa gerar
bot.start_gen()
``` 

## Status em 2026

O fluxo da pesquisa mudou desde a versão deste repositório:

- **Os XPaths quebraram.** A ordem das opções agora muda a cada carregamento,
  e as perguntas mudaram de ids e de páginas.
- **O benefício saiu da página.** No lugar do código impresso no
  `#CouponDemoImage`, a pesquisa entrega um link para o app do Méqui, que só
  pode ser usado uma vez.
- **O site checa um campo escondido** (`JavaScriptEnabled`) e bloqueia
  clientes que não o preenchem.

Por isso o projeto foi arquivado.

## Autor

- [Lucas Barboza Costa](https://github.com/Lucasbc47)

## Background

Uma tarde com os amigos no MC, uma funcionária nos apresentou a oferta. Era simples, fazer o questionário e conseguir os 2 sorvetes pelo preço de 1. Na época era um MC Flurry Ovomaltine Rocks, realizamos a pesquisa e conseguimos os sorvetes. Como um apaixonado em automatização e sorvetes resolvi automatizar o questionário. 🤣

## License

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.
