import begin
import logging


@begin.subcommand
def hello(name):
    "Say hello"
    logging.info(f"Hello {name}")


@begin.subcommand
def goodbye(name):
    "Say goodbye"
    logging.info(f"Goodbye {name}")


@begin.start
@begin.logging
def main():
    "Greetings and salutations"
