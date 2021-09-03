# IP_ADDR is the ip address that the Pod can be reached at
export IP_ADDR=$1
# Get
echo "Testing GET"
curl "$IP_ADDR:5000/history/002"
# POST
export SCAN_DATE=`date "+%Y-%m-%d %H:%M:%S"`
echo "Testing POST - scan date: $SCAN_DATE"
curl --header "Content-Type: application/json" \
	--request POST \
	--data "{\"bag\": \"002\", \"scan_time\": \"$SCAN_DATE\", \"location\": \"AATEST002\"}" \
	"$IP_ADDR:5000/scan"
# GET record we created
curl "$IP_ADDR:5000/status/002"
