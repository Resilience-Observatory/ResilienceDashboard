# Resilience observatory dashboard

## Usage

### Docker

Within this repo run:

```bash
docker build -t local/resilience_observatory .
docker run --rm -d -p 8050:8050 local/resilience_observatory
```

and access the `8050` port of your machine (e.g. <http://localhost:8050/>).
