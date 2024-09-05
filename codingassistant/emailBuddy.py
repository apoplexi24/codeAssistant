#TODO: create a method for specifying html and text components for emailBuddy.createTemplateMIMEMessage()

import smtplib, ssl
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class emailBuddy:
    def __init__(self) -> None:
        load_dotenv(dotenv_path='../env/.env.emailbuddy')
        self.__email_id: str = os.environ.get('EMAIL_ID')
        self.__email_password: str = os.environ.get('EMAIL_PASSWORD')
        self.smtp_server: str = 'smtp.gmail.com'
        self.ssl_port: int = 465
        self.ssl_context: ssl.SSLContext = ssl.create_default_context()
        
        
    def createMIMEMessage(self, receiver_email: str):
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = self.__email_id
        message["To"] = receiver_email
    
    
    def sendTextualEmail(self, receiver_email: str, email_content: str) -> None:
        with smtplib.SMTP_SSL(self.smtp_server, self.ssl_port, context=self.ssl_context) as server:
            server.login(self.__email_id, self.__email_password)
            server.sendmail(self.__email_id, receiver_email, email_content)
    

    def createTemplateMIMEMessage(self, html_components: dict, textual_components: dict, 
                            component_order_mapping: dict, mime_message: MIMEMultipart) -> MIMEMultipart:
        
        """
        ### h* id as keys (random key/id for values) and html components as values for html_components dict 
        html_components = ['h1':html1, 'h2': html2, 'h3': html3, ...]
        ### t* id as keys (random key/id for values) and textual components as values for textual_components dict
        textual_components = ['t1':text1, 't2':text2, 't3':text3, ...]
        ### order of components and the component id in component_order_mapping dict
        component_order_mapping = {
            1: 'h2', 2: 't1', 3: 'h3', 4: 't2', 5: 'h1', 6: 't3' 
        }
        
        """
        components_order_list = list()
        for component, order in component_order_mapping.items():
            components_order_list.insert(order, component)
        
        for component in components_order_list:
            if component in textual_components:
                mime_message.attach(MIMEText(textual_components[component], 'plain'))
            elif component in html_components:
                mime_message.attach(MIMEText(html_components[component], 'html'))   
            else:
                raise Exception("Invalid component")
        
        return mime_message
            

def main():
    e = emailBuddy()
    print("EmailBuddy Instance created => ", e)

if __name__ == '__main__':  
    main()