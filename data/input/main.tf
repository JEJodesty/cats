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
#
#      sudo tar -xvzf kubo_v0.29.0_linux-amd64.tar.gz
#      cd kubo
#      sudo bash install.sh
#      ipfs --version
#    EOF
#    delete = ""
#  }
#  depends_on = [
#    shell_script.delete_cats_k8s
#  ]
#}


resource "shell_script" "setup_cod" {
  lifecycle_commands {
    create = <<-EOF
      cd ~/Projects/Research/cats-research/
      # Function to check if Bacalhau is installed
      is_bacalhau_installed() {
          if command -v bacalhau &> /dev/null; then
              return 0
          else
              return 1
          fi
      }

      # Function to install Bacalhau
      install_bacalhau() {
          echo "Bacalhau is not installed. Installing..."
          # You can replace the following command with the actual installation command for Bacalhau
          curl -sL https://get.bacalhau.org/install.sh | bash
      }

      # Check if Bacalhau is installed
      if is_bacalhau_installed; then
          echo "Bacalhau is already installed."
      else
          install_bacalhau
      fi
    EOF
    delete = ""
  }
  depends_on = [
    shell_script.delete_cats_k8s
  ]
}

provider "kind" {
  # Configuration options
}

resource "kind_cluster" "default" {
  name = "cat-action-plane"
  node_image = "kindest/node:v1.23.0"
  wait_for_ready = "true"
  depends_on = [
    shell_script.delete_cats_k8s,
    shell_script.setup_cod
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
