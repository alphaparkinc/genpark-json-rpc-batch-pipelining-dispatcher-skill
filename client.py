"""JSON-RPC Batch Pipelining Dispatcher.
100% Python Standard Library.
"""

class JsonRpcBatchPipeliningDispatcher:
    """JSON-RPC 2.0 batch pipelining & dependency resolver."""

    @staticmethod
    def execute_batch(requests: list, handlers: dict) -> list:
        results = {}
        ordered_responses = []

        for req in requests:
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            resolved_params = {}
            for pk, pv in params.items():
                if isinstance(pv, str) and pv.startswith("$ref:"):
                    ref_path = pv[5:].split(".")
                    ref_id = ref_path[0]
                    ref_key = ref_path[1] if len(ref_path) > 1 else None
                    if ref_id in results and ref_key in results[ref_id]:
                        resolved_params[pk] = results[ref_id][ref_key]
                    else:
                        resolved_params[pk] = None
                else:
                    resolved_params[pk] = pv

            handler = handlers.get(method)
            if not handler:
                resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {method} not found"}}
            else:
                try:
                    res_val = handler(resolved_params)
                    results[str(req_id)] = res_val
                    resp = {"jsonrpc": "2.0", "id": req_id, "result": res_val}
                except Exception as e:
                    resp = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": str(e)}}

            ordered_responses.append(resp)

        return ordered_responses
