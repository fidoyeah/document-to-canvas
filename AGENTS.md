# Document to Canvas - Implementation Guide (主题式)

## Task Description

将文档转换为**主题驱动**的Canvas思维导图，聚焦核心思想、理论框架和实践方法，而非简单罗列章节。

## Output Directories

- **书籍**: `YOURPATH/书/`（将 `YOURPATH` 替换为包含 `书` 与 `文章` 的目录，或设置 `DOCUMENT_TO_CANVAS_OUTPUT_BASE`）
- **文章**: `YOURPATH/文章/`

## 核心转变：从"章节罗列"到"主题提取"

### ❌ 旧的章节导向
```
[中心] 书名
    ├─ [第一章] 引言
    ├─ [第二章] 概念A
    ├─ [第三章] 概念B
    └─ ... (读者迷失在结构中)
```

### ✅ 新的主题导向
```
                    [核心命题]
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   [问题诊断]        [理论框架]        [实践工具]
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
   [常见误区] ──────── [行动方案] ──────── [效果评估]
```

## Implementation Steps

### Step 1: Deep Content Analysis (深度内容分析)

不是简单提取章节标题，而是深度理解内容：

#### 1.1 识别核心命题
Ask these questions while reading:
- 如果全书只能记住一句话，是什么？
- 作者最想改变读者的什么认知？
- 这本书与同类书的本质区别？

**提取方法**:
```python
def extract_core_proposition(content):
    """从全文中提取核心命题"""
    # 寻找关键句型
    patterns = [
        r'这本书的核心.*?是',
        r'关键.*?(?:在于|是)',
        r'颠覆.*?(?:认知|观念)',
        r'本质.*?(?:区别|不同)',
        r'核心.*?(?:观点|思想|主张)',
    ]
    
    # 寻找重复出现的主题词
    # 寻找结论部分的核心总结
    # 寻找推荐语/序言中的评价
    
    return core_proposition
```

#### 1.2 提取理论框架
寻找以下内容：
- 对比表格（A vs B）
- 流程图描述（步骤1→步骤2→步骤3）
- 层级结构（金字塔、矩阵）
- 自创术语和定义
- 数学公式或模型

**提取方法**:
```python
def extract_frameworks(content):
    """提取理论框架"""
    frameworks = []
    
    # 寻找对比表格
    table_patterns = [
        r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',  # Markdown表格
        r'(?:vs\.?|versus|对比|区别).*?[:：]',
    ]
    
    # 寻找流程描述
    process_patterns = [
        r'步骤\s*\d+',
        r'(?:第一|第二|第三|首先|然后|最后)',
        r'流程.*?[:：]',
    ]
    
    # 寻找自创术语
    # 大写术语或加引号的特殊概念
    
    return frameworks
```

#### 1.3 识别关键概念
选择标准：
- 出现频率高
- 有明确定义
- 与其他概念有关联
- 有实践指导意义

**概念提取模板**:
```json
{
  "concept_name": "概念名称",
  "definition": "一句话定义",
  "importance": "为什么重要",
  "application": "如何应用",
  "example": "具体案例",
  "misconception": "常见误解澄清"
}
```

#### 1.4 提取实践工具
寻找：
- 检查清单（checkbox items）
- 对话/邮件模板
- 步骤清单
- 计算公式
- 工具推荐

**工具分类**:
```python
tools_categories = {
    "templates": ["邮件模板", "对话脚本", "文案框架"],
    "checklists": ["检查清单", "步骤清单", "验证标准"],
    "frameworks": ["决策框架", "分析模型", "评估标准"],
    "resources": ["推荐工具", "延伸阅读", "相关资源"]
}
```

### Step 2: 生成主题式Canvas

#### 2.1 创建中心节点 - 核心命题

```python
center_node = {
    "id": generate_id(),
    "type": "text",
    "x": 500,
    "y": 400,
    "width": 400,
    "height": 180,
    "text": f"""# {title}

**核心命题**
{core_proposition}

💡 适用人群：{target_audience}

🎯 预期效果：{expected_outcome}""",
    "color": "6"  # 紫色 - 中心
}
```

#### 2.2 创建六大主题节点

按照六象限布局：

```python
# 象限布局坐标
quadrants = {
    "problem": {"x": 50, "y": 50, "color": "1"},      # 左上 - 红色
    "framework": {"x": 950, "y": 50, "color": "2"},   # 右上 - 橙色
    "concept": {"x": 50, "y": 400, "color": "3"},     # 左中 - 黄色
    "tools": {"x": 950, "y": 400, "color": "4"},      # 右中 - 绿色
    "mistakes": {"x": 50, "y": 780, "color": "1"},    # 左下 - 红色
    "action": {"x": 950, "y": 780, "color": "5"},     # 右下 - 青色
    "resources": {"x": 500, "y": 1100, "color": "5"}  # 底部 - 青色
}
```

