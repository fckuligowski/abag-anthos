# abag-anthos
The abagdemo app, deployed on Anthos and Service Mesh

# Prerequisites  
Create a Service Account in the Project that you want to use, for this application to use. This service account will need to have Storage Admin perms on the Project. Once the service account is created, then create a .json key file for it, and download it to a local directory.  
For example, you'll have a file ```my-svc-acct.json```.  
Build a container image and deploy it to the Container Registry of your application. See the [notes.md](notes.md) file for more instructions on that. You will need that image and version number (i.e. ```gcr.io/my-project/abagdemo:v0.0.1```) for the deployment file later on.

# Installing with Helm
The Helm chart can be found in the [helm/abagdemo](helm/abagdemo) directory. Edit these values in the [values.yaml](helm/abagdemo/values.yaml) file (or pass them on the command line).  
- Set *image.repository* to where you have pushed your Docker container (i.e. gcr.io/fk-test-04/abagdemo). The image version (tag) will be defined below.  
- Set *service.type* to NodePort, if you don't want an external LoadBalancer (with its public IP).  
Edit this value in the [Chart.yaml](helm/abagdemo/Chart.yaml) file.  
- Set *appVersion* to the container image tag you would like to run (i.e. v0.0.1).  
Now, gather the file name of your Service Account's credential .json file, and pass it to the helm install command, as shown below.  
```
helm upgrade --install abagdemo helm/abagdemo --set-file secret.gcpCreds=/my-dir/my-service-account.json
```
Next, you can find the application's EXTERNAL-IP.  
```
kubectl get svc -n abagdemo
```
With that, you can test the application.  
```
k8s/testapp_curl.sh <EXTERNAL_IP>
```
That should show that the GET and POST tests worked ok. And once it runs ok, a new GCS Bucket named "abagdemo-gcp-yyyyMMdd" will be created in the home Project of my-svc-acct to house the application's database.

# Installing with straight Kubernetes .yaml files  
Run the create_secret.sh script and pass in the key file to it.  
```
./k8s/create_secret.sh ~/tmp/my-svc-acct.json
```
The secret will be created, using the basename of the .json file. You can see this in the new Secret's spec.  
```
kubectl describe secret -n abagdemo abagdemo-gcp-creds
```
Take that basename, copy it and paste it into the [k8s/abagdemo-deployment.yaml](k8s/abagdemo-deployment.yaml) file.  
```
# Find this line in the file
          - name: GOOGLE_APPLICATION_CREDENTIALS
            value: "/home/abagdemo/instance/creds/training-automl-ahead-fkuligowski.json"
# And place your file name in it.
          - name: GOOGLE_APPLICATION_CREDENTIALS
            value: "/home/abagdemo/instance/creds/my-svc-acct.json"
```  
While you are editing the deployment file, also update the container image.  
```
# Find this line in the file
      containers:
      - name: abagdemo
        image: gcr.io/fk-test-04/abagdemo:v0.0.1
# And place your image name in it.
      containers:
      - name: abagdemo
        image: gcr.io/my-project/abagdemo:v0.0.1
```  
Next, you can apply that deployment yaml.  
```
kubectl apply -f k8s/abagdemo-deploy.yaml
```
Next, you can deploy the Service for the app, and then find its EXTERNAL-IP.  
```
kubectl apply -f k8s/abagdemo-service.yaml
kubectl get svc -n abagdemo
```
With that, you can test the application.  
```
k8s/testapp_curl.sh <EXTERNAL_IP>
```
That should show that the GET and POST tests worked ok. And once it runs ok, a new GCS Bucket named "abagdemo-gcp-yyyyMMdd" will be created in the home Project of my-svc-acct to house the application's database.  


# About the Application  
The app is called **abagdemo**. It is meant to be an app that can record and show scan records for luggage bags, as they go through the airport conveyors. That's the premise for the app, so I had something to build for.

It is a Python Flask app that serves up a REST endpoint that one can use to interact with the app, at these endpoints (routes).

- /index is the home page
- /history/001 to show all the scans for bag id 001
- /status/001 to show just the latest scan for bag id 001
- /scan to add a new scan for a bag

The data is  stored in a Google Cloud Platform Storage object. It will automatically create the object on the fly, from a base data file in this repo. This requires GCP credentials. These can't be stored in the repo. They're stored in Google Secret Manager for testing, and in a Kubernetes Secret for 'production'.  The name of the Secret Manager object is "last-baron-abagdemo" and it contains the credential Key file.

This app uses pytest to do some tests, to ensure the app isn't broken.

The pipeline is written in Google Cloud Build script in a file named cloudbuild.yaml. It uses Cloud Builder to build a container, run the tests, and push the container to Google Container Registry. 

At Merge time, a tag is added to the GitHub repo, using the version found above. This requires GitHub creds so Cloud Build can write to the Git repo. These creds are also stored in Secret Manager as "fckuligowski-git-user" and "fckuligowski-git-pwd".

The name of the image that's pushed needs to be defined in "helm/abagdemo/values.yaml", except for the version tag which is stored in "helm/abagdemo/Chart.yaml". When that image tag value changes, Cloud Build will push the image to Container Registry (provided the tests  pass, and provided it is on a Merge).

The container image is deployed to 'production' with "helm install" at the end of the pipeline.

The container image doesn't do anything but install the app and it's Python requirements. Use the "runit.sh" script to start  the app in the container. Use the "tests/testit.sh" script to run the pytests from the container. Use the "rundev.sh" script to run the app from a container on your dev machine (I used a Linux Ubuntu host from Linux Academy).

# Directory Structure  
Here's an overview of the directories in this repo, and what each is for.  
- [helm](helm) contains the Helm charts for the application.  
- [instance](instance) contains configuration information for the abagdemo Python application. It is a construct that is required by Pytest.  
- [k8s](k8s) contains the plain-old Kubernetes .yaml files to install the app without Helm.  
- [project](project) contains the actual Python application.  
- [tests](tests) contains Pytest tests that can be run against the app in a CI/CD pipeline.  
- [Dockerfile](Dockerfile) is the container image definition.  
- [main.py](main.py) is the root Python module when running the application in k8s. This is the way Pytest likes the config to be.  
- [requirements.txt](requirements.txt) lists the abagdemo application's required Python libraries.  
- [rundev.sh](rundev.sh) is a helper script to run the app from a command line. This has not been used/tested recently.  
- [runit.sh](runit.sh) is the startup script that runs the application in k8s. Its copied to the container image, and run as part of the Deployment spec.  
