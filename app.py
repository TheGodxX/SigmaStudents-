import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt



st.set_page_config(
    page_title="Student Toolkit",
    page_icon="📚",
    layout="wide"
)


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Login Required")

    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Login"):
        if password == "Sigmastudents":
            st.session_state.authenticated = True
            st.success("✅ Access Granted")
            st.rerun()
        else:
            st.error("❌ Incorrect Password")

    st.stop()


def show_timetable():
    st.title("🗓️ Timetable Schedule")
    st.subheader("Engage with studies")

    selected_day = st.radio(
        "Select the day to view the schedule:",
        ["Select", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        horizontal=True
    )

    schedules = {
        "Monday": {
            "Period": [1, 2, 3, 4, "Lunch", 5, 6, 7, 8],
            "Subject": ["Maths", "Physics", "Chemistry", "Science Practicals", "Lunch", "PT", "HPE", "Chemistry", "CS"],
            "Time": ["9:00-9:45", "9:45-10:30", "10:30-11:15", "11:15-12:15", "12:15-1:00", "1:00-1:45", "1:45-2:30", "2:30-3:00", "3:00-3:45"]
        },
        "Tuesday": {
            "Period": [1, 2, 3, 4, "Lunch", 5, 6, 7, 8],
            "Subject": ["English", "Maths", "Physics", "Chemistry", "Lunch", "CS", "PT", "Maths Lab", "English"],
            "Time": ["9:00-9:45", "9:45-10:30", "10:30-11:15", "11:15-12:15", "12:15-1:00", "1:00-1:45", "1:45-2:30", "2:30-3:00", "3:00-3:45"]
        },
        "Wednesday": {
            "Period": [1, 2, 3, 4, "Lunch", 5, 6, 7, 8],
            "Subject": ["English", "CS", "Physics", "Chemistry", "Lunch", "CS", "PT", "Art", "English"],
            "Time": ["9:00-9:45", "9:45-10:30", "10:30-11:15", "11:15-12:15", "12:15-1:00", "1:00-1:45", "1:45-2:30", "2:30-3:00", "3:00-3:45"]
        },
        "Thursday": {
            "Period": [1, 2, 3, 4, "Lunch", 5, 6, 7, 8],
            "Subject": ["English", "Chemistry", "Physics", "Maths", "Lunch", "CS", "PT", "Science Practicals", "English"],
            "Time": ["9:00-9:45", "9:45-10:30", "10:30-11:15", "11:15-12:15", "12:15-1:00", "1:00-1:45", "1:45-2:30", "2:30-3:00", "3:00-3:45"]
        },
        "Friday": {
            "Period": [1, 2, 3, 4, "Lunch", 5, 6, 7, 8],
            "Subject": ["English", "Maths", "Physics", "Chemistry", "Lunch", "CS", "PT", "Science Practicals", "English"],
            "Time": ["9:00-9:45", "9:45-10:30", "10:30-11:15", "11:15-12:15", "12:15-1:00", "1:00-1:45", "1:45-2:30", "2:30-3:00", "3:00-3:45"]
        }
    }

    if selected_day in schedules:
        df = pd.DataFrame(schedules[selected_day])
        st.dataframe(df, use_container_width=True)
    elif selected_day != "Select":
        st.info(f"No schedule defined for {selected_day}.")


def show_attendance_tracker():
    st.title("📝 Attendance Sheet")
    st.write("Mark attendance for each student for the week:")

    names = ["Josh", "George", "James", "Henry", "Oliver", "Alan Walker", "Eminem"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    if "attendance" not in st.session_state:
        st.session_state.attendance = pd.DataFrame(index=names, columns=days)
        st.session_state.attendance[:] = "Absent"

    attendance_df = st.session_state.attendance

    col_layout = [2] + [1] * len(days)
    header_cols = st.columns(col_layout)

    with header_cols[0]:
        st.markdown("**Student**")
    for i, day in enumerate(days):
        with header_cols[i + 1]:
            st.markdown(f"**{day}**")

    st.markdown("---")

    for name in names:
        row_cols = st.columns(col_layout)
        with row_cols[0]:
            st.markdown(f"**{name}**")
        for i, day in enumerate(days):
            with row_cols[i + 1]:
                current_value = attendance_df.at[name, day]
                try:
                    default_index = 0 if current_value == "Present" else 1
                except Exception:
                    default_index = 1

                choice = st.selectbox(
                    f"{name} {day} attendance",
                    options=["Present", "Absent"],
                    index=default_index,
                    key=f"att_{name}_{day}",
                    label_visibility="collapsed"
                )
                attendance_df.at[name, day] = choice

    st.markdown("---")
    st.subheader("✅ Final Attendance Data Table")

    # 🌈 Color coding for Present/Absent
    def color_attendance(val):
        if val == "Present":
            return "background-color: #d4edda; color: #155724; font-weight: bold;" # green
        elif val == "Absent":
            return "background-color: #f8d7da; color: #721c24; font-weight: bold;" # red
        return ""

    styled_df = attendance_df.style.applymap(color_attendance)
    st.dataframe(styled_df, use_container_width=True)

    total_present = (attendance_df == "Present").sum().sum()
    total_absent = (attendance_df == "Absent").sum().sum()

    st.markdown("---")
    st.subheader("📊 Overall Attendance Summary")

    if (total_present + total_absent) > 0:
        labels = ["Present", "Absent"]
        sizes = [total_present, total_absent]
        colors = ["#28a745", "#dc3545"] # green, red

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True}
        )
        ax.set_title("Overall Class Attendance", fontsize=14)
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("Mark attendance above to view the summary chart.")


