<img align="right" alt="RSS Logo" width="30%" height="auto" src="https://rss.com/blog/wp-content/uploads/2019/10/social_style_3_rss-512-1.png">

# Rss2Telegram

Envio automático de feed RSS para pessoa, canal ou grupo no Telegram.

[Mais explicações e exemplos de uso aqui](https://blog.gabrf.com/posts/Rss2Telegram/).

## Participe:

Participe das conversas sobre o projeto na aba [Discussions](https://github.com/GabrielRF/Rss2Telegram/discussions).

Issues também são sempre bem vindas.

## Configuração:

Defina as variáveis na aba `Secrets` do repositório:

`DESTINATION`: Destinos das mensagens separados por vírgulas (`@destino` ou ID). Opcionalmente, remova a variável e crie um arquivo de nome `DESTINATION.txt` com os valores;

`URL`: Endereços de feeds RSS separados por vírgulas. Opcionalmente, remova a variável e crie um arquivo de nome `URL.txt` com os valores;

`BOT_TOKEN`: Token do bot que enviará as mensagens no canal ([@BotFather](https://t.me/BotFather));

`PARAMETERS`: (opcional) Parâmetros que serão adicionados ao fim do link;

`MESSAGE_TEMPLATE`: (opcional) Texto da mensagem. Valor padrão: `<b>{TITLE}</b>` ([ver opções](#opções-de-variáveis));

`BUTTON_TEXT`: (opcional) Texto do botão com o link. Sugestão: `{SITE_NAME}`. Se esta variável não for criada não será enviado um botão. ([Ver opções](#opções-de-variáveis));

`EMOJIS`: (opcional) Emojis separados por vírgulas. Podem ser usados na mensagem ou no botão;

### Opções de variáveis

`{SITE_NAME}`: Nome do site;

`{TITLE}`: Título do post;

`{SUMMARY}`: Sumário do post;

`{LINK}`: Link do post;

`{EMOJI}`: Emoji escolhido aleatoriamente da lista.

## Filtros

Por padrão, todos os elementos do feed RSS serão enviados. Caso queira filtrar o conteúdo, crie um arquivo chamado `RULES.txt` e adicione as regras desejadas ao arquivo. As regras serão executadas em ordem!

> O valor contido em termo funcionará independente de letras maiúsculas ou minúsculas.

`ACCEPT:ALL`: Todas as mensagens serão enviadas;

`DROP:ALL`: Todas as mensagens não serão enviadas;

`ACCEPT:termo`: A mensagem será enviada se `termo` estiver presente;

`DROP:termo`: A mensagem não será enviada se `termo` estiver presente.

### Exemplos de Filtros:

1. Todos as mensagens serão enviadas, menos as que tiverem o termo `política`:

```
ACCEPT:ALL
DROP:Política
```

2. Nenhuma mensagem será enviada, com exceção das mensagens com os termos `futebol` e `vôlei`:

```
DROP:ALL
ACCEPT:futebol
ACCEPT:vôlei
```

## Uso

Faça um *Fork*, defina as variáveis e habilite a ação em "*Enable workflow*". Pronto! 

![Enable Workflow](https://user-images.githubusercontent.com/7331540/178158090-bf774cae-071b-4ac2-ab03-9c5c1132b79e.png)

A ação irá buscar as atualizações a cada hora conforme definido no arquivo [cron.yml](.github/workflows/cron.yml).
