## intent: greet
- अरे
- नमस्ते
- नमस्ते!
- hello there
- शुभ प्रभात
- सुसंध्या
- मोइन
- सुनो
- चलो चलते हैं
- अरे यार
- शुभप्रभात
- सुसंध्या!
- नमस्कार

## intent: goodbye
- नमस्कार
- cu
- अलविदा
- बाद में मिलते हैं
- शुभ रात्रि
- shubh raatri
- alavida
- अलविदा!
- आपका दिन शुभ हो
- मैं जल्द ही तुमसे मिलूँगा
- bye bye
- see you later

## intent: mood_affirm
- हाँ
- ह
- वास्तव में
- बेशक
- वह अच्छा प्रतीत होता है
- सही बात

## intent: mood_deny
- नहीं
- न
- कभी नहीं
- मुझे ऐसा नहीं लगता
- यह पसंद नहीं है
- बिलकुल नहीं
- ज़रूरी नहीं

## intent: mood_great
- उत्तम
- वाह् भई वाह
- गजब का
- एक राजा की तरह अद्भुत लग रहा है
- कमाल है
- मुझे बहुत अच्छा लग रहा है
- मैं महान हूं
- मैं अद्भुत हुँ
- मैं दुनिया को बचाने जा रहा हूँ
- सुपर स्टोक्ड
- बहुत खूब
- इतना सही
- बहुत अच्छा
- अति उत्तम

## intent: mood_unhappy
- मेरा दिन भयानक था
- मैं दुखी हूँ
- मुझे बहुत अच्छा नहीं लग रहा है
- मैं निराश हूँ
- अति दुखद
- मैं बहुत दुखी हु
- उदास
- बहुत दुख की बात है
- अप्रसन्न
- अच्छा नही
- बहुत अच्छा नहीं
- अत्यधिक दुखी
- बहुतत दुख की बात
- so sad
- बहुत बुरा - क्या मुझे [पक्षी](समूह: पक्षी) की एक प्यारी सी तस्वीर मिल सकती है, कृपया?
- वास्तव में खराब और केवल [कुत्ते](समूह: शिब्स) तस्वीरें और उसे बदल दें।
- अच्छा नही। केवल एक चीज जो मुझे बेहतर बना सकती है वह है एक प्यारा [बिल्ली का बच्चा](समूह: बिल्लियाँ) की तस्वीर।
- बहुत दुख की बात। केवल [puppy](group:shibes) की तस्वीर ही इसे बेहतर बना सकती है।
- मैं बहुत दुखी हूँ। मुझे एक [बिल्ली](समूह: बिल्लियों) तस्वीर चाहिए।
- अत्यधिक दुखी। केवल सुंदर [कुत्ते](समूह: शिब्स) तस्वीरें मुझे बेहतर महसूस करा सकती हैं।
- खराब। कृपया मुझे एक [पक्षी](समूह:पक्षी) चित्र दिखाएं!
- ईमानदार होना बहुत बुरा है। क्या आप मुझे [पिल्ला](ग्रुप:शिब्स) की तस्वीर दिखा सकते हैं जिससे मैं बेहतर तरीके से गिर सकूं?

## intent: query
- क्या तुम परजीवी हो?
- क्या आप इंसान हैं?
- क्या मैं किसी बॉट से बात कर रहा हूँ?
- क्या मैं एक इंसान से बात कर रहा हूँ?
- आप मेरे लिए क्या कर सकते हैं
- आप किस तरह मेरी सहायता कर सकते हैं
- तुम क्या कर सकते हो
- आप क्या मदद दे सकते हैं
- मुझे आपसे क्या उम्मीद करनी चाहिए

## intent:inform
- [AB-123](alphanumeric)
- [AB_1234567](alphanumeric)
- [AB_AB_1234567](alphanumeric)
- [1234567AB](alphanumeric)
- [ABC-123](alphanumeric)
- [abc@xyz.com](email_entity_name)
- [abc111@xffyz.com](email_entity_name)
- [0160 1234567](number)
- [0161 9876543](number)
- [0151 1234567](number)
- [0167 8765432](number)

## regex:email_entity_name
- (?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])

## regex:alphanumeric
- \b[A-Z]{1,3}[_-]?([A-Z]{1,2})?[_-]?\d{3,7}\b
- \b\d{7}[A-Z]{1,2}\b

## regex:number
- \b\d{1,}\b