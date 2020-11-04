import re
from time import sleep

from todoist.api import TodoistAPI
from todoist.managers.archive import ItemsArchiveManager

"""
Example config: ./config.py.dist
"""
from config.config import API_KEY, PROJECT_ID, USERS, DEBUG_MODE, DELAY

"""
This regex is used to remove emojis from a string
"""
emoji_pattern = re.compile(pattern="["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

# Build API
api: TodoistAPI = TodoistAPI(API_KEY)
api.sync()  # blocking

# Get Project
res = api.projects.get(PROJECT_ID)
project: dict = res['project'] if res != None else None
if res == None or project == None:
    print("😭 Project not found.")
    exit(1)

print("😄 Project found: " + project.get("name"))
in_continue: str = input("Is this the correct project? [Y/n] ")
if len(in_continue) > 0 and (in_continue.lower() != "y"):
    print("Change PROJECT_ID in config.py")
    exit(1)


def fetch_items(project_id: str) -> dict:
    items: dict = {}

    for item in api.items.all():
        item_id: int = item["id"]
        item_id_str: str = str(item_id)

        proj_id: int = item["project_id"]
        if proj_id != project_id:
            continue

        parent_id: int = item['parent_id']
        parent_id_str: str = str(parent_id)

        if parent_id == None:
            if not item_id_str in items:
                items[item_id_str] = {
                    'item': item,
                    'childs': []
                }
            else:
                items[item_id_str]['item'] = item
        else:
            if not parent_id_str in items:
                items[parent_id_str] = {
                    'item': {},
                    'childs': []
                }
            items[parent_id_str]['childs'].append(item)
            continue

        archive: ItemsArchiveManager = api.items_archive.for_parent(item_id)

        # get all sub tasks
        for item2 in archive.items():
            items[item_id_str]['childs'].append(item2)

    return items


def check():
    # was something changed and must be commited to Todoist?
    changes: int = 0

    print("👷‍♂️ Fetching items ...")
    items: dict = fetch_items(PROJECT_ID)

    if DEBUG_MODE:
        print (f"👾 Items = ")
        print(items)

    print("✅ Done! Tasks found:")

    # Print tasks
    for _id in items:
        item = items[_id]

        names: list = []

        print("📂 " + item['item']['content'])
        for child in item['childs']:
            cntnt: str = child['content']

            # strip any emojis
            cntnt = emoji_pattern.sub(r'', cntnt)
            cntnt = cntnt.lower().strip()

            names.append(cntnt)

            print (f"    👾 Cntnt = {cntnt}")

        for user in USERS:
            uid: int = USERS[user]['uid']
            name: str = USERS[user]['name']
            ignored_sections: list = USERS[user]['ignored_sections']

            if item['item']['section_id'] in ignored_sections:
                if DEBUG_MODE:
                    print (f"  👾 Skipped for {user} [{name}]")
                continue

            if not user.lower() in names:
                print(f"  👉 {user} [{name}] missing. Adding to task.")

                # Add as sub-task to main task
                api.add_item(f"  👉 {name}",
                            project_id=PROJECT_ID,
                            parent_id=_id,
                            responsible_uid=uid)

                # Commit changes
                changes += 1

    if changes > 0:
        print(f"👷‍♂️ {changes} changes - commiting to Todoist ...")
        api.commit()


if __name__ == "__main__":
    while True:
        check()

        # rebuild Todoist api because of weird cache issues
        api: TodoistAPI = TodoistAPI(API_KEY)
        api.sync()  # blocking

        print()
        print(f"⏱  {DELAY} second/s ...")
        print()

        sleep(20)
