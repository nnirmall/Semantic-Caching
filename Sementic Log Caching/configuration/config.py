
SERVICE_REGISTRY = {
    "ENGINE_ADDR": "localhost:50051",
    "ADAPTER_ADDR": "localhost:50053"
}

def get_service_address(service_name: str) -> str:
    return SERVICE_REGISTRY[service_name]
