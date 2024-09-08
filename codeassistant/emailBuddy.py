#TODO: create a method for specifying html and text components for emailBuddy.createTemplateMIMEMessage()

import smtplib, ssl
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

class emailBuddy:
    def __init__(self) -> None:
        load_dotenv(dotenv_path='../env/.env.emailbuddy')
        self.__email_id: str = os.environ.get('EMAIL_ID')
        self.__email_password: str = os.environ.get('EMAIL_PASSWORD')
        self.smtp_server: str = 'smtp.gmail.com'
        self.ssl_port: int = 465
        self.ssl_context: ssl.SSLContext = ssl.create_default_context()
        self.textual_components = dict()
        self.html_components = dict()
        self.text_components_index = 1
        self.html_components_index = 1
        self.order = 0
        self.component_order_mapping = dict()
        
    def createMIMEMessage(self, receiver_email: str):
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = self.__email_id
        message["To"] = receiver_email
    
    
    def sendTextualEmail(self, receiver_email: str, email_content: str) -> None:
        with smtplib.SMTP_SSL(self.smtp_server, self.ssl_port, context=self.ssl_context) as server:
            server.login(self.__email_id, self.__email_password)
            server.sendmail(self.__email_id, receiver_email, email_content)
    

    def createTemplateMIMEMessage(self,mime_message: MIMEMultipart) -> MIMEMultipart:
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
        for component, order in self.component_order_mapping.items():
            components_order_list.insert(order, component)
        
        for component in components_order_list:
            if component in self.textual_components:
                mime_message.attach(MIMEText(self.textual_components[component], 'plain'))
            elif component in self.html_components:
                mime_message.attach(MIMEText(self.html_components[component], 'html'))   
            else:
                raise Exception("Invalid component")
        
        return mime_message
    
    
    def add_text_content(self, text_content: str, order: (str|int) = 'next') -> MIMEMultipart:
        self.textual_components['t' + str(self.text_components_index)] = text_content
        if order == 'next':
            self.component_order_mapping['t' + str(self.text_components_index)] = self.order
            self.order+=1
        elif type(order) == int:
            self.component_order_mapping['t' + str(self.text_components_index)] = order
        else:
            raise(Exception("Invalid ordering of element"))
    
    
    def add_html_content(self, html_content: str, order: (str|int) = 'next') -> MIMEMultipart:        
        self.html_components['h' + str(self.html_components_index)] = html_content
        if order == 'next':
            self.component_order_mapping['h' + str(self.html_components_index)] = self.order
            self.order+=1
        elif type(order) == int:
            self.component_order_mapping['h' + str(self.html_components_index)] = order
        else:
            raise(Exception("Invalid ordering of element"))
        
        
    def addAttachment(self, mime_message: MIMEMultipart, attachment_path: str) -> MIMEMultipart:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {attachment_path}',
        )
        mime_message.attach(part)
        return mime_message


def main():
    e = emailBuddy()
    print("EmailBuddy Instance created => ", e)

if __name__ == '__main__':  
    main()