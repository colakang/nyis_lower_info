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
            self.soup = BeautifulSoup(response.read(), 'html.parser')
            response.close()

    def display(self):
        self.parse()
        print self.resUrl
        print self.lawyer

    def get_id(self):
        return re.search(r'(\d+)\.html', self.resUrl).group(1)

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
        return self.soup.select('span[itemprop="ratingValue"]')[0].string

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
        address["street address"] = temp.select('span[itemprop="streetAddress"]')[0].get_text()
        address["city"] = temp.select('span[itemprop="addressLocality"]')[0].get_text()
        address["state"] = temp.select('span[itemprop="addressRegion"]')[0].get_text()
        address["zipcode"] = temp.select('span[itemprop="postalCode"]')[0].get_text()
        return address

    @staticmethod
    def get_fax(temp):
        fax = ""
        fax_html = temp.select('span[itemprop="faxNumber"]')
        if fax_html:
            fax = fax_html[0].a.get('href').split(":")[-1]
        return fax

    def get_contact_info(self):
        contact = {}
        contact_html = self.soup.find(id="contact").find("address")
        contact['address'] = LawyerInfo.get_address(contact_html)
        contact['phone'] = contact_html.select('span[itemprop="telephone"]')[0].a.get('href').split(":")[-1]
        contact['fax'] = LawyerInfo.get_fax(contact_html)
        return contact

    def parse(self):
        self.lawyer['id'] = self.get_id()
        self.lawyer['name'] = self.get_name()
        self.lawyer['licences'] = self.get_licences()
        self.lawyer['avvo score'] = self.get_avvo_score()
        self.lawyer['is claimed'] = False
        self.lawyer['practice areas'] = self.get_practice_areas()
        self.lawyer["contact"] = self.get_contact_info()
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
