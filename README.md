<div align="center" markdown>

<img src="https://user-images.githubusercontent.com/48245050/182845074-905a4570-31bf-4c1a-8cb4-283157781530.jpg"/>

# Import Videos in Supervisely format

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-to-Run">How to Run</a> •
  <a href="#Demo">Demo</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com/apps/supervisely-ecosystem/import-videos-in-sly-format)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-videos-in-sly-format)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/import-videos-in-sly-format.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/import-videos-in-sly-format.png)](https://supervisely.com)

</div>

# Overview

Import videos in [Supervisely format](https://docs.supervisely.com/data-organization/00_ann_format_navi) with annotations. Supported extensions: `.avi`, `.mp4`, `.3gp`, `.flv`, `.webm`, `.wmv`, `.mov`, `.mkv`.

🏋️ Starting from version `v1.1.0` application supports import from special directory on your local computer. It is made for Enterprise Edition customers who need to upload tens or even hundreds of gigabytes of data without using drag-ang-drop mechanism:

1. Run agent on your computer where data is stored. Watch [how-to video](https://youtu.be/aO7Zc4kTrVg).
2. Copy your data to special folder on your computer that was created by agent. Agent mounts this directory to your Supervisely instance and it becomes accessible in Team Files. Learn more [in documentation](https://docs.supervisely.com/customization/agents/agent-storage). Watch [how-to video](https://youtu.be/63Kc8Xq9H0U).
3. Go to `Team Files` -> `Supervisely Agent` and find your folder there.
4. Right click to open context menu and start app. Now app will upload data directly from your computer to the platform.

#### Input files structure

You can upload a directory or an archive. If you are uploading an archive, it must contain a single top-level directory.

Directory name defines project name. Subdirectories define dataset names.<br>
ℹ️ You can download the archive with data example [here](https://github.com/supervisely-ecosystem/import-videos-in-sly-format/files/12546490/my_videos_project.zip).<br>

Project directory example:

```

videos_example_project
├── ds0
│   ├── ann
│   │   ├── sea_lion.mp4.json
│   │   └── cars.mp4.json
│   └── video
│       ├── sea_lion.mp4
│       └── cars.mp4
├── key_id_map.json (optional)
└── meta.json

```

As a result we will get project `videos_example_project` with 1 dataset named: `ds0`.

# How to Run

**Step 1.** Add [Import videos in Supervisely format](https://ecosystem.supervisely.com/apps/supervisely-ecosystem/import-videos-in-sly-format) app to your team from Ecosystem

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-videos-in-sly-format" src="https://i.imgur.com/Fp3AaKn.png" width="350px" style='padding-bottom: 10px'/>

**Step 2.** Run the application from the context menu of the directory with images on Team Files page

<img src="https://i.imgur.com/gcpgmqO.png" width="80%" style='padding-top: 10px'>  

**Step 3.** Press the Run button in the modal window

<img src="https://i.imgur.com/V8mWuPz.png" width="80%" style='padding-top: 10px'>

**Step 4.** After running the application, you will be redirected to the Tasks page. Once application processing has finished, your project will become available. Click on the project name to open it.

<img src="https://i.imgur.com/aKshaPm.png" width="80%" style='padding-top: 10px'>

### Demo
Example of uploading videos project with annotations to Supervisely:
![](https://i.imgur.com/xWPcmLJ.gif)


