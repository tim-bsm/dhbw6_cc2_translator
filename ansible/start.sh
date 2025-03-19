#!/bin/sh

# Location of this script
SCRIPT_DIR=$(dirname $(readlink -f "$0"))

# Get the MongoDB URI from the terraform build
MONGODB_URI=$(terraform -chdir=$SCRIPT_DIR/../terraform output -raw mongodb_uri)
AZURE_TRANSLATOR_APIKEY=$(terraform -chdir=$SCRIPT_DIR/../terraform output -raw azure_translator_apikey)
AZURE_TRANSLATOR_REGION=$(terraform -chdir=$SCRIPT_DIR/../terraform output -raw azure_translator_region)

# Add key value pairs to be added/replaced in the docker .env file
# Usage: $0 <KEY1> <VALUE1> [<KEY2> <VALUE2> ...]
$SCRIPT_DIR/update_docker_dotenv.sh "TRANSLATOR_MONGODB_URI" $MONGODB_URI "TRANSLATOR_AZURE_TEXT_TRANSLATION_APIKEY" $AZURE_TRANSLATOR_APIKEY "TRANSLATOR_AZURE_TEXT_TRANSLATION_REGION" $AZURE_TRANSLATOR_REGION


ansible-playbook -i $SCRIPT_DIR/inventory.ini $SCRIPT_DIR/playbook.yml --private-key ~/.ssh/id_ed25519
