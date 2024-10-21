# Gmail Reader

Projeto que implementa uma função em Python, utilizando Azure Functions, que lê emails com um assunto específico, baixa o anexo e salva e uma conta do Azure Data Lake Storage.

## Funcionamento

O projeto é dividido em 5 funções simples:
- authenticate_gmail: função responsável pela autenticação com o serviço do Gmail utilziando as API's de integração disponibilizadas pelo Google.
- get_samsung_health_email: função responsável pela pela busca do email com o remetente e assuntos pré definidos. 
- get_samsung_health_email: função responsável pela conexão com a STORAGE e o upload do anexo no container e pastas definidos
- process_email_with_attachments: função responsável pela extração do anexo do email
- read_email: função principal da Azure Functions que faz o uso das funções anteriores para processar os anexos dos emails.


## Saber mais

Esse projeto foi feito para uma análise realizada em um artigo feito no Linkedin que pode ser lido [aqui](https://www.linkedin.com/pulse/captura-de-dados-via-email-logic-apps-vs-azure-functions-la%C3%ADs-meuchi-jqrhf/?trackingId=iXvpRqgGRsC076ZSC6%2FFPQ%3D%3D)
