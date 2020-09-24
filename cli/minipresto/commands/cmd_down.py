#!usr/bin/env/python3
# -*- coding: utf-8 -*-

import sys
import click

from minipresto.core import check_daemon
from minipresto.core import generate_identifier
from minipresto.cli import pass_environment

from minipresto.settings import RESOURCE_LABEL


@click.command("down", help="""
Brings down all running minipresto containers. This command follows the
behavior of `docker-compose down`, where containers are both stopped and
removed.
""")
@click.option("-k", "--keep", is_flag=True, default=False, help="""
Does not remove any containers; instead, they will only be stopped.
""")


@pass_environment
def cli(ctx, keep):
    """
    Down command for minipresto. Exits with a 0 status code if there are no
    running minipresto containers.
    """

    check_daemon()

    containers = ctx.docker_client.containers.list(
        filters={"label": RESOURCE_LABEL}, all=True
    )

    if len(containers) == 0:
        ctx.log(f"No containers to bring down.")
        sys.exit(0)

    for container in containers:
        identifier = generate_identifier(
            {"ID": container.short_id, "Name": container.name}
        )
        container.stop()
        ctx.vlog(f"Stopped container: {identifier}")
    if not keep:
        for container in containers:
            identifier = generate_identifier(
                {"ID": container.short_id, "Name": container.name}
            )
            container.remove()  # Default behavior of Compose is to remove containers
            ctx.vlog(f"Removed container: {identifier}")

    ctx.log(f"Brought down all Minipresto containers.")
