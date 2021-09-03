# Pass the path of the Service Account's Key credentials.json file
# as the first parameter. A secret will be created, with the base name
# of the file accessible to pod specs.
KEY_FILE=$1
kubectl create secret generic abagdemo-gcp-creds \
--from-file=$KEY_FILE -n abagdemo \
--dry-run -o yaml | kubectl apply -f -

# kubectl create secret generic abagdemo-gcp-creds \
# --from-file=./instance/creds/hazel-math-279814.json -n abagdemo \
# --dry-run -o yaml | kubectl apply -f -