import streamlit as st
import pandas as pd
from datetime import datetime
import logging
import os
import sys
parent_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(os.path.dirname(parent_path))
sys.path.append(parent_path)
sys.path.append(root_path)
from config import TIMESPAN_DICT, IN_CONTAINER_DIVIDER, CONTAINER_STYLE, LINK_BUTTON_STYLE
from mapping import map_category_to_category_filter, map_color_to_severity

def filter_documents(documents, timespan, category_filter, severity_filter):
    filtered_documents = []
    
    for doc in documents:
        if isinstance(doc['date'], str):
            try:
                doc['datetime_object'] = datetime.strptime(doc['date'], '%d/%m/%Y')
            except Exception as ex:
                logging.error(f'Error in filter_documents: {ex}')
                continue

    try:
        start_date = TIMESPAN_DICT.get(timespan)
        
        if start_date:
            filtered_documents = [doc for doc in documents if ('datetime_object' in doc and doc['datetime_object'] >= start_date)]

        if category_filter and category_filter != 'All':
            filtered_documents = [doc for doc in filtered_documents if 'category' in doc and map_category_to_category_filter(category_filter) in doc['category']]

        if severity_filter and severity_filter != 'All':
            filtered_documents = [doc for doc in filtered_documents if 'sentiment_color' in doc and map_color_to_severity(doc['sentiment_color']) == severity_filter]

    except Exception as ex:
        logging.error(f'Error in filter_documents: {ex}')
        
    return filtered_documents

def sort_documents(documents):
    sorted_documents = []

    try:
        valid_documents = [doc for doc in documents if 'date' in doc and 'sentiment_score' in doc and isinstance(doc['date'], str)]
        for doc in valid_documents:
            try:
                doc['date'] = datetime.strptime(doc['date'], '%d/%m/%Y').strftime('%d-%B-%Y')
                doc['datetime_object'] = datetime.strptime(doc['date'], '%d-%B-%Y').date()
            except Exception as ex:
                logging.error(f'Error in sort_documents: {ex}')
                continue

        sorted_documents = sorted(valid_documents, key=lambda x: (x['datetime_object'], x['sentiment_score']), reverse=True)

    except Exception as ex:
        logging.error(f'Error in sort_documents: {ex}')

    return sorted_documents

def display_content(keys_to_check, keys_found, date, sentiment_color, article_links, non_display_links_length, similar_article_links_markdown, numeric_values_list, display_document_id):
    try:
        st.markdown(CONTAINER_STYLE, unsafe_allow_html=True)
        container = st.container(border=True)
        with container:
            for key, value in zip(keys_to_check, keys_found):
                if key == 'title':
                    st.subheader(value)

            # st.write(category_string)

            st.markdown(IN_CONTAINER_DIVIDER, unsafe_allow_html=True)

            for key, value in zip(keys_to_check, keys_found):
                if key == 'summary':
                    st.markdown(f"**:blue[{date}:]** :{sentiment_color}[{value}]")

            st.markdown(LINK_BUTTON_STYLE, unsafe_allow_html=True)
            st.link_button("View full article", article_links)
                
            toggle_key = 'show_similar_articles' + str(display_document_id)
            if non_display_links_length > 0 and st.toggle("Show similar articles", key=toggle_key):
                st.markdown(f'{similar_article_links_markdown}')

        st.markdown('''
            <hr style="height:1px;border-width:0;color:gray;background-color:gray">
        ''', unsafe_allow_html=True)

    except Exception as ex:
        logging.error(f'Error in display_content: {ex}')


def display_documents(sorted_documents):
    def isNaN(string):
        return (string != string)

    col1, col2 = st.columns(2)

    displayed_clusters = []
    idx = 0

    for doc in sorted_documents:
        try:
            if 'date' not in doc or 'cluster_id' not in doc:
                continue
            if not isinstance(doc['date'], str):
                continue
            if doc['cluster_id'] in displayed_clusters:
                continue

            cluster_id = doc['cluster_id']
            same_cluster_documents = []
            display_document = None
            non_display_links = []
            for document in sorted_documents:
                if document['cluster_id'] == cluster_id:
                    same_cluster_documents.append(sorted_documents)
                    if document['display_document'] == 'yes':
                        display_document = document
                    else:
                        non_display_links.append(document['article_links'])

            non_display_links_length = len(non_display_links)
            displayed_clusters.append(cluster_id)
            similar_article_links_markdown = ""
            if non_display_links_length > 0:
                for non_display_link in non_display_links:
                    similar_article_links_markdown += f"- {non_display_link}\n"

            if display_document:
                display_document_id = display_document['_id']
                date = display_document['date']
                article_links = display_document['article_links']
                try:
                    sentiment_color = display_document['sentiment_color']
                except Exception as ex:
                    logging.error(f'Error in display_documents: {ex}')
                    continue
                
                #TODO: Add category
                # category_key = display_document['category']
                # category_string='Categories: '

                # if isinstance(category_key, str):
                #     category_string += category_key
                # elif isinstance(category_key, list):
                #     category_string += str(category_key).strip('[]').replace("'", "")
                
                keys_to_check = ['summary', 'title']
                keys_found = []
                not_found_messages = {
                    'summary': "No summary available.",
                    'title': "No title found."
                }

                numeric_values_list = []
                skip_document = False
                for key in keys_to_check:
                    if key in display_document:
                        if isNaN(display_document[key]):
                            keys_found.append(not_found_messages.get(key))
                        else:
                            keys_found.append(str(display_document[key]).strip('[]').strip('{}'))

                    else:
                        keys_found.append(not_found_messages.get(key))
                        if key == 'summary' and not_found_messages[key] == display_document[key]:
                            skip_document = True
                            
                if skip_document:
                    continue
                
                if idx % 2 == 0:
                    with col1:
                        display_content(keys_to_check, keys_found, date, sentiment_color, article_links, non_display_links_length, similar_article_links_markdown, numeric_values_list, display_document_id)
                        idx += 1
                else:
                    with col2:
                        display_content(keys_to_check, keys_found, date, sentiment_color, article_links, non_display_links_length, similar_article_links_markdown, numeric_values_list, display_document_id)
                        idx += 1

        except Exception as ex:
            logging.error(f'Error in display_documents: {ex}')
            continue