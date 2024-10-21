# install
# SDKs: cod

terraform {
  required_providers {
    shell = {
      source  = "scottwinkler/shell"
      version = "1.7.10"
    }
    kind = {
      source = "tehcyx/kind"
      version = "0.5.1"
    }
    helm = {
      source = "hashicorp/helm"
      version = "2.15.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
    local = {}
  }
}

locals {
#  KUBE_CONFIG_PATH = pathexpand(var.KUBE_CONFIG_PATH)
  k8s_config_path = pathexpand("~/.kube/config")
  integration_mount_path = pathexpand("$INTEGRATION_INPUT_DATA_CACHE:/outputs")
  docker_host = pathexpand("unix:///var/run/docker.sock")
  ipfs_transport_compose = pathexpand("${path.module}/ipfs_transport_compose.yaml")
}

provider "shell" {
  sensitive_environment = {
    KUBE_CONFIG_PATH = local.k8s_config_path
  }
  interpreter        = ["/bin/sh", "-c"]
  enable_parallelism = false
}

provider "docker" {
  host = local.docker_host
}

resource "shell_script" "docker_compose_ipfs_transport" {
  lifecycle_commands {
    create = <<-EOF
      #!/bin/bash
      docker-compose -f ${local.ipfs_transport_compose} up --scale ipfs_migration=1 --scale ipfs_integration=1 -d --wait
    EOF
    delete = ""
  }
}

provider "kind" {
  # Configuration options
}

resource "kind_cluster" "default" {
  name = "cats"
  kubeconfig_path = local.k8s_config_path
  node_image = "kindest/node:v1.26.0"
  wait_for_ready = "true"
  depends_on = [
    shell_script.docker_compose_ipfs_transport
  ]
}

provider "helm" {
  kubernetes {
    config_context_cluster = "kind-cats"
    config_path = local.k8s_config_path
  }
}

resource "helm_release" "kuberay-operator" {
  name       = "kuberay-operator"
  repository = "https://ray-project.github.io/kuberay-helm/"
  chart      = "kuberay-operator"
  version    = "1.1.1"
  wait_for_jobs = "true"
  depends_on = [
    kind_cluster.default
  ]
}

resource "helm_release" "ray-cluster" {
  name       = "raycluster"
  repository = "https://ray-project.github.io/kuberay-helm/"
  chart      = "ray-cluster"
  version    = "1.1.1"
  wait_for_jobs = "true"
  set {
    name  = "image.tag"
    value = "2.9.0-aarch64"
    type  = "string"
  }
  depends_on = [
    kind_cluster.default,
    helm_release.kuberay-operator
  ]
}
