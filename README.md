<img align="right" alt="RSS Logo" width="30%" height="auto" src="https://rss.com/blog/wp-content/uploads/2019/10/social_style_3_rss-512-1.png">

# Rss2Telegram

Envio automático de feed RSS para pessoa, canal ou grupo no Telegram.

## Configuração:

Defina as variáveis na aba `Secrets` do repositório:

`BOT_TOKEN`: Token do bot que enviará as mensagens no canal ([@BotFather](https://t.me/BotFather));

`DESTINATION`: Destinos das mensagens separados por vírgulas (`@destino` ou ID);

`URL`: Endereços de feeds RSS separados por vírgulas;

`MESSAGE_TEMPLATE`: (opcional) Texto da mensagem. Valor padrão: `<b>{TITLE}</b>` ([ver opções](#opções-de-variáveis));

`BUTTON_TEXT`: (opcional) Texto do botão com o link. Sugestão: `{SITE_NAME}`. Se esta variável não for criada não será enviado um botão. ([Ver opções](#opções-de-variáveis));

`EMOJIS`: (opcional) Emojis separados por vírgulas. Podem ser usados na mensagem ou no botão;

### Opções de variáveis

`{SITE_NAME}`: Nome do site;

`{TITLE}`: Título do post;

`{SUMMARY}`: Sumário do post;

`{LINK}`: Link do post;

`{EMOJI}`: Emoji escolhido aleatoriamente da lista.

## Uso

Faça um *Fork*, defina as variáveis e habilite a ação em "*Enable workflow*". Pronto! 

![Enable Workflow](https://user-images.githubusercontent.com/7331540/178158090-bf774cae-071b-4ac2-ab03-9c5c1132b79e.png)

A ação irá buscar as atualizações a cada hora conforme definido no arquivo [cron.yml](.github/workflows/cron.yml).
