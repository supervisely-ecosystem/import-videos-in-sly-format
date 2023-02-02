import os

import supervisely as sly

# import sly_functions as f
import sly_globals as g


class MyImport(sly.app.Import):

    def process(self, context: sly.app.Import.Context):
        # project_dir = f.download_data_from_team_files(api=g.api, task_id=task_id, save_path=g.STORAGE_DIR)
        project_dir = context.path
        project_name = os.path.basename(project_dir)
        sly.upload_video_project(
            dir=project_dir,
            api=g.api,
            workspace_id=context.workspace_id,
            project_name=project_name,
            log_progress=True,
    )


app = MyImport()
app.run()
