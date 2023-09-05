

from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
import nltk
from nltk.corpus import stopwords
import emoji
import re
from collections import Counter
import seaborn as sns
nltk.download('stopwords')


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        # 1. fetch number of messages
    num_msgs = df.shape[0]
    # 2. number of Words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Media share in group
    num_media = df[df['message'] == '<Media omitted>'].shape[0]

    # Links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_msgs, len(words), num_media, len(links)

def most_busy(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df['user'].shape[0]) * 100, 4).reset_index().rename(
        columns={'count': 'percent', 'user': 'name'})
    return x, new_df

# WordCloud
def create_wc(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'Group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    stop_words = set(stopwords.words('english'))
    urdu_stop_words = {'k', 'ap', 'ok', 'ma', 'ko', 'ha', 'ki', 'kr', 'ho', 'hi', 'bhi', 'b', 'na', 'ka',
                       'ni'}  # Add more Urdu stopwords as needed
    all_stop_words = stop_words.union(urdu_stop_words)
    temp['message'] = temp['message'].apply(
        lambda message: ' '.join([word for word in message.split() if word.lower() not in all_stop_words]))
    wc = WordCloud(width=500, height=500,min_font_size=10,background_color='white')
    dc_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return dc_wc


# Common Words

def common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    stop_words = set(stopwords.words('english'))
    urdu_stop_words = {'k', 'ap', 'ok', 'ma', 'ko', 'ha', 'ki', 'kr', 'ho', 'hi', 'bhi', 'b', 'na', 'ka',
                       'ni'}  # Add more Urdu stopwords as needed
    all_stop_words = stop_words.union(urdu_stop_words)
    temp['message'] = temp['message'].apply(
        lambda message: ' '.join([word for word in message.split() if word.lower() not in all_stop_words]))
    words = []
    for message in temp['message']:
        words.extend(message.split())
    from collections import Counter
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# ------------------EMOJIS---------------------

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    import re

    # Define a regular expression pattern to match emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # Emoticons
                               u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols and Pictographs
                               u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
                               u"\U0001F700-\U0001F77F"  # Alchemical Symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U0001F004-\U0001F0CF"  # Extended B&W Emojis
                               u"\U0001F004-\U0001F0CF"  # Extended B&W Emojis
                               u"\U0001F004-\U0001F0CF"  # Extended B&W Emojis
                               u"\U0001F004-\U0001F0CF"  # Extended B&W Emojis
                               u"\U0001F004-\U0001F0CF"  # Extended B&W Emojis
                               u"\U0001F004-\U0001F0CF"  # Extended B&W Emojis
                               u"\U0001F004-\U0001F0CF"  # Extended B&W Emojis
                               u"\U0001F004-\U0001F0CF"  # Extended B&W Emojis
                               # Add more emoji code ranges as needed
                               "]+", flags=re.UNICODE)

    emojis = []
    for message in df['message']:
        emojis.extend(emoji_pattern.findall(message))

    emojis = pd.DataFrame(Counter(emojis).most_common(20))

    return emojis


# ------------------Monthly TimeLine-------------------
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'num_month', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

#  ---------------Daily TimeLine--------------
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    
    return daily_timeline

# ----------------- BUsy Day -----------
def busy_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()

