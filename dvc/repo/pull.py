from __future__ import unicode_literals

import logging

from dvc.config import Config
from dvc.remote.base import RemoteBASE
from dvc.repo import locked


logger = logging.getLogger(__name__)

REPORT_TITLE = "INFO REPORT:"
LOGGER_FORMAT = "\n ".join(
    (
        "",
        REPORT_TITLE,
        "=" * len(REPORT_TITLE),
        "FETCHED AT: %(asctime)s",
        "TARGETS: %(targets)s",
        "JOBS: %(jobs)s",
        "USED ALL GIT BRANCHES? %(all_branches)s",
        "TRACKED DEPENDENCIES? %(with_deps)s",
        "USED GIT TAGS? %(all_tags)s",
        "SEARCHED TARGETS RECURSIVELY? %(recursive)s",
    )
)


@locked
def pull(
    self,
    targets=None,
    jobs=None,
    remote=None,
    all_branches=False,
    with_deps=False,
    all_tags=False,
    force=False,
    recursive=False,
):

    # Must configure the logging inside this function rather than at the module
    # level, else it will be applied to the root logger and hence all logging.
    logging.basicConfig(
        level=logging.INFO,
        format=LOGGER_FORMAT,
        datefmt='%H:%M:%S'
    )

    processed_files_count = self._fetch(
        targets,
        jobs,
        remote=remote,
        all_branches=all_branches,
        with_deps=with_deps,
        all_tags=all_tags,
        recursive=recursive,
    )
    self._checkout(
        targets=targets, with_deps=with_deps, force=force, recursive=recursive,
        warn=False
    )

    # Get defaults represented by 'None' for relevant settings:
    if not targets:
        targets = "none specified"
    if not jobs:
        jobs = RemoteBASE.JOBS
    if remote is None:  # be specific in case a remote has an alias of 'False'
        remote = Config.SECTION_REMOTE_URL  # TODO NEEDS CHANGING, this == 'url'

    # Define all data to output as an information report upon command return:
    all_data = {
        'targets': targets,
        'jobs': jobs,
        'remote': remote,
        'all_branches': all_branches,
        'with_deps': with_deps,
        'all_tags': all_tags,
        'recursive': recursive
    }
    pull_msg = "Data retrieved successfully from DVC remote storage at '{}'"
    logger.info(pull_msg.format(remote), extra=all_data)
    return processed_files_count
