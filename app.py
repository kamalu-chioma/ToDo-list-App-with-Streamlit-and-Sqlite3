import streamlit as st
import pandas as pd 
from db_funcs import * 
import streamlit.components.v1 as stc
import random
import openai
import os
import plotly.express as px 
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI(
    api_key = os.getenv("open_ai_key"),
)

#openai.api_key = os.getenv('open_ai_key')

# openai.api_key = st.secrets.get("open_ai_key")


HTML_BANNER = """
    <div style="background-color:#800080; padding:30px; border-radius:15px">
    <h2 style="color:silver; text-align:center;" > ToDo App</h2>
    </div>
    """

def main():
    stc.html(HTML_BANNER)

    menu = ["Create","Read","Update","Delete","AI help", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    st.markdown("## Menu")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    if col1.button("Create"):
        choice = "Create"
    if col2.button("Read"):
        choice = "Read"
    if col3.button("Update"):
        choice = "Update"
    if col4.button("Delete"):
        choice = "Delete"
    if col5.button("AI help"):
        choice = "AI help"
    if col6.button("About"):
        choice = "About"

    create_table()

    # Menu item1, Create
    if choice == "Create":
        st.subheader("Add New Task")
        col1, col2 = st.columns(2)
        
        with col1:
            task = st.text_area("Task To Do")

        with col2:
            task_status = st.selectbox("Status", ["Pending", "Doing", "Done"])
            task_due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task, task_status, task_due_date)
            st.success("Added :: {} :: To Tasks".format(task))
            st.rerun()
            

        with st.expander("View All"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Due Date"])
            st.dataframe(clean_df)

    # Menu item2, Read     
    elif choice == "Read":
        with st.expander("View All"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        with st.expander("Task Status"):
            task_df = clean_df['Status'].value_counts().to_frame().reset_index()
            task_df.columns = ['Status', 'count']
            st.dataframe(task_df)

            # Pie Chart
            pie_chart = px.pie(task_df, names='Status', values='count', title='Task Status Distribution')
            st.plotly_chart(pie_chart, use_container_width=True)

        # Automatic Categorization of Tasks
        with st.expander("Categorized Tasks"):
            tasks = [task[0] for task in result]
            categorized_tasks = categorize_tasks(tasks)
            st.dataframe(categorized_tasks)

            categories = categorized_tasks['Category'].unique()
            for category in categories:
                st.write(f"### {category}")
                st.write(categorized_tasks[categorized_tasks['Category'] == category]['Task'].tolist())

    # Menu item3, Update
    elif choice == "Update":
        st.subheader("Edit Items")
        with st.expander("Current Data"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)

        list_of_tasks = [i[0] for i in view_all_task_names()]
        selected_task = st.selectbox("Task", list_of_tasks)
        task_result = get_task(selected_task)
        
        if task_result:
            task = task_result[0][0]
            task_status = task_result[0][1]
            task_due_date = task_result[0][2]

            col1, col2 = st.columns(2)
            
            with col1:
                new_task = st.text_area("Task To Do", task)

            with col2:
                new_task_status = st.selectbox(task_status, ["Pending", "Doing", "Done"])
                new_task_due_date = st.date_input(task_due_date)

            if st.button("Update Task"):
                edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
                st.success("Updated ::{} ::To {}".format(task, new_task))

            with st.expander("View Updated Data"):
                result = view_all_data()
                clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
                st.dataframe(clean_df)

    # Menu item4, Delete
    elif choice == "Delete":
       st.subheader("Delete")
       with st.expander("View Data"):
            result = view_all_data()
            clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
            st.dataframe(clean_df)
    
    # Select multiple tasks to delete
       unique_list = [i[0] for i in view_all_task_names()]
       tasks_to_delete = st.multiselect("Select Tasks to Delete", unique_list)
    
       if st.button("Delete Selected Tasks"):
           for task in tasks_to_delete:
               delete_data(task)
           st.warning(f"Deleted tasks: {', '.join(tasks_to_delete)}")
           st.experimental_rerun()  # Refresh the app to show updated data

       with st.expander("Updated Data"):
           result = view_all_data()
           clean_df = pd.DataFrame(result, columns=["Task", "Status", "Date"])
           st.dataframe(clean_df)

            
	# Menu item5, AI Help
    elif choice == "AI help":
        st.subheader("Ask AI for Task Insights")

        # Select a task from the list
        existing_tasks = [task[0] for task in view_all_task_names()]
        selected_task = st.selectbox("Select an existing task", existing_tasks)

        # Enter a specific question or aspect of the task
        task_detail = st.text_area("Specify what aspect of the task you need help with")

        if st.button("Get Insights"):
            if selected_task and task_detail:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that helps users with concise ways to achieve their tasks."},
                        {"role": "user", "content": f"Task: {selected_task}\nDetail: {task_detail}\nProvide insights and advice on how to best achieve the task."}
                    ], 
                    max_tokens=150
                )
                insights = response.choices[0].message.content.strip()
                st.write("### AI Insights:")
                st.write(insights)
            else:
                st.warning("Please select a task and specify what aspect you need help with.")


    # Menu item6, About App
    else:
        st.subheader("App Description")
        st.info("Add a new task to your todo list, Choose task status and due date; View the task and the task status; Update or edit a task; and delete task after completion. Use ai insights for you selected task   This app demonstrates the use of CRUD operations in Streamlit")
        st.text("App by Chioma Kamalu ")

st.set_page_config(page_icon="✓", page_title="ToDo App")
        
if __name__ == '__main__':
    main()
