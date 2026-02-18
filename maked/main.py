import sys

import yaml
import subprocess
import click

@click.command()
@click.version_option(package_name="maked")
@click.argument("filename", type=click.Path(exists=True), required=False)
@click.option("--dry-run", is_flag=True, help="Print the command without executing it.")
def cli(filename, dry_run):
    """Reads a Markdown file, extracts the command from the YAML front matter, and executes it."""
    if filename:
        with open(filename, 'r') as file:
            content = file.readlines()
    else:
        # If no input_file is provided, read from stdin
        content = sys.stdin.readlines()
    
    # Check if content is empty before processing further
    if not content:
        click.echo("No content received.")
        sys.exit(1)

    # Look for YAML front matter
    if content[0].strip() == "---":
        try:
            end_idx = next(i + 1 for i, line in enumerate(content[1:]) if line.strip() == "---")
            metadata = yaml.safe_load("".join(content[1:end_idx]))
            if "maked" in metadata:
                command = metadata["maked"]
                click.echo(f"Command: {command}")
                if not dry_run:
                    result = subprocess.run(command, shell=True)
                    sys.exit(result.returncode)
            else:
                click.echo("No 'maked' field found in the YAML front matter.")
                sys.exit(1)
        except (ValueError, yaml.YAMLError, StopIteration):
            click.echo("Error parsing YAML front matter.")
            sys.exit(1)
    else:
        click.echo("No YAML front matter found.")
        sys.exit(1)

if __name__ == "__main__":
    cli()

