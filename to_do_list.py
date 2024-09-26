from tkinter import *
from tkinter import messagebox
from tabulate import tabulate
import zipfile
import pandas as pd
import os

FONT_NAME = "Courier"
TASK_FILE = "task_data.txt"

# Initialize task and status lists
task = []
status = []
total_task = {"Task": task, "Status": status}

# Load tasks from file ====================================================================================================
def load_tasks_from_file():
    '''It load data from the file'''
    try:
        # Check if file exists
        if os.path.exists(TASK_FILE):
            # Read the task data file into a DataFrame
            task_df = pd.read_csv(TASK_FILE, sep="\t")
            
            if "Task" in task_df.columns and "Status" in task_df.columns:
                # Clear existing task lists
                global task, status, total_task
                task = task_df["Task"].tolist()
                status = task_df["Status"].tolist()
                total_task = {"Task": task, "Status": status}
            else:
                # If columns are incorrect, initialize with empty data
                print("File found but columns are incorrect, initializing empty task list.")
                initialize_file()

        else:
            # If the file doesn't exist, create it with the correct columns
            print("No task file found. Initializing an empty file.")
            initialize_file()

    except Exception as e:
        print(f"Error loading tasks: {e}")
        initialize_file()


# Initialize an empty task file with correct headers ======================================================================
def initialize_file():
    '''This function is designed to set up a new task file with the appropriate structure'''
    # Create an empty DataFrame with 'Task' and 'Status' columns
    task_df = pd.DataFrame(columns=["Task", "Status"])
    # Save it to the file
    task_df.to_csv(TASK_FILE, sep="\t", index=True)
    print("Initialized task file with correct headers.")

#Delete function===========================================================================================================

# Assuming you have a global DataFrame named task_df 
task_df = pd.read_csv(TASK_FILE, sep="\t", index_col=0)  # Load existing tasks from the file
def delete_task():
    '''Deletes the entire row with the given ID. ID can be 0 for the first task.'''
    global task_df  # Access the global task_df
    
    dlt_id_str = number_task_input.get()  # Get the task ID from the input

    # Input validation
    if not dlt_id_str:
        messagebox.showerror(title="Oops", message="Please don't leave 'task ID' field empty!")
        return
    
    if not dlt_id_str.isdigit():
        messagebox.showerror(title="Error", message="Please enter a valid number for Task ID.")
        return

    dlt_id = int(dlt_id_str)  # Convert the input to an integer

    # Validate the ID range (allow 0 for the first task)
    if 0 <= dlt_id < len(task_df):  # Allow 0 for the first task
        if_yes = messagebox.askokcancel(title="Confirmation", message=f"Do you want to delete Task ID {dlt_id}?")
        
        if if_yes:
            task_df.drop(task_df.index[dlt_id], inplace=True)  # Drop the row at the specified index
            task_df.to_csv(TASK_FILE, sep="\t")  # Save changes to the file
            messagebox.showinfo(title="Success", message=f"Task ID {dlt_id} deleted successfully.")
            view_all_tasks()  # Refresh the displayed tasks
            number_task_input.delete(0,END)
    else:
        messagebox.showerror(title="Error", message="Invalid Task ID. Please enter a valid ID.")

def update_status():
    '''Updates the status of a task based on the provided ID and new status.'''
    global task_df  # Access the global task_df

    # Get the task ID and new status from input fields
    id_str = number_task_input.get()
    status_inp = status_task_input.get()

    # Input validation
    if not id_str or not status_inp:
        messagebox.showerror(title="Oops", message="Please fill both 'task_id' and 'status' fields.")
        return

    if not id_str.isdigit():
        messagebox.showerror(title="Error", message="Please enter a valid number for Task ID.")
        return

    task_id = int(id_str)  # Convert the task ID to an integer

    # Validate the ID range
    if task_id >= 0 and task_id < len(task_df):  # Check if the ID is within valid range
        # Update the status of the specified task directly
        task_df.at[task_id, 'Status'] = status_inp  # Update status at the correct index
        task_df.to_csv(TASK_FILE, sep="\t", index=False)  # Save changes to the file without adding extra index

        # Show success message and refresh tasks
        messagebox.showinfo(title="Success", message=f"Task ID {task_id} status updated to '{status_inp}'.")
        view_all_tasks()  # Refresh the displayed tasks
        number_task_input.delete(0,END)
        status_task_input.delete(0,END)
    else:
        messagebox.showerror(title="Error", message="Invalid Task ID. Please enter a valid ID.")

