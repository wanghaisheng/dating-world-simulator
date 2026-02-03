# 现代都市恋爱模拟 - 改造实施计划文档

## 1. 引言

本文档旨在规划如何在现有的“修仙世界模拟器”架构基础上，通过模块化扩展和配置替换，实现“现代都市恋爱模拟”设定。
核心目标是将原本的“修仙证道”核心循环，转化为“职场生存 + 多线恋爱攻略”体验，同时利用 Git 分支策略保证原有功能的完整性。

## 2. Git 分支管理策略

*   **`main` (稳定分支)**: 保持原有的开放修仙世界设定，以及通用的引擎底层（模拟循环、事件系统、LLM 接口）。
*   **`feat/modern-romance` (特性分支)**: 
    *   基于 `main` 分支创建。
    *   实现现代都市特有的数据结构 (`ModernProfileMixin`)、地点配置和互动逻辑。
    *   **注意**: 此分支与 `feat/thousand-illusions` 是两个平行的世界观实现，互不依赖，但都依赖 `main` 的底层能力。

---

## 3. 代码与架构改造

### 3.1 全局模式控制

在 `src/config.py` 中扩展 `GameMode` 枚举：

```python
class GameMode(Enum):
    OPEN_WORLD = "open_world"            # 原修仙模式
    THOUSAND_ILLUSIONS = "thousand_illusions" # 千幻无情道
    MODERN_ROMANCE = "modern_romance"    # 现代都市恋爱
```

### 3.2 资源配置 (static/game_configs)

利用现有的 CSV 加载机制，创建一套新的配置文件（建议在 `static/game_configs/modern/` 目录下，或通过加载逻辑区分）：

*   **`world_info.csv` (World)**:
    *   定义城市区域：CBD (工作区), 大学城 (教育区), 老城区 (生活区), 网红商圈 (娱乐区)。
*   **`sect.csv` (Organization)**:
    *   定义组织：跨国集团, 创业公司, 综合医院, 艺术学院。
*   **`technique.csv` (Skill/Hobby)**:
    *   定义技能/兴趣：编程, 摄影, 烹饪, 瑜伽, 投资。
*   **`elixir.csv` (Gift/Item)**:
    *   定义物品：奢侈品包, 限量球鞋, 电影票, 爱心便当。
*   **`persona.csv`**:
    *   定义现代性格标签：傲娇, 腹黑, 治愈系, 社恐, E人。

### 3.3 角色数据模型扩展 (src/classes/avatar)

创建 `src/classes/avatar/modern_mixin.py`，实现 `ModernProfileMixin`：

```python
class ModernProfileMixin:
    # 基础社会属性
    occupation: str          # 职业 (程序员/医生/偶像...)
    salary: int              # 月薪
    assets: int              # 存款
    
    # 恋爱核心属性
    charm: int               # 魅力 (影响初次见面好感)
    energy: int              # 精力值 (每日行动点数)
    stress: int              # 压力值 (过高导致生病/崩溃)
    
    # 关系网 (Key: AvatarID, Value: RelationData)
    # 包含: affection (好感), dependency (依赖), jealousy (嫉妒)
    relationships: Dict[str, dict] 
    
    def get_dating_budget(self):
        """根据资产计算约会预算"""
        pass
```

### 3.4 模拟循环与时间系统 (src/sim)

*   **时间粒度调整**:
    *   修仙模式：`run_month()` (每月一次循环)。
    *   恋爱模式：`run_day()` (每日循环)，细分为 `DayPhase` (Morning/Afternoon/Evening/LateNight)。
*   **日程系统 (Schedule System)**:
    *   每个 NPC 生成每日日程表（例如：9:00-18:00 工作，19:00-21:00 健身）。
    *   玩家选择地点移动，如果地点与 NPC 日程重合，触发“偶遇”事件。

### 3.5 互动系统 (Interaction System)

新增 `src/systems/social_system.py`:

*   **Chat Engine (聊天引擎)**:
    *   生成微信/短信风格的对话。
    *   Prompt 需包含：当前好感度、历史话题、双方心情、潜台词指令。
*   **Dating Engine (约会引擎)**:
    *   处理约会邀请、场景选择、突发事件（如遇到熟人）。
    *   结算：根据约会表现更新好感度和依赖度。
*   **Conflict Engine (修罗场引擎)**:
    *   检测冲突：当玩家在已有伴侣的情况下与其他高好感 NPC 互动被发现。
    *   触发后果：降好感、进入“冷战”状态、触发“对质”剧情。

---

## 4. 实施步骤清单

### 阶段一：环境与数据准备
1.  [ ] 创建分支 `feat/modern-romance`。
2.  [ ] 建立 `static/game_configs/modern/` 目录，创建基础的城市、组织、物品 CSV 模板。
3.  [ ] 在 `src/config.py` 中注册 `MODERN_ROMANCE` 模式。

### 阶段二：角色与日程系统
1.  [ ] 实现 `ModernProfileMixin` 并集成到 `Avatar` 类。
2.  [ ] 实现 `ScheduleGenerator`：基于职业和性格生成 NPC 的周日程表。
3.  [ ] 改造 `Simulator`：在现代模式下切换为“日循环”逻辑，消耗 `energy` 执行行动。

### 阶段三：通讯与约会功能
1.  [ ] 开发 `ChatManager`：集成 LLM，支持生成“发送消息”和“回复消息”的内容。
    *   [ ] 编写 `templates/modern_chat.txt` Prompt 模板。
2.  [ ] 开发 `DateManager`：
    *   [ ] 实现地点互动逻辑（花钱/花精力 -> 获得好感/属性）。
    *   [ ] 实现邀约机制（成功率受好感度和心情影响）。

### 阶段四：修罗场与事件
1.  [ ] 实现 `ConflictSystem`：定义“撞车”判定逻辑和嫉妒值增长公式。
2.  [ ] 编写突发事件库（`static/game_configs/modern/events.json`），如“前任复合”、“被上司刁难”等。

### 阶段五：UI 与体验适配 (Web/Frontend)
1.  [ ] 前端增加“手机”界面：用于显示聊天记录、朋友圈。
2.  [ ] 调整主界面布局：显示精力条、金钱、日程表。

---

## 5. 关键技术难点与解决方案

### 5.1 聊天记录的连贯性
*   **问题**: LLM 容易忘记之前的聊天细节。
*   **方案**: 引入向量数据库 (如 ChromaDB 或简单的本地 JSON 索引) 存储关键聊天摘要 (`Summary`)，每次生成对话时检索相关历史作为 Context。

### 5.2 NPC 个性化差异
*   **问题**: 所有 NPC 说话像同一个 AI。
*   **方案**: 在 System Prompt 中强效注入 `Persona` (说话风格、口癖、常用表情包)，并在 `static/locales` 中预设不同性格的 Few-Shot 示例。

### 5.3 经济系统平衡
*   **问题**: 玩家可能通过“刷钱”导致恋爱难度降低。
*   **方案**: 引入“通货膨胀”机制（随着好感度提升，NPC 对礼物的要求变高）和“时间互斥”（赚钱必须消耗大量时间，导致没时间陪伴，好感自然下降）。

