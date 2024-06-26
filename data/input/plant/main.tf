# install
# kubectl, helm
# SDKs: ipfs, cod, terraform

terraform {
  required_providers {
    shell = {
      source  = "scottwinkler/shell"
      version = "1.7.10"
    }
    kind = {
      source = "tehcyx/kind"
      version = "0.2.0"
    }
  }
}

#variable "KUBE_CONFIG_PATH" {
#  type = string
#}


provider "shell" {
  sensitive_environment = {
    #    KUBE_CONFIG_PATH = var.KUBE_CONFIG_PATH
    KUBE_CONFIG_PATH = "~/.kube/config"
  }
  interpreter        = ["/bin/sh", "-c"]
  enable_parallelism = false
}

# InfraStructure cleanup
resource "shell_script" "delete_cats_k8s" {
  lifecycle_commands {
    create = <<-EOF
      cd ~/Projects/cats-research
      kind delete cluster --name cat-action-plane
    EOF
    delete = ""
  }
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
  depends_on = [
    shell_script.delete_cats_k8s
  ]
}

#resource "shell_script" "setup_ipfs_migration" {
#  lifecycle_commands {
#    create = <<-EOF
#      # Check if the container is already running
#      if [ ! "$(docker ps -q -f name=ipfs-migration)" ]; then
#          # Check if the container exists but is not running
#          if [ "$(docker ps -aq -f status=exited -f name=ipfs-migration)" ]; then
#              # Cleanup
#              docker rm ipfs-migration
#          fi
#          # Run the container
#          docker run -d --name ipfs-migration -v ~/Projects/cats/data/output/data:/output ipfs/go-ipfs
#      else
#          echo "ipfs-migration is already running."
#      fi
#    EOF
#    delete = ""
#  }
#  depends_on = [
#    shell_script.delete_cats_k8s,
#    shell_script.pull_ipfs_image
#  ]
#}


#resource "shell_script" "setup_ipfs_integration" {
#  lifecycle_commands {
#    create = <<-EOF
#      # Check if the container is already running
#      if [ ! "$(docker ps -q -f name=ipfs-integration)" ]; then
#          # Check if the container exists but is not running
#          if [ "$(docker ps -aq -f status=exited -f name=ipfs-integration)" ]; then
#              # Cleanup
#              docker rm ipfs-integration
#          fi
#          # Run the container
#          docker run -d --name ipfs-integration -v ~/Projects/cats/data/output/data:/output ipfs/go-ipfs
#      else
#          echo "ipfs-integration is already running."
#      fi
#    EOF
#    delete = ""
#  }
#  depends_on = [
#    shell_script.delete_cats_k8s,
#    shell_script.pull_ipfs_image,
#    shell_script.setup_ipfs_migration
#  ]
#}

provider "kind" {
  # Configuration options
}

resource "kind_cluster" "default" {
  name = "cat-action-plane"
  node_image = "kindest/node:v1.23.0"
  wait_for_ready = "true"
  depends_on = [
    shell_script.delete_cats_k8s,
#    shell_script.setup_ipfs_migration
  ]
}

#resource "shell_script" "setup_helm" {
#  lifecycle_commands {
#    create = <<-EOF
#      cd ~/Projects/cats-research
#      if ! command -v helm &> /dev/null;
#      then
#          sudo curl -sL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
#      fi
#    EOF
#    delete = ""
#  }
#  depends_on = [
#    kind_cluster.default,
#    shell_script.delete_cats_k8s
#  ]
#}

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
  version    = "1.0.0"
  wait_for_jobs = "true"
  depends_on = [
    kind_cluster.default
  ]
}

resource "helm_release" "ray-cluster" {
  name       = "raycluster"
  repository = "https://ray-project.github.io/kuberay-helm/"
  chart      = "ray-cluster"
  version    = "0.6.0"
  wait_for_jobs = "true"
#  set {
#    name  = "image.tag"
#    value = "nightly-aarch64"
#    type  = "string"
#  }
  depends_on = [
    kind_cluster.default,
    helm_release.kuberay-operator
  ]
}
