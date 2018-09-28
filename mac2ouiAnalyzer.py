#!/usr/bin/env python3
# encoding: utf-8

from cortexutils.analyzer import Analyzer
import csv
from os import path
import re

def format_mac(mac):
    mac = re.sub('[.:-]', '', mac).lower()
    mac = ''.join(mac.split())
    assert len(mac) == 12
    assert mac.isalnum()
    mac = ":".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])
    return mac

class mac2ouiAnalyzer(Analyzer):
    """

    """

    def __init__(self):
        Analyzer.__init__(self)
        self.ouis = dict()
        self.company = ''
        self.address = ''

    def summary(self, raw):
        """Returns a summary, needed for 'short.html' template.

        :returns The MAC address and the company"""

        taxonomies = []
        level = "info"
        namespace = "OUI"
        predicate = "oui"
        if raw['company'] == 'Not registered':
            level = 'suspicious'

        value = format_mac(raw['MAC']) + ' (' + raw['company'] + ')'

        taxonomies.append(self.build_taxonomy(level, namespace, predicate, value))

        return {'taxonomies': taxonomies}

    def read_oui_database(self, db):
        """Reads the OUIs from the csv file

        :param db: The path to the csv file, default is oui.csv in the same 
        folder as the analyzer"""

        ouis = dict()

        if not path.exists(db):
            self.error('Cannot read oui database.')

        with open(db, newline='', encoding='utf-8') as csvfile:
            oui_dict_reader = csv.DictReader(csvfile, delimiter=',')
            for row in oui_dict_reader:
                ouis[row['Assignment'].lower()] = row['Organization Name']

        return ouis

    def find_oui(self, address):
        """Resolves the company to the mac address

        :param address: The mac address"""
        mac = format_mac(address)
        mac = mac.replace(':', '')
        mac = mac[:6]
        try:
            return self.ouis[mac]
        except KeyError:
            return 'Not registered'

    def run(self):
        self.ouis = self.read_oui_database(self.get_param('config.db_path', path.join(path.dirname(path.realpath(__file__))), 'oui.csv'))
        self.address = self.get_data()
        self.company = self.find_oui(self.address)
        self.report({
            'MAC': self.address,
            'company': self.company
            })


if __name__ == '__main__':
    mac2ouiAnalyzer().run()
