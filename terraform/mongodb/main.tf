# ----- VERSIONS -----

# Terraform configuration
terraform {
  required_providers {
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~> 1.29.0"
    }
  }
}



# ----- VARIABLES -----

# Create a variable for the imported environment variables
variable "env" {
  description = "Contains all the variables inside the .env file."
  type = map(string)
}

# Create a variable for the public IP of the VM
variable "translator_ip" {
  description = "The public IP of the VM"
  type = string
}



# ----- TASKS -----

# Configure the MongoDB Atlas Provider 
provider "mongodbatlas" {
  public_key = var.env["MONGODB_KEY_PUBLIC"]
  private_key  = var.env["MONGODB_KEY_PRIVATE"]
}

# Create MongoDB project
resource "mongodbatlas_project" "project" {
  name   = "translator_project"
  org_id = var.env["MONGODB_ORGANIZATION_ID"]
}

# Add Azure VM to allowed IPs
resource "mongodbatlas_project_ip_access_list" "ip_access" {
  project_id = mongodbatlas_project.project.id
  ip_address = var.translator_ip
}

# Create MongoDB database user
resource "mongodbatlas_database_user" "user" {
  project_id         = mongodbatlas_project.project.id
  username           = var.env["MONGODB_USERNAME"]
  password           = var.env["MONGODB_PASSWORD"]
  auth_database_name = "admin"

  roles {
    role_name     = "readWriteAnyDatabase"
    database_name = "admin"
  }
}

# Create MongoDB cluster
resource "mongodbatlas_cluster" "cluster" {
  name                        = "translator-cluster"
  project_id                  = mongodbatlas_project.project.id
  provider_name               = "TENANT"
  backing_provider_name       = "AZURE"
  provider_region_name        = "EUROPE_WEST"
  provider_instance_size_name = "M0"
}



# ----- OUTPUTS -----

# Give back connection string for the database
output "uri" {
  # Add everything to one string
  value = join("",
    [
        "mongodb+srv://",
        "${var.env["MONGODB_USERNAME"]}:${var.env["MONGODB_PASSWORD"]}",
        "@${replace(mongodbatlas_cluster.cluster.connection_strings[0].standard_srv, "mongodb+srv://", "")}",
        "/translator_db?retryWrites=true&w=majority",
    ]
  )
  sensitive   = true
}
