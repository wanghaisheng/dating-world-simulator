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

在 `src/utils/config.py` 中扩展 `GameMode` 枚举（已存在，需确认）：

```python
class GameMode(Enum):
    OPEN_WORLD = "open_world"            # 原修仙模式
    THOUSAND_ILLUSIONS = "thousand_illusions" # 千幻无情道
    MODERN_ROMANCE = "modern_romance"    # 现代都市恋爱
```

**配置路径适配**:
- 新架构使用 `src/config/data_paths.py` 注入用户数据目录
- 现代模式配置路径通过 `load_config()` 中的模式检测动态调整到 `static/game_configs/modern/`

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
    *   定义现代性格标签：傲娇, 腹黑, 治愈系, 社恐, E人, 捞女, 海王。

### 3.3 角色数据模型扩展 (src/classes/core/avatar)

**架构更新**: Avatar mixin 已移动到 `src/classes/core/avatar/`

创建 `src/classes/core/avatar/modern_mixin.py`，实现 `ModernProfileMixin`：

```python
@dataclass
class ModernProfileMixin:
    # --- 基础属性 ---
    occupation: str          # 职业
    education: str           # 学历
    mbti: str               # MBTI
    hobbies: List[str]      # 兴趣
    fashion_style: str      # 穿衣风格
    
    # --- 动态状态 ---
    energy: int = 100        # 精力 (每日行动点数)
    stress: int = 0          # 压力
    mood: int = 50           # 心情
    assets: int = 0          # 资产 (现金流)
    
    # --- 隐藏性格属性 (Hidden Traits) ---
    sincerity: int = 80      # 真实度 (0-100). <40 易触发背叛/欺骗
    hidden_archetype: Optional[str] = None # 隐藏原型: GOLD_DIGGER, NPD, SCAMMER, PLAYER, PUA, MOOCHER
    
    # --- 恋爱状态 ---
    relationship_status: str 
    relationships: Dict[str, dict] # 记录详细状态 (affection, stage, exclusivity)
    
    def get_relationship_stage(self, target) -> RelationshipStage:
        """根据好感度计算关系阶段 (Stranger -> Friend -> Crush -> Lover)"""
        pass
```

### 3.4 模拟循环与时间系统 (src/sim/simulator_engine)

**架构更新**: Simulator 已重构为 `src/sim/simulator_engine/simulator.py`，使用相位分离架构

*   **时间粒度调整**:
    *   修仙模式：`step()` (每月一次循环)。
    *   恋爱模式：`step_modern()` (每日/小时循环)，通过配置 `ticks_per_year` 动态调整时间粒度。
*   **日程系统 (Schedule System)**:
    *   每个 NPC 生成每日日程表（例如：9:00-18:00 工作，19:00-21:00 健身）。
    *   玩家选择地点移动，如果地点与 NPC 日程重合，触发"“偶遇”事件。

### 3.5 互动系统 (Interaction System)

**架构更新**: 现代社交系统已实现为 `src/classes/modern/social_system.py`

新增 `src/classes/modern/social_system.py`:

*   **Chat Engine (聊天引擎)**:
    *   生成微信/短信风格的对话。
    *   Prompt 需包含：当前好感度、历史话题、双方心情、潜台词指令。
*   **Dating Engine (约会引擎)**:
    *   处理约会邀请、场景选择、突发事件（如遇到熟人）。
    *   结算：根据约会表现更新好感度和依赖度。
*   **Risk Engine (风险/修罗场引擎)**:
    *   **每日检测**: 针对每个有互动的 NPC 进行风险判定。
    *   **负面原型 (Archetype Events)**:
        *   **男性主角挑战**: 捞女 (GOLD_DIGGER) 索取、NPD 打压、情感诈骗 (SCAMMER) 破财。
        *   **女性主角挑战**: 海王 (PLAYER) 假性分手、PUA 控制、软饭男 (MOOCHER) 吸血。
    *   **多线冲突 (Harem Conflict)**:
        *   **安全区**: 陌生人/朋友阶段，允许无限多线接触。
        *   **危险区**: 暧昧/恋人阶段 (Affection > 60)，触发排他性检查。
        *   **惩罚**: 若在危险区被发现多线操作，触发“修罗场爆发”，导致巨额压力增加和好感清零。

---

## 4. 实施步骤清单

### 阶段一：环境与数据准备
1.  [x] 创建分支 `feat/modern-romance`。
2.  [x] 建立 `static/game_configs/modern/` 目录，创建基础的城市、组织、物品 CSV 模板。
3.  [x] 在 `src/utils/config.py` 中注册 `MODERN_ROMANCE` 模式（通过动态路径调整）。
4.  [x] 适配新架构：配置路径使用 `data_paths` 注入。

### 阶段二：角色与日程系统
1.  [x] 实现 `ModernProfileMixin` 并集成到 `Avatar` 类 (包含 Hidden Traits)。
    *   [x] **架构适配**: 移动到 `src/classes/core/avatar/modern_mixin.py`
2.  [x] 实现 `ScheduleGenerator`：基于职业和性格生成 NPC 的周日程表。
3.  [x] 改造 `Simulator`：在现代模式下切换为“日循环”逻辑，消耗 `energy` 执行行动。

