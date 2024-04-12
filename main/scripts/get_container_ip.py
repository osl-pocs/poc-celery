import subprocess
import json

def get_redis_ip():
    """
    Get the IP address of the Redis container.

    This function runs the docker inspect command to retrieve information about the Redis container,
    parses the output as JSON, and extracts the IP address from the container information.

    Returns:
        str: The IP address of the Redis container.

    Raises:
        subprocess.CalledProcessError: If the docker inspect command fails.
        json.JSONDecodeError: If the output of the docker inspect command cannot be decoded as JSON.
        IndexError: If the container information does not contain the expected structure.
        KeyError: If the container information does not contain the expected keys.
    """
    # Run the docker inspect command to get information about the redis container
    result = subprocess.run(["docker", "inspect", "redis"], capture_output=True, text=True)
    
    # Parse the output as JSON
    container_info = json.loads(result.stdout)
    
    # Extract the IP address from the container information
    ip_address = container_info[0]['NetworkSettings']['IPAddress']
    return ip_address