#### 2.3 问题诊断节点

```python
problem_node = {
    "id": generate_id(),
    "type": "text",
    "x": 50,
    "y": 50,
    "width": 380,
    "height": 300,
    "text": """## 🎯 问题诊断

**你是否有这些困扰？**

{symptoms_checklist}

**根本原因分析**
{root_causes}

**转变方向**
❌ {old_mindset}
✅ {new_mindset}""",
    "color": "1"
}
```

#### 2.4 理论框架节点

```python
framework_node = {
    "id": generate_id(),
    "type": "text",
    "x": 950,
    "y": 50,
    "width": 400,
    "height": 350,
    "text": """## 🏗️ 核心理论框架

### {framework_name}

{framework_description}

**核心对比**
| {dimension} | {concept_a} | {concept_b} |
|------------|------------|------------|
{comparison_table}

**公式/模型**
{formula}

**学术基础**
{academic_basis}""",
    "color": "2"
}
```

#### 2.5 关键概念节点（可多个）

```python
def create_concept_node(concept, index, x, y):
    """创建关键概念节点"""
    return {
        "id": generate_id(),
        "type": "text",
        "x": x,
        "y": y,
        "width": 350,
        "height": 280,
        "text": f"""## 💡 关键概念 {index}：{concept['name']}

**定义**
{concept['definition']}

**为什么重要**
{concept['importance']}

**如何识别**
{concept['identification']}

**实践应用**
{concept['application']}

**常见误解**
❌ {concept['misconception']}
✅ {concept['clarification']}""",
        "color": "3"
    }
```

#### 2.6 实践工具节点

```python
tools_node = {
    "id": generate_id(),
    "type": "text",
    "x": 950,
    "y": 400,
    "width": 380,
    "height": 400,
    "text": """## 🛠️ 实践工具箱

### 工具1：{tool_name_1}
{tool_description_1}

**使用场景**：{usage_scenario_1}
**操作步骤**：
{step_by_step_1}

---

### 工具2：{tool_name_2}
{tool_description_2}

**模板**：
```
{template}
```

---

### 检查清单
- [ ] {checklist_item_1}
- [ ] {checklist_item_2}
- [ ] {checklist_item_3}""",
    "color": "4"
}
```

#### 2.7 常见误区节点

```python
mistakes_node = {
    "id": generate_id(),
    "type": "text",
    "x": 50,
    "y": 780,
    "width": 380,
    "height": 280,
    "text": """## ⚠️ 常见误区

### 误区1：{mistake_1}
**错误认知**：{wrong_belief_1}
**现实情况**：{reality_1}
**纠正方法**：{correction_1}

### 误区2：{mistake_2}
**错误认知**：{wrong_belief_2}
**现实情况**：{reality_2}
**纠正方法**：{correction_2}

### 误区3：{mistake_3}
**错误认知**：{wrong_belief_3}
**现实情况**：{reality_3}
**纠正方法**：{correction_3}""",
    "color": "1"
}
```

#### 2.8 行动方案节点

```python
action_node = {
    "id": generate_id(),
    "type": "text",
    "x": 950,
    "y": 780,
    "width": 380,
    "height": 300,
    "text": """## 🚀 30天行动方案

### Week 1：{week1_theme}
- [ ] {week1_task_1}
- [ ] {week1_task_2}
- [ ] {week1_task_3}

### Week 2：{week2_theme}
- [ ] {week2_task_1}
- [ ] {week2_task_2}
- [ ] {week2_task_3}

### Week 3：{week3_theme}
- [ ] {week3_task_1}
- [ ] {week3_task_2}
- [ ] {week3_task_3}

### Week 4：{week4_theme}
- [ ] {week4_task_1}
- [ ] {week4_task_2}
- [ ] {week4_task_3}

**成功指标**：{success_metrics}""",
    "color": "5"
}
```

#### 2.9 延伸阅读节点

```python
resources_node = {
    "id": generate_id(),
    "type": "text",
    "x": 500,
    "y": 1100,
    "width": 400,
    "height": 180,
    "text": """## 📚 延伸阅读与资源

**关联书籍**
- 《{related_book_1}》({relevance_1})
- 《{related_book_2}》({relevance_2})

**实践工具**
- {tool_link_1}
- {tool_link_2}

**进阶主题**
- {advanced_topic_1}
- {advanced_topic_2}""",
    "color": "5"
}
```

