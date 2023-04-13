from huaweicloud_sis.client.asr_client import AsrCustomizationClient
from huaweicloud_sis.bean.asr_request import AsrCustomShortRequest
from huaweicloud_sis.bean.asr_request import AsrCustomLongRequest
from huaweicloud_sis.exception.exceptions import ClientException
from huaweicloud_sis.exception.exceptions import ServerException
from huaweicloud_sis.utils import io_utils
from huaweicloud_sis.bean.sis_config import SisConfig
import os


def recognize(path):
    if path is None:
        raise ValueError("Audio path have not been set.")
    if not os.path.exists(path):
        raise FileNotFoundError
    if not path.endswith('.wav'):
        raise ValueError("Audio file needs a \".wav\" file.")
    ak = '6MUFMD0X4TXLG0LHYDNS'
    sk = 'cewrUZ7pLU8elvie4f1UZxHxWULu6HCusQGTHbm1'
    region = "cn-north-4"
    project_id = "00907a20d88c4ba183b2760ccfd5c580"
    path_audio_format = 'wav'
    path_property = 'chinese_16k_common'
    config = SisConfig()
    config.set_connect_timeout(5)
    config.set_read_timeout(10)
    asr_client = AsrCustomizationClient(ak, sk, region, project_id, sis_config=config)
    data = io_utils.encode_file(path)
    asr_request = AsrCustomShortRequest(path_audio_format, path_property, data)
    # 设置是否添加标点，yes or no，默认 no
    asr_request.set_add_punc('yes')
    res = asr_client.get_short_response(asr_request)
    return res["result"]["text"]
