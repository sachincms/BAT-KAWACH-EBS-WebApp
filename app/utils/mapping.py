import logging


def map_color_to_severity(color):
    '''
    Maps a color value to a severity level.
    
    Args:
      color (str): The color value to map 
    
    Returns:
      str: The mapped severity level ('High', 'Medium', 'Low')
    '''
    try:
        if color == 'red':
            return 'High'
        elif color == 'orange':
            return 'Medium'
        else:
            return 'Low'
        
    except Exception as ex:
        logging.error(f'Error in map_color_to_severity: {ex}')


def map_category_to_category_filter(category):
    '''
    Maps a category string to a category filter string for filtering documents.

    Args:
        category (str): The category string to map

    Returns:
        str: The mapped category filter string
    '''
    try:
        if category == 'Suspected Outbreak':
            return 'suspected disease outbreak'
        elif category == 'Confirmed Outbreak':
            return 'confirmed disease outbreak'
        elif category == 'Climate':
            return 'climate'
        elif category == 'Disease Information':
            return 'disease information'
        else:
            return 'others'
        
    except Exception as ex:
        logging.error(f'Error in map_category_to_category_filter: {ex}')