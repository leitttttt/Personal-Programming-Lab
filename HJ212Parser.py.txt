import binascii

class HJ212Parser:
    def __init__(self):
        pass

    def is_valid_message(self, message):
        # 检查格式：##开头，\r\n结尾，长度字段是否正确
        if not message.startswith('##') or not message.endswith('\r\n'):
            return False
        # 提取长度（第3位到第6位，共4位）
        try:
            length = int(message[2:6])
            data_segment = message[6:-6]  # 数据段
            return len(data_segment) == length
        except:
            return False

    def validate_crc(self, message):
        # 校验CRC16（ANSI标准）
        if len(message) < 12:
            return False
        # 提取报文中的数据部分（##之后，CRC之前的全部）
        data_to_check = message[2:-6].encode('utf-8')
        # 提取报文末尾的4位CRC值
        provided_crc = message[-6:-2]
        
        crc = 0xFFFF
        for byte in data_to_check:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        # 将计算的CRC与报文中的对比（16进制，大写）
        return format(crc, '04X') == provided_crc.upper()

    def parse_data_segment(self, message):
        # 解析数据段，返回字典
        data_segment = message[6:-6]
        result = {}
        for item in data_segment.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                result[key] = value
        return result

    def extract_monitoring_data(self, message):
        # 从CP字段提取监测因子
        data = self.parse_data_segment(message)
        cp_data = data.get('CP', '')
        if cp_data.startswith('&&') and cp_data.endswith('&&'):
            cp_data = cp_data[2:-2]
        
        monitoring_data = {}
        # CP格式：因子编码-Rtd=值,因子编码-Flag=标志
        for item in cp_data.split(','):
            if '=' in item:
                key, value = item.split('=', 1)
                if '-Rtd' in key:
                    factor_code = key.split('-')[0]
                    monitoring_data[factor_code] = value
        return monitoring_data