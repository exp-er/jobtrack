import streamlit as st
import pandas as pd
from io import BytesIO

REQUIRED_HEADERS = [
    "ID", "Job Title", "Company Name", "Application Status", "Date of Application",
    "Job Analysis", "Company Research", "Resume Update", "Cover Letter Update",
    "Update LinkedIn", "Application Submission", "Follow Up", "Interview Preparation",
    "Thank You"
]



def upload_file():
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    # Upload a CSV file


    if uploaded_file is not None:
        df_temp = pd.read_csv(uploaded_file)
        if all(header in df_temp.columns for header in REQUIRED_HEADERS):
            st.session_state.df = df_temp
            st.sidebar.success("File uploaded and validated successfully!")
            st.sidebar.info("Toggle again to continue")
            
        else:
            missing_headers = [header for header in REQUIRED_HEADERS if header not in df_temp.columns]
            st.error(f"The uploaded file is missing the following required headers: {', '.join(missing_headers)}")
            st.stop()

def main():
    st.title("Application Tracking & Refinement")

    # Initialize session state for DataFrame if not already present
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=REQUIRED_HEADERS)

    # Function to download the current DataFrame as a CSV file
    # st.info("Do not forget to download at session end")
    # def download_data():
    #     st.session_state.df.to_csv("job_data.csv", index=False)
    # st.sidebar.button("Download Data", on_click=download_data)

    if st.sidebar.toggle("Upload Data"):
        upload_file()
        
    
    else:
        
        def download_data():
            st.session_state.df.to_csv("job_data.csv", index=False)
        st.sidebar.button("Download Data", on_click=download_data)
    # Function to add a new job entry
        def add_job():
            st.write("Add a new job entry")
            with st.form("add_job_form"):
                id = st.text_input("ID")
                job_title = st.text_input("Job Title")
                company_name = st.text_input("Company Name")
                application_status = st.selectbox("Application Status", ["Applied", "Interviewed", "Offer Received", "Rejected"])
                date_of_application = st.date_input("Date of Application")
                submitted = st.form_submit_button("Add Job")
                
                # ID validation to ensure uniqueness
                if submitted:
                    if id in st.session_state.df["ID"].values:
                        st.error("The ID already exists. Please use a different ID.")
                    else:
                        new_entry = {
                            "ID": id,
                            "Job Title": job_title,
                            "Company Name": company_name,
                            "Application Status": application_status,
                            "Date of Application": date_of_application,
                            "Job Analysis": False,
                            "Company Research": False,
                            "Resume Update": False,
                            "Cover Letter Update": False,
                            "Update LinkedIn": False,
                            "Application Submission": False,
                            "Follow Up": False,
                            "Interview Preparation": False,
                            "Thank You": False,
                        }
                        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_entry])], ignore_index=True)
                        st.success("Job entry added successfully.")
                        st.write(st.session_state.df)

        # Function to update an existing job's checklist
        def update_job():
            job_selection = st.selectbox(
                "Select Job Application",
                st.session_state.df["ID"]
            )
            row = st.session_state.df[st.session_state.df["ID"] == job_selection].iloc[0]

            st.header(f"Checklist for {row['Job Title']} at {row['Company Name']}")
            with st.form(f"checklist_{row['ID']}"):
                analyze_profile = st.checkbox("Analyze Job Role / Profile", value=row["Job Analysis"])
                research_company = st.checkbox("Research the Company", value=row["Company Research"])
                customize_resume = st.checkbox("Customize Your Resume", value=row["Resume Update"])
                customize_cover_letter = st.checkbox("Customize Cover Letter", value=row["Cover Letter Update"])
                update_linkedin = st.checkbox("Update LinkedIn", value=row["Update LinkedIn"])
                submit_application = st.checkbox("Submit the Application", value=row["Application Submission"])
                prepare_follow_up = st.checkbox("Prepare for Follow-Up", value=row["Follow Up"])
                interview_preparation = st.checkbox("Interview Preparation", value=row["Interview Preparation"])
                thank_you_email = st.checkbox("Thank You E-mail", value=row["Thank You"])
                submitted = st.form_submit_button("Update Status")
                if submitted:
                    st.session_state.df.loc[row.name, "Job Analysis"] = analyze_profile
                    st.session_state.df.loc[row.name, "Company Research"] = research_company
                    st.session_state.df.loc[row.name, "Resume Update"] = customize_resume
                    st.session_state.df.loc[row.name, "Cover Letter Update"] = customize_cover_letter
                    st.session_state.df.loc[row.name, "Update LinkedIn"] = update_linkedin
                    st.session_state.df.loc[row.name, "Application Submission"] = submit_application
                    st.session_state.df.loc[row.name, "Follow Up"] = prepare_follow_up
                    st.session_state.df.loc[row.name, "Interview Preparation"] = interview_preparation
                    st.session_state.df.loc[row.name, "Thank You"] = thank_you_email
                    st.success("Application status updated successfully!")

        # Function to manage and display a generic checklist
        def checklist():
            checklist_data = st.session_state.get('checklist', {
                "Analyze Job Role / Profile": False,
                "Research the Company": False,
                "Customize Your Resume": False,
                "Customize Cover Letter": False,
                "Update LinkedIn": False,
                "Submit the Application": False,
                "Prepare for Follow-Up": False,
                "Interview Preparation": False,
                "Thank You E-mail": False
            })
            completed_tasks = {}
            for task, state in checklist_data.items():
                completed_tasks[task] = st.checkbox(task, value=state)
            completed_count = sum(completed_tasks.values())
            total_tasks = len(completed_tasks)
            progress = int((completed_count / total_tasks) * 100)
            st.progress(progress)
            st.write(f"Progress: {completed_count} out of {total_tasks} tasks completed")
            if st.button("Reset Checklist"):
                st.session_state.checklist = {task: False for task in checklist_data}
                st.experimental_rerun()
            st.sidebar.header("Task Status")
            st.sidebar.success("Completed Tasks")
            for task, is_completed in completed_tasks.items():
                if is_completed:
                    st.sidebar.write(f"- {task}")
            st.sidebar.info("Pending Tasks")
            for task, is_completed in completed_tasks.items():
                if not is_completed:
                    st.sidebar.write(f"- {task}")
            st.session_state.checklist = completed_tasks

        # Radio button menu for different functionalities
        menu = st.radio("", ["Data", "Add Job", "Update Job", "Checklist"], horizontal=True)
        if menu == "Add Job":
            add_job()
        elif menu == "Data":
            st.write(st.session_state.df)
        elif menu == "Update Job":
            update_job()
        elif menu == "Checklist":
            checklist()

    st.divider()

    st.error("Do not forget to download data at the end of the session")

    st.sidebar.warning("Akshat Pande")

if __name__ == '__main__':
    main()
