import sqlite3
import pandas as pd
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()


def create_table():
    with sqlite3.connect('tasks.db') as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT, task_status TEXT, task_due_date DATE)')
        conn.commit()

def add_data(task, task_status, task_due_date):
    with sqlite3.connect('tasks.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO taskstable(task, task_status, task_due_date) VALUES (?, ?, ?)', (task, task_status, task_due_date))
        conn.commit()

def view_all_data():
    with sqlite3.connect('tasks.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM taskstable')
        data = c.fetchall()
    return data

def view_all_task_names():
    with sqlite3.connect('tasks.db') as conn:
        c = conn.cursor()
        c.execute('SELECT task FROM taskstable')
        data = c.fetchall()
    return data

def get_task(task):
    with sqlite3.connect('tasks.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM taskstable WHERE task = ?', (task,))
        data = c.fetchall()
    return data

def edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date):
    with sqlite3.connect('tasks.db') as conn:
        c = conn.cursor()
        c.execute('UPDATE taskstable SET task = ?, task_status = ?, task_due_date = ? WHERE task = ? AND task_status = ? AND task_due_date = ?', (new_task, new_task_status, new_task_due_date, task, task_status, task_due_date))
        conn.commit()

def delete_data(task):
    with sqlite3.connect('tasks.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM taskstable WHERE task = ?', (task,))
        conn.commit()


def categorize_task(description):
    categories = {
        'Work': ['work', 'meeting', 'office', 'report', 'email', 'project'],
        'Home': ['home', 'clean', 'chores', 'house', 'sweep', 'mop', 'dishes', 'wash', 'laundry'],
        'Study': ['study', 'exam', 'homework', 'school', 'research', 'learn', 'read', 'assignment'],
        'Exercise': ['exercise', 'gym', 'workout', 'run', 'walk', 'yoga'],
        'Shopping': ['shopping', 'buy', 'groceries', 'store'],
        'Other': ['other', 'misc']
    }
    
    description = description.lower()
    for category, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            return category
    return 'Uncategorized'

def categorize_tasks(task_list):
    tasks = pd.DataFrame(task_list, columns=['Task'])
    tasks['Category'] = tasks['Task'].apply(categorize_task)
    return tasks