### 阶段三：通讯与约会功能
1.  [x] 开发 `ChatManager` (src/classes/modern/social_system.py)：集成 LLM，支持生成"发送消息"和"回复消息"的内容。
    *   [x] 编写 `templates/modern_chat.txt` Prompt 模板。
2.  [x] 开发 `DateManager`：
    *   [x] 实现地点互动逻辑（花钱/花精力 -> 获得好感/属性）。
    *   [x] 实现邀约机制（成功率受好感度和心情影响）。
3.  [x] 开发 `SocialAppManager` (社交软件探险)：
    *   [x] 实现 `Swipe` (滑卡) 逻辑：基于概率生成随机 Encounter。
    *   [x] 实现遭遇类型生成：普通路人 / 精英男神女神 / 陷阱怪 (照骗, 杀猪盘)。
    *   [x] 实现破冰机制：首轮对话判定是否获得联系方式。

### 阶段四：风险与修罗场系统 (Risk & Conflict)
1.  [x] 实现 `RelationshipRiskEngine` 基础框架。
    *   [x] **架构适配**: 移动到 `src/classes/modern/risk_engine.py`
2.  [x] 实现多线冲突检测 (`_check_harem_conflict`)：安全区 vs 危险区逻辑。
3.  [x] 完善负面原型逻辑 (Archetype Logic)：
    *   [x] **通用**: 实现 `Sincerity` (真实度) 对互动成功率的影响。
    *   [x] **男性主角剧本**:
        *   [x] 实现 `GOLD_DIGGER` (捞女) 索取事件。
        *   [x] 实现 `NPD` (自恋型) 打压/煤气灯效应事件。
        *   [x] 实现 `SCAMMER` (诈骗) 破财事件。
    *   [x] **女性主角剧本**:
        *   [x] 实现 `PLAYER` (海王) 暧昧/失踪事件。
        *   [x] 实现 `PUA` (控制狂) 精神控制事件 (降低 Confidence/Charm)。
        *   [x] 实现 `MOOCHER` (软饭男) 借钱/依赖事件。
4.  [x] 实现情感博弈机制 (Emotional Dynamics)：
    *   [x] **爱的滋养**: 真正爱你的 NPC 提供精力/心情恢复 (Nourishment)。
    *   [x] **吃的亏**: 负面互动导致属性永久下降或状态异常 (Suffering)。
5.  [x] 编写突发事件库 (`static/game_configs/modern/events.json`)。

### 阶段五：UI 与体验适配 (Web/Frontend)
**架构适配**: 前端已重构为使用 composables 架构

1.  [x] 前端增加"手机"界面：用于显示聊天记录、朋友圈。
    *   [x] **架构适配**: PhonePanel 组件已集成到 `web/src/components/game/panels/modern/PhonePanel.vue`
2.  [x] 调整主界面布局：显示精力条、金钱、日程表。
    *   [x] **架构适配**: ModernStats 组件已集成到 StatusBar
3.  [x] 增加"社交软件" App 界面：
    *   [x] 实现卡片滑动交互 (Swipe Left/Right)。
    *   [x] 显示匹配对象的资料卡 (Avatar, Tags, Distance)。

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

## 6. 架构适配说明 (2026 更新)

**新 main 分支架构适配**：

### 6.1 Simulator 重构
- **旧架构**: `src/sim/simulator.py` 单文件实现
- **新架构**: `src/sim/simulator_engine/simulator.py` 使用相位分离架构
- **适配**: 现代模式通过 `step_modern()` 方法实现小时级时间步进，与修仙模式的月级步进共存

### 6.2 Avatar 类重构
- **旧架构**: Avatar mixin 在 `src/classes/avatar/`
- **新架构**: Avatar mixin 移动到 `src/classes/core/avatar/`
- **适配**: `ModernProfileMixin` 已移动到 `src/classes/core/avatar/modern_mixin.py`

### 6.3 Server 端重构
- **旧架构**: `src/server/main.py` 直接定义 API 端点
- **新架构**: 使用 `src/server/command_handlers.py` 创建命令处理器
- **适配**: 现代模式相关功能需要通过 command_handlers 模式集成，而非直接在 main.py 中添加路由

### 6.4 配置系统重构
- **旧架构**: 配置路径硬编码在 `static/`
- **新架构**: 使用 `src/config/data_paths.py` 注入用户数据目录
- **适配**: 现代模式配置路径通过 `load_config()` 中的模式检测动态调整

### 6.5 前端架构重构
- **旧架构**: 直接在组件中管理状态
- **新架构**: 使用 composables (`useAppShell`, `useSystemMenuFlow`, `useSidebarResize`)
- **适配**: PhonePanel 和 ModernStats 组件已集成到新架构中

### 6.6 待完成项 (Rebase 后需补充)

由于 rebase 时跳过了部分提交，以下功能需要重新实现或适配新架构：

1. **README.md 更新**: ✅ 已完成 - 在主 README.md 中添加了现代恋爱模式扩展说明
2. **modern_avatar.py**: ✅ 已完成 - 功能已合并到 `src/classes/core/avatar/modern_mixin.py`，无需单独文件
3. **Server API 集成**: ⏳ 待完成 - SocialAppManager 等功能需要通过 command_handlers 模式集成到 server 端
   - 当前状态：SocialAppManager 已导入到 main.py，但未通过 command_handlers 模式暴露 API
   - 需要添加：社交软件滑动、聊天发送、约会邀约等 API 端点
