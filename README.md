# todoist-project-allocation <img src="./assets/todoist-logo.png" align="right" width=200 height=200>
Little Todoist Bot written in Python.

## Why?!
I wanted a feature that would allow me to give a task to multiple users in a shared project, who could all perform these tasks individually.

The bot automatically adds each user as a sub-task to each task every 30 seconds, which are assigned to the user. These sub-tasks can now be processed individually by the user.
If all users have checked the task, it can be checked completely

## Preview
Let's say you have the project "Test" with some Tasks:
<img src="./assets/preview-before.png">

This bot will now automatically add all users to this task:
<img src="./assets/preview-multi.png">

Even with a filter for sections
<img src="./assets/preview-sections.png">