### Step 3: 创建逻辑连接线

连接线应该展示**逻辑关系**，而非简单结构：

```python
edges = [
    # 问题 → 需要框架解决
    {
        "id": generate_id(),
        "fromNode": problem_node_id,
        "toNode": framework_node_id,
        "fromSide": "right",
        "toSide": "left",
        "label": "需要用...解决"
    },
    
    # 框架 → 由概念支撑
    {
        "id": generate_id(),
        "fromNode": framework_node_id,
        "toNode": concept_node_id,
        "fromSide": "bottom",
        "toSide": "top",
        "label": "建立在...之上"
    },
    
    # 概念 → 转化为工具
    {
        "id": generate_id(),
        "fromNode": concept_node_id,
        "toNode": tools_node_id,
        "fromSide": "right",
        "toSide": "left",
        "label": "转化为"
    },
    
    # 工具 → 避免误区
    {
        "id": generate_id(),
        "fromNode": tools_node_id,
        "toNode": mistakes_node_id,
        "fromSide": "bottom",
        "toSide": "top",
        "label": "同时避免"
    },
    
    # 行动方案 ← 所有要素的汇聚
    {
        "id": generate_id(),
        "fromNode": center_node_id,
        "toNode": action_node_id,
        "fromSide": "bottom",
        "toSide": "top",
        "label": "落地为"
    }
]
```

### Step 4: 保存文件

```python
def save_canvas(canvas_data, title, is_book=True):
    """保存Canvas文件"""
    clean_title = clean_filename(title)
    suffix = "_主题框架" if is_book else "_核心洞见"
    
    output_base = os.environ.get("DOCUMENT_TO_CANVAS_OUTPUT_BASE", "YOURPATH")
    if is_book:
        output_dir = os.path.join(output_base, "书") + os.sep
    else:
        output_dir = os.path.join(output_base, "文章") + os.sep
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{clean_title}{suffix}.canvas")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(canvas_data, f, ensure_ascii=False, indent=2)
    
    return output_path
```

## Quality Validation

转换完成后必须检查：

### ✅ 内容质量
- [ ] 是否能用一句话概括核心命题？
- [ ] 是否识别了至少1个理论框架？
- [ ] 是否提取了3-5个关键概念？
- [ ] 每个概念是否包含定义、应用、案例？
- [ ] 是否提供了立即可用的工具模板？
- [ ] 是否指出了3个以上常见误区？
- [ ] 是否有具体的30天行动方案？

### ✅ 结构质量
- [ ] 节点之间是否有逻辑关联（非简单罗列）？
- [ ] 连接线是否展示了因果关系？
- [ ] 是否适合快速浏览（标题清晰）？
- [ ] 是否便于实践应用（有checklist）？

### ✅ 技术质量
- [ ] JSON格式有效
- [ ] 所有ID唯一
- [ ] 所有连接引用有效
- [ ] 文件保存成功

## Example Workflow

### Input: Reverse the Search

### Step 1: 深度分析

**核心命题**：
从被动求职者转变为主动工作购物者，通过个人品牌建设、精准人脉策略和价值展示，实现薪资增长与职业安全。

**理论框架**：
1. 求职者 vs 购物者 光谱模型
2. 职业安全金字塔（技能+人脉+可见度）

**关键概念**：
1. 弱关系的力量
2. 简历中的价值展示（非经历罗列）
3. 面试中的合作关系
4. 职业安全（非工作安全）

**实践工具**：
- LinkedIn优化清单
- 人脉建设脚本模板
- 面试中的价值展示话术
- 薪资谈判框架

**常见误区**：
1. 降低目标更容易
2. 学历决定竞争力
3. 海投提高概率

**行动方案**：
30天从求职者到购物者的转变计划

### Step 2: 生成Canvas

（按照上述节点模板生成）

### Step 3: 验证质量

- ✅ 一句话概括核心
- ✅ 识别了理论框架
- ✅ 提取了4个关键概念
- ✅ 提供了实用工具
- ✅ 指出了3个误区
- ✅ 有30天行动方案

## Best Practices

1. **深度优于广度**：宁可深挖3个概念，不要罗列10个章节
2. **连接胜于堆砌**：展示概念间的因果关系
3. **行动胜于认知**：每个理论都配套实践方法
4. **反直觉优于常识**：突出颠覆性观点
5. **视觉化优于文字**：使用表格、清单、流程图
6. **用户中心**：始终问"读者能用它来做什么？"
