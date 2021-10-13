from __future__ import annotations
from typing import Optional, Protocol, TypedDict, Dict, Any
from urllib.parse import urljoin
from xml.etree import ElementTree as ET

import requests
from pydantic import BaseModel


class LogMessage(TypedDict):
    campaign: str
    lead_type: str
    lead_json: str
    lead_xml: bytes
    status: int
    response: str


class Logger(Protocol):
    def log_request(self, log_message: LogMessage):
        ...


class Lead(BaseModel):
    campania: str
    source: Optional[str] = None
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    provincia: Optional[str] = None
    mensaje: Optional[str] = None
    fecha: Optional[Any] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    vendedor: Optional[str] = None
    extra: Dict[str, Any] = {}

    def to_xml(self) -> bytes:
        root = ET.Element('root')
        campaign = ET.Element('campania')
        campaign.text = self.campania
        root.append(campaign)

        prospects = ET.Element('prospectos')
        root.append(prospects)
        list_item = ET.Element('list-item')
        prospects.append(list_item)

        for field_name, field_value in self.__dict__.items():
            if field_name not in ['campania', 'extra'] and field_value is not None:
                try:
                    element = ET.Element(field_name)
                    element.text = field_value
                    list_item.append(element)
                except ValueError:
                    pass

        if self.extra:
            extra_element = ET.Element('extra')
            list_item.append(extra_element)
            for key, value in self.extra.items():
                child_item = ET.Element('list-item')
                extra_element.append(child_item)
                child_name = ET.Element('nombre')
                child_name.text = key
                child_item.append(child_name)
                child_value = ET.Element('valor')
                if not isinstance(value, str):
                    value = str(value)
                child_value.text = value
                child_item.append(child_value)

        return ET.tostring(root, encoding='utf-8')


class LeadsService:
    endpoint: str
    token: str
    logger: Optional[Logger]

    def __init__(self, endpoint: str, token: str, logger: Optional[Logger] = None):
        self.endpoint = endpoint
        self.token = token
        self.logger = logger

    @property
    def headers(self):
        "Returns a dict with headers used when calling delivery api."
        return {
            'Authorization': f'Token {self.token}',
            'Content-Type': 'application/xml',
        }

    def send(self, campaign: str, lead: Lead, lead_type: Optional[str] = None) -> LogMessage:
        url = urljoin(self.endpoint, 'prospectos/add/')
        xml = lead.to_xml()
        response = requests.post(url, headers=self.headers, data=xml)

        log_message: LogMessage = {
            'campaign': campaign,
            'lead_type': lead_type or '',
            'lead_json': lead.json(),
            'lead_xml': xml,
            'status': response.status_code,
            'response': response.text,
        }
        if self.logger is not None:
            self.logger.log_request(log_message)

        return log_message
