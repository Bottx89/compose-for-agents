import os, socket
from urllib.parse import urlparse
from collections import defaultdict
from typing import List, Sequence

from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioServerParameters,
    SseServerParams,
)

def _tcp_check(host: str, port: int) -> None:
    """Fail fast if the MCP gateway is unreachable."""
    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"TCP check OK → {host}:{port}")
    except OSError as e:
        raise RuntimeError(f"cannot reach {host}:{port}: {e}") from e


def create_mcp_toolsets(
    tools_cfg: Sequence[str],
) -> List[MCPToolset]:
    """Return *ready-to-use* MCPToolset objects – synchronously."""
    if not tools_cfg:
        return []

    tools_by_server = defaultdict(list)
    for raw in tools_cfg:
        if not raw.startswith("mcp/") or ":" not in raw:
            raise ValueError(f"Bad MCP spec: {raw}")
        server, tool = raw[4:].split(":", 1)
        tools_by_server[server].append(f"{server}:{tool}")

    endpoint = os.environ["MCPGATEWAY_ENDPOINT"]
    if endpoint.startswith(("http://", "https://")):
        parsed = urlparse(endpoint)
        host, port = parsed.hostname, parsed.port or 80
        _tcp_check(host, port)
        conn_params = SseServerParams(url=endpoint)
    else:
        host, port = endpoint.split(":")
        _tcp_check(host, int(port))
        conn_params = StdioServerParameters(
            command="socat",
            args=["STDIO", f"TCP:{endpoint}"],
        )

    return [
        MCPToolset(connection_params=conn_params,
                   tool_filter=tool_list)
        for tool_list in tools_by_server.values()
    ]
