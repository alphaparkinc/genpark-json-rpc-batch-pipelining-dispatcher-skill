"""Example usage for JSON-RPC Batch Pipelining Dispatcher."""
from client import JsonRpcBatchPipeliningDispatcher
import json

handlers = {
    "fetch_user": lambda p: {"id": p.get("uid"), "username": "alpha_user"},
    "generate_token": lambda p: {"token": f"jwt_{p.get('username')}_secure"}
}

batch = [
    {"jsonrpc": "2.0", "id": 1, "method": "fetch_user", "params": {"uid": 101}},
    {"jsonrpc": "2.0", "id": 2, "method": "generate_token", "params": {"username": "$ref:1.username"}}
]

res = JsonRpcBatchPipeliningDispatcher.execute_batch(batch, handlers)
print(json.dumps(res, indent=2))
