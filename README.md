<div align="center" markdown>

<img src="" style="width: 100%;"/>

# Import Videos in Supervisely format

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-to-Run">How to Run</a> •
  <a href="#Demo">Demo</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-videos-project)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-videos-project)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-videos-project&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-videos-project&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-videos-project&counter=runs&label=runs&123)](https://supervise.ly)

</div>

# Overview

Import videos in Supervisely format with annotations. Supported extensions: `.avi`, `.mp4`, `.3gp`, `.flv`, `.webm`, `.wmv`, `.mov`, `.mkv`.

#### Input files structure

You can upload a directory or an archive. If you are uploading an archive, it must contain a single top-level directory.

Directory name defines project name. Subdirectories define dataset names.

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
├── key_id_map.json
└── meta.json

```

As a result we will get project `videos_example_project` with 1 dataset named: `ds0`.

# How to Run

**Step 1.** Add [Import videos in Supervisely format](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-images-project) app to your team from Ecosystem

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-videos-project" src="" width="350px" style='padding-bottom: 10px'/>

**Step 2.** Run the application from the context menu of the directory with images on Team Files page

<img src="" width="80%" style='padding-top: 10px'>  

**Step 3.** Press the Run button in the modal window

<img src="" width="80%" style='padding-top: 10px'>

**Step 4.** After running the application, you will be redirected to the Tasks page. Once application processing has finished, your project will become available. Click on the project name to open it.

<img src="" width="80%" style='padding-top: 10px'>

### Demo
Example of uploading videos project with annotations to Supervisely:
![]()


