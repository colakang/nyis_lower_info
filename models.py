# mongoEngine model
'''def connectdb():
    connect('nyis')

class License(EmbeddedDocument):
    id = IntField(default=0)
    state = StringField(max_length=10, required=True)
    status = StringField(max_length=30, required=True)
    acquired_year = IntField(required=True)
    update_date = DateTimeField(required=True)


class Payment(EmbeddedDocument):
    fee = StringField()
    payment_types = StringField()


class Award(EmbeddedDocument):
    award_name = StringField(required=True)
    grantor = StringField(required=True)
    date_granted = StringField(required=True)


class WorkExp(EmbeddedDocument):
    title = StringField(required=True)
    company_name = StringField(required=True)
    Duration = StringField(required=True)


class Association(EmbeddedDocument):
    association_name = StringField(required=True)
    position = StringField(required=True)
    Duration = StringField(required=True)


class LegalCase(EmbeddedDocument):
    case_name = StringField(required=True)
    outcome = StringField(required=True)


class Publication(EmbeddedDocument):
    publication_name = StringField(required=True)
    title = StringField(required=True)
    date = StringField(required=True, max_length=4)


class Education(EmbeddedDocument):
    school_name = StringField()
    major = StringField()
    degree = StringField()
    graduated = StringField()


class SpeakingEngagement(EmbeddedDocument):
    conference_name = StringField()
    title = StringField()
    date = StringField()


class Lawyer(Document):
    avvo_id = IntField(required=True)
    name = StringField(required=True)
    licenses = ListField(DictField(required=True))   # ListField(EmbeddedDocumentField(License), required=True)
    contact = DictField(required=False)
    badk = StringField()
    practice_areas = ListField(StringField())
    is_claimed = BooleanField(default=False)
    avvo_score = StringField(max_length=5)
    payment = DictField()   # EmbeddedDocumentField(Payment)
    awards = ListField(DictField())  # ListField(EmbeddedDocumentField(Award))
    work_experience = ListField(DictField())   # ListField(EmbeddedDocumentField(WorkExp))
    associations = ListField(DictField())   # ListField(EmbeddedDocumentField(Association))
    legal_cases = ListField(DictField())   # ListField(EmbeddedDocumentField(LegalCase))
    publications = ListField(DictField())   # ListField(EmbeddedDocumentField(Publication))
    education = ListField(DictField())   # ListField(EmbeddedDocumentField(Education))
    speaking_engagements = ListField(DictField())   # ListField(EmbeddedDocumentField(SpeakingEngagement))
'''

# mongoKit model

from mongokit import *
import datetime
import logging

conn = Connection()


@conn.register
class Lawyer(Document):
    __database__ = 'nyis'
    __collection__ = 'lawyers'
    use_schemaless = True
    structure = {
        'avvo_id': int,
        'name':  basestring,
        'licenses': [{
            'id': int,
            'state': basestring,
            'status': basestring,
            'origin': int,
            'updated': datetime.datetime
        }],
        'contact': {
            'address': {
                'name': basestring,
                'street_address': basestring,
                'city': basestring,
                'state': basestring,
                'zipcode': basestring
            },
            'phone': basestring,
            'fax': basestring
        },
        'practice_areas': [basestring],
        'is_claimed': bool,
        'avvo_score': basestring,
        'payment': {
            'fees': basestring,
            'payment_methods': basestring
        },
        'awards': [{
            'award_name': basestring,
            'grantor': basestring,
            'date_granted': basestring
        }],
        'work_experience': [{
            'title': basestring,
            'company_name': basestring,
            'duration': basestring
        }],
        'associations': [{
            'association_name': basestring,
            'position': basestring,
            'duration': basestring
        }],
        'legal_cases': [{
            'case_name': basestring,
            'outcome': basestring
        }],
        'publications': [{
            'publication_name': basestring,
            'title': basestring,
            'date': basestring
        }],
        'education': [{
            'school_name': basestring,
            'major': basestring,
            'degree': basestring,
            'graduated': basestring
        }],
        'speaking_engagements': [{
            'conference_name': basestring,
            'title': basestring,
            'date': basestring
        }]
    }
    required_fields = ['avvo_id', 'name', 'licenses']
    # use avvo_id as index to optimize query
    indexes = [{
        'fields': ['avvo_id'],
        'unique': True
    }]


def save(lawyer):
    result = conn.Lawyer.one({'avvo_id': lawyer['avvo_id']})
    if not result:
        lawyer_db = conn.Lawyer(lawyer)
        lawyer_db.save()
        logging.debug("Lawyer id: %d is created" % lawyer['avvo_id'])
        return
    is_dif = False
    for prop in lawyer:
        if prop not in result:
            result[prop] = lawyer[prop]
            is_dif = True
        elif result[prop] != lawyer[prop]:
            result[prop] = lawyer[prop]
            is_dif = True
    if is_dif:
        logging.debug("Lawyer id: %d is updated" % lawyer['avvo_id'])
        result.save()
    else:
        logging.debug("Lawyer id: %d is kept" % lawyer['avvo_id'])
    print result
