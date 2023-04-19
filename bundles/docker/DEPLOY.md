# Trame deployment

Trame applications can be deployed following different patterns.
The one describe below is the simplest one and will only scale up to what the hardware is capable of handling.
For infinit scaling feel free to consult [Kitware](https://www.kitware.com/contact/) for more guidance.

## Docker

This directory provide the core infrastructure for building docker images that can then be deployed your own way.
But if you are looking for something more Heroku like we suggest using [CapRover](https://caprover.com/).

## Caprover

For that section we will assumed you've setup your own CapRover and you are just aiming to deploy your trame application using the caprover cli from npm.

Before any deployment, you need to create an application from the web interface and check the __Websocket Support__.

Then within the directory that contain this `DEPLOY.md`, you should run the following:

```bash
rm -rf ./server
./scripts/build_server.sh
tar -cvf trame-app.tar captain-definition Dockerfile server
caprover deploy -t trame-app.tar
```

It might be necessary to increase the nginx __client_max_body_size__ for your app upload.
To do that go in: __CapRover > Settings > NGINX Configurations > /etc/nginx/conf.d/captain-root.conf__


```json
# Captain dashboard at captain.captainroot.domain.com
    server {
        client_max_body_size 500m;
```

For GPU access you will need to create a `/etc/docker/daemon.json` with the following content where `GPU-f0ada461` come from the command line below

```bash
nvidia-smi -a | grep GPU-UUID
    GPU UUID                              : GPU-f0ada461-5941-6211-dad3-a5003817fb59
```

=> `/etc/docker/daemon.json`
```json
{
  "runtimes": {
    "nvidia": {
      "path": "/usr/bin/nvidia-container-runtime",
      "runtimeArgs": []
    }
  },
  "default-runtime": "nvidia",
  "node-generic-resources": [
    "NVIDIA-GPU=GPU-f0ada461"
    ]
}
```