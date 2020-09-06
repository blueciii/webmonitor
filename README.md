# WebMonitor

## About <a name = "about"></a>

Just a simple tool to monitor websites and store in a Postgres DB through Kafka

### Prerequisites

- Running Postgres DB service
- Running Kafka service

## Input file sample
- Input file is a json file with sample contents below
- url is the only required key

```
[
    {
      "name": "google",
      "url": "https://google.com",
      "pattern": "^<!doctype[ a-zA-Z<>:\\/.\\=\\-\"]+<head>"
    }
]
```

## Usage <a name = "usage"></a>


```python webmonitor.py --help```
