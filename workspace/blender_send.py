#!/usr/bin/env python3
"""Send a command to Blender MCP addon via TCP socket."""
import socket
import json
import sys

def send_command(cmd_type, params=None, host='127.0.0.1', port=9876):
    command = {"type": cmd_type}
    if params:
        command["params"] = params

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(30)
    sock.connect((host, port))

    payload = json.dumps(command).encode('utf-8')
    sock.sendall(payload)

    chunks = []
    while True:
        try:
            chunk = sock.recv(8192)
            if not chunk:
                break
            chunks.append(chunk)
            try:
                data = b''.join(chunks)
                result = json.loads(data.decode('utf-8'))
                sock.close()
                return result
            except json.JSONDecodeError:
                continue
        except socket.timeout:
            break

    sock.close()
    data = b''.join(chunks)
    return json.loads(data.decode('utf-8')) if data else None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: blender_send.py <command_type> [json_params]")
        sys.exit(1)

    cmd = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
    result = send_command(cmd, params)
    print(json.dumps(result, indent=2))
