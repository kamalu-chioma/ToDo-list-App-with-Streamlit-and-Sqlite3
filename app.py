import streamlit as st
import pandas as pd 
from db_funcs import * 
import streamlit.components.v1 as stc



# Data Viz Pkgs
import plotly.express as px 


HTML_BANNER = """
    <div style="background-color:#800080; padding:30px; border-radius:15px">
    <h2 style="color:silver; text-align:center;" > ToDo App</h2>
    
    </div>
    """


def main():
	stc.html(HTML_BANNER)


	menu = ["Create","Read","Update","Delete","About"]
	choice = st.sidebar.selectbox("Menu", menu)
	create_table()

	#menu item1, Create
	if choice == "Create":
		st.subheader("Add New Task")
		col1,col2 = st.columns(2)
		
		with col1:
			task = st.text_area("Task To Do")

		with col2:
			task_status = st.selectbox("Status",["Pending","Doing","Done"])
			task_due_date = st.date_input("Due Date")

		if st.button("Add Task"):
			add_data(task,task_status,task_due_date)
			st.success("Added ::{} ::To Task".format(task))


	#menu item2, Read		
	elif choice == "Read":
		# st.subheader("View Items")
		with st.expander("View All"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		with st.expander("Task Status"):
			task_df = clean_df['Status'].value_counts().to_frame()
			# st.dataframe(task_df)
			task_df = task_df.reset_index()
			st.dataframe(task_df)

			# p1 = px.pie(task_df,names='index',values='Status')
			# st.plotly_chart(p1,use_container_width=True)

	#menu item3, Update
	elif choice == "Update":
		st.subheader("Edit Items")
		with st.expander("Current Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Task",list_of_tasks)
		task_result = get_task(selected_task)
		# st.write(task_result)
		
		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			col1,col2 = st.columns(2)
			
			with col1:
				new_task = st.text_area("Task To Do",task)

			with col2:
				new_task_status = st.selectbox(task_status,["Pending","Doing","Done"])
				new_task_due_date = st.date_input(task_due_date)

			if st.button("Update Task"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Updated ::{} ::To {}".format(task,new_task))

			with st.expander("View Updated Data"):
				result = view_all_data()
				# st.write(result)
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
				st.dataframe(clean_df)

	#menu item4, Delete
	elif choice == "Delete":
		st.subheader("Delete")
		with st.expander("View Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Select Task",unique_list)
		if st.button("Delete"):
			delete_data(delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))

		with st.expander("Updated Data"):
			result = view_all_data()
			# st.write(result)
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df)
			
        #menu item5, About App
	else:
		st.subheader("App Description")
		st.info("Add a new task to your todo list, Choose task status and due date; View the task and the task status; Update or edit a task; and delete task after completion.  This app demonstrates the use of CRUD operations in Streamlit")
		st.text("App by Chioma Kamalu ")

st.set_page_config(page_icon="✓", page_title="ToDo App")
		   
		   
if __name__ == '__main__':
	main()
