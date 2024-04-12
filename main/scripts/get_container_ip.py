import subprocess
import json

def get_redis_ip():
    # Run the docker inspect command to get information about the redis container
    result = subprocess.run(["docker", "inspect", "redis"], capture_output=True, text=True)
    
    # Parse the output as JSON
    container_info = json.loads(result.stdout)
    
    # Extract the IP address from the container information
    ip_address = container_info[0]['NetworkSettings']['IPAddress']
    return ip_address