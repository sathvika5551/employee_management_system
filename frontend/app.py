import streamlit as st
import requests
from datetime import date


# =========================================================
# CONFIGURATION
# =========================================================

API = "https://employee-management-system-pnaj.onrender.com"

st.set_page_config(
    page_title="Employee Management System",
    page_icon="👥",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "selected_employee" not in st.session_state:
    st.session_state.selected_employee = None


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .employee-card {
        background-color: white;
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.10);
    }

    .employee-name {
        font-size: 25px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .employee-info {
        font-size: 17px;
        margin: 8px 0px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# GET EMPLOYEES
# =========================================================

def get_employees():

    try:
        response = requests.get(
            f"{API}/employees",
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

        st.error("Failed to get employees.")

    except requests.exceptions.RequestException:
        st.error(
            "Cannot connect to FastAPI. "
            "Make sure FastAPI is running."
        )

    return []


# =========================================================
# LOAD EMPLOYEES
# =========================================================

employees = get_employees()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 👥 Employee System")

    st.markdown("---")

    st.markdown("### MENU")

    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):
        st.session_state.page = "Dashboard"
        st.session_state.selected_employee = None
        st.rerun()

    if st.button(
        "➕ Add Employee",
        use_container_width=True
    ):
        st.session_state.page = "Add Employee"
        st.session_state.selected_employee = None
        st.rerun()

    if st.button(
        "✏️ Update Employee",
        use_container_width=True
    ):
        st.session_state.page = "Update Employee"
        st.session_state.selected_employee = None
        st.rerun()

    if st.button(
        "🗑️ Delete Employee",
        use_container_width=True
    ):
        st.session_state.page = "Delete Employee"
        st.session_state.selected_employee = None
        st.rerun()




# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    st.title("👥 Employee Management System")

    st.write(f"Total Employees: **{len(employees)}**")

    st.markdown("---")

    if not employees:

        st.info("No employees found.")

    else:

        for emp in employees:

            with st.container(border=True):

                st.subheader(f"👤 {emp['name']}")

                col1, col2 = st.columns(2)

                with col1:

                    st.write(f"📧 **Email:** {emp['email']}")

                    st.write(f"📞 **Phone:** {emp['phone']}")

                    st.write(f"🏢 **Department:** {emp['department']}")

                with col2:

                    st.write(
                        f"💼 **Designation:** {emp['designation']}"
                    )

                    st.write(
                        f"💰 **Salary:** ₹{float(emp['salary']):,.2f}"
                    )

                    st.write(
                        f"📅 **Joining Date:** {emp['joining_date']}"
                    )

                if st.button(
                    "🗑️ Delete",
                    key=f"dashboard_delete_{emp['id']}",
                    use_container_width=True
                ):

                    try:

                        response = requests.delete(
                            f"{API}/employees/{emp['id']}",
                            timeout=5
                        )

                        if response.status_code == 200:

                            st.success(
                                "Employee deleted successfully!"
                            )

                            st.rerun()

                        else:

                            try:
                                message = response.json().get(
                                    "detail",
                                    "Delete failed"
                                )
                            except:
                                message = "Delete failed"

                            st.error(message)

                    except requests.exceptions.RequestException:

                        st.error(
                            "Cannot connect to FastAPI."
                        )
# =========================================================
# ADD EMPLOYEE
# =========================================================

elif st.session_state.page == "Add Employee":

    st.title("➕ Add Employee")

    st.write("Enter employee details.")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("Name")

        email = st.text_input("Email")

        phone = st.text_input("Phone")

        department = st.text_input("Department")

    with col2:

        designation = st.text_input("Designation")

        salary = st.number_input(
            "Salary",
            min_value=0.0,
            max_value=99999999.99,
            step=1000.0
        )

        joining_date = st.date_input(
            "Joining Date",
            value=date.today()
        )

    st.markdown("---")

    if st.button(
        "➕ Add Employee",
        use_container_width=True
    ):

        if not name or not email:

            st.warning(
                "Name and Email are required."
            )

        else:

            employee = {
                "name": name,
                "email": email,
                "phone": phone,
                "department": department,
                "designation": designation,
                "salary": salary,
                "joining_date": str(joining_date)
            }

            try:

                response = requests.post(
                    f"{API}/employees",
                    json=employee,
                    timeout=5
                )

                if response.status_code == 200:

                    st.success(
                        "Employee added successfully!"
                    )

                    st.rerun()

                else:

                    try:
                        message = response.json().get(
                            "detail",
                            "Failed to add employee"
                        )
                    except:
                        message = "Failed to add employee"

                    st.error(message)

            except requests.exceptions.RequestException:

                st.error(
                    "Cannot connect to FastAPI."
                )


# =========================================================
# UPDATE EMPLOYEE
# =========================================================

elif st.session_state.page == "Update Employee":

    st.title("✏️ Update Employee")

    st.write("Select an employee to update.")

    st.markdown("---")

    if not employees:

        st.info("No employees found.")

    else:

        for emp in employees:

            if st.button(
                f"👤 {emp['name']}",
                key=f"update_select_{emp['id']}",
                use_container_width=True
            ):

                st.session_state.selected_employee = emp["id"]

                st.rerun()

    selected_id = st.session_state.selected_employee

    if selected_id:

        selected = None

        for emp in employees:

            if emp["id"] == selected_id:

                selected = emp
                break

        if selected:

            st.markdown("---")

            st.subheader(
                f"✏️ Update {selected['name']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                name = st.text_input(
                    "Name",
                    value=selected["name"]
                )

                email = st.text_input(
                    "Email",
                    value=selected["email"]
                )

                phone = st.text_input(
                    "Phone",
                    value=selected["phone"]
                )

                department = st.text_input(
                    "Department",
                    value=selected["department"]
                )

            with col2:

                designation = st.text_input(
                    "Designation",
                    value=selected["designation"]
                )

                salary = st.number_input(
                    "Salary",
                    min_value=0.0,
                    max_value=99999999.99,
                    value=float(selected["salary"]),
                    step=1000.0
                )

                old_date = selected["joining_date"]

                try:

                    if isinstance(old_date, str):

                        old_date = date.fromisoformat(
                            old_date
                        )

                except:

                    old_date = date.today()

                joining_date = st.date_input(
                    "Joining Date",
                    value=old_date
                )

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Update Employee",
                    use_container_width=True
                ):

                    employee = {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "department": department,
                        "designation": designation,
                        "salary": salary,
                        "joining_date": str(joining_date)
                    }

                    try:

                        response = requests.put(
                            f"{API}/employees/{selected_id}",
                            json=employee,
                            timeout=5
                        )

                        if response.status_code == 200:

                            st.success(
                                "Employee updated successfully!"
                            )

                            st.session_state.selected_employee = None

                            st.rerun()

                        else:

                            try:
                                message = response.json().get(
                                    "detail",
                                    "Update failed"
                                )
                            except:
                                message = "Update failed"

                            st.error(message)

                    except requests.exceptions.RequestException:

                        st.error(
                            "Cannot connect to FastAPI."
                        )

            with col2:

                if st.button(
                    "❌ Cancel",
                    use_container_width=True
                ):

                    st.session_state.selected_employee = None

                    st.rerun()


# =========================================================
# DELETE EMPLOYEE
# =========================================================

elif st.session_state.page == "Delete Employee":

    st.title("🗑️ Delete Employee")

    st.write("Select an employee to delete.")

    st.markdown("---")

    if not employees:

        st.info("No employees found.")

    else:

        for emp in employees:

            col1, col2 = st.columns([6, 1])

            with col1:

                st.subheader(f"👤 {emp['name']}")

                st.write(f"📧 **Email:** {emp['email']}")

                st.write(f"📞 **Phone:** {emp['phone']}")

            with col2:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_page_{emp['id']}",
                    use_container_width=True
                ):

                    try:

                        response = requests.delete(
                            f"{API}/employees/{emp['id']}",
                            timeout=5
                        )

                        if response.status_code == 200:

                            st.success(
                                "Employee deleted successfully!"
                            )

                            st.rerun()

                        else:

                            try:
                                message = response.json().get(
                                    "detail",
                                    "Delete failed"
                                )
                            except:
                                message = "Delete failed"

                            st.error(message)

                    except requests.exceptions.RequestException:

                        st.error(
                            "Cannot connect to FastAPI."
                        )