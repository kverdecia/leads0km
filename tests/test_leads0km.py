#!/usr/bin/env python

"""Tests for `leads0km` package."""
from typing import List
from xml.etree import ElementTree as ET
import unittest
from unittest.mock import patch, Mock

import cuid

from leads0km import leads0km
from leads0km import factories


class TestLead(unittest.TestCase):
    def test_method_to_xml(self):
        lead: leads0km.Lead = factories.LeadFactory(fecha=cuid.cuid(),
            extra={cuid.cuid(): cuid.cuid(), cuid.cuid(): cuid.cuid()})
        xml_str = lead.to_xml()
        xml = ET.fromstring(xml_str)
        self.assertEqual(xml.tag, 'root')
        campaign_node = xml[0]
        self.assertEqual(campaign_node.tag, 'campania')
        self.assertEqual(campaign_node.text, lead.campania)
        prospects_node = xml[1]
        self.assertEqual(prospects_node.tag, 'prospectos')
        self.assertEqual(len(prospects_node), 1)
        list_item_node = prospects_node[0]
        self.assertEqual(len(list_item_node), 11)
        self.assertEqual(list_item_node.tag, 'list-item')
        self.assertEqual(list_item_node[0].tag, 'source')
        self.assertEqual(list_item_node[0].text, lead.source)
        self.assertEqual(list_item_node[1].tag, 'nombre')
        self.assertEqual(list_item_node[1].text, lead.nombre)
        self.assertEqual(list_item_node[2].tag, 'telefono')
        self.assertEqual(list_item_node[2].text, lead.telefono)
        self.assertEqual(list_item_node[3].tag, 'email')
        self.assertEqual(list_item_node[3].text, lead.email)
        self.assertEqual(list_item_node[4].tag, 'provincia')
        self.assertEqual(list_item_node[4].text, lead.provincia)
        self.assertEqual(list_item_node[5].tag, 'mensaje')
        self.assertEqual(list_item_node[5].text, lead.mensaje)
        self.assertEqual(list_item_node[6].tag, 'fecha')
        self.assertEqual(list_item_node[6].text, lead.fecha)
        self.assertEqual(list_item_node[7].tag, 'marca')
        self.assertEqual(list_item_node[7].text, lead.marca)
        self.assertEqual(list_item_node[8].tag, 'modelo')
        self.assertEqual(list_item_node[8].text, lead.modelo)
        self.assertEqual(list_item_node[9].tag, 'vendedor')
        self.assertEqual(list_item_node[9].text, lead.vendedor)
        extra_node = list_item_node[10]
        self.assertEqual(extra_node.tag, 'extra')
        self.assertEqual(len(extra_node), 2)
        key1, key2 = lead.extra.keys()
        # first extra field
        extra1_node = extra_node[0]
        self.assertEqual(extra1_node.tag, 'list-item')
        self.assertEqual(extra1_node[0].tag, 'nombre')
        self.assertEqual(extra1_node[0].text, key1)
        self.assertEqual(extra1_node[1].tag, 'valor')
        self.assertEqual(extra1_node[1].text, lead.extra[key1])
        # second extra field
        extra2_node = extra_node[1]
        self.assertEqual(extra2_node.tag, 'list-item')
        self.assertEqual(extra2_node[0].tag, 'nombre')
        self.assertEqual(extra2_node[0].text, key2)
        self.assertEqual(extra2_node[1].tag, 'valor')
        self.assertEqual(extra2_node[1].text, lead.extra[key2])


