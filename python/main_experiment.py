import json
import requests
from openai import OpenAI

# ================= 配置区 =================
DEEPSEEK_API_KEY = "sk-808502f2dd294d70b893be74a614a6c5"
GAODE_API_KEY = "2b01faf1437313a9819a6885fd665e0b"
# ==========================================

# 1. 初始化 DeepSeek
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


# 2. 定义提取函数 (AI)
def extract_addresses_by_ai(text):
    print(f"正在使用AI分析文本: {text[:20]}...")
    prompt = """
    请提取文本中所有的详细地址。
    要求：
    1. 仅输出一个 JSON 格式的字符串列表 (List[str])。
    2. 不要包含 Markdown 格式（如 ```json）。
    3. 如果没有地址，返回空列表 []。
    文本：
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role":"system","content":"你是一个严谨的数据提取助手。"},{"role":"user","content":prompt + text}],
            temperature=0.1
        )
        content = response.choices[0].message.content
        # 简单清洗一下，防止模型有时还是会加 Markdown
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except Exception as e:
        print(f"AI提取失败: {e}")
        return []


# 3. 定义坐标转换函数 (GIS)
def get_coordinate(address):
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {"key": GAODE_API_KEY, "address": address}
    res = requests.get(url, params=params).json()
    if res["status"] == "1" and res["count"] != "0":
        lon, lat = res["geocodes"][0]["location"].split(",")
        return float(lon), float(lat)
    return None


# ================= 主程序 =================
if __name__ == "__main__":
    # 模拟输入数据（你可以从新闻里复制一段真实的）
    input_text = "昨日，武汉光谷广场发生拥堵，随后交警前往关山大道保利广场进行疏导，并在华中科技大学南门设置了临时检查点。"

    # Step 1: AI 提取地址
    addresses = extract_addresses_by_ai(input_text)
    print(f"AI提取到的地址: {addresses}")

    # Step 2: 获取坐标
    results = []
    for addr in addresses:
        coord = get_coordinate(addr)
        if coord:
            results.append({"name": addr, "coord": coord})
            print(f"成功定位: {addr} -> {coord}")
        else:
            print(f"无法定位: {addr}")

    # Step 3: 输出最终结果（你可以把这个截图放到论文里）
    print("\n=== 最终结构化数据 ===")
    print(json.dumps(results, ensure_ascii=False, indent=2))