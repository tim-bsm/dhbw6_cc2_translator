## Ansible

### Scripts
This directory contains two scripts. The [`start.sh`](/ansible/start.sh) script is used to deploy the docker container on the previously via terraform created VM. For that, it gets the created secrets from the terraform run and writes them into an `.env`-file in the [`/docker`](/docker) directory using the [`update_docker_dotenv.sh`](/ansible/update_docker_dotenv.sh) script. After that, it executes the ansible command with the previously by terraform (out of the [`inventory.tpl.ini`](/ansible/inventory.tpl.ini)-file) created `inventory.ini`-file to configure the VM and deploy the container on it. 

### Playbook
In the [`playbook.yml`](/ansible/playbook.yml), docker and its  compose plugin get installed. After that the [`compose.yml`](/docker/compose.yml) and the previously created `.env`-file get copied to the VM for the VM to run docker compose afterwards.
