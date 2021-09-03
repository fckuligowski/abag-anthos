**Introduction**
This repo houses the abagdemo app and provides an example of how to build it with a Dockerfile. It came from the abagdemo-gcp repo, but we removed the Cloud Build pieces from it.  

**Install**

I had trouble with "pip3 install -r requirements.txt" with the google-cloud-storage library. It would get an error saying *error: invalid command 'bdist_wheel*. To fix this, [this post](https://stackoverflow.com/questions/34819221/why-is-python-setup-py-saying-invalid-command-bdist-wheel-on-travis-ci) said to "pip3 install wheel", which fixes the issue, so I added wheel to the requirements.txt. But I still got that error when it was right before google-cloud-storage. I had to move wheel to the top of the file, then the error stopped coming up. (I'm not sure this isn't going to come back later, though).

**Docker**

Create the image for abagdemo. The first statement extracts the version number from the helm chart.  

```
ABAG_VER=$(sed -r -n 's/appVersion:\s+(.*)/\1/p' helm/abagdemo/Chart.yaml | sed -e 's/^[ \t]*//')
docker build -t fk-test-04/abagdemo:$ABAG_VER .
```

If you want to run the container from Docker, and shell into it.
```
docker run --rm -td fk-test-04/abagdemo:$ABAG_VER 
docker ps
docker exec -it f1048684b081 /bin/sh
docker stop f1048684b081
```

This was the old way I was running it.

```
docker run --name abagdemo -d -p 30080:5000 --rm -v instance/creds/abag-anthos.json=/home/fkuligowski/tmp/training-automl-ahead-fkuligowski.json \
 -e GOOGLE_APPLICATION_CREDENTIALS=instance/creds/abag-anthos.json fk-test-04/abagdemo:$ABAG_VER
or
docker run --name abagdemo -p 30080:5000 --rm -v instance/creds/abag-anthos.json=/home/fkuligowski/tmp/training-automl-ahead-fkuligowski.json \
 -e GOOGLE_APPLICATION_CREDENTIALS=instance/creds/abag-anthos.json fk-test-04/abagdemo:$ABAG_VER
```
If you want to run pytest to test it from Docker
```
docker run --name abagdemo -p 30080:5000 --rm -e MODE='TESTING' -v instance/creds/justademo-acoustic-apex.json=/abagdemo/justademo-acoustic-apex.json -e GOOGLE_APPLICATION_CREDENTIALS=/abagdemo/instance/creds/justademo-acoustic-apex.json -v ~/py/abagdemo/tests/:/abagdemo/tests fckuligowski/abagdemo:v1.1
```
Note that the image name needs to be at the end of the command, after the "-e" env var parms (else Docker will pass them to the shell script as arguments, not env vars).

Docker push to repo

```
docker push fk-test-04/abagdemo:v1.x
```
