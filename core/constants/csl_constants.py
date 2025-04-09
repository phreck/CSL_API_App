"""
Constants for the Consolidated Screening List (CSL) API.
Source definitions from: https://developer.trade.gov/api-details#api=consolidated-screening-list&operation=search
"""

# CSL API Source Lists with their descriptions
CSL_SOURCES = [
    {
        'code': 'SDN',
        'name': 'Specially Designated Nationals',
        'agency': 'Office of Foreign Assets Control',
        'description': 'Individuals and companies owned or controlled by, or acting for or on behalf of, targeted countries.'
    },
    {
        'code': 'FSE',
        'name': 'Foreign Sanctions Evaders',
        'agency': 'Office of Foreign Assets Control',
        'description': 'Foreign individuals and entities determined to have violated, attempted to violate, conspired to violate, or caused a violation of U.S. sanctions.'
    },
    {
        'code': 'EL',
        'name': 'Entity List',
        'agency': 'Bureau of Industry and Security',
        'description': 'Parties whose presence in a transaction can trigger a license requirement under the Export Administration Regulations.'
    },
    {
        'code': 'DPL',
        'name': 'Denied Persons List',
        'agency': 'Bureau of Industry and Security',
        'description': 'Individuals and entities that have been denied export privileges.'
    },
    {
        'code': 'UVL',
        'name': 'Unverified List',
        'agency': 'Bureau of Industry and Security',
        'description': 'Parties who BIS has been unable to verify in prior transactions.'
    },
    {
        'code': 'ISN',
        'name': 'Nonproliferation Sanctions',
        'agency': 'State Department',
        'description': 'Parties that have been sanctioned under various statutes.'
    },
    {
        'code': 'DTC',
        'name': 'ITAR Debarred',
        'agency': 'Directorate of Defense Trade Controls',
        'description': 'Entities and individuals prohibited from participating in exports of defense articles and services.'
    },
    {
        'code': 'CAP',
        'name': 'Foreign Financial Institutions Subject to Part 561',
        'agency': 'Office of Foreign Assets Control',
        'description': 'Foreign financial institutions subject to Part 561.'
    },
    {
        'code': 'SSI',
        'name': 'Sectoral Sanctions Identifications List',
        'agency': 'Office of Foreign Assets Control',
        'description': 'Identifies persons operating in sectors of the Russian economy identified by the Secretary of the Treasury.'
    },
    {
        'code': 'MEU',
        'name': 'Military End User List',
        'agency': 'Bureau of Industry and Security',
        'description': 'Parties that represent an unacceptable risk of use in or diversion to a \'military end use\' or \'military end user\'.'
    },
    {
        'code': 'NS-ISA',
        'name': 'Non-SDN Iranian Sanctions Act',
        'agency': 'Office of Foreign Assets Control',
        'description': 'List of persons identified by OFAC as having certain Iran-related activities.'
    },
    {
        'code': 'PLC',
        'name': 'Palestinian Legislative Council List',
        'agency': 'Office of Foreign Assets Control',
        'description': 'Members of the Palestinian Legislative Council who were elected on the party slate of Hamas or other designated entities.'
    },
    {
        'code': '561',
        'name': 'Non-SDN Menu-Based Sanctions',
        'agency': 'Office of Foreign Assets Control',
        'description': 'List of persons subject to non-SDN Menu-Based Sanctions'
    },
    {
        'code': 'CAPTA',
        'name': 'CAPTA List',
        'agency': 'Office of Foreign Assets Control',
        'description': 'Foreign financial institutions subject to correspondent account or payable-through account sanctions.'
    },
    {
        'code': 'CMIC',
        'name': 'Non-SDN Chinese Military-Industrial Complex Companies List',
        'agency': 'Office of Foreign Assets Control',
        'description': 'Chinese Military-Industrial Complex Companies'
    },
    {
        'code': 'FTO',
        'name': 'Foreign Terrorist Organizations',
        'agency': 'State Department',
        'description': 'Foreign organizations that are designated by the Secretary of State.'
    },
    {
        'code': 'UKRAINE-EO',
        'name': 'Executive Order 13662 Directive Entities',
        'agency': 'Office of Foreign Assets Control',
        'description': 'Entities subject to directives under EO 13662 regarding the situation in Ukraine.'
    }
]

# Dictionary for quick lookup of source details by code
CSL_SOURCES_DICT = {source['code']: source for source in CSL_SOURCES}

# Entity types available in the CSL API
CSL_ENTITY_TYPES = [
    {'code': 'Individual', 'name': 'Individual'},
    {'code': 'Entity', 'name': 'Entity'},
    {'code': 'Vessel', 'name': 'Vessel'},
    {'code': 'Aircraft', 'name': 'Aircraft'}
]