from xiaoai import *
import random

def outputJson(toSpeakText, is_session_end, openMic=True):
    xiaoAIResponse=XiaoAIResponse(to_speak=XiaoAIToSpeak(type_=0, text=toSpeakText), open_mic=openMic)
    response = xiaoai_response(XiaoAIOpenResponse(version="1.0",
                                     is_session_end=is_session_end,
                                     response=xiaoAIResponse))
    return response

def main(event):
    req = xiaoai_request(event)
    
    if req.request.type == 0:
        return outputJson("欢迎来到随机数，你可以说随机一个数，或者 来一个10以内的随机数，或者 来个10到20之间的随机数", False)
    elif req.request.type == 1:
        if ((not hasattr(req.request, "slot_info")) or (not hasattr(req.request.slot_info, "intent_name"))):
            return outputJson("抱歉，我没有听懂", False)
        else:
            if req.request.slot_info.intent_name == 'random_any':
                return outputJson("您要的随机数是：" + str(random.randint(0,1000000)), False)
            elif req.request.slot_info.intent_name == 'random_range':
                slotsList = req.request.slot_info.slots
                maxValueList = [item for item in slotsList if item['name'] == 'numbermax']
                minValueList = [item for item in slotsList if item['name'] == 'numbermix']
                if len(maxValueList) == 0:
                    return outputJson("抱歉，缺少最大值，请重试", False)
                if len(minValueList) == 0:
                    return outputJson("抱歉，缺少最小值，请重试", False)
                maxValue = maxValueList[0].get('value', "")
                minValue = minValueList[0].get('value', "")

                if maxValue == '':
                    return outputJson("抱歉，缺少最大值，请重试", False)
                if minValue == '':
                    return outputJson("抱歉，缺少最小值，请重试", False)

                return outputJson("您要的随机数是：" + str(random.randint(int(minValue), int(maxValue))), False)
            elif req.request.slot_info.intent_name == 'random_range_max':
                slotsList = req.request.slot_info.slots
                maxValue = [item for item in slotsList if item['name'] == 'number'][0]['value']
                return outputJson("您要的随机数是：" + str(random.randint(0, int(maxValue))), False)
            else:
                return outputJson("抱歉，我没有听懂", False)
    else:
        return outputJson("感谢使用随机数，下次再见", True, False)

