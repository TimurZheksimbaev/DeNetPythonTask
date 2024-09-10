import click
import requests
from requests.auth import HTTPBasicAuth
import os
# Set the base URL of the FastAPI server
BASE_URL = "http://127.0.0.1:8000"

DOWNLOADS_DIR = "downloads/"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


# Click Group to manage multiple commands
@click.group()
def cli():
    """Client CLI for interacting with the server"""
    pass


# Register a new user command
@cli.command()
# @click.argument("username")
# @click.argument("password")
@click.option("--username", prompt="Enter your username", help="Your username")
@click.option("--password", prompt="Enter your password", help="Your password")
def register(username, password):
    """Register a new user on the server."""
    response = requests.post(f"{BASE_URL}/register", json={"username": username, "password": password})

    if response.status_code == 200:
        click.echo(f"User {username} registered successfully!")
    else:
        click.echo(f"Error: {response.json().get('detail')}")


# Upload a file command
@cli.command()
@click.argument("file_path")
@click.option("--username", prompt="Enter your username", help="Your username")
@click.option("--password", prompt="Enter your password", hide_input=True, help="Your password")
def upload(file_path, username, password):
    """Upload a file to the server."""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        auth = HTTPBasicAuth(username, password)
        response = requests.post(f"{BASE_URL}/upload", files=files, auth=auth)

    if response.status_code == 200:
        click.echo(f"File {file_path} uploaded successfully!")
    else:
        click.echo(f"Error: {response.json().get('detail')}")


# Download a file command
@cli.command()
@click.argument("filename")
@click.option("--username", prompt="Enter your username", help="Your username")
@click.option("--password", prompt="Enter your password", hide_input=True, help="Your password")
def download(filename, username, password):
    """Download a file from the server."""
    auth = HTTPBasicAuth(username, password)
    response = requests.get(f"{BASE_URL}/download", params={"filename": filename}, auth=auth)

    if response.status_code == 200:
        with open(DOWNLOADS_DIR + filename, 'wb') as f:
            f.write(response.content)
        click.echo(f"File {filename} downloaded successfully!")
    else:
        click.echo(f"Error: {response.json().get('detail')}")


# Main function to invoke CLI
if __name__ == "__main__":
    cli()
