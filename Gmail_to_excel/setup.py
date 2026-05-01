import os
import Gmail_to_excel_Package

config = {
    'username': os.environ['GMAIL_USERNAME'],
    'password': os.environ['GMAIL_APP_PASSWORD'],
    'search_query': 'Prospective PhD',
    'output_file_path': os.environ.get('SPREADSHEET_URL', ''),
    'gmail_label_name': 'in:sent'
}

Gmail_to_excel_Package.write_gmail_messages_to_excel(config)
