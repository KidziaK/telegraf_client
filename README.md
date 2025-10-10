# telegraf-client

Python bindings for the Rust telegraf client library.

## Installation

```bash
pip install telegraf-client
```

## Usage

```python
import telegraf_client

client = telegraf_client.Client("udp://localhost:8089")
point = telegraf_client.Point(
    measurement="cpu",
    tags={"host": "server-01"},
    fields={"usage": 75.5}
)
client.write_point(point)
client.close()
```

## Development

```bash
uv sync
uv run pytest
```
