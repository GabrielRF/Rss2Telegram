<img align="right" alt="RSS Logo" width="30%" height="auto" src="https://rss.com/blog/wp-content/uploads/2019/10/social_style_3_rss-512-1.png">

# RSS2Telegram

Envio automático de feed RSS para pessoa, canal ou grupo no Telegram.

## Configuração:

Defina as variáveis na aba `Secrets` do repositório:

`BOT_TOKEN`: Token do bot que enviará as mensagens no canal ([@BotFather](https://t.me/BotFather));

`DESTINATION`: Destinos das mensagens separados por vírgulas (`@destino` ou ID);

`URL`: Endereços de feeds RSS separados por vírgulas;

`EMOJIS`: Emojis separados por vírgulas usados na composição do botão.

## Uso

A ação irá buscar as atualizações a cada hora conforme definido no arquivo [cron.yml](.github/workflows/cron.yml).
