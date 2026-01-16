import requests
import json
import os

# --- 配置 ---
# Lothrik 的数据源 (通常包含翻译文件)
# 注意：实际 URL 可能会随仓库结构变化，需要定期检查。
# 这里我们假设利用他的 locale 文件，因为里面有中文翻译
SOURCE_URL = "https://raw.githubusercontent.com/lothrik/diablo4-build-calc/master/data/locales/zh_CN/data.json"

# 本地保存路径 (Uni-app 的 static 目录，方便前端读取)
OUTPUT_PATH = "../static/data/tempering_processed.json"

def fetch_and_process():
    print(f"🚀 开始抓取数据: {SOURCE_URL}")
    
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status() # 检查请求是否成功
        raw_data = response.json()
        
        print("✅ 原始数据下载成功，开始清洗...")

        # --- 数据清洗逻辑 (核心) ---
        # 假设 raw_data 里有一个 key 叫 "tempering_recipes" 或类似的结构
        # 注意：你需要先手动下载一次他的 json 看看具体结构，这里是伪代码逻辑
        
        processed_data = {
            "version": "Auto-Generated",
            "categories": []
        }

        # 模拟：如果找不到特定 key，就打印所有 keys 方便调试
        # 实际开发中，你需要根据 Lothrik 的真实结构修改下面的解析逻辑
        if "tempering_recipes" not in raw_data:
            print("⚠️ 警告：未找到 tempering_recipes，可能结构已变。Keys:", raw_data.keys())
            # 这里为了演示，我们假设数据在 root 或者某个 key 下
            # 实际情况可能是 raw_data['2']['tempering'] 等
            target_data = raw_data 
        else:
            target_data = raw_data["tempering_recipes"]

        # 示例转换逻辑：将复杂结构简化为前端好用的结构
        # for recipe_id, recipe_content in target_data.items():
        #     item = {
        #         "name": recipe_content.get("name"),
        #         "affixes": []
        #     }
        #     for affix in recipe_content.get("affixes", []):
        #         item["affixes"].append({
        #             "name": affix.get("description"),
        #             "weight": affix.get("weight", 100)
        #         })
        #     processed_data["categories"].append(item)
            
        # 暂时写入原始数据，方便你第一步调试
        processed_data = raw_data 

        # --- 保存文件 ---
        # 确保目录存在
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)
            
        print(f"🎉 数据已保存至: {OUTPUT_PATH}")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        exit(1) # 返回非0状态码，让 GitHub Action 报错

if __name__ == "__main__":
    fetch_and_process()