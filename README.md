# dou-utils

Composition of utils for Dou Inc. projects.

## DouCLI

Installs files for python formatting options.

### Quickstart

```bash
# initiate project with `uv init`
# add dou-utils with `uv add dou-utils`
dou install formatting
```

## DouLogger

A simple and flexible Python logging utility with enhanced features for structured logging.

### Features

- **Easy-to-use logging methods**: `info`, `debug`, `warning`, `error`.
- **Structured logging support**: Pass additional metadata with your log messages.
- **Configurable logging levels**: Control the verbosity of your logs.

### Installation

Install DouLogger directly from the GitHub repository:

```bash
pip install git+https://github.com/douinc/dou-python-utils.git@v0.1.0
```

#### Quick Start

Import the logger from the dou package:

```python
from dou import logger
```

#### Basic Logging

Log messages at different severity levels:

```python
logger.info("This is an info message")
logger.debug("This is a debug message")
logger.warning("This is a warning message")
logger.error("This is an error message")
```

#### Structured Logging

Include additional metadata in your logs for better traceability:

```python
logger.info(
    message={
        "event": "user_signup",
        "user_id": 12345,
    },
    search_id="abcde12345",
)
```

## Development

```bash
uv build
uv pip install -e .
```

## Publish

```bash
uv publish
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or suggestions, please open an issue or contact us at team@dou.so

