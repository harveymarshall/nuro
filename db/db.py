from tinydb import TinyDB, Query

db = TinyDB('db.json')

tasks_table = db.table("tasks")
lists_table = db.table("lists")
notes_table = db.table("notes")
