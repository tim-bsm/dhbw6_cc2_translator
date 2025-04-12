# https://support.hashicorp.com/hc/en-us/articles/4547786359571-Reading-and-using-environment-variables-in-Terraform-runs
# Run the script to get the environment variables from .env file.
data "external" "env" {
  program = ["${path.module}/import_env.sh"]
}




# ----- MODULES -----

# Create module to include the azure part
module "azure" {
  source                = "./azure"
  env                   = data.external.env.result
}

# Create module to include the mongodb atlas part
module "mongodb" {
  source                = "./mongodb"
  env                   = data.external.env.result
  translator_ip         = module.azure.public_ip
}

# Create ansible inventory from a template
resource "local_file" "inventory" {
  filename = "${path.module}/../ansible/inventory.ini" 
  content  = templatefile("${path.module}/../ansible/inventory.tpl.ini", {
    public_ip = module.azure.public_ip
    vm_user = module.azure.user_vm
  })
}



# ----- OUTPUTS -----

output "azure_ip_address" {
  description = "The public IP of the VM"
  value       = module.azure.public_ip
}

output "mongodb_uri" {
  description = "MongoDB Atlas connection string"
  value       = module.mongodb.uri
  sensitive   = true
}

output "azure_translator_apikey" {
  description = "The API key for the Azure translator"
  value = data.external.env.result["TRANSLATOR_AZURE_TEXT_TRANSLATION_APIKEY"]
  sensitive = true
}

output "azure_translator_region" {
  description = "The region for the Azure translator"
  value = data.external.env.result["TRANSLATOR_AZURE_TEXT_TRANSLATION_REGION"]
  sensitive = true
}
