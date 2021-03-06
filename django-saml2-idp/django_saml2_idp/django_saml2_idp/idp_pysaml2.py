import os
import saml2
from django.utils.translation import gettext as _
from saml2 import (BINDING_HTTP_POST,
                   BINDING_SOAP,
                   BINDING_HTTP_ARTIFACT,
                   BINDING_HTTP_REDIRECT,
                   BINDING_PAOS)
from saml2.saml import (NAMEID_FORMAT_TRANSIENT,
                        NAMEID_FORMAT_PERSISTENT)
from saml2.saml import (NAME_FORMAT_URI,
                        NAME_FORMAT_UNSPECIFIED,
                        NAME_FORMAT_BASIC)

from saml2.sigver import get_xmlsec_binary

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_URL = '/login/'

# idp protocol:fqdn:port
HOST = 'idp1.testunical.it'
PORT = 9000
HTTPS = False
if HTTPS:
    BASE = "https://%s:%s" % (HOST, PORT)
else:
    BASE = "http://%s:%s" % (HOST, PORT)
BASE_URL = '{}/idp'.format(BASE)
# end

SP_METADATA_URL = 'http://sp1.testunical.it:8000/saml2/metadata/'

SAML_IDP_CONFIG = {
    'debug' : True,
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin', '/usr/bin/xmlsec1']),
    'entityid': '%s/metadata' % BASE_URL,
    'attribute_map_dir': os.path.join(os.path.join(os.path.join(BASE_DIR,
                                                                'idp'),
                                      'saml2_config'),
                                      'attribute-maps'),
    'description': 'Example IdP setup',

    'service': {
        # TODO
        # "aa": {
            # "endpoints": {
                # "attribute_service": [
                    # ("%s/aap" % BASE, BINDING_HTTP_POST),
                    # ("%s/aas" % BASE, BINDING_SOAP)
                # ]
            # },
        # },
        'idp': {
            'name': 'Django localhost IdP',
            'endpoints': {
                'single_sign_on_service': [
                    ('%s/sso/post' % BASE_URL, BINDING_HTTP_POST),
                    ('%s/sso/redirect' % BASE_URL, BINDING_HTTP_REDIRECT),
                    # TODO
                    # ("%s/sso/art" % BASE, BINDING_HTTP_ARTIFACT),
                ],
                # TODO
                # "assertion_consumer_service": [
                    # ("%s/acs/post" % BASE, BINDING_HTTP_POST),
                    # ("%s/acs/redirect" % BASE, BINDING_HTTP_REDIRECT),
                    # ("%s/acs/artifact" % BASE, BINDING_HTTP_ARTIFACT),
                    # ("%s/acs/soap" % BASE, BINDING_SOAP),
                    # ("%s/ecp" % BASE, BINDING_PAOS)
                # ],
                # "artifact_resolution_service":[
                    # ("%s/ars" % BASE, BINDING_SOAP)
                # ],
                "single_logout_service": [
                    ("%s/slo/post" % BASE, BINDING_HTTP_POST),
                    ("%s/slo/redirect" % BASE, BINDING_HTTP_REDIRECT)
                    # ("%s/slo/soap" % BASE, BINDING_SOAP),
                ],
            },
            'name_id_format': [NAMEID_FORMAT_PERSISTENT,
                               NAMEID_FORMAT_TRANSIENT],

            'sign_response': True,
            'sign_assertion': True,
            'logout_requests_signed': True,
            'validate_certificate': True,
            # this is default
            'only_use_keys_in_metadata': True,

            # this must be a cert, not a boolean
            #'verify_ssl_cert': None,
            # 'verify_encrypt_cert_assertion': None,
            # 'verify_encrypt_cert_advice': None,

            # this works if pysaml2 is installed from peppelinux's fork
            # 'signing_algorithm':  saml2.xmldsig.SIG_RSA_SHA256,
            # 'digest_algorithm':  saml2.xmldsig.DIGEST_SHA256,

            # attribute policy
            # it seems that only SAML_IDP_SPCONFIG[SP]['attribute_mappings'] work as a filter!
            # policy with django-saml2-idp seems not!

            "policy": {
                "default": {
                    "lifetime": {"minutes": 15},

                    # if the sp is not conform to entity_categories the attributes will not be released
                    #"entity_categories": ["swamid", "edugain"],

                    "name_form": NAME_FORMAT_URI,
                    # "name_form": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri"
                    # "attribute_restrictions": {
                        # ## defaults Django User Account attributes (better do not show)
                        # "date_joined": None,
                        # "last_login": None,
                        # "password": None, # it's not readable but do not show by default
                        # "id": None,
                        # "user_permissions": None,

                        # ## only these will be showed
                        # 'username': None,
                        # 'first_name': None,
                        # 'last_name': None,
                        #
                        ## Here only mail addresses that end with ".umu.se" will be returned.
                        # 'email': None,
                        # #'email': [".*\.umu\.se$"],
                        # "mail": [".*\.umu\.se$"],
                    # },
                },
                # "https://example.com/sp": {
                    # "lifetime": {"minutes": 5},
                    # "nameid_format": NAMEID_FORMAT_PERSISTENT,
                    # "name_form": NAME_FORMAT_BASIC
                # }
            },
            # } # end attribute policy

        },
    },

    'metadata': [{
        # periodically download this file with a scheduler like cron
        # 'local': [os.path.join(os.path.join(os.path.join(BASE_DIR, 'idp'),
                  # 'saml2_config'), 'sp_metadata.xml')],
        #"remote": [{
            #"url": SP_METADATA_URL,
            # "cert":"idp_https_cert.pem"}]
            #}]

        "class": "saml2.mdstore.MetaDataFile",
        "metadata": [
                     (os.path.join(os.path.join(os.path.join(BASE_DIR, 'idp'),
                      'saml2_config'), 'sp_metadata.xml'), ),
                     # (full_path("metadata_sp_2.xml"), ),
                     # (full_path("vo_metadata.xml"), )
                     ],
    }],
    # Signing
    'key_file': BASE_DIR + '/certificates/private_key.pem',
    'cert_file': BASE_DIR + '/certificates/public_key.pem',
    # Encryption
    'encryption_keypairs': [{
        'key_file': BASE_DIR + '/certificates/private_key.pem',
        'cert_file': BASE_DIR + '/certificates/public_key.pem',
    }],

    # How many hours this configuration is expected to be accurate.
    # This of course is only used by make_metadata.py. The server will not stop working when this amount of time has elapsed :-).
    'valid_for': 24 * 10,

    # own metadata settings
    'contact_person': [
      {'given_name': 'Giuseppe',
       'sur_name': 'De Marco',
       'company': 'Universita della Calabria',
       'email_address': 'giuseppe.demarco@unical.it',
       'contact_type': 'administrative'},
      {'given_name': 'Giuseppe',
       'sur_name': 'De Marco',
       'company': 'Universita della Calabria',
       'email_address': 'giuseppe.demarco@unical.it',
       'contact_type': 'technical'},
      ],
    # you can set multilanguage information here
    'organization': {
      'name': [('Unical', 'it'), ('Unical', 'en')],
      'display_name': [('Unical', 'it'), ('Unical', 'en')],
      'url': [('http://www.unical.it', 'it'),
              ('http://www.unical.it', 'en')],
      },

    # TODO: put idp logs in a separate file too
    # "logger": {
        # "rotating": {
            # "filename": "idp.log",
            # "maxBytes": 500000,
            # "backupCount": 5,
        # },
        # "loglevel": "debug",
    # }

}


