import subprocess
import time

def create_postgres_container(args=None, kwargs=None):
    """
    Create and run a PostgreSQL Docker container.
    Args:
        args: Positional arguments (not used).
        kwargs: Keyword arguments (not used).
    Returns:
        None
    """
    print("Creating PostgreSQL container...")
    subprocess.run([
        "docker", "run", "-d",
        "--name", "my_postgres",
        "-e", "POSTGRES_USER=admin",
        "-e", "POSTGRES_PASSWORD=secret",
        "-e", "POSTGRES_DB=mydb",
        "-p", "5433:5432",
        "postgres:latest"
    ], check=True)

def attach_shell():
    """
    Attach to the PostgreSQL container shell.
    """
    print("Attaching to PostgreSQL container shell...")
    # time.sleep(5)  # Wait for the container to initialize
    TIMEOUT = 30
    start = time.time()
    while True:
        try:
            subprocess.run(["docker", "exec", "-it",
                "my_postgres",
                "psql", "-U", "admin", "-d", "mydb"], check=True)
            break
        except subprocess.CalledProcessError:
            if time.time()-start>TIMEOUT:
                raise TimeoutError("Could not connect to PostgreSQL container within timeout period.")
            time.sleep(1)

def destroy_postgres_container():
    """
    Destroy the PostgreSQL container.
    """
    print("Destroying PostgreSQL container...")
    subprocess.run(["docker", "rm", "-f", "my_postgres"], check=True)

def destroy_postgres_image():
    """
    Destroy the PostgreSQL image.
    """
    print("Destroying PostgreSQL image...")
    subprocess.run(["docker", "rmi", "-f", "postgres:latest"], check=True)

if __name__ == "__main__":
    create_postgres_container()
    attach_shell()
    destroy_postgres_container()
    # destroy_postgres_image()
