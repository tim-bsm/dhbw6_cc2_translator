# Cloud Computing 2 - Final Project: Translator

### Die Ausarbeitung ist [hier](/docu/document/document.pdf) zu finden.

### What is the project?

In this project, a docker container gets created. This container consists of a Python Flask webserver for a translator frontend. This frontend communicates with the Azure Translator API to translate the given phrases and an Atlas MongoDB to cache all the phrases that were inserted into the translator by the user.
For a quick and easy deployment, terraform is used to create a VM on which docker and the translator container are then being installed using Ansible.

### Structure

This project is split up into three source directorys. Each directory contains its own `README.md`-file to better explain the content and the function of the directory. As a quick overview, the [`/docker`](/docker) directory contains everything relating to the translator app itself. The [`/terraform`](/terraform) directory contains the necessary directives to deploy a VM on a Microsoft Azure server. Lastly, the [`/ansible`](/ansible) directory contains the directives to install docker and deploy the container onto the VM.  
Lastly, the [`/docu`](/docu) directory contains all the LaTeX-files to build the `.pdf`-file of the elaboration. Just as a side-note: [this document](/docu/document/document.pdf) is written in german.
