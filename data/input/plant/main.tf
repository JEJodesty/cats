# install
# kubectl
# SDKs: ipfs, cod

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
}


provider "shell" {
  sensitive_environment = {
    KUBE_CONFIG_PATH = local.k8s_config_path
  }
  interpreter        = ["/bin/sh", "-c"]
  enable_parallelism = false
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_image" "go-ipfs" {
  name = "ipfs/go-ipfs:latest"
}

# Create a container
resource "docker_container" "ipfs-migration" {
  image = docker_image.go-ipfs.image_id
  name  = "ipfs-migration"
}

resource "docker_container" "ipfs-integration" {
  image = docker_image.go-ipfs.image_id
  name  = "ipfs-integration"
  volumes {
    container_path = local.integration_mount_path
  }
}

provider "kind" {
  # Configuration options
}

resource "kind_cluster" "default" {
  name = "cat-action-plane"
  kubeconfig_path = local.k8s_config_path
  node_image = "kindest/node:v1.26.0"
  wait_for_ready = "true"
  depends_on = [
    docker_container.ipfs-migration,
    docker_container.ipfs-integration
  ]
}

provider "helm" {
  kubernetes {
    config_context_cluster = "kind-cat-action-plane"
    config_path = "~/.kube/config"
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
