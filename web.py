# Copyright [2017] [GLORIA CABRERA MORENO]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import http.server
import socketserver
import http.client
import json

class OpenFDAClient():

    OPEN_API_URL= "api.fda.gov"
    OPEN_API_EVENT= "/drug/event.json"
    OPEN_API_DRUG= '&search=patient.drug.medicinalproduct:'
    OPEN_API_COMPANY= '&search=companynumb:'

    def get_event (self,limit):
        ##
        # GET EVENT
        ##
        conn = http.client.HTTPSConnection(self.OPEN_API_URL)
        conn.request("GET", self.OPEN_API_EVENT + "?limit=" + limit)
        r1 = conn.getresponse()
        data1 = r1.read()
        data2 = data1.decode ("utf8")
        library_data2= json.loads(data2)
        events= library_data2 ['results']
        return events

    def get_event_search_drug(self,drug_name):
        conn = http.client.HTTPSConnection(self.OPEN_API_URL)
        conn.request("GET", self.OPEN_API_EVENT + "?limit=10" + self.OPEN_API_DRUG + drug_name)
        r1 = conn.getresponse()
        data1 = r1.read()
        data2 = data1.decode ("utf8")
        library_data2= json.loads(data2)
        events_search_drug= library_data2 ['results']
        return events_search_drug

    def get_event_search_company(self,company_name):
        conn = http.client.HTTPSConnection(self.OPEN_API_URL)
        conn.request("GET", self.OPEN_API_EVENT + "?limit=10" + self.OPEN_API_COMPANY + company_name)
        r1 = conn.getresponse()
        data1 = r1.read()
        data2 = data1.decode ("utf8")
        library_data2= json.loads(data2)
        events_search_company= library_data2 ['results']
        return events_search_company

class OpenFDAParser():

    def get_drugs_from_events (self,events):
        drugs=[]
        for event in events:
            drugs += [event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_companies_from_events (self,events):
        companies=[]
        for event in events:
            companies += [event['companynumb']]
        return companies

    def get_companies_from_search_drug (self, events_search_drug):
        company_drugs=[]
        for event in events_search_drug:
            company_drugs += [event['companynumb']]
        return company_drugs

    def get_medicines_from_search_company (self, events_search_company):
        company_event = []
        for event in events_search_company:
            company_event += [event['patient']['drug'][0]['medicinalproduct']]
        return company_event

    def get_gender_from_event (self, events):
        gender = []
        for event in events:
            gender +=[event['patient']['patientsex']]
        return gender

class OpenFDAHTML():

    def get_main_page(self):
            html = """
            <html>
                <head>
                    <title>OpenFDA Cool App</title>
                </head>
                <body>
                    <h1>OpenFDA Client</h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List: Send to Open FDA"></input>
                        <input type = "number" name ="limit">
                        </input>
                    </form>
                    <form method="get" action="searchDrug">
                        <input type = "text" name="drug"></input>
                        <input type= "submit" value="Drug Search: Send to Open FDA">
                        </input>
                    </form>
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List: Send to Open FDA"></input>
                        <input type = "number" name ="limit">
                        </input>
                    </form>
                    <form method="get" action="searchCompany">
                        <input type = "text" name="company"></input>
                        <input type="submit" value="Company Search: Send to Open FDA"></input>
                    </form>
                    <form method= "get" action="listGender">
                        <input type = "submit" value = "Gender List: Send to Open FDA"></input>
                        <input type = "number" name ="limit">
                        </input>
                    </form>
                </body>
            </html>
            """
            return html

    def get_second_page(self,name,event):
        #med=self.get_drugs_from_events()
        medicinal=''
        for i in event:
            medicinal += "<li>"+i+"</li>"
        html2="""
        <html>
            <head><h2>%s</h2></head>
                <body>
                    <ol>
                        %s
                    </ol>
                </body>
        </html>
        """ %(name, medicinal)
        return html2

    def implement_error (self):
        html= """
        <html>
            <head></head>
            <body>
            <h1>Error 404 NOT FOUND</h1>
            </body>
        </html>
        """
        return html

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        main_page = False
        is_event_drug = False
        is_search_drug = False
        is_event_company = False
        is_search_company = False
        is_event_gender = False
        is_secret = False
        is_redirect = False
        if self.path == '/':
            main_page=True
        elif 'listDrugs' in self.path:
            is_event_drug= True
        elif 'searchDrug' in self.path:
            is_search_drug= True
        elif 'listCompanies' in self.path:
            is_event_company=True
        elif 'searchCompany' in self.path:
            is_search_company=True
        elif 'listGender' in self.path:
            is_event_gender= True
        elif self.path == '/secret':
            is_secret = True
        elif self.path == '/redirect':
            is_redirect = True

        RESPONSE=200
        header1 = 'Content-type'
        header2 = 'text/html'

        client_object= OpenFDAClient()
        parser_object= OpenFDAParser()
        html_object = OpenFDAHTML()

        if main_page:
            html= html_object.get_main_page()
        elif is_event_drug:
            limit= self.path.split("=")[1]
            event=client_object.get_event(limit)
            drugs = parser_object.get_drugs_from_events(event)
            title= "List of the drugs"
            html= html_object.get_second_page(title, drugs)
        elif is_search_drug:
            drug=self.path.split("=")[1]
            event=client_object.get_event_search_drug(drug)
            companynumb=parser_object.get_companies_from_search_drug(event)
            title= "Search of the drugs"
            html= html_object.get_second_page(title, companynumb)
        elif is_event_company:
            limit= self.path.split("=")[1]
            event=client_object.get_event(limit)
            companies = parser_object.get_companies_from_events(event)
            title= "List of the companies"
            html= html_object.get_second_page(title, companies)
        elif is_search_company:
            company=self.path.split("=")[1]
            events=client_object.get_event_search_company (company)
            medicinalproduct= parser_object.get_medicines_from_search_company(events)
            title= "Search of the drugs"
            html = html_object.get_second_page (title, medicinalproduct)
        elif is_event_gender:
            limit= self.path.split("=")[1]
            event= client_object.get_event(limit)
            gender= parser_object.get_gender_from_event(event)
            title = "List of the patiente's gender"
            html=html_object.get_second_page(title,gender)
        elif is_secret:
            RESPONSE = 401
            header1 = 'WWW-Authenticate'
            header2 = 'Basic realm="My Realm"'
        elif is_redirect:
            RESPONSE = 302
            header1 = 'Location'
            header2 = 'http://localhost:8000/'
        else:
            RESPONSE=404
            html = html_object.implement_error()

        self.send_response(RESPONSE)
        self.send_header(header1,header2)
        self.end_headers()

        if not is_secret and not is_redirect:
            self.wfile.write(bytes(html, "utf8"))

        return
