## Docker

### Example of a full docker compose file: [compose.yml](/compose.yml).

### Port
The flask server for the translator exposes its http port on port `5000`. It is recommended to bind this port on the default port for http (port `80`), if this port is available.

### Environment variables:
Any API keys, passwords etc. should be provided via environemnt variables. For the app to work, the following variables have to be provided in the `compose.yaml`.
- `TRANSLATOR_AZURE_TEXT_TRANSLATION_APIKEY`:  
`KEY1` or `KEY2` shown in the image [here](https://learn.microsoft.com/de-de/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=csharp#prerequisites).
- `TRANSLATOR_AZURE_TEXT_TRANSLATION_REGION`:  
`Location/Region` shown in the image [here](https://learn.microsoft.com/de-de/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=csharp#prerequisites).
- `TRANSLATOR_MONGODB_URI`:  
String in the format `mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@cluster0.example.mongodb.net/?retryWrites=true&w=majority`. For more information see [here](https://www.mongodb.com/docs/manual/reference/connection-string/#find-your-mongodb-atlas-connection-string).
