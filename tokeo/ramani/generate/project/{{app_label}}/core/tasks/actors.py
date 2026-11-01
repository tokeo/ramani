"""
Business task actors for distributed processing with Dramatiq.

This module provides a centralized location for defining business-specific
Dramatiq actors in Tokeo and Cement applications. Actors are distributed
task processors that can handle asynchronous workloads through message passing.

### Features

- Keeps actor definitions in one place for maintainable organization
- Processes work from queues with configurable timeouts and retries
- Rate-limits via the ```app.dramatiq.locks``` interface
- Calls app-specific business logic through the application context

### Example

Register actors with the @app.dramatiq.actor decorator:

```python
from tokeo.ext.appshare import app

@app.dramatiq.actor(queue_name="default")
def process_business_data(item_id):
    # Application-specific business logic
    pass
```

For rate-limited operations that need controlled concurrency:

```python
@app.dramatiq.actor(queue_name="api_operations")
@app.dramatiq.locks.throttle(count=5, per_seconds=60)
def process_business_data(item_id):
    # Rate-limited to 5 calls per minute across all workers
    pass
```

### Notes

- Tasks defined here will be discovered automatically when dramatiq workers
    are started via the 'dramatiq serve' command
- Define app.dramatiq.actors in your application's config file to point to
    this module
- Actors should handle serialization/deserialization of complex data structures

"""

from tokeo.ext.appshare import app  # noqa: F401
from {{ app_label }}.core.logic import words


@app.dramatiq.actor(queue_name='count_words')
def count_words(url):
    """
    Actor function to asynchronously: 'count words on a webpage'.

    This example runs the word counting of ```core.logic.words``` in an
    asynchronous worker using Dramatiq.

    ### Args

    - **url** (str, optional): URL of the webpage to analyze.
        Argument is given by the worker from RabbitMQ on start.
        Value was set on putting the task on the queue.

    """
    words.count_words(url)
