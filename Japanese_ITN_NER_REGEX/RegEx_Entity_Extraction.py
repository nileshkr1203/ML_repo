import sys
from typing import List
from summary.data.evaluate_model_request import ModelRequest
from summary.data.summry import Entity                             ##call this file based on production version location
import re
from summary.constants import logger                                ##call this file based on production version location
from summary.predefined_entities.entity_type import EntityType      ##call this file based on production version location
import Entity_extractor as pattern_based_entity_extractor


def get_pattern_entities(model_request: ModelRequest) -> List[Entity]:
    """"""
    transcripts = model_request.transcripts
    entities = []
    for index, turn in enumerate(transcripts):
        channel = turn.turn_channel.strip()
        line = turn.turn_text.strip()
        # unmodified text of each turn of the transcript
        turn_text = turn.turn_text.strip()
        turn_id = turn.line_no
        raw_turn_id = turn.raw_turn_id
        line, sec_number_entities = _sec_number(line, turn_id, channel, turn_text, raw_turn_id)
        line, chassis_entities = _chassis(line, turn_id, channel, turn_text, raw_turn_id)
        line, model_entities = _model(line, turn_id, channel, turn_text, raw_turn_id)
        line, cont_number_entities = _cont_number(line, turn_id, channel, turn_text, raw_turn_id)
        line, reg_number_entities = _reg_number(line, turn_id, channel, turn_text, raw_turn_id)
        
        all_entities = sec_number_entities + chassis_entities + model_entities + cont_number_entities + reg_number_entities 
        entities.extend(all_entities)
    return entities

#Entity functions
def _sec_number(line: str, turn_number: int, channel: str, turn_text: str, raw_turn_id: List[int]):
    sec_number_pattern = r'\bF\s{0,1}\d{8,9}\b'
    return pattern_based_entity_extractor.alphanumeric_entity(sec_number_pattern, line, turn_number, channel, turn_text, raw_turn_id)

def _chassis(line: str, turn_number: int, channel: str, turn_text: str, raw_turn_id: List[int]):
    chassis_pattern = r'\b[A-Z]{3}\s{0,1}\d\s{0,1}[A-Z]\s{0,1}\d{5}\s{0,1}[A-Z]{2}\s{0,1}\d{5}\b|\b[A-Z]{1,4}\s{0,1}\d{1,8}\s{0,1}[A-Z]{0,2}\s{0,1}\d{0,8}\b|'\
         r'\b[A-Z]{1,2}\s{0,1}\d{1,2}\s{0,1}[A-Z]\s{0,1}\d{7}\b|\b[A-Z]{1,2}\s{0,1}\d{3}\s{0,1}[A-Z]\s{0,1}\d{7}\b|'\
         r'\b[A-Z]{2}\s{0,1}\d\s{0,1}[A-Z]{2}\s{0,1}\d{6}\b|\b[A-Z]{5}\s{0,1}\d{6}\b'
    return pattern_based_entity_extractor.alphanumeric_entity(chassis_pattern, line, turn_number, channel, turn_text, raw_turn_id)

def _model(line: str, turn_number: int, channel: str, turn_text: str, raw_turn_id: List[int]):
    model_pattern = r'\b6AA-MXPH10\b|\b6AA-ZVW51\b|\b5BA-NSP170G\b|\bDAA-ZWR80G\b|\b6AA-ZWE214\b|\bDBA-M910A\b|\b5AA-A202A\b|\bDBA-ANH25W\b|\bCBA-NZT240\b|\bDBA-GRS182\b|\bCBA-ANM10W\b|\bCBA-ZZT240\b|\b6AA-MXPH10\b|'\
        r'\b6AA-ZVW51\b|\b5BA-NSP170G\b|\bDAA-ZWR80G\b|\b6AA-ZWE214\b|\bCBA-AZR60G\b|\b6AA-GR8\b|\bDBA-JF4\b|\b6BA-JH3\b|\b6BA-GB5\b|\b6BA-FL1\b|\bDBA-RC2\b|\bCBA-GD3\b|'\
        r'\b5AA-MK53S\b|\bDAA-MK42S\b|\b4AA-MR52S\b|\b5BA-MH85S\b|\b3BA-HA37S\b|\b3BA-JB64W\b|\b6AA-SNE13\b|\b6AA-HFC2\b|\b5BA-RV37\b|\b6BA-KFEP\b|\b5BA-DKLAW\b|'\
        r'\b3DA-KG2P\b|\b5BA-LA150S\b|\bDBA-L275S\b|\b6BA-LA900S\b|\b3BA-LA260S\b|\b5BA-M700S\b|\b3BA-GT3\b|\b4BA-SK5\b|\b4BA-VN5\b|\bDBA-164186\b|\b3DA-6L20\b|'\
        r'\bUA-ACM26W\b|\bGF-SF5\b'
    return pattern_based_entity_extractor.alphanumeric_entity(model_pattern, line, turn_number, channel, turn_text, raw_turn_id)

def _cont_number(line: str, turn_number: int, channel: str, turn_text: str, raw_turn_id: List[int]):
    cont_number_pattern = r'\b^(?![0-]{9,14})0[\d-]{9,14}\b'
    return pattern_based_entity_extractor.contact_entity(cont_number_pattern, line, turn_number, channel, turn_text, raw_turn_id)

def _reg_number(line: str, turn_number: int, channel: str, turn_text: str, raw_turn_id: List[int]):
    reg_number_pattern = r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b????????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b???\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b????????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b?????????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b???\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b??????\d{1,3}\s{0,1}[?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????ABEHKMTY]\s{0,1}\d{1,4}\b'
    return pattern_based_entity_extractor.alphanumeric_entity(reg_number_pattern, line, turn_number, channel, turn_text, raw_turn_id)