class TestFlatLead(unittest.TestCase):
    def test_method_to_xml(self):
        lead: leads0km.FlatLead = factories.FlatLeadFactory(fecha=cuid.cuid(),
            extra={cuid.cuid(): cuid.cuid(), cuid.cuid(): cuid.cuid()})
        xml_str = lead.to_xml()
        xml = ET.fromstring(xml_str)
        self.assertEqual(xml.tag, 'root')
        campaign_node = xml[0]
        self.assertEqual(campaign_node.tag, 'campania')
        self.assertEqual(campaign_node.text, lead.campania)
        prospects_node = xml[1]
        self.assertEqual(prospects_node.tag, 'prospectos')
        self.assertEqual(len(prospects_node), 1)
        list_item_node = prospects_node[0]
        self.assertEqual(len(list_item_node), 12)
        self.assertEqual(list_item_node.tag, 'list-item')
        self.assertEqual(list_item_node[0].tag, 'source')
        self.assertEqual(list_item_node[0].text, lead.source)
        self.assertEqual(list_item_node[1].tag, 'nombre')
        self.assertEqual(list_item_node[1].text, lead.nombre)
        self.assertEqual(list_item_node[2].tag, 'telefono')
        self.assertEqual(list_item_node[2].text, lead.telefono)
        self.assertEqual(list_item_node[3].tag, 'email')
        self.assertEqual(list_item_node[3].text, lead.email)
        self.assertEqual(list_item_node[4].tag, 'provincia')
        self.assertEqual(list_item_node[4].text, lead.provincia)
        self.assertEqual(list_item_node[5].tag, 'mensaje')
        self.assertEqual(list_item_node[5].text, lead.mensaje)
        self.assertEqual(list_item_node[6].tag, 'fecha')
        self.assertEqual(list_item_node[6].text, lead.fecha)
        self.assertEqual(list_item_node[7].tag, 'marca')
        self.assertEqual(list_item_node[7].text, lead.marca)
        self.assertEqual(list_item_node[8].tag, 'modelo')
        self.assertEqual(list_item_node[8].text, lead.modelo)
        self.assertEqual(list_item_node[9].tag, 'vendedor')
        self.assertEqual(list_item_node[9].text, lead.vendedor)
        self.assertEqual(list_item_node[10].tag, 'valor2')
        self.assertEqual(list_item_node[10].text, lead.valor2)
        self.assertEqual(list_item_node[11].tag, 'valor1')
        self.assertEqual(list_item_node[11].text, lead.valor1)


class TestLeadsService(unittest.TestCase):
    def test_constructor(self):
        endpoint = cuid.cuid()
        token = cuid.cuid()
        mocked_logger = Mock()
        service = leads0km.LeadsService(endpoint, token, mocked_logger)
        self.assertEqual(service.endpoint, endpoint)
        self.assertEqual(service.token, token)
        self.assertIs(service.logger, mocked_logger)

    def test_property_headers(self):
        token = cuid.cuid()
        service = leads0km.LeadsService(cuid.cuid(), token, Mock())

        expected = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/xml',
        }
        self.assertEqual(service.headers, expected)

    def test_method_send(self):
        campaign = cuid.cuid()
        endpoint = f'https://{cuid.cuid()}.com'
        token = cuid.cuid()
        mocked_logger = Mock()
        service = leads0km.LeadsService(endpoint, token, mocked_logger)
        # lead: leads0km.Lead = factories.LeadFactory()

        flat_lead: leads0km.FlatLead = factories.FlatLeadFactory()
        non_flat_lead: leads0km.Lead = factories.LeadFactory()
        test_cases: List[leads0km.LeadProtocol] = [flat_lead, non_flat_lead]

        for lead in test_cases:
            with patch('requests.post') as mocked_post:
                mocked_post.return_value = Mock()
                mocked_post.return_value.status_code = 201
                mocked_post.return_value.text = cuid.cuid()
                lead_type = cuid.cuid()
                response = service.send(campaign, lead, lead_type)

                xml = lead.to_xml()
                expected_url = f'{endpoint}/prospectos/add/'

                mocked_post.assert_called_once_with(expected_url, headers=service.headers,
                    data=xml)
                self.assertEqual(response['campaign'], campaign)
                self.assertEqual(response['lead_type'], lead_type)
                self.assertEqual(response['lead_json'], lead.json())
                self.assertEqual(response['lead_xml'], lead.to_xml())
                self.assertEqual(response['response'], mocked_post.return_value.text)
                self.assertEqual(response['status'], 201)


if __name__ == '__main__':
    unittest.main()
