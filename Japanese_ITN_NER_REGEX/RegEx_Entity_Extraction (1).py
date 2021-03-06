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
    sec_number_pattern = r'\b[Ff]\s{0,1}\d{9,10}\b'
    return pattern_based_entity_extractor.alphanumeric_entity(sec_number_pattern, line, turn_number, channel, turn_text, raw_turn_id)

def _chassis(line: str, turn_number: int, channel: str, turn_text: str, raw_turn_id: List[int]):
    chassis_pattern = r'\b[a-z]{2,4}\s{0,1}\d{8,9}\b|\b[a-z]\s{0,1}\d{8}\b|\b[a-z]{2}\s{0,1}\d\s{0,1}[a-z]\s{0,1}\d{8}\b|\b[a-z]{2}\s{0,1}\d{2}\s{0,1}S\s{0,1}\d{6}\b|\b[a-z]{1,2}\s{0,1}\d{1,2}\s{0,1}[a-z]\s{0,1}\d{7}\b|'\
        r'\b[a-z]{1,2}\s{0,1}\d{3}\s{0,1}[a-z]\s{0,1}\d{7}\b|\b[a-z]{2}\s{0,1}\d\s{0,1}[a-z]{2}\s{0,1}\d{6}\b|\b[a-z]{5}\s{0,1}\d{6}\b|'\
        r'\b[a-z]{3}\s{0,1}\d\s{0,1}[a-z]{1}\s{0,1}\d{5}\s{0,1}[a-z]{2}\s{0,1}\d{5}\b|\b[a-z]{2}\s{0,1}\d\s{0,1}[a-z]{2}\s{0,1}\d{5}\b'
    return pattern_based_entity_extractor.alphanumeric_entity(chassis_pattern, line, turn_number, channel, turn_text, raw_turn_id)

def _model(line: str, turn_number: int, channel: str, turn_text: str, raw_turn_id: List[int]):
    model_pattern = r'\b\d{0,1}[a-z]{2,3}-[a-z0-9]{2,6}\b'
    return pattern_based_entity_extractor.alphanumeric_entity(model_pattern, line, turn_number, channel, turn_text, raw_turn_id)

def _cont_number(line: str, turn_number: int, channel: str, turn_text: str, raw_turn_id: List[int]):
    cont_number_pattern = r'\b(?![0-]{9,14}|0123456789|0\d{12,14})0[\d-]{9,14}\b'
    return pattern_based_entity_extractor.contact_entity(cont_number_pattern, line, turn_number, channel, turn_text, raw_turn_id)

def _reg_number(line: str, turn_number: int, channel: str, turn_text: str, raw_turn_id: List[int]):
    reg_number_pattern = r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b????????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b???\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b????????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b?????????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b???\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b|'\
    r'\b??????\s{0,1}\d{1,3}\s{0,1}[-?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????abehkmty]\s{0,1}\d{1,4}\b'
    return pattern_based_entity_extractor.alphanumeric_entity(reg_number_pattern, line, turn_number, channel, turn_text, raw_turn_id)


