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
    data = bytes_data.decode('utf-8')
    df = preprocess.preprocessor(data)

    # Add the app name at the top
    st.title("WhatsApp Chat Analyzer")
    
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('Group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
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
            st.header("Total media")
            st.title(num_media)
        with col4:
            st.header("Total links")
            st.title(links)


        #---------Create monthly timeline--------
        st.markdown("<h1 style='color: green;'>Monthly TimeLine</h1>", unsafe_allow_html=True)

        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        
        ax.plot(timeline['time'], timeline['message'], color="orange")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        plt.show()
        st.pyplot(fig)

        #---------Create daily timeline--------
        st.markdown("<h1 style='color: green;'>Daily TimeLine</h1>", unsafe_allow_html=True)

        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color="orange")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        plt.show()
        st.pyplot(fig)
        
        
        # ----------------  --Activity Map------------
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
        # ----------pivot/heatmap---------------
        st.markdown("<h1 style='color: green;'>Weekly Activity Heatmap</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            activity_heatmap = helper.activity_heat(selected_user, df)
            st.dataframe(activity_heatmap)
        with col2:
            activity_heatmap = helper.activity_heat(selected_user, df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(activity_heatmap)
            st.pyplot(fig)
            
        
            
       
        
        # find the busiest users in the group
        if selected_user == 'Overall':
            # st.title(':blue[Most Busiest Users]')
            st.markdown('<h1 style="color: green; font_size=32px">Most Busiest Users</h1>',unsafe_allow_html=True)
            x, new_df = helper.most_busy(df)
            fig, ax = plt.subplots()


            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                ax.set_xticks(x.index)
                ax.set_xticklabels(x.index, rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

#-------------- WORD CLOUD--------------
        st.markdown('<h1 style="color: green;">Word Cloud</h1>', unsafe_allow_html=True)

        dc_wc = helper.create_wc(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(dc_wc)
        st.pyplot(fig)
# -----------------Common Words ------------------
        st.markdown('<h1 style="color: green;">Common Words</h1>', unsafe_allow_html=True)

        most_common_df = helper.common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0], most_common_df[1], color='yellow')
        ax.set_xticklabels(most_common_df[0], rotation='vertical')
        st.pyplot(fig)

# ---------------Emoji Analysis -----------------
        st.markdown('<h1 style="color: green;">Emojis</h1>', unsafe_allow_html=True)
        emojis = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emojis)
        with col2:
            fig, ax = plt.subplots()
            plt.figure(figsize=(10, 10))
            # ax.pie(emojis[1], labels=emojis[0])
            ax.pie(emojis[1].head(7), labels=emojis[0].head(7),autopct="%0.2f")
            st.pyplot(fig)



    
    st.sidebar.title("Contact Us")
    st.sidebar.write("Have questions or feedback? Feel free to reach out.")
    st.sidebar.text_input("Your Name", "")
    st.sidebar.text_area("Message", "")
    if st.sidebar.button("Send"):
        st.sidebar.success("Message sent successfully!")

