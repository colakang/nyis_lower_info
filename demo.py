from bs4 import BeautifulSoup
import urllib2
import re

'''parse a single lawyer information'''


class LawyerInfo:
    'baseUrl = "https://www.avvo.com/attorneys/"'

    def __init__(self, request, lawyer_id):
        self.lawyer_id = lawyer_id
        self.lawyer = {}
        'self.url = LawyerInfo.baseUrl + str(lawyer_id) + ".html"'
        self.request = request
        try:
            """self.request = urllib2.Request(self.url)
            self.request.add_header('User-Agent', '''Mozilla/5.0 (Windows NT 10.0; WOW64)
                                                    AppleWebKit/537.36 (KHTML, like Gecko)
                                                    Chrome/50.0.2661.102 Safari/537.36''')"""
            response = urllib2.urlopen(self.request)
        except urllib2.HTTPError as e:
            print "The server couldn't fulfill the request"
            print "Error code: ", e.code
            self.rescode = e.code
        except urllib2.URLError as e:
            print "Failed to reach the server"
            print "The reason: ", e.reason
        else:
            self.rescode = 200
            self.resUrl = response.geturl()
            self.soup = BeautifulSoup(response.read(), 'lxml')
            response.close()
            self.res_id = re.search(r'(\d+)\.html', self.resUrl).group(1)
            if self.lawyer_id != int(self.res_id):
                self.rescode = 600
                print "read a person twice, origin: ", self.lawyer_id, " response id: ", self.res_id

    def display(self):
        self.parse()
        print self.resUrl
        print self.lawyer

    def get_name(self):
        name = {}
        fullname = self.soup.select('h1 span[itemprop="name"]')[0].string.split(" ")
        name['lastName'] = fullname.pop()
        name['firstName'] = " ".join(fullname)
        return name

    def get_licences(self):
        licences_html = self.soup.find("caption", text="License").find_next_sibling("tbody").find_all("tr")
        licences = []
        for lh in licences_html:
            licence = {"id": None}
            licence["state"] = lh.find(attrs={"data-title": "State"}).get_text()
            licence["status"] = lh.find(attrs={"data-title": "Status"}).get_text()
            licence["origin"] = lh.find(attrs={"data-title": "Origin"}).get_text()
            licence["updated"] = lh.find(attrs={"data-title": "Updated"}).get_text()
            licences.append(licence)
        return licences

    def get_field(self, field):
        caption = self.soup.find("caption", text=field)
        if caption:
            return LawyerInfo.get_from_template(caption)
        return None

    @staticmethod
    def get_from_template(temp):
        entries = []
        prop = temp.find_next_sibling("thead").tr.th.string
        entries_html = temp.find_next_sibling("tbody").find_all("tr")
        for eh in entries_html:
            entry = {}
            entry[prop] = eh.th.string
            props = eh.find_all("td")
            for p in props:
                entry[p["data-title"]] = p.string
            entries.append(entry)
        return entries

    def get_work_experience(self):
        work_exp = None
        caption = self.soup.find("caption", text="Work experience")
        if caption:
            work_exp = LawyerInfo.get_from_template(caption)
        return work_exp

    def get_awards(self):
        awards = None
        caption = self.soup.find("caption", text="Awards")
        if caption:
            '''awards_html = caption.find_next_sibling("tbody").find_all("tr")
            awards = []
            for aw in awards_html:
                award = {}
                award["award name"] = aw.th.string
                award["grantor"] = aw.find(attrs={"data-title": "Grantor"}).get_text()
                award["grant date"] = aw.find(attrs={"data-title": "Date granted"}).get_text()
                awards.append(award)'''
            awards = LawyerInfo.get_from_template(caption)
        return awards

    def get_payment(self):
        payment = None
        caption = self.soup.find(text="Payment")
        if caption:
            payment_area = caption.find_parent("div").find_next_sibling(class_="row")
            payment_titles_html = payment_area.find_all("strong")
            payment_titles = [title.string for title in payment_titles_html]
            payment_info_html = payment_area.find_all("small")
            payment_info = [info.string for info in payment_info_html]
            payment = dict(zip(payment_titles, payment_info))
        'print payment'
        return payment

    def get_spec_info(self):
        payment = self.get_payment()
        if payment:
            self.lawyer['payment'] = payment
        awards = self.get_field("Awards")
        if awards:
            self.lawyer['awards'] = awards
        work_exp = self.get_field("Work experience")
        if work_exp:
            self.lawyer['work experience'] = work_exp
        associations = self.get_field("Associations")
        if associations:
            self.lawyer["associations"] = associations
        legal_cases = self.get_field("Legal cases")
        if legal_cases:
            self.lawyer["legal cases"] = legal_cases
        publications = self.get_field("Publications")
        if publications:
            self.lawyer["publications"] = publications
        education = self.get_field("Education")
        if education:
            self.lawyer["education"] = education
        speaking_engagements = self.get_field("Speaking engagements")
        if speaking_engagements:
            self.lawyer["Speaking engagements"] = speaking_engagements

    def get_avvo_score(self):
        rating_html = self.soup.select('span[itemprop="ratingValue"]')
        if len(rating_html) != 0:
            return rating_html[0].string
        return "N/A"

    def get_practice_areas(self):
        areas_html = self.soup.find(href='#practice_areas')
        areas = areas_html.string.split(",")
        return areas

    @staticmethod
    def get_address(temp):
        address = {}
        name = temp.find("strong")
        if name:
            address["name"] = name.string
        street_html = temp.select('span[itemprop="streetAddress"]')
        if len(street_html) != 0:
            address["street address"] = street_html[0].get_text()
        city_html = temp.select('span[itemprop="addressLocality"]')
        if len(city_html) != 0:
            address["city"] = city_html[0].get_text()
        state_html = temp.select('span[itemprop="addressRegion"]')
        if len(state_html) != 0:
            address["state"] = state_html[0].get_text()
        zip_html = temp.select('span[itemprop="postalCode"]')
        if len(zip_html) != 0:
            address["zipcode"] = zip_html[0].get_text()
        return address

    def get_contact_info(self):
        '''contact information is also optional'''
        contact_html = self.soup.find(id="contact")
        if contact_html:
            contact = {}
            contact['address'] = LawyerInfo.get_address(contact_html)
            phone_html = contact_html.select('span[itemprop="telephone"]')
            if len(phone_html) != 0:
                contact['phone'] = phone_html[0].a.get('href').split(":")[-1]
            fax_html = contact_html.select('span[itemprop="faxNumber"]')
            if len(fax_html) != 0:
                contact['fax'] = fax_html[0].a.get('href').split(":")[-1]
            self.lawyer['contact'] = contact

    def parse(self):
        if self.rescode == 200:
            self.lawyer['id'] = self.res_id
            self.lawyer['name'] = self.get_name()
            self.lawyer['licences'] = self.get_licences()
            self.lawyer['avvo score'] = self.get_avvo_score()
            self.lawyer['is claimed'] = False
            self.lawyer['practice areas'] = self.get_practice_areas()
            self.get_contact_info()
            self.get_spec_info()
            '''awards = self.get_field("Awards")
            if awards:
                self.lawyer['awards'] = awards
            work_exp = self.get_field("Work experience")
            if work_exp:
                self.lawyer['work experience'] = work_exp
            associations = self.get_field("Associations")
            if associations:
                self.lawyer["associations"] = associations
            legal_cases = self.get_field("Legal cases")
            if legal_cases:
                self.lawyer["legal cases"] = legal_cases
            publications = self.get_field("Publications")
            if publications:
                self.lawyer["publications"] = publications
            education = self.get_field("Education")
            if education:
                self.lawyer["education"] = education
            speaking_engagements = self.get_field("Speaking engagements")
            if speaking_engagements:
                self.lawyer["Speaking engagements"] = speaking_engagements'''
            return self.lawyer
        return None
