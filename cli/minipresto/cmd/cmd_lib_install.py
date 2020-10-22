#!usr/bin/env/python3
# -*- coding: utf-8 -*-

import os
import sys
import click
import shutil

import minipresto.cli
import minipresto.errors as err
import minipresto.utils as utils


# fmt: off
@click.command("lib_install", help="""
Install the Minipresto library.
""")
@click.option("-v", "--version", default="", type=str, help="""
The version of the library to install. 
""")
# fmt: on


@utils.exception_handler
@minipresto.cli.pass_environment
def cli(ctx, version):
    """Library installation command for Minipresto."""

    if not version:
        version = utils.get_cli_ver()

    lib_dir = os.path.join(ctx.minipresto_user_dir, "lib")
    if os.path.isdir(lib_dir):
        response = ctx.logger.prompt_msg(
            f"The Minipresto library at {lib_dir} will be overwritten. "
            f"Continue? [Y/N]"
        )
        if utils.validate_yes(response):
            ctx.logger.log(
                "Removing existing library directory...", level=ctx.logger.verbose
            )
            shutil.rmtree(lib_dir)
        else:
            ctx.logger.log("Opted to skip library installation.")
            sys.exit(0)

    # Download version tarball
    github_uri = f"https://github.com/jefflester/minipresto/archive/{version}.tar.gz"
    tarball = os.path.join(ctx.minipresto_user_dir, f"{version}.tar.gz")

    cmd = f"curl -fsSL {github_uri} > {tarball}"
    ctx.cmd_executor.execute_commands(cmd)

    if not os.path.isfile(tarball):
        raise err.MiniprestoError(
            f"Failed to download Minipresto library ({tarball} not found)."
        )

    # Unpack tarball and copy lib
    ctx.logger.log(
        f"Unpacking tarball at {tarball} and copying library...",
        level=ctx.logger.verbose,
    )

    file_basename = f"minipresto-{version}"
    lib_dir = os.path.join(ctx.minipresto_user_dir, file_basename, "lib")
    ctx.cmd_executor.execute_commands(
        f"tar -xzvf {tarball} -C {ctx.minipresto_user_dir}",
        f"mv {lib_dir} {ctx.minipresto_user_dir}",
        f"rm -rf {tarball} {os.path.join(ctx.minipresto_user_dir, file_basename)}",
    )

    # Check that the library is present
    lib_dir = os.path.join(ctx.minipresto_user_dir, "lib")
    if not os.path.isdir(lib_dir):
        raise err.MiniprestoError(f"Library failed to install (not found at {lib_dir})")

    ctx.logger.log("Library installation complete.")