import os

import supervisely as sly

import sly_functions as f
import sly_globals as g


@g.my_app.callback("import-images-project")
@sly.timeit
def import_images_project(
        api: sly.Api, task_id: int, context: dict, state: dict, app_logger
) -> None:
    project_dir = f.download_data_from_team_files(
        api=api, task_id=task_id, save_path=g.STORAGE_DIR
    )
    project_name = os.path.basename(project_dir)
    sly.upload_video_project(
        dir=project_dir,
        api=api,
        workspace_id=g.WORKSPACE_ID,
        project_name=project_name,
        log_progress=True,
    )
    g.my_app.stop()


def main():
    sly.logger.info(
        "Script arguments", extra={"TEAM_ID": g.TEAM_ID, "WORKSPACE_ID": g.WORKSPACE_ID}
    )
    g.my_app.run(initial_events=[{"command": "import-images-project"}])


if __name__ == "__main__":
    sly.main_wrapper("main", main)
