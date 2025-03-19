#!/bin/sh

# Location of this script
SCRIPT_DIR=$(dirname $(readlink -f "$0"))

# Path to the .env file
DOTENV_FILE="$SCRIPT_DIR/../docker/.env"

# Check if at least one argument is provided
if [ "$#" -lt 2 ] || [ $(expr $# % 2) -ne 0 ]; then
    echo "Usage: $0 <KEY1> <VALUE1> [<KEY2> <VALUE2> ...]"
    exit 1
fi

# Create the file if it does not exist
if [ ! -f "$DOTENV_FILE" ]; then
    touch "$DOTENV_FILE"
fi

# Iterate over all arguments in pairs
while [ "$#" -gt 0 ]; do
    KEY="$1"
    NEW_VALUE="$2"
    shift 2

    # Escape special characters in NEW_VALUE
    ESCAPED_VALUE=$(printf '%s
' "$NEW_VALUE" | sed 's/[\/&]/\\&/g')

    # Check if the key exists
    if grep -q "^$KEY=" "$DOTENV_FILE"; then
        # Key exists -> Replace value
        sed -i "s/^$KEY=.*/$KEY=$ESCAPED_VALUE/" "$DOTENV_FILE"
    else
        # Key does not exist -> Add new entry
        echo "$KEY=$NEW_VALUE" >> "$DOTENV_FILE"
    fi

done

echo "Updated keys in $DOTENV_FILE"

