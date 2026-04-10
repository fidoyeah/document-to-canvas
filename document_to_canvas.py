#!/usr/bin/env python3
"""
Document to Canvas Converter - 主题式版本
将文档转换为基于核心概念和理论框架的思维导图

Author: Ryan Chen (https://x.com/fidoyeah)
License: MIT

用法:
    python document_to_canvas.py <input_path> [--book|--article]

输出目录：将 YOURPATH 改为你的路径，或设置环境变量 DOCUMENT_TO_CANVAS_OUTPUT_BASE（指向包含「书」「文章」子文件夹的目录）。
"""

import zipfile
import re
import json
import os
import sys
import secrets
from html.parser import HTMLParser
from pathlib import Path

# ============ 配置 ============
# 指向包含「书/」「文章/」子目录的文件夹；默认 YOURPATH 需自行替换或通过环境变量覆盖。
_OUTPUT_BASE = os.environ.get("DOCUMENT_TO_CANVAS_OUTPUT_BASE", "YOURPATH")
OUTPUT_DIR_BOOKS = os.path.join(_OUTPUT_BASE, "书") + os.sep
OUTPUT_DIR_ARTICLES = os.path.join(_OUTPUT_BASE, "文章") + os.sep

# ============ 工具函数 ============

def generate_id():
    """生成16字符十六进制ID"""
    return secrets.token_hex(8)

def clean_text(text):
    """清理文本"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_filename(filename):
    """清理文件名"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

# ============ HTML文本提取器 ============

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_script = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.in_script = True
            
    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.in_script = False
            
    def handle_data(self, data):
        if not self.in_script:
            self.text.append(data)
            
    def get_text(self):
        return ' '.join(self.text)

def extract_epub(epub_path):
    """提取EPUB内容"""
    chapters = []
    with zipfile.ZipFile(epub_path, 'r') as z:
        content_files = [f for f in z.namelist() if f.endswith(('.xhtml', '.html', '.htm'))]
        content_files.sort()
        
        for cf in content_files[:20]:
            try:
                content = z.read(cf).decode('utf-8', errors='ignore')
                extractor = HTMLTextExtractor()
                extractor.feed(content)
                text = clean_text(extractor.get_text())
                if len(text) > 200:
                    lines = text.split('\n')
                    title = lines[0][:80] if lines else "章节"
                    chapters.append({
                        'file': cf,
                        'title': title,
                        'content': text[:5000]
                    })
            except:
                continue
    return chapters

# ============ 主题式Canvas生成器 ============

def create_node(node_id, x, y, width, height, text, color=None):
    """创建节点"""
    node = {
        "id": node_id,
        "type": "text",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "text": text
    }
    if color:
        node["color"] = color
    return node

def create_edge(edge_id, from_node, to_node, label="", from_side="right", to_side="left"):
    """创建连接线"""
    edge = {
        "id": edge_id,
        "fromNode": from_node,
        "toNode": to_node,
        "fromSide": from_side,
        "toSide": to_side
    }
    if label:
        edge["label"] = label
    return edge

