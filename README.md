# RSS2Telegram

Envio automático de feed RSS para canal ou grupo público no Telegram

## Configuração:

Defina as variáveis na aba `Secrets` do repositório:

`BOT_TOKEN`: Token do bot que enviará as mensagens no canal. Fornecido pelo [@BotFather](https://t.me/BotFather);

`DESTINATION`: Canal público que receberá as mensagens. Exemplo: `PromoPassagens` (não use `@`!);

`FEED_URL`: Endereços de RSS separados por vírgulas;

`EMOJIS`: Emojis separados por vírgula usados na composição do botão.

## Uso

A ação irá buscar as atualizações a cada hora conforme definido no arquivo [cron.yml](.github/workflows/cron.yml).
