# ----- VERSIONS -----

# Terraform configuration
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}



# ----- VARIABLES -----

# Create a variable for the imported environment variables
variable "env" {
  description = "Contains all the variables inside the .env file."
  type = map(string)
}



# ----- TASKS -----

# Azure provider configuration
provider "azurerm" {
  features {}
  resource_provider_registrations = "none"

  subscription_id = var.env["AZURE_SUBSCRIPTION_ID"]
  client_id       = var.env["AZURE_CLIENT_ID"]
  client_secret   = var.env["AZURE_CLIENT_SECRET"]
  tenant_id       = var.env["AZURE_TENANT_ID"]
}

# Create resource group
resource "azurerm_resource_group" "rg" {
  name     = "translator_rg"
  location = "westeurope"
}

# Create virtual network
resource "azurerm_virtual_network" "vnet" {
  name                = "translator_vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

# Create subnet
resource "azurerm_subnet" "subnet" {
  name                 = "translator_subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create public IP
resource "azurerm_public_ip" "public_ip" {
  name                = "translator_publicIP"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Create network interface
resource "azurerm_network_interface" "nic" {
  name                = "translator_nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "myNicConfiguration"
    subnet_id                     = azurerm_subnet.subnet.id
    public_ip_address_id          = azurerm_public_ip.public_ip.id
    private_ip_address_allocation = "Dynamic"
  }
}

# Create network Security Group
resource "azurerm_network_security_group" "nsg" {
  name                = "translator_nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  # SSH
  security_rule {
    name                       = "AllowSSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Translator
  security_rule {
    name                       = "Allow_Translator"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

// NSG Association with NIC
resource "azurerm_network_interface_security_group_association" "nic_nsg_asso" {
  network_interface_id      = azurerm_network_interface.nic.id
  network_security_group_id = azurerm_network_security_group.nsg.id
}

# Create Linux virtual machine
resource "azurerm_linux_virtual_machine" "vm" {
  name                = "translator-vm"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_DS1_v2"
  admin_username      = "azureuser"
  network_interface_ids = [azurerm_network_interface.nic.id]

  admin_ssh_key {
    username   = "azureuser"
    public_key = file("~/.ssh/id_ed25519.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts"
    version   = "latest"
  }
}



# ----- OUTPUTS -----

# Output the public IP of the VM
output "public_ip" {
  description = "The public IP of the VM"
  value       = azurerm_public_ip.public_ip.ip_address
}

# Output the user of the VM
output "user_vm" {
  description = "The user of the VM"
  value       = azurerm_linux_virtual_machine.vm.admin_username
}