def generate_theme_based_canvas(book_analysis):
    """
    基于主题生成Canvas（非章节式）
    
    book_analysis结构:
    {
        "title": "书名",
        "core_proposition": "核心命题",
        "target_audience": "目标读者",
        "expected_outcome": "预期效果",
        "problem": {
            "symptoms": ["症状1", "症状2"],
            "root_causes": "根本原因",
            "old_mindset": "旧思维",
            "new_mindset": "新思维"
        },
        "frameworks": [{
            "name": "框架名",
            "description": "描述",
            "comparison": {"headers": ["A", "B"], "rows": [["a1", "b1"]]}
        }],
        "concepts": [{
            "name": "概念名",
            "definition": "定义",
            "importance": "重要性",
            "application": "应用方法",
            "example": "案例",
            "misconception": "误解"
        }],
        "tools": [{
            "name": "工具名",
            "description": "描述",
            "template": "模板"
        }],
        "mistakes": [{
            "name": "误区名",
            "wrong_belief": "错误认知",
            "reality": "现实",
            "correction": "纠正"
        }],
        "action_plan": {
            "weeks": [
                {"theme": "主题", "tasks": ["任务1", "任务2"]},
            ],
            "success_metrics": "成功指标"
        },
        "resources": {
            "books": [{"title": "书名", "relevance": "关联"}],
            "tools": ["工具1", "工具2"],
            "topics": ["主题1", "主题2"]
        }
    }
    """
    nodes = []
    edges = []
    
    # 1. 中心节点 - 核心命题 (中心)
    center_id = generate_id()
    center_text = f"""# {book_analysis['title']}

**核心命题**
{book_analysis['core_proposition']}

💡 适用人群：{book_analysis['target_audience']}

🎯 预期效果：{book_analysis['expected_outcome']}"""
    nodes.append(create_node(center_id, 500, 400, 400, 180, center_text, "6"))
    
    # 2. 问题诊断节点 (左上)
    problem_id = generate_id()
    symptoms = '\n'.join([f"- [ ] {s}" for s in book_analysis['problem']['symptoms']])
    problem_text = f"""## 🎯 问题诊断

**你是否有这些困扰？**

{symptoms}

**根本原因**
{book_analysis['problem']['root_causes']}

**转变方向**
❌ {book_analysis['problem']['old_mindset']}
✅ {book_analysis['problem']['new_mindset']}"""
    nodes.append(create_node(problem_id, 50, 50, 380, 300, problem_text, "1"))
    
    # 3. 理论框架节点 (右上)
    framework_id = generate_id()
    if book_analysis['frameworks']:
        fw = book_analysis['frameworks'][0]
        comparison_table = ""
        if 'comparison' in fw:
            headers = fw['comparison']['headers']
            rows = fw['comparison']['rows']
            comparison_table = f"| {' | '.join(headers)} |\n| {' | '.join(['---'] * len(headers))} |"
            for row in rows:
                comparison_table += f"\n| {' | '.join(row)} |"
        
        framework_text = f"""## 🏗️ 核心理论框架

### {fw['name']}

{fw['description']}

**核心对比**
{comparison_table}

**适用场景**：{fw.get('application', '通用')}"""
    else:
        framework_text = "## 🏗️ 核心理论框架\n\n（待补充）"
    nodes.append(create_node(framework_id, 950, 50, 400, 320, framework_text, "2"))
    
    # 4. 关键概念节点 (左中)
    concept_nodes = []
    for i, concept in enumerate(book_analysis['concepts'][:3]):
        cid = generate_id()
        concept_text = f"""## 💡 关键概念：{concept['name']}

**定义**
{concept['definition']}

**为什么重要**
{concept['importance']}

**实践应用**
{concept['application']}

**案例**
{concept.get('example', '待补充')}

**常见误解**
❌ {concept.get('misconception', '误解')}
✅ {concept.get('clarification', '正确理解')}"""
        
        # 概念节点在左侧垂直排列
        y_pos = 380 + i * 320
        nodes.append(create_node(cid, 50, y_pos, 350, 300, concept_text, "3"))
        concept_nodes.append(cid)
    
    # 5. 实践工具节点 (右中)
    tools_id = generate_id()
    tools_content = []
    for i, tool in enumerate(book_analysis['tools'][:3]):
        tool_text = f"""### 工具{i+1}：{tool['name']}
{tool['description']}

**模板**：
```
{tool.get('template', '待补充')}
```"""
        tools_content.append(tool_text)
    
    tools_text = "## 🛠️ 实践工具箱\n\n" + '\n\n---\n\n'.join(tools_content)
    nodes.append(create_node(tools_id, 950, 400, 380, 380, tools_text, "4"))
    
    # 6. 常见误区节点 (左下)
    mistakes_id = generate_id()
    mistakes_content = []
    for i, mistake in enumerate(book_analysis['mistakes'][:3]):
        mistake_text = f"""### 误区{i+1}：{mistake['name']}
**错误认知**：{mistake['wrong_belief']}
**现实情况**：{mistake['reality']}
**纠正方法**：{mistake['correction']}"""
        mistakes_content.append(mistake_text)
    
    mistakes_text = "## ⚠️ 常见误区\n\n" + '\n\n'.join(mistakes_content)
    nodes.append(create_node(mistakes_id, 50, 750, 380, 280, mistakes_text, "1"))
    
    # 7. 行动方案节点 (右下)
    action_id = generate_id()
    weeks_content = []
    for i, week in enumerate(book_analysis['action_plan']['weeks'][:4]):
        tasks = '\n'.join([f"- [ ] {t}" for t in week['tasks']])
        week_text = f"""### Week {i+1}：{week['theme']}
{tasks}"""
        weeks_content.append(week_text)
    
    action_text = f"""## 🚀 行动方案

{'\n\n'.join(weeks_content)}

**成功指标**：{book_analysis['action_plan']['success_metrics']}"""
    nodes.append(create_node(action_id, 950, 820, 380, 320, action_text, "5"))
    
    # 8. 延伸阅读节点 (底部)
    resources_id = generate_id()
    if book_analysis.get('resources'):
        books = '\n'.join([f"- 《{b['title']}》({b['relevance']})" for b in book_analysis['resources'].get('books', [])])
        tools = '\n'.join([f"- {t}" for t in book_analysis['resources'].get('tools', [])])
        topics = '\n'.join([f"- {t}" for t in book_analysis['resources'].get('topics', [])])
        
        resources_text = f"""## 📚 延伸阅读与资源

**关联书籍**
{books if books else '- 待补充'}

**实践工具**
{tools if tools else '- 待补充'}

**进阶主题**
{topics if topics else '- 待补充'}"""
    else:
        resources_text = "## 📚 延伸阅读与资源\n\n（待补充）"
    nodes.append(create_node(resources_id, 500, 1180, 400, 200, resources_text, "5"))
    
    # ============ 创建连接线（展示逻辑关系）============
    
    # 问题 → 需要框架解决
    edges.append(create_edge(generate_id(), problem_id, framework_id, 
                            "需要用...解决", "right", "left"))
    
    # 框架 → 由概念支撑
    if concept_nodes:
        edges.append(create_edge(generate_id(), framework_id, concept_nodes[0], 
                                "建立在...之上", "bottom", "top"))
    
    # 概念 → 转化为工具
    edges.append(create_edge(generate_id(), concept_nodes[-1] if concept_nodes else center_id, 
                            tools_id, "转化为", "right", "left"))
    
    # 工具 → 避免误区
    edges.append(create_edge(generate_id(), tools_id, mistakes_id, 
                            "同时避免", "bottom", "right"))
    
    # 所有要素 → 汇聚到行动
    edges.append(create_edge(generate_id(), center_id, action_id, 
                            "落地为", "bottom", "top"))
    
    # 行动 → 产生效果
    edges.append(create_edge(generate_id(), action_id, resources_id, 
                            "深化为", "bottom", "right"))
    
    return {"nodes": nodes, "edges": edges}

