from collections import defaultdict
import os

import supervisely as sly

import sly_functions as f
import sly_globals as g


@g.my_app.callback("import-videos-project")
@sly.timeit
def import_videos_project(
        api: sly.Api, task_id: int, context: dict, state: dict, app_logger
) -> None:
    project_dirs, only_videos = f.download_data_from_team_files(
        api=api, task_id=task_id, save_path=g.STORAGE_DIR
    )
    if len(project_dirs) == 0 and len(only_videos) == 0:
        raise Exception(f"Not found any videos for import. Please, check your input data.")
    
    elif len(project_dirs) == 0 and len(only_videos) > 0:
        sly.logger.warn(
            f"Not found datasets/projects in Supervisely format. "
            f"Will upload all videos from directories: {only_videos}."
        )
        f.upload_only_videos(api, task_id, only_videos)
    else:
        sly.logger.info(
            f"Found {len(project_dirs)} project directories in the given directory. "
            f"Paths to the projects: {project_dirs}."
        )

        fails = []
        for project_dir in project_dirs:
            project_name = os.path.basename(os.path.normpath(project_dir))

            sly.logger.info(f"Working with project '{project_name}' from path '{project_dir}'.")
            meta_json = sly.json.load_json_file(os.path.join(project_dir, "meta.json"))
            meta = sly.ProjectMeta.from_json(meta_json)
            project_items_cnt = 0
            for dataset_dir in os.listdir(project_dir):
                dataset_items_cnt = 0
                failed_ann_names = defaultdict(list)
                dataset_path = os.path.join(project_dir, dataset_dir)
                vids_dir = os.path.join(dataset_path, "video")
                ann_dir = os.path.join(dataset_path, "ann")
                if not sly.fs.dir_exists(dataset_path):
                    continue
                if (
                    len(os.listdir(dataset_path)) == 0
                    or not sly.fs.dir_exists(vids_dir)
                    or len(os.listdir(vids_dir)) == 0
                ):
                    sly.fs.remove_dir(dataset_path)
                    continue
                if not sly.fs.dir_exists(ann_dir):
                    sly.fs.mkdir(ann_dir)

                vid_names = os.listdir(vids_dir)
                raw_ann_names = os.listdir(ann_dir)
                res_ann_names = []
                for vid_name in vid_names:
                    ann_name = f.get_effective_ann_name(vid_name, raw_ann_names)
                    try:
                        if ann_name is None:
                            raise Exception("Annotation file not found")
                        sly.VideoAnnotation.load_json_file(os.path.join(ann_dir, ann_name), meta)
                    except Exception as e:
                        failed_ann_names[e.args[0]].append(ann_name)
                        ann_name = f.create_empty_ann(vids_dir, vid_name, ann_dir)
                    res_ann_names.append(ann_name)
                    project_items_cnt += 1
                    dataset_items_cnt += 1
                if len(failed_ann_names) > 0:
                    for error, ann_names in failed_ann_names.items():
                        sly.logger.warn(
                            f"[{error}] error in {len(ann_names)} annotation files: {ann_names}. "
                            "Will create empty annotation files instead..."
                        )
                if dataset_items_cnt == 0:
                    sly.fs.remove_dir(dataset_path)
                    continue
                unwanted_ann_names = list(set(raw_ann_names) - set(res_ann_names))
                if len(unwanted_ann_names) > 0:
                    sly.logger.warn(
                        f"Found {len(unwanted_ann_names)} annotation files without corresponding videos: {unwanted_ann_names}. "
                    )
                    for name in unwanted_ann_names:
                        sly.fs.silent_remove(os.path.join(ann_dir, name))

            if project_items_cnt == 0:
                sly.logger.warn(
                    f"Incorrect project structure for project '{project_name}'. Skipping..."
                )
                fails.append(project_name)
                continue

            try:

                sly.logger.info(f"Start uploading project '{project_name}'...")

                project = sly.VideoProject.read_single(project_dir)
                pr_id, project_name = sly.upload_video_project(
                    dir=project_dir,
                    api=api,
                    workspace_id=g.WORKSPACE_ID,
                    project_name=project_name,
                    log_progress=True,
                )

                sly.logger.info(f"Project '{project_name}' uploaded successfully.")
            except Exception as e:
                try:
                    sly.logger.warn(f"Project '{project_name}' uploading failed: {str(e)}.")
                    project_name = f.upload_only_videos(api, task_id, [ds.item_dir for ds in project.datasets])
                except Exception as e:
                    fails.append(project_name)
                    sly.logger.warn(f"Not found videos in the directory '{project_dir}'.")

        success = len(project_dirs) - len(fails)
        if success > 0:
            sly.logger.info(
                f"{success} project{'s were' if success > 1 else ' was'} uploaded successfully."
            )
        else:
            raise Exception(f"Failed to import data. Not found videos or projects in Supervisely format.")


    g.my_app.stop()


def main():
    sly.logger.info(
        "Script arguments", extra={"TEAM_ID": g.TEAM_ID, "WORKSPACE_ID": g.WORKSPACE_ID}
    )
    g.my_app.run(initial_events=[{"command": "import-videos-project"}])


if __name__ == "__main__":
    sly.main_wrapper("main", main)
