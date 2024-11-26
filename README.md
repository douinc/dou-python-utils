## Quick Start

1. Installation

```bash
uv add git+https://github.com/douinc/dou-python-utils.git@v0.1.0
```

2. How to Use

```python
from dou import logger

logger.info("This is an info message")
logger.debug("This is a debug message")
logger.warning("This is a warning message")
logger.error("This is an error message")

logger.info(
    message={
        "test": "message",
    },
    search_id="id",
)

```
