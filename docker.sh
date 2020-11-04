#!/bin/bash

# Docker Build
docker build . -t todoist-project-allocation:latest

# Docker Run
docker run -it --rm --name todoist-proj-alloc todoist-project-allocation:latest