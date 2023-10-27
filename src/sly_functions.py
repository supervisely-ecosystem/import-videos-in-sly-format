import functools
import os
import shutil
from os.path import basename, dirname, normpath
from typing import Callable

import supervisely as sly
from supervisely.io.fs import get_file_name_with_ext, silent_remove

import sly_globals as g


def update_progress(count, api: sly.Api, task_id: int, progress: sly.Progress) -> None:
    count = min(count, progress.total - progress.current)
    progress.iters_done(count)
    if progress.need_report():
        progress.report_progress()


def get_progress_cb(
    api: sly.Api,
    task_id: int,
    message: str,
    total: int,
    is_size: bool = False,
    func: Callable = update_progress,
) -> functools.partial:
    progress = sly.Progress(message, total, is_size=is_size)
    progress_cb = functools.partial(func, api=api, task_id=task_id, progress=progress)
    progress_cb(0)
    return progress_cb


def search_projects(dir_path):
    files = os.listdir(dir_path)
    meta_exists = "meta.json" in files
    datasets = [f for f in files if sly.fs.dir_exists(os.path.join(dir_path, f))]
    datasets_exists = len(datasets) > 0
    return meta_exists and datasets_exists


def search_videos_dir(dir_path):
    listdir = os.listdir(dir_path)
    is_video_dir = any(
        sly.fs.get_file_ext(f) in sly.video.ALLOWED_VIDEO_EXTENSIONS for f in listdir
    )
    return is_video_dir


def download_data_from_team_files(api: sly.Api, task_id: int, save_path: str) -> str:
    """Download data from remote directory in Team Files."""
    if g.INPUT_DIR:
        listdir = api.file.listdir(g.TEAM_ID, g.INPUT_DIR)
        if len(listdir) == 1 and sly.fs.get_file_ext(listdir[0]) in [".zip", ".tar"]:
            sly.logger.info(
                "Folder mode is selected, but archive file is uploaded. Switching to file mode."
            )
            g.INPUT_DIR, g.INPUT_FILE = None, listdir[0]
        elif len(listdir) > 1 and any(
            sly.fs.get_file_ext(file) in [".zip", ".tar"] for file in listdir
        ):
            raise ValueError("Multiple archives are not supported.")
        elif basename(normpath(g.INPUT_DIR)) in ["video", "ann"]:
            if len(g.INPUT_DIR.strip("/").split("/")) > 2:
                g.INPUT_DIR = dirname(dirname(normpath(g.INPUT_DIR)))
            elif len(g.INPUT_DIR.strip("/").split("/")) > 1:
                g.INPUT_DIR = dirname(normpath(g.INPUT_DIR))
        elif any(basename(normpath(x)) in ["video", "ann"] for x in listdir):
            parent_dir = dirname(normpath(g.INPUT_DIR))
            if parent_dir != "/":
                g.INPUT_DIR = parent_dir

    if g.INPUT_FILE:
        available_archive_formats = list(zip(*shutil.get_archive_formats()))[0]
        file_ext = sly.fs.get_file_ext(g.INPUT_FILE)
        if file_ext.lstrip(".") not in available_archive_formats:
            sly.logger.info("File mode is selected, but uploaded file is not archive.")
            if basename(normpath(g.INPUT_FILE)) in ["meta.json", "key_id_map.json"]:
                g.INPUT_DIR, g.INPUT_FILE = dirname(g.INPUT_FILE), None
            elif sly.video.is_valid_ext(file_ext) or file_ext == ".json":
                parent_dir = dirname(normpath(g.INPUT_FILE))
                if basename(normpath(parent_dir)) in ["video", "ann"]:
                    if len(parent_dir.strip("/").split("/")) > 2:
                        parent_dir = dirname(dirname(normpath(parent_dir)))
                    elif len(parent_dir.strip("/").split("/")) > 1:
                        parent_dir = dirname(normpath(parent_dir))
                if not parent_dir.endswith("/"):
                    parent_dir += "/"
                g.INPUT_DIR, g.INPUT_FILE = parent_dir, None

    storage_dir = None
    if g.INPUT_DIR is not None:
        if g.IS_ON_AGENT:
            agent_id, cur_files_path = api.file.parse_agent_id_and_path(g.INPUT_DIR)
        else:
            cur_files_path = g.INPUT_DIR

        remote_path = g.INPUT_DIR
        storage_dir = os.path.join(save_path, os.path.basename(os.path.normpath(cur_files_path)))
        sizeb = api.file.get_directory_size(g.TEAM_ID, remote_path)
        progress_cb = get_progress_cb(
            api=api,
            task_id=task_id,
            message=f"Downloading {remote_path.lstrip('/').rstrip('/')}",
            total=sizeb,
            is_size=True,
        )
        api.file.download_directory(
            team_id=g.TEAM_ID,
            remote_path=remote_path,
            local_save_path=storage_dir,
            progress_cb=progress_cb,
        )
        sly.fs.remove_junk_from_dir(storage_dir)

    elif g.INPUT_FILE is not None:
        if g.IS_ON_AGENT:
            agent_id, cur_files_path = api.file.parse_agent_id_and_path(g.INPUT_FILE)
        else:
            cur_files_path = g.INPUT_FILE

        remote_path = g.INPUT_FILE
        save_archive_path = os.path.join(save_path, get_file_name_with_ext(cur_files_path))
        sizeb = api.file.get_info_by_path(g.TEAM_ID, remote_path).sizeb
        progress_cb = get_progress_cb(
            api=api,
            task_id=task_id,
            message=f"Downloading {remote_path.lstrip('/')}",
            total=sizeb,
            is_size=True,
        )
        api.file.download(
            team_id=g.TEAM_ID,
            remote_path=remote_path,
            local_save_path=save_archive_path,
            progress_cb=progress_cb,
        )
        sly.fs.unpack_archive(save_archive_path, save_path)
        silent_remove(save_archive_path)

        storage_dir = save_path

    project_dirs = [project_dir for project_dir in sly.fs.dirs_filter(storage_dir, search_projects)]

    only_videos = []
    if len(project_dirs) == 0:
        only_videos = [img_dir for img_dir in sly.fs.dirs_filter(storage_dir, search_videos_dir)]
    return project_dirs, only_videos


