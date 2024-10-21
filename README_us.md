# Gmail Reader

Project that implements a Python function, using Azure Functions, that reads emails with a specific subject, downloads the attachment and saves it to an Azure Data Lake Storage account.

## Functioning

The project is divided into 5 simple functions:
- authenticate_gmail: function responsible for authentication with the Gmail service using the integration APIs provided by Google.
- get_samsung_health_email: function responsible for searching the email with the sender and predefined subjects.
- get_samsung_health_email: função responsável pela conexão com a _storage_ e o upload do anexo no container e pastas definidos
- process_email_with_attachments: function responsible for extracting the email attachment
- read_email: main function of Azure Functions that uses the previous functions to process email attachments.


## Learn more

This project was made for an analysis carried out on an article made on Linkedin that can be read [here](https://www.linkedin.com/pulse/captura-de-dados-via-email-logic-apps-vs-azure-functions-la%C3%ADs-meuchi-jqrhf/?trackingId=iXvpRqgGRsC076ZSC6%2FFPQ%3D%3D)
