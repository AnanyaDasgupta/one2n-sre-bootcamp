import logging


def configure_logging():
    # Configure the root logger once for the whole application.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
