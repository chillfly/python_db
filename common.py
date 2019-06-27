import base64
import uuid


def create_token():
    uuid4_bytes = uuid.uuid4().bytes + uuid.uuid4().bytes
    return base64.b64encode(uuid4_bytes)