def add_task_to_file():
    task_inp = task_input.get()
    curr_status = "Pending"

    if task_inp:
        # Confirm task addition
        is_ok = messagebox.askokcancel(title=task_inp, message=f"Do you want to add this task: {task_inp}?")

        if is_ok:
            # Append task and status to the global lists
            task.append(task_inp)
            status.append(curr_status)

            # Update the global DataFrame
            global task_df
            task_df = pd.DataFrame({"Task": task, "Status": status})

            # Save the updated tasks to the file
            task_df.to_csv(TASK_FILE, sep="\t")

            # Clear input field
            task_input.delete(0, END)
            view_all_tasks()  # Refresh the displayed tasks

    else:
        # Show error if the task input is empty
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")


# Show all tasks from file =======================================================================================================
def view_all_tasks():
    # Reload tasks from the file (to ensure we show the most recent data)
    load_tasks_from_file()

    # Convert the global dictionary (total_task) to a DataFrame
    task_df = pd.DataFrame(total_task)

    # Clear the text widget and display the updated task data
    task_text.delete('1.0', END)
    task_table = tabulate(task_df, headers="keys", tablefmt="pretty", showindex=True)
    task_text.insert('1.0', task_table)


# Creating interface for todo list ===========================================================================================================================
window = Tk()
window.title("TO DO List")
window.config(padx=20, pady=20)

canvas = Canvas(width=455, height=530)
zip_file_path = r'C:\Users\pkrit\OneDrive\Desktop\100DaysOfCode\to_do_list\jpg2png.zip'
image_inside_zip = 'todo.png'
extracted_image_path = 'to_do_list/todo.png'

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract(image_inside_zip, 'to_do_list')

logo_image = PhotoImage(file=extracted_image_path)
canvas.create_image(225, 265, image=logo_image)
canvas.grid(column=1, row=0)

# Label for task input
task_label = Label(text="Enter the Task:", font=(FONT_NAME, 15, "bold"), bg="white")
canvas.create_window(225, 130, window=task_label)

task_input = Entry(width=50, bg="#f0f0f0", font=("Arial", 11))
canvas.create_window(225, 160, window=task_input)

# Add task button
add_button = Button(width=20, text="Add Task", bg="#d3d3d3", command=add_task_to_file)
canvas.create_window(225, 195, window=add_button)

# Task number Entry
number_task_input = Entry(width=10, bg="#f0f0f0", font=("Arial", 11))
number_task_input.insert(0, "Task id")
canvas.create_window(65, 235, window=number_task_input)

# Status update Entry
status_task_input = Entry(width=35, bg="#f0f0f0", font=("Arial", 11))
status_task_input.insert(0, "Status")
canvas.create_window(280, 235, window=status_task_input)

# Delete Button
delete_button = Button(width=25, text="Delete Task", bg="#d3d3d3",command=delete_task)
canvas.create_window(115, 270, window=delete_button)

# Update button
update_button = Button(width=25, text="Update Task", bg="#d3d3d3",command=update_status)
canvas.create_window(334, 270, window=update_button)

# View all tasks button
view_button = Button(width=56, text="View all Task", bg="#d3d3d3", command=view_all_tasks)
canvas.create_window(224, 305, window=view_button)

# Exit button
exit_button = Button(width=56, text="EXIT", bg="#d3d3d3", command=exit)
canvas.create_window(224, 340, window=exit_button)

# Text widget to show all tasks
task_text = Text(width=50, height=10, bg="#f0f0f0")
canvas.create_window(224, 450, window=task_text)

# Load existing tasks from file on program start
load_tasks_from_file()

window.mainloop()