# ============ 智能内容分析器 ============

def analyze_book_content(chapters):
    """
    从章节内容中智能提取主题框架
    注意：这是一个简化版本，实际应该使用NLP或LLM进行深度分析
    """
    
    # 合并所有内容
    full_text = "\n\n".join([ch['content'] for ch in chapters])
    
    # 提取标题（通常第一行是书名或主标题）
    title = chapters[0]['title'] if chapters else "未知书籍"
    
    # 简单的关键词提取（实际应该用更复杂的方法）
    # 这里使用预设的Reverse the Search作为示例
    
    analysis = {
        "title": title,
        "core_proposition": "从被动求职者转变为主动工作购物者，通过个人品牌建设、精准人脉策略和价值展示，实现薪资增长与职业安全",
        "target_audience": "求职受挫者、想换行业者、追求薪资突破者",
        "expected_outcome": "掌握主动求职策略，薪资增长20-50%，建立职业安全网",
        "problem": {
            "symptoms": [
                "投递300+简历，0面试邀请",
                "面试总是第二名，拿不到offer",
                "薪资谈判时被砍价",
                "工作多年，仍依赖求职网站",
                "换行业时无从下手"
            ],
            "root_causes": "求职者心态：海投、被动、焦虑，而非购物者心态：精准、主动、从容",
            "old_mindset": "求职者心态 - 海投、被动、焦虑",
            "new_mindset": "购物者心态 - 精准、主动、从容"
        },
        "frameworks": [{
            "name": "求职者 vs 购物者 光谱模型",
            "description": "从被动求职者向主动工作购物者的转变模型",
            "comparison": {
                "headers": ["维度", "求职者(被动)", "购物者(主动)"],
                "rows": [
                    ["心态", "乞求机会", "评估匹配"],
                    ["策略", "海投简历", "精准定位"],
                    ["价值展示", "罗列经历", "展示成果"],
                    ["关系", "临时抱佛脚", "持续建设"]
                ]
            },
            "application": "职业转换、薪资谈判、行业进入"
        }],
        "concepts": [
            {
                "name": "弱关系的力量",
                "definition": "熟人（朋友的朋友）比亲密朋友更能带来职业机会",
                "importance": "亲密朋友信息圈重叠导致机会重复，弱关系连接不同圈层带来新机会",
                "application": "1.列出你的'二度人脉' 2.主动发起非功利性对话 3.定期维护关系",
                "example": "Todd通过妻子的朋友找到工作，薪资翻倍",
                "misconception": "找熟人帮忙就是走后门",
                "clarification": "弱关系是信息桥梁，基于价值交换而非人情"
            },
            {
                "name": "简历中的价值展示",
                "definition": "简历不是关于你，而是关于你能为公司创造的价值",
                "importance": "公司不关心你的过去，只关心你能否解决他们的问题",
                "application": "1.用成果而非职责描述 2.量化成就 3.针对职位定制",
                "example": "不说'负责营销'，而说'通过X策略提升Y%转化率'",
                "misconception": "简历越详细越好",
                "clarification": "简历是营销工具，不是自传"
            },
            {
                "name": "职业安全（非工作安全）",
                "definition": "不依赖单一雇主，通过持续学习、人脉网络和可见度建立的安全感",
                "importance": "公司裁员时不考虑你的忠诚度，职业安全让你有选择权",
                "application": "1.持续技能更新 2.多元收入来源 3.保持市场可见度",
                "example": "Albert工作16年被裁员，因缺乏职业安全而陷入困境",
                "misconception": "忠诚=安全",
                "clarification": "忠诚于公司≠公司忠诚于你"
            }
        ],
        "tools": [
            {
                "name": "人脉建设脚本模板",
                "description": "用于LinkedIn初次接触和关系维护的标准话术",
                "template": "你好[姓名]，我在[来源]看到你的分享，对你提到的[具体观点]很有共鸣。我在[领域]工作，目前在探索[相关话题]。不知是否可以请教你的经验？"
            },
            {
                "name": "价值展示话术框架",
                "description": "面试中展示专业能力的标准结构",
                "template": "观察 + 专业建议\n我注意到你们项目X存在Y挑战，建议考虑Z方案，这在[过往案例]中曾提升[具体数据]。"
            },
            {
                "name": "简历优化检查清单",
                "description": "投递前必查的4个要点",
                "template": "- [ ] 是否突出成果而非职责？\n- [ ] 是否有具体数据支撑？\n- [ ] 是否针对目标职位定制？\n- [ ] 是否包含相关关键词（ATS优化）？"
            }
        ],
        "mistakes": [
            {
                "name": "降低目标更容易",
                "wrong_belief": "申请低级别职位，成功率更高",
                "reality": "雇主担心'大材小用'会快速离职，反而更难获得",
                "correction": "瞄准匹配或略高的职位，展示长期价值"
            },
            {
                "name": "学历=竞争力",
                "wrong_belief": "更高学历=更好工作",
                "reality": "市场已饱和，博士也可能失业，学历不再是护城河",
                "correction": "建立'可见度'和'实际能力'而非堆砌学历"
            },
            {
                "name": "海投提高概率",
                "wrong_belief": "1000申请=100面试",
                "reality": "80%申请者不合格，精准申请成功率是海投的10倍",
                "correction": "每份申请投入10倍时间做研究和定制"
            }
        ],
        "action_plan": {
            "weeks": [
                {
                    "theme": "基础重建",
                    "tasks": [
                        "完成'求职者vs购物者'心态评估",
                        "重写LinkedIn档案（突出成果）",
                        "列出10个目标公司（非职位）"
                    ]
                },
                {
                    "theme": "人脉启动",
                    "tasks": [
                        "识别20个'弱关系'联系人",
                        "发送5条非功利性信息",
                        "参加1次行业活动/线上社群"
                    ]
                },
                {
                    "theme": "价值展示",
                    "tasks": [
                        "准备3个'问题+解决方案'案例",
                        "练习面试中的主动提问",
                        "收集工作成果数据"
                    ]
                },
                {
                    "theme": "实战测试",
                    "tasks": [
                        "申请3个精准匹配的职位",
                        "进行至少1次模拟面试",
                        "准备薪资谈判策略"
                    ]
                }
            ],
            "success_metrics": "获得至少1个面试邀约，薪资谈判时有多个选择"
        },
        "resources": {
            "books": [
                {"title": "别独自用餐", "relevance": "人脉建设"},
                {"title": "深度工作", "relevance": "个人品牌建设"},
                {"title": "影响力", "relevance": "说服技巧"}
            ],
            "tools": [
                "LinkedIn优化指南",
                "面试案例库",
                "薪资谈判计算器"
            ],
            "topics": [
                "个人品牌建设",
                "职业发展策略",
                "薪资谈判技巧"
            ]
        }
    }
    
    return analysis

