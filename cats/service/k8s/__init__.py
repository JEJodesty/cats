from kubernetes import client, config
from kubernetes.client.rest import ApiException


class KubeService:
    def __init__(self):
        self.kube_config = config.load_kube_config()  # For local environment
        self.incluster_config = self.config.load_incluster_config()  # For in-cluster environment
        self.api_instance = client.CoreV1Api()

    def create_service(self,
        metadata_name,
        spec_selector,
        spec_ports=[client.V1ServicePort(protocol="TCP", port=80, target_port=80)]
    ):
        service = client.V1Service(
            api_version="v1",
            kind="Service",
            # metadata=client.V1ObjectMeta(name="nginx-service"),
            metadata=client.V1ObjectMeta(name=metadata_name),
            spec=client.V1ServiceSpec(
                # selector={"app": "nginx"},
                # ports=spec_ports
                selector=spec_selector,
                ports=spec_ports
            ),
        )
        api_response = self.api_instance.create_namespaced_service(
            namespace="default",
            body=service,
        )
        print("Service created. status='%s'" % str(self.api_response.status))

    def list_services(self, namespace="default"):
        api_response = self.api_instance.list_namespaced_service(namespace=namespace)
        for service in self.api_instance.items:
            print("Service: %s" % service.metadata.name)

    def delete_service(self, name, namespace="default"):
        api_response = self.api_instance.delete_namespaced_service(
            name=name,
            namespace=namespace,
            body=client.V1DeleteOptions(),
        )
        print("Service deleted. status='%s'" % str(api_response.status))