"""MCP Server for JSON-RPC Batch Pipelining Dispatcher.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import JsonRpcBatchPipeliningDispatcher

def dummy_echo(params):
    return {"echo": params}

handlers = {"echo": dummy_echo}

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "execute_batch",
                                "description": "Execute JSON-RPC 2.0 batch with dynamic $ref inter-call dependencies",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "requests": {"type": "array"}
                                    },
                                    "required": ["requests"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                res = JsonRpcBatchPipeliningDispatcher.execute_batch(args.get("requests", []), handlers)
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