# ----------------- Busy_month -----------
def busy_month(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

# ------------- Activity heatmap-------------
def activity_heat(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity_heatmap = df.pivot_table(index='day_name', columns='period', values= 'message', aggfunc='count').fillna(0)
    # activity_heatmap = sns.heatmap(df.pivot_table(index='day_name', columns='period', values= 'message', aggfunc='count').fillna(0))    
    return activity_heatmap












# st.sidebar.title("Whatsapp Chat Analyzer")
# uploaded_file = st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#     bytes_data = uploaded_file.getvalue()
#     data = bytes_data.decode('utf-8')
#     df = preprocess.preprocessor(data)

#     # st.dataframe(df)

#     # fetch unique users
#     user_list = df['user'].unique().tolist()
#     user_list.remove('Group_notification')
#     user_list.sort()
#     user_list.insert(0, "Overall")

#     selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
#     if st.sidebar.button("Show Analysis"):
#         num_msgs, words, num_media, links = helper.fetch_stats(selected_user, df)
#         st.markdown("<h1 style='text-align: center; color: red; font-size: 52px;'>Top Statistics</h1>", unsafe_allow_html=True)

#         col1, col2, col3, col4 = st.columns(4)

#         with col1:
#             st.header("Total Messages")
#             st.title(num_msgs)
#         with col2:
#             st.header("Total Words")
#             st.title(words)
#         with col3:
#             st.header("Total media")
#             st.title(num_media)
#         with col4:
#             st.header("Total links")
#             st.title(links)


#         #---------Create monthly timeline--------
#         st.markdown("<h1 style='color: green;'>Monthly TimeLine</h1>", unsafe_allow_html=True)

#         timeline = helper.monthly_timeline(selected_user, df)
#         fig, ax = plt.subplots()
        
#         ax.plot(timeline['time'], timeline['message'], color="orange")
#         ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
#         plt.show()
#         st.pyplot(fig)

#         #---------Create daily timeline--------
#         st.markdown("<h1 style='color: green;'>Daily TimeLine</h1>", unsafe_allow_html=True)

#         daily_timeline = helper.daily_timeline(selected_user, df)
#         fig, ax = plt.subplots()
        
#         ax.plot(daily_timeline['only_date'], daily_timeline['message'], color="orange")
#         ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
#         plt.show()
#         st.pyplot(fig)
        
        
#         # ----------------  --Activity Map------------
#         st.markdown("<h1 style='color: green;'>Activity Map</h1>", unsafe_allow_html=True)
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown('<h1 style="color: blue; font-size: 22px;">Busy Week</h1>', unsafe_allow_html=True)
#             busy_day = helper.busy_day(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_day.index, busy_day.values)
#             ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
#             st.pyplot(fig)

#         with col2:
#             st.markdown('<h1 style="color: blue; font-size: 22px;">Busy Month</h1>', unsafe_allow_html=True)
#             busy_month = helper.busy_month(selected_user, df)
#             fig, ax = plt.subplots()
#             ax.bar(busy_month.index, busy_month.values)
#             ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
#             st.pyplot(fig)        
#         # ----------pivot/heatmap---------------
#         st.markdown("<h1 style='color: green;'>Weekly Activity Heatmap</h1>", unsafe_allow_html=True)
        
#         col1, col2 = st.columns(2)
#         with col1:
#             activity_heatmap = helper.activity_heat(selected_user, df)
#             st.dataframe(activity_heatmap)
#         with col2:
#             activity_heatmap = helper.activity_heat(selected_user, df)
#             fig, ax = plt.subplots()
#             ax = sns.heatmap(activity_heatmap)
#             st.pyplot(fig)
            
        
            
       
        
#         # find the busiest users in the group
#         if selected_user == 'Overall':
#             # st.title(':blue[Most Busiest Users]')
#             st.markdown('<h1 style="color: green; font_size=32px">Most Busiest Users</h1>',unsafe_allow_html=True)
#             x, new_df = helper.most_busy(df)
#             fig, ax = plt.subplots()


#             col1, col2 = st.columns(2)

#             with col1:
#                 ax.bar(x.index, x.values, color='red')
#                 ax.set_xticks(x.index)
#                 ax.set_xticklabels(x.index, rotation=45)
#                 st.pyplot(fig)

#             with col2:
#                 st.dataframe(new_df)

# #-------------- WORD CLOUD--------------
#         st.markdown('<h1 style="color: green;">Word Cloud</h1>', unsafe_allow_html=True)

#         dc_wc = helper.create_wc(selected_user, df)
#         fig, ax = plt.subplots()
#         plt.imshow(dc_wc)
#         st.pyplot(fig)
# # -----------------Common Words ------------------
#         st.markdown('<h1 style="color: green;">Common Words</h1>', unsafe_allow_html=True)

#         most_common_df = helper.common_words(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.bar(most_common_df[0], most_common_df[1], color='yellow')
#         ax.set_xticklabels(most_common_df[0], rotation='vertical')
#         st.pyplot(fig)

# # ---------------Emoji Analysis -----------------
#         st.markdown('<h1 style="color: green;">Emojis</h1>', unsafe_allow_html=True)
#         emojis = helper.emoji_helper(selected_user, df)

#         col1, col2 = st.columns(2)
#         with col1:
#             st.dataframe(emojis)
#         with col2:
#             fig, ax = plt.subplots()
#             plt.figure(figsize=(10, 10))
#             # ax.pie(emojis[1], labels=emojis[0])
#             ax.pie(emojis[1].head(7), labels=emojis[0].head(7),autopct="%0.2f")
#             st.pyplot(fig)

