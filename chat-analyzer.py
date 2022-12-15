import streamlit as st
import function as f
import matplotlib.pyplot as plt


st.sidebar.title("Whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a chat txt file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = f.data_preprocessing(data)
    # st.dataframe(df)

    user_list = df['sender'].unique().tolist()
    user_list.insert(0, "All")
    selected_user = st.sidebar.selectbox("Select user", user_list)

    ## Adding the button
    if st.sidebar.button("Analyze"):
        st.title("Analysis with repect to {}".format(selected_user))

        if selected_user != "All":
            df = df[df['sender'] == selected_user]
        
        ## Some variables for later use
        words = f.total_words(df)

        ## Defined four columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total chats")
            st.title(df.shape[0])
        
        with col2:
            st.header("Total words")
            st.title(len(words))
        
        with col3:
            st.header("Total media")
            st.title(str(f.total_media(df)))
        
        with col4:
            st.header("Total Links")
            st.title(str(f.total_links(df)))
        
        ## Now adding the most busy user.
        if selected_user == "All":
            st.title("Top Busy Users")
            busy_users = f.top_busy_user(df)
            col1 , col2 = st.columns(2)

            with col1:
                plt.figure(figsize=(6,6))
                fig, ax = plt.subplots()
                plt.xticks(rotation='vertical')
                ax.bar(busy_users.index, busy_users.values, color='blue')
                st.pyplot(fig)
            
            with col2:
                perc_busy_user = f.top_busy_user_percentage(df)
                st.dataframe(perc_busy_user)
        
        ## Now plotting the word cloud
        st.title("Word cloud")
        wordcloud = f.create_wordcloud(words)        

        # plot the WordCloud image                      
        plt.figure(figsize = (8, 8), facecolor = None)
        plt.axis("off")
        plt.tight_layout(pad = 4)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud)
        st.pyplot(fig)

        ## Most frequent words
        st.title("Most frequent words")
        freq_words = f.most_freq_words(words)
        st.dataframe(freq_words)
