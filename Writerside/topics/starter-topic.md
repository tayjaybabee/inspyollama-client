# insPyOllama-Client

## Getting Started

> __WARNING__:
> <br>This project is in early stages of development. The steps listed in this section should start you on your way of
using this, but it's not finished.

### Recommended

1) Install poetry
2) `cd inspyollama-client`
3) `poetry install`
4) `poetry shell`
5) Open python

```python
from inspyollama_client.client import get_client, send_and_receive_no_stream

HOST = '192.168.2.188'
PORT = 9090

# Get a ollama client object
CLIENT = get_client(HOST, PORT)

query = 'Are you a large language model?'

response = send_and_receive_no_stream(CLIENT, query)

```
