# staff_dashboard_metrics.py
# Functions to display staff dashboard metrics in staff_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

from streamlit_extras.metric_cards import style_metric_cards # https://arnaudmiribel.github.io/streamlit-extras/

from connect_data import STAFF_VIEW
from connect_data import ordinal

# --- Load data ---
staff_view = STAFF_VIEW.copy()  # "staff_view"

# Define summary_metrics(df):
def summary_metrics(df: pd.DataFrame = staff_view):
    """Display summary statistics of JCPAO staff"""

    cols = st.columns(5)

    cols[0].metric("Total Staff", value=len(df), delta=None, delta_color="normal")
    cols[1].metric("Executive Staff", value=len(df[df["Position"] == "Exec"]), delta=None, delta_color="normal")
    cols[2].metric("Total Attorneys", value=len(df[df["Position"].isin(['CTA', 'TTL', 'APA'])]), delta=None, delta_color="normal")
    cols[3].metric("Total Support Staff", value=len(df[df["Position"].isin(['I', 'LA', 'VA', 'SS'])]), delta=None, delta_color="normal")
    cols[4].metric("Total Interns", value=len(df[df["Position"] == 'INTERN']), delta=None, delta_color="normal")

    style_metric_cards()


# Define position_metrics(df)
def position_metrics(df: pd.DataFrame = staff_view):
    """Display job position breakdown of JCPAO staff"""

    st.subheader("💼 JCPAO Staff by Job Position")

    positions_dict = {
        'Exec': 'Executive Staff', 
        'CTA': 'Chief Trial Attorneys', 
        'TTL': 'Team Trial Leaders', 
        'APA': 'Assistant Prosecuting Attorneys',
        'I': 'Investigators',
        'VA': 'Victim Advocates',
        'LA': 'Legal Assistants',
        'SS': 'Support Staff',
        'INTERN': 'Interns'
    }

    # ----- Count and Percentage -----
    # df = df.dropna(subset=['Position'])
    position_counts = df["Position"].value_counts().reset_index()
    position_counts.columns = ["Position", "Count"]
    position_counts["Position"] = position_counts["Position"].replace(positions_dict)
    position_counts["Percent"] = (position_counts["Count"] / position_counts["Count"].sum() * 100).round(2)

    # ----- Plotly Bar Chart -----
    fig = px.bar(
        position_counts,
        x="Position",
        y="Count",
        color="Position",
        text="Count",
        title="JCPAO Staff by Job Position",
        color_discrete_sequence=px.colors.qualitative.Set2,
        custom_data=["Percent"],
        orientation="v",
        height=600
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="%{x}<br>Count: %{y}<br>Percent: %{customdata[0]:.2f}%"+"<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,
        barmode="overlay",
        xaxis_title="Job Position",
        yaxis_title="Number of Employees",
        yaxis=dict(tickmode="auto"), # linear
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Job Position Display
    position_display = st.columns(2, vertical_alignment="center") 

    with position_display[0]:
        
        # ----- Display Chart -----
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Bar chart depicting job position breakdown of JCPAO staff (n={len(df)}).")

    with position_display[1]:

        # st.dataframe 
        st.write("**Table View**")
        st.dataframe(
            position_counts, 
            column_config={
                "Percent": st.column_config.NumberColumn(
                    "Percent",
                    format="%.2f%%",
                    help=r"% of JCPAO staff"
                )
            },
            hide_index=True
        )

# Define unit_metrics(df)
def unit_metrics(df: pd.DataFrame = staff_view):
    """Display assigned unit breakdown of JCPAO staff"""

    st.subheader("🧑‍🧑‍🧒‍🧒 JCPAO Staff by Assigned Unit")

    units_dict = {
        'Exec': 'Executive Staff',
        'GCU': 'General Crimes Unit (GCU)',
        'SVU': 'Special Victims Unit (SVU)',
        'VCU': 'Violent Crimes Unit (VCU)',
        'CSU': 'Crime Strategies Unit (CSU)',
        'COMBAT': 'COMBAT',
        'Drug': 'Drug Court',
        'FSD': 'Family Support Division',
        'WARRANT': 'Warrant Desk'
    }

    # ----- Count and Percentage -----

    # Get length of employee_info_view (active JCPAO employees)
    total_rows = len(df)

    # df = df.dropna(subset=['Assigned Unit'])
    exploded = df.explode('Assigned Unit').reset_index(drop=True) # Flatten enum[]
    unit_total_counts = exploded['Assigned Unit'].value_counts().reset_index()
    unit_total_counts.columns = ['Assigned Unit', 'Count']
    unit_total_counts['Assigned Unit'] = unit_total_counts['Assigned Unit'].replace(units_dict)
    unit_total_counts['Percent'] = (unit_total_counts['Count'] / total_rows * 100).round(2)

    # ----- Plotly Bar Chart -----
    fig = px.bar(
        unit_total_counts,
        x="Assigned Unit",
        y="Count",
        color="Assigned Unit", # color_discrete_sequence=px.colors.qualitative.Set2
        text="Count",
        title="JCPAO Staff by Assigned Unit",
        # color_discrete_map=colors_dict,
        custom_data=["Percent"],
        orientation="v",
        height=600
    )

    fig.update_traces(
        textposition="outside",
        # customdata=race_total_counts[["Percent"]].values,
        hovertemplate="%{x}<br>Count: %{y}<br>Percent: %{customdata[0]:.2f}%"+"<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,
        barmode="overlay",
        xaxis_title="Assigned Unit",
        yaxis_title="Number of Employees",
        yaxis=dict(tickmode="auto"), # linear
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Job Position Display
    unit_display = st.columns(2, vertical_alignment="center") 

    with unit_display[0]:
        # ----- Display Chart -----
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Bar chart depicting breakdown of JCPAO staff by assigned unit(s). Staff who are assigned to more than one unit are counted in each unit (n={len(exploded)}).")
    
    with unit_display[1]:
        # st.dataframe 
        st.write("**Table View**")
        st.dataframe(
            unit_total_counts, 
            column_config={
                "Percent": st.column_config.NumberColumn(
                    "Percent",
                    format="%.2f%%",
                    help=r"% of JCPAO staff assigned to unit"
                )
            },
            hide_index=True
        )

# Define office_metrics(df)
def office_metrics(df: pd.DataFrame = staff_view):
    """Display office location breakdown of JCPAO staff"""

    locations_dict = {
        'Dt-11': 'Downtown (11th)',
        'Dt-10': 'Downtown (10th)',
        'Dt-9': 'Downtown (9th)',
        'Dt-7M': 'Downtown (7M)',
        'Indy': 'Independence',
        'FSD': 'Family Support Division'
    }

    st.subheader("🏢 JCPAO Staff by Office Location")

    # ----- Count and Percentage -----
    # df = df.dropna(subset=['Office Location'])
    office_counts = df["Office Location"].value_counts().reset_index()
    office_counts.columns = ["Office Location", "Count"]
    office_counts["Percent"] = (office_counts["Count"] / office_counts["Count"].sum() * 100).round(2)
    office_counts["Office Location"] = office_counts["Office Location"].replace(locations_dict)

    # ----- Plotly Bar Chart -----
    fig = px.bar(
        office_counts,
        x="Office Location",
        y="Count",
        color="Office Location",
        text="Count",
        title="JCPAO Staff by Office Location",
        # color_discrete_sequence=px.colors.qualitative.Set2,
        custom_data=["Percent"],
        orientation="v",
        height=600
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="%{x}<br>Count: %{y}<br>Percent: %{customdata[0]:.2f}%"+"<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,
        barmode="overlay",
        xaxis_title="Office Location",
        yaxis_title="Number of Employees",
        yaxis=dict(tickmode="auto"), # linear
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Office Display
    office_display = st.columns(2, vertical_alignment="center") 

    with office_display[0]:
        
        # ----- Display Chart -----
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Bar chart depicting breakdown of JCPAO staff by office location (n={len(df)}).")

    with office_display[1]:

        # st.dataframe 
        st.write("**Table View**")
        st.dataframe(
            office_counts, 
            column_config={
                "Percent": st.column_config.NumberColumn(
                    "Percent",
                    format="%.2f%%",
                    help=r"% of JCPAO staff at office location"
                )
            },
            hide_index=True
        )

# Define service_years_metrics(df)
def service_years_metrics(df: pd.DataFrame = staff_view): # user_email: str, 
    """Display service duration statistics of JCPAO staff"""

    # ----- Filter Data -----
    df["Service (years)"] = (df["Service (days)"] / 365).round(2)  # Convert days to years

    min_years = int(df["Service (years)"].min())
    max_years = int(df["Service (years)"].max())

    filtered = df[df["Service (years)"].between(min_years, max_years)]["Service (years)"].dropna().reset_index(drop=True).copy()
    # user_data = df[df["Work Email Address"] == user_email].reset_index(drop=True).copy()
    # service_years = user_data.loc[0, "Service (years)"]
    # service_percentile = user_data.loc[0, "Service (percentile)"]

    # ----- Stats -----
    mean_val = int(round(filtered.mean()))
    median_val = int(round(filtered.median()))

    st.write(f":green[**Average:** {mean_val:.0f} years]")
    st.write(f":red[**Median (50th percentile):** {median_val:.0f} years]")

    # ----- Interactive Plotly Histogram -----
    fig = px.histogram(
        filtered,
        nbins=50, # bins
        labels={"value": "Service total (in years)"},
        title="JCPAO Staff by Length of Service (in years)",
        opacity=0.75,
        marginal="box"
    )

    # Add vertical line for mean
    fig.add_vline(
        x=mean_val,
        line_dash="dot",
        line_color="green",
        # annotation_text=f"  Average: {mean_val:.0f} yrs",
        # annotation_position="top right",
        # annotation_font=dict(color="green")
    )

    # Add vertical line for median
    fig.add_vline(
        x=median_val,
        line_dash="dot",
        line_color="red",
        # annotation_text=f"  Median: {median_val:.0f} yrs",
        # annotation_position="top right",
        # annotation_font=dict(color="red")
    )

    # Customize hover/tooltip text
    fig.update_traces(
        hovertemplate="Range: %{x} yrs<br>Count: %{y}<extra></extra>"
    )

    # Remove legend
    fig.update_layout(
        showlegend=False,
        xaxis_title="Total Years Employed",
        yaxis_title="Number of Employees",
        bargap=0.05
    )

    st.plotly_chart(fig, width="stretch")
    # st.caption(f"*For context, you have been with the JCPAO for {service_years} years (i.e., ***:blue[{ordinal(service_percentile)} percentile]*** among all active JCPAO employees)!*")


# Define service_days_metrics(df)
def service_days_metrics(df: pd.DataFrame = staff_view): # user_email: str, 
    """Display service duration statistics of JCPAO staff"""

    # ----- Sidebar Filters -----
    min_days = int(df["Service (days)"].min())
    max_days = int(df["Service (days)"].max())

    # with st.sidebar:

    #     day_range = st.slider(
    #         "Filter by total days employed",
    #         min_value=min_days,
    #         max_value=max_days,
    #         value=(min_days, max_days),
    #         step=10
    #     )

    #     bins = st.slider("Number of histogram bins", min_value=5, max_value=100, value=30, step=5)

    # ----- Filter Data -----
        # df[df["Service (days)"].between(day_range[0], day_range[1])]["Service (days)"].dropna().reset_index(drop=True).copy()
    filtered = df[df["Service (days)"].between(min_days, max_days)]["Service (days)"].dropna().reset_index(drop=True).copy()
    # user_data = df[df["Work Email Address"] == user_email].reset_index(drop=True).copy()
    # service_days = user_data.loc[0, "Service (days)"]
    # service_percentile = user_data.loc[0, "Service (percentile)"]

    # ----- Stats -----
    mean_val = int(round(filtered.mean()))
    median_val = int(round(filtered.median()))

    # st.subheader("📊 Descriptive Stats")
    st.write(f":green[**Average:** {mean_val:.0f} days]")
    st.write(f":red[**Median (50th percentile):** {median_val:.0f} days]")
    # st.write(f"**Count:** {len(filtered)} employees")

    # ----- Interactive Plotly Histogram -----
    fig = px.histogram(
        filtered,
        nbins=50, # bins
        labels={"value": "Service total (in days)"},
        title="JCPAO Staff by Length of Service (in days)",
        opacity=0.75,
        marginal="box"
    )

    # Add vertical line for mean
    fig.add_vline(
        x=mean_val,
        line_dash="dot",
        line_color="green",
        # annotation_text=f"  Average: {mean_val:.0f} days",
        # annotation_position="top right",
        # annotation_font=dict(color="green")
    )

    # Add vertical line for median
    fig.add_vline(
        x=median_val,
        line_dash="dot",
        line_color="red",
        # annotation_text=f"  Median: {median_val:.0f} days",
        # annotation_position="top right",
        # annotation_font=dict(color="red")
    )

    # Customize hover/tooltip text
    fig.update_traces(
        hovertemplate="Range: %{x} days<br>Count: %{y}<extra></extra>"
    )

    # Remove legend
    fig.update_layout(
        showlegend=False,
        xaxis_title="Total Days Employed",
        yaxis_title="Number of Employees",
        bargap=0.05
    )

    st.plotly_chart(fig, width="stretch")
    # st.caption(f"*For context, you have been with the JCPAO for {service_days} days (i.e., ***:blue[{ordinal(service_percentile)} percentile]*** among all active JCPAO employees)!*")


# Define race_total_metrics(df)
def race_total_metrics(df: pd.DataFrame = staff_view):
    """Display racial/ethnic breakdown (how many identify with 'x' race) of JCPAO staff"""

    race_dict = {
        "W": "White",
        "B": "Black / African American",
        "A": "Asian",
        "H": "Hispanic / Latino",
        "AIAN": "American Indian / Alaska Native",
        "NHPI": "Native Hawaiian / Pacific Islander",
        "O": "Other"
    }

    colors_dict = {
        "White": "#66c2a5",
        "Black / African American": "#fc8d62",
        "Asian": "#8da0cb",
        "Hispanic / Latino": "#e78ac3",
        "American Indian / Alaska Native": "#a6d854",
        "Native Hawaiian / Pacific Islander": "#ffd92f",
        "Other": "#e5c494"
    }

    # ----- Count and Percentage -----

    # Get length of employee_info_view (active JCPAO employees)
    total_rows = len(df)

    # df = df.dropna(subset=['Race'])
    exploded = df.explode('Race').reset_index(drop=True) # Flatten enum[]
    race_total_counts = exploded['Race'].value_counts().reset_index()
    race_total_counts.columns = ['Race/Ethnicity', 'Count']
    race_total_counts['Race/Ethnicity'] = race_total_counts['Race/Ethnicity'].replace(race_dict)
    race_total_counts['Percent'] = (race_total_counts['Count'] / total_rows * 100).round(2)

    # ----- Plotly Bar Chart -----
    fig = px.bar(
        race_total_counts,
        x="Race/Ethnicity",
        y="Count",
        color="Race/Ethnicity", # color_discrete_sequence=px.colors.qualitative.Set2
        text="Count",
        title="JCPAO Staff by Total Race/Ethnicity",
        color_discrete_map=colors_dict,
        custom_data=["Percent"],
        orientation="v",
        height=600
    )

    fig.update_traces(
        textposition="outside",
        # customdata=race_total_counts[["Percent"]].values,
        hovertemplate="%{x}<br>Count: %{y}<br>Percent: %{customdata[0]:.2f}%"+"<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,
        barmode="overlay",
        xaxis_title="Race/Ethnicity",
        yaxis_title="Number of Employees",
        yaxis=dict(tickmode="auto"), # linear
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # ----- Display Chart -----
    st.plotly_chart(fig, width="stretch")
    st.caption(f"Bar chart depicting racial/ethnic breakdown of JCPAO staff. Staff who identify with more than one race/ethnicity are counted in each category they identify with (n={len(exploded)}).")

    # st.dataframe 
    st.write("**Table View**")
    st.dataframe(
        race_total_counts, 
        column_config={
            "Percent": st.column_config.NumberColumn(
                "Percent",
                format="%.2f%%",
                help=r"% of JCPAO staff who identify with racial/ethnic category"
            )
        },
        hide_index=True
    )


# Define race_unique_metrics(df)
def race_unique_metrics(df: pd.DataFrame = staff_view):
    """Display racial/ethnic breakdown (incl. "Multiple" value) of JCPAO staff"""

    race_dict = {
        "W": "White",
        "B": "Black / African American",
        "A": "Asian",
        "H": "Hispanic / Latino",
        "AIAN": "American Indian / Alaska Native",
        "NHPI": "Native Hawaiian / Pacific Islander",
        "O": "Other",
        "Multiple": "Multiple"
    }

    colors_dict = {
        "White": "#66c2a5",
        "Black / African American": "#fc8d62",
        "Asian": "#8da0cb",
        "Hispanic / Latino": "#e78ac3",
        "American Indian / Alaska Native": "#a6d854",
        "Native Hawaiian / Pacific Islander": "#ffd92f",
        "Other": "#e5c494",
        "Multiple": "#b3b3b3"
    }

    # ----- Count and Percentage -----
    df["race_unique"] = ["Unknown" if len(value) == 0 else "Multiple" if len(value) > 1 else value[0] for value in df["Race"]]
    race_unique_counts = df["race_unique"].value_counts().reset_index()
    race_unique_counts.columns = ["Race/Ethnicity", "Count"]
    race_unique_counts["Race/Ethnicity"] = race_unique_counts["Race/Ethnicity"].replace(race_dict)
    race_unique_counts["Percent"] = (race_unique_counts["Count"] / race_unique_counts["Count"].sum() * 100).round(2)

    # ----- Plotly Pie Chart -----
    fig = px.pie(
        race_unique_counts,
        names="Race/Ethnicity",
        values="Count",
        title="JCPAO Staff by Unique Race/Ethnicity (incl. 'Multiple')",
        color="Race/Ethnicity",
        color_discrete_map=colors_dict,  # Use custom colors
        height=600,
        # color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.3  # if you want a donut-style chart
    )

    # Show percentage & raw count in hover
    fig.update_traces(
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="%{label}<br>Count: %{value}<br>Percent: %{percent}<extra></extra>"
    )

    fig.update_layout(
        showlegend=False
    )

    # ----- Display Chart -----
    st.plotly_chart(fig, width="stretch")
    st.caption(f"Pie chart depicting racial/ethnic breakdown of JCPAO staff. Staff who identify with more than one race/ethnicity are categorized as 'multiple' (n={race_unique_counts['Count'].sum()}). Each staff member is counted only once.")

    # st.dataframe 
    st.write("**Table View**")
    st.dataframe(
        race_unique_counts, 
        column_config={
            "Percent": st.column_config.NumberColumn(
                "Percent",
                format="%.2f%%",
                help=r"% of unique JCPAO staff"
            )
        },
        hide_index=True
    )


# Define gender_metrics(df)
def gender_metrics(df: pd.DataFrame = staff_view):
    """Display gender breakdown of JCPAO staff"""

    # ----- Title -----
    st.subheader("👥 JCPAO Staff by Gender")

    # ----- Count and Percentage -----
    gender_counts = df["Sex"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    gender_counts["Gender"] = gender_counts["Gender"].replace({
        "M": "Male",
        "F": "Female",
        "O": "Other / Prefer not to say"
    })
    gender_counts["Percent"] = (gender_counts["Count"] / gender_counts["Count"].sum() * 100).round(2)

    # ----- Plotly Pie Chart -----
    fig = px.pie(
        gender_counts,
        names="Gender",
        values="Count",
        title="JCPAO Staff by Gender",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.3  # if you want a donut-style chart
    )

    # Show percentage & raw count in hover
    fig.update_traces(
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="%{label}<br>Count: %{value}<br>Percent: %{percent}<extra></extra>"
    )

    # Gender Display
    gender_display = st.columns(2, vertical_alignment="center") 

    with gender_display[0]:
        
        # ----- Display Chart -----
        st.plotly_chart(fig, width="stretch")
        st.caption(f"Pie chart depicting gender breakdown of JCPAO staff (n={len(df)}).")

    with gender_display[1]:

        # st.dataframe 
        st.write("**Table View**")
        st.dataframe(
            gender_counts, 
            column_config={
                "Percent": st.column_config.NumberColumn(
                    "Percent",
                    format="%.2f%%",
                    help=r"% of JCPAO staff"
                )
            },
            hide_index=True
        )