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
    reg_number_pattern = r'\b品川\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b函館\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b旭川\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b室蘭\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b釧路\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b帯広\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b北見\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b青森\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b八戸\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b岩手\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b宮城\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b秋田\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b山形\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b庄内\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b福島\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\bいわき\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b水戸\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b土浦\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b宇都宮\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\bとちぎ\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b群馬\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b大宮\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b所沢\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b熊谷\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b春日部\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b千葉\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b習志野\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b袖ヶ浦\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b野田\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b品川\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b練馬\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b足立\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b八王子\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b多摩\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b横浜\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b川崎\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b湘南\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b相模\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b山梨\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b新潟\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b長岡\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b富山\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b石川\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b長野\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b松本\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b福井\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b岐阜\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b飛騨\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b静岡\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b浜松\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b沼津\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b名古屋\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b豊橋\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b三河\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b尾張小牧\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b三重\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b滋賀\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b京都\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b大阪\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\bなにわ\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b和泉\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b神戸\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b姫路\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b奈良\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b和歌山\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b鳥取\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b島根\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b岡山\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b広島\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b福山\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b山口\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b徳島\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b香川\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b愛媛\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b高知\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b福岡\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b北九州\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b久留米\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b筑豊\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b佐賀\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b長崎\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b佐世保\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b熊本\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b大分\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b宮崎\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b鹿児島\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b沖縄\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b苫小牧\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b知床\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b弘前\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b盛岡\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b平泉\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b仙台\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b会津\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b郡山\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b白河\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\bつくば\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b那須\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b高崎\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b前橋\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b川越\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b川口\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b越谷\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b柏\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b松戸\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b成田\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b市川\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b船橋\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b市原\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b杉並\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b板橋\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b世田谷\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b江東\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b葛飾\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b富士山\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b伊豆\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b上越\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b金沢\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b諏訪\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b一宮\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b豊田\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b岡崎\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b春日井\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b鈴鹿\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b伊勢志摩\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b四日市\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b堺\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b飛鳥\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b出雲\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b倉敷\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b下関\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b高松\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b奄美\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b奄美\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b|'\
r'\b札幌\d{1,3}\s{0,1}[のあいうえかきくけこさすせそたちつてとなにぬねのはひふほまみむめもやゆよらりるろをれわABEHKMTY]\s{0,1}\d{1,4}\b'
    return pattern_based_entity_extractor.alphanumeric_entity(reg_number_pattern, line, turn_number, channel, turn_text, raw_turn_id)


