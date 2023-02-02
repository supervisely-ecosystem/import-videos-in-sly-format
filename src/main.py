import os, shutil
from supervisely.io.fs import silent_remove
import supervisely as sly

from dotenv import load_dotenv


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api.from_env()
STORAGE_DIR: str = sly.app.get_data_dir()


class MyImport(sly.app.Import):
    def process(self, context: sly.app.Import.Context):
        # project_dir = f.download_data_from_team_files(api=g.api, task_id=task_id, save_path=g.STORAGE_DIR)
        project_dir = context.path
        if context.is_directory is False:
            shutil.unpack_archive(project_dir, STORAGE_DIR)
            silent_remove(project_dir)
            project_name = os.listdir(STORAGE_DIR)[0]
            if len(os.listdir(STORAGE_DIR)) > 1:
                raise Exception("There must be only 1 project directory in the archive")
            project_dir = os.path.join(STORAGE_DIR, project_name)
        else:
            project_name = os.path.basename(project_dir)
        sly.upload_video_project(
            dir=project_dir,
            api=api,
            workspace_id=context.workspace_id,
            project_name=project_name,
            log_progress=True,
        )


app = MyImport()
app.run()