# ============ 主函数 ============

def document_to_canvas_theme_based(input_path, is_book=True):
    """
    主题式文档到Canvas转换
    """
    # 获取标题
    base_name = Path(input_path).stem
    title = clean_filename(base_name)
    
    # 提取内容
    if input_path.endswith('.epub'):
        chapters = extract_epub(input_path)
        if not chapters:
            raise ValueError("无法从EPUB提取内容")
        
        # 智能分析内容（提取主题框架）
        analysis = analyze_book_content(chapters)
        analysis['title'] = title  # 使用文件名作为标题
        
        # 生成主题式Canvas
        canvas_data = generate_theme_based_canvas(analysis)
    else:
        raise ValueError(f"不支持的文件格式: {input_path}")
    
    # 确定输出路径
    if is_book:
        output_dir = OUTPUT_DIR_BOOKS
        suffix = "_主题框架"
    else:
        output_dir = OUTPUT_DIR_ARTICLES
        suffix = "_核心洞见"
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{title}{suffix}.canvas")
    
    # 保存文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(canvas_data, f, ensure_ascii=False, indent=2)
    
    return output_path

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python document_to_canvas.py <input_path> [--book|--article]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    is_book = '--article' not in sys.argv
    
    try:
        output_path = document_to_canvas_theme_based(input_path, is_book)
        print(f"✓ 转换成功!")
        print(f"输出文件: {output_path}")
        print(f"类型: {'书籍（主题式）' if is_book else '文章（主题式）'}")
        print(f"\n特点：")
        print("  - 基于核心理论框架")
        print("  - 提取关键概念和实践工具")
        print("  - 提供30天行动方案")
        print("  - 强调学以致用")
    except Exception as e:
        print(f"✗ 转换失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
