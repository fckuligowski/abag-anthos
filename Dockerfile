  
FROM python:3.8-alpine
# Install the Python runtime dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev
# Expose the Flask port (5000) that the app listens on
EXPOSE 5000

# Create a group and user
RUN addgroup -S abagdemogroup && adduser -S abagdemo -u 1001 -G abagdemogroup

# Copy the Python library dependency list and install the libraries
COPY requirements.txt /abagdemo/requirements.txt
WORKDIR /abagdemo
RUN pip3 install -r requirements.txt

# Copy the application source code
COPY . /abagdemo

# Get the version of image from the k8s deployment and create
# a file named version.txt with the application version.
# Then delete the k8s deploy file because we don't need it any more.
RUN sed -r -n 's/appVersion:\s+(.*)/\1/p' helm/abagdemo/Chart.yaml | sed -e 's/^[ \t]*//' > version.txt && rm helm/abagdemo/Chart.yaml && rmdir helm/abagdemo -p --ignore-fail-on-non-empty
# Change the ownership on the files so that we can run as non-root
RUN chown -R abagdemo:abagdemogroup /abagdemo
# Tell docker that all future commands should run as abagdemo (UID=1001)
USER 1001