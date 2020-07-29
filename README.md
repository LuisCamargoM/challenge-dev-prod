# Convert a CSV stream to JSONL text

## Setup

To start the datasource with random data:
```bash
docker-compose up
```

Wait until the code compiles and the service shows `Listening at tcp://0.0.0.0:9999`

Then that you could test it running the following command:
```bash
nc localhost 9999 | python streamer.py
```

After that, will print a log stage process.... 
```bash
- Streaming new Data....
```

For quit: 
``` bash
PRESS Ctrl+C
```

After quit,
It will generate a json file with all results printed inline .
