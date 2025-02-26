import streamlit as st
import logging
import os
import sys
current_path = os.path.abspath(__file__)
root_path = os.path.dirname(os.path.dirname(current_path))
sys.path.append(root_path)
from config import BAT_LOGO_PATH, CMS_LOGO_PATH, SEVERITY_LEGEND_HTML, BAT_LOGO_STYLE_HTML, CMS_LOGO_STYLE_HTML, INTRO_MESSAGE, TIMESPAN_DICT, SEVERITY_LIST, PAGE_TITLE
from utils.documents import filter_documents, sort_documents, display_documents
from utils.images import img_to_html
from utils.data import get_data

def set_page_configs():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=BAT_LOGO_PATH, layout="wide")

def display_legend():
    try:
        with open(SEVERITY_LEGEND_HTML) as f:
            st.markdown(f.read(), unsafe_allow_html=True)
        st.write()
    except Exception as ex:
        logging.error(f'Error in display_legend: {ex}')
        return None

def display_image_and_intro():
    try:
        # col1, col2 = st.columns(2)

        # with open(CMS_LOGO_STYLE_HTML) as f:
        #     st.markdown(f.read(), unsafe_allow_html=True)

        # with col1:
        #     st.markdown(img_to_html(CMS_LOGO_PATH), unsafe_allow_html=True)
        
        with open(BAT_LOGO_STYLE_HTML) as f:
            st.markdown(f.read(), unsafe_allow_html=True)
        
        st.markdown(img_to_html(BAT_LOGO_PATH), unsafe_allow_html=True)

    except Exception as ex:
        logging.error(f'Error in display_image_and_intro: {ex}')
        return None
    
    finally:
        st.markdown(f"<p style='text-align:center; font-size:15px;'><em>{INTRO_MESSAGE}</em></p>", unsafe_allow_html=True)

def display_filters():
    timespan = 'this week'
    category_filter = 'All'
    severity_filter = 'All'

    try:
        _, col3, col4, _ = st.columns([2, 3, 3, 2])
        
        with col3:
            st.write('Date range: ')
            timespan = st.selectbox(
                "Select Timespan:", TIMESPAN_DICT.keys(),
                label_visibility='collapsed',
                disabled=False,
                key='articles_time_option'
            )
        with col4:
            st.write('Severity: ')
            severity_filter = st.selectbox(
                "Select Severity:", SEVERITY_LIST,
                label_visibility='collapsed',
                disabled=False,
                key='articles_severity_option'
            )

        st.divider()
    
    except Exception as ex:
        logging.error(f'Error in display_filters: {ex}')
        
    return timespan, category_filter, severity_filter

def main():
    try:

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('app.log')
            ]
        )

        set_page_configs()
        display_image_and_intro()
        display_legend()
        timespan, category_filter, severity_filter = display_filters()

        documents = get_data()
    
        filtered_documents = filter_documents(
            documents, 
            timespan, 
            category_filter, 
            severity_filter
        )

        sorted_docs = sort_documents(filtered_documents)
        display_documents(sorted_docs)

    except Exception as ex:
        logging.error(f'Error in main: {ex}')
            
if __name__ == "__main__":
    main()