def show_homework_tracker():
    st.title("📚 Homework Deadline Tracker")
    st.header("MAKE SURE YOU DO YOUR HOMEWORK DAILY")

    if "homework" not in st.session_state:
        st.session_state.homework = {}
    st.subheader("➕ Add New Homework")

    with st.form("add_homework_form", clear_on_submit=True):
        subject = st.text_input("Subject")
        task = st.text_area("Homework/Task")
        due_date = st.date_input("Due Date", min_value=datetime.date.today(), value=datetime.date.today())
        submitted = st.form_submit_button("Add Homework")

        if submitted:
            if subject.strip() == "" or task.strip() == "":
                st.warning("Please fill in both subject and homework task.")
            else:
                st.session_state.homework[subject.strip()] = {"task": task.strip(), "due_date": due_date}
                st.success(f"Homework for **{subject.strip()}** added successfully!")

    st.markdown("---")
    st.subheader("📋 Your Homework List")

    if not st.session_state.homework:
        st.info("No homework added yet.")
    else:
        today = datetime.date.today()
        sorted_homework = sorted(
            st.session_state.homework.items(),
            key=lambda item: item[1]['due_date']
        )
        for subject, info in sorted_homework:
            due = info["due_date"]
            days_left = (due - today).days
            if days_left > 2:
                color = "green"
                status = "On Time"
            elif days_left >= 0:
                color = "orange"
                status = "Due Today" if days_left == 0 else "Due Soon"
            else:
                color = "red"
                status = "Late"

            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; background-color: #f9f9f9;">
                    <h4 style="margin: 0; color: #2E86C1;">{subject}</h4>
                    <p style="margin: 5px 0;">{info['task']}</p>
                    <strong>Due Date:</strong> {due}<br>
                    <strong>Time Left:</strong> {abs(days_left)} day(s) {'left' if days_left >= 0 else 'late'}
                    <br><span style='font-weight: bold; color:{color};'>{status}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    if st.button("Clear All Homework"):
        st.session_state.homework = {}
        st.success("All homework cleared!")


def show_announcements():
    st.title("🏫 School Announcements Dashboard")

    st.sidebar.subheader("📂 Upload Announcements CSV (optional)")
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("No file uploaded — showing sample school announcements.")
        data = {
            "Date": ["2025-11-05", "2025-11-06", "2025-11-07", "2025-11-08"],
            "Title": ["Math Quiz", "Sports Day", "Science Fair", "PTA Meeting"],
            "Type": ["Exam", "Event", "Event", "Meeting"],
            "Grade": ["Grade 9", "All Grades", "Grade 8", "All Grades"],
            "Description": [
                "Math quiz for Grade 9 students in Room 203.",
                "Annual Sports Day – everyone join at the field!",
                "Science projects display in the school hall.",
                "Parents and teachers meeting at 3 PM in the auditorium.",
            ],
        }
        df = pd.DataFrame(data)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.sidebar.markdown("---")
    st.sidebar.header("🎯 Filter Announcements")
    grades = st.sidebar.multiselect("Select Grade(s):", df["Grade"].unique())
    types = st.sidebar.multiselect("Select Type(s):", df["Type"].unique())
    start_date = st.sidebar.date_input("Start Date:", df["Date"].min())
    end_date = st.sidebar.date_input("End Date:", df["Date"].max())

    filtered_df = df.copy()
    if grades:
        filtered_df = filtered_df[filtered_df["Grade"].isin(grades)]
    if types:
        filtered_df = filtered_df[filtered_df["Type"].isin(types)]
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(start_date))
        & (filtered_df["Date"] <= pd.to_datetime(end_date))
    ]

    st.subheader("📋 Announcements List")
    if not filtered_df.empty:
        st.dataframe(filtered_df[["Date", "Title", "Type", "Grade", "Description"]], use_container_width=True)
    else:
        st.warning("No announcements found for the selected filters.")


st.sidebar.title("📚 Student Toolkit")
tool_selection = st.sidebar.radio(
    "Choose a Tool:",
    ("Timetable", "Attendance Tracker", "Homework Tracker", "Announcements")
)
st.sidebar.markdown("---")
st.sidebar.info("Use the navigation above to manage your schedule, attendance, homework, and announcements efficiently!")

if tool_selection == "Timetable":
    show_timetable()
elif tool_selection == "Attendance Tracker":
    show_attendance_tracker()
elif tool_selection == "Homework Tracker":
    show_homework_tracker()
elif tool_selection == "Announcements":
    show_announcements()

















