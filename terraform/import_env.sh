#!/bin/sh

# Parses the .env file in the same direcotry as this script and
# returns them as JSON.
#
# Edited version of the following link:
# https://support.hashicorp.com/hc/en-us/articles/4547786359571-Reading-and-using-environment-variables-in-Terraform-runs


# Location of this script
SCRIPT_DIR=$(dirname $(readlink -f "$0"))

# Name of the .env file
ENV_FILE="$SCRIPT_DIR/.env"

# Check if the file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "File $ENV_FILE not found."
  exit 1
fi

# Initialize the JSON object
json="{"
first=1

# Read each line of the .env file
while IFS= read -r line || [ -n "$line" ]; do
  # Trim the line (remove leading and trailing whitespace)
  trimmed=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  
  # Skip empty lines
  if [ -z "$trimmed" ]; then
    continue
  fi

  # Skip comment lines (lines starting with #)
  case "$trimmed" in
    \#*)
      continue
      ;;
  esac

  # If the line does not contain '=', skip it
  case "$trimmed" in
    *=*)
      ;;
    *)
      continue
      ;;
  esac

  # Extract key and value
  key=$(echo "$trimmed" | cut -d '=' -f 1)
  value=$(echo "$trimmed" | cut -d '=' -f 2-)

  # Trim key and value again
  key=$(echo "$key" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  value=$(echo "$value" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

  # Escape double quotes in key and value
  key=$(echo "$key" | sed 's/"/\\"/g')
  value=$(echo "$value" | sed 's/"/\\"/g')

  # Prepend a comma if it is not the first element
  if [ "$first" -eq 1 ]; then
    first=0
  else
    json="$json, "
  fi

  # Append the key-value pair to the JSON string
  json="$json\"$key\": \"$value\""
done < "$ENV_FILE"

json="$json}"
echo "$json"
