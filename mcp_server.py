import sys
import json
from client import ReedSolomonCoder

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-reed-solomon-error-correcting-code-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "encode_and_check_rs",
                        "description": "Encode message with Reed-Solomon parity and evaluate syndromes",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "message_bytes": {"type": "array", "items": {"type": "integer"}, "description": "Byte values (0-255)"},
                                "parity_symbols": {"type": "integer", "default": 4}
                            },
                            "required": ["message_bytes"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "encode_and_check_rs":
            msg = args.get("message_bytes", [])
            nsym = args.get("parity_symbols", 4)
            rs = ReedSolomonCoder(nsym=nsym)
            codeword = rs.encode(msg)
            syn = rs.compute_syndromes(codeword)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"codeword": codeword, "syndromes": syn, "has_errors": any(s != 0 for s in syn)})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
