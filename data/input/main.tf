# install
# kubectl, helm
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
    local = {}
  }
}

locals {
#  KUBE_CONFIG_PATH = pathexpand(var.KUBE_CONFIG_PATH)
  k8s_config_path = pathexpand("~/.kube/config")
}


provider "shell" {
  sensitive_environment = {
    KUBE_CONFIG_PATH = local.k8s_config_path
  }
  interpreter        = ["/bin/sh", "-c"]
  enable_parallelism = false
}

#resource "shell_script" "set_bsd_udp_buffer_size_for_go" {
#  lifecycle_commands {
#    create = <<-EOF
#      cd ~/Projects/cats-research
#      # https://github.com/quic-go/quic-go/wiki/UDP-Buffer-Sizes
#      sudo sysctl -w net.core.wmem_max=7500000
#      sudo sysctl -w net.core.rmem_max=7500000
#    EOF
#    delete = ""
#  }
#  depends_on = [
#    shell_script.delete_cats_k8s
#  ]
#}

resource "shell_script" "pull_ipfs_image" {
  lifecycle_commands {
    create = <<-EOF
      docker pull ipfs/go-ipfs
    EOF
    delete = ""
  }
}

resource "shell_script" "setup_ipfs_migration" {
  lifecycle_commands {
    create = <<-EOF
      # Check if the container is running
      if [ "$(docker ps -q -f name=ipfs-migration)" ]; then
         echo "Stopping the running container: ipfs-migration"
         docker stop ipfs-migration
      fi

      # Check if the container exists (but is not running)
      if [ "$(docker ps -aq -f name=ipfs-migration)" ]; then
         echo "Removing the existing container: ipfs-migration"
         docker rm ipfs-migration
      fi

      echo "Starting a new container: ipfs-migration"
      docker run -d --name ipfs-migration ipfs/go-ipfs
    EOF
    delete = ""
  }
  depends_on = [
    shell_script.pull_ipfs_image
  ]
}


resource "shell_script" "destroy_ipfs_integration" {
  lifecycle_commands {
    create = <<-EOF
      # Check if the container is running
      if [ "$(docker ps -q -f name=ipfs-integration)" ]; then
         echo "Stopping the running container: ipfs-integration"
         docker stop ipfs-integration
      fi

      # Check if the container exists (but is not running)
      if [ "$(docker ps -aq -f name=ipfs-integration)" ]; then
         echo "Removing the existing container: ipfs-integration"
         docker rm ipfs-integration
      fi

      echo "Starting a new container: ipfs-integration"
      docker run -d --name ipfs-integration -v $INTEGRATION_INPUT_DATA_CACHE:/outputs ipfs/go-ipfs
    EOF
    delete = ""
  }
  depends_on = [
    shell_script.pull_ipfs_image,
    shell_script.setup_ipfs_migration
  ]
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
    shell_script.setup_ipfs_migration,
    shell_script.destroy_ipfs_integration
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
