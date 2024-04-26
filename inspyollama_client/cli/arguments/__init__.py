from argparse import ArgumentParser


PARSER = ArgumentParser('inspyollama-client', description='Client for ollama API')


PARSER.add_argument(
    '--query',
    type=str,
    help='A message to send to the AI',
    required=False,
)

PARSER.add_argument(
    '--host',
    type=str,
    help='The host to connect to',
    required=False,
    default='localhost',
)

PARSER.add_argument(
    '--port',
    type=int,
    help='The port to connect to',
    required=False,
    default=8080,
)

PARSER.add_argument(
    '--model',
    type=str,
    help='The model to use',
    required=False,
    default='llama3',
)
