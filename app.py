
import streamlit as st
import preprocess
import helper
from urlextract import URLExtract
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Add a welcome message
st.markdown("<h1 style='text-align: center; color: green;'>Welcome to WhatsApp Chat Analyzer</h1>", unsafe_allow_html=True)

extractor = URLExtract()
st.sidebar.title("Upload your WhatsApp Chat")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # Decode file with error handling for different encodings
    try:
        data = bytes_data.decode('utf-8')
    except UnicodeDecodeError:
        data = bytes_data.decode('latin-1')
    
    # Preprocess the chat data
    df = preprocess.preprocessor(data)

    # Add the app name at the top
    st.title("WhatsApp Chat Analyzer")
    
    # Fetch unique users
    user_list = df['user'].unique().tolist()
    # Only try to remove 'Group_notification' if it exists in the list
    if 'Group_notification' in user_list:
        user_list.remove('Group_notification')
    
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    # Show analysis when button is clicked
    if st.sidebar.button("Show Analysis"):
        num_msgs, words, num_media, links = helper.fetch_stats(selected_user, df)
        st.markdown("<h1 style='text-align: center; color: red; font-size: 52px;'>Top Statistics</h1>", unsafe_allow_html=True)

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

        # Monthly timeline
        st.markdown("<h1 style='color: green;'>Monthly Timeline</h1>", unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user, df)
        if not timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color="orange")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            st.pyplot(fig)
        else:
            st.warning("No monthly data available.")

        # Daily timeline
        st.markdown("<h1 style='color: green;'>Daily Timeline</h1>", unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user, df)
        if not daily_timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color="orange")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
            st.pyplot(fig)
        else:
            st.warning("No daily data available.")
        
        # Activity Map
        st.markdown("<h1 style='color: green;'>Activity Map</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<h1 style="color: blue; font-size: 22px;">Busy Week</h1>', unsafe_allow_html=True)
            busy_day = helper.busy_day(selected_user, df)
            if not busy_day.empty:
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                st.pyplot(fig)
            else:
                st.warning("No busy day data available.")

        with col2:
            st.markdown('<h1 style="color: blue; font-size: 22px;">Busy Month</h1>', unsafe_allow_html=True)
            busy_month = helper.busy_month(selected_user, df)
            if not busy_month.empty:
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)
                ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
                st.pyplot(fig)
            else:
                st.warning("No busy month data available.")

        # Weekly Activity Heatmap
        st.markdown("<h1 style='color: green;'>Weekly Activity Heatmap</h1>", unsafe_allow_html=True)
        activity_heatmap = helper.activity_heat(selected_user, df)

        # Check if activity_heatmap is empty before plotting
        if not activity_heatmap.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(activity_heatmap)
            with col2:
                fig, ax = plt.subplots()
                sns.heatmap(activity_heatmap, ax=ax)
                st.pyplot(fig)
        else:
            st.warning("No activity data available to display heatmap.")

        # Busiest users in the group
        if selected_user == 'Overall':
            st.markdown('<h1 style="color: green; font-size: 32px;">Most Busiest Users</h1>', unsafe_allow_html=True)
            x, new_df = helper.most_busy(df)
            if not x.empty:
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values, color='red')
                    ax.set_xticks(x.index)
                    ax.set_xticklabels(x.index, rotation=45)
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)
            else:
                st.warning("No data available for busiest users.")

        # Word Cloud
        st.markdown('<h1 style="color: green;">Word Cloud</h1>', unsafe_allow_html=True)
        dc_wc = helper.create_wc(selected_user, df)
        if dc_wc is not None:
            fig, ax = plt.subplots()
            plt.imshow(dc_wc)
            plt.axis("off")
            st.pyplot(fig)
        else:
            st.warning("No word cloud data available.")

        # Common Words
        st.markdown('<h1 style="color: green;">Common Words</h1>', unsafe_allow_html=True)
        most_common_df = helper.common_words(selected_user, df)
        if not most_common_df.empty:
            fig, ax = plt.subplots()
            ax.bar(most_common_df[0], most_common_df[1], color='yellow')
            ax.set_xticklabels(most_common_df[0], rotation='vertical')
            st.pyplot(fig)
        else:
            st.warning("No common words data available.")

        # Emoji Analysis
        st.markdown('<h1 style="color: green;">Emojis</h1>', unsafe_allow_html=True)
        emojis = helper.emoji_helper(selected_user, df)
        if not emojis.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emojis)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emojis[1].head(7), labels=emojis[0].head(7), autopct="%0.2f")
                st.pyplot(fig)
        else:
            st.warning("No emoji data available.")