SAML_IDP_SHOW_USER_AGREEMENT_SCREEN = True
SAML_IDP_USER_AGREEMENT_ATTR_EXCLUDE = []
# User agreements will be valid for 1 year unless overriden. If this attribute is not used, user agreements will not expire
SAML_IDP_USER_AGREEMENT_VALID_FOR = 24 * 365

#SAML_IDP_DJANGO_USERNAME_FIELD = 'username'

SAML_AUTHN_SIGN_ALG = saml2.xmldsig.SIG_RSA_SHA1
SAML_AUTHN_DIGEST_ALG = saml2.xmldsig.DIGEST_SHA1

# Encrypt authn response
SAML_ENCRYPT_AUTHN_RESPONSE = True

SAML_IDP_SPCONFIG = {
    '{}'.format(SP_METADATA_URL): {
        #'processor': 'djangosaml2idp.processors.BaseProcessor',
        'processor': 'idp.processors.LdapAcademiaProcessor',
        'attribute_mapping': {
            # DJANGO: SAML
            # only these attributes from this IDP
            # 'email': 'email',
            # 'first_name': 'first_name',
            # 'last_name': 'last_name',
            # 'username': 'username',
            # 'is_staff': 'is_staff',
            # 'is_superuser':  'is_superuser',
            'schacPersonalUniqueID': 'schacPersonalUniqueID',
            'eduPersonPrincipalName': 'eduPersonPrincipalName',
            'eduPersonEntitlement': 'eduPersonEntitlement',
            'schacPersonalUniqueCode': 'schacPersonalUniqueCode',
            'cn': 'cn',
            'sn': 'sn',
            'mail': 'mail',
        },
        #'user_agreement_attr_exclude': ['sp_specific_secret_attr'],
        # Because we specify display name, that will be shown instead of entity id.
        'display_name': 'SP Number 1',
        'display_description': 'This SP does something that\'s probably important',
        # 'display_agreement_message': "ciao mamma",
        'user_agreement_valid_for': 24 * 3650 , # User agreements will be valid for 10 years for this SP only
        'signing_algorithm': saml2.xmldsig.SIG_RSA_SHA256,
        'digest_algorithm': saml2.xmldsig.DIGEST_SHA256,
        'encrypt_saml_responses': False,
    }
}
