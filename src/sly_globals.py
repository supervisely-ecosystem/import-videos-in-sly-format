import os
import sys

from dotenv import load_dotenv
from pathlib import Path

import supervisely as sly
from supervisely.io.fs import mkdir

root_source_dir = str(Path(sys.argv[0]).parents[1])
print(f"App source directory: {root_source_dir}")
sys.path.append(root_source_dir)

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

TEAM_ID = int(os.environ["context.teamId"])
WORKSPACE_ID = int(os.environ["context.workspaceId"])
TASK_ID = int(os.environ["TASK_ID"])

INPUT_DIR: str = os.environ.get("modal.state.slyFolder", None)
INPUT_FILE: str = os.environ.get("modal.state.slyFile", None)

if INPUT_DIR:
    IS_ON_AGENT = api.file.is_on_agent(INPUT_DIR)
else:
    IS_ON_AGENT = api.file.is_on_agent(INPUT_FILE)

STORAGE_DIR = sly.app.get_data_dir()
mkdir(STORAGE_DIR, True)

ANN_EXT = ".json"
