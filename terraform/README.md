## Terraform

### Structure
The folder contains one [`main.tf`](/terraform/main.tf)-file which firstly reads in the environment vairables. For that, the [`import_env.sh`](/terraform/import_env.sh) script parses the local `.env`-file and returns it as valid JSON. It then declares a module for creating the Azure VM and one for creating a MongoDB. Based on the outputs of those modules, the variables inside the [`inventory.tpl.ini`](/ansible/inventory.tpl.ini) get replaced with values and a new `inventory.ini`-file gets created inside the [`ansible`](/ansible) directory. Moreover, some of the output values get used by the [`start.sh`](/ansible/start.sh) script in combination with the [`update_docker_dotenv.sh`](/ansible/update_docker_dotenv.sh) script to create the `.env`-file in the [`/docker`](/docker) directory.

### Environment variables:
Any API keys, passwords etc. should be provided via environemnt variables. For everything to work, the following variables have to be provided in an extra `.env`-file inside the [`/terraform`](/terraform) directory.
- `ALLOWED_SSH_HOSTS`: The public IPs of the machines that should have SSH acces to the created VM. At least insert the IP of the machine which runs the ansible command.  
&nbsp;
- `AZURE_SUBSCRIPTION_ID`: The `id` retrieved by logging into the Azure CLI.
- `AZURE_CLIENT_ID`: The `appId` retrieved by the Azure CLI.
- `AZURE_CLIENT_SECRET`: The `password` retrieved by the Azure CLI.
- `AZURE_TENANT_ID`: The `tenantId` retrieved by the Azure CLI.  
&nbsp;
- `MONGODB_KEY_PUBLIC`: The public key decribed [here](https://www.mongodb.com/docs/atlas/configure-api-access/#in---go-to-the-organization-access-manager-page.).
- `MONGODB_KEY_PRIVATE`: The private key decribed [here](https://www.mongodb.com/docs/atlas/configure-api-access/#in---go-to-the-organization-access-manager-page.).
- `MONGODB_ORGANIZATION_ID`: The ID of the MongoDB Atlas organization (can be found in the organization settings of the MongoDB Atlas UI).
- `MONGODB_USERNAME`: The username that should get created to connect to the database.
- `MONGODB_PASSWORD`: The password that should get created to connect to the database.  
&nbsp;
- `TRANSLATOR_AZURE_TEXT_TRANSLATION_APIKEY`: `KEY1` or `KEY2` shown in the image [here](https://learn.microsoft.com/de-de/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=csharp#prerequisites).
- `TRANSLATOR_AZURE_TEXT_TRANSLATION_REGION`: `Location/Region` shown in the image [here](https://learn.microsoft.com/de-de/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=csharp#prerequisites).
