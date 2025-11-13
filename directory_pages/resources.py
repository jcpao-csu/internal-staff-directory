import streamlit as st
from pathlib import Path


# --- Initialize links ---

# Online links 
jcpao_home = r"https://www.jacksoncountyprosecutor.com"
karpel_login = r"https://mogov.hostedbykarpel.com/mojackson/app/#/login"
case_net = r"https://www.courts.mo.gov/cnet/welcome.do"
mshp_manual = r"https://www.mshp.dps.missouri.gov/CJ08Client/Home/ChargeCode"
mo_statutes = r"https://revisor.mo.gov/main/Home.aspx"

# Office help
it_helpdesk = r"http://itservicecenter.jacksongov.org/helpdesk"
whitelist = r"https://jcgis.jacksongov.org/it/whitelist.html"
workday = r"https://wd5.myworkday.com/wday/authgwy/jacksongov/login.htmld?returnTo=%2fjacksongov%2fd%2fhome.htmld%3freloadToken%3dcd1ecc783d150ffa2cd0a828900ca9cb2570101ba04c0f9ff9d446577767b1d4"
jaco_link = r"https://jacksonmo.sharepoint.com/sites/JACOLink"
jaco_associates_portal = r"https://jacksonmo.sharepoint.com/sites/JacksonCountyMO"
jaco_sharepoint = r"https://jacksonmo.sharepoint.com/_layouts/15/sharepoint.aspx"

# Training resources 
docket_call_trainings = r"https://www.youtube.com/playlist?list=PL2sfEiSjLlkwNKbonn6aefZvuJY9f_yYW"
search_warrant_training = r"https://youtu.be/o-00QWQ3K54"
apa_trainings= r"https://youtube.com/playlist?list=PL2sfEiSjLlkye83HbFSazeWLrjk2rIQZM&si=tOxuvxsntaLcIXZY"

# Portal troubleshooting
headshots = r"https://jacksonmo-my.sharepoint.com/:f:/g/personal/ujcho_jacksongov_org/EkQfmaAtb4xIkG8g8EDluEQB6zQdDATdw2CPYcgWcyNirw?e=LYIcnk"

# Office social media
jcpao_twitter = r"https://x.com/JACOProsecutor"
jcpao_facebook = r"https://www.facebook.com/share/1BZPYhgULm/?mibextid=wwXIfr"
jcpao_instagram = r"https://www.instagram.com/jacoprosecutor?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
jcpao_youtube = r"https://youtube.com/@jacksoncountyprosecutor?feature=shared"
jcpao_linkedin = r"https://www.linkedin.com/in/jcpao" # outdated link? (JPB) -- https://www.linkedin.com/company/jcpao/posts/?feedView=all

# CSU resources 
report_search = r"https://jcpao-search.streamlit.app/"
jcpao_dashboard = r"https://jcpao-dashboard.streamlit.app/"

# # --- Configure Streamlit page settings --- 
# jcpao_logo = Path("assets/logo/jcpao_logo_500x500.png")


# # --- JCPAO Streamlit page logo --- 
# st.logo(jcpao_logo, size="large", link=jcpao_home)


# --- Sidebar Filter functions --- 

with st.sidebar:

    st.title("Jackson County Prosecuting Attorney's Office")
    st.write("***Office Resources***")
    st.divider()
    st.write("Cick on any of the resources below to open in a new tab. If you would like to add other resources, please reach out to [Joseph Cho](mailto:ujcho@jacksongov.org).")
    st.divider()
    st.write("To securely exit portal, logout or just exit page:")

    # Logout 
    logout = st.button(
        label="Logout",
        key="logout",
        on_click=lambda: st.session_state.clear(), # Clear session state
        type="secondary",
        icon=":material/logout:"
    )


# --- Run page ---

st.markdown("<h1 style='text-align: center; color: black;'>Office Resources</h1>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2, gap="small", vertical_alignment="top", border=False, width="stretch")

with col1:

    # Online links
    st.header("Online Links", divider="blue")

    st.page_link(jcpao_home, label="Jackson County Prosecutor Home Page", icon="⚖️")
    st.page_link(karpel_login, label="Karpel (PbK) Portal", icon="🔎")
    st.page_link(case_net, label="Missouri Case Net", icon="📁")
    st.page_link(mshp_manual, label="MSHP Charge Code Manual", icon="🫆")
    st.page_link(mo_statutes, label="Missouri Revisor of Statutes", icon="📜")

    # Traning resources
    st.header("Training Resources", divider="blue")

    st.page_link(docket_call_trainings, label="2025 Docket Call Karpel Training Refreshers", icon="📚")
    st.page_link(search_warrant_training, label="Search Warrant Training (Kristiane Bryant)", icon="🚨")
    st.page_link(apa_trainings, label="October 2025 APA Training", icon="📖")

    # CSU resources
    st.header("CSU Resources", divider="blue")

    st.page_link(report_search, label="Police Report Number Search Tool", icon="🚔")
    st.page_link(jcpao_dashboard, label="JCPAO Dashboard", icon="📊")

with col2:

    # Office help
    st.header("Office Help", divider="blue")

    st.page_link(it_helpdesk, label="IT Help Desk ***:red[(must be connected to County network)]***", icon="🖥️")
    st.page_link(whitelist, label="Whitelist public websites within County network", icon="🌐")
    st.page_link(workday, label="Workday", icon="💼")
    st.page_link(jaco_link, label=":yellow-background[JACO Link (New Associate Intranet Site) ***:red[(NEW)]***]", icon="🏢")
    st.page_link(jaco_associates_portal, label="Jackson County Associates Portal ***:red[(use new JACO link above)]***", icon="🏢")
    st.page_link(jaco_sharepoint, label="Jackson County SharePoint", icon="🗃️")

    # Directory troubleshooting 
    st.header("Directory Troubleshooting", divider="blue")

    st.write("If you are experiencing any issues with the directory, please report them to [Joseph Cho](mailto:ujcho@jacksongov.org)! Thank you for your patience and understanding as we launch this online tool.")
    st.write("Likewise, to update your headshot photo, please contact [Joseph Cho](mailto:ujcho@jacksongov.org) with your desired photo. The Office will periodically hold headshot photo sessions for new employees and those interested in updating their office headshot photo. Staff can view office headshots via the link below:")
    st.page_link(headshots, label="JCPAO Staff Headshots", icon="📸")

    # Office social media
    st.header("Office Social Media", divider="blue")

    st.page_link(jcpao_twitter, label="Twitter", icon="🐦")
    st.page_link(jcpao_facebook, label="Facebook", icon="📘")
    st.page_link(jcpao_instagram, label="Instagram", icon="📸")
    st.page_link(jcpao_youtube, label="YouTube", icon="📺")
    st.page_link(jcpao_linkedin, label="LinkedIn", icon="🔗")

