import streamlit as st
import preprocess
import helper
from urlextract import URLExtract
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Function to handle chat file decoding
def decode_file(bytes_data):
    try:
        return bytes_data.decode('utf-8')
    except UnicodeDecodeError:
        return bytes_data.decode('latin-1')  # Fallback to a more lenient encoding

# Function to show the statistics in columns
def show_statistics(num_msgs, words, num_media, links):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header("Total Messages")
        st.title(num_msgs)
    with col2:
        st.header("Total Words")
        st.title(words)
    with col3:
        st.header("Total Media")
        st.title(num_media)
    with col4:
        st.header("Total Links")
        st.title(links)

# Function to plot a timeline
def plot_timeline(title, data, x_label, y_label, color="orange"):
    st.markdown(f"<h1 style='color: green;'>{title}</h1>", unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.plot(data[x_label], data[y_label], color=color)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

# Welcome message
st.markdown("<h1 style='text-align: center; color: green;'>Welcome to WhatsApp Chat Analyzer</h1>", unsafe_allow_html=True)

# Sidebar - File uploader
extractor = URLExtract()
st.sidebar.title("Upload your WhatsApp Chat")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = decode_file(bytes_data)
    
    # Preprocess the chat data
    df = preprocess.preprocessor(data)

    # App title
    st.title("WhatsApp Chat Analyzer")

    # Fetch unique users and add an option for overall analysis
    user_list = df['user'].unique().tolist()
    if 'Group_notification' in user_list:
        user_list.remove('Group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # Sidebar - User selection
    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    # Sidebar - Analysis button
    if st.sidebar.button("Show Analysis"):
        try:
            # Fetch statistics
            num_msgs, words, num_media, links = helper.fetch_stats(selected_user, df)
            st.markdown("<h1 style='text-align: center; color: red; font-size: 52px;'>Top Statistics</h1>", unsafe_allow_html=True)
            show_statistics(num_msgs, words, num_media, links)

            # Monthly timeline
            timeline = helper.monthly_timeline(selected_user, df)
            plot_timeline("Monthly Timeline", timeline, 'time', 'message')

            # Daily timeline
            daily_timeline = helper.daily_timeline(selected_user, df)
            plot_timeline("Daily Timeline", daily_timeline, 'only_date', 'message')

            # Activity Map
            st.markdown("<h1 style='color: green;'>Activity Map</h1>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<h1 style="color: blue; font-size: 22px;">Busy Week</h1>', unsafe_allow_html=True)
                busy_day = helper.busy_day(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                st.pyplot(fig)

            with col2:
                st.markdown('<h1 style="color: blue; font-size: 22px;">Busy Month</h1>', unsafe_allow_html=True)
                busy_month = helper.busy_month(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                st.pyplot(fig)

            # Weekly Activity Heatmap
            st.markdown("<h1 style='color: green;'>Weekly Activity Heatmap</h1>", unsafe_allow_html=True)
            activity_heatmap = helper.activity_heat(selected_user, df)
            fig, ax = plt.subplots()
            sns.heatmap(activity_heatmap, ax=ax)
            st.pyplot(fig)

            # Most busy users
            if selected_user == 'Overall':
                st.markdown('<h1 style="color: green; font-size: 32px;">Most Busiest Users</h1>', unsafe_allow_html=True)
                x, new_df = helper.most_busy(df)
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values, color='red')
                    ax.set_xticks(x.index)
                    ax.set_xticklabels(x.index, rotation=45)
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            # Word Cloud
            st.markdown('<h1 style="color: green;">Word Cloud</h1>', unsafe_allow_html=True)
            dc_wc = helper.create_wc(selected_user, df)
            fig, ax = plt.subplots()
            plt.imshow(dc_wc)
            plt.axis('off')  # Hide axis
            st.pyplot(fig)

            # Common Words
            st.markdown('<h1 style="color: green;">Common Words</h1>', unsafe_allow_html=True)
            most_common_df = helper.common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(most_common_df[0], most_common_df[1], color='yellow')
            ax.set_xticklabels(most_common_df[0], rotation='vertical')
            st.pyplot(fig)

            # Emoji Analysis
            st.markdown('<h1 style="color: green;">Emojis</h1>', unsafe_allow_html=True)
            emojis = helper.emoji_helper(selected_user, df)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emojis)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emojis[1].head(7), labels=emojis[0].head(7), autopct="%0.2f")
                st.pyplot(fig)

        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")

# Sidebar - Contact Us section
st.sidebar.title("Contact Us")
st.sidebar.write("Have questions or feedback? Feel free to reach out.")
st.sidebar.text_input("Your Name", "")
st.sidebar.text_area("Message", "")
if st.sidebar.button("Send"):
    st.sidebar.success("Message sent successfully!")
