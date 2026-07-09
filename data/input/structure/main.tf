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
  host_ipfs_daemon_pidfile = "${path.module}/.host-ipfs-daemon.pid"
  host_ipfs_daemon_logfile = "${path.module}/.host-ipfs-daemon.log"
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

resource "shell_script" "host_ipfs_daemon" {
  # Idempotent: probes with `ipfs id` (the daemon's live API) rather than
  # the repo.lock file, since a stale lock can outlive a crashed daemon.
  # Only starts `ipfs daemon` - and only ever kills it again on destroy -
  # when this resource is the one that started it, so a daemon already
  # running from outside Terraform is never disturbed and never hit with
  # a second `ipfs daemon` (which would fail with "someone else has the
  # lock").
  lifecycle_commands {
    create = <<-EOF
      #!/bin/bash
      set -e
      if ipfs id >/dev/null 2>&1; then
        echo "Host IPFS daemon already running; not starting another one."
        exit 0
      fi
      nohup ipfs daemon >"${local.host_ipfs_daemon_logfile}" 2>&1 &
      echo $! > "${local.host_ipfs_daemon_pidfile}"
      for i in $(seq 1 30); do
        ipfs id >/dev/null 2>&1 && exit 0
        sleep 1
      done
      echo "Timed out waiting for host IPFS daemon to become ready" >&2
      exit 1
    EOF
    delete = <<-EOF
      #!/bin/bash
      if [ -f "${local.host_ipfs_daemon_pidfile}" ]; then
        kill "$(cat "${local.host_ipfs_daemon_pidfile}")" 2>/dev/null || true
        rm -f "${local.host_ipfs_daemon_pidfile}"
      fi
    EOF
  }
}

resource "shell_script" "docker_compose_ipfs_transport" {
  lifecycle_commands {
    create = <<-EOF
      #!/bin/bash
      set -e
      mkdir -p "$INTEGRATION_INPUT_DATA_CACHE"
      export INTEGRATION_INPUT_DATA_CACHE="$(cd "$INTEGRATION_INPUT_DATA_CACHE" && pwd)"
      docker-compose -f ${local.ipfs_transport_compose} up --scale ipfs_migration=1 --scale ipfs_integration=1 -d --wait
      bash ${path.module}/ipfs_connect_peers.sh
    EOF
    delete = <<-EOF
      #!/bin/bash
      docker-compose -f ${local.ipfs_transport_compose} down || true
    EOF
  }
  depends_on = [
    shell_script.host_ipfs_daemon
  ]
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