def update_progress(count, api: sly.Api, task_id: int, progress: sly.Progress) -> None:
    count = min(count, progress.total - progress.current)
    progress.iters_done(count)
    if progress.need_report():
        progress.report_progress()


def get_progress_cb(
    api: sly.Api,
    task_id: int,
    message: str,
    total: int,
    is_size: bool = False,
    func: Callable = update_progress,
) -> functools.partial:
    progress = sly.Progress(message, total, is_size=is_size)
    progress_cb = functools.partial(func, api=api, task_id=task_id, progress=progress)
    progress_cb(0)
    return progress_cb


def get_effective_ann_name(vid_name, ann_names):
    new_format_name = vid_name + g.ANN_EXT
    if new_format_name in ann_names:
        return new_format_name
    else:
        old_format_name = os.path.splitext(vid_name)[0] + g.ANN_EXT
        return old_format_name if (old_format_name in ann_names) else None


def create_empty_ann(vids_dir, vid_name, ann_dir):
    vid_path = os.path.join(vids_dir, vid_name)
    import numpy
    numpy.float = numpy.float64
    numpy.int = numpy.int_
    img_size, frames_count = sly.video.get_image_size_and_frames_count(vid_path)
    ann = sly.VideoAnnotation(img_size, frames_count)
    ann_name = vid_name + g.ANN_EXT
    sly.json.dump_json_file(ann.to_json(), os.path.join(ann_dir, ann_name))
    return ann_name


def upload_only_videos(api: sly.Api, task_id, vid_dirs: list):
    project_name = "Videos project"
    project = api.project.create(
        g.WORKSPACE_ID, project_name, type=sly.ProjectType.VIDEOS, change_name_if_conflict=True
    )
    videos_cnt = 0
    for vid_dir in vid_dirs:
        if not sly.fs.dir_exists(vid_dir):
            continue
        video_paths = sly.fs.list_files(
            vid_dir,
            valid_extensions=sly.video.ALLOWED_VIDEO_EXTENSIONS,
            ignore_valid_extensions_case=True,
        )
        if len(video_paths) == 0:
            continue
        total_size = sum([sly.fs.get_file_size(path) for path in video_paths])
        dataset_name = os.path.basename(os.path.normpath(vid_dir))
        progress_project_cb = get_progress_cb(
            api,
            task_id,
            f"Uploading videos from directory '{vid_dir}' to dataset '{dataset_name}'",
            total_size,
        )
        dataset = api.dataset.create(project.id, dataset_name, change_name_if_conflict=True)
        video_names = [
            os.path.basename(path) for path in video_paths if sly.video.has_valid_ext(path)
        ]
        videos = api.video.upload_paths(dataset.id, video_names, video_paths, progress_project_cb)
        videos_cnt += len(videos)
    if videos_cnt > 0:
        sly.logger.info(f"{videos_cnt} videos were uploaded to project '{project_name}'.")

    return project.name