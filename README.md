# Flyte_Demo
Notes of learning to use the MLOps tool Flyte


## Flyte Notes

### Local set up

1. Set up local cluster
use flyte demo to create local cluster
```flytectl demo start```
then
```export FLYTECTL_CONFIG=~/.flyte/config-sandbox.yaml```

2. Create project

```
flytectl create project \
    --id "my-project" \
    --labels "my-label=my-project" \
    --description "My Flyte project" \
    --name "My project"
```

then, use demo template to create a project repo
```pyflyte init --template flyte-simple my-project```

3. Running workflow (cd to my-project repo first)
use `uv` to create venv locally
```uv sync```
```source .venv/bin/activate```

- run workflow locally
```pyflyte run hello_world.py hello_world_wf```

- run workflow in the remote cluster (run directly)
```pyflyte run --remote --project my-project --domain development hello_world.py hello_world_wf```

- Register workflow to the remote cluster (and run later with GUI)
```pyflyte register --project my-project --domain development .```


- Clean up (local machine)
```flytectl demo teardown```
```docker system prune -a --volumes```